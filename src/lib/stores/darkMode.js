import { readable } from 'svelte/store';

// Use a readable store with a constant value of true to ensure dark mode is always active
const darkMode = readable(true);

export { darkMode };