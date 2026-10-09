-- Migration 014: an audit trail for every Stripe webhook event, and the row
-- that makes a replayed event recognisable. Plan items B-08 and B-06.
--
-- Run in the Supabase SQL Editor. Idempotent: safe to run more than once.
-- Purely additive, one new table, so it can be applied before the code that
-- uses it ships without breaking the deployment currently serving traffic.
--
-- WHY THIS EXISTS
--
-- 1. B-08. Nothing anywhere recorded `event.id`. An identical signed payload
--    replayed twice returned 200 both times and left no trace that it had been
--    seen before. Session-level protection did already exist (claimSession's
--    unique constraint on fulfilled_sessions.session_id), so a replay did not
--    double-email a customer, but there was no record of the event itself and
--    therefore no way to answer "did Stripe deliver this, and what did we do
--    about it".
--
-- 2. B-06. On 2026-07-29 Stripe held 23 complete-and-paid sessions against 13
--    fulfilled_sessions rows. Ten paid sessions had no application row and
--    nothing noticed, because a webhook that never arrives runs no code that
--    could notice. All ten were test mode and no money was lost. Detection has
--    to come from comparing two records after the fact, which needs both
--    records to exist.
--
-- THE TRAP THIS TABLE IS DESIGNED AROUND, STATED LOUDLY
--
-- STRIPE REUSES THE SAME EVENT ID WHEN IT RETRIES. So `event_id` present must
-- NEVER be read as "already handled". That is precisely the bug migration 013
-- removed from fulfilled_sessions, where a row meant "began" and got read as
-- "done", and a crash between claim and send left a tombstone that turned every
-- Stripe retry into a no-op while a paid customer got nothing.
--
-- Hence `status` below, and hence the rule enforced in
-- src/lib/server/webhookEventPolicy.js: only 'processed' earns a skip.
-- 'processing' means in flight, 'failed' means retry it. A retry is the
-- delivery mechanism working, not a duplicate.

-- ---------------------------------------------------------------------------
-- 1. The event log
-- ---------------------------------------------------------------------------

create table if not exists public.webhook_events (
  -- Stripe's own event id (evt_...). Primary key rather than a surrogate,
  -- because "have we seen this exact event" is the only question this table is
  -- asked, and the unique violation on insert IS the detection mechanism.
  event_id      text        primary key,

  -- Kept even for event types we take no action on. An event type arriving that
  -- nothing handles is worth being able to see; those rows are marked
  -- 'processed' because handling them correctly meant doing nothing.
  type          text        not null,

  -- Whether this came from live mode. The store has only ever seen test-mode
  -- traffic, so this column is how the first real event becomes findable.
  livemode      boolean,

  -- The checkout session this event concerns, when it concerns one. Denormalised
  -- from the payload so the B-06 reconciliation can join against
  -- checkout_transactions without unpacking JSON.
  session_id    text,

  -- processing = we started handling it, outcome unknown. The dangerous state.
  -- processed  = handling finished, including "correctly did nothing".
  --              The ONLY state that earns a skip on redelivery.
  -- failed     = handling ran and something went wrong. Explicitly retryable.
  status        text        not null default 'processing'
                            check (status in ('processing', 'processed', 'failed')),

  -- Bumped each time a redelivery is allowed through to repair a prior attempt.
  -- A high count is the signal that something is wedged.
  attempts      int         not null default 1,
  last_error    text,

  -- Immutable: the first time this event id was ever seen. Kept separate from
  -- received_at because the staleness window needs "when did the CURRENT attempt
  -- start" while an audit trail needs "when did this first show up", and one
  -- column cannot answer both.
  first_seen_at timestamptz not null default now(),

  -- Reset each time an attempt begins. This is what the staleness check reads.
  received_at   timestamptz not null default now(),

  completed_at  timestamptz
);

-- "What has Stripe sent us lately", the ordinary audit read.
create index if not exists webhook_events_received_idx
  on public.webhook_events (received_at desc);

-- "Which events did we start and never finish" - the operational queue. Partial
-- so it stays small: the healthy state is for this index to be nearly empty.
create index if not exists webhook_events_unfinished_idx
  on public.webhook_events (status, received_at desc)
  where status <> 'processed';

-- Joining an event back to the checkout it belongs to, for B-06.
create index if not exists webhook_events_session_idx
  on public.webhook_events (session_id)
  where session_id is not null;

-- The first live-mode event ever received is a milestone worth being able to
-- find in one query rather than scanning.
create index if not exists webhook_events_livemode_idx
  on public.webhook_events (livemode, received_at desc)
  where livemode is true;

-- RLS on with no policies: deny-all for anon and authenticated, matching every
-- other table here. This holds payment references and must never be reachable
-- with the publishable key that ships to browsers.
alter table public.webhook_events enable row level security;
revoke all on public.webhook_events from anon, authenticated;

-- ---------------------------------------------------------------------------
-- 2. The reconciliation view behind B-06
-- ---------------------------------------------------------------------------

-- "Money arrived and the customer has nothing to show for it, and it has been
-- long enough that this is not just a race."
--
-- Deliberately a view and not a materialised one: it must never be able to
-- answer from a stale snapshot. A reconciliation report that is quietly out of
-- date is worse than no report, because it reads as an all-clear.
--
-- The 15 minute floor is not arbitrary. The success page and the webhook
-- routinely land within seconds of each other, and Stripe's own retry schedule
-- spaces attempts minutes apart, so anything tighter would alert on healthy
-- traffic mid-retry and train whoever receives it to ignore the alert.
create or replace view public.unreconciled_paid_sessions as
select
  t.session_id,
  t.email,
  t.name,
  t.edition_type,
  t.amount_total,
  t.currency,
  t.created_at                                       as paid_at,
  round(extract(epoch from (now() - t.created_at)) / 60)::int as minutes_outstanding,
  f.status                                           as fulfillment_status,
  f.last_error                                       as fulfillment_error,
  (f.session_id is null)                             as never_claimed,
  e.event_id                                         as webhook_event_id,
  e.status                                           as webhook_status
from public.checkout_transactions t
left join public.fulfilled_sessions f on f.session_id = t.session_id
left join public.webhook_events    e on e.session_id = t.session_id
where t.status = 'completed'
  and t.created_at < now() - interval '15 minutes'
  and (
    -- Nothing ever claimed it: the webhook probably never arrived.
    f.session_id is null
    -- Or it was claimed and never confirmed delivered.
    or f.status is distinct from 'delivered'
    -- Or our own ledger says fulfillment never ran.
    or t.fulfilled = false
  );

-- Views inherit no RLS of their own; lock the grant down explicitly so this
-- cannot be read with the anon key even though the tables beneath it are safe.
revoke all on public.unreconciled_paid_sessions from anon, authenticated;

-- ---------------------------------------------------------------------------
-- 3. Verification - run this and READ THE OUTPUT rather than assuming
-- ---------------------------------------------------------------------------

-- Expect: webhook_events with rls_enabled = true, policies = 0, anon_grants = none.
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
  and c.relname in ('webhook_events', 'checkout_transactions', 'fulfilled_sessions')
order by 1;

-- The B-06 backlog as it stands right now. On a healthy store this returns zero
-- rows. It is expected to return the historical test-mode gap on first run.
select count(*) as unreconciled_now from public.unreconciled_paid_sessions;
