-- Migration 005: Author's Edition copy-number race fix
-- Run in the Supabase SQL Editor after 004_fulfilled_sessions.sql.
-- Idempotent: safe to run more than once.
--
-- Problem: the BEFORE INSERT trigger in 003 does:
--   select coalesce(max(copy_number), 0) + 1
-- with no unique constraint and no serialization. Two concurrent author's-edition
-- inserts can both read the same max() and claim the same copy number, or both
-- slip past the > 100 check and oversell the edition.
--
-- Fix (belt + suspenders):
--   1. pg_advisory_xact_lock serializes the read+assign so concurrent inserts
--      queue and each reads the committed max (suspenders — prevents the race).
--   2. UNIQUE (edition_type, copy_number) is a hard failsafe that errors loudly
--      (23505) instead of silently duplicating (belt — survives any edge case).

-- Belt: unique constraint on the assigned copy number.
-- IF NOT EXISTS keeps this idempotent.
alter table public.preorders
  add constraint if not exists preorders_edition_copy_unique
  unique (edition_type, copy_number);

-- Suspenders: replace the trigger function to acquire a transaction-scoped
-- advisory lock before reading max(). The lock is released automatically
-- when the transaction commits or rolls back, so concurrent inserts queue up
-- and each sees the fully committed state before picking the next number.
create or replace function public.assign_authors_copy_number()
returns trigger language plpgsql as $$
declare
  next_num int;
begin
  if new.edition_type = 'authors' then
    perform pg_advisory_xact_lock(hashtext('authors_copy'));

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
