import { BOOK_ACCESS_COOKIE } from '$lib/server/bookAccess.js';

// Password-gated route: must run per-request (cookie check), so it cannot
// be baked to static HTML at build time. Overrides the site-wide
// prerender=true from the root layout for everything under /book.
export const prerender = false;

/** @type {import('./$types').LayoutServerLoad} */
export async function load(event) {
  return { unlocked: event.cookies.get(BOOK_ACCESS_COOKIE) === '1' };
}
