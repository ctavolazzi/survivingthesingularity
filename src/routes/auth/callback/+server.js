/**
 * The single landing point for every credential that arrives by link.
 *
 * Three different flows end up here, and they do not all look the same on the
 * wire, which is the main thing this file exists to absorb:
 *
 *   OAuth (PKCE)          -> ?code=<uuid>
 *   Magic link            -> ?code=<uuid>, or ?token_hash=&type=magiclink
 *   Email confirmation    -> ?token_hash=&type=signup, or ?code=
 *
 * Which one Supabase sends depends on the project's email templates. The
 * default templates use `{{ .ConfirmationURL }}`, which produces a `code`;
 * templates edited to use `{{ .TokenHash }}` produce the other. Handling only
 * the shape your project emits today means the flow breaks the day someone
 * edits a template in the dashboard, with no code change to point at. Both are
 * handled.
 *
 * A failure here never throws a 500 at the visitor. Every path ends in a
 * redirect back to /signup carrying a readable message, because this URL is
 * reached by clicking a link in an email - often days later, often on a
 * different device - and "expired" is the normal case, not an exception.
 */

import { redirect } from '@sveltejs/kit';
import { safeRedirect } from '$lib/server/safeRedirect.js';
import { MESSAGES, mapAuthError } from '$lib/server/authErrors.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';

// Opt out of the site-wide `prerender = true` (src/routes/+layout.server.js).
// This endpoint exists to read a one-time code out of a live request; a
// prerendered copy would be meaningless.
export const prerender = false;

/** Send the visitor back to the form with something to read. */
function backToSignup(message, next) {
  const params = new URLSearchParams({ error: message });
  if (next && next !== '/') params.set('next', next);
  return redirect(303, `/signup?${params}`);
}

/** @type {import('./$types').RequestHandler} */
export async function GET(event) {
  const params = event.url.searchParams;
  const next = safeRedirect(params.get('next'), '/');

  // The provider refused, or the person hit "cancel" on the consent screen.
  // Supabase forwards these verbatim. Not an error worth alarming about.
  const providerError = params.get('error') ?? params.get('error_code');
  if (providerError) {
    console.error('[auth:callback] provider returned', providerError, params.get('error_description') ?? '');
    throw backToSignup(MESSAGES.oauthFailed, next);
  }

  if (!event.locals.supabaseAuth) {
    throw backToSignup(MESSAGES.unavailable, next);
  }

  const code = params.get('code');
  const tokenHash = params.get('token_hash');
  const type = params.get('type');

  let result;

  if (code) {
    // PKCE. The verifier is in an httpOnly cookie written when the flow
    // started; this fails if the browser that finishes is not the one that
    // began, which is the property that makes the GET entry point safe.
    result = await event.locals.supabaseAuth.auth.exchangeCodeForSession(code);
  } else if (tokenHash && type) {
    result = await event.locals.supabaseAuth.auth.verifyOtp({
      token_hash: tokenHash,
      type: /** @type {any} */ (type)
    });
  } else {
    // Someone opened /auth/callback directly.
    throw redirect(303, '/signup');
  }

  if (result.error) {
    const mapped = mapAuthError(result.error, 'callback');
    throw backToSignup(mapped.message, next);
  }

  const user = result.data?.user;

  // Now that the address is confirmed - by clicking the link, or by the
  // provider asserting it - attach anything bought under it. For OAuth this is
  // the first time we have seen this person, and the trigger in sql/015 has
  // already run; calling again is idempotent and covers orders placed since.
  if (user?.id && user?.email) {
    await claimEntitlements(user.id, user.email.toLowerCase());
    await ensureProfile(user);
  }

  throw redirect(303, next);
}

/**
 * @param {string} userId
 * @param {string} email
 */
async function claimEntitlements(userId, email) {
  if (!supabaseAdmin) return;
  const { error } = await supabaseAdmin.rpc('claim_preorders_for_user', {
    p_user_id: userId,
    p_email: email
  });
  if (error) console.error('[auth:callback] entitlement claim failed:', error.message);
}

/**
 * Backstop for the profile row.
 *
 * The trigger in sql/015 is what normally creates it. This exists because a
 * trigger is a deploy-time dependency: if 015 has not been run against the
 * environment yet, every OAuth sign-in would otherwise produce a session with
 * no profile behind it, and the failure would surface far away from the cause.
 * Upsert, so it is a no-op when the trigger did its job.
 *
 * @param {{id: string, email?: string, user_metadata?: Record<string, any>}} user
 */
async function ensureProfile(user) {
  if (!supabaseAdmin) return;
  const meta = user.user_metadata ?? {};
  const { error } = await supabaseAdmin
    .from('profiles')
    .upsert(
      {
        id: user.id,
        email: (user.email ?? '').toLowerCase(),
        display_name:
          meta.full_name || meta.name || (user.email ?? '').split('@')[0] || '',
        // sql/015 defaults access_source to 'purchase'. Someone arriving
        // through /signup has not bought anything, and recording that they did
        // would corrupt the entitlement question this column exists to answer.
        // sql/016 widens the constraint to allow 'signup'.
        access_source: 'signup'
      },
      { onConflict: 'id', ignoreDuplicates: true }
    );
  if (error) console.error('[auth:callback] profile upsert failed:', error.message);
}
