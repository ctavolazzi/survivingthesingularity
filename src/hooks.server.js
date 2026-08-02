/**
 * Server hooks.
 *
 * AUTH, AND WHY THE OLD COMMENT HERE IS NO LONGER TRUE
 *
 * This file used to open "no auth. The site is read-only and does not maintain
 * user sessions", and stubbed safeGetSession() to null. That was accurate from
 * WO-08 until the /signup flow landed. Accounts now exist, so the stub is a
 * real implementation.
 *
 * What has NOT changed is the rule the old comment was protecting: there is
 * still no browser-side Supabase client and no publishable key in the bundle.
 * Sessions are established server-side and carried in httpOnly cookies. See
 * the header of `$lib/server/supabaseAuth.js` for why that is the only shape
 * of auth compatible with sql/012, and README's "Database access" section for
 * the data rule, which is untouched: every table read still goes through
 * `$lib/server/supabaseAdmin.js` on the service role.
 *
 * `event.locals` after this hook:
 *   supabaseAuth  - request-scoped GoTrue client, or null if unconfigured
 *   safeGetSession- verified session getter (round-trips to the auth server)
 *   session/user  - resolved once per request, null when signed out
 */

import { createAuthClient, safeGetSession } from '$lib/server/supabaseAuth.js';

export async function handle({ event, resolve }) {
  // Fix for "[object Object]" navigation errors (pre-existing safety net)
  if (event.url.pathname.includes('[object%20Object]') || event.url.pathname.includes('[object Object]')) {
    return new Response('Redirect', {
      status: 302,
      headers: { Location: '/' }
    });
  }

  // Request-scoped auth client. Null when SUPABASE_ANON_KEY is unset, which is
  // the normal state of a local checkout with no secrets - every consumer below
  // degrades to signed-out rather than throwing, so the site still renders.
  event.locals.supabaseAuth = createAuthClient(event);

  // Verified, not decoded. See safeGetSession()'s header: it round-trips to the
  // auth server, because the cookie it would otherwise trust is attacker input.
  event.locals.safeGetSession = () => safeGetSession(event.locals.supabaseAuth);

  const { session, user } = await event.locals.safeGetSession();
  event.locals.session = session;
  event.locals.user = user;

  const response = await resolve(event, {
    // Supabase's client library reads these off responses it makes itself. It
    // makes none in the browser here, but SvelteKit strips unlisted headers
    // from `fetch` responses it serializes into the page, and omitting this is
    // a documented source of silent session-refresh failures if a load
    // function ever proxies an auth call. Cheap insurance, no downside.
    filterSerializedResponseHeaders: (name) =>
      name === 'content-range' || name === 'x-supabase-api-version'
  });

  // Security headers for SSR routes (Worker). CSP is handled by kit.csp in
  // svelte.config.js, which injects per-request nonces into SvelteKit's own
  // inline scripts and sets the CSP header automatically. Prerendered pages
  // get CSP from static/_headers (served by Cloudflare Pages CDN, no Worker).
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'SAMEORIGIN');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=()');
  response.headers.set('Cross-Origin-Opener-Policy', 'same-origin');
  response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');

  return response;
}
