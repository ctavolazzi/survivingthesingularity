import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
import { sceneCatalog, sceneIds } from '../../../src/lib/bookScenes/catalog.js';

const base = 'http://127.0.0.1:5191';
const output = 'docs/v0.10.3/reader-proof';
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const result = { base, reduced_motion: true, scenes: [], note: 'Each detail row is separately scrolled into the real reading viewport and checked. Viewport captures supplement the larger element captures, whose content can be clipped by the continuous reader scrolling container.' };
try {
  for (const width of [390, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 844 }, reducedMotion: 'reduce' });
    await page.goto(base + '/read');
    await page.waitForLoadState('networkidle');
    await page.evaluate(async () => { const { bookUnlocked } = await import('/src/lib/stores/bookAccess.js'); bookUnlocked.set(true); });
    await page.locator('.gate-form').waitFor({ state: 'detached' });
    const consent = page.getByRole('button', { name: 'I have read and agree to the Terms, Disclaimer, and Privacy', exact: true });
    if (await consent.isVisible()) await consent.click();
    await page.getByRole('button', { name: 'Chapters', exact: true }).click();
    await page.locator('#reader-toc').getByRole('button', { name: /^Appendix H:/ }).click();
    for (const id of sceneIds) {
      const scene = page.locator(`[data-book-scene="${id}"]`);
      const image = scene.locator('img');
      await image.scrollIntoViewIfNeeded();
      await image.evaluate(async el => { if (!el.complete) await el.decode(); });
      assert.equal(await scene.locator('[data-scene-state]').getAttribute('data-scene-state'), 'still');
      assert.equal(await scene.locator('canvas').count(), 0);
      await image.screenshot({ path: `${output}/scene-${width}-${id}-image.png` });
      await scene.locator('summary').click();
      const rows = scene.locator('tbody tr');
      const checks = [];
      for (let index = 0; index < 4; index++) {
        const row = rows.nth(index);
        await row.scrollIntoViewIfNeeded();
        const state = await row.evaluate(el => {
          const box = el.getBoundingClientRect();
          return { text: [...el.children].map(cell => cell.textContent), box: box.toJSON(), visible: box.top >= 56 && box.bottom <= innerHeight + 1 && box.left >= 0 && box.right <= innerWidth + 1 };
        });
        assert.deepEqual(state.text, sceneCatalog[id].rows[index]);
        assert.equal(state.visible, true, `${id} row ${index} is visible within viewport`);
        checks.push(state);
      }
      await page.screenshot({ path: `${output}/scene-${width}-${id}-details-viewport.png` });
      result.scenes.push({ id, width, still: true, rows: checks });
      await scene.locator('summary').click();
    }
    await page.close();
  }
  result.passed = true;
} finally {
  await browser.close();
  await writeFile(`${output}/scene-details.json`, JSON.stringify(result, null, 2) + '\n');
}
console.log(JSON.stringify({ passed: result.passed, scene_views: result.scenes.length, visible_rows: result.scenes.reduce((sum, scene) => sum + scene.rows.length, 0) }));
