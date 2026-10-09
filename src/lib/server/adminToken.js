/**
 * Bearer-token check for admin-only endpoints.
 *
 * Pure and dependency-free for the same reason webhookEventPolicy.js is: this is
 * the code standing between the open internet and a list of customer email
 * addresses with payment references attached, so it needs to be exhaustively
 * testable without a server, a database, or an environment.
 *
 * THIS LAYER FAILS SHUT. THAT IS THE OPPOSITE OF THE BOOKKEEPING LAYER.
 *
 * webhookEvents.js deliberately degrades OPEN: if its table is missing it lets
 * the order through, because blocking a paid order to protect a log entry is the
 * wrong trade. This module degrades SHUT: no token configured means no access,
 * ever. The asymmetry is the point, and it comes from what each one is
 * protecting. Losing a log line costs a report. Leaking the customer list costs
 * the customers.
 *
 * A missing secret is the single most common way an admin endpoint ends up
 * world-readable, because "unset" and "matches" both look like falsy-versus-falsy
 * to a careless comparison. Hence the explicit configured check below, and hence
 * the minimum length: a token of "admin" is not protection, and silently
 * accepting one would be the same class of false reassurance as a comment
 * claiming an invariant nothing enforces.
 */

/**
 * Shortest token this will operate with.
 *
 * 32 characters of a reasonable alphabet is past the point where online guessing
 * matters. The reason for enforcing it here rather than trusting whoever sets the
 * variable is that the failure is invisible: a weak token works perfectly in
 * testing and is the whole security boundary in production.
 */
export const MIN_TOKEN_LENGTH = 32;

/**
 * Compare two strings without leaking their contents through timing.
 *
 * `crypto.timingSafeEqual` is a Node API and does not exist on the Cloudflare
 * Workers runtime this deploys to, so the comparison is done by hand. Every byte
 * of the longer string is always visited and the result is accumulated with OR,
 * so the loop count depends on length alone and never on where the first
 * mismatch falls.
 *
 * Length itself is not hidden. That is accepted: token length is not the secret.
 */
export function constantTimeEqual(a, b) {
  const sa = String(a ?? '');
  const sb = String(b ?? '');

  // Compare over the longer of the two so a short candidate cannot exit early.
  const len = Math.max(sa.length, sb.length);
  let diff = sa.length ^ sb.length;

  for (let i = 0; i < len; i++) {
    // charCodeAt past the end returns NaN, and NaN ^ x is not usable, so read
    // out-of-range positions as 0. Positions beyond one string are already
    // accounted for by the length term seeded into diff above.
    const ca = i < sa.length ? sa.charCodeAt(i) : 0;
    const cb = i < sb.length ? sb.charCodeAt(i) : 0;
    diff |= ca ^ cb;
  }

  return diff === 0;
}

/**
 * Pull the bearer token out of an Authorization header.
 *
 * Header only, never a query parameter. A token in a URL ends up in access logs,
 * proxy logs, browser history and Referer headers, which turns one secret into
 * as many copies as there are hops.
 *
 * @param {string|null|undefined} header
 * @returns {string|null}
 */
export function parseBearer(header) {
  if (typeof header !== 'string') return null;
  const match = /^Bearer[ \t]+(.+)$/i.exec(header.trim());
  if (!match) return null;
  const token = match[1].trim();
  return token.length > 0 ? token : null;
}

/**
 * @typedef {object} AuthResult
 * @property {boolean} ok
 * @property {'ok'|'not-configured'|'token-too-short'|'missing-token'|'bad-token'} reason
 * @property {number} status HTTP status the caller should return
 */

/**
 * Decide whether a request carrying `header` may see admin data.
 *
 * @param {string|null|undefined} header the raw Authorization header
 * @param {string|null|undefined} expected the configured secret
 * @returns {AuthResult}
 */
export function authorizeAdmin(header, expected) {
  const secret = typeof expected === 'string' ? expected.trim() : '';

  // Not configured. 503 rather than 401 on purpose: 401 would tell an operator
  // their token was wrong when the truth is the server has no token at all, and
  // that misdiagnosis is how an endpoint stays broken for weeks.
  if (secret.length === 0) {
    return { ok: false, reason: 'not-configured', status: 503 };
  }

  // Configured but too weak to be a boundary. Refuse rather than pretend.
  if (secret.length < MIN_TOKEN_LENGTH) {
    return { ok: false, reason: 'token-too-short', status: 503 };
  }

  const provided = parseBearer(header);
  if (provided === null) {
    return { ok: false, reason: 'missing-token', status: 401 };
  }

  if (!constantTimeEqual(provided, secret)) {
    return { ok: false, reason: 'bad-token', status: 401 };
  }

  return { ok: true, reason: 'ok', status: 200 };
}
