/**
 * The single source of truth for "a preorder Stripe session was paid, now
 * make it real": claim the session (idempotent), insert the preorder row
 * (duplicate-safe), send the customer their download + confirmation, and
 * alert the admin for genuinely new preorders.
 *
 * Called from two places that must never diverge:
 *   - the success-page load (fast path: most customers land here right
 *     after paying and get instant confirmation)
 *   - the Stripe webhook (source of truth: fires server-to-server the
 *     moment Stripe confirms payment, independent of whether the
 *     customer's browser ever makes it back to the success page - covers
 *     closed tabs, dropped connections, crashed browsers)
 * Both call `fulfillPreorder`; `claimSession`'s unique constraint on
 * `session_id` means whichever one gets there first does the work and the
 * other one is a no-op, so a customer never gets double-emailed.
 */
import { env } from '$env/dynamic/private';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { sendDownloadEmail, sendAdminPreorderAlert } from '$lib/server/email.js';

const BUNDLE_PATH = env.DOWNLOAD_BUNDLE_PATH || 'research-bundle-v1.zip';
const BUCKET = env.DOWNLOAD_BUCKET || 'downloads';
const LINK_TTL = 60 * 60 * 24 * 7; // 7 days in seconds

// Allowed to repeat-purchase the same edition for testing the checkout flow.
// Deletes its own prior row before each insert so it never trips the
// (email, edition_type) unique constraint below. Unset in production, so no
// email can ever trigger the delete-then-insert path there.
const DUPLICATE_CHECK_EXEMPT_EMAIL = (env.TEST_REPEAT_PURCHASE_EMAIL || '').toLowerCase() || null;

/**
 * Claim a session ID in Supabase before doing anything else. Returns true if
 * this is the first claim (proceed with fulfillment), false if already
 * claimed - the mechanism that keeps the success page and the webhook from
 * ever both fulfilling the same session.
 */
export async function claimSession(sessionId, email) {
  if (!supabaseAdmin) return true;
  const { error } = await supabaseAdmin
    .from('fulfilled_sessions')
    .insert({ session_id: sessionId, email });
  if (error?.code === '23505') return false; // duplicate key -> already claimed
  if (error) console.error('[fulfillment] claimSession error:', error.message);
  return !error;
}

/**
 * Generates a Supabase Storage signed URL for the research bundle. Falls
 * back to null when storage isn't configured (mock mode / local dev).
 */
export async function getBundleUrl() {
  if (!supabaseAdmin) return null;
  const { data, error } = await supabaseAdmin.storage
    .from(BUCKET)
    .createSignedUrl(BUNDLE_PATH, LINK_TTL);
  if (error) {
    console.error('[fulfillment] Supabase signed URL error:', error.message);
    return null;
  }
  return data.signedUrl;
}

/**
 * @param {{ sessionId: string, email: string, name?: string, editionType: 'standard'|'authors' }} args
 * @returns {Promise<{ alreadyFulfilled: boolean, duplicate?: boolean, bundleUrl?: string|null, copyNumber?: number|null }>}
 */
export async function fulfillPreorder({ sessionId, email, name = '', editionType }) {
  const claimed = await claimSession(sessionId, email).catch((e) => {
    console.error('[fulfillment] claimSession threw:', e?.message ?? e);
    return false;
  });
  if (!claimed) return { alreadyFulfilled: true };

  const bundleUrl = await getBundleUrl();

  let copyNumber = null;
  let duplicate = false;
  const isExempt = DUPLICATE_CHECK_EXEMPT_EMAIL !== null
    && email.toLowerCase() === DUPLICATE_CHECK_EXEMPT_EMAIL;

  if (supabaseAdmin) {
    if (isExempt) {
      await supabaseAdmin.from('preorders').delete().eq('email', email).eq('edition_type', editionType);
    }
    const { data: preorder, error: preorderErr } = await supabaseAdmin
      .from('preorders')
      .insert({ email, name, edition_type: editionType, source: 'stripe' })
      .select('copy_number')
      .single();
    if (preorderErr) {
      if (preorderErr.code === '23505') {
        duplicate = true;
        console.warn(`[fulfillment] duplicate preorder blocked: ${email} already has a ${editionType} preorder.`);
      } else {
        console.error('[fulfillment] preorder insert error:', preorderErr.message);
      }
    } else {
      copyNumber = preorder?.copy_number ?? null;
    }
  }

  // They always get the download link (on a duplicate this just resends
  // access to what they already have); the admin alert only fires for
  // genuinely new preorders so a re-payment doesn't spam a second alert.
  const sends = [
    sendDownloadEmail({ to: email, sessionId, edition_type: editionType, copy_number: copyNumber })
      .catch((e) => console.error('[fulfillment] download email threw:', e?.message ?? e)),
  ];
  if (!duplicate) {
    sends.push(
      sendAdminPreorderAlert({ name, email, edition_type: editionType, copy_number: copyNumber })
        .catch((e) => console.error('[fulfillment] admin alert threw:', e?.message ?? e))
    );
  }
  await Promise.allSettled(sends);

  return { alreadyFulfilled: false, duplicate, bundleUrl, copyNumber };
}
