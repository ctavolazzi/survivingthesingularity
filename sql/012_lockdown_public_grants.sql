-- Migration 012: take the public API key out of the database entirely.
-- Run in the Supabase SQL Editor. Idempotent: safe to run more than once.
--
-- WHY THIS EXISTS
--
-- Probed against production on 2026-07-28 with the publishable key:
--
--   POST /rest/v1/waitlist   {}  -> 400 23502 (null value in column "email")
--   POST /rest/v1/preorders  {}  -> 400 23502 (null value in column "email")
--
-- A 23502 is a *constraint* rejection, which means the request had already
-- cleared both the table grant and the RLS policy. The public key could write.
-- The control - the same request against discord_applications - returned
-- 401 42501, which is what a properly locked table looks like.
--
-- That came from 001 and 003, which each did:
--
--   create policy "anon_insert_..." ... for insert to anon with check (true);
--   grant insert on public.<table> to anon;
--
-- That was deliberate once: the browser posted signups straight to PostgREST.
-- It is no longer true. Every write now goes through a server endpoint using
-- the service role (57bd124 moved the last one, /api/waitlist). The grant
-- outlived the design that needed it.
--
-- WHAT THE OPEN GRANT ACTUALLY BOUGHT AN ATTACKER
--
-- Not spam. `preorders` is the redundancy against Stripe, and it carries
-- `unique (email, edition_type)`. Demonstrated end-to-end against production
-- and then cleaned up:
--
--   1. insert {email: victim, edition_type: 'standard'} with the public key -> 201
--   2. the real fulfillment path inserts the same pair as service_role    -> 409 23505
--
-- Step 2 is what fulfillPreorder() does when a customer actually pays. It
-- reads that 23505 as `violatedConstraint() === 'email'`, sets `duplicate =
-- true`, and `duplicate` is precisely what suppresses the admin alert
-- (fulfillment.js: `if (!duplicate) sends.push(sendAdminPreorderAlert...)`).
--
-- So a pre-planted row makes a genuine paid order vanish from the table that
-- exists to survive Stripe going down, sends the customer a confirmation
-- carrying the attacker's copy_number and discount_code, and fires no alert.
-- Nobody finds out. One anonymous POST per targeted email address.
--
-- SCOPE NOTE, honestly stated: the publishable key is not currently published.
-- It is absent from the deployed bundle, from every tracked file, and from
-- git history - the only two modules that would ship it (stores/tacticLibrary,
-- stores/researchLinksStore) are orphans no route imports, and they query
-- `tactics` and `research_links`, which do not exist in this database. So the
-- attack above needs a key an attacker does not trivially have today. That is
-- not a defence. Supabase publishable keys are *designed* to be public, one
-- `import` re-publishes it, and a credential's confidentiality is not a
-- control. Fix the grant, not the exposure.

begin;

-- 1. Drop the permissive policies. Named explicitly rather than looped over
--    pg_policies so this migration cannot quietly delete a policy someone adds
--    later for a good reason - a blind "drop every policy on this table" is how
--    a future intentional rule disappears without a diff.
drop policy if exists "anon_insert_waitlist"  on public.waitlist;
drop policy if exists "anon_insert_preorders" on public.preorders;

-- 2. RLS on everywhere. Already true for all five, asserted anyway so a table
--    restored from an older dump cannot come back with it off. RLS *on* with no
--    policy is deny-all for anon and authenticated; service_role bypasses it.
alter table public.waitlist             enable row level security;
alter table public.preorders            enable row level security;
alter table public.fulfilled_sessions   enable row level security;
alter table public.discord_applications enable row level security;

-- email_deliveries only exists once 011 has run. Guarded so 012 is runnable in
-- either order rather than aborting the whole transaction on a missing table.
do $$
begin
  if to_regclass('public.email_deliveries') is not null then
    execute 'alter table public.email_deliveries enable row level security';
    execute 'revoke all on public.email_deliveries from anon, authenticated';
  else
    raise notice '011_email_deliveries.sql has not run yet - skipping that table.';
  end if;
end $$;

