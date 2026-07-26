// The book-page unlock codes. Deliberately plain client-visible constants,
// not server secrets: the gate is a friction speed-bump for paying
// customers, not a real access control. CT's call - if someone reads it out
// of the bundle and unlocks the draft for free, that's fine.

// The code that ships in the preorder confirmation email.
export const BOOK_ACCESS_PASSWORD = 'SHOUSE2026';

// The code handed out personally for /exclusive-friends-only. Same access,
// different door: it opens the friends page AND the book reader, so a friend
// never has to type a second password to get from one to the other.
export const FRIENDS_ACCESS_PASSWORD = 'bring-it-on-2027';

// Every code that unlocks the book reader.
const ACCEPTED = [BOOK_ACCESS_PASSWORD, FRIENDS_ACCESS_PASSWORD];

/**
 * Case-insensitive, whitespace-tolerant password check. People retype these
 * from an email or a text message, so a stray space or a capitalized first
 * letter shouldn't read as "wrong password".
 * @param {string} input
 * @returns {boolean}
 */
export function isValidBookPassword(input) {
  const normalized = String(input ?? '').trim().toLowerCase();
  return ACCEPTED.some((code) => code.toLowerCase() === normalized);
}

/**
 * The friends-only code specifically. /exclusive-friends-only uses this so the
 * preorder code doesn't quietly double as a friends code.
 * @param {string} input
 * @returns {boolean}
 */
export function isValidFriendsPassword(input) {
  return String(input ?? '').trim().toLowerCase() === FRIENDS_ACCESS_PASSWORD.toLowerCase();
}
