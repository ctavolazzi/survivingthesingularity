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

// Unambiguous charset for a code a customer has to type back in later - no
// 0/O, 1/I/L, so it reads cleanly out loud or off a screenshot.
const CODE_CHARS = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
function generateDiscountCode() {
  let code = '';
  // crypto.getRandomValues over Math.random: this code is handed to the
  // customer as proof of a genuine preorder, so it should not be guessable
  // from other codes issued nearby. Available in both Workers and Node 18+.
  const bytes = crypto.getRandomValues(new Uint8Array(6));
  for (let i = 0; i < 6; i++) {
    code += CODE_CHARS[bytes[i] % CODE_CHARS.length];
  }
  return code;
}

/**
 * `preorders` has three unique constraints, and every one of them surfaces as
 * the same Postgres 23505:
 *   - (email, edition_type)        -> a genuine repeat customer
 *   - (edition_type, copy_number)  -> the author's-edition numbering race
 *   - discount_code                -> two generated codes collided
 * Only the first means "already preordered". Treating the other two as a
 * duplicate customer silently drops a paid order: no row is written, no admin
 * alert fires, and the customer still gets their download, so nobody finds
 * out. PostgREST puts the violated constraint's name in `message`, which is
 * the only thing that tells them apart.
 */
function violatedConstraint(err) {
  if (err?.code !== '23505') return null;
  const msg = err.message ?? '';
  if (/discount_code/.test(msg)) return 'discount_code';
  if (/edition_copy|copy_number/.test(msg)) return 'copy_number';
  return 'email';
}

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
 * Generates a Supabase Storage signed URL for The Precedent File bundle. Falls
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
  let discountCode = null;
  let duplicate = false;
  const isExempt = DUPLICATE_CHECK_EXEMPT_EMAIL !== null
    && email.toLowerCase() === DUPLICATE_CHECK_EXEMPT_EMAIL;

  if (supabaseAdmin) {
    if (isExempt) {
      await supabaseAdmin.from('preorders').delete().eq('email', email).eq('edition_type', editionType);
    }

    // Retry a code collision with a fresh code before any of the duplicate
    // handling below can mistake it for a repeat customer. Five attempts
    // against a 31^6 space is far beyond what any realistic order volume
    // needs; it exists so the failure is impossible rather than merely rare.
    let preorder = null;
    let preorderErr = null;
    for (let attempt = 1; attempt <= 5; attempt++) {
      ({ data: preorder, error: preorderErr } = await supabaseAdmin
        .from('preorders')
        .insert({ email, name, edition_type: editionType, source: 'stripe', discount_code: generateDiscountCode() })
        .select('copy_number, discount_code')
        .single());
      if (violatedConstraint(preorderErr) !== 'discount_code') break;
      console.warn(`[fulfillment] discount code collision for ${email}, retrying (attempt ${attempt}/5).`);
    }

    // sql/009_preorder_discount_code.sql may not have run yet on this
    // project - if the column itself is missing, PostgREST rejects the
    // whole insert. Retry without it rather than let a schema migration
    // gap take down the entire preorder pipeline; the code is simply
    // omitted from the email until the migration runs.
    if (preorderErr && preorderErr.code !== '23505') {
      console.warn('[fulfillment] insert with discount_code failed, retrying without it:', preorderErr.message);
      ({ data: preorder, error: preorderErr } = await supabaseAdmin
        .from('preorders')
        .insert({ email, name, edition_type: editionType, source: 'stripe' })
        .select('copy_number')
        .single());
    }

    if (preorderErr) {
      if (violatedConstraint(preorderErr) === 'email') {
        duplicate = true;
        console.warn(`[fulfillment] duplicate preorder blocked: ${email} already has a ${editionType} preorder.`);
        // Look up their existing code so a resend still shows the real one.
        const { data: existing } = await supabaseAdmin
          .from('preorders')
          .select('copy_number, discount_code')
          .eq('email', email).eq('edition_type', editionType)
          .maybeSingle();
        copyNumber = existing?.copy_number ?? null;
        discountCode = existing?.discount_code ?? null;
      } else {
        // Not a repeat customer: a real paid order just failed to record.
        // `duplicate` stays false so the admin alert still fires - that alert
        // is now the only way anyone finds out this happened.
        console.error(
          `[fulfillment] PAID ORDER NOT RECORDED for ${email} (${editionType}, session ${sessionId}). ` +
          `Constraint: ${violatedConstraint(preorderErr) ?? 'none'}. Error: ${preorderErr.message}`
        );
      }
    } else {
      copyNumber = preorder?.copy_number ?? null;
      discountCode = preorder?.discount_code ?? null;
    }
  }

  // They always get the download link (on a duplicate this just resends
  // access to what they already have); the admin alert only fires for
  // genuinely new preorders so a re-payment doesn't spam a second alert.
  const sends = [
    sendDownloadEmail({ to: email, sessionId, edition_type: editionType, copy_number: copyNumber, discount_code: discountCode })
      .catch((e) => console.error('[fulfillment] download email threw:', e?.message ?? e)),
  ];
  if (!duplicate) {
    sends.push(
      sendAdminPreorderAlert({ name, email, edition_type: editionType, copy_number: copyNumber })
        .catch((e) => console.error('[fulfillment] admin alert threw:', e?.message ?? e))
    );
  }
  await Promise.allSettled(sends);

  return { alreadyFulfilled: false, duplicate, bundleUrl, copyNumber, discountCode };
}
