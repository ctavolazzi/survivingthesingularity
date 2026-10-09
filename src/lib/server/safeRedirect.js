/**
 * Where a `?next=` parameter is allowed to send someone.
 *
 * WHY THIS IS NOT JUST `params.get('next') ?? '/'`
 *
 * Every auth route here takes a return path: the signup page keeps it so you
 * land back where you were, and the OAuth callback has to carry it across the
 * provider round trip. Handing that value straight to `redirect()` is the
 * classic open-redirect bug, and on an auth route specifically it is the
 * phishing primitive: a link to
 *
 *   https://survivingthesingularity.com/signup?next=https://evil.example/login
 *
 * is a genuine link to this site, on this domain, with a valid certificate,
 * which lands the visitor on a copy of our sign-in form the moment they
 * authenticate. The domain in the address bar is the only thing most people
 * check, and up until the final hop it is ours.
 *
 * So: allow same-site paths only, and be strict about what counts as one.
 */

/**
 * True if the string contains a C0 control character or DEL.
 *
 * Written as a codepoint scan rather than a regex character class on purpose:
 * a class like /[\x00-\x1f]/ invites someone to paste the literal bytes into
 * the source while editing, which produces a file with raw NULs in it that
 * looks fine in a diff. This form cannot be got wrong by copy-paste.
 *
 * What it stops: a CR or LF inside the redirect target, which on some stacks
 * splits the Location header and lets the caller append headers of their own.
 *
 * @param {string} s
 * @returns {boolean}
 */
function hasControlChars(s) {
  for (let i = 0; i < s.length; i++) {
    const c = s.charCodeAt(i);
    if (c <= 0x1f || c === 0x7f) return true;
  }
  return false;
}

/**
 * @param {unknown} target the untrusted `next` value
 * @param {string} [fallback] where to go when `target` is not acceptable
 * @returns {string} a path that is safe to redirect to
 */
export function safeRedirect(target, fallback = '/') {
  if (typeof target !== 'string' || target.length === 0) return fallback;

  // Must be an absolute path on this site. This one check rejects
  // `https://evil.example`, `//evil.example` (protocol-relative, which browsers
  // treat as absolute), and `javascript:alert(1)` in one go, because none of
  // them start with a single `/`.
  if (!target.startsWith('/') || target.startsWith('//')) return fallback;

  // `/\evil.example` - some browsers normalise the backslash to a forward
  // slash, which turns it back into a protocol-relative URL after the check
  // above has already passed it.
  if (target.startsWith('/\\')) return fallback;

  if (hasControlChars(target)) return fallback;

  // Do not bounce someone back into the auth flow they just finished; that
  // produces a redirect loop between /signup and /auth/callback.
  if (target.startsWith('/auth/')) return fallback;

  return target;
}
