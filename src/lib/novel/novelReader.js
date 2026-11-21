import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Reader settings and place for /novel, kept in this browser only. Neither is
// a secret. The unlock itself is not stored: it is the shared in-memory
// bookUnlocked store, so it resets on a full page load like /book does.

const PREFS_KEY = 'sts:novel-prefs:v1';
const PLACE_KEY = 'sts:novel-place:v1';

export const FONT_SIZES = [16, 18, 20, 22, 24];

function readJson(key) {
  if (!browser) return null;
  try { return JSON.parse(localStorage.getItem(key) || 'null'); } catch { return null; }
}
function writeJson(key, value) {
  if (!browser) return;
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode or full */ }
}

function createPrefs() {
  const saved = readJson(PREFS_KEY);
  const initial = {
    size: FONT_SIZES.includes(saved?.size) ? saved.size : 20,
    theme: saved?.theme === 'paper' ? 'paper' : 'night'
  };
  const store = writable(initial);
  store.subscribe((value) => writeJson(PREFS_KEY, value));
  return store;
}

export const novelPrefs = createPrefs();

/** @returns {{id: string, ratio: number} | null} */
export function readPlace() {
  const p = readJson(PLACE_KEY);
  if (!p || typeof p.id !== 'string') return null;
  return { id: p.id, ratio: Math.min(1, Math.max(0, Number(p.ratio) || 0)) };
}

/** @param {string} id @param {number} ratio */
export function savePlace(id, ratio) {
  writeJson(PLACE_KEY, { id, ratio: Math.min(1, Math.max(0, ratio || 0)) });
}
