import { json } from '@sveltejs/kit';
import Stripe from 'stripe';
import { STRIPE_SECRET_KEY, STRIPE_PRICE_ID } from '$env/static/private';
import { PUBLIC_BASE_URL } from '$env/static/public';

const stripe = new Stripe(STRIPE_SECRET_KEY);

export async function POST({ request }) {
  console.log('Received request to create checkout session');

  if (!STRIPE_SECRET_KEY || !STRIPE_PRICE_ID || !PUBLIC_BASE_URL) {
    console.error('Missing environment variables');
    console.log('STRIPE_SECRET_KEY:', STRIPE_SECRET_KEY ? 'Set' : 'Not set');
    console.log('STRIPE_PRICE_ID:', STRIPE_PRICE_ID ? 'Set' : 'Not set');
    console.log('PUBLIC_BASE_URL:', PUBLIC_BASE_URL ? 'Set' : 'Not set');
    return json({ error: 'Server configuration error' }, { status: 500 });
  }

  try {
    console.log('Creating Stripe checkout session');
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: STRIPE_PRICE_ID,
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${PUBLIC_BASE_URL}/success`,
      cancel_url: `${PUBLIC_BASE_URL}/cancel`,
    });

    console.log('Checkout session created successfully', { sessionId: session.id });
    return json({ url: session.url });
  } catch (err) {
    console.error('Error creating checkout session:', err);
    return json({ error: 'An error occurred with the payment processor.' }, { status: 500 });
  }
}