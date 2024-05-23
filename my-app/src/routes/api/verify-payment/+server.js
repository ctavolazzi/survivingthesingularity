import Stripe from 'stripe';
import { SECRET_STRIPE_KEY_TEST, SECRET_STRIPE_KEY_LIVE } from '$env/static/private';
import crypto from 'crypto';

const stripe = new Stripe(SECRET_STRIPE_KEY_TEST);

export async function GET({ url }) {
  const sessionId = url.searchParams.get('session_id');
  const session = await stripe.checkout.sessions.retrieve(sessionId);

  if (session.payment_status === 'paid') {
    // Generate a secure token or unique identifier for the download link
    const token = generateSecureToken(sessionId);
    return new Response(JSON.stringify({ link: `/download?token=${token}` }), { status: 200 });
  } else {
    return new Response(JSON.stringify({ error: 'Payment not verified' }), { status: 400 });
  }
}

// Helper function to generate a secure token
function generateSecureToken(sessionId) {
  return crypto.createHash('sha256').update(sessionId + SECRET_STRIPE_KEY).digest('hex');
}

