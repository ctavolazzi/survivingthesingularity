/**
 * Reject future-dated Stripe webhook timestamps (plan item B-09).
 *
 * Pure and dependency-free for the same reason webhookEventPolicy.js and
 * adminToken.js are: this sits on the money path and there is no vitest in this
 * project, so a module that imports $lib or $env cannot be tested at all. Keep
 * the imports at zero.
 *
 * WHAT THE HOLE ACTUALLY IS, STATED HONESTLY
 *
 * Stripe's constructEvent tolerance is enforced on the PAST side only. A payload
 * signed with `t` set far in the future therefore satisfies the tolerance check
 * forever, so its signature never expires. Measured on 2026-07-29: t-600s
 * returned 400 and t+600s returned 200.
 *
 * Do not oversell this. The timestamp is inside the signed string, so an attacker
 * cannot move it without the signing secret, and an attacker who HAS the secret
 * can simply mint a fresh payload instead. This closes an unbounded-validity
 * window and makes clock disagreement visible. It is hygiene, not a patch for an
 * exploitable hole, which is exactly why it is a P2 and why the failure mode
 * below is tuned the way it is.
 *
 * THE FAILURE MODE IS TUNED TO NOT BREAK THE MONEY PATH
 *
 * The realistic way this code hurts anyone is by rejecting legitimate traffic:
 * if our clock ran behind Stripe's, every genuine webhook would look
 * future-dated and 100% of paid orders would start bouncing. That is a far worse
 * outcome than the thing being defended against. So:
 *
 *   future-dated beyond tolerance   400, with the measured skew in the log
 *   timestamp missing/unparseable   ALLOWED, loudly. See `degradesOpen` below.
 *
 * Degrading open on an unparseable header is deliberate. Reaching that branch
 * means Stripe's signature header format changed under us, and failing shut on
 * that would take the whole checkout down for the three days Stripe retries and
 * then lose the orders. The signature check is still the real guard and still
 * runs; this only ever adds a rejection on top of it.
 */

/**
 * How far ahead of our clock a signed timestamp may sit before it is refused.
 *
 * 300 seconds, chosen to mirror the default tolerance Stripe already applies on
 * the past side, so the accepted window is symmetric rather than an arbitrary
 * new number. Real clock skew between Cloudflare's runtime and Stripe is
 * sub-second, so this is roughly two orders of magnitude of headroom.
 */
export const FUTURE_TOLERANCE_SECONDS = 300;

/**
 * Pull the `t=` value out of a stripe-signature header.
 *
 * The header is a comma-separated list of key=value pairs, for example
 * `t=1717171717,v1=abc...,v0=def...`. Only `t` is of interest here.
 *
 * Returns null rather than throwing or guessing for anything that is not a
 * finite integer count of seconds. Callers must treat null as "cannot tell",
 * never as "zero" and never as "invalid": see the degrade-open note above.
 *
 * @param {string|null|undefined} header raw stripe-signature header
 * @returns {number|null} unix seconds, or null if not determinable
 */
export function parseSignatureTimestamp(header) {
  if (typeof header !== 'string') return null;

  for (const part of header.split(',')) {
    const eq = part.indexOf('=');
    if (eq === -1) continue;
    if (part.slice(0, eq).trim() !== 't') continue;

    const raw = part.slice(eq + 1).trim();

    // Deliberately strict. Number('') is 0 and Number(' 12 ') is 12, and both
    // of those coercions would turn a malformed header into a confident wrong
    // answer. Only a plain run of digits, optionally signed, counts.
    if (!/^-?\d+$/.test(raw)) return null;

    const seconds = Number(raw);
    return Number.isSafeInteger(seconds) ? seconds : null;
  }

  return null;
}

/**
 * @typedef {object} FreshnessResult
 * @property {boolean} ok whether the caller may proceed
 * @property {'ok'|'future-dated'|'no-timestamp'} reason
 * @property {boolean} degradesOpen true when ok is true DESPITE not having
 *   verified anything, so the caller can log it rather than read it as a pass
 * @property {number|null} skewSeconds signed seconds ahead of now, null if
 *   unknown. Positive means the timestamp is in the future.
 */

/**
 * Decide whether a signed timestamp is acceptably fresh on the future side.
 *
 * The past side is left entirely to Stripe's own tolerance check, which already
 * enforces it inside constructEventAsync. Re-implementing that here would mean
 * two separate expiry windows that can drift apart, and the second one would be
 * the one nobody remembers exists.
 *
 * @param {string|null|undefined} header raw stripe-signature header
 * @param {number} nowSeconds current unix time in seconds
 * @param {number} [toleranceSeconds]
 * @returns {FreshnessResult}
 */
export function checkFreshness(header, nowSeconds, toleranceSeconds = FUTURE_TOLERANCE_SECONDS) {
  const timestamp = parseSignatureTimestamp(header);

  if (timestamp === null) {
    return { ok: true, reason: 'no-timestamp', degradesOpen: true, skewSeconds: null };
  }

  // A caller that hands us a nonsense clock gets the same treatment as a
  // nonsense header. Guessing at "now" is how a guard starts rejecting real
  // traffic for reasons nobody can reconstruct from the logs.
  if (!Number.isFinite(nowSeconds)) {
    return { ok: true, reason: 'no-timestamp', degradesOpen: true, skewSeconds: null };
  }

  const skewSeconds = timestamp - nowSeconds;

  // Strictly greater than. A timestamp sitting exactly on the tolerance boundary
  // is accepted, matching how Stripe treats its own boundary and keeping the
  // window closed-interval on both ends.
  if (skewSeconds > toleranceSeconds) {
    return { ok: false, reason: 'future-dated', degradesOpen: false, skewSeconds };
  }

  return { ok: true, reason: 'ok', degradesOpen: false, skewSeconds };
}
