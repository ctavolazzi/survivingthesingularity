import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';

const STORAGE_KEY = 'sts-blueprint-progress';

function loadProgress() {
	if (!browser) return {};
	try {
		const stored = localStorage.getItem(STORAGE_KEY);
		return stored ? JSON.parse(stored) : {};
	} catch {
		return {};
	}
}

function createProgressStore() {
	const store = writable(loadProgress());

	if (browser) {
		store.subscribe((value) => {
			try {
				localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
			} catch {}
		});
	}

	return {
		subscribe: store.subscribe,
		markRead(slug) {
			store.update((progress) => {
				if (progress[slug]) return progress;
				return { ...progress, [slug]: { readAt: new Date().toISOString(), scrollPercent: 100 } };
			});
		},
		updateScroll(slug, percent) {
			store.update((progress) => {
				const existing = progress[slug];
				if (existing?.readAt) return progress; // Already fully read
				return { ...progress, [slug]: { ...existing, scrollPercent: Math.max(existing?.scrollPercent || 0, percent) } };
			});
		},
		isRead(slug) {
			return !!get(store)[slug]?.readAt;
		},
		getAll() {
			return get(store);
		},
		getCompletedCount() {
			const data = get(store);
			return Object.values(data).filter((v) => v.readAt).length;
		},
		reset() {
			store.set({});
		}
	};
}

export const blueprintProgress = createProgressStore();
