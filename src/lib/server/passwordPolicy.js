/**
 * The password rule, server-side and authoritative.
 *
 * The signup page has a strength meter and a `pw.length < 8` check in its
 * submit handler. Both are guidance for the person typing. Neither is a
 * control: the form posts to an endpoint, and an endpoint that trusts the
 * page's validation has no validation. This module is what actually decides.
 *
 * WHY THE FLOOR IS 8 AND NOT 12
 *
 * Because the UI already promises "8 characters minimum" in the field hint,
 * and a server that rejects what the label invites is a bug in the pair, not a
 * stricter policy. If the floor should be 12, the hint changes with it - in
 * `strengthHint()` below, which the page renders, so the two cannot drift.
 *
 * The composition rules (a digit, a symbol, mixed case) that usually accompany
 * a length floor are deliberately absent. They push people toward `Password1!`
 * and are not what NIST SP 800-63B has recommended since 2017; the guidance is
 * length plus a check against known-compromised and obvious values, which is
 * what this does.
 */

// bcrypt silently truncates at 72 BYTES, and Supabase hashes with bcrypt. A
// 100-character passphrase is therefore only its first 72 bytes, and - worse -
// two different passwords sharing a 72-byte prefix both authenticate. Rejecting
// above the limit is honest; silently truncating is not.
const MAX_PASSWORD_BYTES = 72;
const MIN_PASSWORD_LENGTH = 8;

/**
 * Values common enough that an online guesser tries them before anything else.
 * Short list on purpose: this is a server module loaded on every auth request,
 * not a breach corpus. The real defence against credential stuffing is the
 * per-identifier budget in authRateLimit.js; this only catches the passwords
 * that would fall to the first handful of guesses.
 */
const OBVIOUS = new Set([
  'password', 'password1', 'password123', '12345678', '123456789', '1234567890',
  'qwertyui', 'qwerty123', 'letmein', 'welcome1', 'iloveyou', 'admin123',
  'football', 'baseball', 'sunshine', 'princess', 'trustno1', 'starwars',
  'monkey123', 'abc12345', 'passw0rd', 'p@ssw0rd', 'singularity', 'changeme'
]);

/**
 * @typedef {{ok: true} | {ok: false, message: string}} PolicyVerdict
 */

/**
 * @param {unknown} password
 * @param {string} [email] the address being registered, used for the similarity check
 * @returns {PolicyVerdict}
 */
export function checkPassword(password, email = '') {
  if (typeof password !== 'string' || password.length === 0) {
    return { ok: false, message: 'Enter a password.' };
  }

  if (password.length < MIN_PASSWORD_LENGTH) {
    return { ok: false, message: `Use at least ${MIN_PASSWORD_LENGTH} characters.` };
  }

  // Byte length, not character length: one emoji is four bytes, so a password
  // that looks short can still cross the bcrypt limit.
  if (new TextEncoder().encode(password).length > MAX_PASSWORD_BYTES) {
    return {
      ok: false,
      message: 'That password is too long. Use 72 bytes or fewer (about 72 characters).'
    };
  }

  const lower = password.toLowerCase();

  if (OBVIOUS.has(lower)) {
    return { ok: false, message: 'That password is too common. Pick something else.' };
  }

  // A password that is just the address, or just the part before the @, is a
  // password an attacker types first because they already know it.
  const local = String(email).toLowerCase().split('@')[0];
  if (local.length >= 3 && (lower === local || lower === String(email).toLowerCase())) {
    return { ok: false, message: 'Your password cannot be your email address.' };
  }

  // A single repeated character passes a length check and nothing else.
  if (/^(.)\1+$/.test(password)) {
    return { ok: false, message: 'That password is too simple. Pick something else.' };
  }

  return { ok: true };
}

/**
 * The strength score the meter renders: 0 Weak, 1 Fair, 2 Good, 3 Strong.
 *
 * Kept identical to the client-side `score()` in the signup page so the meter
 * cannot disagree with the server about what "Strong" means. This is advisory
 * only - `checkPassword()` decides what is accepted, and a "Weak" password
 * that clears the policy is still accepted, exactly as the UI implies.
 *
 * @param {string} v
 * @returns {0|1|2|3}
 */
export function strengthScore(v) {
  if (typeof v !== 'string') return 0;
  let s = 0;
  if (v.length >= 8) s++;
  if (v.length >= 14) s++;
  if (/[0-9]/.test(v) && /[a-zA-Z]/.test(v)) s++;
  if (/[^a-zA-Z0-9]/.test(v)) s++;
  return /** @type {0|1|2|3} */ (Math.max(0, Math.min(3, s - 1)));
}

/** The field hint the form renders. Single source for the advertised floor. */
export function strengthHint() {
  return `${MIN_PASSWORD_LENGTH} characters minimum`;
}

export { MIN_PASSWORD_LENGTH, MAX_PASSWORD_BYTES };
