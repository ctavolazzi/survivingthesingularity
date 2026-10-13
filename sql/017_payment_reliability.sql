-- Apply after 013 and 014, before the launch-readiness code is deployed.
-- Additive, service-role-only. If replaying prerequisites, use this release's
-- corrected 013; older copies promote unfinished claims on every rerun.
begin;

alter table public.fulfilled_sessions
  add column if not exists lease_token uuid,
  add column if not exists lease_expires_at timestamptz;
alter table public.preorders
  add column if not exists payment_session_id text;
alter table public.checkout_transactions
  add column if not exists review_reason text;

-- Row locking serializes a webhook/return-page race and concurrent stale repairs.
-- The fencing token prevents an old worker from finishing a replacement's lease.
create or replace function public.claim_fulfillment_session(p_session_id text, p_email text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  claim public.fulfilled_sessions%rowtype;
  token uuid := gen_random_uuid();
begin
  insert into public.fulfilled_sessions(session_id, email, status, lease_token, lease_expires_at)
    values (p_session_id, lower(trim(p_email)), 'claimed', token, now() + interval '2 minutes')
    on conflict (session_id) do nothing;
  if found then
    return jsonb_build_object('state', 'claimed', 'lease_token', token);
  end if;

  select * into strict claim from public.fulfilled_sessions
    where session_id = p_session_id for update;
  if claim.status = 'delivered' then
    return jsonb_build_object('state', 'already_delivered');
  end if;
  if claim.status = 'claimed' and
     coalesce(claim.lease_expires_at, claim.created_at + interval '2 minutes') > now() then
    return jsonb_build_object('state', 'in_flight');
  end if;
  update public.fulfilled_sessions set
    status = 'claimed', lease_token = token,
    lease_expires_at = now() + interval '2 minutes',
    attempts = attempts + 1, completed_at = null, last_error = null
    where session_id = p_session_id;
  return jsonb_build_object('state', 'claimed', 'lease_token', token);
end;
$$;
revoke all on function public.claim_fulfillment_session(text, text) from public, anon, authenticated;
grant execute on function public.claim_fulfillment_session(text, text) to service_role;

-- Keep fulfilled-session idempotency records. Purging them made old receipt
-- links and manual Stripe replays resend an already completed fulfillment.
create or replace function public.delete_old_fulfilled_sessions()
returns void language plpgsql as $$ begin return; end; $$;

-- A reservation gives concurrent checkout requests the SAME Stripe idempotency
-- key. It is rotated only after Stripe confirms the previous session expired.
create table if not exists public.checkout_reservations (
  email text not null,
  edition_type text not null,
  reservation_key uuid not null default gen_random_uuid(),
  session_id text,
  created_at timestamptz not null default now(),
  primary key (email, edition_type)
);
alter table public.checkout_reservations enable row level security;
revoke all on public.checkout_reservations from public, anon, authenticated;
grant all on public.checkout_reservations to service_role;

create or replace function public.reserve_checkout(p_email text, p_edition_type text, p_expired_session text default null)
returns jsonb language plpgsql security definer set search_path = public as $$
declare reservation public.checkout_reservations%rowtype;
begin
  insert into public.checkout_reservations(email, edition_type)
    values (lower(trim(p_email)), p_edition_type) on conflict do nothing;
  select * into strict reservation from public.checkout_reservations
    where email = lower(trim(p_email)) and edition_type = p_edition_type for update;
  if p_expired_session is not null and reservation.session_id = p_expired_session then
    update public.checkout_reservations set reservation_key = gen_random_uuid(),
      session_id = null, created_at = now()
      where email = reservation.email and edition_type = reservation.edition_type
      returning * into reservation;
  end if;
  return to_jsonb(reservation);
end;
$$;
revoke all on function public.reserve_checkout(text, text, text) from public, anon, authenticated;
grant execute on function public.reserve_checkout(text, text, text) to service_role;

-- A non-wildcard, case-insensitive lookup also finds historical mixed-case
-- buyers without destructively merging their order history.
create or replace function public.find_preorder(p_email text, p_edition_type text)
returns setof public.preorders language sql stable security definer set search_path = public as $$
  select * from public.preorders
    where lower(trim(email)) = lower(trim(p_email)) and edition_type = p_edition_type
    order by created_at asc limit 1;
$$;
revoke all on function public.find_preorder(text, text) from public, anon, authenticated;
grant execute on function public.find_preorder(text, text) to service_role;

-- Older handlers marked delivery failures processed. Make a deliberate replay
-- of those paid-but-unfulfilled events useful; Stripe does not retry them just
-- because this state changes, so reconciliation must still trigger a replay.
update public.webhook_events e
  set status = 'failed', last_error = 'Reopened: paid fulfillment was not completed', completed_at = null
  from public.checkout_transactions t
  where e.session_id = t.session_id and e.status = 'processed'
    and e.type in ('checkout.session.completed', 'checkout.session.async_payment_succeeded')
    and t.status = 'completed' and t.fulfilled = false;

create index if not exists checkout_transactions_review_idx
  on public.checkout_transactions(created_at) where review_reason is not null;
commit;

-- Expected: all three functions callable only by owner and service_role;
-- checkout_reservations has RLS enabled with no public policies.
select proname, proacl from pg_proc where pronamespace = 'public'::regnamespace
  and proname in ('claim_fulfillment_session', 'reserve_checkout', 'find_preorder');
