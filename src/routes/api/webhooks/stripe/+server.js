import { json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { fulfillPreorder } from '$lib/server/fulfillment.js';
import {
  recordCheckoutCompleted,
  recordCheckoutExpired,
  markTransactionFulfilled,
} from '$lib/server/transactions.js';

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

  // The customer started checkout and never finished. Recorded, not acted on:
  // the ask was to be able to see that it happened, not to chase it. Without
  // this event an abandoned cart is indistinguishable from a cart that never
  // existed, because nothing else in the system ever hears about it.
  if (event.type === 'checkout.session.expired') {
    await recordCheckoutExpired(event.data.object.id);
    return json({ received: true });
  }

  if (event.type === 'checkout.session.completed' || event.type === 'checkout.session.async_payment_succeeded') {
    const session = event.data.object;

    // checkout.session.completed can fire before an async payment method
    // (bank transfer, etc.) actually clears; async_payment_succeeded is what
    // confirms those. Card payments are synchronous and already paid here.
    if (session.payment_status !== 'paid') {
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
    await recordCheckoutCompleted({
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

    if (!email) {
      // Nothing to deliver to, but the payment is now on the ledger and will
      // show up in the "completed but not fulfilled" report rather than
      // vanishing.
      console.error(`[webhook] paid session ${session.id} has no customer email; recorded but not fulfilled.`);
      return json({ received: true });
    }

    try {
      const result = await fulfillPreorder({ sessionId: session.id, email, name, editionType });
      // Only claim fulfilment when this call actually delivered. `alreadyFulfilled`
      // means another worker owns it and will set the flag itself.
      if (result?.delivered) await markTransactionFulfilled(session.id);
    } catch (err) {
      console.error('[webhook] fulfillPreorder threw:', err.message);
      // 500 so Stripe retries with backoff instead of a transient failure
      // silently dropping a real paid order. The retry is now genuinely useful:
      // claimSession repairs its own stale claim rather than treating the
      // half-finished first attempt as done.
      return json({ error: 'Fulfillment failed' }, { status: 500 });
    }
  }

  return json({ received: true });
}
