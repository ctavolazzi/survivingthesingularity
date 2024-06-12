import Stripe from 'stripe';
import { SECRET_STRIPE_KEY_TEST } from '$env/static/private';

const stripe = new Stripe(SECRET_STRIPE_KEY_TEST);

export async function POST({ request }) {
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', {
      status: 405,
      headers: { 'Allow': 'POST' },
    });
  }

  try {
    console.log('Environment Variable SECRET_STRIPE_KEY_TEST:', SECRET_STRIPE_KEY_TEST);
    const requestBody = await request.json();
    console.log('Request Body:', requestBody);

    const { priceId } = requestBody;

    if (!priceId) {
      throw new Error('priceId is required');
    }

    const session = await stripe.checkout.sessions.create({
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${request.headers.get('origin')}/?success=true`,
      cancel_url: `${request.headers.get('origin')}/?canceled=true`,
      automatic_tax: { enabled: true },
    });

    console.log('Checkout Session created:', session);

    return new Response(
      JSON.stringify({ url: session.url }),
      {
        status: 303,
        headers: {
          'Content-Type': 'application/json',
          'Location': session.url,
        },
      }
    );
  } catch (err) {
    console.error('Error creating checkout session:', err);

    return new Response(
      JSON.stringify({ error: err.message }),
      {
        status: err.statusCode || 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }
}
