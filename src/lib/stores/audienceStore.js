import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const AUDIENCES = {
	individual: {
		key: 'individual',
		label: 'Individual',
		short: 'Individual',
		icon: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
	},
	policy: {
		key: 'policy',
		label: 'Civic Planner',
		short: 'Civic',
		icon: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
	},
	leader: {
		key: 'leader',
		label: 'Decision Maker',
		short: 'Decision',
		icon: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="7" width="6" height="14"/><rect x="9" y="2" width="6" height="19"/><rect x="16" y="11" width="6" height="10"/></svg>`,
	},
};

const STORAGE_KEY = 'sts_audience';

function createAudienceStore() {
	const initial = browser
		? (localStorage.getItem(STORAGE_KEY) ?? 'individual')
		: 'individual';

	const { subscribe, set } = writable(
		Object.keys(AUDIENCES).includes(initial) ? initial : 'individual'
	);

	return {
		subscribe,
		set(value) {
			if (browser) localStorage.setItem(STORAGE_KEY, value);
			set(value);
		},
	};
}

export const audience = createAudienceStore();
