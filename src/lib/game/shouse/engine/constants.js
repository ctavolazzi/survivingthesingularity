// Shouse Builder — core simulation constants.
// Sim cadence and difficulty model adapted from Johnny Autoseed's
// homestead-engine (johnnyautoseed.com/game).

export const DAY_FRAMES = 1200; // ~20s per day at 60fps, 1x speed

export const WATER_CAP = 100;
export const POWER_CAP = 100;

export const DIFFICULTIES = {
	homesteader: {
		label: 'Homesteader',
		desc: 'Long season, calm weather. Learn the build.',
		maxDay: 60,
		eventChance: 0.15,
		drainMult: 0.8,
		stressFrames: 450,
		startCash: 25000,
		startWater: 80,
		startPower: 60
	},
	builder: {
		label: 'Builder',
		desc: 'The real $25k sprint. 45 days.',
		maxDay: 45,
		eventChance: 0.25,
		drainMult: 1.0,
		stressFrames: 300,
		startCash: 25000,
		startWater: 70,
		startPower: 50
	},
	scavenger: {
		label: 'Scavenger',
		desc: 'Short season, thin budget, rough weather.',
		maxDay: 38,
		eventChance: 0.35,
		drainMult: 1.2,
		stressFrames: 200,
		startCash: 23000,
		startWater: 60,
		startPower: 45
	}
};

// Manual actions (cooldowns in frames)
export const ACTIONS = {
	haulWater: { gain: 30, cooldown: 480, cost: 0 },
	runGenerator: { gain: 35, cooldown: 360, cost: 40 }
};

// Resources must be at least this high to start a build (stages that need utilities)
export const BUILD_RESOURCE_MIN = 25;

export const STORAGE_KEY = 'sts-shouse-builder';
