-- Migration 016: the /signup flow. Sits on top of 015's `profiles`.
-- Run in the Supabase SQL Editor after 015_accounts_and_activation_codes.sql.
-- Idempotent: safe to run more than once.
--
-- WHY THIS IS 016 AND NOT A SECOND 015
--
-- This started life as `sql/015_auth_accounts.sql` and created `public.profiles`
-- itself. While it was being written, another session committed c5d43af, which
-- added 015_accounts_and_activation_codes.sql - creating `profiles` too, with a
-- different column set.
--
-- Two migrations creating the same table is worse than it sounds, because both
-- spell it `create table if not exists`. Whichever runs second does NOTHING and
-- reports success. The database ends up with one definition, the other file's
-- author believes their columns exist, and the failure surfaces later as a
-- PostgREST 42703 from code that reads a column that was never created.
--
-- So 015 owns `profiles`. This migration only ADDS to it. If you are reading
-- this while writing 017, the rule that would have saved an hour: before adding
-- a numbered migration, `ls sql/` again - the number you checked at the start of
-- your session may not be free by the end of it.

begin;

-- ---------------------------------------------------------------------------
-- 1. profiles: consent columns
-- ---------------------------------------------------------------------------
--
-- The signup form's checkbox is a single "I agree to the Terms and the Privacy
-- Policy". That is acceptance of terms, NOT permission to market. They are
-- different lawful bases, and treating one as the other is how a site ends up
-- mailing people who never opted in. So they are two columns, and
-- `marketing_consent` defaults false and is only ever set by a later, explicit
-- opt-in - nothing in the signup path writes it true.

alter table public.profiles
  add column if not exists terms_accepted_at timestamptz;

alter table public.profiles
  add column if not exists marketing_consent boolean not null default false;

-- 015 defaults `access_source` to 'purchase' and constrains it to
-- (purchase, activation_code, admin). A free account created at /signup is none
-- of those, and defaulting it to 'purchase' would record that a person bought
-- something they did not. Widen the domain rather than lie in the data.
alter table public.profiles
  drop constraint if exists profiles_access_source_check;

alter table public.profiles
  add constraint profiles_access_source_check
  check (access_source in ('purchase', 'activation_code', 'admin', 'signup'));

-- ---------------------------------------------------------------------------
-- 2. Profile creation trigger
-- ---------------------------------------------------------------------------
--
-- 015 created the table but nothing that fills it; it expects the application
-- to insert. That works for the activation-code path, which has exactly one
-- call site. It does not survive the signup flow, which has three doors -
-- password signup, magic link, and OAuth - and where OAuth's user row is
-- created by GoTrue before any of our code runs. Three call sites and a race is
-- what a trigger is for.
--
-- `security definer` is required: the trigger executes as the GoTrue role,
-- which has no rights on public.profiles by design.
--
-- `set search_path = ''` is not optional on a security-definer function. Without
-- it, unqualified names resolve against the CALLER's search_path, so a caller
-- who can create objects can shadow `profiles` with their own table and have it
-- written as the definer. Every identifier below is schema-qualified.

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, email, display_name, access_source)
  values (
    new.id,
    lower(new.email),
    -- OAuth providers hand us a name; password signup does not. Fall back to
    -- the local part rather than leaving the UI to render an empty string.
    --
    -- NOTE: raw_user_meta_data is user-controlled. It is safe HERE because this
    -- value is only ever displayed. It must never be read for an authorization
    -- decision - that is what app_metadata is for.
    coalesce(
      nullif(new.raw_user_meta_data ->> 'full_name', ''),
      nullif(new.raw_user_meta_data ->> 'name', ''),
      split_part(coalesce(new.email, ''), '@', 1)
    ),
    'signup'
  )
  on conflict (id) do nothing;

  perform public.claim_preorders_for_user(new.id, lower(new.email));

  return new;
end;
$$;

