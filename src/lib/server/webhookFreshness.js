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
 * THE MALFORMED-TIMESTAMP BYPASS. READ THIS BEFORE LOOSENING ANYTHING.
 *
 * The first version of this module degraded open on ANY timestamp it could not
 * parse, which left the guard trivially bypassable. Measured, not theorised:
 * `t=abc` and `t=` both returned 200 with a valid signature.
 *
 * The mechanism is in stripe-node. `parseHeader` does
 * `accum.timestamp = parseInt(kv[1], 10)` with no validity check, and
 * `makeHMACContent` signs the PARSED value back: `${details.timestamp}.${payload}`.
 * So `t=abc` parses to NaN, and an attacker who signs over the literal string
 * "NaN.{body}" produces a signature Stripe accepts. The tolerance test is then
 * `timestampAge > tolerance` where timestampAge is `now - NaN`, and `NaN > 300`
 * is false, so Stripe's own past-side check does not fire either. The result was
 * a payload with NO time bound in either direction, which is exactly the
 * unbounded-validity window this module claims to close.
 *
 * Hence the split below between ABSENT and MALFORMED. They are not the same
 * event and must not share a branch:
 *
 *   future-dated beyond tolerance   400, with the measured skew in the log
 *   `t` present but unparseable     400. Stripe cannot produce this with a
 *                                   valid signature, so the only way to reach
 *                                   it is a hand-crafted header. Fail SHUT.
 *   `t` absent entirely             ALLOWED, loudly. Unreachable in practice
 *                                   (Stripe defaults to -1, which its own
 *                                   tolerance rejects as ancient) and kept open
 *                                   only as a safety valve for a genuine header
 *                                   format change.
 *   clock unusable                  ALLOWED, loudly, and reported as its own
 *                                   reason so the log names the real cause.
 *
 * The asymmetry is the point. A format change is a Stripe-side event we should
 * survive; a garbage value inside a well-formed header is a chosen input.
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
 * @typedef {object} ParsedTimestamp
 * @property {boolean} present a `t` key existed in the header at all
 * @property {number|null} seconds the parsed value, or null when `t` was
 *   present but its value could not be read as an exact integer
 */

/**
 * Pull the `t=` value out of a stripe-signature header.
 *
 * The header is a comma-separated list of key=value pairs, for example
 * `t=1717171717,v1=abc...,v0=def...`. Only `t` is of interest here.
 *
 * RETURNS `present` SEPARATELY FROM `seconds`, and that distinction is the
 * whole fix for the bypass described in the module header. Collapsing "there
 * was no timestamp" and "there was a timestamp and it was garbage" into a
 * single null is what let `t=abc` through. One of those is a Stripe-side
 * format change worth surviving; the other is a chosen input.
 *
 * @param {string|null|undefined} header raw stripe-signature header
 * @returns {ParsedTimestamp}
 */
export function parseSignatureTimestamp(header) {
  if (typeof header !== 'string') return { present: false, seconds: null };

  for (const part of header.split(',')) {
    const eq = part.indexOf('=');
    if (eq === -1) continue;
    if (part.slice(0, eq).trim() !== 't') continue;

    const raw = part.slice(eq + 1).trim();

    // Deliberately strict, and stricter than stripe-node's own parseInt. Number('')
    // is 0 and parseInt('123abc') is 123, and both of those coercions would turn a
    // malformed header into a confident wrong answer. A leading + is tolerated
    // because Number() and parseInt() agree on it; nothing else is.
    if (!/^[+-]?\d+$/.test(raw)) return { present: true, seconds: null };

    const seconds = Number(raw);
    return { present: true, seconds: Number.isSafeInteger(seconds) ? seconds : null };
  }

  return { present: false, seconds: null };
}

/**
 * @typedef {object} FreshnessResult
 * @property {boolean} ok whether the caller may proceed
 * @property {'ok'|'future-dated'|'malformed-timestamp'|'no-timestamp'|'unusable-clock'} reason
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
  const { present, seconds } = parseSignatureTimestamp(header);

  // FAIL SHUT. A `t` that exists but does not parse cannot come from Stripe with
  // a valid signature, because Stripe signs its own parseInt result back into
  // the HMAC content. Reaching here therefore means someone hand-built the
  // header, and it is the exact input that bypassed both this guard and Stripe's
  // tolerance before. Do not relax this to a degrade-open without re-reading the
  // module header.
  if (present && seconds === null) {
    return { ok: false, reason: 'malformed-timestamp', degradesOpen: false, skewSeconds: null };
  }

  // Degrade OPEN, and only here. No `t` at all is what a Stripe-side header
  // format change would look like, and failing shut on that would bounce every
  // real webhook. Unreachable in practice: with no `t`, stripe-node defaults the
  // timestamp to -1 and its own tolerance rejects that as ancient.
  if (!present) {
    return { ok: true, reason: 'no-timestamp', degradesOpen: true, skewSeconds: null };
  }

  // Its own reason code, not folded into no-timestamp. A log line that names the
  // wrong cause is how the constructEventAsync bug cost someone a long night,
  // and collapsing these two was repeating that mistake.
  if (!Number.isFinite(nowSeconds)) {
    return { ok: true, reason: 'unusable-clock', degradesOpen: true, skewSeconds: null };
  }

  const skewSeconds = seconds - nowSeconds;

  // Strictly greater than. A timestamp sitting exactly on the tolerance boundary
  // is accepted, matching how Stripe treats its own boundary and keeping the
  // window closed-interval on both ends.
  if (skewSeconds > toleranceSeconds) {
    return { ok: false, reason: 'future-dated', degradesOpen: false, skewSeconds };
  }

  return { ok: true, reason: 'ok', degradesOpen: false, skewSeconds };
}
