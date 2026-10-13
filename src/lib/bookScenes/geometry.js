import * as THREE from 'three';

export const palettes = {
  dark: { paper: '#020617', ink: '#f1f5f9', muted: '#94a3b8', floor: '#1e293b', edge: '#475569', wall: '#cbd5e1', shade: '#94a3b8', roof: '#3b82f6', amber: '#f59e0b', blue: '#3b82f6', green: '#22c55e', leaf: '#16a34a', soil: '#78350f', earth: '#92400e', wood: '#d97706', dark: '#0f172a', water: '#60a5fa' },
  light: { paper: '#ffffff', ink: '#0f172a', muted: '#475569', floor: '#e2e8f0', edge: '#94a3b8', wall: '#f1f5f9', shade: '#cbd5e1', roof: '#2563eb', amber: '#b45309', blue: '#1d4ed8', green: '#15803d', leaf: '#166534', soil: '#78350f', earth: '#a16207', wood: '#b45309', dark: '#334155', water: '#2563eb' }
};

function workshop(kit) {
  const { box, cylinder, line, cone, person, group, palette: p } = kit;
  const floor = group('tools');
  box(floor, [0, -.16, 0], [10.4, .3, 7], p.floor).renderOrder = -100;
  // Two low walls leave the working interior open to the reader.
  box(floor, [0, .56, -3.3], [10.4, 1.1, .18], p.shade);
  box(floor, [-5.1, .56, 0], [.18, 1.1, 6.6], p.wall);
  for (let x = -4.6; x < 5; x += 1) line(floor, [[x, .002, -3], [x, .002, 3.1]], p.edge, .014);
  // Repair bench, vise, tools and a visible replacement gear.
  box(floor, [-2.8, 1.12, -1.6], [3.6, .17, 1.2], p.wood);
  for (const x of [-4.2, -1.4]) for (const z of [-2, -1.2]) box(floor, [x, .55, z], [.12, 1.1, .12], p.dark);
  box(floor, [-4, 1.4, -1.6], [.5, .36, .46], p.blue);
  cylinder(floor, [-4, 1.54, -1.25], .055, .7, p.shade, 8, [Math.PI / 2, 0, 0]);
  for (let i = 0; i < 5; i++) {
    box(floor, [-3.1 + i * .29, 1.23, -1.7], [.1, .07, .52 - (i % 2) * .12], i % 2 ? p.amber : p.shade);
  }
  // Open printer frame, gantry, build plate and a small printed bracket.
  const printer = group('tools');
  box(printer, [.3, .7, -1.55], [1.9, 1.4, 1.4], p.dark);
  box(printer, [.3, 1.46, -1.55], [2.1, .14, 1.7], p.shade);
  for (const x of [-.57, 1.17]) for (const z of [-2.18, -.92]) box(printer, [x, 2.17, z], [.1, 1.4, .1], p.blue);
  for (const z of [-2.18, -.92]) box(printer, [.3, 2.86, z], [1.84, .1, .1], p.blue);
  box(printer, [.3, 2.13, -1.6], [1.8, .1, .13], p.shade);
  box(printer, [.12, 1.97, -1.6], [.32, .27, .3], p.amber);
  box(printer, [.3, 1.62, -1.5], [1.44, .09, 1.07], p.floor);
  box(printer, [.3, 1.8, -1.5], [.45, .3, .12], p.amber);
  box(printer, [.45, 1.68, -1.5], [.5, .1, .3], p.amber);
  cylinder(printer, [.3, 3.11, -1.5], .29, .14, p.amber, 18, [Math.PI / 2, 0, 0]);
  cylinder(printer, [.3, 3.11, -1.59], .13, .2, p.dark, 16, [Math.PI / 2, 0, 0]);
  // Shared walk-behind tractor with tread, handles and attachment.
  const tractor = group('tools');
  for (const x of [2.35, 3.85]) {
    cylinder(tractor, [x, .55, 1.35], .56, .35, p.dark, 18, [0, 0, Math.PI / 2]);
    cylinder(tractor, [x + .18, .55, 1.35], .27, .045, p.amber, 14, [0, 0, Math.PI / 2]);
    for (let i = 0; i < 10; i++) { const a = i * Math.PI / 5; const block = box(tractor, [x, .55 + Math.cos(a) * .53, 1.35 + Math.sin(a) * .53], [.38, .09, .17], p.edge); block.rotation.x = -a; }
  }
  box(tractor, [3.1, .72, 1.2], [1.15, .55, 1.2], p.blue);
  box(tractor, [3.1, 1.12, 1.25], [.7, .26, .8], p.amber);
  for (const x of [2.77, 3.43]) line(tractor, [[x, .9, 1.45], [x, 1.7, 2.7], [x, 1.73, 3]], p.shade, .05);
  line(tractor, [[2.77, 1.7, 2.7], [3.43, 1.7, 2.7]], p.shade, .05);
  box(tractor, [3.1, .23, .15], [1.9, .23, .55], p.shade);
  // Materials rack, bins, a documented spare and incoming supply line.
  const supplies = group('supplies');
  for (const x of [3.05, 4.55]) for (const z of [-2.65, -1.7]) box(supplies, [x, 1.05, z], [.1, 2.1, .1], p.edge);
  for (const y of [.3, 1.1, 1.9]) {
    box(supplies, [3.8, y, -2.16], [1.7, .08, 1.14], p.shade);
    for (const x of [3.38, 4.12]) box(supplies, [x, y + .23, -2.16], [.6, .38, .75], y === 1.1 ? p.blue : p.wood);
  }
  line(supplies, [[5.6, .06, -2.2], [4.9, .06, -2.2]], p.amber, .055);
  // People remain visible, including the person bringing the repair in.
  const people = group('people');
  person(people, -2.6, -.3, p.amber, .96);
  person(people, .15, 1.2, p.blue, 1.08);
  // A repaired part at the open edge of the workshop, not a production metric.
  const output = group('output');
  box(output, [-2.65, .53, 2.1], [1.9, .12, 1.05], p.wood);
  for (const x of [-3.4, -1.9]) box(output, [x, .25, 2.1], [.12, .5, .7], p.dark);
  cylinder(output, [-2.65, .69, 2.1], .4, .15, p.amber, 14);
  cylinder(output, [-2.65, .79, 2.1], .15, .08, p.dark, 14);
  for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; const tooth = box(output, [-2.65 + Math.cos(a) * .4, .7, 2.1 + Math.sin(a) * .4], [.2, .15, .18], p.amber); tooth.rotation.y = -a; }
  kit.arrow(output, [[-2.5, .08, 2.85], [-2.5, .08, 3.8], [-1, .08, 3.8]], p.amber);
  return [
    { number: 1, point: [-2.6, 2.2, -.3] }, { number: 2, point: [3.8, 2.7, -2.2] },
    { number: 3, point: [.3, 3.5, -1.6] }, { number: 4, point: [-2.65, 1.4, 2.1] }
  ];
}

