import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const STORAGE_KEY = 'sts_book_last_read';

function readStoredSection() {
  if (!browser) return null;
  return localStorage.getItem(STORAGE_KEY);
}

function createBookPageStore() {
  const { subscribe, set, update } = writable({
    currentSectionId: null,
    lastVisitedSectionId: readStoredSection(),
  });

  return {
    subscribe,
    setCurrentSection: (sectionId) => update(state => ({ ...state, currentSectionId: sectionId })),
    // Persists to localStorage so "continue reading" survives a reload or a
    // return visit days later, not just in-memory navigation.
    updateLastVisited: () => update(state => {
      if (browser && state.currentSectionId) {
        localStorage.setItem(STORAGE_KEY, state.currentSectionId);
      }
      return { ...state, lastVisitedSectionId: state.currentSectionId };
    }),
    reset: () => {
      if (browser) localStorage.removeItem(STORAGE_KEY);
      set({ currentSectionId: null, lastVisitedSectionId: null });
    },
  };
}

export const bookPage = createBookPageStore();
