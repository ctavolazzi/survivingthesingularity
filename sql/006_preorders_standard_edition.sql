-- Migration 006: rename the non-author edition_type value from 'regular' to
-- 'standard' to match the app's vocabulary (UI copy, Stripe metadata, and
-- email templates all say "Standard Edition" / "standard").
-- Run in the Supabase SQL Editor after 005_preorders_copy_lock.sql.
-- Idempotent: safe to run more than once.

-- Backfill any existing 'regular' rows before the constraint stops accepting it.
UPDATE public.preorders SET edition_type = 'standard' WHERE edition_type = 'regular';

ALTER TABLE public.preorders ALTER COLUMN edition_type SET DEFAULT 'standard';

ALTER TABLE public.preorders DROP CONSTRAINT IF EXISTS preorders_edition_type_check;
ALTER TABLE public.preorders
  ADD CONSTRAINT preorders_edition_type_check
  CHECK (edition_type IN ('standard', 'authors'));
