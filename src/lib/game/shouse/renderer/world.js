import * as THREE from 'three';
import { COLORS } from './palette.js';

// Static world: ground parcel, dirt road, fence line, scatter rocks/shrubs.
// 1 world unit = 1 meter.

export function createWorld() {
	const group = new THREE.Group();
	group.name = 'world';

	// Ground with slight vertex noise so it reads as dirt, not a void
	const groundGeo = new THREE.PlaneGeometry(48, 38, 24, 19);
	const pos = groundGeo.attributes.position;
	for (let i = 0; i < pos.count; i++) {
		const x = pos.getX(i);
		const y = pos.getY(i);
		// deterministic ripple, calmer near the build pad
		const d = Math.hypot(x, y);
		const amp = d > 8 ? 0.18 : 0.04;
		pos.setZ(i, Math.sin(x * 0.7) * Math.cos(y * 0.9) * amp);
	}
	groundGeo.computeVertexNormals();
	const ground = new THREE.Mesh(
		groundGeo,
		new THREE.MeshStandardMaterial({ color: COLORS.ground, roughness: 1 })
	);
	ground.rotation.x = -Math.PI / 2;
	ground.receiveShadow = true;
	group.add(ground);

	// Dirt road along the south edge
	const road = new THREE.Mesh(
		new THREE.BoxGeometry(48, 0.06, 4),
		new THREE.MeshStandardMaterial({ color: COLORS.road, roughness: 1 })
	);
	road.position.set(0, 0.04, 15);
	road.receiveShadow = true;
	group.add(road);

	// Fence posts around three sides (road side open)
	const postGeo = new THREE.BoxGeometry(0.15, 1.1, 0.15);
	const postMat = new THREE.MeshStandardMaterial({ color: COLORS.fence, roughness: 0.9 });
	const railGeo = new THREE.BoxGeometry(4, 0.06, 0.06);
	function fenceRun(x0, z0, x1, z1) {
		const n = Math.round(Math.hypot(x1 - x0, z1 - z0) / 4);
		for (let i = 0; i <= n; i++) {
			const t = i / n;
			const post = new THREE.Mesh(postGeo, postMat);
			post.position.set(x0 + (x1 - x0) * t, 0.55, z0 + (z1 - z0) * t);
			post.castShadow = true;
			group.add(post);
			if (i < n) {
				const rail = new THREE.Mesh(railGeo, postMat);
				rail.position.set(
					x0 + (x1 - x0) * (t + 0.5 / n),
					0.85,
					z0 + (z1 - z0) * (t + 0.5 / n)
				);
				rail.rotation.y = Math.atan2(z1 - z0, x1 - x0) * -1;
				group.add(rail);
			}
		}
	}
	fenceRun(-23, 12.5, -23, -18);
	fenceRun(-23, -18, 23, -18);
	fenceRun(23, -18, 23, 12.5);

	// Scatter: rocks + shrubs
	const rockMat = new THREE.MeshStandardMaterial({ color: COLORS.rock, roughness: 1 });
	const shrubMat = new THREE.MeshStandardMaterial({ color: COLORS.shrub, roughness: 1 });
	const scatter = [
		{ kind: 'rock', x: -18, z: -12, s: 0.8 },
		{ kind: 'rock', x: 16, z: -14, s: 0.5 },
		{ kind: 'rock', x: 20, z: 4, s: 0.6 },
		{ kind: 'shrub', x: -19, z: 6, s: 0.7 },
		{ kind: 'shrub', x: -14, z: -15, s: 0.9 },
		{ kind: 'shrub', x: 18, z: -8, s: 0.6 },
		{ kind: 'shrub', x: 12, z: -16, s: 0.8 }
	];
	for (const s of scatter) {
		const mesh =
			s.kind === 'rock'
				? new THREE.Mesh(new THREE.DodecahedronGeometry(s.s, 0), rockMat)
				: new THREE.Mesh(new THREE.IcosahedronGeometry(s.s, 0), shrubMat);
		mesh.position.set(s.x, s.s * 0.55, s.z);
		mesh.rotation.y = s.x * 1.7;
		mesh.castShadow = true;
		group.add(mesh);
	}

	return group;
}
