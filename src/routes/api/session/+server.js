/**
 * Who is signed in, for the navbar. GET /api/session
 *
 * WHY THIS ENDPOINT HAS TO EXIST
 *
 * The obvious way to render a signed-in navbar is `data.user` from the root
 * layout load. That cannot work here: src/routes/+layout.server.js sets
 * `prerender = true`, so the layout's HTML is baked once at build time and
 * served from the CDN. There is no request at build time, therefore no session,
 * and its load() returns a stub `{session: null, user: null}` precisely because
 * of that.
 *
 * Un-prerendering the root layout would fix the navbar and cost the entire
 * site its static delivery, which is a bad trade for one widget. So the navbar
 * ships its account control EMPTY and asks this endpoint who it is talking to
 * once it hydrates. It renders nothing at all until the answer arrives, rather
 * than defaulting to "Sign in": an empty slot for ~50ms is quieter than showing
 * every signed-in visitor the wrong label on every page load. The control
 * reserves its width up front so resolving it does not shift the nav sideways.
 * See the three-valued `status` in $lib/stores/session.js, which exists to make
 * "not asked yet" distinguishable from "signed out".
 *
 * WHAT IT DELIBERATELY DOES NOT RETURN
 *
 * No email, no id, no token. A display name and a boolean are everything the
 * navbar needs, and anything more is a detail that would end up in a fetch
 * response that some future proxy decides to cache.
 *
 * CACHING IS THE WHOLE RISK
 *
 * This response is per-user and must never be shared. Cloudflare sits in front
 * of this origin and caches aggressively by default; one cached hit of this
 * endpoint would show one visitor's name to everyone who asked next.
 * `private, no-store` plus `Vary: Cookie` is what stops that, and it is the
 * reason this file exists rather than the state being folded into some other
 * response that does not carry those headers.
 */

import { json } from '@sveltejs/kit';

// Reads a live session off the request. Nothing to prerender.
export const prerender = false;

/** @type {import('./$types').RequestHandler} */
export async function GET(event) {
  const user = event.locals.user;

  /** @type {Record<string, string>} */
  const headers = {
    'cache-control': 'private, no-store, max-age=0',
    vary: 'Cookie'
  };

  if (!user) {
    return json({ signedIn: false }, { headers });
  }

  const meta = user.user_metadata ?? {};
  const displayName =
    meta.full_name ||
    meta.name ||
    (typeof user.email === 'string' ? user.email.split('@')[0] : '') ||
    'Account';

  return json({ signedIn: true, displayName }, { headers });
}
