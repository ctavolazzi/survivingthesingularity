import { redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { sendDownloadEmail } from '$lib/server/email.js';

// Per-request: reads session_id/email from the query string. Never prerender.
export const prerender = false;

const SECRET_KEY  = env.STRIPE_SECRET_KEY;
const BUNDLE_PATH = env.DOWNLOAD_BUNDLE_PATH || 'research-bundle-v1.zip';
const BUCKET      = env.DOWNLOAD_BUCKET      || 'downloads';
const LINK_TTL    = 60 * 60 * 24 * 7; // 7 days in seconds

const stripe = SECRET_KEY && !SECRET_KEY.startsWith('your_')
  ? new Stripe(SECRET_KEY, { apiVersion: '2024-06-20' })
  : null;

// Claim a session ID in Supabase before sending the email.
// Returns true if this is the first claim (send email), false if already claimed (skip).
// Falls back to true (always send) when Supabase isn't configured — acceptable for local dev.
async function claimSession(sessionId, email) {
  if (!supabaseAdmin) return true;
  const { error } = await supabaseAdmin
    .from('fulfilled_sessions')
    .insert({ session_id: sessionId, email });
  if (error?.code === '23505') return false; // duplicate key → already sent
  if (error) console.error('[success] claimSession error:', error.message);
  return !error;
}

/**
 * Generates a Supabase Storage signed URL for the research bundle.
 * Falls back to a placeholder URL in development / when storage isn't configured.
 */
async function getBundleUrl() {
  if (!supabaseAdmin) {
    return null; // mock mode — page will show placeholder
  }
  const { data, error } = await supabaseAdmin.storage
    .from(BUCKET)
    .createSignedUrl(BUNDLE_PATH, LINK_TTL);

  if (error) {
    console.error('[success] Supabase signed URL error:', error.message);
    return null;
  }
  return data.signedUrl;
}

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {
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

  // ── GENERATE DOWNLOAD URL ────────────────────────────────────────────────────
  const bundleUrl = await getBundleUrl();

  // ── SEND EMAIL (once per session) ───────────────────────────────────────────
  if (customerEmail) {
    claimSession(sessionId, customerEmail).then((claimed) => {
      if (!claimed) return;
      sendDownloadEmail({ to: customerEmail, downloadUrl: bundleUrl ?? null, sessionId })
        .catch((e) => console.error('[success] download email threw:', e?.message ?? e));
    }).catch((e) => console.error('[success] claimSession threw:', e?.message ?? e));
  }

  return {
    ok:        true,
    mock:      false,
    email:     customerEmail,
    bundleUrl: bundleUrl ?? null,
    sessionId,
  };
}