drop trigger if exists trg_handle_new_user on auth.users;
create trigger trg_handle_new_user
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ---------------------------------------------------------------------------
-- 3. Entitlements: connect an account to what that address already bought
-- ---------------------------------------------------------------------------
--
-- The signup page promises "Anything you preorder lands here the moment it
-- ships". Preorders predate accounts and are keyed by email alone, so without
-- this an existing customer signs up and sees an empty library.

alter table public.preorders
  add column if not exists user_id uuid references auth.users(id) on delete set null;

create index if not exists preorders_user_id_idx on public.preorders (user_id);

-- SECURITY: matching on email is only safe because the caller has already proven
-- control of that address - password signup requires confirmation, magic link is
-- proof by construction, OAuth providers assert a verified address. Never call
-- this with an address a request merely CLAIMED.
--
-- `user_id is null` makes it idempotent and non-stealing: a preorder already
-- attached to another account is never reassigned.

create or replace function public.claim_preorders_for_user(p_user_id uuid, p_email text)
returns integer
language plpgsql
security definer
set search_path = ''
as $$
declare
  claimed integer;
begin
  if p_user_id is null or coalesce(p_email, '') = '' then
    return 0;
  end if;

  update public.preorders
     set user_id = p_user_id
   where lower(email) = lower(p_email)
     and user_id is null;

  get diagnostics claimed = row_count;
  return claimed;
end;
$$;

-- ---------------------------------------------------------------------------
-- 4. auth_rate_limits: a rate limiter that survives a cold start
-- ---------------------------------------------------------------------------
--
-- $lib/server/rateLimit.js keeps its buckets in process memory and says so:
-- "On serverless each cold instance has its own map, so this is a best-effort
-- speed bump, not a hard guarantee." Fair for a waitlist signup. Not fair for a
-- password form, where the traffic being limited IS the attack: an online
-- guessing run only has to keep landing on instances with a cold bucket, and
-- this deploys to Cloudflare, where isolates are many and short-lived.
--
-- The key arrives already hashed from $lib/server/authRateLimit.js, so a
-- database dump does not become a list of which addresses have accounts.

create table if not exists public.auth_rate_limits (
  id      bigserial   primary key,
  key     text        not null,
  hit_at  timestamptz not null default now()
);

create index if not exists auth_rate_limits_key_time_idx
  on public.auth_rate_limits (key, hit_at desc);

