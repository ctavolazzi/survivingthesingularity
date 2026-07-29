/**
 * "Does this address already own a copy?", answered BEFORE a card is charged.
 *
 * WHY THIS EXISTS
 *
 * `preorders` carries `unique (email, edition_type)`, which is what enforces one
 * copy per customer. Until now that constraint was the ONLY enforcement, and it
 * fired in the wrong place: `stripe-checkout` passed `customer_email: undefined`,
 * so Stripe collected the address during checkout and the app did not learn who
 * the buyer was until the webhook arrived, which is after the money moved. A
 * returning customer was charged, the insert failed 23505, `fulfillment.js` read
 * that as `duplicate = true`, and they were quietly deduplicated with no refund
 * path and no admin alert.
 *
 * In test mode that is invisible, because a test card is not real money. With
 * live keys it is a chargeback and a customer who has every right to be angry.
 *
 * So the check moves in front of the charge. If the address already owns the
 * edition, no Stripe session is created at all, which means there is nothing to
 * refund because nothing was ever charged.
 *
 * WHAT THIS IS NOT
 *
 * It is not a replacement for the unique constraint. Two browser tabs can race
 * past this check in the same second. The constraint stays as the backstop that
 * makes the guarantee true rather than merely likely; this makes the common case
 * cost the customer nothing.
 */
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { sendDownloadEmail } from '$lib/server/email.js';

/**
 * How recently we must have emailed this address before a repeat request
 * declines to send again.
 *
 * The resend below is reachable by anyone who can type an address into the
 * form, so without a cooldown it is a way to send a stranger a burst of mail
 * from our domain. The IP rate limit does not cover it, because the abuse is
 * one request per victim rather than many from one source. Fifteen minutes is
 * long enough that a real customer refreshing the page does not trigger a
 * second copy either.
 */
const RESEND_COOLDOWN_MS = 15 * 60 * 1000;

/**
 * Case variants to match on.
 *
 * The stored rows come from Stripe's `customer_details.email`, which preserves
 * whatever the buyer typed, so historical rows may be mixed case while the form
 * now normalizes to lowercase. Matching an explicit list of both keeps this
 * exact. `ilike` would be the obvious alternative and is wrong here: `_` and `%`
 * are wildcards in a LIKE pattern and both are legal in an address, so
 * `a_b@x.com` would match `axb@x.com` and refuse a sale to someone who never
 * bought anything.
 *
 * The real fix is a case-insensitive unique index (`lower(email)`) or a citext
 * column, which is a migration and is logged as follow-up work rather than
 * slipped in here.
 */
function caseVariants(email, raw) {
  const set = new Set([email]);
  if (typeof raw === 'string' && raw.trim()) set.add(raw.trim());
  return [...set];
}

/**
 * @param {{ email: string, rawEmail?: string, editionType: string }} args
 * @returns {Promise<{ found: boolean, preorder?: object|null, checked: boolean }>}
 *   `checked: false` means the lookup could not run (no service role, or the
 *   query itself failed). The caller must decide what to do about that rather
 *   than reading a false negative as "no existing order".
 */
export async function findExistingPreorder({ email, rawEmail, editionType }) {
  if (!supabaseAdmin) return { found: false, checked: false };
  try {
    const { data, error } = await supabaseAdmin
      .from('preorders')
      .select('email, name, edition_type, copy_number, discount_code, created_at')
      .in('email', caseVariants(email, rawEmail))
      .eq('edition_type', editionType)
      .limit(1);
    if (error) {
      console.error(`[preorderLookup] duplicate check failed for ${editionType}: ${error.message}`);
      return { found: false, checked: false };
    }
    return { found: data.length > 0, preorder: data[0] ?? null, checked: true };
  } catch (e) {
    console.error('[preorderLookup] duplicate check threw:', e?.message ?? e);
    return { found: false, checked: false };
  }
}

/**
 * The session id whose success page will mint this customer a fresh download.
 *
 * Two sources, newest first, because they cover different eras. Sessions
 * created since sql/013 are on `checkout_transactions`, which is never purged.
 * Everyone who bought before that exists only in `fulfilled_sessions`.
 *
 * `fulfilled_sessions` ships with a 30-day delete function, which would make
 * these links expire. Checked rather than assumed: nothing schedules it. There
 * is no pg_cron job and no caller anywhere in the codebase, so the rows are
 * still there. If that purge is ever turned on, this lookup starts returning
 * null for older customers and they fall through to the support path below
 * rather than being sent a link that does not work.
 */
async function findSessionId(variants) {
  const tx = await supabaseAdmin
    .from('checkout_transactions')
    .select('session_id, created_at')
    .in('email', variants)
    .eq('status', 'completed')
    .order('created_at', { ascending: false })
    .limit(1);
  if (tx.data?.[0]?.session_id) return tx.data[0].session_id;

  const fs = await supabaseAdmin
    .from('fulfilled_sessions')
    .select('session_id, created_at')
    .in('email', variants)
    .order('created_at', { ascending: false })
    .limit(1);
  return fs.data?.[0]?.session_id ?? null;
}

/** Have we already emailed this address a download link very recently? */
async function sentRecently(variants) {
  const since = new Date(Date.now() - RESEND_COOLDOWN_MS).toISOString();
  const { data, error } = await supabaseAdmin
    .from('email_deliveries')
    .select('id')
    .in('to_email', variants)
    .eq('email_type', 'preorder_download')
    .gte('created_at', since)
    .limit(1);
  // On error, assume we DID send. Declining to send is a mild inconvenience;
  // failing open here turns a broken query into an open mail relay.
  if (error) {
    console.error('[preorderLookup] cooldown check failed, declining to resend:', error.message);
    return true;
  }
  return data.length > 0;
}

/**
 * Re-send an existing customer their download link.
 *
 * Never throws. This runs on the checkout path, and a customer who is correctly
 * being told "you already own this" must get that answer whether or not the
 * courtesy email succeeds.
 *
 * @returns {Promise<{ resent: boolean, reason: 'sent'|'cooldown'|'no_session'|'error' }>}
 */
export async function resendPreorderDownload({ email, rawEmail, editionType, preorder }) {
  if (!supabaseAdmin) return { resent: false, reason: 'error' };
  const variants = caseVariants(email, rawEmail);
  try {
    if (await sentRecently(variants)) return { resent: false, reason: 'cooldown' };

    const sessionId = await findSessionId(variants);
    // No session means no page that can mint a signed URL, so there is no
    // honest link to send. Say so rather than emailing a button that fails.
    if (!sessionId) return { resent: false, reason: 'no_session' };

    const result = await sendDownloadEmail({
      to: email,
      sessionId,
      edition_type: editionType,
      copy_number: preorder?.copy_number ?? null,
      discount_code: preorder?.discount_code ?? null,
    });
    if (result?.error || result?.skipped) return { resent: false, reason: 'error' };
    return { resent: true, reason: 'sent' };
  } catch (e) {
    console.error('[preorderLookup] resend threw:', e?.message ?? e);
    return { resent: false, reason: 'error' };
  }
}
