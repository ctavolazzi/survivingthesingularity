import { writable } from 'svelte/store';

// Whether the reader has cleared a book password this page load.
//
// Deliberately in-memory only, never persisted to storage: the unlock is meant
// to reset on any full page load (refresh, closed-and-reopened tab, new tab),
// which is how the /book gate has always behaved. Lifting it out of the /book
// layout into a store just means a client-side navigation carries the unlock
// with it, so someone who typed the code on /exclusive-friends-only lands in
// the reader without a second gate.
export const bookUnlocked = writable(false);
