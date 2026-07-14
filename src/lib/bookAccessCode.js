// The book-page unlock code. Deliberately a plain client-visible constant,
// not a server secret: the gate is a friction speed-bump for paying
// customers, not a real access control. CT's call - if someone reads it out
// of the bundle and unlocks the draft for free, that's fine.
export const BOOK_ACCESS_PASSWORD = 'SHOUSE2026';
export const BOOK_ACCESS_STORAGE_KEY = 'sts_book_access';
