import { redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { getBundleUrl, fulfillPreorder } from '$lib/server/fulfillment.js';

// Per-request: reads session_id/email from the query string. Never prerender.
export const prerender = false;

const SECRET_KEY = env.STRIPE_SECRET_KEY;

const stripe = SECRET_KEY && !SECRET_KEY.startsWith('your_')
  ? new Stripe(SECRET_KEY, { apiVersion: '2024-06-20' })
  : null;

/** @type {import('./$types').PageServerLoad} */
export async function load({ url, platform }) {
  const sessionId = url.searchParams.get('session_id') ?? '';

  // ── WAITLIST MODE (email capture, Stripe not yet wired) ─────────────────────
  if (sessionId === 'waitlist') {
    const email = url.searchParams.get('email') ?? null;
    const bundleUrl = await getBundleUrl();
    return {
      ok:        true,
      mock:      false,
      email,
      bundleUrl: bundleUrl ?? null,
      sessionId,
    };
  }

  // ── MOCK MODE ────────────────────────────────────────────────────────────────
  if (!stripe || sessionId === 'mock_session' || sessionId.startsWith('mock_')) {
    const bundleUrl = await getBundleUrl();
    return {
      ok:         true,
      mock:       true,
      email:      null,
      bundleUrl:  bundleUrl ?? null,
      sessionId,
    };
  }

  // ── VALIDATE SESSION ─────────────────────────────────────────────────────────
  if (!sessionId || !sessionId.startsWith('cs_')) {
    throw redirect(302, '/early-access');
  }

  let session;
  try {
    session = await stripe.checkout.sessions.retrieve(sessionId);
  } catch (err) {
    console.error('[success] stripe retrieve error:', err.message);
    return { ok: false, error: 'Could not verify your payment. Contact us for help.' };
  }

  if (session.payment_status !== 'paid') {
    return { ok: false, error: 'Payment not yet confirmed. Refresh in a moment, or contact us.' };
  }

  const customerEmail = session.customer_details?.email ?? session.customer_email ?? null;
  const customerName  = session.customer_details?.name ?? '';
  const editionType   = session.metadata?.edition_type === 'authors' ? 'authors' : 'standard';

  // ── GENERATE DOWNLOAD URL ────────────────────────────────────────────────────
  const bundleUrl = await getBundleUrl();

  // ── FULFILL (once per session; also covered independently by the Stripe
  // webhook at /api/webhooks/stripe if the browser never gets this far) ───────
  if (customerEmail) {
    const fulfillment = fulfillPreorder({ sessionId, email: customerEmail, name: customerName, editionType })
      .catch((e) => console.error('[success] fulfillPreorder threw:', e?.message ?? e));

    if (platform?.context?.waitUntil) {
      platform.context.waitUntil(fulfillment);
    }
  }

  return {
    ok:          true,
    mock:        false,
    email:       customerEmail,
    editionType,
    bundleUrl:   bundleUrl ?? null,
    sessionId,
  };
}
