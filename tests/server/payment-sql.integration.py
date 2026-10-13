#!/usr/bin/env python3
"""Run the real payment migrations in disposable PostgreSQL 17 (Docker required).

Run from the repository root: python3 tests/server/payment-sql.integration.py
No ports, production credentials, or application/provider requests are used.
The fixture gives service_role Supabase-style default table privileges and RLS
bypass; it does not certify a hosted project's existing grants or PostgREST.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
NAME = "sts-payment-sql-" + uuid.uuid4().hex[:10]
ENV = {key: value for key, value in os.environ.items() if key not in
       {"DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_TLS", "DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH"}}
DOCKER = ["docker", "--host=unix:///var/run/docker.sock"]


def docker(*args, input=None, check=True):
    return subprocess.run(DOCKER + list(args), input=input, text=True,
                          capture_output=True, check=check, timeout=90, env=ENV)


def sql(statement, role=None, fail=False):
    if role:
        assert role in {"anon", "authenticated", "service_role"}
        statement = f"set role {role};\n" + statement
    result = docker("exec", "-i", NAME, "psql", "-U", "postgres", "-XqAt",
                    "-v", "ON_ERROR_STOP=1", input=statement, check=False)
    if fail:
        assert result.returncode != 0 and "permission denied" in result.stderr, result
    else:
        assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def expect(statement, expected, role=None):
    actual = sql(statement, role)
    assert actual == str(expected), (statement, actual, expected)


def rpc(statement):
    return json.loads(sql(statement, "service_role"))


def parallel(statement, count=8):
    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as pool:
        return list(pool.map(lambda _: rpc(statement), range(count)))


def migration(number):
    path, = ROOT.glob(f"sql/{number:03d}_*.sql")
    sql(path.read_text())


def check(label):
    print("PASS " + label, flush=True)


try:
    docker("run", "--rm", "--detach", "--name", NAME, "--network", "none",
           "-e", "POSTGRES_HOST_AUTH_METHOD=trust", "postgres:17")
    for _ in range(60):
        # The image's temporary initialization server only listens on a Unix
        # socket. Wait for TCP readiness so it cannot disappear mid-migration.
        if docker("exec", NAME, "pg_isready", "-h", "127.0.0.1", "-U", "postgres", check=False).returncode == 0:
            break
        time.sleep(0.25)
    else:
        raise RuntimeError("Disposable PostgreSQL did not become ready")
    print(sql("select version();"), flush=True)
    sql("""
      create role anon nologin; create role authenticated nologin;
      create role service_role nologin bypassrls;
      grant usage on schema public to anon, authenticated, service_role;
      alter default privileges in schema public grant all on tables to anon, authenticated, service_role;
      alter default privileges in schema public grant all on sequences to anon, authenticated, service_role;
    """)
    for number in range(1, 13):
        migration(number)
    sql("insert into public.fulfilled_sessions(session_id,email) values ('cs_legacy','legacy@example.test');")
    migration(13)
    expect("select status from public.fulfilled_sessions where session_id='cs_legacy';", "delivered")
    sql("insert into public.fulfilled_sessions(session_id,email) values ('cs_unfinished','new@example.test');")
    migration(13)
    expect("select status from public.fulfilled_sessions where session_id='cs_unfinished';", "claimed")
    migration(14)
    sql("""
      insert into public.checkout_transactions(session_id,status,fulfilled) values
        ('cs_reopen','completed',false),('cs_finished','completed',true),('cs_unpaid','initiated',false);
      insert into public.webhook_events(event_id,type,session_id,status,completed_at) values
        ('evt_reopen','checkout.session.completed','cs_reopen','processed',now()),
        ('evt_finished','checkout.session.completed','cs_finished','processed',now()),
        ('evt_unpaid','checkout.session.completed','cs_unpaid','processed',now());
    """)
    migration(17)
    check("migrations 001–014 and 017 execute; 013 replay preserves unfinished claims")
    expect("select status from public.webhook_events where event_id='evt_reopen';", "failed")
    expect("select count(*) from public.webhook_events where event_id in ('evt_finished','evt_unpaid') and status='processed';", "2")
    expect("select completed_at is null from public.webhook_events where event_id='evt_reopen';", "t")
    check("017 reopens only previously acknowledged, locally paid and unfulfilled events")

    for role in ("anon", "authenticated"):
        for statement in (
            "select public.claim_fulfillment_session('cs_forbidden','blocked@example.test');",
            "select public.reserve_checkout('blocked@example.test','standard');",
            "select * from public.find_preorder('blocked@example.test','standard');",
            "select * from public.checkout_reservations;",
            "insert into public.checkout_reservations(email,edition_type) values ('blocked@example.test','standard');",
            "select * from public.fulfilled_sessions;",
        ):
            sql(statement, role, fail=True)
    expect("select relrowsecurity from pg_class where oid='public.checkout_reservations'::regclass;", "t")
    expect("select count(*) from pg_policies where schemaname='public' and tablename='checkout_reservations';", "0")
    expect("select count(*) from public.checkout_reservations;", "0", "service_role")
    check("anon/authenticated cannot call payment RPCs or read/write protected records; service_role can")

    initial = rpc("select public.claim_fulfillment_session('cs_lease',' Buyer@Example.test ');")
    assert initial["state"] == "claimed" and initial["lease_token"]
    expect("select email from public.fulfilled_sessions where session_id='cs_lease';", "buyer@example.test")
    assert rpc("select public.claim_fulfillment_session('cs_lease','buyer@example.test');")["state"] == "in_flight"
    sql("update public.fulfilled_sessions set status='failed',last_error='fixture provider rejection' where session_id='cs_lease';", "service_role")
    retry = rpc("select public.claim_fulfillment_session('cs_lease','buyer@example.test');")
    assert retry["state"] == "claimed" and retry["lease_token"] != initial["lease_token"]
    expect("select attempts from public.fulfilled_sessions where session_id='cs_lease';", "2")
    expect("select last_error is null from public.fulfilled_sessions where session_id='cs_lease';", "t")
    sql("update public.fulfilled_sessions set lease_expires_at=now()-interval '1 second' where session_id='cs_lease';", "service_role")
    replacement = rpc("select public.claim_fulfillment_session('cs_lease','buyer@example.test');")
    assert replacement["state"] == "claimed" and replacement["lease_token"] != retry["lease_token"]
    expect(f"""with updated as (update public.fulfilled_sessions set status='delivered'
      where session_id='cs_lease' and lease_token='{retry['lease_token']}' and status='claimed'
      returning session_id) select count(*) from updated;""", "0", "service_role")
    expect(f"""with updated as (update public.fulfilled_sessions set status='delivered',lease_expires_at=null
      where session_id='cs_lease' and lease_token='{replacement['lease_token']}' and status='claimed'
      returning session_id) select count(*) from updated;""", "1", "service_role")
    assert rpc("select public.claim_fulfillment_session('cs_lease','buyer@example.test');")["state"] == "already_delivered"
    check("fresh/in-flight/failed/stale/delivered lease transitions and fenced outcome writes")

    claims = parallel("select public.claim_fulfillment_session('cs_race','race@example.test');")
    assert sum(row["state"] == "claimed" for row in claims) == 1, claims
    assert sum(row["state"] == "in_flight" for row in claims) == 7, claims
    sql("update public.fulfilled_sessions set lease_expires_at=now()-interval '1 second' where session_id='cs_race';")
    reclaimed = parallel("select public.claim_fulfillment_session('cs_race','race@example.test');")
    assert sum(row["state"] == "claimed" for row in reclaimed) == 1, reclaimed
    assert sum(row["state"] == "in_flight" for row in reclaimed) == 7, reclaimed
    check("eight concurrent initial claims and eight stale repairs each produce one owner")

    reservations = parallel("select public.reserve_checkout(' Buyer@Example.test ','standard');")
    original_key = reservations[0]["reservation_key"]
    assert {row["reservation_key"] for row in reservations} == {original_key}
    expect("select email from public.checkout_reservations;", "buyer@example.test")
    sql("update public.checkout_reservations set session_id='cs_expired' where email='buyer@example.test';", "service_role")
    assert rpc("select public.reserve_checkout('buyer@example.test','standard','cs_wrong');")["reservation_key"] == original_key
    rotated = parallel("select public.reserve_checkout('buyer@example.test','standard','cs_expired');")
    new_key = rotated[0]["reservation_key"]
    assert new_key != original_key and {row["reservation_key"] for row in rotated} == {new_key}
    expect(f"""with updated as (update public.checkout_reservations set session_id='cs_stale'
      where email='buyer@example.test' and edition_type='standard' and reservation_key='{original_key}'
      returning session_id) select count(*) from updated;""", "0", "service_role")
    check("eight concurrent checkout requests share one key; eight expiry rotations rotate once; stale attachment blocked")

    sql("""insert into public.preorders(email,edition_type,discount_code) values
      (' A_B@Example.test ','standard','EXACT1'),('axb@example.test','standard','EXACT2');""", "service_role")
    expect("select discount_code from public.find_preorder('a_b@example.test','standard');", "EXACT1", "service_role")
    expect("select count(*) from public.find_preorder('a%b@example.test','standard');", "0", "service_role")
    check("historical mixed-case/whitespace ownership lookup is exact, with no SQL wildcard expansion")

    migration(17)
    expect("select reservation_key from public.checkout_reservations where email='buyer@example.test';", new_key)
    expect("select lease_token from public.fulfilled_sessions where session_id='cs_lease';", replacement["lease_token"])
    sql("update public.fulfilled_sessions set created_at=now()-interval '40 days' where session_id='cs_legacy';")
    sql("select public.delete_old_fulfilled_sessions();")
    expect("select count(*) from public.fulfilled_sessions where session_id='cs_legacy';", "1")
    check("017 is replayable and preserves completed receipt/idempotency records beyond 30 days")
    print("All 8 PostgreSQL integration groups passed.", flush=True)
finally:
    docker("rm", "--force", NAME, check=False)
