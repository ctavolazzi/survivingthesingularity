import { json, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { dev } from '$app/environment';
import Stripe from 'stripe';
import { rateLimit } from '$lib/server/rateLimit.js';

const PRICE_ID      = env.STRIPE_PRICE_ID;
const SECRET_KEY    = env.STRIPE_SECRET_KEY;

// Per-edition Stripe prices. Falls back to the shared STRIPE_PRICE_ID so the
// endpoint keeps working if the edition-specific vars aren't set.
const EDITION_PRICE_IDS = {
  standard: env.STRIPE_PRICE_ID_STANDARD || PRICE_ID,
  authors:  env.STRIPE_PRICE_ID_AUTHORS  || PRICE_ID,
};

// Graceful: if no Stripe key, we run in mock mode so the rest of the UI
// can be tested without credentials. Remove the mock branch before launch.
const isMockKey = !SECRET_KEY || SECRET_KEY === 'placeholder' || SECRET_KEY.startsWith('your_');
const stripe = isMockKey ? null : new Stripe(SECRET_KEY, { apiVersion: '2024-06-20' });

/** @type {import('./$types').RequestHandler} */
export async function POST({ request, url, getClientAddress }) {
  const origin = request.headers.get('origin');
  if (origin && origin !== url.origin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  const contentType = request.headers.get('content-type') ?? '';
  if (!contentType.includes('application/json')) {
    return json({ error: 'Bad request.' }, { status: 400 });
  }

  const ip = getClientAddress();
  const { allowed } = rateLimit(`stripe:${ip}`, 5, 10 * 60_000);
  if (!allowed) {
    return json({ error: 'Too many requests.' }, { status: 429 });
  }

  const body = await request.json().catch(() => ({}));
  const editionType = body.edition_type === 'authors' ? 'authors' : 'standard';
  const priceId = EDITION_PRICE_IDS[editionType];

  // MOCK MODE - dev-only. Lets the UI be tested without Stripe credentials.
  // In production, a missing/placeholder key must fail loudly, not fake a
  // successful checkout for a real customer.
  const isMockPrice = !priceId || priceId === 'placeholder' || priceId.startsWith('your_');
  if (!stripe || isMockPrice) {
    if (!dev) {
      console.error('[stripe-checkout] Missing Stripe credentials in production.');
      return json({ error: 'Checkout is temporarily unavailable. Please try again shortly.' }, { status: 503 });
    }
    return json({
      url: `${url.origin}/early-access/success?session_id=mock_session`,
    });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${url.origin}/early-access/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url:  `${url.origin}/early-access`,
      customer_email: undefined,
      metadata: { product: 'early-access-bundle-v1', edition_type: editionType },
      allow_promotion_codes: true,
      billing_address_collection: 'auto',
    });

    return json({ url: session.url });
  } catch (err) {
    console.error('[stripe-checkout]', err.message);
    return json({ error: 'Could not create checkout session.' }, { status: 500 });
  }
}
