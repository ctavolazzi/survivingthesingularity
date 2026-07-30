import { json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { fulfillPreorder } from '$lib/server/fulfillment.js';
import {
  recordCheckoutCompleted,
  recordCheckoutExpired,
  markTransactionFulfilled,
} from '$lib/server/transactions.js';
import {
  beginEvent,
  markEventProcessed,
  markEventFailed,
} from '$lib/server/webhookEvents.js';

const SECRET_KEY = env.STRIPE_SECRET_KEY;
const WEBHOOK_SECRET = env.STRIPE_WEBHOOK_SECRET;

const stripe = SECRET_KEY && !SECRET_KEY.startsWith('your_')
  ? new Stripe(SECRET_KEY, { apiVersion: '2024-06-20' })
  : null;

/**
 * Source of truth for preorder fulfillment. Stripe calls this directly
 * server-to-server the moment a checkout session completes, independent of
 * whether the customer's browser ever makes it back to /early-access/success
 * (closed tab, dropped connection, crashed browser mid-redirect - all
 * covered). The success page's own fulfillment call is a fast path for the
 * common case; this is what guarantees a paid order is never silently lost.
 *
 * @type {import('./$types').RequestHandler}
 */
export async function POST({ request }) {
  if (!stripe || !WEBHOOK_SECRET) {
    console.error('[webhook] Stripe/webhook secret not configured; rejecting.');
    return json({ error: 'Not configured' }, { status: 503 });
  }

  const signature = request.headers.get('stripe-signature');
  if (!signature) {
    return json({ error: 'Missing signature' }, { status: 400 });
  }

  // Signature verification needs the exact raw body bytes; a JSON.parse ->
  // JSON.stringify round trip would change whitespace/key order and break
  // the HMAC check, so read it as text and hand Stripe's SDK the raw string.
  const rawBody = await request.text();

  let event;
  try {
    // MUST be constructEventAsync, not constructEvent. In production this runs
    // on the Cloudflare Workers runtime, where the Stripe SDK resolves its
    // "workerd" export condition and its crypto provider is SubtleCrypto -
    // which is async-only. The synchronous constructEvent therefore throws
    // CryptoProviderOnlySupportsAsyncError on EVERY request, whatever the
    // secret, and the catch below turns that into an indistinguishable
    // "Invalid signature" 400. The async form picks the right provider on both
    // the worker build (SubtleCrypto) and the node build used by local dev.
    event = await stripe.webhooks.constructEventAsync(rawBody, signature, WEBHOOK_SECRET);
  } catch (err) {
    // A crypto-provider/config fault and a genuinely bad signature both landed
    // here as the same opaque message, which cost a long night of chasing the
    // wrong cause. Keep them distinguishable in the logs.
    const misconfigured = err?.type !== 'StripeSignatureVerificationError';
    console.error(
      misconfigured
        ? `[webhook] verification could not run (likely misconfiguration): ${err?.constructor?.name}: ${err?.message}`
        : `[webhook] signature rejected: ${err.message}`
    );
    return json({ error: 'Invalid signature' }, { status: 400 });
  }

  // Event-level bookkeeping and replay detection (B-08). Claimed AFTER signature
  // verification so an unsigned or forged payload can never write a row, and
  // BEFORE any handling so a replay is recognised before it does work twice.
  //
  // `proceed: false` is not an error and must answer 200: either this exact
  // event was already handled to completion, or another worker is handling it
  // right now. Returning anything else would make Stripe retry a duplicate.
  //
  // Read webhookEventPolicy.js before changing this. Stripe REUSES the event id
  // on retries, so "seen before" is emphatically not "already handled", and a
  // dedup that skips retries would silently strand paid orders whose first
  // attempt failed.
  const disposition = await beginEvent({
    eventId: event.id,
    type: event.type,
    livemode: event.livemode ?? null,
    sessionId: event.data?.object?.id ?? null,
  });

  if (!disposition.proceed) {
    return json({
      received: true,
      duplicate: disposition.duplicate,
      reason: disposition.reason,
    });
  }

  // The customer started checkout and never finished. Recorded, not acted on:
  // the ask was to be able to see that it happened, not to chase it. Without
  // this event an abandoned cart is indistinguishable from a cart that never
  // existed, because nothing else in the system ever hears about it.
  if (event.type === 'checkout.session.expired') {
    await recordCheckoutExpired(event.data.object.id);
    await markEventProcessed(event.id);
    return json({ received: true });
  }

  if (event.type === 'checkout.session.completed' || event.type === 'checkout.session.async_payment_succeeded') {
    const session = event.data.object;

    // checkout.session.completed can fire before an async payment method
    // (bank transfer, etc.) actually clears; async_payment_succeeded is what
    // confirms those. Card payments are synchronous and already paid here.
    if (session.payment_status !== 'paid') {
      // Handled correctly by doing nothing: async_payment_succeeded will follow
      // if it ever clears. Marked processed so it does not sit in the
      // unfinished-events queue looking like a stuck job.
      await markEventProcessed(event.id);
      return json({ received: true });
    }

    const email = session.customer_details?.email ?? session.customer_email ?? null;
    const name = session.customer_details?.name ?? '';
    const editionType = session.metadata?.edition_type === 'authors' ? 'authors' : 'standard';

    // Ledger first, and unconditionally. This runs before fulfillment and
    // outside the `if (email)` guard on purpose: the money moved whether or not
    // we can identify the buyer or successfully deliver to them, and that fact
    // must survive every failure below it. Previously a session with no email
    // returned 200 having recorded nothing anywhere.
    const ledger = await recordCheckoutCompleted({
      sessionId: session.id,
      paymentIntent: typeof session.payment_intent === 'string'
        ? session.payment_intent
        : session.payment_intent?.id ?? null,
      email,
      name,
      editionType,
      amountTotal: session.amount_total ?? null,
      currency: session.currency ?? null,
    });

    /**
     * THE FINANCIAL LEDGER FAILS CLOSED. The event audit trail does not.
     *
     * This is the one place the degrade-open rule is deliberately inverted, and
     * the reasoning is worth keeping because the two layers now behave
     * differently on purpose:
     *
     *   webhook_events    an audit trail. Losing a row costs a report, so it
     *                     degrades OPEN and never blocks a paid order.
     *   checkout_transactions  the financial record. Losing a row destroys
     *                     chargeback defence and makes reconciliation
     *                     impossible, and Stripe will retry for about three
     *                     days at no cost. So it fails CLOSED.
     *
     * Answering 200 here when the write failed is what makes the loss
     * permanent: Stripe treats 200 as delivered and stops retrying. Returning
     * 500 costs a retry and keeps the order recoverable.
     *
     * SAFE BECAUSE OF WHERE IT SITS. This runs BEFORE fulfillPreorder, which is
     * where every email is sent, so a retry triggered here cannot re-send
     * anything to the customer. Verified by reading the order of operations: the
     * ledger write is line ~133 and fulfillment is line ~160. If anyone ever
     * moves fulfillment above this point, this early return becomes a
     * duplicate-email generator, so keep the ordering.
     *
     * `configured: false` means no database is wired up at all, which is the
     * normal state in local dev. That must NOT 500, or every local webhook and
     * every run of scripts/probe-stripe-webhook.mjs starts failing.
     */
    if (ledger.configured && !ledger.ok) {
      console.error(
        `[webhook] LEDGER WRITE FAILED for paid session ${session.id}: ${ledger.error}. ` +
          'Returning 500 so Stripe retries; no email has been sent yet.'
      );
      await markEventFailed(event.id, `ledger write failed: ${ledger.error}`);
      return json({ error: 'Ledger write failed' }, { status: 500 });
    }

    if (!email) {
      // Nothing to deliver to, but the payment is now on the ledger and will
      // show up in the "completed but not fulfilled" report rather than
      // vanishing.
      console.error(`[webhook] paid session ${session.id} has no customer email; recorded but not fulfilled.`);
      // Our handling of the event is complete; there is nothing further this
      // code can do. The order still shows up in the B-06 reconciliation view
      // as paid and unfulfilled, which is where a human needs to see it. A
      // Stripe retry cannot conjure an email address, so leaving this
      // retryable would only produce noise.
      await markEventProcessed(event.id);
      return json({ received: true });
    }

    try {
      const result = await fulfillPreorder({ sessionId: session.id, email, name, editionType });
      // Only claim fulfilment when this call actually delivered. `alreadyFulfilled`
      // means another worker owns it and will set the flag itself.
      if (result?.delivered) await markTransactionFulfilled(session.id);
    } catch (err) {
      console.error('[webhook] fulfillPreorder threw:', err.message);
      // Mark FAILED, not processed. This is what makes the retry below actually
      // work: the policy lets a failed event straight back through, so the next
      // delivery repairs rather than being mistaken for a duplicate.
      await markEventFailed(event.id, err.message);
      // 500 so Stripe retries with backoff instead of a transient failure
      // silently dropping a real paid order. The retry is now genuinely useful:
      // claimSession repairs its own stale claim rather than treating the
      // half-finished first attempt as done.
      return json({ error: 'Fulfillment failed' }, { status: 500 });
    }
  }

  // Reached by a successful paid session and by any event type nothing above
  // subscribes to. Both are finished handling, so both are 'processed'.
  await markEventProcessed(event.id);
  return json({ received: true });
}
