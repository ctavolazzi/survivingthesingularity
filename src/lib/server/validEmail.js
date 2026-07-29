/**
 * One email validator, shared.
 *
 * WHY THIS IS A MODULE
 *
 * The same rule was written out separately in `/api/waitlist` and
 * `/api/discord-application`, character for character, and a third, looser
 * variant lives in `/api/checklist-email`. That is exactly the shape of the
 * fail-open origin check: one rule, several copies, and a fix that lands in one
 * of them. `$lib/server/sameOrigin.js` exists for the same reason.
 *
 * `/api/checklist-email` is deliberately NOT converted here. Its rule is
 * genuinely different (it accepts addresses this one rejects), so folding it in
 * would change what that endpoint accepts as a side effect of a refactor. It
 * should be converted on purpose, with its own before-and-after, not smuggled
 * into an unrelated change.
 */

// Deliberately conservative. This gates the money path: an address that passes
// here is the address Stripe will charge and the address the bundle is sent to,
// and there is no second chance to correct a typo after the card is charged.
const EMAIL_RE = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;
const MAX_EMAIL_LENGTH = 254; // RFC 5321

/**
 * Trim and lowercase. Lowercasing matters beyond tidiness: `preorders` carries
 * `unique (email, edition_type)` over raw text, so `A@b.com` and `a@b.com` are
 * two different rows and would each be allowed to buy a copy. Normalizing
 * everything we send onward converges the stored data on one form.
 *
 * @param {unknown} v
 * @returns {string} normalized address, or '' if the input was not a string
 */
export function normalizeEmail(v) {
  return typeof v === 'string' ? v.trim().toLowerCase() : '';
}

/**
 * @param {string} email an already-normalized address
 * @returns {boolean}
 */
export function isValidEmail(email) {
  return Boolean(email) && email.length <= MAX_EMAIL_LENGTH && EMAIL_RE.test(email);
}
