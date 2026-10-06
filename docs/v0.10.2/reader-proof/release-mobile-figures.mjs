import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';

const base = 'http://127.0.0.1:5190';
const output = 'docs/v0.10.2/reader-proof';
const registry = JSON.parse(await readFile('src/lib/data/book/visuals.json', 'utf8'));
const result = {
  base, viewport: [390, 844], registry_entries: Object.keys(registry.images).length,
  page_errors: [], console_errors: [], console_warnings: [], failed_requests: [], http_errors: [], figures: {},
};
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' });
  page.on('pageerror', error => result.page_errors.push(error.message));
  page.on('console', message => {
    if (message.type() === 'error') result.console_errors.push(message.text());
    if (message.type() === 'warning') result.console_warnings.push(message.text());
  });
  page.on('requestfailed', request => result.failed_requests.push({ url: request.url(), failure: request.failure()?.errorText }));
  page.on('response', response => { if (response.status() >= 400) result.http_errors.push({ url: response.url(), status: response.status() }); });
  await page.goto(base + '/read');
  await page.waitForLoadState('networkidle');
  await page.evaluate(async () => {
    const { bookUnlocked } = await import('/src/lib/stores/bookAccess.js');
    bookUnlocked.set(true);
  });
  await page.locator('.gate-form').waitFor({ state: 'detached' });
  const consent = page.getByRole('button', { name: 'I have read and agree to the Terms, Disclaimer, and Privacy', exact: true });
  if (await consent.isVisible()) await consent.click();

  for (const [file, chapterName] of [
    ['intro-nine-stages.svg', /^Introduction: The Uncompromising Truth/],
    ['appd-precedent-timeline.svg', /^Appendix D: The Precedent Ledger/],
  ]) {
    // Continuous reading mounts sections progressively. Use its real chapter
    // navigation before looking for a late figure that is not mounted yet.
    await page.getByRole('button', { name: 'Chapters', exact: true }).click();
    await page.locator('#reader-toc').getByRole('button', { name: chapterName }).click();
    const image = page.locator(`img[src="/book-images/${file}"]`).first();
    await image.scrollIntoViewIfNeeded();
    await image.evaluate(async element => { if (!element.complete) await element.decode(); });
    const figure = image.locator('xpath=..');
    assert.equal(await figure.evaluate(element => element.matches('figure.book-figure')), true);
    const metrics = await figure.evaluate(element => {
      const image = element.querySelector('img');
      const figure = element.getBoundingClientRect();
      const box = image.getBoundingClientRect();
      return {
        alt: image.alt, caption: element.querySelector('figcaption')?.textContent.trim(),
        loaded: image.complete && image.naturalWidth > 0,
        natural: [image.naturalWidth, image.naturalHeight],
        attributes: [Number(image.getAttribute('width')), Number(image.getAttribute('height'))],
        image: box.toJSON(), figure: figure.toJSON(),
        viewport_width: innerWidth,
        image_inside_viewport: box.left >= 0 && box.right <= innerWidth,
        figure_inside_viewport: figure.left >= 0 && figure.right <= innerWidth,
        figure_horizontal_overflow: element.scrollWidth > element.clientWidth + 1,
        page_horizontal_overflow: document.documentElement.scrollWidth > innerWidth,
      };
    });
    assert.equal(metrics.loaded, true);
    assert.ok(metrics.alt.length > 25);
    assert.ok(metrics.caption?.length > 25);
    assert.equal(metrics.image_inside_viewport, true);
    assert.equal(metrics.figure_inside_viewport, true);
    assert.equal(metrics.figure_horizontal_overflow, false);
    assert.equal(metrics.page_horizontal_overflow, false);
    assert.deepEqual(metrics.attributes, registry.images[file].pixels);
    await figure.screenshot({ path: `${output}/mobile-release-${file.replace('.svg', '.png')}` });
    result.figures[file] = metrics;
  }
  await page.waitForLoadState('networkidle');
  assert.deepEqual(result.page_errors, []);
  assert.deepEqual(result.console_errors, []);
  result.unexpected_console_warnings = result.console_warnings.filter(message =>
    !/^<(Layout|Page)> was created with unknown prop 'params'$/.test(message));
  assert.deepEqual(result.unexpected_console_warnings, []);
  assert.deepEqual(result.failed_requests, []);
  assert.deepEqual(result.http_errors, []);
} finally {
  await browser.close();
  await writeFile(`${output}/release-mobile-figures.json`, JSON.stringify(result, null, 2) + '\n');
}
console.log(JSON.stringify(result, null, 2));
