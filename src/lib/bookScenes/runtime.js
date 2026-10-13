import * as THREE from 'three';
import { createBookScene, projectPins } from './geometry.js';

// This module is imported only after the reader requests the 3D view.
// Every frame responds to a control or a resize; there is no animation loop.
export function mountScene(host, id, onLost, onPins) {
  const model = createBookScene(id, 'dark');
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'low-power' });
  } catch (error) { model.dispose(); throw error; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.domElement.setAttribute('aria-hidden', 'true');
  renderer.domElement.setAttribute('data-three-canvas', id);
  host.append(renderer.domElement);
  let visible = true, alive = true;
  function render() {
    if (!alive || !visible) return;
    const width = Math.max(1, host.clientWidth);
    renderer.setSize(width, width * 510 / 960, false);
    renderer.render(model.scene, model.camera);
    onPins(projectPins(model));
  }
  function lost(event) { event.preventDefault(); onLost(); }
  renderer.domElement.addEventListener('webglcontextlost', lost);
  const resize = new ResizeObserver(render); resize.observe(host);
  const visibility = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; if (visible) render(); });
  visibility.observe(host);
  render();
  return {
    focus(id) { model.focus(id); render(); },
    view(angle, mode) { model.setView(angle, mode); render(); },
    dispose() {
      if (!alive) return;
      alive = false; resize.disconnect(); visibility.disconnect();
      renderer.domElement.removeEventListener('webglcontextlost', lost);
      model.dispose(); renderer.dispose(); renderer.forceContextLoss(); renderer.domElement.remove();
    }
  };
}
