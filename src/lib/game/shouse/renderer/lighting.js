import * as THREE from 'three';

// Day/night lighting cycle keyed to the sim's day timer.
// Day occupies ~75% of the cycle, night ~25%. Night keeps a visible
// moonlit floor so the scene never goes black.

const DAY_END = 0.75; // fraction of the cycle that is daylight

const PHASES = [
	{ t: 0.0, sun: 0.9, hemi: 0.55, color: new THREE.Color(0xf59e0b) }, // dawn
	{ t: 0.08, sun: 1.6, hemi: 0.95, color: new THREE.Color(0xfff3df) }, // morning
	{ t: 0.45, sun: 1.8, hemi: 1.1, color: new THREE.Color(0xffffff) }, // noon
	{ t: 0.68, sun: 1.55, hemi: 0.95, color: new THREE.Color(0xffe8c4) }, // afternoon
	{ t: DAY_END, sun: 0.9, hemi: 0.55, color: new THREE.Color(0xf59e0b) }, // dusk
	{ t: 0.83, sun: 0.5, hemi: 0.5, color: new THREE.Color(0x7d9cc4) }, // moonlit night
	{ t: 0.94, sun: 0.48, hemi: 0.48, color: new THREE.Color(0x7d9cc4) }, // deep night
	{ t: 1.0, sun: 0.9, hemi: 0.55, color: new THREE.Color(0xf59e0b) } // wrap to dawn
];

export function createLighting(scene, { shadows = true } = {}) {
	const hemi = new THREE.HemisphereLight(0x9fc2ff, 0x4a3a26, 0.6);
	scene.add(hemi);

	const sun = new THREE.DirectionalLight(0xffffff, 1.2);
	sun.position.set(30, 40, 10);
	if (shadows) {
		sun.castShadow = true;
		sun.shadow.mapSize.set(1024, 1024);
		sun.shadow.camera.left = -28;
		sun.shadow.camera.right = 28;
		sun.shadow.camera.top = 28;
		sun.shadow.camera.bottom = -28;
		sun.shadow.camera.far = 120;
		sun.shadow.bias = -0.002;
	}
	scene.add(sun);
	scene.add(sun.target);

	// Ambient floor: keeps the scene readable even at deep night
	const fill = new THREE.AmbientLight(0x44567d, 0.7);
	scene.add(fill);

	const tmpColor = new THREE.Color();

	// phase: 0..1 through the in-game day
	function update(phase) {
		let a = PHASES[0];
		let b = PHASES[PHASES.length - 1];
		for (let i = 0; i < PHASES.length - 1; i++) {
			if (phase >= PHASES[i].t && phase <= PHASES[i + 1].t) {
				a = PHASES[i];
				b = PHASES[i + 1];
				break;
			}
		}
		const span = b.t - a.t || 1;
		const f = (phase - a.t) / span;

		sun.intensity = a.sun + (b.sun - a.sun) * f;
		hemi.intensity = a.hemi + (b.hemi - a.hemi) * f;
		tmpColor.copy(a.color).lerp(b.color, f);
		sun.color.copy(tmpColor);

		// Sun arcs east -> west across the daylight portion; hangs low as a
		// "moon" through the night so shadows never vanish entirely.
		const dayT = Math.min(1, phase / DAY_END);
		const angle = Math.PI * dayT;
		sun.position.set(Math.cos(angle) * 45, Math.max(8, Math.sin(angle) * 45), 14);

		return { isNight: sun.intensity < 0.7 };
	}

	return { update, sun, hemi };
}
