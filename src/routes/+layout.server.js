// Prerender by default: this is a read-only content site, so every page should
// be baked to static HTML and served from the CDN edge. Genuinely dynamic routes
// (live counts, query-param pages, API endpoints) opt back out with
// `export const prerender = false`.
export const prerender = true;

/** @type {import('./$types').LayoutServerLoad} */
export async function load() {
  // No auth on this site. Returning stub user/session so layout components
  // that destructure data.user don't blow up during the transition.
  return { session: null, user: null };
}
