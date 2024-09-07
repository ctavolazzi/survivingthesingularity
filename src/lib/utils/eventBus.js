import { writable } from 'svelte/store';

function createEventBus() {
    const { subscribe, set } = writable(null);

    return {
        subscribe,
        emit: (event, data) => set({ event, data }),
        reset: () => set(null)
    };
}

export const eventBus = createEventBus();