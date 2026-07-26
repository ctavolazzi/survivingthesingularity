import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Where the reader left off in the continuous reader (/read).
//
// Persisted to localStorage, unlike the password unlock: losing your place is
// a real cost to a reader, and a position is not a secret. Stored as a section
// id plus how far into that section you were (0..1), NOT a raw pixel offset -
// pixel offsets break the moment the viewport width, font size, or the prose
// itself changes, and this book is a live draft that changes weekly.

const STORAGE_KEY = 'sts:reading-position:v1';

function read() {
  if (!browser) return null;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (typeof parsed?.sectionId !== 'string') return null;
    return {
      sectionId: parsed.sectionId,
      // Clamp on read: a corrupted or hand-edited value should degrade to
      // "top of that section" rather than scrolling somewhere impossible.
      ratio: Math.min(1, Math.max(0, Number(parsed.ratio) || 0)),
      savedAt: Number(parsed.savedAt) || 0
    };
  } catch {
    return null;
  }
}

function createReadingPosition() {
  const { subscribe, set } = writable(read());

  return {
    subscribe,

    /** Record the reader's place. Called throttled from a scroll handler. */
    save(sectionId, ratio, now) {
      if (!browser || !sectionId) return;
      const value = {
        sectionId,
        ratio: Math.min(1, Math.max(0, ratio || 0)),
        // Timestamp is passed in rather than read here so this stays a pure
        // function of its inputs and is trivial to test.
        savedAt: now ?? 0
      };
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
        set(value);
      } catch {
        // Private browsing / quota. Reading still works, the place just
        // won't survive the session. Not worth interrupting anyone over.
      }
    },

    clear() {
      if (browser) {
        try { localStorage.removeItem(STORAGE_KEY); } catch { /* see above */ }
      }
      set(null);
    }
  };
}

export const readingPosition = createReadingPosition();
