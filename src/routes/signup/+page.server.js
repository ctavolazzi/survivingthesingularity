/**
 * The /signup flow: create account, sign in, magic link, resend.
 *
 * SHAPE
 *
 * These are SvelteKit form actions rather than JSON endpoints under /api,
 * unlike the rest of this codebase. That is deliberate and it buys two things:
 *
 *  1. CSRF is handled for us. SvelteKit's built-in protection covers form
 *     content types (urlencoded/multipart/text-plain) and rejects cross-origin
 *     posts before our code runs. $lib/server/sameOrigin.js exists because the
 *     JSON routes fall outside that protection - see its header. A form action
 *     is inside it, so this file does not repeat the check, and there is no
 *     second copy to drift out of sync.
 *
 *  2. The whole flow works with JavaScript off. `use:enhance` upgrades it to a
 *     fetch when JS is available; without it the browser posts the form and
 *     follows the redirect. An auth page that hard-fails without JS locks
 *     people out of their own accounts for no reason.
 *
 * ENUMERATION
 *
 * Read $lib/server/authErrors.js before changing any message in here. The
 * short version: signup and signin must not reveal whether an address has an
 * account, so `signup` renders the same "check your inbox" view whether the
 * address was new or already registered, and `signin` returns one message for
 * both a wrong password and a nonexistent user.
 */

import { fail, redirect } from '@sveltejs/kit';
import { normalizeEmail, isValidEmail } from '$lib/server/validEmail.js';
import { checkPassword, strengthHint } from '$lib/server/passwordPolicy.js';
import { MESSAGES, mapAuthError } from '$lib/server/authErrors.js';
import { enforceAuthBudget, authRateReset } from '$lib/server/authRateLimit.js';
import { safeRedirect } from '$lib/server/safeRedirect.js';
import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';
import { authConfigured } from '$lib/server/supabaseAuth.js';

// src/routes/+layout.server.js sets `prerender = true` for the whole site.
// Nothing here can be prerendered: the page depends on the request's session
// and the route has form actions, which SvelteKit refuses to prerender at all.
export const prerender = false;

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, url }) {
  const next = safeRedirect(url.searchParams.get('next'), '/');

  // Already signed in - nothing to do here.
  if (locals.user) throw redirect(303, next);

  return {
    next,
    passwordHint: strengthHint(),
    // Lets the page explain itself instead of failing silently when the
    // deployment has no Supabase keys (a fresh clone, or a preview build).
    authConfigured,
    // Rendered as the OAuth buttons. Read from here rather than hardcoded in
    // the markup so turning a provider off is a one-line change on the server.
    providers: ['google', 'github']
  };
}

/**
 * Read and normalize the fields every action shares.
 * @param {FormData} form
 */
function readCommon(form) {
  return {
    email: normalizeEmail(form.get('email')),
    next: safeRedirect(form.get('next'), '/'),
    // Bots fill hidden fields; humans cannot see them. Same trick as
    // /api/waitlist, which answers 201 to a filled honeypot so the bot learns
    // nothing from the response.
    trapped: Boolean(form.get('_hp'))
  };
}

/**
 * The failure shape the page renders. `field` drives which input gets the
 * error ring; `email` is echoed back so a rejected submit does not clear it.
 */
function problem(status, { message, field = null, email = '', mode = 'signup' }) {
  return fail(status, { message, field, email, mode });
}

