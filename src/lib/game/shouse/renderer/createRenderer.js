import * as THREE from 'three';
import { COLORS } from './palette.js';
import { createCameraRig } from './camera.js';
import { createLighting } from './lighting.js';
import { createWorld } from './world.js';
import { createBuildables, STAGE_FOCUS, SCAFFOLD_BOUNDS } from './buildables.js';
import { createBuilders } from './builders.js';
import { createEffects } from './effects.js';
import { DAY_FRAMES } from '../engine/constants.js';

// Three.js bootstrap for Shouse Builder. Client-side only — this module is
// loaded via dynamic import inside onMount, never during SSR.

export function createShouseRenderer(canvas) {
	const coarsePointer =
		typeof window !== 'undefined' && window.matchMedia?.('(pointer: coarse)').matches;
	const dprCap = coarsePointer ? 1.5 : 2;

	const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
	renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, dprCap));
	renderer.shadowMap.enabled = !coarsePointer;
	renderer.shadowMap.type = THREE.PCFSoftShadowMap;

	const scene = new THREE.Scene();
	scene.background = new THREE.Color(COLORS.bg);
	scene.fog = new THREE.Fog(COLORS.bg, 55, 110);

	const rig = createCameraRig(canvas);
	const lighting = createLighting(scene, { shadows: !coarsePointer });
	const world = createWorld();
	scene.add(world);
	const buildables = createBuildables();
	scene.add(buildables.group);
	const builders = createBuilders();
	scene.add(builders.group);
	const effects = createEffects(scene);

	// dust burst + camera glide when a stage finishes building
	buildables.onStageShown = (index) => {
		const f = STAGE_FOCUS[index];
		if (f) {
			rig.focusOn(f.x, f.z);
			effects.burstAt(f.x, 1, f.z);
		}
	};

	let cutaway = false;
	let elapsed = 0;

	function render(state, dt) {
		elapsed += dt;
		rig.update();
		const phase = state ? state.dayTimer / DAY_FRAMES : 0.4;
		const { isNight } = lighting.update(phase);
		if (state) {
			buildables.update(state, dt, elapsed, isNight);
			buildables.updatePlants(state.plants, elapsed);
			builders.update(
				state.building ? SCAFFOLD_BOUNDS[state.building.index] : null,
				state.paused ? 0 : dt,
				elapsed,
				effects.burstAt
			);
			effects.update(state, dt);
		}
		renderer.render(scene, rig.camera);
	}

	function resize(width, height) {
		renderer.setSize(width, height, false);
		rig.resize(width, height);
	}

	function setCutaway(on) {
		cutaway = on;
		buildables.setCutaway(on);
	}

	function toggleCutaway() {
		setCutaway(!cutaway);
		return cutaway;
	}

	function rotate(dir) {
		rig.rotate(dir);
	}

	function burstAt(x, y, z, color) {
		effects.burstAt(x, y, z, color);
	}

	function dispose() {
		rig.dispose();
		effects.dispose();
		scene.traverse((obj) => {
			if (obj.geometry) obj.geometry.dispose();
			if (obj.material) {
				const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
				for (const m of mats) m.dispose();
			}
		});
		renderer.dispose();
	}

	return { render, resize, setCutaway, toggleCutaway, rotate, burstAt, dispose };
}
