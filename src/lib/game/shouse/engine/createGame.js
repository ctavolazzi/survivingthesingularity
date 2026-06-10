// Shouse Builder simulation core. Framework-agnostic: no DOM, no Three.js,
// no Svelte. The UI subscribes for discrete happenings; the renderer reads
// getState() directly every frame.
//
// Sim cadence, event discipline, and scoring shape adapted from Johnny
// Autoseed's homestead-engine (Autoseed Tycoon).

import { DAY_FRAMES, WATER_CAP, POWER_CAP, DIFFICULTIES, ACTIONS, BUILD_RESOURCE_MIN, STORAGE_KEY } from './constants.js';
import { STAGES } from './stages.js';
import { EVENTS, generateForecast } from './events.js';
import { getUpgradeTier } from './upgrades.js';
import { ACHIEVEMENT_DEFS } from './achievements.js';
import { computeScore, computeGrade } from './scoring.js';
import { getCropPreset } from '../data/plants.js';

// Days the finished shouse must run stable after the last build to win.
const SHAKEDOWN_DAYS = 3;

function loadBest() {
	try {
		if (typeof localStorage === 'undefined') return { bestScore: 0, bestGrade: '', gamesPlayed: 0 };
		const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
		return {
			bestScore: data.bestScore || 0,
			bestGrade: data.bestGrade || '',
			gamesPlayed: data.gamesPlayed || 0
		};
	} catch {
		return { bestScore: 0, bestGrade: '', gamesPlayed: 0 };
	}
}

