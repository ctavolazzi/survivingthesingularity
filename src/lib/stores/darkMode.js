import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function createDarkModeStore() {
    const initialValue = browser && localStorage.getItem('darkMode') === 'true';
    const { subscribe, set, update } = writable(initialValue);

    return {
        subscribe,
        toggle: () => update(n => {
            const newValue = !n;
            if (browser) {
                localStorage.setItem('darkMode', newValue);
                document.documentElement.classList.toggle('dark', newValue);
            }
            return newValue;
        }),
        set: (value) => {
            set(value);
            if (browser) {
                localStorage.setItem('darkMode', value);
                document.documentElement.classList.toggle('dark', value);
            }
        }
    };
}

export const darkMode = createDarkModeStore();