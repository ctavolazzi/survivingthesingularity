-- Adds unsubscribe support to the waitlist table.
-- Run in the Supabase SQL Editor after 001_waitlist.sql.
-- Idempotent: safe to run more than once.

-- 1. Add unsubscribe token (unique per row, used in email link).
alter table public.waitlist
  add column if not exists unsubscribe_token uuid not null default gen_random_uuid();

-- 2. Add timestamp set when the user clicks the unsubscribe link.
alter table public.waitlist
  add column if not exists unsubscribed_at timestamptz;

-- 3. Index for fast token lookups (the unsubscribe endpoint queries by this).
create index if not exists waitlist_unsubscribe_token_idx
  on public.waitlist (unsubscribe_token);