export function createShouseGame({ difficulty = 'builder' } = {}) {
	const preset = DIFFICULTIES[difficulty] || DIFFICULTIES.builder;
	const listeners = new Set();

	const state = {
		difficulty,
		difficultyLabel: preset.label,
		// clock
		day: 1,
		dayTimer: 0,
		maxDay: preset.maxDay,
		paused: false,
		speed: 1,
		frame: 0,
		// resources
		cash: preset.startCash,
		water: preset.startWater,
		power: preset.startPower,
		waterCap: WATER_CAP,
		powerCap: POWER_CAP,
		// build progress: number of completed stages (0..6)
		stage: 0,
		// active construction: { index, id, daysLeft, totalDays } or null
		building: null,
		buildLockUntilDay: 0,
		discountNext: 0,
		upgrades: [],
		pendingUpgrade: null,
		// shakedown: days survived after final stage
		shakedownDays: 0,
		// events
		activeEvents: [],
		forecast: generateForecast(1, preset.maxDay),
		lastEventDay: 0,
		eventsTriggered: 0,
		// actions / cooldowns (frames)
		haulCd: 0,
		generatorCd: 0,
		haulUses: 0,
		generatorUses: 0,
		// farmbot
		cropPreset: 'greens',
		plants: [],
		harvests: 0,
		produceEarned: 0,
		// stress / fail
		stressFrames: 0,
		stressLimit: preset.stressFrames,
		peakStress: 0,
		// outcome
		won: false,
		lost: false,
		loseReason: null,
		// meta
		achievements: [],
		moneySpent: 0,
		best: loadBest()
	};

	function notify(evt) {
		for (const fn of listeners) fn(evt, state);
	}

	function hasUpgrade(id) {
		return state.upgrades.includes(id);
	}

	function hasActiveEffect(effect) {
		return state.activeEvents.some((e) => e.effect === effect);
	}

	function saveBest() {
		const score = computeScore(state);
		const grade = computeGrade(score);
		state.best.gamesPlayed++;
		if (score > state.best.bestScore) {
			state.best.bestScore = score;
			state.best.bestGrade = grade;
		}
		try {
			if (typeof localStorage !== 'undefined') {
				localStorage.setItem(STORAGE_KEY, JSON.stringify(state.best));
			}
		} catch {
			/* private mode etc. */
		}
	}

	function checkAchievements() {
		for (const def of ACHIEVEMENT_DEFS) {
			if (state.achievements.includes(def.id)) continue;
			try {
				if (def.check(state)) {
					state.achievements.push(def.id);
					notify({ type: 'achievement', achievement: def });
				}
			} catch {
				/* defensive: a bad check must not kill the loop */
			}
		}
	}

	function applyInstant(values) {
		if (!values) return;
		if (values.water) state.water = Math.max(0, Math.min(state.waterCap, state.water + values.water));
		if (values.power) state.power = Math.max(0, Math.min(state.powerCap, state.power + values.power));
		if (values.cash) state.cash = Math.max(0, state.cash + values.cash);
	}

	function rollEvent() {
		if (state.day < 5 || state.day - state.lastEventDay < 3) return;
		if (Math.random() > (DIFFICULTIES[state.difficulty] || DIFFICULTIES.builder).eventChance) return;
		const pool = EVENTS.filter((ev) => {
			if (state.activeEvents.some((a) => a.id === ev.id)) return false;
			if (ev.minStage !== undefined && state.stage < ev.minStage) return false;
			if (ev.maxStage !== undefined && state.stage > ev.maxStage) return false;
			return true;
		});
		if (pool.length === 0) return;
		const chosen = pool[Math.floor(Math.random() * pool.length)];
		state.lastEventDay = state.day;
		state.eventsTriggered++;

		applyInstant(chosen.instant);
		if (chosen.effect === 'wind_damage' && state.stage < 2) {
			state.cash = Math.max(0, state.cash - 200);
		}
		if (chosen.effect === 'discount_next') {
			state.discountNext = 0.15;
		}
		if (chosen.effect === 'build_lock') {
			state.buildLockUntilDay = Math.max(state.buildLockUntilDay, state.day + chosen.duration);
		}
		if (chosen.duration > 0) {
			state.activeEvents.push({
				id: chosen.id,
				name: chosen.name,
				icon: chosen.icon,
				effect: chosen.effect,
				endsOnDay: state.day + chosen.duration
			});
		}
		notify({ type: 'event', event: chosen });
	}

	function expireEvents() {
		state.activeEvents = state.activeEvents.filter((e) => e.endsOnDay > state.day);
	}

	function growPlants() {
		if (state.plants.length === 0) return;
		const growthMult = 1;
		for (const p of state.plants) {
			p.growth += growthMult / p.gameDays;
			if (p.growth >= 1) {
				p.growth = 0;
				state.harvests++;
				state.cash += p.salePrice;
				state.produceEarned += p.salePrice;
				p.justHarvested = state.frame; // renderer reads this for the pop effect
				notify({ type: 'harvest', plant: p });
			}
		}
	}

	function dailyIncome() {
		let income = 0;
		for (let i = 0; i < state.stage; i++) {
			const st = STAGES[i];
			let perDay = st.incomePerDay || 0;
			if (st.id === 'crucible') {
				if (hasUpgrade('sponsor_pipeline')) perDay *= 1.4;
				if (hasActiveEffect('gpu_market')) perDay += 60;
			}
			income += perDay;
		}
		return Math.round(income);
	}

	function applyDayTick() {
		state.day++;
		state.forecast = generateForecast(state.day, state.maxDay);
		const diffPreset = DIFFICULTIES[state.difficulty] || DIFFICULTIES.builder;

		// Drains from every built stage
		let waterDrain = 0;
		let powerDrain = 0;
		for (let i = 0; i < state.stage; i++) {
			const st = STAGES[i];
			let w = st.waterDrain || 0;
			let p = st.powerDrain || 0;
			if (st.id === 'living' && hasUpgrade('wood_stove')) p *= 0.5;
			if (st.id === 'crucible' && hasUpgrade('quantized_models')) p *= 0.6;
			waterDrain += w;
			powerDrain += p;
		}
		waterDrain *= diffPreset.drainMult;
		powerDrain *= diffPreset.drainMult;
		if (hasUpgrade('pex_manifold')) waterDrain *= 0.7;
		if (hasUpgrade('pro_conduit')) powerDrain *= 0.75;
		if (hasActiveEffect('water_drain_2x')) waterDrain *= 2;

		state.water -= waterDrain;
		state.power -= powerDrain;

		// Regen
		const solarStage = STAGES[5];
		if (state.stage >= 6) {
			let regen = solarStage.powerRegen || 0;
			if (hasUpgrade('tracking_mounts')) regen *= 1.5;
			if (hasActiveEffect('power_regen_zero')) regen = 0;
			state.power += regen;
		}
		if (hasUpgrade('rain_catchment')) state.water += 6;

		// Income
		state.cash += dailyIncome();

		// Caps + floors
		state.water = Math.max(0, Math.min(state.waterCap, state.water));
		state.power = Math.max(0, Math.min(state.powerCap, state.power));

		growPlants();
		advanceConstruction();
		rollEvent();
		expireEvents();

		// Shakedown countdown after final stage
		if (state.stage >= 6 && !state.won) {
			state.shakedownDays++;
			if (state.shakedownDays >= SHAKEDOWN_DAYS) {
				win();
			}
		}

		if (!state.won && state.day > state.maxDay) {
			lose('deadline');
		}
		notify({ type: 'day' });
	}

	function advanceConstruction() {
		if (!state.building) return;
		state.building.daysLeft--;
		if (state.building.daysLeft > 0) return;

		const builtIndex = state.building.index;
		const st = STAGES[builtIndex];
		state.building = null;
		state.stage = builtIndex + 1;

		// FarmBot bed comes alive with the final stage
		if (st.id === 'solar_farmbot') {
			const preset = getCropPreset(state.cropPreset);
			state.plants = [];
			for (let i = 0; i < 8; i++) {
				const plant = preset.plants[i % preset.plants.length];
				state.plants.push({ ...plant, slot: i, growth: 0, justHarvested: 0 });
			}
		}

		notify({ type: 'stage', stage: st, index: builtIndex });
		checkAchievements();

		// Offer the paired upgrade choice (free pick of two)
		const tier = getUpgradeTier(builtIndex);
		if (tier) {
			state.pendingUpgrade = tier;
			notify({ type: 'upgradeOffer', tier });
		}
	}

	function win() {
		if (state.won || state.lost) return;
		state.won = true;
		state.paused = true;
		checkAchievements();
		saveBest();
		notify({ type: 'win' });
	}

	function lose(reason) {
		if (state.won || state.lost) return;
		state.lost = true;
		state.loseReason = reason;
		state.paused = true;
		saveBest();
		notify({ type: 'lose', reason });
	}

	function tick() {
		if (state.won || state.lost || state.paused || state.pendingUpgrade) return;
		for (let t = 0; t < state.speed; t++) {
			state.frame++;
			state.dayTimer++;
			if (state.dayTimer >= DAY_FRAMES) {
				state.dayTimer = 0;
				applyDayTick();
				if (state.won || state.lost) return;
			}
			if (state.haulCd > 0) state.haulCd--;
			if (state.generatorCd > 0) state.generatorCd--;

			const stressed = state.stage >= 3 && (state.water <= 0 || state.power <= 0);
			if (stressed) {
				state.stressFrames++;
				state.peakStress = Math.max(state.peakStress, state.stressFrames);
				if (state.stressFrames > state.stressLimit) {
					lose('systems');
					return;
				}
			} else {
				state.stressFrames = 0;
			}
		}
		if (state.frame % 60 === 0) checkAchievements();
	}

	// ── Player actions ────────────────────────────────────────────

	function nextStageCost() {
		const st = STAGES[state.stage];
		if (!st) return 0;
		let cost = st.cost;
		if (st.id === 'crucible' && hasActiveEffect('gpu_market')) cost += 400;
		if (state.discountNext > 0) cost = Math.round(cost * (1 - state.discountNext));
		return cost;
	}

	function canBuild() {
		const st = STAGES[state.stage];
		if (!st || state.won || state.lost) return { ok: false, reason: 'done' };
		if (state.building) {
			return { ok: false, reason: `Crew busy: ${STAGES[state.building.index].shortName} (${state.building.daysLeft}d left)` };
		}
		if (state.day < state.buildLockUntilDay) {
			return { ok: false, reason: `Builds locked until day ${state.buildLockUntilDay}` };
		}
		const cost = nextStageCost();
		if (state.cash < cost) return { ok: false, reason: `Need $${cost.toLocaleString()}` };
		if (st.needsResources && (state.water < BUILD_RESOURCE_MIN || state.power < BUILD_RESOURCE_MIN)) {
			return { ok: false, reason: `Water & power must be ≥ ${BUILD_RESOURCE_MIN}` };
		}
		return { ok: true, cost };
	}

	function buildNextStage() {
		const check = canBuild();
		if (!check.ok) return check;
		const index = state.stage;
		const st = STAGES[index];
		state.cash -= check.cost;
		state.moneySpent += check.cost;
		state.discountNext = 0;
		state.building = { index, id: st.id, daysLeft: st.buildDays, totalDays: st.buildDays };
		notify({ type: 'buildStart', stage: st, index });
		return { ok: true, stage: st };
	}

	function selectUpgrade(id) {
		if (!state.pendingUpgrade) return;
		const valid = state.pendingUpgrade.options.some((o) => o.id === id);
		if (!valid) return;
		state.upgrades.push(id);
		if (id === 'lifepo4_expansion') state.powerCap = 150;
		state.pendingUpgrade = null;
		notify({ type: 'upgradeSelected', id });
	}

	function haulWater() {
		if (state.won || state.lost || state.haulCd > 0) return;
		state.water = Math.min(state.waterCap, state.water + ACTIONS.haulWater.gain);
		state.haulCd = ACTIONS.haulWater.cooldown;
		state.haulUses++;
		notify({ type: 'action', action: 'haulWater' });
	}

	function runGenerator() {
		if (state.won || state.lost || state.generatorCd > 0) return;
		if (state.cash < ACTIONS.runGenerator.cost) return;
		state.cash -= ACTIONS.runGenerator.cost;
		state.moneySpent += ACTIONS.runGenerator.cost;
		state.power = Math.min(state.powerCap, state.power + ACTIONS.runGenerator.gain);
		state.generatorCd = ACTIONS.runGenerator.cooldown;
		state.generatorUses++;
		notify({ type: 'action', action: 'runGenerator' });
	}

	function setCrop(id) {
		if (state.stage >= 6) return; // locked once the bed is planted
		state.cropPreset = id;
		notify({ type: 'crop', id });
	}

	function setSpeed(s) {
		state.speed = Math.max(1, Math.min(3, s));
		notify({ type: 'speed', speed: state.speed });
	}

	function togglePause() {
		if (state.won || state.lost) return;
		state.paused = !state.paused;
		notify({ type: 'pause', paused: state.paused });
	}

	return {
		getState: () => state,
		tick,
		buildNextStage,
		canBuild,
		nextStageCost,
		selectUpgrade,
		haulWater,
		runGenerator,
		setCrop,
		setSpeed,
		togglePause,
		subscribe(fn) {
			listeners.add(fn);
			return () => listeners.delete(fn);
		}
	};
}

export { SHAKEDOWN_DAYS };