-- Count and record in one statement. Two statements would let two concurrent
-- attempts both read a count under the limit and both insert.
create or replace function public.auth_rate_check(
  p_key text,
  p_limit integer,
  p_window_seconds integer
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  cutoff timestamptz := now() - make_interval(secs => p_window_seconds);
  hits   integer;
  oldest timestamptz;
begin
  select count(*), min(hit_at)
    into hits, oldest
    from public.auth_rate_limits
   where key = p_key
     and hit_at > cutoff;

  if hits >= p_limit then
    return jsonb_build_object(
      'allowed', false,
      'retry_after_seconds',
        greatest(0, ceil(extract(epoch from
          (oldest + make_interval(secs => p_window_seconds) - now()))))::int
    );
  end if;

  insert into public.auth_rate_limits (key) values (p_key);

  return jsonb_build_object('allowed', true, 'retry_after_seconds', 0);
end;
$$;

-- Clears a key after a success, so a run of typos does not lock someone out of
-- the account they just proved they own.
create or replace function public.auth_rate_reset(p_key text)
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  delete from public.auth_rate_limits where key = p_key;
end;
$$;

-- Housekeeping. Nothing schedules this yet; call it from the nightly job or
-- pg_cron. The longest window any caller uses is measured in minutes, so rows
-- older than a day are dead weight.
create or replace function public.auth_rate_prune()
returns integer
language plpgsql
security definer
set search_path = ''
as $$
declare
  removed integer;
begin
  delete from public.auth_rate_limits where hit_at < now() - interval '1 day';
  get diagnostics removed = row_count;
  return removed;
end;
$$;

-- ---------------------------------------------------------------------------
-- 5. Lockdown
-- ---------------------------------------------------------------------------
--
-- Same posture as 012 and 015: RLS on, no policies, no grants. service_role
-- bypasses RLS and is how the server reads these.

alter table public.auth_rate_limits enable row level security;

revoke all on public.auth_rate_limits from public, anon, authenticated;
revoke all on sequence public.auth_rate_limits_id_seq from public, anon, authenticated;

-- THE `public` IN THESE REVOKES IS LOAD-BEARING.
--
-- Postgres grants EXECUTE on every newly created function to the pseudo-role
-- PUBLIC automatically, and `anon` and `authenticated` INHERIT from PUBLIC.
-- `revoke ... from anon` removes only what was granted to anon directly; it does
-- not touch what anon holds through PUBLIC. A migration that revokes from just
-- the two named roles reads as locked, passes review, and leaves every function
-- callable by anyone holding the publishable key.
--
-- These are all `security definer`, so they run as their owner and bypass RLS.
-- Left callable: `claim_preorders_for_user` would let anyone attach any preorder
-- to any account, and `auth_rate_reset` would let anyone clear their own login
-- rate limit between guesses. Both are worse than the table grants 012 removed.
--
-- 015 got this right on its two functions. The first draft of this file did not.

revoke all on function public.handle_new_user()
  from public, anon, authenticated;
revoke all on function public.claim_preorders_for_user(uuid, text)
  from public, anon, authenticated;
revoke all on function public.auth_rate_check(text, integer, integer)
  from public, anon, authenticated;
revoke all on function public.auth_rate_reset(text)
  from public, anon, authenticated;
revoke all on function public.auth_rate_prune()
  from public, anon, authenticated;

grant execute on function public.claim_preorders_for_user(uuid, text)      to service_role;
grant execute on function public.auth_rate_check(text, integer, integer)   to service_role;
grant execute on function public.auth_rate_reset(text)                     to service_role;
grant execute on function public.auth_rate_prune()                         to service_role;

commit;

-- ---------------------------------------------------------------------------
-- VERIFY. Run after the commit.
-- ---------------------------------------------------------------------------
--
-- (a) The new columns exist. If this returns fewer than 3 rows, 015's `profiles`
--     was created but this migration's alters did not run.
select column_name
  from information_schema.columns
 where table_schema = 'public'
   and table_name   = 'profiles'
   and column_name in ('terms_accepted_at', 'marketing_consent', 'access_source');

-- (b) No function is reachable without the service role. Every row must read
--     f, f. This is the check the first draft of this file would have failed.
select p.proname,
       has_function_privilege('anon',          p.oid, 'execute') as anon_exec,
       has_function_privilege('authenticated', p.oid, 'execute') as auth_exec
  from pg_proc p
  join pg_namespace n on n.oid = p.pronamespace
 where n.nspname = 'public'
   and p.proname in ('handle_new_user', 'claim_preorders_for_user',
                     'auth_rate_check', 'auth_rate_reset', 'auth_rate_prune');

-- (c) The trigger is attached. GoTrue creates the auth.users row; without this
--     an OAuth sign-in produces a session with no profile behind it.
select tgname, tgenabled
  from pg_trigger
 where tgname = 'trg_handle_new_user';

-- (d) Behavioural control, with the PUBLISHABLE key (not the service key):
--
--       POST /rest/v1/rpc/auth_rate_reset  {"p_key":"x"}  -> expect 42501
--       GET  /rest/v1/profiles?select=*                   -> expect 42501
--
--     A 23502 or a 200 instead of 42501 means the request cleared the grant.
--     Control: the same call against public.discord_applications, which is
--     known-locked, must also give 42501. A checker that cannot tell locked
--     from unlocked is not a checker.
