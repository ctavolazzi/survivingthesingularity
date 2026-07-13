import { redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { sendDownloadEmail, sendAdminPreorderAlert } from '$lib/server/email.js';

// Per-request: reads session_id/email from the query string. Never prerender.
export const prerender = false;

const SECRET_KEY  = env.STRIPE_SECRET_KEY;
const BUNDLE_PATH = env.DOWNLOAD_BUNDLE_PATH || 'research-bundle-v1.zip';
const BUCKET      = env.DOWNLOAD_BUCKET      || 'downloads';
const LINK_TTL    = 60 * 60 * 24 * 7; // 7 days in seconds

const stripe = SECRET_KEY && !SECRET_KEY.startsWith('your_')
  ? new Stripe(SECRET_KEY, { apiVersion: '2024-06-20' })
  : null;

// Allowed to repeat-purchase the same edition for testing the checkout flow.
// Deletes its own prior row before each insert so it never trips the
// (email, edition_type) unique constraint below. Unset in production, so no
// email can ever trigger the delete-then-insert path there.
const DUPLICATE_CHECK_EXEMPT_EMAIL = (env.TEST_REPEAT_PURCHASE_EMAIL || '').toLowerCase() || null;

// Claim a session ID in Supabase before sending the email.
// Returns true if this is the first claim (send email), false if already claimed (skip).
// Falls back to true (always send) when Supabase isn't configured - acceptable for local dev.
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
    return null; // mock mode - page will show placeholder
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

  // ── FULFILL (once per session) ───────────────────────────────────────────────
  if (customerEmail) {
    // Handed to waitUntil below so it survives after the response ships on
    // Cloudflare (a bare promise can be killed when the isolate freezes);
    // locally it just runs in the background. The awaits inside .then() are
    // required for that to work - without them this promise would resolve
    // before the emails actually finish, defeating the point of waitUntil.
    const fulfillment = claimSession(sessionId, customerEmail).then(async (claimed) => {
      if (!claimed) return;

      // 1. Insert preorder row - trigger assigns copy_number for authors edition.
      // The (email, edition_type) unique constraint blocks a real repeat
      // purchase; the exempt test email clears its own prior row first so it
      // can buy the same edition repeatedly without tripping that constraint.
      let copyNumber = null;
      let duplicate = false;
      const isExempt = DUPLICATE_CHECK_EXEMPT_EMAIL !== null
        && customerEmail.toLowerCase() === DUPLICATE_CHECK_EXEMPT_EMAIL;
      if (supabaseAdmin) {
        if (isExempt) {
          await supabaseAdmin.from('preorders').delete().eq('email', customerEmail).eq('edition_type', editionType);
        }
        const { data: preorder, error: preorderErr } = await supabaseAdmin
          .from('preorders')
          .insert({ email: customerEmail, name: customerName, edition_type: editionType, source: 'stripe' })
          .select('copy_number')
          .single();
        if (preorderErr) {
          if (preorderErr.code === '23505') {
            duplicate = true;
            console.warn(`[success] duplicate preorder blocked: ${customerEmail} already has a ${editionType} preorder.`);
          } else {
            console.error('[success] preorder insert error:', preorderErr.message);
          }
        } else {
          copyNumber = preorder?.copy_number ?? null;
        }
      }

      // 2. Send the bundle (they paid, so they always get the download link -
      // on a duplicate this just resends access to what they already have)
      // and, for genuinely new preorders only, the admin alert. The two sends
      // are independent, so run them in parallel; allSettled keeps one
      // failure from swallowing the other.
      const sends = [
        sendDownloadEmail({ to: customerEmail, downloadUrl: bundleUrl ?? null, sessionId, edition_type: editionType, copy_number: copyNumber })
          .catch((e) => console.error('[success] download email threw:', e?.message ?? e)),
      ];
      if (!duplicate) {
        sends.push(
          sendAdminPreorderAlert({ name: customerName, email: customerEmail, edition_type: editionType, copy_number: copyNumber })
            .catch((e) => console.error('[success] admin alert threw:', e?.message ?? e))
        );
      }
      await Promise.allSettled(sends);

    }).catch((e) => console.error('[success] claimSession threw:', e?.message ?? e));

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
