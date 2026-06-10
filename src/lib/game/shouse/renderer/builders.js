import * as THREE from 'three';
import { COLORS } from './palette.js';

// Little construction crew. Appears while a stage is under construction:
// workers walk the site, stop, hammer (with dust puffs), repeat. A supply
// crate + sawhorse sit at the edge of the work zone.

const CREW_SIZE = 4;
const WALK_SPEED = 1.6;
const VEST_COLORS = [0xf59e0b, 0x3b82f6, 0xf59e0b, 0x10b981];

function makeWorker(vestColor) {
	const g = new THREE.Group();

	const legsMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.9 });
	const legs = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.3, 0.16), legsMat);
	legs.position.y = 0.15;
	g.add(legs);

	const bodyMat = new THREE.MeshStandardMaterial({ color: vestColor, roughness: 0.85 });
	const body = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.4, 0.2), bodyMat);
	body.position.y = 0.5;
	body.castShadow = true;
	g.add(body);

	const headMat = new THREE.MeshStandardMaterial({ color: 0xd9b48f, roughness: 0.9 });
	const head = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 7), headMat);
	head.position.y = 0.82;
	g.add(head);

	const hatMat = new THREE.MeshStandardMaterial({ color: COLORS.amber, roughness: 0.6 });
	const hat = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.14, 0.09, 10), hatMat);
	hat.position.y = 0.93;
	g.add(hat);

	// tool arm: pivot at the shoulder so the hammer swings
	const arm = new THREE.Group();
	arm.position.set(0.18, 0.62, 0);
	const armMesh = new THREE.Mesh(
		new THREE.BoxGeometry(0.08, 0.3, 0.08),
		new THREE.MeshStandardMaterial({ color: vestColor, roughness: 0.85 })
	);
	armMesh.position.y = -0.12;
	arm.add(armMesh);
	const hammerHead = new THREE.Mesh(
		new THREE.BoxGeometry(0.14, 0.07, 0.07),
		new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.5 })
	);
	hammerHead.position.y = -0.28;
	arm.add(hammerHead);
	g.add(arm);

	return { group: g, arm };
}

export function createBuilders() {
	const group = new THREE.Group();
	group.name = 'builders';
	group.visible = false;

	const workers = [];
	for (let i = 0; i < CREW_SIZE; i++) {
		const w = makeWorker(VEST_COLORS[i % VEST_COLORS.length]);
		group.add(w.group);
		workers.push({
			...w,
			state: 'walk', // walk | work
			target: new THREE.Vector3(),
			workTimer: 0,
			puffTimer: 0,
			offset: i * 1.7 // desync animation phases
		});
	}

	// site props: supply crate stack + sawhorse
	const props = new THREE.Group();
	const crateMat = new THREE.MeshStandardMaterial({ color: 0x86653e, roughness: 0.9 });
	const crate1 = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.5, 0.7), crateMat);
	crate1.position.y = 0.25;
	crate1.castShadow = true;
	props.add(crate1);
	const crate2 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.4, 0.5), crateMat);
	crate2.position.set(0.15, 0.7, -0.05);
	crate2.rotation.y = 0.4;
	crate2.castShadow = true;
	props.add(crate2);
	const horseMat = new THREE.MeshStandardMaterial({ color: COLORS.amber, roughness: 0.8 });
	const horseBeam = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.08, 0.12), horseMat);
	horseBeam.position.set(1.4, 0.5, 0.3);
	props.add(horseBeam);
	for (const dx of [-0.45, 0.45]) {
		const leg = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.5, 0.3), horseMat);
		leg.position.set(1.4 + dx, 0.25, 0.3);
		props.add(leg);
	}
	group.add(props);

	let activeBounds = null;

	function randomPointIn(bounds, out) {
		out.set(
			bounds.x + (Math.random() - 0.5) * bounds.w * 0.85,
			0,
			bounds.z + (Math.random() - 0.5) * bounds.d * 0.85
		);
		return out;
	}

	function activate(bounds) {
		activeBounds = bounds;
		group.visible = true;
		props.position.set(bounds.x - bounds.w / 2 - 1.2, 0, bounds.z + bounds.d / 2 + 1.0);
		for (const w of workers) {
			randomPointIn(bounds, w.group.position);
			randomPointIn(bounds, w.target);
			w.state = 'walk';
			w.group.scale.set(0.01, 0.01, 0.01);
		}
	}

	// bounds: scaffold box of the stage under construction, or null when idle.
	// burstAt: effects dust emitter for hammer puffs.
	function update(bounds, dt, time, burstAt) {
		if (!bounds) {
			if (activeBounds) {
				activeBounds = null;
				group.visible = false;
			}
			return;
		}
		if (!activeBounds || activeBounds !== bounds) activate(bounds);

		for (const w of workers) {
			// pop-in
			if (w.group.scale.x < 1) {
				const s = Math.min(1, w.group.scale.x + dt * 3);
				w.group.scale.set(s, s, s);
			}

			if (w.state === 'walk') {
				const pos = w.group.position;
				const dx = w.target.x - pos.x;
				const dz = w.target.z - pos.z;
				const dist = Math.hypot(dx, dz);
				if (dist < 0.15) {
					w.state = 'work';
					w.workTimer = 1.5 + Math.random() * 2;
					w.puffTimer = 0.4 + Math.random() * 0.5;
				} else {
					const step = Math.min(dist, WALK_SPEED * dt);
					pos.x += (dx / dist) * step;
					pos.z += (dz / dist) * step;
					w.group.rotation.y = Math.atan2(dx, dz);
					// walk bob
					pos.y = Math.abs(Math.sin((time + w.offset) * 9)) * 0.06;
					w.arm.rotation.x = Math.sin((time + w.offset) * 9) * 0.4;
				}
			} else {
				// work: hammer swing toward the ground
				w.group.position.y = 0;
				const swing = (Math.sin((time + w.offset) * 11) + 1) / 2; // 0..1
				w.arm.rotation.x = -0.4 - swing * 1.4;
				w.workTimer -= dt;
				w.puffTimer -= dt;
				if (w.puffTimer <= 0 && burstAt) {
					// puff at the hammer strike point, in front of the worker
					const fx = w.group.position.x + Math.sin(w.group.rotation.y) * 0.35;
					const fz = w.group.position.z + Math.cos(w.group.rotation.y) * 0.35;
					burstAt(fx, 0.25, fz, COLORS.dust, 8);
					w.puffTimer = 0.7 + Math.random() * 0.8;
				}
				if (w.workTimer <= 0) {
					randomPointIn(bounds, w.target);
					w.state = 'walk';
				}
			}
		}
	}

	return { group, update };
}
