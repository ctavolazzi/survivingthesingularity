/**
 * The durable ledger of every checkout attempt: created, paid, expired, or
 * abandoned. Written by `checkout_transactions` (sql/013_checkout_durability.sql)
 * and never purged.
 *
 * WHY THIS IS SEPARATE FROM `preorders`
 *
 * `preorders` carries a unique constraint on (email, edition_type), which is
 * what enforces one copy per customer. That is correct for a product catalogue
 * and useless as a financial record: a repeat purchase writes no row at all.
 * Live data on 2026-07-29 showed 12 completed Stripe sessions producing 3
 * preorder rows. The other 9 payments existed only in `fulfilled_sessions`,
 * which is a 30-day dedup cache. There was no answer to "who paid us, when,
 * and how much" that came from our own database.
 *
 * So: one row per SESSION, not per customer. Repeat purchases, expiries and
 * abandoned carts all get a row, because all three are things you eventually
 * want to count.
 *
 * Every function here is best-effort and never throws. The ledger is
 * redundancy against Stripe; failing to write it must never take down the
 * fulfillment it is recording. A missing ledger row is a reporting gap, a
 * thrown error here would be a lost order.
 */
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';

/** Shared error reporting so a missing migration is named rather than guessed at. */
function report(op, sessionId, error) {
  if (!error) return;
  console.error(
    `[transactions] ${op} failed for ${sessionId}: ${error.message}` +
    (error.code === 'PGRST205' || error.code === 'PGRST204'
      ? ' (run sql/013_checkout_durability.sql)'
      : '')
  );
}

/**
 * Record that a checkout session was created. The customer may never pay, and
 * that is precisely why this is written: without it, an abandoned checkout is
 * indistinguishable from a checkout that never happened.
 *
 * No email here on purpose. Stripe collects the address during checkout, so at
 * creation time we genuinely do not know who this is. An abandoned cart is
 * anonymous, which is a fact about the flow rather than a hole in the logging.
 *
 * @param {{ sessionId: string, editionType?: string, amountTotal?: number|null, currency?: string|null }} args
 */
export async function recordCheckoutInitiated({ sessionId, editionType = 'standard', amountTotal = null, currency = null }) {
  if (!supabaseAdmin || !sessionId) return;
  try {
    const { error } = await supabaseAdmin.from('checkout_transactions').insert({
      session_id: sessionId,
      edition_type: editionType,
      amount_total: amountTotal,
      currency,
      status: 'initiated',
    });
    // 23505 means the webhook beat us to it, which is fine and expected under
    // load - the session is already on the ledger either way.
    if (error && error.code !== '23505') report('recordCheckoutInitiated', sessionId, error);
  } catch (e) {
    console.error('[transactions] recordCheckoutInitiated threw:', e?.message ?? e);
  }
}

/**
 * Record that Stripe confirmed payment. Upserts, because the webhook and the
 * success page both reach this and either may arrive first - and because a
 * session created before sql/013 shipped has no `initiated` row to update.
 *
 * @param {{ sessionId: string, paymentIntent?: string|null, email?: string|null, name?: string, editionType?: string, amountTotal?: number|null, currency?: string|null }} args
 */
export async function recordCheckoutCompleted({
  sessionId, paymentIntent = null, email = null, name = '',
  editionType = 'standard', amountTotal = null, currency = null,
}) {
  if (!supabaseAdmin || !sessionId) return;
  try {
    const { error } = await supabaseAdmin
      .from('checkout_transactions')
      .upsert(
        {
          session_id: sessionId,
          payment_intent: paymentIntent,
          email,
          name,
          edition_type: editionType,
          amount_total: amountTotal,
          currency,
          status: 'completed',
        },
        { onConflict: 'session_id' }
      );
    report('recordCheckoutCompleted', sessionId, error);
  } catch (e) {
    console.error('[transactions] recordCheckoutCompleted threw:', e?.message ?? e);
  }
}

/**
 * Record that Stripe expired the session: the customer started checkout and
 * never finished. This is the abandoned-cart signal.
 *
 * Guarded so a late `expired` event can never overwrite a `completed` row.
 * Stripe can deliver events out of order, and silently downgrading a paid
 * order to "abandoned" would be worse than not recording the expiry at all.
 */
export async function recordCheckoutExpired(sessionId) {
  if (!supabaseAdmin || !sessionId) return;
  try {
    const { error } = await supabaseAdmin
      .from('checkout_transactions')
      .update({ status: 'expired' })
      .eq('session_id', sessionId)
      .eq('status', 'initiated');
    report('recordCheckoutExpired', sessionId, error);
  } catch (e) {
    console.error('[transactions] recordCheckoutExpired threw:', e?.message ?? e);
  }
}

/**
 * Flag that fulfillment ran for this session. Kept separate from payment
 * status deliberately: "they paid" and "they received it" are different
 * questions, and conflating them is how a dropped delivery stays invisible.
 *
 * `where status = 'completed' and fulfilled = false` is the query that finds a
 * paid order nobody delivered.
 */
export async function markTransactionFulfilled(sessionId) {
  if (!supabaseAdmin || !sessionId) return;
  try {
    const { error } = await supabaseAdmin
      .from('checkout_transactions')
      .update({ fulfilled: true })
      .eq('session_id', sessionId);
    report('markTransactionFulfilled', sessionId, error);
  } catch (e) {
    console.error('[transactions] markTransactionFulfilled threw:', e?.message ?? e);
  }
}