-- 3. Revoke the grants themselves, not just the policies.
--
--    This is the part that matters and the part that is easy to skip. RLS and
--    grants are two independent gates. Supabase ships `grant all on all tables
--    in schema public to anon, authenticated`, so these three tables are today
--    protected *only* by RLS - one policy deep. Add one permissive `for all`
--    policy by accident, or restore a table with RLS off, and the grants are
--    still sitting there waiting. Revoking means the next mistake fails closed.
revoke all on public.waitlist             from anon, authenticated;
revoke all on public.preorders            from anon, authenticated;
revoke all on public.fulfilled_sessions   from anon, authenticated;
revoke all on public.discord_applications from anon, authenticated;

-- 4. The aggregate view. `preorder_counts` was granted to anon in 003 so the
--    frontend could render "X of 100 claimed" without the admin client.
--    Verified 2026-07-28: nothing reads it. Not one reference in src/ - the
--    only mention left in the repo is a line in docs/ARCHITECTURE.md. It is a
--    live RLS bypass (a view executes as its owner, so selecting it reads
--    `preorders` past that table's policies) kept alive for a caller that no
--    longer exists.
revoke all on public.preorder_counts from anon, authenticated;

-- Belt to that suspenders: make the view run as the caller, so if it is ever
-- re-granted it can no longer launder a read around RLS. Postgres 15+; wrapped
-- so an older server logs and continues instead of failing the migration.
do $$
begin
  execute 'alter view public.preorder_counts set (security_invoker = on)';
exception when others then
  raise notice 'could not set security_invoker on preorder_counts (%), continuing.', sqlerrm;
end $$;

-- 5. Future tables. The real lesson from 001/003 is not that someone granted
--    anon too much - it is that the *default* is generous, so the next table
--    created in the dashboard arrives pre-granted to anon and is protected only
--    by whether whoever made it remembered to enable RLS. Change the default.
--
--    Trade-off, stated plainly: after this, a new table is unreachable by the
--    public key until you grant it explicitly. That is the intended direction
--    for this project, where 100% of database access is server-side through the
--    service role. If you later want a genuinely public table, grant it by name.
--    Per-role exception handling is load-bearing, not defensive padding. The
--    SQL Editor connects as `postgres`, and `supabase_admin` is a Supabase-owned
--    superuser that `postgres` may not alter - so the naive version of this loop
--    raises 42501 and, because everything above runs in one transaction, rolls
--    the entire lockdown back. Observed on 2026-07-28 against this project.
--    Existence of a role does not imply permission over it. Catching per role
--    means the grant we can change still gets changed.
--
--    `postgres` is the one that matters: it owns tables created from the
--    dashboard and the SQL Editor, so its defaults govern the next table
--    somebody makes. `supabase_admin` is belt-and-braces and is expected to skip.
do $$
declare r text;
begin
  foreach r in array array['postgres', 'supabase_admin'] loop
    if exists (select 1 from pg_roles where rolname = r) then
      begin
        execute format(
          'alter default privileges for role %I in schema public revoke all on tables from anon, authenticated', r);
        execute format(
          'alter default privileges for role %I in schema public revoke all on sequences from anon, authenticated', r);
        execute format(
          'alter default privileges for role %I in schema public revoke all on functions from anon, authenticated', r);
      exception when insufficient_privilege then
        raise notice 'no permission to change default privileges for role % - skipping, continuing.', r;
      end;
    end if;
  end loop;
end $$;

commit;

-- ---------------------------------------------------------------------------
-- VERIFY. Run this after the commit above; every row should read GRANTS: none.
-- ---------------------------------------------------------------------------
select
  c.relname                                                as object,
  case c.relkind when 'r' then 'table' when 'v' then 'view' else c.relkind::text end as kind,
  c.relrowsecurity                                         as rls_enabled,
  coalesce((select count(*) from pg_policies p
             where p.schemaname = 'public' and p.tablename = c.relname), 0) as policies,
  coalesce(nullif(array_to_string(array(
    select distinct a.privilege_type
      from information_schema.role_table_grants a
     where a.table_schema = 'public'
       and a.table_name   = c.relname
       and a.grantee in ('anon', 'authenticated')
     order by 1), ', '), ''), 'none')                      as anon_grants
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind in ('r', 'v')
order by 1;
