import * as THREE from 'three';
import { COLORS } from './palette.js';
import { createPlantBed } from './plantsMesh.js';

// Stage mesh groups for the shouse build. All primitives, no model files.
// Group index i becomes visible once state.stage > i.

// Camera glide targets per completed stage index
export const STAGE_FOCUS = [
	{ x: 0, z: -3 }, // foundation
	{ x: 0, z: -3 }, // container
	{ x: 5, z: -2 }, // utilities
	{ x: 9.5, z: -2 }, // living / RV
	{ x: -3.5, z: -3 }, // crucible
	{ x: -11, z: 8 } // solar + farmbot
];

// Construction scaffold bounds per stage index (also used by the builder crew)
export const SCAFFOLD_BOUNDS = [
	{ x: 0, y: 0.4, z: -3, w: 13.4, h: 0.8, d: 3.8 },
	{ x: 0, y: 1.95, z: -3, w: 12.6, h: 3.2, d: 3 },
	{ x: 5, y: 1.4, z: -2.2, w: 4, h: 2.8, d: 3.2 },
	{ x: 9.5, y: 1.2, z: -2.2, w: 6, h: 2.4, d: 3.4 },
	{ x: -3.5, y: 1.6, z: -3, w: 2.4, h: 3.2, d: 2.8 },
	{ x: -12, y: 1, z: 8.5, w: 11, h: 2, d: 6 }
];

function mat(color, opts = {}) {
	return new THREE.MeshStandardMaterial({ color, roughness: 0.85, ...opts });
}

function box(w, h, d, material, x = 0, y = 0, z = 0, shadow = true) {
	const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
	m.position.set(x, y, z);
	if (shadow) m.castShadow = true;
	m.receiveShadow = true;
	return m;
}

