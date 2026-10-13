/**
 * Compare delivery records with both the local ledger and Stripe. Local rows
 * alone cannot reveal a paid session whose webhook/return request never arrived.
 * The external comparison covers the past seven days (including Stripe's retry
 * window); older historical reconciliation remains an explicit operator task.
 */
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { DEFAULT_GRACE_MINUTES } from './reconcileFormat.js';

// Thresholds and rendering live in a dependency-free module so they can be
// tested without a server or a database, the same reason webhookEventPolicy.js
// and adminToken.js are split that way. Re-exported here so callers have one
// import site and do not need to know about the split.
export { DEFAULT_GRACE_MINUTES, formatReconciliationReport } from './reconcileFormat.js';

const stripe = env.STRIPE_SECRET_KEY && !env.STRIPE_SECRET_KEY.startsWith('your_')
  ? new Stripe(env.STRIPE_SECRET_KEY, { apiVersion: '2024-06-20' }) : null;
const LOOKBACK_SECONDS = 7 * 24 * 60 * 60;

/**
 * Find paid sessions that never completed fulfillment.
 *
 * Reads the `unreconciled_paid_sessions` view from sql/014. The view rather than
 * a hand-built join, so the definition of "unreconciled" lives in exactly one
 * place and this function cannot drift from the SQL the way the offer copy
 * drifted from the offer.
 *
 * @param {{ graceMinutes?: number, limit?: number }} [opts]
 * @returns {Promise<object>}
 */
export async function findUnreconciled({ graceMinutes = DEFAULT_GRACE_MINUTES, limit = 100 } = {}) {
  const base = { graceMinutes, rows: [], count: 0, stripeLookbackDays: 7, checkedThrough: new Date().toISOString() };

  if (!supabaseAdmin || !stripe) {
    // Explicitly NOT reported as "ok, nothing found". A check that cannot run
    // and a check that found nothing are the same shape on the wire and must
    // never be conflated: that is how a broken monitor reads as an all-clear.
    return { ...base, ok: false, configured: false, error: 'Supabase or Stripe not configured' };
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

    const rows = new Map((data ?? []).map((row) => [row.session_id, row]));
    // Include second paid sessions explicitly flagged for a refund review,
    // even when their download email has already been sent successfully.
    const review = await supabaseAdmin.from('checkout_transactions')
      .select('session_id,email,name,edition_type,amount_total,currency,created_at,review_reason')
      .not('review_reason', 'is', null).limit(limit);
    if (review.error) throw new Error(review.error.message);
    for (const row of review.data ?? []) rows.set(row.session_id, {
      ...row, paid_at: row.created_at, fulfillment_error: row.review_reason,
    });
    let cursor;
    let scanned = 0;
    let more = false;
    const oldest = Math.floor(Date.now() / 1000) - LOOKBACK_SECONDS;
    const cutoff = Math.floor(Date.now() / 1000) - graceMinutes * 60;
    for (let page = 0; page < 10; page++) {
      const batch = await stripe.checkout.sessions.list({
        limit: 100, created: { gte: oldest, lte: cutoff },
        ...(cursor ? { starting_after: cursor } : {}),
      });
      scanned += batch.data.length;
      const paid = batch.data.filter((session) => session.payment_status === 'paid'
        && session.metadata?.product === 'early-access-bundle-v1');
      if (paid.length) {
        const ledger = await supabaseAdmin.from('checkout_transactions')
          .select('session_id,status,fulfilled').in('session_id', paid.map((session) => session.id));
        if (ledger.error) throw new Error(ledger.error.message);
        const recorded = new Map((ledger.data ?? []).map((row) => [row.session_id, row]));
        for (const session of paid) {
          const local = recorded.get(session.id);
          if (local?.status === 'completed' && local.fulfilled) continue;
          if (rows.has(session.id)) continue;
          rows.set(session.id, {
            session_id: session.id,
            email: session.customer_details?.email ?? session.customer_email,
            name: session.customer_details?.name ?? '',
            edition_type: session.metadata?.edition_type ?? 'standard',
            amount_total: session.amount_total, currency: session.currency,
            paid_at: new Date(session.created * 1000).toISOString(),
            minutes_outstanding: Math.floor((Date.now() / 1000 - session.created) / 60),
            never_claimed: !local,
            fulfillment_error: !local ? 'Paid in Stripe; absent from local ledger' : 'Paid in Stripe; fulfillment incomplete',
            source: 'stripe',
          });
        }
      }
      more = batch.has_more;
      if (!more) break;
      cursor = batch.data.at(-1)?.id;
      if (!cursor) throw new Error('Stripe reconciliation pagination did not advance');
    }
    const incomplete = more || data?.length === limit || review.data?.length === limit;
    const result = [...rows.values()];
    return {
      ...base, ok: !incomplete, configured: true, rows: result, count: result.length, scanned,
      ...(incomplete ? { error: 'Reconciliation scan reached its limit; this is not an all-clear' } : {}),
    };
  } catch (e) {
    return { ...base, ok: false, configured: true, error: e?.message ?? String(e) };
  }
}
