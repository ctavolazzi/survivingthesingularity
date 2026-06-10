import * as THREE from 'three';

// Orthographic isometric camera rig: drag pan, wheel/pinch zoom,
// 45-degree azimuth snaps (Q/E or buttons). Fixed isometric elevation.

const ELEVATION = Math.atan(1 / Math.sqrt(2)); // ~35.26 deg
const RADIUS = 60;
const VIEW_SIZE = 13; // ortho half-height in world units at zoom 1
const PAN_LIMIT_X = 24;
const PAN_LIMIT_Z = 20;

export function createCameraRig(canvas) {
	const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 220);
	let aspect = 1;

	let azimuthIndex = 1; // x 45deg -> start at 45
	let azimuth = azimuthIndex * (Math.PI / 4);
	let targetAzimuth = azimuth;

	let zoom = 1;
	let targetZoom = 1;

	const pivot = new THREE.Vector3(0, 0, 0);
	const targetPivot = new THREE.Vector3(0, 0, 0);

	// Scripted glide target (stage completion focus)
	let glide = null; // { point: Vector3, t: 0 }

	const pointers = new Map();
	let pinchDist = 0;

	function onPointerDown(e) {
		pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
		if (pointers.size === 2) {
			const [a, b] = [...pointers.values()];
			pinchDist = Math.hypot(a.x - b.x, a.y - b.y);
		}
		canvas.setPointerCapture?.(e.pointerId);
	}

	function onPointerMove(e) {
		const prev = pointers.get(e.pointerId);
		if (!prev) return;
		const dx = e.clientX - prev.x;
		const dy = e.clientY - prev.y;
		pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });

		if (pointers.size === 1) {
			glide = null;
			const wpp = (2 * VIEW_SIZE) / (canvas.clientHeight || 1) / zoom;
			const right = new THREE.Vector3(Math.sin(azimuth), 0, -Math.cos(azimuth));
			const forward = new THREE.Vector3(-Math.cos(azimuth), 0, -Math.sin(azimuth));
			targetPivot.addScaledVector(right, -dx * wpp);
			targetPivot.addScaledVector(forward, (dy * wpp) / Math.sin(ELEVATION));
			clampPivot();
		} else if (pointers.size === 2) {
			const [a, b] = [...pointers.values()];
			const d = Math.hypot(a.x - b.x, a.y - b.y);
			if (pinchDist > 0) {
				targetZoom = THREE.MathUtils.clamp(targetZoom * (d / pinchDist), 0.5, 3);
			}
			pinchDist = d;
		}
	}

	function onPointerUp(e) {
		pointers.delete(e.pointerId);
		pinchDist = 0;
	}

	function onWheel(e) {
		e.preventDefault();
		targetZoom = THREE.MathUtils.clamp(targetZoom * Math.exp(-e.deltaY * 0.0012), 0.5, 3);
	}

	function clampPivot() {
		targetPivot.x = THREE.MathUtils.clamp(targetPivot.x, -PAN_LIMIT_X, PAN_LIMIT_X);
		targetPivot.z = THREE.MathUtils.clamp(targetPivot.z, -PAN_LIMIT_Z, PAN_LIMIT_Z);
		targetPivot.y = 0;
	}

	canvas.addEventListener('pointerdown', onPointerDown);
	canvas.addEventListener('pointermove', onPointerMove);
	canvas.addEventListener('pointerup', onPointerUp);
	canvas.addEventListener('pointercancel', onPointerUp);
	canvas.addEventListener('wheel', onWheel, { passive: false });

	function rotate(dir) {
		azimuthIndex += dir;
		targetAzimuth = azimuthIndex * (Math.PI / 4);
	}

	function focusOn(x, z) {
		glide = { point: new THREE.Vector3(x, 0, z) };
	}

	function resize(width, height) {
		aspect = width / Math.max(1, height);
		camera.left = -VIEW_SIZE * aspect;
		camera.right = VIEW_SIZE * aspect;
		camera.top = VIEW_SIZE;
		camera.bottom = -VIEW_SIZE;
		camera.updateProjectionMatrix();
	}

	function update() {
		// Smooth-lerp everything (same easing trick as the original engine)
		azimuth += (targetAzimuth - azimuth) * 0.08;
		zoom += (targetZoom - zoom) * 0.08;
		if (glide) {
			targetPivot.lerp(glide.point, 0.04);
			if (targetPivot.distanceTo(glide.point) < 0.3) glide = null;
			clampPivot();
		}
		pivot.lerp(targetPivot, 0.1);

		camera.zoom = zoom;
		camera.position.set(
			pivot.x + RADIUS * Math.cos(ELEVATION) * Math.cos(azimuth),
			pivot.y + RADIUS * Math.sin(ELEVATION),
			pivot.z + RADIUS * Math.cos(ELEVATION) * Math.sin(azimuth)
		);
		camera.lookAt(pivot);
		camera.updateProjectionMatrix();
	}

	function dispose() {
		canvas.removeEventListener('pointerdown', onPointerDown);
		canvas.removeEventListener('pointermove', onPointerMove);
		canvas.removeEventListener('pointerup', onPointerUp);
		canvas.removeEventListener('pointercancel', onPointerUp);
		canvas.removeEventListener('wheel', onWheel);
	}

	return { camera, update, resize, rotate, focusOn, dispose };
}
