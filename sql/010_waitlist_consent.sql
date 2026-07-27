-- Migration 010: record the consent flags the signup form already collects.
-- Run in the Supabase SQL Editor. Idempotent: safe to run more than once.
--
-- Why this exists as 010 rather than a rebuilt 001: the live waitlist table
-- currently has exactly four columns (id, email, source, created_at), so the
-- consent columns that src/routes/api/waitlist/+server.js inserts have never
-- existed on this project. That endpoint catches the resulting 42703/PGRST204
-- and silently retries with an email-only row, so every consent choice a
-- visitor has ticked so far was captured by the UI and then dropped on the
-- floor. The form asks the question; nothing was recording the answer.
--
-- The column types are not guesswork - they are what the endpoint already
-- sends: `newsletter_consent` and `book_release_consent` are passed as JS
-- booleans (`body.newsletter_consent === true`).
--
-- Deliberately NULLABLE with no default. Existing rows predate consent
-- tracking, and NULL states that honestly: "we do not know what this person
-- agreed to." Defaulting them to false would assert they declined, and
-- defaulting to true would manufacture consent that was never given. Treat
-- NULL as "do not market to" until the person re-confirms.

alter table public.waitlist
  add column if not exists newsletter_consent boolean;

alter table public.waitlist
  add column if not exists book_release_consent boolean;

-- Marketing sends filter on these; the partial index keeps that lookup cheap
-- without indexing the NULL/false majority.
create index if not exists waitlist_newsletter_consent_idx
  on public.waitlist (email)
  where newsletter_consent is true;
