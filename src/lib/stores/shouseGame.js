import { writable } from 'svelte/store';

// UI-facing snapshot of the Shouse Builder sim. The Three.js renderer reads
// game.getState() directly each frame; this store only carries the throttled
// snapshots the HUD and menus need.
function createShouseGameStore() {
	const { subscribe, set } = writable(null);

	return {
		subscribe,
		sync(state) {
			set({
				day: state.day,
				dayTimer: state.dayTimer,
				maxDay: state.maxDay,
				paused: state.paused,
				speed: state.speed,
				cash: Math.round(state.cash),
				water: Math.round(state.water),
				power: Math.round(state.power),
				waterCap: state.waterCap,
				powerCap: state.powerCap,
				stage: state.stage,
				building: state.building ? { ...state.building } : null,
				buildLockUntilDay: state.buildLockUntilDay,
				discountNext: state.discountNext,
				upgrades: [...state.upgrades],
				pendingUpgrade: state.pendingUpgrade,
				shakedownDays: state.shakedownDays,
				activeEvents: state.activeEvents.map((e) => ({ ...e })),
				forecast: state.forecast.map((f) => ({ ...f })),
				eventsTriggered: state.eventsTriggered,
				haulCd: state.haulCd,
				generatorCd: state.generatorCd,
				haulUses: state.haulUses,
				generatorUses: state.generatorUses,
				cropPreset: state.cropPreset,
				harvests: state.harvests,
				produceEarned: state.produceEarned,
				stressFrames: state.stressFrames,
				stressLimit: state.stressLimit,
				won: state.won,
				lost: state.lost,
				loseReason: state.loseReason,
				achievements: [...state.achievements],
				best: { ...state.best }
			});
		},
		reset() {
			set(null);
		}
	};
}

export const shouseGame = createShouseGameStore();
