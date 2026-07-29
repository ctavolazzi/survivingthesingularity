-- Migration 007: remove the 100-copy hard cap on the Author's Edition.
-- The site still markets it as "limited to 100 copies," but we're fine
-- overselling past that number rather than blocking a sale. Keeps the
-- advisory lock (still serializes concurrent inserts so copy numbers never
-- collide) and the unique constraint from 005, just drops the SOLD_OUT
-- exception above 100.
-- Run in the Supabase SQL Editor after 006_preorders_standard_edition.sql.
-- Idempotent: safe to run more than once.

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

    new.copy_number := next_num;
  END IF;
  RETURN new;
END;
$$;