export function createBuildables() {
	const group = new THREE.Group();
	group.name = 'buildables';

	const stageGroups = [];
	const cutawayMats = [];
	const windowMats = [];
	const ledMats = [];

	// ── Stage 1: foundation ─────────────────────────────────────
	const g1 = new THREE.Group();
	g1.add(box(13.2, 0.3, 3.6, mat(COLORS.gravel), 0, 0.15, -3));
	const pierMat = mat(COLORS.pier);
	for (let i = 0; i < 6; i++) {
		const px = -5.5 + (i % 3) * 5.5;
		const pz = -3 + (i < 3 ? -1.2 : 1.2);
		const pier = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.3, 0.5, 10), pierMat);
		pier.position.set(px, 0.45, pz);
		pier.castShadow = true;
		g1.add(pier);
	}
	stageGroups.push(g1);

	// ── Stage 2: container shell ────────────────────────────────
	const g2 = new THREE.Group();
	const hullMat = mat(COLORS.container, { transparent: true });
	const roofMat = mat(COLORS.containerRoof, { transparent: true });
	cutawayMats.push(hullMat, roofMat);
	// hull walls as 5 panels so cutaway can fade them but keep the floor
	const floorMat = mat(COLORS.steelDark);
	g2.add(box(12.2, 0.12, 2.6, floorMat, 0, 0.72, -3)); // floor
	g2.add(box(12.2, 2.9, 0.1, hullMat, 0, 2.23, -4.25)); // back wall
	g2.add(box(12.2, 2.9, 0.1, hullMat, 0, 2.23, -1.75)); // front wall
	g2.add(box(0.1, 2.9, 2.6, hullMat, -6.05, 2.23, -3)); // west end
	g2.add(box(0.1, 2.9, 2.6, hullMat, 6.05, 2.23, -3)); // east end
	g2.add(box(12.3, 0.12, 2.7, roofMat, 0, 3.72, -3)); // roof
	// corrugation ribs on the front wall
	const ribMat = mat(COLORS.containerRib, { transparent: true });
	cutawayMats.push(ribMat);
	for (let i = 0; i < 14; i++) {
		g2.add(box(0.18, 2.7, 0.06, ribMat, -5.7 + i * 0.88, 2.23, -1.69, false));
	}
	// roll-up shop door (shop side of front wall)
	g2.add(box(2.8, 2.3, 0.08, mat(COLORS.doorShop), -2.5, 1.93, -1.68, false));
	// living-third windows (emissive at night)
	for (const wx of [3.4, 5.0]) {
		const wMat = new THREE.MeshStandardMaterial({
			color: 0x223044,
			emissive: COLORS.windowGlow,
			emissiveIntensity: 0
		});
		windowMats.push(wMat);
		const win = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.7, 0.08), wMat);
		win.position.set(wx, 2.5, -1.68);
		g2.add(win);
	}
	// interior, revealed by cutaway: partition, workbench, bunk, kitchenette
	const interior = new THREE.Group();
	interior.add(box(0.1, 2.8, 2.5, mat(0x2c3b52), 2.0, 2.2, -3)); // partition at 2/3
	interior.add(box(2.6, 0.5, 0.8, mat(0x6b4f2f), -4.5, 1.05, -3.8)); // workbench
	interior.add(box(1.2, 0.45, 0.9, mat(0x475569), 4.4, 1.0, -3.7)); // bunk
	interior.add(box(0.8, 0.9, 0.5, mat(0x334155), 5.6, 1.25, -3.7)); // kitchenette
	interior.visible = false;
	g2.add(interior);
	stageGroups.push(g2);

	// ── Stage 3: utilities ──────────────────────────────────────
	const g3 = new THREE.Group();
	g3.add(box(0.7, 1.0, 0.18, mat(COLORS.panelBox), 5.2, 2.1, -1.66)); // 200A panel
	// conduit run along the front wall base
	const conduitPath = new THREE.CatmullRomCurve3([
		new THREE.Vector3(5.2, 1.55, -1.64),
		new THREE.Vector3(2.0, 1.0, -1.62),
		new THREE.Vector3(-2.0, 1.0, -1.62),
		new THREE.Vector3(-5.6, 1.0, -1.64)
	]);
	const conduit = new THREE.Mesh(
		new THREE.TubeGeometry(conduitPath, 24, 0.05, 6, false),
		mat(COLORS.conduit)
	);
	g3.add(conduit);
	// water line + spigot + small pressure tank at the east end
	const spigot = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.9, 8), mat(COLORS.steel));
	spigot.position.set(6.6, 0.45, -2.2);
	g3.add(spigot);
	const tank = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 1.1, 12), mat(COLORS.tank));
	tank.position.set(7.2, 0.55, -3.2);
	tank.castShadow = true;
	g3.add(tank);
	stageGroups.push(g3);

	// ── Stage 4: living quarters (RV ramps in) ──────────────────
	const g4 = new THREE.Group();
	const rv = new THREE.Group();
	rv.add(box(5.4, 1.9, 2.3, mat(COLORS.rvBody), 0, 1.45, 0));
	rv.add(box(5.4, 0.25, 2.3, mat(COLORS.rvStripe), 0, 1.0, 0, false));
	rv.add(box(1.1, 0.8, 2.31, mat(0x1e293b), -1.6, 1.7, 0, false)); // window strip
	const wheelMat = mat(COLORS.wheel);
	for (const [wx, wz] of [[-1.8, 1.15], [1.8, 1.15], [-1.8, -1.15], [1.8, -1.15]]) {
		const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.3, 12), wheelMat);
		wheel.rotation.x = Math.PI / 2;
		wheel.position.set(wx, 0.45, wz);
		rv.add(wheel);
	}
	g4.add(rv);
	stageGroups.push(g4);
	// RV drive-in waypoints
	const RV_START = new THREE.Vector3(20, 0, 15);
	const RV_MID = new THREE.Vector3(13, 0, 4);
	const RV_DOCK = new THREE.Vector3(10.2, 0, -2.4);
	let rvT = 0;

	// ── Stage 5: the Crucible + mesh ────────────────────────────
	const g5 = new THREE.Group();
	const rack = box(1.0, 2.2, 0.9, mat(COLORS.rack), -3.5, 1.85, -3.3);
	g5.add(rack);
	// blinking LED strips on the rack face
	for (let i = 0; i < 8; i++) {
		const ledMat = new THREE.MeshStandardMaterial({
			color: 0x05140d,
			emissive: i % 3 === 0 ? COLORS.amber : COLORS.led,
			emissiveIntensity: 0.8
		});
		ledMats.push(ledMat);
		const led = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.05, 0.02), ledMat);
		led.position.set(-3.5, 0.95 + i * 0.24, -2.84);
		g5.add(led);
	}
	// roof antenna mast + mesh nodes
	const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, 2.4, 8), mat(COLORS.antenna));
	mast.position.set(-3.5, 4.95, -3);
	mast.castShadow = true;
	g5.add(mast);
	const nodeMat = new THREE.MeshStandardMaterial({
		color: 0x0f172a,
		emissive: COLORS.blue,
		emissiveIntensity: 0.7
	});
	for (let i = 0; i < 3; i++) {
		const node = new THREE.Mesh(new THREE.SphereGeometry(0.09, 8, 8), nodeMat);
		node.position.set(-3.5, 5.4 + i * 0.35, -3);
		g5.add(node);
	}
	stageGroups.push(g5);

	// ── Stage 6: solar + battery + FarmBot ──────────────────────
	const g6 = new THREE.Group();
	const panelMat = mat(COLORS.solarPanel, { roughness: 0.4, metalness: 0.3 });
	const frameMat = mat(COLORS.solarFrame);
	for (let row = 0; row < 2; row++) {
		for (let col = 0; col < 4; col++) {
			const px = -17 + col * 2.6;
			const pz = 7 + row * 3.2;
			const panel = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.08, 1.5), panelMat);
			panel.position.set(px, 1.15, pz);
			panel.rotation.x = -0.42;
			panel.castShadow = true;
			g6.add(panel);
			const leg = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.9, 0.12), frameMat);
			leg.position.set(px, 0.45, pz + 0.3);
			g6.add(leg);
		}
	}
	// battery cabinet against the container's west end
	g6.add(box(1.1, 1.3, 0.7, mat(COLORS.battery), -7.2, 0.65, -1.2));
	// FarmBot raised bed + rails + gantry
	const bed = new THREE.Group();
	bed.position.set(10, 0, 8);
	bed.add(box(3.2, 0.55, 1.8, mat(COLORS.bedFrame), 0, 0.28, 0));
	bed.add(box(2.9, 0.1, 1.5, mat(COLORS.bedSoil), 0, 0.58, 0, false));
	const railMat = mat(COLORS.rail);
	bed.add(box(3.3, 0.08, 0.08, railMat, 0, 0.95, -0.85, false));
	bed.add(box(3.3, 0.08, 0.08, railMat, 0, 0.95, 0.85, false));
	for (const [lx, lz] of [[-1.55, -0.85], [1.55, -0.85], [-1.55, 0.85], [1.55, 0.85]]) {
		bed.add(box(0.08, 0.4, 0.08, railMat, lx, 0.75, lz, false));
	}
	const gantry = new THREE.Group();
	const beamMat = mat(COLORS.gantry);
	gantry.add(box(0.1, 0.1, 1.9, beamMat, 0, 1.05, 0, false));
	gantry.add(box(0.08, 0.5, 0.08, beamMat, 0, 0.78, -0.88, false));
	gantry.add(box(0.08, 0.5, 0.08, beamMat, 0, 0.78, 0.88, false));
	const zColumn = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.6, 0.07), beamMat);
	zColumn.position.set(0, 0.85, 0);
	gantry.add(zColumn);
	bed.add(gantry);
	g6.add(bed);
	// plant bed slots
	const plantBed = createPlantBed();
	plantBed.group.position.set(10, 0.62, 8);
	g6.add(plantBed.group);
	stageGroups.push(g6);

	for (const sg of stageGroups) {
		sg.visible = false;
		group.add(sg);
	}

	// ── Construction scaffold (ghost box while building) ────────
	const scaffoldMat = new THREE.MeshBasicMaterial({
		color: COLORS.scaffold,
		wireframe: true,
		transparent: true,
		opacity: 0.3
	});
	const scaffold = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), scaffoldMat);
	scaffold.visible = false;
	group.add(scaffold);

	// ── Animation state ─────────────────────────────────────────
	let shownStage = 0;
	const popAnims = [];
	let gantryT = 0;
	let gantryDir = 1;
	let dipT = 0;
	let onStageShown = null;

	function easeOutBack(t) {
		const c1 = 1.70158;
		const c3 = c1 + 1;
		return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
	}

	function update(state, dt, time, isNight) {
		// reveal newly completed stages with a pop-in
		while (shownStage < state.stage && shownStage < stageGroups.length) {
			const sg = stageGroups[shownStage];
			sg.visible = true;
			sg.scale.set(1, 0.01, 1);
			popAnims.push({ group: sg, t: 0 });
			if (onStageShown) onStageShown(shownStage);
			shownStage++;
		}
		for (let i = popAnims.length - 1; i >= 0; i--) {
			const a = popAnims[i];
			a.t += dt / 0.6;
			if (a.t >= 1) {
				a.group.scale.set(1, 1, 1);
				popAnims.splice(i, 1);
			} else {
				a.group.scale.y = Math.max(0.01, easeOutBack(a.t));
			}
		}

		// scaffold ghost while construction runs
		if (state.building) {
			const b = SCAFFOLD_BOUNDS[state.building.index];
			scaffold.visible = true;
			scaffold.position.set(b.x, b.y, b.z);
			scaffold.scale.set(b.w, b.h, b.d);
			scaffoldMat.opacity = 0.18 + 0.14 * Math.sin(time * 4);
		} else {
			scaffold.visible = false;
		}

		// RV drives in after living quarters complete
		if (state.stage >= 4 && rvT < 1) {
			rvT = Math.min(1, rvT + dt / 3.5);
			const t = rvT;
			const p =
				t < 0.5
					? RV_START.clone().lerp(RV_MID, t * 2)
					: RV_MID.clone().lerp(RV_DOCK, (t - 0.5) * 2);
			rv.position.copy(p);
			const ahead = t < 0.5 ? RV_MID : RV_DOCK;
			rv.lookAt(ahead.x, 0, ahead.z);
		}

		// window glow at night once living quarters exist
		const glow = isNight && state.stage >= 4 ? 0.9 : 0;
		for (const wm of windowMats) {
			wm.emissiveIntensity += (glow - wm.emissiveIntensity) * 0.05;
		}

		// rack LEDs blink with power
		if (state.stage >= 5) {
			const alive = state.power > 0;
			ledMats.forEach((lm, i) => {
				lm.emissiveIntensity = alive ? 0.4 + 0.6 * ((Math.sin(time * (2 + i * 0.7)) + 1) / 2) : 0.05;
			});
		}

		// FarmBot gantry patrol + Z-dip
		if (state.stage >= 6) {
			gantryT += dt * 0.12 * gantryDir;
			if (gantryT > 1) {
				gantryT = 1;
				gantryDir = -1;
				dipT = 1;
			} else if (gantryT < 0) {
				gantryT = 0;
				gantryDir = 1;
				dipT = 1;
			}
			gantry.position.x = -1.3 + gantryT * 2.6;
			if (dipT > 0) {
				dipT = Math.max(0, dipT - dt * 1.5);
				zColumn.position.y = 0.85 - Math.sin(dipT * Math.PI) * 0.3;
			}
		}

		// cutaway interior visibility follows hull opacity
		interior.visible = cutawayMats[0].opacity < 0.9;
	}

	function setCutaway(on) {
		for (const m of cutawayMats) {
			m.opacity = on ? 0.22 : 1;
			m.transparent = true;
			m.needsUpdate = true;
		}
		interior.visible = on;
	}

	return {
		group,
		update,
		setCutaway,
		updatePlants: plantBed.update,
		set onStageShown(fn) {
			onStageShown = fn;
		}
	};
}
