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
 * other one retries after the lease finishes. Provider idempotency covers
 * uncertain send results within its 24-hour retention window.
 */
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { sendDownloadEmail, sendAdminPreorderAlert } from '$lib/server/email.js';
import { currentBundleRelease } from '$lib/server/bundleRelease.js';

const LINK_TTL = 60 * 60 * 24 * 7; // 7 days in seconds

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
 * Acquire a database lease atomically. A row existing is not evidence of a
 * successful send. Missing migrations, unavailable storage and races all stay
 * retryable; only a persisted delivered outcome earns a terminal success.
 * Requires sql/017_payment_reliability.sql, applied before this code deploys.
 */
export async function claimSession(sessionId, email) {
  if (!supabaseAdmin) return { state: 'retryable_failure', error: 'Supabase not configured' };
  try {
    const { data, error } = await supabaseAdmin.rpc('claim_fulfillment_session', {
      p_session_id: sessionId, p_email: email,
    });
    if (error) throw new Error(error.message);
    if (!data || !['claimed', 'already_delivered', 'in_flight'].includes(data.state)) {
      throw new Error('Invalid fulfillment lease response');
    }
    return data;
  } catch (error) {
    console.error('[fulfillment] claim failed:', error?.message ?? error);
    return { state: 'retryable_failure', error: error?.message ?? String(error) };
  }
}

async function markSessionOutcome(sessionId, leaseToken, status, lastError = null) {
  const { data, error } = await supabaseAdmin
    .from('fulfilled_sessions')
    .update({
      status,
      completed_at: new Date().toISOString(),
      last_error: lastError ? String(lastError).slice(0, 500) : null,
      lease_expires_at: null,
    })
    .eq('session_id', sessionId)
    .eq('lease_token', leaseToken)
    .eq('status', 'claimed')
    .select('session_id');
  if (error || !data?.length) {
    throw new Error(error?.message ?? 'Fulfillment lease changed before outcome was recorded');
  }
}

/**
 * Generates a Supabase Storage signed URL for The Precedent File bundle. Falls
 * back to null when storage isn't configured (mock mode / local dev).
 */
export async function getBundleUrl() {
  if (!supabaseAdmin) return null;
  const bundle = currentBundleRelease();
  if (!bundle.ok) {
    console.error('[fulfillment] download unavailable:', bundle.error);
    return null;
  }
  try {
    const { data, error } = await supabaseAdmin.storage
      .from(bundle.bucket)
      .createSignedUrl(bundle.path, LINK_TTL);
    if (error) throw new Error(error.message);
    return data?.signedUrl ?? null;
  } catch (error) {
    console.error('[fulfillment] Supabase signed URL error:', error?.message ?? error);
    return null;
  }
}

/**
 * @param {{ sessionId: string, email: string, name?: string, editionType: 'standard'|'authors',
 *          amountTotal?: number|null, currency?: string|null,
 *          paymentIntent?: string|null, orderedAt?: number|null }} args
 * @returns {Promise<object>} Explicit state: accepted, already_delivered, in_flight, retryable_failure.
 *
 * The four payment fields are passed straight through to the confirmation
 * email's receipt block and are not used for anything else here. They are
 * OPTIONAL and default to null on purpose: both callers already hold the Stripe
 * session, so nothing has to be fetched, but a caller that genuinely does not
 * have them (a manual replay, a future admin resend) still gets a working
 * email with the receipt rows it cannot fill simply absent.
 */
