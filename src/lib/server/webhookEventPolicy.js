/**
 * WHETHER TO PROCESS A STRIPE WEBHOOK EVENT WE HAVE SEEN BEFORE  (plan item B-08)
 *
 * Pure decision logic, deliberately in its own file with ZERO imports. Not for
 * tidiness: `supabaseAdmin` needs `$env/dynamic/private`, and a module carrying
 * a SvelteKit alias cannot be loaded by a plain test runner. This project has no
 * vitest, so the only way to test the load-bearing rule below exhaustively is to
 * keep it importable by relative path from a Playwright spec. The database
 * wiring lives next door in webhookEvents.js and stays thin enough to read.
 *
 * THE HAZARD THIS FILE EXISTS TO AVOID
 *
 * B-08 was written up as "identical signed bytes replayed twice produce 200
 * both times", which sounds like it asks for dedup on `event.id`. Implemented
 * naively, that would be worse than the gap it closes.
 *
 * STRIPE RETRIES REUSE THE SAME EVENT ID. A retry after a genuine failure is
 * not a duplicate, it is the delivery mechanism working as designed, and it is
 * the thing that rescues a paid order when the first attempt died halfway. If
 * this returned "already seen, skip" on any second sighting of an event id, then
 * the first failed attempt would poison every retry, the webhook would answer
 * 200, and a paying customer would receive nothing while the events table
 * insisted the event was handled.
 *
 * That is exactly the bug sql/013 was written to remove from
 * `fulfilled_sessions`, where a row meant "began" and was read as "done". Adding
 * it back one layer up would be a regression dressed as hardening.
 *
 * So the rule is: SKIP ONLY ON A TERMINAL SUCCESS. A prior attempt that is
 * still in flight is left alone, and a prior attempt that failed or died is
 * allowed to run again.
 *
 * WHY THIS IS SAFE TO GET WRONG IN THE PERMISSIVE DIRECTION
 *
 * Event-level dedup is an audit trail and an optimisation. It is NOT the safety
 * net. The safety net is `claimSession`, whose unique constraint on
 * `fulfilled_sessions.session_id` already stops the success page and the webhook
 * from double-fulfilling the same session. So this policy must be strictly LESS
 * aggressive than the session-level claim, never more: letting an extra event
 * through costs one redundant claim check that returns "stand down", while
 * wrongly blocking one costs a real order.
 *
 * When the two disagree, the session claim wins. That ordering is the whole
 * design.
 */

/**
 * How long an event may sit in `processing` before a later delivery treats it as
 * abandoned rather than in flight.
 *
 * Matched to STALE_CLAIM_MS in fulfillment.js on purpose. The two windows govern
 * the same physical situation, a worker that died mid-fulfillment, and if the
 * event window were shorter than the claim window there would be a band of time
 * where this file says "retry it" and claimSession says "another worker owns
 * it", so the retry would do nothing while both layers believed they had acted.
 *
 * Stripe spaces its own retries minutes apart, so anything this side of that is
 * a repair rather than a race.
 */
export const STALE_EVENT_MS = 2 * 60 * 1000;

/** Terminal success. The only state that earns a skip. */
export const PROCESSED = 'processed';
/** Started, outcome unknown. The dangerous state, same as 'claimed' next door. */
export const PROCESSING = 'processing';
/** Ran and failed. Explicitly retryable. */
export const FAILED = 'failed';

/**
 * @typedef {object} EventRow
 * @property {string} [status]      one of processing | processed | failed
 * @property {string} [received_at] ISO timestamp of when the CURRENT attempt
 *   began, reset on each repair. Not the first sighting: sql/014 keeps that in
 *   `first_seen_at`, immutable, because the staleness window needs "when did
 *   this attempt start" while the audit trail needs "when did this first show
 *   up", and one column cannot answer both.
 * @property {number} [attempts]
 */

/**
 * @typedef {object} Disposition
 * @property {boolean} proceed  true to run fulfillment, false to stand down
 * @property {string}  reason   stable machine-readable token, safe to log and assert on
 * @property {boolean} duplicate true when this delivery is a genuine repeat of
 *                               completed work, which is the B-08 acceptance
 *                               condition and NOT the same thing as !proceed
 */

/**
 * Decide what to do about an event we have a prior row for.
 *
 * @param {EventRow|null|undefined} existing prior row, or null when this event
 *   has never been seen (the insert succeeded)
 * @param {number} nowMs current time in epoch ms, injected rather than read so
 *   the behaviour is testable without faking the clock
 * @returns {Disposition}
 */
export function decideEventDisposition(existing, nowMs) {
  // Never seen. The overwhelmingly common case: process it.
  if (!existing) {
    return { proceed: true, reason: 'first-delivery', duplicate: false };
  }

  // Terminal success. This is the actual duplicate, and the only skip.
  if (existing.status === PROCESSED) {
    return { proceed: false, reason: 'already-processed', duplicate: true };
  }

  // A prior attempt failed. Stripe retrying is the point of the retry. Let it
  // through: claimSession decides whether there is anything left to do.
  if (existing.status === FAILED) {
    return { proceed: true, reason: 'retry-after-failure', duplicate: false };
  }

  // Row exists with no usable timestamp. Cannot tell in-flight from dead.
  // Proceed, for the same reason claimSession does: a duplicate attempt is
  // absorbed one layer down, whereas standing down here can lose a paid order
  // permanently. Bias toward the recoverable error.
  const startedAt = existing.received_at ? Date.parse(existing.received_at) : NaN;
  if (!Number.isFinite(startedAt)) {
    return { proceed: true, reason: 'unknown-age-proceeding', duplicate: false };
  }

  // In flight and recent: another worker owns this. Stand down, but this is NOT
  // a duplicate in the B-08 sense. Nothing has completed yet.
  if (nowMs - startedAt < STALE_EVENT_MS) {
    return { proceed: false, reason: 'in-flight', duplicate: false };
  }

  // In flight but old: the worker that claimed it is not coming back.
  return { proceed: true, reason: 'stale-repair', duplicate: false };
}

/**
 * Whether a disposition should answer Stripe with a 200 rather than a retryable
 * error. Every branch above is a 200: either we did the work, someone else did,
 * or someone else is doing it. A non-200 is reserved for fulfillment actually
 * throwing, which the handler decides, not this file.
 */
export function isAcknowledged(disposition) {
  return Boolean(disposition);
}