/** @type {import('./$types').Actions} */
export const actions = {
  /**
   * Create an account with email + password.
   *
   * Always ends in the same place from the caller's point of view: the neutral
   * "we sent you a link" view. Whether that link is a confirmation for a new
   * account or a "you already have an account" notice is decided by Supabase
   * and delivered to the inbox, which is the one place the answer belongs.
   */
  signup: async (event) => {
    const form = await event.request.formData();
    const { email, next, trapped } = readCommon(form);
    const password = form.get('password');
    const consent = form.get('consent') === 'on' || form.get('consent') === 'true';

    // Silent success. Identical to the real success shape so a bot cannot
    // distinguish them.
    if (trapped) return { pending: true, email, mode: 'signup' };

    if (!isValidEmail(email)) {
      return problem(400, { message: MESSAGES.invalidEmail, field: 'email', email });
    }

    // The checkbox is acceptance of the Terms and Privacy Policy. It is a
    // hard gate: without it we have no recorded basis for the account.
    if (!consent) {
      return problem(400, { message: MESSAGES.consentRequired, field: 'consent', email });
    }

    const policy = checkPassword(password, email);
    if (!policy.ok) {
      return problem(400, { message: policy.message, field: 'password', email });
    }

    if (!event.locals.supabaseAuth) {
      return problem(503, { message: MESSAGES.unavailable, email });
    }

    const budget = await enforceAuthBudget('signup', event.getClientAddress(), email);
    if (!budget.allowed) {
      return problem(429, { message: MESSAGES.rateLimited, email });
    }

    const { data, error } = await event.locals.supabaseAuth.auth.signUp({
      email,
      password,
      options: {
        // Where the confirmation link lands. `next` rides along so the person
        // ends up where they started rather than on the homepage.
        emailRedirectTo: `${event.url.origin}/auth/callback?next=${encodeURIComponent(next)}`,
        data: { terms_accepted_at: new Date().toISOString() }
      }
    });

    if (error) {
      const mapped = mapAuthError(error, 'signup');
      // A 200 back from the mapper means "this is the already-exists case";
      // render the neutral view rather than an error. See authErrors.js.
      if (mapped.status === 200) return { pending: true, email, mode: 'signup' };
      return problem(mapped.status, { message: mapped.message, email });
    }

    await recordConsent(data?.user?.id, email);

    // Confirmations disabled on the Supabase project: signUp returns a live
    // session and the person is already signed in. Nothing to wait for.
    if (data?.session) throw redirect(303, next);

    return { pending: true, email, mode: 'signup' };
  },

  /**
   * Sign in with email + password.
   */
  signin: async (event) => {
    const form = await event.request.formData();
    const { email, next, trapped } = readCommon(form);
    const password = form.get('password');

    if (trapped) return problem(400, { message: MESSAGES.badCredentials, mode: 'signin' });

    if (!isValidEmail(email) || typeof password !== 'string' || password.length === 0) {
      // Same message as a genuine mismatch. A distinct "enter a valid email"
      // here would be fine, but keeping it uniform means no branch of this
      // action can be used to probe anything.
      return problem(400, {
        message: MESSAGES.badCredentials,
        field: 'email',
        email,
        mode: 'signin'
      });
    }

    if (!event.locals.supabaseAuth) {
      return problem(503, { message: MESSAGES.unavailable, email, mode: 'signin' });
    }

    const rateKey = `signin:id:${email}`;
    const budget = await enforceAuthBudget('signin', event.getClientAddress(), email);
    if (!budget.allowed) {
      return problem(429, {
        message: MESSAGES.rateLimited,
        email,
        mode: 'signin'
      });
    }

    const { data, error } = await event.locals.supabaseAuth.auth.signInWithPassword({
      email,
      password
    });

    if (error) {
      const mapped = mapAuthError(error, 'signin');
      return problem(mapped.status, { message: mapped.message, email, mode: 'signin' });
    }

    // Success clears the budget, so a run of typos does not lock someone out
    // of the account they just proved they own.
    await authRateReset(rateKey);

    // Attach any preorder placed under this address before accounts existed.
    // The trigger in sql/015 does this at account creation; doing it again on
    // sign-in picks up orders placed after that, and is idempotent.
    await claimEntitlements(data?.user?.id, email);

    throw redirect(303, next);
  },

  /**
   * Passwordless sign-in. "Prefer no password? Email me a sign-in link".
   *
   * `shouldCreateUser: false` matters. Left at its default of true, this
   * endpoint creates an account for any address posted to it, which turns the
   * form into a way to send our branded mail to strangers and fills the user
   * table with addresses that never consented to anything. Account creation
   * happens in `signup`, where the consent checkbox is.
   */
  magiclink: async (event) => {
    const form = await event.request.formData();
    const { email, next, trapped } = readCommon(form);

    if (trapped) return { pending: true, email, mode: 'magiclink' };

    if (!isValidEmail(email)) {
      return problem(400, { message: MESSAGES.invalidEmail, field: 'email', email });
    }

    if (!event.locals.supabaseAuth) {
      return problem(503, { message: MESSAGES.unavailable, email });
    }

    const budget = await enforceAuthBudget('magiclink', event.getClientAddress(), email);
    if (!budget.allowed) {
      return problem(429, { message: MESSAGES.emailRateLimited, email });
    }

    const { error } = await event.locals.supabaseAuth.auth.signInWithOtp({
      email,
      options: {
        shouldCreateUser: false,
        emailRedirectTo: `${event.url.origin}/auth/callback?next=${encodeURIComponent(next)}`
      }
    });

    // Note what is NOT branched on here: an address with no account produces an
    // error from GoTrue, and surfacing it would answer "does this person have
    // an account". The pending view is returned either way.
    if (error) mapAuthError(error, 'magiclink');

    return { pending: true, email, mode: 'magiclink' };
  },

  /**
   * "Resend the link" on the pending view. Same call as magiclink; separate
   * action so it carries its own budget and cannot be used to bypass that one.
   */
  resend: async (event) => {
    const form = await event.request.formData();
    const { email, next } = readCommon(form);

    if (!isValidEmail(email)) {
      return problem(400, { message: MESSAGES.invalidEmail, field: 'email', email });
    }
    if (!event.locals.supabaseAuth) {
      return problem(503, { message: MESSAGES.unavailable, email });
    }

    const budget = await enforceAuthBudget('resend', event.getClientAddress(), email);
    if (!budget.allowed) {
      return problem(429, { message: MESSAGES.emailRateLimited, email });
    }

    const { error } = await event.locals.supabaseAuth.auth.resend({
      type: 'signup',
      email,
      options: {
        emailRedirectTo: `${event.url.origin}/auth/callback?next=${encodeURIComponent(next)}`
      }
    });

    if (error) mapAuthError(error, 'resend');

    return { pending: true, resent: true, email };
  }
};

