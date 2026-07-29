/**
 * The same-origin check for state-changing API routes, in one place.
 *
 * WHY THIS IS A MODULE AND NOT FIVE COPIES
 *
 * Every POST route here carried its own copy of:
 *
 *   const origin = request.headers.get('origin');
 *   if (origin && origin !== url.origin) return 403;
 *
 * which fails OPEN. The `origin &&` guard means the entire check is skipped
 * whenever the header is absent, so any non-browser client walks straight
 * through by simply not sending it. Browsers always attach Origin to a POST;
 * curl does not. The check was therefore blocking honest browsers from other
 * sites while waving through exactly the scripted clients it existed to stop.
 *
 * That was fixed in /api/waitlist on 2026-07-28 and verified in production.
 * The other four routes kept their copies and stayed broken - confirmed live on
 * 2026-07-29, where a POST to /api/checklist-email with no Origin header
 * reached email validation instead of being refused. One fix, five files, four
 * of them missed: the copies are the bug.
 *
 * SvelteKit's built-in CSRF protection covers form-style content types
 * (urlencoded, multipart, text/plain) but deliberately not application/json,
 * because JSON cannot be produced by a plain HTML form cross-site. Every route
 * here takes JSON, so this check is what stands in that gap rather than a
 * redundant belt on top of SvelteKit's.
 */

/** Origin of a Referer URL, or null if it is absent or unparseable. */
function refererOrigin(referer) {
  if (!referer) return null;
  try {
    return new URL(referer).origin;
  } catch {
    return null;
  }
}

/**
 * True when the request demonstrably came from our own origin.
 *
 * Fails CLOSED: a request carrying neither an Origin nor a same-origin Referer
 * is refused. That costs no real traffic, because browsers attach Origin to
 * every POST including same-origin ones, and every caller in this codebase is
 * a same-origin fetch. Referer is accepted as a fallback for the rare privacy
 * tool that strips one header but not the other.
 *
 * @param {Request} request
 * @param {URL} url the request URL, whose `.origin` is what we expect to match
 * @returns {boolean}
 */
export function isSameOrigin(request, url) {
  const origin = request.headers.get('origin');
  const expected = url.origin;
  return origin
    ? origin === expected
    : refererOrigin(request.headers.get('referer')) === expected;
}
