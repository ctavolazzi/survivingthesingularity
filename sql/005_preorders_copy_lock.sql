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

-- Belt: unique constraint (idempotent via DO block — ADD CONSTRAINT IF NOT EXISTS
-- is not valid PostgreSQL syntax).
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'preorders_edition_copy_unique'
      AND conrelid = 'public.preorders'::regclass
  ) THEN
    ALTER TABLE public.preorders
      ADD CONSTRAINT preorders_edition_copy_unique
      UNIQUE (edition_type, copy_number);
  END IF;
END $$;

-- Suspenders: replace the trigger function to acquire a transaction-scoped
-- advisory lock before reading max(). The lock is released automatically
-- when the transaction commits or rolls back, so concurrent inserts queue up
-- and each sees the fully committed state before picking the next number.
CREATE OR REPLACE FUNCTION public.assign_authors_copy_number()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
  next_num int;
BEGIN
  IF new.edition_type = 'authors' THEN
    PERFORM pg_advisory_xact_lock(hashtext('authors_copy'));

    SELECT coalesce(max(copy_number), 0) + 1
      INTO next_num
      FROM public.preorders
     WHERE edition_type = 'authors';

    IF next_num > 100 THEN
      RAISE EXCEPTION 'SOLD_OUT' USING HINT = 'All 100 author''s edition copies have been claimed.';
    END IF;

    new.copy_number := next_num;
  END IF;
  RETURN new;
END;
$$;
