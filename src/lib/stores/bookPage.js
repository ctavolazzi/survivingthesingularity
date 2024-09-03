import { writable } from 'svelte/store';

function createBookPageStore() {
  const { subscribe, set, update } = writable({
    currentSectionId: null,
    lastVisitedSectionId: null,
  });

  return {
    subscribe,
    setCurrentSection: (sectionId) => update(state => ({ ...state, currentSectionId: sectionId })),
    updateLastVisited: () => update(state => ({ ...state, lastVisitedSectionId: state.currentSectionId })),
    reset: () => set({ currentSectionId: null, lastVisitedSectionId: null }),
  };
}

export const bookPage = createBookPageStore();