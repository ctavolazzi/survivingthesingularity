/**
 * Sign out. POST only.
 *
 * WHY NOT A GET
 *
 * A `<a href="/auth/signout">` is easier and is a bug. Anything that can cause
 * a GET to a URL can then sign people out: a prefetch, a link preview bot, an
 * `<img src>` on someone else's page. It is a mild denial of service rather
 * than a breach, but it is also trivially avoidable. This being a form action
 * additionally puts it inside SvelteKit's CSRF protection, which a GET route
 * would sit outside.
 *
 * Use it from anywhere with:
 *
 *   <form method="POST" action="/auth/signout"><button>Sign out</button></form>
 *
 * There is no +page.svelte beside this file on purpose: the action always
 * redirects, so the page is never rendered. A GET to /auth/signout falls
 * through to `load`, which sends the visitor home.
 */

import { redirect } from '@sveltejs/kit';
import { safeRedirect } from '$lib/server/safeRedirect.js';

// Opt out of the site-wide `prerender = true` (src/routes/+layout.server.js).
export const prerender = false;

/** @type {import('./$types').PageServerLoad} */
export function load() {
  throw redirect(303, '/');
}

/** @type {import('./$types').Actions} */
export const actions = {
  default: async (event) => {
    const form = await event.request.formData().catch(() => null);
    const next = safeRedirect(form?.get('next'), '/');

    if (event.locals.supabaseAuth) {
      // Revokes the refresh token server-side, so the session is dead even if
      // a copy of the cookie was captured. `signOut()` also instructs the
      // cookie adapter in supabaseAuth.js to clear the auth cookies.
      const { error } = await event.locals.supabaseAuth.auth.signOut();
      if (error) console.error('[auth:signout]', error.message);
    }

    // Clear locals too. Without this, anything that runs after this action in
    // the same request still sees the old user.
    event.locals.session = null;
    event.locals.user = null;

    throw redirect(303, next);
  }
};
