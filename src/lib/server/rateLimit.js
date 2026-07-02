/**
 * Minimal in-memory sliding-window rate limiter.
 *
 * NOTE: state lives in the server process's memory. On a single long-lived
 * Node server this works well. On serverless (Vercel/Cloudflare) each cold
 * instance has its own map, so this is a best-effort speed bump, not a hard
 * guarantee. For durable limits across instances, back this with Supabase or
 * a KV store (Upstash) later. Good enough to stop casual abuse / bots.
 */

const buckets = new Map(); // key -> number[] (timestamps, ms)

/**
 * @param {string} key            identifier to limit on (e.g. ip:route)
 * @param {number} limit          max requests allowed per window
 * @param {number} windowMs       window size in milliseconds
 * @returns {{ allowed: boolean, retryAfterMs: number }}
 */
export function rateLimit(key, limit, windowMs) {
  const now = Date.now();
  const cutoff = now - windowMs;

  const hits = (buckets.get(key) ?? []).filter((t) => t > cutoff);

  if (hits.length >= limit) {
    const retryAfterMs = hits[0] + windowMs - now;
    buckets.set(key, hits);
    return { allowed: false, retryAfterMs: Math.max(0, retryAfterMs) };
  }

  hits.push(now);
  buckets.set(key, hits);

  cleanup(cutoff);

  return { allowed: true, retryAfterMs: 0 };
}

/**
 * Like rateLimit(), but does NOT record a hit — use with recordHit() when
 * only some outcomes should count against the budget (e.g. rate-limit failed
 * password attempts without penalizing successful ones, so legitimate users
 * behind a shared IP can't lock each other out).
 */
export function peekRate(key, limit, windowMs) {
  const now = Date.now();
  const cutoff = now - windowMs;

  const hits = (buckets.get(key) ?? []).filter((t) => t > cutoff);
  buckets.set(key, hits);

  if (hits.length >= limit) {
    const retryAfterMs = hits[0] + windowMs - now;
    return { allowed: false, retryAfterMs: Math.max(0, retryAfterMs) };
  }
  return { allowed: true, retryAfterMs: 0 };
}

/** Record one hit against `key` (pairs with peekRate). */
export function recordHit(key) {
  const hits = buckets.get(key) ?? [];
  hits.push(Date.now());
  buckets.set(key, hits);
}

// Opportunistic cleanup so the map doesn't grow unbounded.
function cleanup(cutoff) {
  if (buckets.size <= 5000) return;
  for (const [k, v] of buckets) {
    const live = v.filter((t) => t > cutoff);
    if (live.length === 0) buckets.delete(k);
    else buckets.set(k, live);
  }
}
