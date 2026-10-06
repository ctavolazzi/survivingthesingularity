import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';
import { sceneCatalog, sceneIds } from '../../../src/lib/bookScenes/catalog.js';
import { splitBookFigures } from '../../../src/lib/bookScenes/segments.js';
import { createBookScene, projectPins } from '../../../src/lib/bookScenes/geometry.js';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const manifest = JSON.parse(await readFile(resolve(ROOT, 'docs/v0.10.1/scenes/render-manifest.json')));
const placements = JSON.parse(await readFile(resolve(ROOT, 'docs/v0.10.1/scenes/placements.json')));
const results = { inputs: [], scenes: [], negative_controls: [] };
function assertFresh(expected, actual, file) { assert.equal(actual, expected, `Stale scene artifact: ${file}`); }
for (const [file, expected] of Object.entries(manifest.inputs)) { assertFresh(expected, sha(await readFile(resolve(ROOT, file))), file); results.inputs.push(file); }
try { assertFresh('correct-hash', 'changed-artifact', 'deliberate stale artifact'); throw new Error('Gate failed to reject stale artifact'); }
catch (error) { assert.match(error.message, /Stale scene artifact/); results.negative_controls.push('Hash gate rejected a deliberately stale artifact.'); }
// The extraction must leave unknown markers and their original image intact.
const unknown = '<!-- interactive:unknown-scene -->\n\n![preserve me](/book-images/unknown.svg)\n\n*Keep this caption.*';
assert.deepEqual(splitBookFigures(unknown), [{ type: 'markdown', raw: unknown }]);
for (const placement of placements) {
  const book = `Before.\n\n${placement.markdown}\n\nAfter.`;
  const segments = splitBookFigures(book);
  assert.deepEqual(segments.map(s => s.type), ['markdown', 'scene', 'markdown']);
  assert.equal(segments[0].raw, 'Before.\n\n'); assert.equal(segments[2].raw, '\n\nAfter.');
  assert.equal(segments[1].id, placement.id); assert.equal(segments[1].alt, sceneCatalog[placement.id].alt);
  const changedFile = book.replace(sceneCatalog[placement.id].file, 'different-source.svg');
  assert.deepEqual(splitBookFigures(changedFile), [{ type: 'markdown', raw: changedFile }]);
}
results.negative_controls.push('Unknown scene and mismatched still preserve the original Markdown instead of dropping it.');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 960, height: 800 } });
  for (const id of sceneIds) {
    const model = createBookScene(id); let meshes = 0; let triangles = 0;
    model.scene.traverse(object => { if (object.isMesh) { meshes++; triangles += object.geometry.index ? object.geometry.index.count / 3 : object.geometry.attributes.position.count / 3; } });
    assert.ok(meshes > 60, `${id} is not a substantive model`); assert.ok(triangles > 1000);
    for (const pin of projectPins(model)) { assert.ok(pin.x > 15 && pin.x < 945); assert.ok(pin.y > 15 && pin.y < 495); }
    model.setView(Math.PI / 8, 'top');
    for (const pin of projectPins(model)) { assert.ok(Number.isFinite(pin.x) && Number.isFinite(pin.y)); }
    model.dispose();
    const record = manifest.figures[sceneCatalog[id].file];
    const checks = [];
    for (const mode of ['source', 'print']) {
      const file = record[mode], source = await readFile(resolve(ROOT, file), 'utf8');
      assertFresh(record[`${mode}_sha256`], sha(source), file);
      assert.match(source, /data-renderer="Three.js r168 SVGRenderer"/);
      assert.doesNotMatch(source, /<script|<foreignObject|<image|https?:\/\/(?!www\.w3\.org)/);
      await page.setContent(source);
      const check = await page.evaluate(() => {
        const svg = document.querySelector('svg'), texts = [...svg.querySelectorAll('text')];
        const boxes = texts.map(el => { const b = el.getBBox(); return { text: el.textContent, x: b.x, y: b.y, w: b.width, h: b.height, size: Number(el.getAttribute('font-size')) }; });
        return { textCount: boxes.length, outOfBounds: boxes.filter(b => b.x < 0 || b.y < 0 || b.x + b.w > 960 || b.y + b.h > 800), tooSmall: boxes.filter(b => b.size < 24), paths: svg.querySelectorAll('path').length };
      });
      assert.deepEqual(check.outOfBounds, [], `${file}: clipped text`); assert.deepEqual(check.tooSmall, []); assert.ok(check.paths > 50);
      checks.push({ mode, sha256: sha(source), ...check });
    }
    results.scenes.push({ id, meshes, triangles, checks });
  }
} finally { await browser.close(); }
await writeFile(resolve(ROOT, 'docs/v0.10.1/scenes/scene-checks.json'), JSON.stringify(results, null, 2) + '\n');
console.log('Scene source preservation, stale-artifact rejection, substantive geometry, vector exports, and annotation bounds passed.');
