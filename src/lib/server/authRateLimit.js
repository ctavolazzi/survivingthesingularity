/**
 * Rate limiting for auth, backed by the database instead of process memory.
 *
 * WHY NOT $lib/server/rateLimit.js
 *
 * That module is honest about its own limits, in its own header: "state lives
 * in the server process's memory... On serverless each cold instance has its
 * own map, so this is a best-effort speed bump, not a hard guarantee."
 *
 * For /api/waitlist that trade is fine. The worst case is some duplicate rows.
 * For a password form the trade inverts, because the traffic being limited is
 * the attack rather than a side effect of it. An online guessing run against
 * one known address does not need to defeat the limiter; it just needs to keep
 * landing on instances whose bucket is empty. This project deploys behind
 * adapter-auto to Cloudflare, where isolates are numerous and short-lived, so
 * "empty bucket" is the common case, not the rare one.
 *
 * Hence a shared counter. `sql/015_auth_accounts.sql` holds the table and the
 * check-and-record function; this is the client half.
 *
 * FAIL-CLOSED ON THE LIMITER ITSELF
 *
 * If the database call fails we deny the request. That is the uncomfortable
 * direction - a Supabase blip briefly stops people signing in - but the
 * alternative is that anyone who can degrade the database gets an unlimited
 * password oracle, which means the limiter is decorative exactly when it
 * matters. $lib/server/sameOrigin.js exists because of a check that failed
 * open; this one is not going to repeat that.
 *
 * The in-memory limiter is still applied first as a cheap local pre-filter, so
 * a flood does not turn into one database round trip per attempt.
 */

import { createHash } from 'node:crypto';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { rateLimit } from '$lib/server/rateLimit.js';

/**
 * Hash the key before it is stored.
 *
 * The natural key for a login limiter is `signin:someone@example.com`, and
 * storing that verbatim turns the limiter table into a list of addresses that
 * have accounts here - readable by anything that can read the table, and by
 * anyone who ends up with a database export. Hashing keeps the limiter working
 * (equality is all it needs) while making the table useless as a directory.
 *
 * @param {string} key
 * @returns {string}
 */
function hashKey(key) {
  return createHash('sha256').update(key).digest('hex').slice(0, 48);
}

/**
 * @typedef {{allowed: boolean, retryAfterSeconds: number}} RateVerdict
 */

/**
 * Check a durable sliding-window limit and record the attempt if it passes.
 *
 * @param {string} key            e.g. `signin:ip:1.2.3.4` or `signin:email:<addr>`
 * @param {number} limit          attempts permitted in the window
 * @param {number} windowSeconds  window length
 * @returns {Promise<RateVerdict>}
 */
export async function authRateCheck(key, limit, windowSeconds) {
  // Local pre-filter. Deliberately looser than the durable limit (3x) so it
  // only catches a burst hammering one instance, and never rejects traffic the
  // shared counter would have allowed.
  const local = rateLimit(`authlocal:${key}`, limit * 3, windowSeconds * 1000);
  if (!local.allowed) {
    return { allowed: false, retryAfterSeconds: Math.ceil(local.retryAfterMs / 1000) };
  }

  if (!supabaseAdmin) {
    // No service key configured. Auth cannot work at all in this state, so the
    // caller is about to fail anyway - but say no here rather than silently
    // running an auth endpoint with no limiter.
    console.error('[authRateLimit] SUPABASE_SERVICE_KEY is not configured; denying.');
    return { allowed: false, retryAfterSeconds: 60 };
  }

  const { data, error } = await supabaseAdmin.rpc('auth_rate_check', {
    p_key: hashKey(key),
    p_limit: limit,
    p_window_seconds: windowSeconds
  });

  if (error) {
    // Fail closed. See the header.
    console.error('[authRateLimit] check failed, denying:', error.message);
    return { allowed: false, retryAfterSeconds: 30 };
  }

  return {
    allowed: data?.allowed === true,
    retryAfterSeconds: Number(data?.retry_after_seconds ?? 30)
  };
}

/**
 * Clear a key after a successful authentication.
 *
 * Without this, five failed attempts followed by the correct password still
 * leaves the account rate limited, so the person who just proved they own it
 * gets locked out by their own typos. Only ever call this after success.
 *
 * @param {string} key
 * @returns {Promise<void>}
 */
export async function authRateReset(key) {
  if (!supabaseAdmin) return;
  const { error } = await supabaseAdmin.rpc('auth_rate_reset', { p_key: hashKey(key) });
  if (error) console.error('[authRateLimit] reset failed:', error.message);
}

/**
 * Budgets, in one place so they can be read against each other.
 *
 * Per-IP limits stop one host running a broad campaign. Per-identifier limits
 * stop a distributed campaign against one account, which per-IP cannot see.
 * Both are needed; neither substitutes for the other.
 *
 * Email-sending actions (magic link, signup confirmation) are limited harder
 * than sign-in, because there the abuse is using us to mail a third party -
 * the cost lands on someone who never visited the site, and on our sending
 * reputation.
 */
export const BUDGETS = {
  signin:      { ip: { limit: 20, window: 600 }, id: { limit: 8,  window: 900 } },
  signup:      { ip: { limit: 5,  window: 600 }, id: { limit: 3,  window: 3600 } },
  magiclink:   { ip: { limit: 5,  window: 600 }, id: { limit: 3,  window: 900 } },
  resend:      { ip: { limit: 5,  window: 600 }, id: { limit: 3,  window: 900 } },
  oauth:       { ip: { limit: 20, window: 600 }, id: null }
};

/**
 * Apply both the per-IP and per-identifier budget for an action.
 *
 * @param {keyof typeof BUDGETS} action
 * @param {string} ip
 * @param {string} [identifier] normalized email, when the action has one
 * @returns {Promise<RateVerdict>}
 */
export async function enforceAuthBudget(action, ip, identifier) {
  const budget = BUDGETS[action];
  if (!budget) return { allowed: true, retryAfterSeconds: 0 };

  const byIp = await authRateCheck(`${action}:ip:${ip}`, budget.ip.limit, budget.ip.window);
  if (!byIp.allowed) return byIp;

  if (budget.id && identifier) {
    return authRateCheck(`${action}:id:${identifier}`, budget.id.limit, budget.id.window);
  }
  return { allowed: true, retryAfterSeconds: 0 };
}
