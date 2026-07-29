-- Tracks Stripe sessions that have already had their download email sent.
-- Used to prevent duplicate emails when a user refreshes the success page.
-- Run in the Supabase SQL Editor after 003_preorders.sql.
-- Idempotent: safe to run more than once.

create table if not exists public.fulfilled_sessions (
  session_id  text        primary key,
  email       text,
  created_at  timestamptz not null default now()
);

-- Service role only — no anon access needed.
alter table public.fulfilled_sessions enable row level security;

-- Clean up old records after 30 days (Stripe sessions expire in 24h anyway).
create or replace function public.delete_old_fulfilled_sessions()
returns void language sql as $$
  delete from public.fulfilled_sessions
  where created_at < now() - interval '30 days';
$$;
