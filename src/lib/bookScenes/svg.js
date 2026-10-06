import { SVGRenderer } from 'three/addons/renderers/SVGRenderer.js';
import { createBookScene, projectPins } from './geometry.js';
import { sceneCatalog, sceneSize } from './catalog.js';

const NS = 'http://www.w3.org/2000/svg';
function node(name, attrs = {}, text) {
  const el = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, String(v));
  if (text !== undefined) el.textContent = text;
  return el;
}

/** Same geometry and camera as the reader. No WebGL or GPU is used here. */
export function renderSceneSvg(id, theme = 'dark') {
  const info = sceneCatalog[id], model = createBookScene(id, theme), p = model.palette;
  const svg = node('svg', { xmlns: NS, width: sceneSize.width, height: sceneSize.height, viewBox: `0 0 ${sceneSize.width} ${sceneSize.height}`, role: 'img', 'aria-labelledby': `${id}-title ${id}-desc`, 'data-scene': id, 'data-renderer': 'Three.js r168 SVGRenderer', 'data-theme': theme });
  svg.append(node('title', { id: `${id}-title` }, info.title), node('desc', { id: `${id}-desc` }, info.alt));
  svg.append(node('rect', { width: 960, height: 800, fill: p.paper }));
  svg.append(node('text', { x: 40, y: 54, fill: p.ink, 'font-size': 39, 'font-family': 'Inter,Arial,sans-serif', 'font-weight': 700 }, info.title));
  svg.append(node('path', { d: 'M40 83H920', stroke: p.edge, 'stroke-width': 1.5, fill: 'none' }));
  const renderer = new SVGRenderer();
  renderer.setSize(960, 510); renderer.setPrecision(3); renderer.overdraw = 0.35;
  renderer.render(model.scene, model.camera);
  const geometry = node('g', { transform: 'translate(480 355)', 'data-layer': 'three-geometry' });
  while (renderer.domElement.firstChild) {
    const el = renderer.domElement.firstChild;
    // Presentation attributes make the scene inspectable by the print tooling.
    if (el.getAttribute('style')) {
      for (const item of el.getAttribute('style').split(';')) {
        const colon = item.indexOf(':'); if (colon < 0) continue;
        el.setAttribute(item.slice(0, colon).trim(), item.slice(colon + 1).trim());
      }
      el.removeAttribute('style');
    }
    geometry.append(el);
  }
  svg.append(geometry);
  const annotations = node('g', { 'data-layer': 'annotations', 'font-family': 'Inter,Arial,sans-serif' });
  for (const pin of projectPins(model)) {
    annotations.append(node('circle', { cx: pin.x.toFixed(3), cy: (pin.y + 100).toFixed(3), r: 19, fill: p.paper, stroke: p.amber, 'stroke-width': 3 }));
    annotations.append(node('text', { x: pin.x.toFixed(3), y: (pin.y + 108).toFixed(3), fill: p.ink, 'text-anchor': 'middle', 'font-size': 25, 'font-weight': 700 }, pin.number));
  }
  annotations.append(node('path', { d: 'M40 610H920', stroke: p.edge, 'stroke-width': 1.5, fill: 'none' }));
  info.labels.forEach(([label, detail], i) => {
    const x = i % 2 ? 505 : 40, y = i < 2 ? 646 : 719;
    annotations.append(node('text', { x, y, fill: p.amber, 'font-size': 25, 'font-weight': 700 }, `${i + 1}  ${label}`));
    annotations.append(node('text', { x, y: y + 30, fill: p.ink, 'font-size': 26 }, detail));
  });
  annotations.append(node('text', { x: 40, y: 788, fill: p.muted, 'font-size': 24 }, info.note));
  svg.append(annotations);
  model.dispose();
  return new XMLSerializer().serializeToString(svg);
}
