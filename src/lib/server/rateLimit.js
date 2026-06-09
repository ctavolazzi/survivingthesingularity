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

  // Opportunistic cleanup so the map doesn't grow unbounded.
  if (buckets.size > 5000) {
    for (const [k, v] of buckets) {
      const live = v.filter((t) => t > cutoff);
      if (live.length === 0) buckets.delete(k);
      else buckets.set(k, live);
    }
  }

  return { allowed: true, retryAfterMs: 0 };
}
