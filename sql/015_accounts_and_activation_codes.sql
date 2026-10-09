-- Migration 015: accounts. Two doors in - a preorder email, or an activation code.
-- Run in the Supabase SQL Editor after 014_webhook_events.sql.
-- Idempotent: safe to run more than once.
--
-- WHY THIS EXISTS
--
-- fulfillment.js mints download links with `LINK_TTL = 60 * 60 * 24 * 7`. Seven
-- days after buying the book, a paying customer has no self-serve way back to
-- the thing they paid for; the only route is emailing a human. An account is the
-- durable answer to "let me back in", and it is the first thing on this site
-- that needs to know who someone is.
--
-- WHAT SHAPE THE AUTH HAS TO TAKE, AND WHY IT IS NOT THE USUAL ONE
--
-- The obvious Supabase pattern is a browser-side client holding a session and
-- RLS policies keyed to `auth.uid()`. Two things already in this repo rule that
-- out, and both were deliberate:
--
--   1. svelte.config.js omits supabase.co from `connect-src`, with a comment
--      saying every Supabase call happens server-side and the browser "must not
--      be permitted to" open one. A browser-side auth client needs exactly that
--      connection.
--
--   2. Migration 012 revoked every grant from `anon` AND `authenticated`, then
--      changed default privileges so new tables arrive unreachable by both. An
--      RLS-scoped `authenticated` client against these tables would see nothing,
--      by design.
--
-- So sessions live in httpOnly cookies, the server verifies them, and every read
-- and write here goes through the service role - the same path everything else
-- already uses. That means the tables below follow 012's posture rather than
-- carving an exception into it: RLS on, no grants, no policies.
--
-- THE SECURITY-DEFINER TRAP, STATED UP FRONT
--
-- This migration adds functions, which 012 did not have to think about. A
-- `security definer` function runs as its owner and Postgres grants EXECUTE to
-- `public` by default. Left alone, that is a hole shaped exactly like the one
-- 012 closed: a caller with the publishable key could invoke a function that
-- reads and mutates tables they have no grant on, laundering the access the same
-- way `preorder_counts` laundered a read around RLS. Every function below is
-- therefore revoked from `public, anon, authenticated` immediately after it is
-- created. That revoke is load-bearing, not tidiness.

begin;

-- ---------------------------------------------------------------------------
-- 1. profiles
-- ---------------------------------------------------------------------------
-- One row per authenticated user, keyed to Supabase's own `auth.users`. We keep
-- our own row rather than leaning on auth.users metadata because `access_source`
-- is our business logic, not the auth system's, and because auth.users is a
-- managed table we do not own.

