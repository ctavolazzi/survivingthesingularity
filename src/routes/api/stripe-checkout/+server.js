import { json, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';

const PRICE_ID      = env.STRIPE_PRICE_ID;
const SECRET_KEY    = env.STRIPE_SECRET_KEY;
const PUBLIC_BASE   = env.PUBLIC_BASE_URL || 'http://localhost:5173';

// Graceful: if no Stripe key, we run in mock mode so the rest of the UI
// can be tested without credentials. Remove the mock branch before launch.
const isMockKey = !SECRET_KEY || SECRET_KEY === 'placeholder' || SECRET_KEY.startsWith('your_');
const stripe = isMockKey ? null : new Stripe(SECRET_KEY, { apiVersion: '2024-06-20' });

/** @type {import('./$types').RequestHandler} */
export async function POST({ request, url }) {
  const origin = request.headers.get('origin');
  if (origin && origin !== url.origin) {
    return json({ error: 'Bad request.' }, { status: 403 });
  }

  // MOCK MODE — no Stripe key configured yet. Use request origin so the
  // redirect works on any dev port without touching PUBLIC_BASE_URL.
  const isMockPrice = !PRICE_ID || PRICE_ID === 'placeholder' || PRICE_ID.startsWith('your_');
  if (!stripe || isMockPrice) {
    return json({
      url: `${url.origin}/early-access/success?session_id=mock_session`,
    });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items: [{ price: PRICE_ID, quantity: 1 }],
      success_url: `${PUBLIC_BASE}/early-access/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url:  `${PUBLIC_BASE}/early-access`,
      // Collect email so we can send the download link.
      customer_email: undefined, // Stripe will ask on checkout
      metadata: { product: 'early-access-bundle-v1' },
      allow_promotion_codes: true,
      billing_address_collection: 'auto',
    });

    return json({ url: session.url });
  } catch (err) {
    console.error('[stripe-checkout]', err.message);
    return json({ error: 'Could not create checkout session.' }, { status: 500 });
  }
}
