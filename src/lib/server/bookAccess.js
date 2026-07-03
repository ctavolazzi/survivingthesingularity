import { env } from '$env/dynamic/private';

export const BOOK_ACCESS_COOKIE = 'sts_book_access';

// Single shared password mailed to every paying customer (not a per-user
// secret), so a plain comparison is fine — constant-time comparison matters
// for distinguishing valid vs invalid user accounts, not a shared word.
// Fails closed (false) when unset so a misconfigured deploy never opens the gate.
export function verifyBookPassword(input) {
  const expected = env.BOOK_ACCESS_PASSWORD;
  if (!expected) {
    console.warn('[book-access] BOOK_ACCESS_PASSWORD unset — gate cannot be unlocked.');
    return false;
  }
  return typeof input === 'string' && input === expected;
}
