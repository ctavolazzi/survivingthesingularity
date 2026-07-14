-- Migration 009: per-customer launch discount code.
-- Every preorder gets its own unique code, stored here and echoed back in the
-- confirmation email, alongside the shared "PREORDER50" Stripe promotion code
-- (created directly in the Stripe dashboard/API, not tracked in this table).
-- The personal code is proof-of-preorder; the master code is what Stripe
-- actually redeems for the 50% discount at the future book checkout.
-- Run in the Supabase SQL Editor after 008_discord_applications.sql.
-- Idempotent: safe to run more than once.

alter table public.preorders
  add column if not exists discount_code text;

drop index if exists preorders_discount_code_unique;
create unique index preorders_discount_code_unique
  on public.preorders (discount_code)
  where discount_code is not null;
