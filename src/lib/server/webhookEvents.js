/**
 * The database side of webhook event idempotency (plan item B-08).
 *
 * Thin on purpose. Every interesting decision lives in webhookEventPolicy.js,
 * which has no dependencies and is therefore exhaustively tested in
 * tests/e2e/j-webhook-event-policy.spec.js. What is left here is the Supabase
 * plumbing, kept boring so that reading it is enough to trust it.
 *
 * EVERY FUNCTION HERE DEGRADES OPEN.
 *
 * If the events table is missing, unreachable, or Supabase is not configured at
 * all, these return "proceed" rather than blocking. That direction is chosen
 * deliberately and it is the opposite of what a dedup layer usually wants:
 *
 *   failing open  -> at worst a redundant claimSession call that stands down
 *   failing shut  -> a paid order silently never fulfilled
 *
 * This layer is an audit trail and an optimisation. `claimSession` in
 * fulfillment.js, backed by the unique constraint on
 * fulfilled_sessions.session_id, is the actual safety net. A bookkeeping table
 * must never be able to take down the pipeline it is only observing, which is
 * the same principle transactions.js states for the checkout ledger.
 */
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import {
  decideEventDisposition,
  PROCESSED,
  FAILED,
  PROCESSING
} from './webhookEventPolicy.js';

/** Shared error reporting so a missing migration is named rather than guessed at. */
function report(op, eventId, error) {
  if (!error) return;
  console.error(
    `[webhook-events] ${op} failed for ${eventId}: ${error.message}` +
      (error.code === 'PGRST205' || error.code === 'PGRST204'
        ? ' (run sql/014_webhook_events.sql)'
        : '')
  );
}

/**
 * Claim an event id before doing any work, and report what to do about it.
 *
 * The insert is the detection mechanism: a 23505 unique violation means we have
 * seen this event id before, and only then do we look at what state the prior
 * attempt reached.
 *
 * @param {{ eventId: string, type: string, livemode?: boolean|null, sessionId?: string|null }} args
 * @returns {Promise<{ proceed: boolean, reason: string, duplicate: boolean }>}
 */
export async function beginEvent({ eventId, type, livemode = null, sessionId = null }) {
  if (!supabaseAdmin || !eventId) {
    return { proceed: true, reason: 'no-database', duplicate: false };
  }

  try {
    const { error } = await supabaseAdmin.from('webhook_events').insert({
      event_id: eventId,
      type,
      livemode,
      session_id: sessionId,
      status: PROCESSING
    });

    if (!error) return decideEventDisposition(null, Date.now());

    if (error.code !== '23505') {
      // Could not record the event. Do NOT let bookkeeping stop a real order.
      report('beginEvent insert', eventId, error);
      return { proceed: true, reason: 'insert-failed-proceeding', duplicate: false };
    }

    const { data: existing, error: lookupErr } = await supabaseAdmin
      .from('webhook_events')
      .select('status, received_at, attempts')
      .eq('event_id', eventId)
      .maybeSingle();

    if (lookupErr || !existing) {
      console.error(
        `[webhook-events] conflict on ${eventId} but lookup failed; proceeding rather than risk a lost order:`,
        lookupErr?.message ?? 'no row'
      );
      return { proceed: true, reason: 'lookup-failed-proceeding', duplicate: false };
    }

    const disposition = decideEventDisposition(existing, Date.now());

    // Standing down: leave the row exactly as it is. Bumping attempts here would
    // make a healthy in-flight race look like a wedged retry loop.
    if (!disposition.proceed) {
      console.warn(
        `[webhook-events] ${eventId} not reprocessed (${disposition.reason}, status ${existing.status}).`
      );
      return disposition;
    }

    // Repairing. Restart the attempt clock so the staleness window measures THIS
    // attempt, and bump the counter so a wedged event is visible in the table.
    // first_seen_at is untouched by design; it is the audit trail.
    const attempts = (existing.attempts ?? 1) + 1;
    const { error: updateErr } = await supabaseAdmin
      .from('webhook_events')
      .update({
        status: PROCESSING,
        attempts,
        received_at: new Date().toISOString(),
        completed_at: null
      })
      .eq('event_id', eventId);
    report('beginEvent repair', eventId, updateErr);

    console.warn(
      `[webhook-events] reprocessing ${eventId} (${disposition.reason}, ` +
        `prior status ${existing.status}, attempt ${attempts}).`
    );
    return disposition;
  } catch (e) {
    console.error('[webhook-events] beginEvent threw:', e?.message ?? e);
    return { proceed: true, reason: 'threw-proceeding', duplicate: false };
  }
}

/**
 * Record how handling ended. Best-effort and never throws: failing to write the
 * outcome must not undo work that already happened.
 *
 * `status = 'processed'` is what makes a redelivery safe to skip, so writing it
 * is what closes the loop. An event stuck in 'processing' will be repaired by
 * the next delivery once it goes stale, which is the intended failure mode: the
 * system errs toward doing the work again rather than assuming it was done.
 */
async function markEventOutcome(eventId, status, lastError = null) {
  if (!supabaseAdmin || !eventId) return;
  try {
    const { error } = await supabaseAdmin
      .from('webhook_events')
      .update({
        status,
        completed_at: new Date().toISOString(),
        last_error: lastError ? String(lastError).slice(0, 500) : null
      })
      .eq('event_id', eventId);
    report(`markEventOutcome(${status})`, eventId, error);
  } catch (e) {
    console.error('[webhook-events] markEventOutcome threw:', e?.message ?? e);
  }
}

/**
 * Handling finished successfully. Includes the case where the correct handling
 * was to do nothing, such as an event type nothing subscribes to: we did
 * complete our handling of it, and marking it 'processed' is what stops it being
 * mistaken for an unfinished job in the operational queue.
 */
export async function markEventProcessed(eventId) {
  await markEventOutcome(eventId, PROCESSED);
}

/**
 * Handling ran and failed. Explicitly retryable: the next delivery of this same
 * event id will be allowed straight through by the policy.
 */
export async function markEventFailed(eventId, error) {
  await markEventOutcome(eventId, FAILED, error);
}
