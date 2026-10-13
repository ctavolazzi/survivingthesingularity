/**
 * Activation codes: the pure half. Generation, normalization, hashing.
 *
 * Split from activationCodes.js for the same reason reconcileFormat.js is split
 * from reconcile.js and webhookEventPolicy.js from webhookEvents.js - nothing in
 * here touches the database, the network, or the environment, so it can be
 * tested directly by importing it. The half that talks to Postgres imports these
 * functions; these functions import nothing.
 *
 * An activation code is a bearer credential. Whoever holds the string gets an
 * account, so every decision here is the one you would make for a password
 * rather than for a coupon:
 *
 *   1. Unguessable      - 60 bits from a CSPRNG. Never Math.random().
 *   2. Unreadable at rest - only the SHA-256 digest ever reaches the database.
 *   3. Unambiguous aloud  - an alphabet that survives a phone call.
 *
 * The fourth property, unspendable-twice, cannot live here: it needs a row lock.
 * See redeem_activation_code() in sql/015 and the note in activationCodes.js.
 */

/**
 * Crockford base32, minus the letters that get misread.
 *
 * I, L and O are absent because they are indistinguishable from 1, 1 and 0 in
 * most typefaces and in all handwriting. U is absent for the reason Crockford
 * gives: excluding it makes accidental obscenities substantially less likely,
 * which matters for a string that gets printed on cards and read aloud at
 * conferences. 32 symbols is exactly 5 bits each, which is what makes the
 * generator below bias-free.
 */
export const ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';

/** Symbols per code. 12 x 5 bits = 60 bits of entropy. */
export const CODE_LENGTH = 12;

/** Rendered as XXXX-XXXX-XXXX. Grouping is for human eyes only. */
export const GROUP_SIZE = 4;

/**
 * Transcription repairs, applied during normalization.
 *
 * Someone reading a code off a card will type O for 0 and I or L for 1, because
 * that is what the glyphs look like. Crockford's decoding rules say to accept
 * those and fold them in. It costs nothing - the excluded letters can never
 * appear in a generated code, so there is no collision to create - and it turns
 * a guaranteed class of support email into a silent success.
 */
export const CONFUSABLES = { O: '0', I: '1', L: '1', U: 'V' };

/**
 * A fresh code, in display form.
 *
 * No modulo bias, and worth spelling out rather than trusting: a CSPRNG byte is
 * uniform over 0-255, and 256 is exactly 8 x 32, so every value of `byte & 31`
 * is produced by exactly eight byte values. The mask is uniform over the
 * alphabet. The usual `% alphabet.length` version of this bug needs the alphabet
 * length to divide 256 too - but the mask states that dependency instead of
 * hiding it, and the assertion below makes shortening ALPHABET fail loudly
 * rather than skew the distribution quietly.
 *
 * @returns {string} e.g. "K3QP-7ZMR-9TFA"
 */
export function generateActivationCode() {
  if (ALPHABET.length !== 32) {
    throw new Error('ALPHABET must be exactly 32 symbols; the 5-bit mask depends on it.');
  }
  const bytes = new Uint8Array(CODE_LENGTH);
  globalThis.crypto.getRandomValues(bytes);

  let out = '';
  for (let i = 0; i < CODE_LENGTH; i++) {
    if (i > 0 && i % GROUP_SIZE === 0) out += '-';
    out += ALPHABET[bytes[i] & 31];
  }
  return out;
}

/**
 * Fold user input into the exact string that was hashed at mint time.
 *
 * Everything presentational comes out: case, the grouping dashes, spaces a phone
 * keyboard inserted, zero-width characters that survive a paste out of a styled
 * email. Then confusable glyphs are repaired. What remains must be CODE_LENGTH
 * symbols drawn from ALPHABET, or this returns null and the caller rejects the
 * input without ever touching the database.
 *
 * @param {unknown} input
 * @returns {string|null} canonical ungrouped code, or null if it cannot be one
 */
export function normalizeActivationCode(input) {
  if (typeof input !== 'string') return null;

  // Strip anything that is not a letter or digit: dashes, spaces, non-breaking
  // spaces, and the zero-width joiners that survive a copy out of HTML email.
  const stripped = input.toUpperCase().replace(/[^0-9A-Z]/g, '');
  if (stripped.length !== CODE_LENGTH) return null;

  let canonical = '';
  for (const ch of stripped) {
    const repaired = CONFUSABLES[ch] ?? ch;
    if (!ALPHABET.includes(repaired)) return null;
    canonical += repaired;
  }
  return canonical;
}

/** Insert the display dashes back into a canonical code. */
export function formatActivationCode(canonical) {
  return (canonical.match(new RegExp(`.{1,${GROUP_SIZE}}`, 'g')) ?? []).join('-');
}

/**
 * SHA-256 of a canonical code, lowercase hex.
 *
 * Unsalted, which is correct here rather than an oversight. Salt exists to
 * defeat precomputation against low-entropy secrets - the passwords people
 * choose. These are 60 CSPRNG bits: there is no dictionary to precompute and
 * nothing for a salt to buy. Unsalted also keeps lookup a single indexed
 * equality on `code_hash` rather than a scan that rehashes every row against
 * the candidate.
 *
 * Web Crypto rather than node:crypto, so this runs unchanged on Cloudflare
 * Workers - which is what adapter-auto targets for this site, and is where the
 * previous attempt at auth here fell over.
 *
 * @param {string} canonical output of normalizeActivationCode()
 * @returns {Promise<string>}
 */
export async function hashActivationCode(canonical) {
  const bytes = new TextEncoder().encode(canonical);
  const digest = await globalThis.crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Reasons a code can fail, in words safe to show a stranger.
 *
 * `not_found` deliberately reads identically to a malformed code. Distinguishing
 * "that code does not exist" from "that is not a code" hands an attacker an
 * enumeration oracle for free and helps a real user not at all - either way the
 * answer is "check what you typed".
 */
const REASON_TEXT = {
  not_found: "That code isn't valid. Check for typos and try again.",
  expired: 'That code has expired.',
  revoked: 'That code is no longer active.',
  exhausted: 'That code has already been used.',
  unavailable: 'Activation codes are temporarily unavailable. Try again shortly.',
};

/** @param {string} reason */
export function activationErrorText(reason) {
  return REASON_TEXT[reason] ?? REASON_TEXT.not_found;
}
