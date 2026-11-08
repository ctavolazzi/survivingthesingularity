-- Discord membership applications: a visitor fills out a short form to
-- request permanent access to the Discord community. Reviewed by hand
-- (update `status` directly in the table editor after deciding).
-- Run in the Supabase SQL Editor after 007_authors_edition_no_cap.sql.
-- Idempotent: safe to run more than once.

create table if not exists public.discord_applications (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  email text not null,
  answer text not null,
  status text not null default 'pending' check (status in ('pending', 'accepted', 'rejected')),
  created_at timestamptz not null default now()
);

-- RLS: anonymous visitors may INSERT (submit an application) but never
-- SELECT/UPDATE/DELETE. Review happens via the Supabase dashboard directly.
alter table public.discord_applications enable row level security;

drop policy if exists "anon_insert_discord_applications" on public.discord_applications;
create policy "anon_insert_discord_applications" on public.discord_applications
  for insert to anon
  with check (true);

grant insert on public.discord_applications to anon;
