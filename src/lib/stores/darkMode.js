import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const darkMode = writable(true);

export { darkMode };