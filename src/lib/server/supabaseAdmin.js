import { createClient } from '@supabase/supabase-js';
import { env } from '$env/dynamic/private';
import { supabaseConfigured } from '$lib/server/supabaseEnv.js';

// Server-only privileged client. Uses the SECRET key, which bypasses RLS - so
// this file must never be imported into client code. ($lib/server is enforced
// server-only by SvelteKit.) Dynamic env so a missing key never breaks builds;
// the client is simply null and callers degrade gracefully.
const url = env.SUPABASE_URL;
const key = env.SUPABASE_SERVICE_KEY;

// The guard used to be `url && key && !key.startsWith('placeholder')`, which
// let a malformed URL through to createClient(), which throws at module scope -
// taking down every route that imports this, including ones with no database
// access at all. Verified: an unedited .env.example URL 500'd the homepage.
// $lib/server/supabaseEnv.js carries the reasoning and the measurement.
export const supabaseAdmin = supabaseConfigured(url, key, 'supabaseAdmin')
  ? createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } })
  : null;

// Tiny in-memory cache so we don't hit the DB on every page render.
let cache = { value: null, at: 0 };
const TTL_MS = 60_000;

/**
 * Total waitlist signups, or null if unavailable (no key / error).
 * Cached for 60s.
 * @returns {Promise<number|null>}
 */
export async function getWaitlistCount() {
  if (!supabaseAdmin) return null;
  const now = Date.now();
  if (cache.value !== null && now - cache.at < TTL_MS) return cache.value;

  const { count, error } = await supabaseAdmin
    .from('waitlist')
    .select('*', { count: 'exact', head: true });

  if (error) {
    console.error('[waitlist count]', error.message);
    return null;
  }
  cache = { value: count ?? 0, at: now };
  return cache.value;
}