function food(kit) {
  const { box, line, cylinder, cone, group, person, palette: p } = kit;
  const ground = group('route');
  box(ground, [0, -.18, 0], [12.7, .3, 8.5], p.floor).renderOrder = -100;
  box(ground, [0, .005, .55], [12.6, .045, 1.18], p.edge).renderOrder = -99;
  for (let x = -5.6; x <= 5.6; x += .8) box(ground, [x, .04, .57], [.34, .018, .038], p.shade);
  // Productive beds and a small open greenhouse, with individual crops.
  const garden = group('garden');
  for (const z of [-2.9, -1.5]) {
    box(garden, [-4.25, .17, z], [3.4, .32, 1], p.wood);
    box(garden, [-4.25, .35, z], [3.15, .12, .8], p.soil);
    for (let i = 0; i < 6; i++) kit.plant(garden, -5.55 + i * .52, .43, z, .45 + .1 * (i % 2));
  }
  for (const x of [-5.9, -4.2, -2.6]) {
    const arch = [];
    for (let i = 0; i <= 12; i++) { const a = i * Math.PI / 12; arch.push([x, .42 + Math.sin(a) * 1.7, -2.2 + Math.cos(a) * 1.48]); }
    line(garden, arch, p.shade, .035);
  }
  for (const z of [-3.67, -.73]) line(garden, [[-5.9, .43, z], [-2.6, .43, z]], p.shade, .035);
  line(garden, [[-5.9, 2.12, -2.2], [-2.6, 2.12, -2.2]], p.shade, .035);
  // Packing room, open at the front, with crates and a person at the table.
  const pack = group('people');
  box(pack, [-.35, .62, -2.25], [2.25, 1.2, 1.8], p.wall);
  box(pack, [-.35, .67, -1.32], [2.3, .1, .56], p.wood);
  box(pack, [-.35, 1.52, -2.25], [2.55, .16, 2.16], p.blue).renderOrder = 5;
  for (const x of [-1.25, .55]) box(pack, [x, .9, -1.1], [.09, 1.8, .09], p.shade);
  for (let i = 0; i < 3; i++) kit.crate(pack, -.97 + i * .63, .82, -1.32, .47);
  person(pack, -.35, -.56, p.amber, .8);
  // The partner is visibly outside the garden; its food joins the route.
  const partner = group('partner');
  kit.house(partner, 3.5, -2.25, 2.25, 1.45, p.blue);
  box(partner, [3.5, .9, -1.24], [1.7, .16, .65], p.amber);
  kit.crate(partner, 4.5, .25, -1, .65);
  kit.crate(partner, 4.5, .76, -1, .6);
  person(partner, 2.25, -1, p.blue, .88);
  // Five separate doors rather than an undifferentiated output box.
  const homes = group('homes');
  for (let i = 0; i < 5; i++) {
    const x = -4.8 + i * 2.4;
    kit.house(homes, x, 2.75, 1.58, .98 + (i % 2) * .15, i % 2 ? p.amber : p.blue);
    box(homes, [x, .045, 1.64], [.55, .08, 1.28], p.shade);
    kit.crate(homes, x + .57, .18, 1.98, .34);
    kit.arrow(homes, [[x, .115, 1], [x, .115, 1.86]], p.amber, .026);
  }
  kit.arrow(garden, [[-3, .11, -.5], [-3, .11, .25], [-1.3, .11, .25]], p.amber, .036);
  kit.arrow(partner, [[3.1, .13, -.85], [3.1, .13, .25], [.8, .13, .25]], p.blue, .046);
  // Cargo cart and visible wheels imply transport without pretending it is automatic.
  box(pack, [.1, .48, .45], [1.05, .5, .65], p.wood);
  for (const x of [-.31, .5]) for (const z of [.08, .83]) cylinder(pack, [x, .19, z], .18, .08, p.dark, 12, [Math.PI / 2, 0, 0]);
  line(pack, [[-.42, .65, .4], [-1, .85, .4]], p.shade, .04);
  return [
    { number: 1, point: [-4.5, 2.8, -2.2] }, { number: 2, point: [3.5, 3.3, -2.25] },
    { number: 3, point: [-.3, 2.7, -.8] }, { number: 4, point: [0, 2.35, 2.75] }
  ];
}