export async function fulfillPreorder({
  sessionId, email, name = '', editionType,
  amountTotal = null, currency = null, paymentIntent = null, orderedAt = null,
}) {
  email = email.trim().toLowerCase();
  const claim = await claimSession(sessionId, email);
  if (claim.state !== 'claimed') {
    return { ...claim, alreadyFulfilled: claim.state === 'already_delivered', delivered: false };
  }

  try {
    const bundleUrl = await getBundleUrl();
    if (!bundleUrl) throw new Error('Download storage unavailable');

    let copyNumber = null;
    let discountCode = null;
    let duplicate = false;
    if (supabaseAdmin) {
      // Retry a code collision with a fresh code before any of the duplicate
      // handling below can mistake it for a repeat customer. Five attempts
      // against a 31^6 space is far beyond what any realistic order volume
      // needs; it exists so the failure is impossible rather than merely rare.
      let preorder = null;
      let preorderErr = null;
      for (let attempt = 1; attempt <= 5; attempt++) {
        ({ data: preorder, error: preorderErr } = await supabaseAdmin
          .from('preorders')
          .insert({ email, name, edition_type: editionType, source: 'stripe', payment_session_id: sessionId, discount_code: generateDiscountCode() })
          .select('copy_number, discount_code')
          .single());
        if (violatedConstraint(preorderErr) !== 'discount_code') break;
        console.warn(`[fulfillment] discount code collision for ${email}, retrying (attempt ${attempt}/5).`);
      }

      if (preorderErr) {
        if (violatedConstraint(preorderErr) === 'email') {
          duplicate = true;
          console.warn(`[fulfillment] duplicate preorder blocked: ${email} already has a ${editionType} preorder.`);
          // Look up their existing code so a resend still shows the real one.
          const { data: existing, error: existingError } = await supabaseAdmin
            .from('preorders')
            .select('copy_number, discount_code, payment_session_id')
            .eq('email', email).eq('edition_type', editionType)
            .maybeSingle();
          if (existingError || !existing) throw new Error(existingError?.message ?? 'Existing preorder missing');
          duplicate = existing.payment_session_id !== sessionId;
          if (duplicate) {
            const { error } = await supabaseAdmin.from('checkout_transactions')
              .update({ review_reason: 'possible_duplicate_payment' }).eq('session_id', sessionId);
            if (error) throw new Error(error.message);
          }
          copyNumber = existing?.copy_number ?? null;
          discountCode = existing?.discount_code ?? null;
        } else {
          throw new Error(`Paid preorder could not be recorded: ${preorderErr.message}`);
        }
      } else {
        copyNumber = preorder?.copy_number ?? null;
        discountCode = preorder?.discount_code ?? null;
      }
    }

    // A second paid session still receives access, but is flagged for a human
    // refund review. A retry of the same session is provider-idempotent.
    //
    // The download email's result is captured rather than swallowed, because it
    // is the one send that decides whether this session counts as delivered. The
    // admin alert failing is our problem; the customer still got their bundle.
    const downloadPromise = sendDownloadEmail({
      to: email, sessionId, edition_type: editionType, copy_number: copyNumber, discount_code: discountCode,
      amountTotal, currency, paymentIntent, orderedAt,
      idempotencyKey: `fulfillment/${sessionId}/download`,
    }).catch((e) => {
      console.error('[fulfillment] download email threw:', e?.message ?? e);
      return { error: e?.message ?? String(e) };
    });

    const adminPromise = sendAdminPreorderAlert({
      name, email, edition_type: editionType, copy_number: copyNumber,
      sessionId, duplicatePayment: duplicate,
      idempotencyKey: `fulfillment/${sessionId}/admin`,
    }).catch((e) => console.error('[fulfillment] admin alert threw:', e?.message ?? e));

    const [downloadResult] = await Promise.all([downloadPromise, adminPromise]);

    // `skipped: true` means RESEND_API_KEY is unset, which is a configuration
    // fault, not a delivery. Calling that 'delivered' would let a misconfigured
    // deployment quietly mark every order complete while sending nothing.
    const deliveryFailed = downloadResult?.ok !== true;
    await markSessionOutcome(
      sessionId, claim.lease_token,
      deliveryFailed ? 'failed' : 'delivered',
      downloadResult?.error?.message ?? downloadResult?.error ?? (deliveryFailed ? 'Email provider did not accept delivery' : null)
    );

    return {
      state: deliveryFailed ? 'retryable_failure' : 'accepted',
      alreadyFulfilled: false, duplicate, bundleUrl, copyNumber, discountCode,
      delivered: !deliveryFailed,
      error: deliveryFailed ? 'Email provider did not accept delivery' : undefined,
    };
  } catch (error) {
    const message = error?.message ?? String(error);
    await markSessionOutcome(sessionId, claim.lease_token, 'failed', message)
      .catch((e) => console.error('[fulfillment] could not record failure:', e?.message ?? e));
    return { state: 'retryable_failure', alreadyFulfilled: false, delivered: false, error: message };
  }
}
