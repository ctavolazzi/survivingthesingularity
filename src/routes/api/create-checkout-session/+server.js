import { json } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
  return json({
    error: true,
    message: "The crowdfunding campaign has concluded. Purchases are no longer available."
  }, { status: 410 }); // 410 Gone status code
}

// Original code commented out for reference
/*
import { json } from '@sveltejs/kit';
import { STRIPE_SECRET_KEY } from '$env/static/private';
import Stripe from 'stripe';

const stripe = new Stripe(STRIPE_SECRET_KEY);

export async function POST({ request }) {
  const { priceId, quantity = 1 } = await request.json();

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId,
          quantity,
        },
      ],
      mode: 'payment',
      success_url: `${request.headers.get('origin')}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${request.headers.get('origin')}/cancel`,
    });

    return json({ id: session.id });
  } catch (error) {
    console.error('Error creating checkout session:', error);
    return json({ error: { message: error.message } }, { status: 400 });
  }
}
*/