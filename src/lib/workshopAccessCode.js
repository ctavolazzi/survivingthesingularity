// The workshop dashboard unlock code.
//
// Same shape and same honest limits as $lib/bookAccessCode.js: this is a
// client-visible constant, not a server secret. Anyone who reads the JS bundle
// can find it. It is a friction speed-bump that keeps the work-in-progress
// dashboard out of search results and off casual view, NOT access control.
//
// That is an acceptable trade for what the dashboard shows (build stats,
// commit subjects, devlog essays) and an unacceptable one for anything private.
// If the dashboard ever carries something that genuinely must not leak, this
// has to move to a server-side check in hooks.server.js with the code in an
// environment variable, and this comment should be deleted along with the file.

export const WORKSHOP_ACCESS_PASSWORD = 'glass-box-2026';

/**
 * Case-insensitive, whitespace-tolerant. People retype these from a text
 * message, so a stray space or a capital should not read as "wrong password".
 * @param {string} input
 * @returns {boolean}
 */
export function isValidWorkshopPassword(input) {
  return String(input ?? '').trim().toLowerCase() === WORKSHOP_ACCESS_PASSWORD.toLowerCase();
}
