import * as THREE from 'three';
import { COLORS } from './palette.js';

// Low-poly plant clusters for the 8 FarmBot bed slots. Category decides the
// silhouette; growth (0..1) scales the cluster.

const SLOT_POSITIONS = [];
for (let col = 0; col < 4; col++) {
	for (let row = 0; row < 2; row++) {
		SLOT_POSITIONS.push({ x: -1.05 + col * 0.7, z: row === 0 ? -0.37 : 0.37 });
	}
}

function makePlantMesh(category) {
	const g = new THREE.Group();
	if (category === 'leafy-green') {
		const leafMat = new THREE.MeshStandardMaterial({ color: COLORS.leafGreen, roughness: 0.9 });
		for (let i = 0; i < 3; i++) {
			const leaf = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 5), leafMat);
			leaf.scale.set(1, 0.55, 1);
			leaf.position.set(Math.cos(i * 2.1) * 0.07, 0.08 + i * 0.04, Math.sin(i * 2.1) * 0.07);
			g.add(leaf);
		}
	} else if (category === 'root-vegetable') {
		const topMat = new THREE.MeshStandardMaterial({ color: COLORS.rootGreen, roughness: 0.9 });
		for (let i = 0; i < 4; i++) {
			const frond = new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.22, 5), topMat);
			frond.position.set(Math.cos(i * 1.6) * 0.05, 0.12, Math.sin(i * 1.6) * 0.05);
			frond.rotation.z = Math.cos(i * 1.6) * 0.35;
			frond.rotation.x = -Math.sin(i * 1.6) * 0.35;
			g.add(frond);
		}
	} else {
		// fruiting: stem + fruit spheres
		const stemMat = new THREE.MeshStandardMaterial({ color: COLORS.leafDark, roughness: 0.9 });
		const fruitMat = new THREE.MeshStandardMaterial({
			color: COLORS.fruitRed,
			emissive: COLORS.fruitRed,
			emissiveIntensity: 0.15,
			roughness: 0.6
		});
		const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.035, 0.3, 6), stemMat);
		stem.position.y = 0.15;
		g.add(stem);
		for (let i = 0; i < 2; i++) {
			const fruit = new THREE.Mesh(new THREE.SphereGeometry(0.055, 6, 6), fruitMat);
			fruit.position.set(i === 0 ? 0.07 : -0.06, 0.16 + i * 0.09, 0.03);
			g.add(fruit);
		}
	}
	return g;
}

export function createPlantBed() {
	const group = new THREE.Group();
	group.name = 'plantBed';
	const slots = new Array(8).fill(null); // { mesh, category }

	function update(plants, time) {
		if (!plants || plants.length === 0) return;
		for (const p of plants) {
			const pos = SLOT_POSITIONS[p.slot];
			if (!pos) continue;
			let slot = slots[p.slot];
			if (!slot || slot.category !== p.category) {
				if (slot) group.remove(slot.mesh);
				const mesh = makePlantMesh(p.category);
				mesh.position.set(pos.x, 0, pos.z);
				group.add(mesh);
				slot = { mesh, category: p.category };
				slots[p.slot] = slot;
			}
			// growth scale, with a gentle idle sway when mature
			const heightFactor = 0.7 + Math.min(1.2, (p.height || 30) / 60) * 0.6;
			const s = 0.15 + 0.85 * Math.min(1, p.growth);
			slot.mesh.scale.set(s, s * heightFactor, s);
			slot.mesh.rotation.z = Math.sin(time * 1.4 + p.slot * 1.7) * 0.04 * p.growth;
		}
	}

	return { group, update };
}
