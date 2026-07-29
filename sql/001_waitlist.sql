-- Waitlist table for email capture (newsletter + book-release notifications).
-- Run in the Supabase SQL Editor (or via `supabase db push` once linked).
-- Idempotent: safe to run more than once.

create table if not exists public.waitlist (
  id uuid default gen_random_uuid() primary key,
  email text not null,
  source text not null default 'homepage',
  newsletter_consent boolean not null default false,
  book_release_consent boolean not null default false,
  created_at timestamptz default now() not null,
  constraint waitlist_email_unique unique (email)
);

-- If the table predates the consent columns, add them.
alter table public.waitlist
  add column if not exists newsletter_consent boolean not null default false,
  add column if not exists book_release_consent boolean not null default false;

-- RLS: anonymous visitors may INSERT (sign up) but never SELECT/UPDATE/DELETE.
alter table public.waitlist enable row level security;

drop policy if exists "anon_insert_waitlist" on public.waitlist;
create policy "anon_insert_waitlist" on public.waitlist
  for insert to anon
  with check (true);

grant insert on public.waitlist to anon;
