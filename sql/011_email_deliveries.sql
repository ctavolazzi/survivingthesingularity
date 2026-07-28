-- Migration 011: record whether each transactional email actually arrived.
-- Run in the Supabase SQL Editor. Idempotent: safe to run more than once.
--
-- WHY THIS EXISTS
--
-- Until now nothing recorded email outcomes. fulfillPreorder() fired the
-- download email and the admin alert, logged a failure to the console, and
-- moved on. A bounced confirmation and a delivered confirmation left the
-- database in exactly the same state, so "did this customer actually get
-- their bundle link?" was unanswerable from our own data. The only record was
-- Resend's dashboard, which is a third party and retains ~30 days.
--
-- That is the wrong shape for a table whose entire job is redundancy against
-- Stripe. This closes it: one row per send attempt, updated in place as
-- Resend reports what happened to it.
--
-- Two writers:
--   1. the send path, which inserts a row the moment a send is attempted
--      (status 'sent', or 'failed' when the API call itself errored), and
--   2. /api/webhooks/resend, which updates status as delivery events arrive.

create table if not exists public.email_deliveries (
  -- Resend's message id. Nullable because a send that fails at the API call
  -- never gets one, and we still want the attempt on the record - a failed
  -- send is precisely the case this table exists to make visible.
  -- Postgres allows many NULLs under a unique constraint, so those rows
  -- coexist fine while real ids stay unique. The webhook upserts on this.
  message_id    text unique,

  id            uuid primary key default gen_random_uuid(),
  to_email      text not null,

  -- Which email this was, so a bounced admin alert is not mistaken for a
  -- customer never receiving their bundle.
  email_type    text not null,

  -- The Stripe session for fulfillment emails, so a delivery outcome can be
  -- joined straight back to the order it belongs to. Null for welcome and
  -- checklist emails, which have no session.
  session_id    text,

  status        text not null default 'sent',
  error         text,
  created_at    timestamptz not null default now(),
  last_event_at timestamptz not null default now(),

  -- Constrained on purpose. A typo'd status silently breaks every "who did
  -- not get their email" query, and that query is the reason for the table.
  -- These are Resend's event names plus 'failed' for send-time errors.
  constraint email_deliveries_status_check check (status in (
    'sent', 'delivered', 'delivery_delayed', 'bounced', 'complained',
    'opened', 'clicked', 'failed'
  ))
);

-- "Show me everyone whose fulfillment email did not make it" - the query this
-- table exists to answer - filters on status and reads newest first.
create index if not exists email_deliveries_status_idx
  on public.email_deliveries (status, created_at desc);

-- Per-customer history: "did this person ever actually receive anything?"
create index if not exists email_deliveries_to_email_idx
  on public.email_deliveries (to_email);

-- Join back to the order.
create index if not exists email_deliveries_session_id_idx
  on public.email_deliveries (session_id)
  where session_id is not null;

-- RLS on with no policies: deny-all for anon and authenticated, exactly like
-- discord_applications and fulfilled_sessions. Only the service role touches
-- this table, and it bypasses RLS. This holds customer email addresses and
-- must never be reachable with the public key that ships to browsers.
alter table public.email_deliveries enable row level security;

revoke all on public.email_deliveries from anon, authenticated;