create table if not exists public.profiles (
  id             uuid        primary key references auth.users(id) on delete cascade,
  email          text        not null,
  display_name   text,
  -- How this person got in. Not decoration: a comp reader and a paying customer
  -- have different entitlements later, and reconstructing that after the fact
  -- from redemption tables is guesswork.
  access_source  text        not null default 'purchase'
                             check (access_source in ('purchase', 'activation_code', 'admin')),
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

-- Case-insensitive uniqueness on email, enforced by the database.
--
-- preorderLookup.js carries a comment naming this as "the real fix" for its
-- caseVariants() workaround and defers it as follow-up work, because retrofitting
-- it onto `preorders` is a migration against live rows that may already collide.
-- `profiles` is empty, so there is no reason to inherit the problem: it gets the
-- index now and never needs the workaround. Note it is lower(email), not citext -
-- citext would need an extension for a single column.
create unique index if not exists profiles_email_lower_key
  on public.profiles (lower(email));

-- ---------------------------------------------------------------------------
-- 2. activation_codes
-- ---------------------------------------------------------------------------
-- A bearer credential that grants account access without a purchase: comps,
-- review copies, gifts, conference handouts.
--
-- THE PLAINTEXT CODE IS NEVER STORED. `code_hash` is the SHA-256 of the
-- normalized code, and that is all the database ever sees. The reasoning is the
-- same one that applies to passwords: a code is a bearer credential, so anyone
-- who reads this table with plaintext in it can use every code in it. A database
-- dump, a support screenshot, an over-broad SELECT in an admin tool - all of them
-- become harmless when the column is a digest. The plaintext exists exactly once,
-- in the mint response, and is never recoverable afterwards. Lose it, revoke the
-- row and mint another.
--
-- The digest is unsalted, and that is correct here rather than sloppy: salting
-- exists to defeat precomputation against low-entropy secrets, and these codes
-- carry 60 bits from a CSPRNG. There is no dictionary to precompute. Unsalted
-- also means the lookup is a single indexed equality on `code_hash`, instead of
-- a table scan hashing every row against a candidate.

create table if not exists public.activation_codes (
  id           uuid        primary key default gen_random_uuid(),
  code_hash    text        not null unique,
  -- What this code is for, in words a human will recognise in six months.
  label        text        not null default '',
  -- Number of distinct redemptions permitted. 1 = the single-use default.
  max_uses     int         not null default 1 check (max_uses >= 1),
  uses         int         not null default 0 check (uses >= 0),
  -- NULL = never expires. Prefer setting it; an immortal bearer credential is
  -- a liability with no upside.
  expires_at   timestamptz,
  -- Manual kill switch, independent of uses/expiry. Set it and the code is dead
  -- immediately, whatever its counters say.
  revoked_at   timestamptz,
  created_at   timestamptz not null default now(),
  created_by   text        not null default '',
  -- The counter can never exceed its own ceiling. redeem_activation_code() is
  -- what enforces this in practice; the constraint is the backstop that makes it
  -- true rather than merely intended, in the same spirit as the unique index on
  -- preorders(email, edition_type).
  constraint activation_codes_uses_within_max check (uses <= max_uses)
);

create index if not exists activation_codes_created_at_idx
  on public.activation_codes (created_at desc);

-- ---------------------------------------------------------------------------
-- 3. activation_code_redemptions
-- ---------------------------------------------------------------------------
-- Who burned what, and when. Two jobs: an audit trail, and the thing that makes
-- re-submitting a code idempotent instead of expensive.

create table if not exists public.activation_code_redemptions (
  id          uuid        primary key default gen_random_uuid(),
  code_id     uuid        not null references public.activation_codes(id) on delete cascade,
  -- Nullable because a redemption survives the deletion of the account that made
  -- it. The audit trail outliving the user is the point of an audit trail.
  user_id     uuid        references auth.users(id) on delete set null,
  email       text        not null,
  redeemed_at timestamptz not null default now()
);

-- One redemption per (code, email), case-insensitively.
--
-- Without this, a multi-use code handed to one person and clicked twice burns
-- two of its uses. With it, the second attempt collides, redeem_activation_code()
-- reads that as "already yours" and returns success without decrementing
-- anything. A retry after a dropped connection costs the code nothing.
create unique index if not exists activation_code_redemptions_code_email_key
  on public.activation_code_redemptions (code_id, lower(email));

-- ---------------------------------------------------------------------------
-- 4. activation_intents
-- ---------------------------------------------------------------------------
-- The bridge across the magic-link round trip.
--
-- A code must not be burned when it is typed - only when the person who typed it
-- proves they control the email address. Otherwise anyone holding a valid code
-- can spend it against addresses they do not own, and a single-use code is
-- destroyed by a stranger before its intended recipient ever sees it.
--
-- So the sign-in form validates the code without burning it, records the intent
-- here, and emails a link. Redemption happens on the far side of that link, when
-- the address is proven. This table is what remembers which code was in play, and
-- it stores `code_id` rather than the code itself so no plaintext crosses the
-- round trip - not in this table, not in the link, not in the email.

create table if not exists public.activation_intents (
  email      text        primary key,
  code_id    uuid        not null references public.activation_codes(id) on delete cascade,
  created_at timestamptz not null default now(),
  -- Short. The intent only has to survive someone walking to their inbox.
  expires_at timestamptz not null default (now() + interval '1 hour')
);

-- ---------------------------------------------------------------------------
-- 5. redeem_activation_code(): the only correct way to spend a code
-- ---------------------------------------------------------------------------
-- WHY THIS IS A FUNCTION AND NOT THREE STATEMENTS IN JAVASCRIPT
--
-- The tempting shape is: SELECT the code, check `uses < max_uses` in the
-- application, then UPDATE. That is a check-then-act race with a real exploit.
-- Two requests carrying the last use of a code both SELECT `uses = 0,
-- max_uses = 1`, both conclude they may proceed, and both UPDATE. The code is
-- spent twice. On a serverless runtime the two requests are not even on the same
-- machine, so no amount of in-process locking helps.
--
-- `select ... for update` takes a row lock inside a transaction, so the second
-- caller blocks until the first commits and then re-reads the incremented
-- counter. The check and the act become one indivisible step. This is the same
-- reason assign_authors_copy_number() in 003 lives in a trigger rather than in
-- the checkout handler.
--
-- Returns jsonb rather than raising, because "expired" and "already spent" are
-- ordinary outcomes the sign-in page must render as sentences, not 500s.

create or replace function public.redeem_activation_code(
  p_code_id uuid,
  p_user_id uuid,
  p_email   text
) returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  c public.activation_codes%rowtype;
begin
  -- The lock. Everything below is safe only because of this line.
  select * into c from public.activation_codes where id = p_code_id for update;

  if not found then
    return jsonb_build_object('ok', false, 'reason', 'not_found');
  end if;

  if c.revoked_at is not null then
    return jsonb_build_object('ok', false, 'reason', 'revoked');
  end if;

  if c.expires_at is not null and c.expires_at <= now() then
    return jsonb_build_object('ok', false, 'reason', 'expired');
  end if;

  -- Idempotency, checked before the ceiling so that a retry by someone who has
  -- already redeemed succeeds even once the code is fully spent.
  if exists (
    select 1 from public.activation_code_redemptions r
     where r.code_id = c.id and lower(r.email) = lower(p_email)
  ) then
    -- Backfill the user id if the first redemption predated the account row.
    update public.activation_code_redemptions
       set user_id = coalesce(user_id, p_user_id)
     where code_id = c.id and lower(email) = lower(p_email);
    return jsonb_build_object('ok', true, 'reason', 'already_redeemed', 'remaining', c.max_uses - c.uses);
  end if;

  if c.uses >= c.max_uses then
    return jsonb_build_object('ok', false, 'reason', 'exhausted');
  end if;

  update public.activation_codes set uses = uses + 1 where id = c.id;
  insert into public.activation_code_redemptions (code_id, user_id, email)
       values (c.id, p_user_id, p_email);

  return jsonb_build_object(
    'ok', true,
    'reason', 'redeemed',
    'remaining', c.max_uses - c.uses - 1
  );
end;
$$;

-- ---------------------------------------------------------------------------
-- 6. inspect_activation_code(): validate without spending
-- ---------------------------------------------------------------------------
-- Used by the sign-in form to answer "is this code worth emailing a link about?"
-- Deliberately returns no identifying detail about the code beyond whether it
-- currently works and why not - a probe should not be able to enumerate labels
-- or redemption history.

create or replace function public.inspect_activation_code(p_code_hash text)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  c public.activation_codes%rowtype;
begin
  select * into c from public.activation_codes where code_hash = p_code_hash;

  if not found then
    return jsonb_build_object('ok', false, 'reason', 'not_found');
  end if;
  if c.revoked_at is not null then
    return jsonb_build_object('ok', false, 'reason', 'revoked');
  end if;
  if c.expires_at is not null and c.expires_at <= now() then
    return jsonb_build_object('ok', false, 'reason', 'expired');
  end if;
  if c.uses >= c.max_uses then
    return jsonb_build_object('ok', false, 'reason', 'exhausted');
  end if;

  return jsonb_build_object('ok', true, 'reason', 'valid', 'code_id', c.id);
end;
$$;

-- ---------------------------------------------------------------------------
-- 7. Lock it all down, 012-style
-- ---------------------------------------------------------------------------
-- RLS on with no policies is deny-all for anon and authenticated; service_role
-- bypasses it. Asserted rather than assumed, so a table restored from a dump
-- cannot come back with it off.

alter table public.profiles                     enable row level security;
alter table public.activation_codes             enable row level security;
alter table public.activation_code_redemptions  enable row level security;
alter table public.activation_intents           enable row level security;

-- Grants revoked as well as policies withheld. 012's central lesson: RLS and
-- grants are two independent gates, and revoking means the next mistake fails
-- closed. 012 also flipped the default privileges for role `postgres`, so tables
-- created after it arrive ungranted - these revokes are belt to that suspenders,
-- and they are what makes this migration correct even if it is ever replayed
-- against a database where 012's default-privileges block was skipped.
revoke all on public.profiles                    from anon, authenticated;
revoke all on public.activation_codes            from anon, authenticated;
revoke all on public.activation_code_redemptions from anon, authenticated;
revoke all on public.activation_intents          from anon, authenticated;

-- The functions. See the header: `security definer` plus Postgres's default
-- `EXECUTE to public` is how a locked table gets read through the front door.
-- Only the service role may call these.
revoke all on function public.redeem_activation_code(uuid, uuid, text)
  from public, anon, authenticated;
revoke all on function public.inspect_activation_code(text)
  from public, anon, authenticated;

grant execute on function public.redeem_activation_code(uuid, uuid, text) to service_role;
grant execute on function public.inspect_activation_code(text)            to service_role;

commit;

-- ---------------------------------------------------------------------------
-- VERIFY. Run after the commit. Every table should read rls_enabled = t,
-- policies = 0, anon_grants = none. Both functions should read anon_exec = f.
-- ---------------------------------------------------------------------------
select
  c.relname                                                as object,
  c.relrowsecurity                                         as rls_enabled,
  coalesce((select count(*) from pg_policies p
             where p.schemaname = 'public' and p.tablename = c.relname), 0) as policies,
  coalesce(nullif(array_to_string(array(
    select distinct a.privilege_type
      from information_schema.role_table_grants a
     where a.table_schema = 'public'
       and a.table_name   = c.relname
       and a.grantee in ('anon', 'authenticated')
     order by 1), ', '), ''), 'none')                      as anon_grants
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind = 'r'
  and c.relname in ('profiles', 'activation_codes',
                    'activation_code_redemptions', 'activation_intents')
order by 1;

select
  p.proname                                                    as function,
  p.prosecdef                                                  as security_definer,
  has_function_privilege('anon',          p.oid, 'execute')    as anon_exec,
  has_function_privilege('authenticated', p.oid, 'execute')    as authenticated_exec,
  has_function_privilege('service_role',  p.oid, 'execute')    as service_role_exec
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public'
  and p.proname in ('redeem_activation_code', 'inspect_activation_code')
order by 1;