function soil(kit) {
  const { box, line, cylinder, cone, sphere, group, palette: p } = kit;
  const ground = group('bed');
  box(ground, [0, -.23, 0], [11.3, .3, 7.1], p.floor).renderOrder = -100;
  // Back half of a raised bed; the open face exposes the roots, not a glass box.
  box(ground, [-.5, .63, -.2], [5.5, 1.25, 3], p.soil).renderOrder = -80;
  box(ground, [-.5, 1.28, -.2], [5.5, .12, 3], p.earth).renderOrder = -79;
  for (let i = 0; i < 14; i++) {
    const x = -3 + i * .39;
    box(ground, [x, 1.38, -.3 + .13 * Math.sin(i)], [.3, .05, 2.55], p.wood).rotation.y = .12 * Math.sin(i * 2);
  }
  for (const x of [-3.32, 2.32]) box(ground, [x, 1.25, -.2], [.14, .48, 3.18], p.wood);
  box(ground, [-.5, 1.25, -1.77], [5.75, .48, .12], p.wood);
  const roots = group('roots');
  for (let i = 0; i < 5; i++) {
    const x = -2.7 + i * 1.06;
    kit.plant(roots, x, 1.43, -.1, .88 + .13 * (i % 2));
    // Roots on the exposed face vary in branching, deliberately without a scale.
    const z = 1.315;
    line(roots, [[x, 1.36, -.1], [x, 1.16, .52], [x + .12, .78, z], [x -.03, .14, z]], p.shade, .036);
    for (let j = 0; j < 4; j++) {
      const y = 1.1 - j * .22; const s = j % 2 ? -1 : 1;
      line(roots, [[x + .08, y, z], [x + s * .24, y -.11, z + .02], [x + s * .46, y -.29, z + .03]], p.shade, .021);
      line(roots, [[x + s * .24, y -.11, z + .02], [x + s * .38, y -.1, z + .02]], p.shade, .015);
    }
  }
  // Soil organisms are marks for living activity, not organisms drawn to scale.
  for (let i = 0; i < 30; i++) {
    const x = -3 + ((i * .713) % 5.1); const y = .1 + ((i * .317) % 1.09);
    sphere(roots, [x, y, 1.37], .038 + (i % 3) * .013, i % 2 ? p.amber : p.blue, 6);
  }
  const inputs = group('inputs');
  // Separate compost bin with slatted sides and organic matter.
  for (let y = .2; y < 1.4; y += .28) {
    box(inputs, [-4.65, y, -1], [1.25, .2, 1.25], p.wood);
    box(inputs, [-4.65, y + .01, -.35], [1.3, .13, .055], p.shade);
  }
  box(inputs, [-4.65, 1.31, -1], [1.05, .1, 1.05], p.soil);
  for (let i = 0; i < 8; i++) sphere(inputs, [-5.03 + (i % 3) * .31, 1.42, -1.32 + Math.floor(i / 3) * .3], .16, p.leaf, 6);
  kit.arrow(inputs, [[-4.5, .1, .2], [-4.5, .1, .9], [-3.6, .1, .9]], p.amber);
  // Water barrel and pipe, with water entering the soil and drainage leaving.
  cylinder(inputs, [3.85, .88, -1.45], .65, 1.65, p.blue, 20);
  cylinder(inputs, [3.85, 1.72, -1.45], .63, .07, p.shade, 20);
  for (const y of [.3, 1.4]) cylinder(inputs, [3.85, y, -1.45], .68, .07, p.dark, 20);
  line(inputs, [[3.85, .28, -.8], [3.2, .28, -.2], [2.8, 1.62, -.2], [-2.6, 1.62, -.2]], p.water, .045);
  for (let i = 0; i < 5; i++) kit.arrow(inputs, [[-2.6 + i * 1.04, 1.58, -.2], [-2.6 + i * 1.04, 1.4, -.2]], p.water, .019);
  // Sun is an explicit outside input with directional rays.
  sphere(inputs, [-2.8, 4.1, -2], .53, p.amber, 16);
  for (let i = 0; i < 8; i++) { const a = Math.PI * i / 4; line(inputs, [[-2.8 + Math.cos(a) * .69, 4.1 + Math.sin(a) * .69, -2], [-2.8 + Math.cos(a) * .88, 4.1 + Math.sin(a) * .88, -2]], p.amber, .04); }
  kit.arrow(inputs, [[-2, 3.65, -1.8], [-1.25, 2.8, -1]], p.amber);
  const harvest = group('harvest');
  kit.crate(harvest, 4.1, .28, 1.78, 1.18);
  for (let i = 0; i < 5; i++) sphere(harvest, [3.72 + (i % 3) * .35, .72, 1.52 + Math.floor(i / 3) * .4], .22, i % 2 ? p.leaf : p.amber, 8);
  kit.arrow(harvest, [[1.8, .1, 2], [2.9, .1, 2], [3.2, .1, 2]], p.amber);
  kit.arrow(harvest, [[-.8, .05, 1.8], [-.8, .05, 2.85], [.7, .05, 2.85]], p.blue);
  // Two gentle upward paths indicate losses through plants and air.
  kit.arrow(harvest, [[1.4, 2.3, -.7], [1.55, 2.9, -.7], [1.42, 3.5, -.7]], p.water, .025);
  return [
    { number: 1, point: [3.85, 2.6, -1.45] }, { number: 2, point: [-1.5, .8, 1.65] },
    { number: 3, point: [4.1, 1.55, 1.78] }, { number: 4, point: [-.6, .4, 3.2] }
  ];
}

