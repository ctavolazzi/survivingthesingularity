/**
 * Turning GoTrue errors into something safe to show a visitor.
 *
 * THE RULE THIS MODULE EXISTS TO ENFORCE: DO NOT CONFIRM WHO HAS AN ACCOUNT
 *
 * The tempting messages are the leaky ones. "No account with that email" and
 * "That email is already registered" are helpful, and between them they turn
 * the login form into a membership oracle: feed it a list of addresses and the
 * responses partition it into customers and strangers. For this site that list
 * is worth having - it identifies people who bought a book about preparing for
 * technological upheaval, which is exactly the kind of inference someone might
 * want to make about a person, and it is inferable by anyone with a script.
 *
 * So both signup and signin answer identically whether or not the account
 * exists, and the code that calls this is arranged so the *timing* matches too
 * (see the signup action: it always performs the same work).
 *
 * The one place we deliberately do NOT hide state is a locked-out account,
 * because "try again in ten minutes" is information the person needs in order
 * to do anything, and it is already inferable from the 429 status.
 */

/**
 * Messages, in one place, so the same condition reads the same everywhere.
 * Sentence case, no exclamation marks, matching the copy in the signup page.
 */
export const MESSAGES = {
  // Shown for a wrong password AND for an address with no account. Identical
  // on purpose - see the header.
  badCredentials: 'That email and password do not match. Check both and try again.',

  // Shown after signup regardless of whether the address was already taken.
  // The page then renders the "check your inbox" view either way. Someone who
  // already has an account gets a real email from Supabase telling them so,
  // which routes the truth to the person who owns the address rather than to
  // whoever typed it into the form.
  signupPending: 'Check your inbox to confirm your account.',

  unconfirmed: 'Confirm your email first. Check your inbox for the link we sent.',
  rateLimited: 'Too many attempts. Wait a few minutes and try again.',
  emailRateLimited: 'We have sent several emails to that address already. Wait a few minutes.',
  invalidEmail: 'Enter a valid email address.',
  weakPassword: 'That password is too weak. Use at least 8 characters.',
  expiredLink: 'That link has expired. Request a new one.',
  usedLink: 'That link has already been used. Sign in, or request a new one.',
  oauthFailed: 'That sign-in did not complete. Try again, or use your email address.',
  providerDisabled: 'That sign-in method is not available right now. Use your email address.',
  consentRequired: 'You need to accept the Terms and the Privacy Policy to continue.',
  unavailable: 'Accounts are temporarily unavailable. Try again shortly.',
  generic: 'Something went wrong. Try again.'
};

/**
 * Map a GoTrue error onto a message and status.
 *
 * Matching is on `error.code` where Supabase provides one and on the message
 * text where it does not, because GoTrue's older errors carry only a string.
 * Anything unrecognised falls through to the generic message and is logged
 * server-side with its real text - the visitor gets nothing useful, and we do
 * not lose the diagnosis.
 *
 * @param {{code?: string, status?: number, message?: string}|null} error
 * @param {string} context short label for the log line, e.g. 'signin'
 * @returns {{message: string, status: number}}
 */
export function mapAuthError(error, context = 'auth') {
  if (!error) return { message: MESSAGES.generic, status: 400 };

  const code = error.code ?? '';
  const raw = (error.message ?? '').toLowerCase();

  // Log the truth. This is the only place the real error survives, and without
  // it every failure in production reads as "Something went wrong".
  console.error(`[auth:${context}]`, error.status ?? '', code || '(no code)', error.message ?? '');

  if (code === 'invalid_credentials' || raw.includes('invalid login credentials')) {
    return { message: MESSAGES.badCredentials, status: 400 };
  }
  if (code === 'email_not_confirmed' || raw.includes('email not confirmed')) {
    return { message: MESSAGES.unconfirmed, status: 400 };
  }
  if (code === 'over_email_send_rate_limit' || raw.includes('email rate limit')) {
    return { message: MESSAGES.emailRateLimited, status: 429 };
  }
  if (code === 'over_request_rate_limit' || error.status === 429) {
    return { message: MESSAGES.rateLimited, status: 429 };
  }
  if (code === 'weak_password' || raw.includes('password should be at least')) {
    return { message: MESSAGES.weakPassword, status: 400 };
  }
  if (code === 'validation_failed' && raw.includes('email')) {
    return { message: MESSAGES.invalidEmail, status: 400 };
  }
  if (code === 'otp_expired' || raw.includes('expired')) {
    return { message: MESSAGES.expiredLink, status: 400 };
  }
  if (code === 'provider_disabled' || raw.includes('provider is not enabled')) {
    return { message: MESSAGES.providerDisabled, status: 400 };
  }
  if (
    code === 'user_already_exists' ||
    code === 'email_exists' ||
    raw.includes('already registered')
  ) {
    // Not an error the visitor sees. The caller is expected to catch this case
    // before calling here and render the neutral pending view instead; if it
    // reaches this point, still refuse to confirm the address is taken.
    return { message: MESSAGES.signupPending, status: 200 };
  }

  return { message: MESSAGES.generic, status: 400 };
}
