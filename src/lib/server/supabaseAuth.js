/**
 * The Supabase Auth client, constructed per request, server-side only.
 *
 * WHY THIS FILE DOES NOT CONTRADICT THE "NO BROWSER CLIENT" RULE
 *
 * README's "Database access" section and CLAUDE.md both say: no browser-side
 * Supabase client, no PUBLIC_SUPABASE_* key, src/lib/supabase.js was deleted in
 * WO-08 and must not come back. Supabase's own SvelteKit auth quickstart tells
 * you to do the opposite - create a browser client, ship the publishable key,
 * let the browser talk to /auth/v1 directly. That guide is written for projects
 * that also let the browser talk to PostgREST. This one does not, and sql/012
 * revoked the grants that would make it work anyway.
 *
 * So auth is done the other way round. The browser posts an ordinary form to a
 * SvelteKit action; this module, running on the server, talks to GoTrue and
 * writes the resulting session into cookies. What the browser gets back is a
 * cookie and a redirect. Consequences, all of them good:
 *
 *   * the anon key stays in $env/dynamic/private and never enters the bundle
 *   * svelte.config.js `connect-src` stays `'self'` - no supabase.co origin has
 *     to be added, so the CSP comment there stays true
 *   * session cookies can be httpOnly, which is impossible when a browser
 *     client has to read them. An XSS on this site cannot exfiltrate a session.
 *   * the flow degrades to a plain HTML form post with JS disabled
 *
 * The cost is one server round trip per auth action, which is the same round
 * trip every other form on this site already makes.
 *
 * ENV
 *
 * SUPABASE_ANON_KEY is new. It is the same publishable key Supabase shows in
 * the dashboard; the name has no PUBLIC_ prefix precisely because SvelteKit
 * would then inline it into client bundles, which is the thing we are avoiding.
 * Dynamic env, so a missing key yields a null client and callers degrade -
 * matching supabaseAdmin.js rather than crashing the build.
 */

import { createServerClient } from '@supabase/ssr';
import { env } from '$env/dynamic/private';
import { dev } from '$app/environment';
import { supabaseConfigured } from '$lib/server/supabaseEnv.js';

const url = env.SUPABASE_URL;
const anonKey = env.SUPABASE_ANON_KEY;

/**
 * True when auth is configured well enough to attempt a sign-in.
 *
 * Validates the URL, not just its presence. createServerClient throws on a
 * malformed one, and this module is reached from hooks.server.js on every
 * request, so an unvalidated value turns one bad environment variable into a
 * site-wide 500. See $lib/server/supabaseEnv.js.
 */
export const authConfigured = supabaseConfigured(url, anonKey, 'supabaseAuth');

/**
 * Cookie options for every auth cookie we set.
 *
 * httpOnly: nothing in the browser reads these - there is no browser client.
 * sameSite 'lax' rather than 'strict': the OAuth provider redirects the user
 * back to us with a top-level GET, and 'strict' withholds cookies on a
 * cross-site-initiated navigation, which would drop the PKCE verifier and make
 * every OAuth sign-in fail at the callback. 'lax' sends them on top-level GETs
 * and withholds them on cross-site POSTs, which is exactly the boundary we want.
 */
const COOKIE_DEFAULTS = {
  path: '/',
  httpOnly: true,
  sameSite: 'lax',
  secure: !dev
};

/**
 * Build a request-scoped auth client bound to this event's cookie jar.
 *
 * @param {import('@sveltejs/kit').RequestEvent} event
 * @returns {import('@supabase/supabase-js').SupabaseClient|null} null when unconfigured
 */
export function createAuthClient(event) {
  if (!authConfigured) return null;

  return createServerClient(url, anonKey, {
    cookies: {
      getAll: () => event.cookies.getAll(),
      setAll: (cookiesToSet) => {
        for (const { name, value, options } of cookiesToSet) {
          // Our defaults win over the library's. It proposes sameSite/secure
          // values tuned for a browser client that needs to read the cookie;
          // we override because nothing here does. `path` must be set or
          // SvelteKit throws, and the library does not always supply one.
          event.cookies.set(name, value, { ...options, ...COOKIE_DEFAULTS });
        }
      }
    },
    auth: {
      // PKCE, not implicit. The code lands in a server-side query string and is
      // exchanged server-side against a verifier held in an httpOnly cookie, so
      // no token ever transits the URL fragment or touches client JS.
      flowType: 'pkce'
    }
  });
}

/**
 * Resolve the current session, verifying it rather than trusting the cookie.
 *
 * WHY NOT JUST getSession()
 *
 * getSession() decodes the JWT sitting in the cookie and hands it back without
 * asking the auth server whether it is real. On the server that is a trust
 * boundary violation: the cookie is attacker-supplied input, and a forged one
 * decodes just fine. getUser() makes a round trip that validates the signature
 * and the revocation state.
 *
 * So: take the claims from getSession() for cheap fields, but let getUser()
 * decide whether there is a user at all. If getUser() fails, there is no
 * session, whatever the cookie says.
 *
 * @param {import('@supabase/supabase-js').SupabaseClient|null} supabase
 * @returns {Promise<{session: any|null, user: any|null}>}
 */
export async function safeGetSession(supabase) {
  if (!supabase) return { session: null, user: null };

  const { data: { session } } = await supabase.auth.getSession();
  if (!session) return { session: null, user: null };

  const { data: { user }, error } = await supabase.auth.getUser();
  if (error || !user) {
    // Expired, revoked, or forged. Treat all three the same.
    return { session: null, user: null };
  }

  return { session, user };
}
