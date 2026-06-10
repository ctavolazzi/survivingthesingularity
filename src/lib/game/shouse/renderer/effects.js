import * as THREE from 'three';
import { COLORS } from './palette.js';

// Particle effects: dust bursts on builds, power pulses along the conduit
// once solar is online, water droplets under the FarmBot gantry.

const PULSE_PATH = new THREE.CatmullRomCurve3([
	new THREE.Vector3(-13, 1.4, 8.5), // solar array
	new THREE.Vector3(-7.2, 1.0, -1.2), // battery cabinet
	new THREE.Vector3(5.2, 1.8, -1.7), // 200A panel
	new THREE.Vector3(-3.5, 1.9, -2.9) // the Crucible
]);

export function createEffects(scene) {
	const bursts = [];
	const pulses = [];

	// power pulse spheres
	const pulseMat = new THREE.MeshBasicMaterial({ color: COLORS.amber });
	for (let i = 0; i < 4; i++) {
		const m = new THREE.Mesh(new THREE.SphereGeometry(0.09, 6, 6), pulseMat);
		m.visible = false;
		scene.add(m);
		pulses.push({ mesh: m, t: i / 4 });
	}

	function burstAt(x, y, z, color = COLORS.dust, count = 26) {
		const geo = new THREE.BufferGeometry();
		const positions = new Float32Array(count * 3);
		const velocities = [];
		for (let i = 0; i < count; i++) {
			positions[i * 3] = x + (Math.random() - 0.5) * 0.5;
			positions[i * 3 + 1] = y + Math.random() * 0.3;
			positions[i * 3 + 2] = z + (Math.random() - 0.5) * 0.5;
			velocities.push(
				new THREE.Vector3(
					(Math.random() - 0.5) * 2.4,
					Math.random() * 2 + 0.5,
					(Math.random() - 0.5) * 2.4
				)
			);
		}
		geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
		const mat = new THREE.PointsMaterial({
			color,
			size: 0.14,
			transparent: true,
			opacity: 0.9
		});
		const points = new THREE.Points(geo, mat);
		scene.add(points);
		bursts.push({ points, velocities, life: 1 });
	}

	function update(state, dt) {
		// dust bursts decay
		for (let i = bursts.length - 1; i >= 0; i--) {
			const b = bursts[i];
			b.life -= dt / 0.9;
			if (b.life <= 0) {
				scene.remove(b.points);
				b.points.geometry.dispose();
				b.points.material.dispose();
				bursts.splice(i, 1);
				continue;
			}
			const pos = b.points.geometry.attributes.position;
			for (let j = 0; j < pos.count; j++) {
				const v = b.velocities[j];
				v.y -= 4 * dt; // gravity
				pos.setXYZ(j, pos.getX(j) + v.x * dt, Math.max(0.05, pos.getY(j) + v.y * dt), pos.getZ(j) + v.z * dt);
			}
			pos.needsUpdate = true;
			b.points.material.opacity = b.life * 0.9;
		}

		// power pulses run solar -> battery -> panel -> rack while solar is up
		const flowing = state.stage >= 6 && !state.activeEvents.some((e) => e.effect === 'power_regen_zero');
		for (const p of pulses) {
			p.mesh.visible = flowing;
			if (!flowing) continue;
			p.t += dt * 0.12 * state.speed;
			if (p.t > 1) p.t -= 1;
			PULSE_PATH.getPointAt(p.t, p.mesh.position);
		}
	}

	function dispose() {
		for (const b of bursts) {
			scene.remove(b.points);
			b.points.geometry.dispose();
			b.points.material.dispose();
		}
		bursts.length = 0;
		for (const p of pulses) scene.remove(p.mesh);
		pulseMat.dispose();
	}

	return { burstAt, update, dispose };
}
