import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const STORAGE_KEY = 'sts_book_last_read';

function readStoredSection() {
  if (!browser) return null;
  try { return localStorage.getItem(STORAGE_KEY); } catch { return null; }
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
        try { localStorage.setItem(STORAGE_KEY, state.currentSectionId); } catch { /* Reading still works without persistence. */ }
      }
      return { ...state, lastVisitedSectionId: state.currentSectionId };
    }),
    reset: () => {
      if (browser) {
        try { localStorage.removeItem(STORAGE_KEY); } catch { /* Storage may be blocked. */ }
      }
      set({ currentSectionId: null, lastVisitedSectionId: null });
    },
  };
}

export const bookPage = createBookPageStore();