/** No random numbers, clocks, external textures, or measured-looking dimensions. */
export function createBookScene(id, theme = 'dark') {
  const palette = palettes[theme];
  if (!palette) throw new Error(`Unknown scene theme: ${theme}`);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(palette.paper);
  const groups = [];
  const material = color => new THREE.MeshBasicMaterial({ color });
  function group(role) { const g = new THREE.Group(); g.userData.role = role; groups.push(g); scene.add(g); return g; }
  function add(parent, geometry, color, xyz, rotation) {
    const m = new THREE.Mesh(geometry, material(color)); m.position.set(...xyz); if (rotation) m.rotation.set(...rotation); parent.add(m); return m;
  }
  function box(parent, xyz, size, color) {
    const mesh = add(parent, new THREE.BoxGeometry(...size, Math.max(1, Math.ceil(size[0] / .8)), Math.max(1, Math.ceil(size[1] / .8)), Math.max(1, Math.ceil(size[2] / .8))), color, xyz);
    // Three flat face tones retain depth in grayscale and in the SVG renderer.
    const base = new THREE.Color(color);
    mesh.material = [1, .73, 1.12, .65, .9, .78].map(k => new THREE.MeshBasicMaterial({ color: base.clone().multiplyScalar(k) }));
    return mesh;
  }
  function cylinder(parent, xyz, radius, height, color, segments = 12, rotation) { return add(parent, new THREE.CylinderGeometry(radius, radius, height, segments), color, xyz, rotation); }
  function cone(parent, xyz, radius, height, color, segments = 10, rotation) { return add(parent, new THREE.ConeGeometry(radius, height, segments), color, xyz, rotation); }
  function sphere(parent, xyz, radius, color, segments = 10) { return add(parent, new THREE.SphereGeometry(radius, segments, Math.max(4, Math.floor(segments / 2))), color, xyz); }
  function line(parent, points, color, radius = .025) {
    const vectors = points.map(p => new THREE.Vector3(...p));
    for (let i = 1; i < vectors.length; i++) {
      const a = vectors[i - 1], b = vectors[i], direction = b.clone().sub(a);
      if (direction.length() < .0001) continue;
      const mesh = cylinder(parent, a.clone().add(b).multiplyScalar(.5).toArray(), radius, direction.length(), color, 6);
      mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.normalize());
    }
  }
  function arrow(parent, points, color, radius = .04) {
    line(parent, points, color, radius);
    const a = new THREE.Vector3(...points.at(-2)), b = new THREE.Vector3(...points.at(-1));
    const direction = b.clone().sub(a).normalize();
    const tip = cone(parent, b.clone().sub(direction.clone().multiplyScalar(.1)).toArray(), radius * 3, .28, color, 8);
    tip.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction);
  }
  function plant(parent, x, y, z, size = .6) {
    line(parent, [[x, y, z], [x, y + size * .95, z]], palette.leaf, .025);
    for (let i = 0; i < 5; i++) {
      const a = i * 2.4, leaf = sphere(parent, [x + Math.cos(a) * size * .27, y + .15 + i * size * .14, z + Math.sin(a) * size * .27], size * .29, i % 2 ? palette.green : palette.leaf, 8);
      leaf.scale.set(1.5, .22, .62); leaf.rotation.set(.2, -a, .3 * (i % 2 ? -1 : 1));
    }
  }
  function person(parent, x, z, color, scale = 1) {
    const person = new THREE.Group(); parent.add(person); person.position.set(x, 0, z); person.scale.setScalar(scale);
    sphere(person, [0, 1.5, 0], .18, palette.shade, 10);
    cone(person, [0, 1.61, 0], .24, .09, palette.amber, 12);
    box(person, [0, 1, 0], [.41, .68, .26], color);
    for (const s of [-1, 1]) {
      line(person, [[s * .12, .69, 0], [s * .16, .1, .07]], palette.dark, .08);
      line(person, [[s * .23, 1.18, 0], [s * .34, .82, -.05], [s * .24, .76, -.28]], palette.shade, .065);
      box(person, [s * .16, .06, .01], [.17, .12, .32], palette.dark);
    }
  }
  function crate(parent, x, y, z, size) {
    box(parent, [x, y, z], [size, size * .62, size * .74], palette.wood);
    for (let i = 0; i < 3; i++) box(parent, [x, y + size * (-.22 + i * .21), z + size * .38], [size * .98, size * .075, .02], palette.shade);
    box(parent, [x, y + size * .33, z], [size * .79, .035, size * .53], palette.soil);
  }
  function house(parent, x, z, width, height, roofColor) {
    const d = width * .92;
    box(parent, [x, height / 2, z], [width, height, d], palette.wall);
    box(parent, [x, .015, z], [width + .2, .08, d + .2], palette.shade);
    // Gabled roof made of two sloped panels, with visible eaves.
    const pitch = .58, panel = Math.sqrt((width * .56) ** 2 + pitch ** 2);
    for (const s of [-1, 1]) { const r = box(parent, [x + s * width * .28, height + pitch / 2, z], [panel, .095, d + .28], roofColor); r.rotation.z = -s * Math.atan2(pitch, width * .56); r.renderOrder = 5; }
    box(parent, [x -.24 * width, height * .32, z + d / 2 + .012], [width * .23, height * .64, .055], palette.dark);
    box(parent, [x + .23 * width, height * .63, z + d / 2 + .025], [width * .27, height * .28, .06], palette.blue);
    line(parent, [[x + .23 * width, height * .48, z + d / 2 + .063], [x + .23 * width, height * .78, z + d / 2 + .063]], palette.shade, .02);
  }
  const kit = { palette, group, box, cylinder, cone, sphere, line, arrow, plant, person, crate, house };
  const builders = { 'food-delivery': food, 'living-soil': soil, 'shared-workshop': workshop };
  if (!builders[id]) throw new Error(`Unknown scene: ${id}`);
  const pins = builders[id](kit);
  const extent = id === 'food-delivery' ? 9.9 : 8.9;
  const camera = new THREE.OrthographicCamera(-extent, extent, extent * .53, -extent * .53, .1, 100);
  const target = new THREE.Vector3(0, id === 'living-soil' ? 1.35 : .95, 0);
  function setView(angle = 0, view = 'illustration') {
    const a = .73 + angle, radius = 18;
    const framing = extent * (view === 'top' ? 1.2 : 1);
    camera.left = -framing; camera.right = framing; camera.top = framing * .53; camera.bottom = -framing * .53;
    camera.position.set(Math.sin(a) * radius, view === 'top' ? 23 : view === 'front' ? 6.8 : 14, Math.cos(a) * radius);
    camera.lookAt(target); camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  }
  setView();
  scene.updateMatrixWorld(true);
  // Focus uses tone as an addition to a selected button and descriptive text.
  for (const g of groups) g.traverse(object => {
    if (!object.isMesh) return;
    for (const m of (Array.isArray(object.material) ? object.material : [object.material])) m.userData.original = m.color.clone();
  });
  function focus(id) {
    for (const g of groups) g.traverse(object => {
      if (!object.isMesh) return;
      for (const m of (Array.isArray(object.material) ? object.material : [object.material])) {
        m.color.copy(m.userData.original);
        if (id !== 'all' && g.userData.role !== id) m.color.lerp(new THREE.Color(palette.floor), .6);
      }
    });
  }
  function dispose() {
    scene.traverse(object => {
      object.geometry?.dispose();
      for (const m of (Array.isArray(object.material) ? object.material : object.material ? [object.material] : [])) m.dispose();
    });
  }
  return { scene, camera, pins, palette, setView, focus, dispose };
}

export function projectPins(model, width = 960, height = 510) {
  return model.pins.map(pin => {
    const v = new THREE.Vector3(...pin.point).project(model.camera);
    return { number: pin.number, x: (v.x + 1) * width / 2, y: (1 - v.y) * height / 2 };
  });
}
