-- Migration 008: Discord community application intake.
-- Run in the Supabase SQL Editor after 005_preorders_copy_lock.sql and before
-- 009_preorder_discount_code.sql.
-- Idempotent: safe to run more than once.
--
-- Backs the DiscordApplication form on /checklist, which POSTs to
-- /api/discord-application. Until this runs, that endpoint's insert fails with
-- PGRST205 and the route returns its "isn't wired up yet" 503 instead of
-- accepting applications.
--
-- Column widths mirror the limits the endpoint already enforces
-- (src/routes/api/discord-application/+server.js): name 120, email 254,
-- answer 2000. The endpoint truncates name/answer and rejects over-long
-- emails, so these checks should never be what rejects a real submission -
-- they exist so a future caller that skips validation fails loudly here
-- rather than silently storing a malformed row.

create table if not exists public.discord_applications (
  id         uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name       text not null check (char_length(name)   between 1 and 120),
  email      text not null check (char_length(email)  between 3 and 254),
  answer     text not null check (char_length(answer) between 1 and 2000)
);

-- Admin review queries read newest-first; applicant lookups go by email.
create index if not exists discord_applications_created_at_idx
  on public.discord_applications (created_at desc);

create index if not exists discord_applications_email_idx
  on public.discord_applications (email);

-- RLS on with no policies: the anon and authenticated roles get no access at
-- all. The only writer is /api/discord-application via supabaseAdmin (service
-- role), which bypasses RLS by design. Applications contain personal contact
-- details and free-text answers and are never read by the browser, so there is
-- no policy to add - leaving RLS off would expose the whole table to anon.
alter table public.discord_applications enable row level security;