/**
 * Record Terms/Privacy acceptance on the profile row.
 *
 * The row itself is created by the `trg_handle_new_user` trigger in sql/015,
 * so this only stamps the consent time. `is null` in the filter makes it
 * non-destructive: re-running signup for an address that already accepted does
 * not move the original timestamp, which is the one that matters if acceptance
 * is ever questioned.
 *
 * @param {string|undefined} userId
 * @param {string} email
 */
async function recordConsent(userId, email) {
  if (!supabaseAdmin || !userId) return;
  const { error } = await supabaseAdmin
    .from('profiles')
    .update({ terms_accepted_at: new Date().toISOString(), updated_at: new Date().toISOString() })
    .eq('id', userId)
    .is('terms_accepted_at', null);
  if (error) console.error('[signup] consent stamp failed:', error.message);

  await claimEntitlements(userId, email);
}

/**
 * Attach preorders made under this address to the account.
 *
 * Safe to call on every sign-in: the SQL function only claims rows whose
 * user_id is null, so it never reassigns someone else's order.
 *
 * @param {string|undefined} userId
 * @param {string} email
 */
async function claimEntitlements(userId, email) {
  if (!supabaseAdmin || !userId) return;
  const { error } = await supabaseAdmin.rpc('claim_preorders_for_user', {
    p_user_id: userId,
    p_email: email
  });
  if (error) console.error('[signup] entitlement claim failed:', error.message);
}
