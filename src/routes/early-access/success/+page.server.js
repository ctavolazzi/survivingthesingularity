import { redirect } from '@sveltejs/kit';
import { dev } from '$app/environment';
import { env } from '$env/dynamic/private';
import Stripe from 'stripe';
import { isPreorderSession } from '$lib/server/preorderSession.js';
import { BOOK_ACCESS_PASSWORD } from '$lib/bookAccessCode.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { getBundleUrl, fulfillPreorder } from '$lib/server/fulfillment.js';
import { recordCheckoutCompleted, markTransactionFulfilled } from '$lib/server/transactions.js';

// Per-request: reads session_id/email from the query string. Never prerender.
export const prerender = false;

const SECRET_KEY = env.STRIPE_SECRET_KEY;

const stripe = SECRET_KEY && !SECRET_KEY.startsWith('your_')
  ? new Stripe(SECRET_KEY, { apiVersion: '2024-06-20' })
  : null;

/**
 * Was this session already paid for, according to records we own?
 *
 * `fulfilled_sessions` rows are written by exactly one thing: `claimSession()`,
 * called from `fulfillPreorder()`, which runs only after Stripe confirmed
 * `payment_status === 'paid'` (from the success page) or emitted
 * `checkout.session.completed` (from the webhook). Both write with the service
 * role. So a row here is independent proof of payment that does not require
 * Stripe to be reachable, or even to still recognise the session id.
 *
 * This is deliberately keyed on the row and never on the shape of the string.
 * `cs_`-prefixed ids are guessable in principle, and the bundle is a real
 * product, so "looks like a session id" must never be sufficient to mint a
 * download.
 *
 * @returns {Promise<{session_id: string, email: string|null}|null>}
 */
async function paidAccordingToOurRecords(sessionId) {
  if (!supabaseAdmin) return null;
  const ledger = await supabaseAdmin.from('checkout_transactions')
    .select('session_id, email').eq('session_id', sessionId).eq('status', 'completed').maybeSingle();
  if (!ledger.error && ledger.data) return ledger.data;
  // Retain compatibility with paid orders predating the permanent ledger.
  const { data, error } = await supabaseAdmin.from('fulfilled_sessions')
    .select('session_id, email').eq('session_id', sessionId).maybeSingle();
  if (error) {
    console.error('[success] paid-record lookup failed:', error.message);
    return null;
  }
  return data ?? null;
}

/**
 * Stripe could not confirm this purchase. Before showing a paying customer an
 * error, check whether we already know the purchase is real.
 *
 * This recovers access, not an email-delivery assertion. A claim can have
 * failed after payment, and a ledger row is not proof the inbox received mail.
 * The verified webhook retry/reconciliation handles unfinished fulfillment.
 *
 * @param {string} sessionId
 * @param {string} error   what to say if we have no record either
 */
async function serveFromOwnRecords(sessionId, error) {
  const row = await paidAccordingToOurRecords(sessionId);

  if (!row) {
    // Genuinely unknown. Keep the error, but hand over something support can
    // actually search on rather than asking the customer to describe it.
    return { ok: false, error, orderRef: sessionId.slice(0, 24) };
  }

  const bundleUrl = await getBundleUrl();
  return {
    ok:        true,
    mock:      false,
    email:     row.email ?? null,
    bundleUrl: bundleUrl ?? null,
    sessionId,
    // The page stays honest about which path served it. The download is real;
    // the live confirmation is not available.
    recovered: true,
    emailStatus: 'unknown',
    bookAccessPassword: BOOK_ACCESS_PASSWORD,
  };
}

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {
  const sessionId = url.searchParams.get('session_id') ?? '';

  // Synthetic sessions never access storage, even in development. Missing
  // production credentials are an unavailable verifier, not a paid purchase.
  if (dev && (sessionId === 'mock_session' || sessionId.startsWith('mock_'))) {
    return { ok: true, mock: true, email: null, bundleUrl: null, sessionId, emailStatus: 'unknown' };
  }

  // ── VALIDATE SESSION ─────────────────────────────────────────────────────────
  if (!sessionId || !sessionId.startsWith('cs_')) {
    throw redirect(302, '/early-access');
  }

  if (!stripe) {
    return await serveFromOwnRecords(sessionId, 'Payment verification is temporarily unavailable. Contact us with your order reference.');
  }

  // Stripe is the fast path, not the only path. Every failure below falls
  // through to `fulfilled_sessions`, which is the record we own. The reason
  // this matters is not hypothetical: a live-mode key cannot retrieve a
  // test-mode session, so the moment STRIPE_SECRET_KEY flips to sk_live_,
  // every existing customer's download link starts throwing here.
  let session;
  try {
    session = await stripe.checkout.sessions.retrieve(sessionId);
  } catch (err) {
    console.error('[success] stripe retrieve error:', err.message);
    return await serveFromOwnRecords(
      sessionId,
      'Could not verify your payment. Contact us and we will send your download.'
    );
  }

  if (!isPreorderSession(session)) {
    // Old receipts may be recovered only from our own paid-order ledger.
    return await serveFromOwnRecords(sessionId, 'This checkout does not match an early-access purchase. Contact us with your order reference.');
  }

  if (session.payment_status !== 'paid') {
    // Stripe answered and says this is not paid. Our own record still wins if
    // we have one, because a `fulfilled_sessions` row is only ever written
    // after a confirmed payment, and it is the more conservative failure: a
    // customer who paid and is told they did not is worse than a stale row.
    return await serveFromOwnRecords(
      sessionId,
      'Payment not yet confirmed. Refresh in a moment, or contact us.'
    );
  }

  const customerEmail = session.customer_details?.email ?? session.customer_email ?? null;
  const customerName  = session.customer_details?.name ?? '';
  const editionType   = session.metadata?.edition_type === 'authors' ? 'authors' : 'standard';

  // ── GENERATE DOWNLOAD URL ────────────────────────────────────────────────────
  const bundleUrl = await getBundleUrl();

  // Await on every runtime. A detached promise is not durable work outside a
  // Worker waitUntil context, and would make the page claim a send it lost.
  let emailStatus = 'retryable_failure';
  try {
    const ledger = await recordCheckoutCompleted({
      sessionId,
      paymentIntent: typeof session.payment_intent === 'string' ? session.payment_intent : session.payment_intent?.id ?? null,
      email: customerEmail, name: customerName, editionType,
      amountTotal: session.amount_total ?? null, currency: session.currency ?? null,
    });
    if (!ledger.configured || !ledger.ok) throw new Error(ledger.error ?? 'Payment ledger unavailable');
    if (customerEmail) {
      const result = await fulfillPreorder({
        sessionId, email: customerEmail, name: customerName, editionType,
        amountTotal: session.amount_total ?? null, currency: session.currency ?? null,
        paymentIntent: typeof session.payment_intent === 'string' ? session.payment_intent : session.payment_intent?.id ?? null,
        orderedAt: session.created ?? null,
      });
      emailStatus = result.state;
      if (['accepted', 'already_delivered'].includes(result.state)) {
        const recorded = await markTransactionFulfilled(sessionId);
        if (!recorded?.ok) console.error('[success] fulfillment ledger update failed:', recorded?.error);
      }
    }
  } catch (error) {
    console.error('[success] fulfillment pending:', error?.message ?? error);
  }

  return {
    ok:          true,
    mock:        false,
    email:       customerEmail,
    editionType,
    emailStatus,
    bookAccessPassword: BOOK_ACCESS_PASSWORD,
    bundleUrl:   bundleUrl ?? null,
    sessionId,
  };
}
