import { json, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { dev } from '$app/environment';
import Stripe from 'stripe';
import { rateLimit } from '$lib/server/rateLimit.js';

const PRICE_ID      = env.STRIPE_PRICE_ID;
const SECRET_KEY    = env.STRIPE_SECRET_KEY;

// Per-edition Stripe prices.
//
// The shared STRIPE_PRICE_ID is a convenience fallback for local dev, where
// having one variable set is enough to exercise the flow. In production it is a
// hazard: an unset, misspelled, or dropped edition variable does not fail - it
// silently bills whatever the shared one happens to point at. That is exactly
// the shape of the 2026-07 defect where a $5 product charged $9, and it is the
// shape of a live bug right now, since STRIPE_PRICE_ID_AUTHORS is not set in
// production and `authors` therefore resolves to the standard price. The
// endpoint accepts edition_type from any caller, so that path is reachable
// whether or not the UI exposes a button for it.
//
// So: dev keeps the fallback, production demands the edition's own variable and
// refuses the sale without it. Refusing is the safe failure - a customer who
// cannot check out complains; a customer billed the wrong amount may not.
const EDITION_PRICE_IDS = {
  standard: env.STRIPE_PRICE_ID_STANDARD || (dev ? PRICE_ID : undefined),
  authors:  env.STRIPE_PRICE_ID_AUTHORS  || (dev ? PRICE_ID : undefined),
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
      // Name the actual cause. These two failures need completely different
      // fixes, and "missing credentials" sends whoever reads this log hunting
      // for an API key that is fine.
      const cause = !stripe
        ? 'STRIPE_SECRET_KEY is missing or a placeholder'
        : `no price configured for the "${editionType}" edition - set STRIPE_PRICE_ID_${editionType.toUpperCase()} in the production environment`;
      console.error(`[stripe-checkout] Refusing checkout: ${cause}.`);
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
      // PREORDER50 is a 50%-off `duration: once` coupon that is emailed to
      // every customer, and it is meant for the FUTURE book launch - not for
      // this $5 preorder. Stripe applies a promotion code to whatever is in
      // the cart, so leaving the promo box on THIS checkout would let anyone
      // holding that code buy the preorder for $2.50, and the code is a fixed
      // string sitting in every buyer's inbox. Off unless deliberately
      // enabled; turn it on only once the live coupon is restricted to the
      // product it is actually for (Stripe coupon -> Applies to -> specific
      // product), so enabling promos here cannot reopen the discount hole.
      allow_promotion_codes: env.ALLOW_PROMOTION_CODES === 'true',
      billing_address_collection: 'auto',
    });

    return json({ url: session.url });
  } catch (err) {
    console.error('[stripe-checkout]', err.message);
    return json({ error: 'Could not create checkout session.' }, { status: 500 });
  }
}
