import Stripe from 'stripe';
import { SECRET_STRIPE_KEY_TEST, SECRET_STRIPE_KEY_LIVE } from '$env/static/private';

const stripe = new Stripe(SECRET_STRIPE_KEY_TEST);

export async function POST({ request }) {
  try {
    const { priceId } = await request.json();

    const protocol = request.headers.get('x-forwarded-proto') || 'http';
    const host = request.headers.get('host');
    const baseUrl = `${protocol}://${host}`;

    const session = await stripe.checkout.sessions.create({
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      mode: 'payment',
      // Use these endpoints to redirect to the success and cancel conditionals
      // success_url: `${baseUrl}/?success=true`,
      // cancel_url: `${baseUrl}/?canceled=true`,
      // Use these endpoints to redirect to the success and cancel hardcoded pages
      success_url: `${baseUrl}/success`,
      cancel_url: `${baseUrl}/canceled`,
      automatic_tax: { enabled: true },
    });

    return new Response(
      JSON.stringify({ url: session.url }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': request.headers.origin,
        },
      }
    );
  } catch (err) {
    console.error('Error:', err);
    return new Response(
      JSON.stringify({ error: 'An error occurred' }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': request.headers.origin,
        },
      }
    );
  }
}