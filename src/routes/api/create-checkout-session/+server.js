import { json } from '@sveltejs/kit';
import Stripe from 'stripe';
import { STRIPE_SECRET_KEY, STRIPE_PRICE_ID } from '$env/static/private';
import { PUBLIC_BASE_URL } from '$env/static/public';

// Initialize Stripe with API version
const stripe = new Stripe(STRIPE_SECRET_KEY, {
  apiVersion: '2023-10-16', // Specify API version for stability
});

/**
 * Creates a Stripe checkout session for purchasing the book
 */
export async function POST({ request, getClientAddress }) {
  const clientIp = getClientAddress();
  console.log(`Received checkout request from ${clientIp}`);

  // Validate environment variables
  if (!STRIPE_SECRET_KEY || !STRIPE_PRICE_ID || !PUBLIC_BASE_URL) {
    const missingVars = [];
    if (!STRIPE_SECRET_KEY) missingVars.push('STRIPE_SECRET_KEY');
    if (!STRIPE_PRICE_ID) missingVars.push('STRIPE_PRICE_ID');
    if (!PUBLIC_BASE_URL) missingVars.push('PUBLIC_BASE_URL');

    console.error(`Missing required environment variables: ${missingVars.join(', ')}`);
    return json({
      error: 'Server configuration error',
      details: 'Missing required environment variables'
    }, { status: 500 });
  }

  try {
    // Parse request body for customization options
    let customData = {};
    try {
      customData = await request.json();
    } catch (e) {
      // If parsing fails, continue with default options
      console.log('No custom checkout options provided');
    }

    const { quantity = 1, metadata = {} } = customData;

    console.log('Creating Stripe checkout session');
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: STRIPE_PRICE_ID,
          quantity,
        },
      ],
      mode: 'payment',
      success_url: `${PUBLIC_BASE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${PUBLIC_BASE_URL}/cancel`,
      metadata: {
        ...metadata,
        source: 'website',
        timestamp: new Date().toISOString(),
      },
    });

    console.log('Checkout session created successfully', {
      sessionId: session.id,
      amount: session.amount_total,
      currency: session.currency
    });

    return json({ url: session.url, sessionId: session.id });
  } catch (err) {
    console.error('Error creating checkout session:', {
      message: err.message,
      type: err.type,
      code: err.code,
      statusCode: err.statusCode
    });

    // Return appropriate error based on the type
    if (err.type === 'StripeCardError') {
      return json({ error: 'Your card was declined. Please try again with a different payment method.' }, { status: 400 });
    } else if (err.type === 'StripeRateLimitError') {
      return json({ error: 'Too many requests. Please try again after a short delay.' }, { status: 429 });
    } else if (err.type === 'StripeInvalidRequestError') {
      return json({ error: 'Invalid request parameters.' }, { status: 400 });
    } else {
      return json({ error: 'An error occurred with the payment processor.' }, { status: 500 });
    }
  }
}