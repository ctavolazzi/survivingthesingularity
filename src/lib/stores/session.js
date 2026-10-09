/**
 * Client-side view of "am I signed in", for chrome that has to render before
 * the answer is known.
 *
 * The root layout is prerendered (src/routes/+layout.server.js), so no
 * component rendered inside it can learn the session from layout data - the
 * HTML was built long before the request existed. Anything that needs the
 * answer asks /api/session after hydration. See that endpoint's header for why
 * un-prerendering the layout is the wrong fix.
 *
 * `status` is three-valued rather than a boolean, and that matters:
 *
 *   'unknown'  - not asked yet. The navbar renders NOTHING in this state, so a
 *                signed-in visitor never sees "Sign in" flash before their own
 *                name appears. A boolean would have to default to false, which
 *                is a guess rendered as fact.
 *   'signedIn' / 'signedOut' - measured.
 *
 * Deliberately not persisted to localStorage. A cached "signed in" that
 * outlives the cookie shows an account menu to someone with no session, and
 * every link in it would then bounce them to /signup. The real session lives in
 * an httpOnly cookie; this is a render hint, and it is cheap to re-ask.
 */

import { writable } from 'svelte/store';
import { browser } from '$app/environment';

/** @type {import('svelte/store').Writable<{status: 'unknown'|'signedIn'|'signedOut', displayName: string}>} */
export const session = writable({ status: 'unknown', displayName: '' });

let inFlight = null;

/**
 * Ask the server who we are. Safe to call from several components: concurrent
 * callers share one request.
 *
 * @param {typeof fetch} [fetchImpl]
 * @returns {Promise<void>}
 */
export function refreshSession(fetchImpl = globalThis.fetch) {
  if (!browser) return Promise.resolve();
  if (inFlight) return inFlight;

  inFlight = fetchImpl('/api/session', {
    headers: { accept: 'application/json' },
    // The endpoint sets no-store, but a browser will still reuse a fresh
    // response from its own memory cache within a navigation; this makes the
    // answer follow a sign-out that happened in another tab.
    cache: 'no-store'
  })
    .then((r) => (r.ok ? r.json() : null))
    .then((data) => {
      if (!data) {
        // Endpoint unreachable or erroring. Signed-out is the safe render:
        // it offers a way in, whereas a wrong signed-in state offers a menu
        // of links that all fail.
        session.set({ status: 'signedOut', displayName: '' });
        return;
      }
      session.set({
        status: data.signedIn ? 'signedIn' : 'signedOut',
        displayName: typeof data.displayName === 'string' ? data.displayName : ''
      });
    })
    .catch(() => {
      session.set({ status: 'signedOut', displayName: '' });
    })
    .finally(() => {
      inFlight = null;
    });

  return inFlight;
}
