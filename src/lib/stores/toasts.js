import { writable } from 'svelte/store';

function createToastStore() {
	const { subscribe, update } = writable([]);
	let id = 0;

	return {
		subscribe,
		add(message, type = 'info', duration = 4000) {
			const toast = { id: ++id, message, type, duration };
			update((all) => [...all, toast]);
			if (duration > 0) {
				setTimeout(() => {
					update((all) => all.filter((t) => t.id !== toast.id));
				}, duration);
			}
			return toast.id;
		},
		success(message, duration = 4000) {
			return this.add(message, 'success', duration);
		},
		error(message, duration = 5000) {
			return this.add(message, 'error', duration);
		},
		info(message, duration = 4000) {
			return this.add(message, 'info', duration);
		},
		dismiss(toastId) {
			update((all) => all.filter((t) => t.id !== toastId));
		},
		clear() {
			update(() => []);
		}
	};
}

export const toasts = createToastStore();
