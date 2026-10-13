import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const STORAGE_KEY = 'sts_reader_mode';

function readStoredValue() {
  if (!browser) return false;
  try { return localStorage.getItem(STORAGE_KEY) === '1'; } catch { return false; }
}

function createReaderModeStore() {
  const { subscribe, update } = writable(readStoredValue());

  return {
    subscribe,
    toggle: () => update(current => {
      const next = !current;
      if (browser) {
        try { localStorage.setItem(STORAGE_KEY, next ? '1' : '0'); } catch { /* Keep the current session usable. */ }
      }
      return next;
    }),
  };
}

export const readerMode = createReaderModeStore();
