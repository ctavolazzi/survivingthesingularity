// The password gate is now a pure client-side check (see +layout.svelte and
// $lib/bookAccessCode.js) - no server env var to misconfigure across
// environments. This file now only keeps the prerender override: /book and
// /book/[sectionId] load per-request markdown content, so they can't be
// baked to static HTML at build time like the site-wide default.
export const prerender = false;
