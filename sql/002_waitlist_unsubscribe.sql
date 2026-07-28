-- Adds unsubscribe support to the waitlist table.
-- Run in the Supabase SQL Editor after 001_waitlist.sql.
-- Idempotent: safe to run more than once.

-- 1. Add the unsubscribe token used in the email link.
--    gen_random_uuid() is volatile, so adding the column rewrites the table and
--    every existing row gets its own value - the 8 rows already on the waitlist
--    are covered, not left null.
--    The index below is deliberately NOT unique. Uniqueness here would be
--    enforcement theatre: collision odds for random v4 UUIDs are negligible, and
--    a unique index would turn an impossible collision into a failed signup.
--    /api/unsubscribe already treats the token as a lookup key, not a claim of
--    uniqueness - it matches one row and updates it.
alter table public.waitlist
  add column if not exists unsubscribe_token uuid not null default gen_random_uuid();

-- 2. Add timestamp set when the user clicks the unsubscribe link.
alter table public.waitlist
  add column if not exists unsubscribed_at timestamptz;

-- 3. Index for fast token lookups (the unsubscribe endpoint queries by this).
create index if not exists waitlist_unsubscribe_token_idx
  on public.waitlist (unsubscribe_token);
