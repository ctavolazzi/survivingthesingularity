import assert from 'node:assert/strict';
import { writeFile, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';
import { sceneCatalog, sceneIds } from '../../../src/lib/bookScenes/catalog.js';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const OUT = resolve(ROOT, 'docs/v0.10.2/reader-proof');
const base = process.env.SCENE_PROOF_URL || 'http://127.0.0.1:5190';
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const result = { base, browser: 'Installed Chrome, local macOS', viewport: [1280, 1600], scenes: [], fallback: {}, continuous: {}, mobile: {}, negative_controls: [] };
const browser = await chromium.launch({ channel: 'chrome', headless: true });
async function unlock(page, path) {
  await page.goto(base + path); await page.waitForLoadState('networkidle');
  // Existing development-only in-memory gate, unchanged by this feature.
  await page.evaluate(async () => { const { bookUnlocked } = await import('/src/lib/stores/bookAccess.js'); bookUnlocked.set(true); });
  await page.locator('.gate-form').waitFor({ state: 'detached' });
  const consent = page.getByRole('button', { name: 'I have read and agree to the Terms, Disclaimer, and Privacy', exact: true });
  if (await consent.isVisible()) await consent.click();
}
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 1600 } });
  const pageErrors = []; page.on('pageerror', e => pageErrors.push(e.message));
  for (const id of sceneIds) {
    const data = sceneCatalog[id];
    await unlock(page, '/book/' + data.chapter);
    const figure = page.locator(`[data-book-scene="${id}"]`);
    await figure.waitFor(); await figure.scrollIntoViewIfNeeded();
    assert.equal(await figure.locator('img').count(), 1, 'Only one fallback image belongs to each figure');
    assert.equal(await figure.locator('canvas').count(), 0, 'No GPU context before reader asks');
    const resourcesBefore = await page.evaluate(() => performance.getEntriesByType('resource').filter(e => /bookScenes\/runtime|three\.js|three\.module/.test(e.name)).map(e => e.name));
    assert.deepEqual(resourcesBefore, [], 'Three must not load eagerly');
    await figure.screenshot({ path: resolve(OUT, `${id}-reader-still.png`) });
    await page.evaluate(() => {
      window.__sceneDrawCalls = 0;
      for (const name of ['drawElements', 'drawArrays']) {
        const original = WebGL2RenderingContext.prototype[name];
        WebGL2RenderingContext.prototype[name] = function (...args) { window.__sceneDrawCalls++; return original.apply(this, args); };
      }
    });
    const open = figure.getByRole('button', { name: 'Explore in 3D' });
    await open.focus(); await page.keyboard.press('Enter');
    await figure.locator('[data-scene-state="webgl"] canvas').waitFor();
    await page.waitForTimeout(300);
    const context = await figure.locator('canvas').evaluate(canvas => {
      const gl = canvas.getContext('webgl2'); return { version: gl.getParameter(gl.VERSION), width: canvas.width, height: canvas.height, drawCalls: window.__sceneDrawCalls };
    });
    assert.match(context.version, /WebGL 2/); assert.ok(context.width > 0 && context.height > 0); assert.ok(context.drawCalls > 30);
    const stillCalls = await page.evaluate(() => window.__sceneDrawCalls); await page.waitForTimeout(250);
    assert.equal(await page.evaluate(() => window.__sceneDrawCalls), stillCalls, 'No continuous render loop');
    const annotationBounds = await figure.locator('.scene-annotations').evaluate(svg => [...svg.querySelectorAll('text')].filter(el => { const b = el.getBBox(); return b.x < 0 || b.y < 0 || b.x + b.width > 960 || b.y + b.height > 800; }).map(el => el.textContent));
    assert.deepEqual(annotationBounds, [], 'Live annotations fit the same bounds as the still');
    const original = await figure.locator('.scene-presentation').screenshot();
    await figure.screenshot({ path: resolve(OUT, `${id}-reader-3d.png`) });
    await figure.getByRole('button', { name: 'Rotate view right' }).click();
    const rotated = await figure.locator('.scene-presentation').screenshot();
    assert.notEqual(digest(original), digest(rotated), 'Rotation must change the rendered view');
    const option = data.options[2];
    await figure.getByRole('button', { name: option.label, exact: true }).click();
    assert.equal(await figure.getByRole('button', { name: option.label, exact: true }).getAttribute('aria-pressed'), 'true');
    assert.equal(await figure.locator('.scene-explanation').textContent(), option.text);
    await figure.getByRole('button', { name: 'View from above', exact: true }).click();
    await figure.screenshot({ path: resolve(OUT, `${id}-reader-selected.png`) });
    await figure.getByRole('button', { name: 'Reset view', exact: true }).click();
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.tagName), 'SUMMARY', 'Tab exits camera controls without a trap');
    await figure.getByRole('button', { name: 'Use still illustration', exact: true }).click();
    assert.equal(await figure.locator('canvas').count(), 0, 'Closing frees the GPU canvas');
    assert.equal(await figure.locator('.scene-still').evaluate(el => getComputedStyle(el).visibility), 'visible');
    await figure.locator('summary').click(); assert.equal(await figure.locator('tbody tr').count(), 4);
    result.scenes.push({ id, context, no_eager_three: true, no_animation_loop: true, keyboard_open: true, camera_changes_pixels: true, selection_description_matches: true, static_restored: true, accessible_rows: 4 });
  }
  const lostFigure = page.locator('[data-book-scene="shared-workshop"]');
  await lostFigure.locator('summary').click();
  await lostFigure.getByRole('button', { name: 'Explore in 3D' }).click();
  await lostFigure.locator('canvas').waitFor();
  await lostFigure.locator('canvas').evaluate(canvas => canvas.getContext('webgl2').getExtension('WEBGL_lose_context').loseContext());
  await lostFigure.locator('[data-scene-state="fallback"]').waitFor();
  assert.equal(await lostFigure.locator('canvas').count(), 0);
  await lostFigure.screenshot({ path: resolve(OUT, 'webgl-context-lost-fallback.png') });
  result.context_lost = { deliberately_lost_context: true, still_restored: true };
  result.negative_controls.push('Lost an active WebGL context deliberately; still restored and canvas disposed.');
  // Deliberately deny WebGL. The complete illustration and text must survive.
  const fallback = await browser.newContext({ viewport: { width: 1280, height: 1600 }, reducedMotion: 'reduce' });
  await fallback.addInitScript(() => {
    const getContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (kind, ...args) { if (kind === 'webgl2' || kind === 'webgl') return null; return getContext.call(this, kind, ...args); };
  });
  const fallbackPage = await fallback.newPage(); await unlock(fallbackPage, '/book/chapter9');
  const fallbackFigure = fallbackPage.locator('[data-book-scene="food-delivery"]');
  await fallbackFigure.getByRole('button', { name: 'Explore in 3D' }).click();
  await fallbackFigure.locator('[data-scene-state="fallback"]').waitFor();
  assert.equal(await fallbackFigure.locator('canvas').count(), 0);
  assert.equal(await fallbackFigure.locator('img').evaluate(el => getComputedStyle(el).visibility), 'visible');
  assert.match(await fallbackFigure.locator('[role="status"]').textContent(), /isn’t available/);
  await fallbackFigure.screenshot({ path: resolve(OUT, 'webgl-unavailable-fallback.png') });
  result.fallback = { deliberately_denied_webgl: true, still_visible: true, explanatory_status: true };
  result.negative_controls.push('WebGL denied deliberately; still and text remain usable.');
  await fallback.close();
  // Small-screen layout and a real reduced-motion context.
  const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  const smallPage = await mobile.newPage(); await unlock(smallPage, '/book/chapter15');
  const small = smallPage.locator('[data-book-scene="living-soil"]');
  await small.getByRole('button', { name: 'Explore in 3D' }).click(); await small.locator('canvas').waitFor();
  await smallPage.setViewportSize({ width: 390, height: 2400 });
  await small.scrollIntoViewIfNeeded();
  await small.screenshot({ path: resolve(OUT, 'mobile-reduced-motion-3d.png') });
  await smallPage.setViewportSize({ width: 390, height: 844 });
  const smallCheck = await small.evaluate(el => ({ width: el.getBoundingClientRect().width, viewport: innerWidth, overflow: el.scrollWidth > el.clientWidth, animations: el.getAnimations({subtree:true}).length, targets: [...el.querySelectorAll('button')].map(b => b.getBoundingClientRect().height) }));
  assert.equal(smallCheck.overflow, false); assert.equal(smallCheck.animations, 0); assert.ok(smallCheck.targets.every(h => h >= 44));
  result.mobile = smallCheck; await mobile.close();
  // Continuous reader must enhance the same ordinary source figure once.
  await unlock(page, '/read');
  await page.getByRole('button', { name: 'Chapters', exact: true }).first().click();
  await page.getByRole('button', { name: /Chapter 9:/ }).first().click();
  const continuous = page.locator('[data-book-scene="food-delivery"]');
  await continuous.waitFor(); await continuous.scrollIntoViewIfNeeded();
  assert.equal(await continuous.count(), 1);
  await continuous.getByRole('button', { name: 'Explore in 3D' }).click(); await continuous.locator('canvas').waitFor();
  await continuous.screenshot({ path: resolve(OUT, 'continuous-reader-3d.png') });
  result.continuous = { chapter9_mounted: true, figure_count: 1, webgl: true };
  assert.deepEqual(pageErrors, []); result.page_errors = pageErrors;
} finally { await browser.close(); }
await writeFile(resolve(OUT, 'browser-proof.json'), JSON.stringify(result, null, 2) + '\n');
console.log('Actual chapter and continuous-reader controls, WebGL, lazy loading, fallback, mobile, and reduced-motion proof passed.');
