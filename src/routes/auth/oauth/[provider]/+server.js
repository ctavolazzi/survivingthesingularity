/**
 * Start an OAuth sign-in. GET /auth/oauth/google?next=/read
 *
 * WHY THIS IS A GET LINK AND NOT A FORM POST
 *
 * Everything else in the signup flow is a form action, because SvelteKit's
 * CSRF protection covers form posts and JSON endpoints have to roll their own
 * (see $lib/server/sameOrigin.js). Starting OAuth the same way looks obviously
 * right and does not work, because of a policy already in svelte.config.js:
 *
 *   'form-action': ["'self'"]
 *
 * `form-action` is enforced against the whole navigation chain a form
 * submission starts, redirects included - Firefox has always done this and
 * Chrome does it too. So a POST to our own origin that answers `303 Location:
 * https://accounts.google.com/...` is blocked by our own CSP, silently, at the
 * redirect. The button would do nothing and the console would blame a policy
 * nobody was thinking about.
 *
 * A plain link is a top-level navigation, which `form-action` does not govern,
 * and no `connect-src` or `frame-src` entry is needed either because nothing is
 * fetched or framed. The provider origins therefore stay out of the CSP
 * entirely, which keeps svelte.config.js's "no Supabase origin here" comment
 * true.
 *
 * WHAT PROTECTS A GET THAT STARTS A LOGIN
 *
 * Not much needs to. The risk for a GET entry point is login CSRF - tricking
 * someone into starting a sign-in they did not intend - and it is bounded
 * here: the PKCE verifier is written to an httpOnly, SameSite=Lax cookie on
 * this request, and /auth/callback will only complete an exchange that matches
 * it. An attacker can cause a redirect to Google; they cannot complete a
 * session in this browser, and they cannot read the result.
 */

import { error, redirect } from '@sveltejs/kit';
import { safeRedirect } from '$lib/server/safeRedirect.js';
import { enforceAuthBudget } from '$lib/server/authRateLimit.js';
import { MESSAGES } from '$lib/server/authErrors.js';

/**
 * Allowlist. `[provider]` is a path parameter, which means it is attacker
 * controlled, and it is passed to signInWithOAuth. Without this, the route
 * accepts any provider string Supabase happens to recognise and turns our
 * domain into a redirector to whatever is configured on the project.
 */
const ALLOWED_PROVIDERS = new Set(['google', 'github']);

// Opt out of the site-wide `prerender = true` (src/routes/+layout.server.js).
export const prerender = false;

/** @type {import('./$types').RequestHandler} */
export async function GET(event) {
  const provider = event.params.provider;

  if (!ALLOWED_PROVIDERS.has(provider)) {
    throw error(404, 'Unknown sign-in provider.');
  }

  const next = safeRedirect(event.url.searchParams.get('next'), '/');

  if (!event.locals.supabaseAuth) {
    throw redirect(303, `/signup?error=${encodeURIComponent(MESSAGES.unavailable)}`);
  }

  const budget = await enforceAuthBudget('oauth', event.getClientAddress());
  if (!budget.allowed) {
    throw redirect(303, `/signup?error=${encodeURIComponent(MESSAGES.rateLimited)}`);
  }

  const { data, error: oauthError } = await event.locals.supabaseAuth.auth.signInWithOAuth({
    provider,
    options: {
      redirectTo: `${event.url.origin}/auth/callback?next=${encodeURIComponent(next)}`,
      // Do not let the library perform the redirect itself; we want the URL so
      // SvelteKit issues it, and so the PKCE cookie set above is committed to
      // the same response.
      skipBrowserRedirect: true
    }
  });

  if (oauthError || !data?.url) {
    console.error('[auth:oauth]', provider, oauthError?.message ?? 'no url returned');
    throw redirect(303, `/signup?error=${encodeURIComponent(MESSAGES.oauthFailed)}`);
  }

  throw redirect(303, data.url);
}
