-- Migration 013: make a paid order impossible to lose silently.
--
-- Run in the Supabase SQL Editor. Idempotent: safe to run more than once.
-- Purely additive - one new table plus nullable columns on an existing one -
-- so it can be applied before the code that uses it ships, without breaking
-- the deployment currently serving traffic.
--
-- WHY THIS EXISTS
--
-- Two holes, both found by reading the pipeline against live data on
-- 2026-07-29.
--
-- 1. `fulfilled_sessions` recorded that fulfillment STARTED, never that it
--    FINISHED. `claimSession()` inserts the row first, then mints the download
--    URL, inserts the preorder and sends the emails. If anything between the
--    claim and the last send failed - a worker timeout, a deploy mid-flight, a
--    Resend outage - Stripe would retry, the claim would come back "already
--    taken", the webhook would answer 200, and the customer would receive
--    nothing. Nobody would ever find out. The row said "done" when it meant
--    "began".
--
-- 2. There was no transaction log at all. `preorders` carries no session id, no
--    payment intent, no amount, and its `status` column is 'pending' on every
--    row ever written, including delivered ones. Worse, the unique
--    (email, edition_type) constraint means a repeat purchase writes NO row -
--    live data showed 12 sessions producing 3 preorder rows. Those other 9
--    payments existed only in `fulfilled_sessions`, which ships with a
--    30-day delete function. At a thousand orders you could not answer "who
--    paid us, and when" from your own data.

-- ---------------------------------------------------------------------------
-- 1. Completion tracking on the claim table
-- ---------------------------------------------------------------------------

-- 'claimed'   = fulfillment started, outcome unknown. The dangerous state.
-- 'delivered' = every send for this session completed. Safe to skip on retry.
-- 'failed'    = fulfillment ran and something went wrong. Needs a human or a
--               retry; deliberately distinct from 'claimed' so a stuck row and
--               a known-bad row are not confused.
alter table public.fulfilled_sessions
  add column if not exists status       text        not null default 'claimed',
  add column if not exists completed_at timestamptz,
  add column if not exists attempts     int         not null default 1,
  add column if not exists last_error   text;

do $$
begin
  alter table public.fulfilled_sessions
    add constraint fulfilled_sessions_status_check
    check (status in ('claimed', 'delivered', 'failed'));
exception when duplicate_object then
  null;
end $$;

-- Existing rows predate this column. They were all fulfilled successfully as
-- far as anyone knows, and marking them 'claimed' would make them look stuck
-- forever in the "needs attention" query below.
update public.fulfilled_sessions
   set status = 'delivered', completed_at = created_at
 where status = 'claimed' and completed_at is null;

-- "Which paid orders started fulfillment and never finished?" - the question
-- this table could not answer before.
create index if not exists fulfilled_sessions_incomplete_idx
  on public.fulfilled_sessions (status, created_at desc)
  where status <> 'delivered';

-- The 30-day purge must never delete a row that is not confirmed delivered.
-- An unfinished order is exactly the thing worth keeping.
create or replace function public.delete_old_fulfilled_sessions()
returns void language sql as $$
  delete from public.fulfilled_sessions
   where created_at < now() - interval '30 days'
     and status = 'delivered';
$$;

-- ---------------------------------------------------------------------------
-- 2. The durable transaction log
-- ---------------------------------------------------------------------------

-- One row per checkout attempt, from the moment it is created through to
-- whatever became of it. Never purged. This is the ledger you reconcile
-- against Stripe, and unlike `preorders` it records repeat purchases, expiries
-- and abandonments rather than only the first successful order per address.
create table if not exists public.checkout_transactions (
  id             uuid        primary key default gen_random_uuid(),

  -- Stripe's checkout session id. Unique so the webhook and the success page
  -- can both upsert without racing, exactly like fulfilled_sessions.
  session_id     text        not null unique,

  -- Populated once Stripe reports payment. Null for sessions that were created
  -- and never paid, which is the whole point of recording them.
  payment_intent text,

  -- Null at creation: Stripe collects the email during checkout, so we do not
  -- know who this is until the session completes. An abandoned checkout is
  -- therefore genuinely anonymous, and that is a fact about the flow rather
  -- than a gap in the logging.
  email          text,
  name           text,

  edition_type   text        not null default 'standard',

  -- Money, in Stripe's minor units. Recorded so the ledger can be reconciled
  -- without calling the Stripe API for every historical order.
  amount_total   int,
  currency       text,

  -- initiated = we created the session; the customer may never pay
  -- completed = Stripe confirmed payment
  -- expired   = Stripe expired the session (the abandoned-checkout signal)
  -- failed    = payment was attempted and did not succeed
  status         text        not null default 'initiated'
                             check (status in ('initiated', 'completed', 'expired', 'failed')),

  -- Whether fulfillment ran for this transaction, kept separate from payment
  -- status on purpose: "they paid" and "they received it" are different
  -- questions and conflating them is how the original hole stayed invisible.
  fulfilled      boolean     not null default false,

  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

-- "What happened today", and the abandoned-checkout report.
create index if not exists checkout_transactions_status_idx
  on public.checkout_transactions (status, created_at desc);

-- Per-customer history across repeat purchases, which `preorders` cannot show.
create index if not exists checkout_transactions_email_idx
  on public.checkout_transactions (email)
  where email is not null;

-- "Paid but never fulfilled" - the query that catches a dropped order.
create index if not exists checkout_transactions_unfulfilled_idx
  on public.checkout_transactions (created_at desc)
  where status = 'completed' and fulfilled = false;

create or replace function public.touch_checkout_transactions_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

drop trigger if exists trg_touch_checkout_transactions on public.checkout_transactions;
create trigger trg_touch_checkout_transactions
  before update on public.checkout_transactions
  for each row execute function public.touch_checkout_transactions_updated_at();

-- RLS on with no policies: deny-all for anon and authenticated, matching every
-- other table here. This holds customer emails and payment references and must
-- never be reachable with the publishable key that ships to browsers.
alter table public.checkout_transactions enable row level security;
revoke all on public.checkout_transactions from anon, authenticated;

-- ---------------------------------------------------------------------------
-- 3. Verification - run and read the output rather than assuming
-- ---------------------------------------------------------------------------

select
  c.relname                as object,
  c.relrowsecurity         as rls_enabled,
  coalesce((select count(*) from pg_policies p
             where p.schemaname = 'public' and p.tablename = c.relname), 0) as policies,
  coalesce(nullif(array_to_string(array(
    select distinct a.privilege_type
      from information_schema.role_table_grants a
     where a.table_schema = 'public'
       and a.table_name   = c.relname
       and a.grantee in ('anon', 'authenticated')
     order by 1), ', '), ''), 'none') as anon_grants
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relname in ('checkout_transactions', 'fulfilled_sessions')
order by 1;
