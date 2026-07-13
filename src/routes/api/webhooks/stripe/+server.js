import { json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { fulfillPreorder } from '$lib/server/fulfillment.js';

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
    event = stripe.webhooks.constructEvent(rawBody, signature, WEBHOOK_SECRET);
  } catch (err) {
    console.error('[webhook] signature verification failed:', err.message);
    return json({ error: 'Invalid signature' }, { status: 400 });
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

    if (email) {
      try {
        await fulfillPreorder({ sessionId: session.id, email, name, editionType });
      } catch (err) {
        console.error('[webhook] fulfillPreorder threw:', err.message);
        // 500 so Stripe retries with backoff instead of a transient failure
        // silently dropping a real paid order.
        return json({ error: 'Fulfillment failed' }, { status: 500 });
      }
    }
  }

  return json({ received: true });
}
