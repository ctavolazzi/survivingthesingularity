import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const STORAGE_KEY = 'sts_reader_mode';

function readStoredValue() {
  if (!browser) return false;
  return localStorage.getItem(STORAGE_KEY) === '1';
}

function createReaderModeStore() {
  const { subscribe, update } = writable(readStoredValue());

  return {
    subscribe,
    toggle: () => update(current => {
      const next = !current;
      if (browser) localStorage.setItem(STORAGE_KEY, next ? '1' : '0');
      return next;
    }),
  };
}

export const readerMode = createReaderModeStore();
