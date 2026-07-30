/**
 * RECONCILIATION: money arrived and the customer has nothing to show for it.
 * Plan item B-06.
 *
 * WHY THIS CANNOT BE DONE INLINE
 *
 * The failure being detected is a webhook that never arrived. When that happens
 * none of our code runs, so no amount of care inside the handler can notice it.
 * Detection has to come from comparing two records after the fact: Stripe said
 * paid (recorded in `checkout_transactions`) against we delivered (recorded in
 * `fulfilled_sessions`). On 2026-07-29 that comparison stood at 23 paid sessions
 * against 13 delivery rows, and nothing had noticed for as long as it had been
 * true. All test mode, no money lost, which is the only reason it is a P1 and
 * not an emergency.
 *
 * THIS MODULE DOES NOT SCHEDULE ITSELF
 *
 * It cannot. The site deploys to Cloudflare Pages, which has no cron trigger of
 * its own, so something outside has to call the endpoint that wraps this. Until
 * that caller exists, the check is on-demand only, and an on-demand check that
 * nobody demands is not an alert. Do not record B-06 as closed on the strength
 * of this module alone.
 */
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { DEFAULT_GRACE_MINUTES } from './reconcileFormat.js';

// Thresholds and rendering live in a dependency-free module so they can be
// tested without a server or a database, the same reason webhookEventPolicy.js
// and adminToken.js are split that way. Re-exported here so callers have one
// import site and do not need to know about the split.
export { DEFAULT_GRACE_MINUTES, formatReconciliationReport } from './reconcileFormat.js';

/**
 * Find paid sessions that never completed fulfillment.
 *
 * Reads the `unreconciled_paid_sessions` view from sql/014. The view rather than
 * a hand-built join, so the definition of "unreconciled" lives in exactly one
 * place and this function cannot drift from the SQL the way the offer copy
 * drifted from the offer.
 *
 * @param {{ graceMinutes?: number, limit?: number }} [opts]
 * @returns {Promise<{ ok: boolean, configured: boolean, rows: object[], count: number, error?: string, graceMinutes: number }>}
 */
export async function findUnreconciled({ graceMinutes = DEFAULT_GRACE_MINUTES, limit = 100 } = {}) {
  const base = { graceMinutes, rows: [], count: 0 };

  if (!supabaseAdmin) {
    // Explicitly NOT reported as "ok, nothing found". A check that cannot run
    // and a check that found nothing are the same shape on the wire and must
    // never be conflated: that is how a broken monitor reads as an all-clear.
    return { ...base, ok: false, configured: false, error: 'Supabase not configured' };
  }

  try {
    const { data, error } = await supabaseAdmin
      .from('unreconciled_paid_sessions')
      .select('*')
      .gte('minutes_outstanding', graceMinutes)
      .order('paid_at', { ascending: true })
      .limit(limit);

    if (error) {
      const missingView = error.code === 'PGRST205' || error.code === 'PGRST204';
      return {
        ...base,
        ok: false,
        configured: true,
        error: error.message + (missingView ? ' (run sql/014_webhook_events.sql)' : ''),
      };
    }

    const rows = data ?? [];
    return { ...base, ok: true, configured: true, rows, count: rows.length };
  } catch (e) {
    return { ...base, ok: false, configured: true, error: e?.message ?? String(e) };
  }
}
