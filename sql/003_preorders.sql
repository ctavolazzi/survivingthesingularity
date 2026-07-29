-- Book preorders table: tracks both regular and author's-edition preorders.
-- Run in the Supabase SQL Editor after 002_waitlist_unsubscribe.sql.
-- Idempotent: safe to run more than once.

create table if not exists public.preorders (
  id               uuid        default gen_random_uuid() primary key,
  email            text        not null,
  name             text        not null default '',
  edition_type     text        not null default 'regular'
                               check (edition_type in ('regular', 'authors')),
  copy_number      int,        -- null for regular; 1-100 for author's edition
  status           text        not null default 'pending'
                               check (status in ('pending', 'confirmed', 'fulfilled', 'cancelled')),
  source           text        not null default 'launch-page',
  honeypot_flag    boolean     not null default false,
  created_at       timestamptz not null default now(),
  constraint preorders_email_edition_unique unique (email, edition_type)
);

-- Auto-assign the next copy_number for author's edition on insert.
-- Enforces the 100-copy limit at the database level.
create or replace function public.assign_authors_copy_number()
returns trigger language plpgsql as $$
declare
  next_num int;
begin
  if new.edition_type = 'authors' then
    select coalesce(max(copy_number), 0) + 1
      into next_num
      from public.preorders
     where edition_type = 'authors';

    if next_num > 100 then
      raise exception 'SOLD_OUT' using hint = 'All 100 author''s edition copies have been claimed.';
    end if;

    new.copy_number := next_num;
  end if;
  return new;
end;
$$;

drop trigger if exists trg_assign_authors_copy_number on public.preorders;
create trigger trg_assign_authors_copy_number
  before insert on public.preorders
  for each row execute function public.assign_authors_copy_number();

-- RLS: anonymous visitors may INSERT but never SELECT/UPDATE/DELETE their own rows.
alter table public.preorders enable row level security;

drop policy if exists "anon_insert_preorders" on public.preorders;
create policy "anon_insert_preorders" on public.preorders
  for insert to anon
  with check (true);

grant insert on public.preorders to anon;

-- Public view: exposes only the aggregate counts (no PII) so the frontend
-- can show "X of 100 remaining" without needing the admin client.
create or replace view public.preorder_counts as
  select
    edition_type,
    count(*) filter (where status != 'cancelled') as claimed
  from public.preorders
  group by edition_type;

grant select on public.preorder_counts to anon;
