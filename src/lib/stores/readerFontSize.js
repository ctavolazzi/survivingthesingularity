import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Text size for the continuous reader. Persisted, because someone who needs
// larger text needs it every session, not just this one.

const STORAGE_KEY = 'sts:reader-font-size:v1';
const SIZES = ['small', 'medium', 'large', 'xlarge'];
const DEFAULT = 'medium';

function read() {
  if (!browser) return DEFAULT;
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return SIZES.includes(stored) ? stored : DEFAULT;
  } catch {
    return DEFAULT;
  }
}

function createReaderFontSize() {
  const { subscribe, set } = writable(read());

  function commit(next) {
    if (browser) {
      try { localStorage.setItem(STORAGE_KEY, next); } catch { /* private mode */ }
    }
    set(next);
  }

  function step(delta) {
    // Read through the store rather than tracking a local copy, so this stays
    // correct if the value is ever set from somewhere else.
    let current = DEFAULT;
    subscribe((v) => (current = v))();
    const index = SIZES.indexOf(current);
    const next = SIZES[Math.min(SIZES.length - 1, Math.max(0, index + delta))];
    if (next && next !== current) commit(next);
  }

  return {
    subscribe,
    increase: () => step(1),
    decrease: () => step(-1),
    reset: () => commit(DEFAULT)
  };
}

export const readerFontSize = createReaderFontSize();
