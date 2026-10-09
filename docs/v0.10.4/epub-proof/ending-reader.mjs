import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { marked } from 'marked';

const base = 'http://127.0.0.1:5192';
const output = 'docs/v0.10.4/epub-proof';
const review = JSON.parse(await readFile('docs/v0.10.4/ending-review.json', 'utf8'));
const manifest = JSON.parse(await readFile('src/lib/data/book/book.json', 'utf8'));
const sections = Object.fromEntries(manifest.sections.map(section => [section.file, section]));
const report = {
  version: manifest.version, base, viewports: [390, 1280], measurements: [], captures: [],
  page_errors: [], console_errors: [], http_errors: [], failed_requests: [], negative_controls: [],
  scope: 'Six changed ending passages in individual chapter routes and continuous reader at both widths. Browser text and horizontal-bound checks plus element captures; no dedicated e-reader or physical-device claim.'
};
const browser = await chromium.launch({ channel: 'chrome', headless: true });
report.browser = browser.version();

async function unlock(page, path) {
  await page.goto(base + path, { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    const { bookUnlocked } = await import('/src/lib/stores/bookAccess.js');
    bookUnlocked.set(true);
  });
  await page.locator('.gate-form').waitFor({ state: 'detached' });
  const consent = page.getByRole('button', { name: 'I have read and agree to the Terms, Disclaimer, and Privacy', exact: true });
  if (await consent.isVisible()) await consent.click();
}

async function match(page, scope, text) {
  const index = await page.locator(scope).locator('p, li, h2').evaluateAll((nodes, expected) => {
    const normalize = value => value.normalize('NFKC').replace(/\s+/g, ' ').trim();
    return nodes.findIndex(node => normalize(node.textContent) === normalize(expected));
  }, text);
  assert.ok(index >= 0, `Changed passage not found: ${text}`);
  return page.locator(scope).locator('p, li, h2').nth(index);
}

try {
  for (const width of report.viewports) {
    const page = await browser.newPage({ viewport: { width, height: 1000 }, reducedMotion: 'reduce' });
    page.on('pageerror', error => report.page_errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') report.console_errors.push(message.text()); });
    page.on('requestfailed', request => report.failed_requests.push(request.url()));
    page.on('response', response => { if (response.status() >= 400) report.http_errors.push({ url: response.url(), status: response.status() }); });
    for (const mode of ['chapter', 'continuous']) {
      if (mode === 'continuous') {
        await unlock(page, '/read');
        await page.getByRole('button', { name: 'Chapters', exact: true }).click();
        const last = manifest.sections.at(-1);
        await page.locator('#reader-toc').getByRole('button', { name: new RegExp('^' + last.title) }).click();
        await page.locator(`#s-${last.id}`).waitFor();
      }
      for (const [index, edit] of review.edits.entries()) {
        const section = sections[edit.file.split('/').at(-1)];
        if (mode === 'chapter') await unlock(page, `/book/${section.id}`);
        const expected = await page.evaluate(html => new DOMParser().parseFromString(html, 'text/html').body.textContent.trim(), marked.parse(edit.after));
        const scope = mode === 'chapter' ? 'article' : `#s-${section.id} article`;
        const node = await match(page, scope, expected);
        await node.scrollIntoViewIfNeeded();
        const metrics = await node.evaluate(element => {
          const rect = element.getBoundingClientRect();
          return { text: element.textContent, bounds: rect.toJSON(), viewport: innerWidth,
            horizontal_overflow: rect.left < -.5 || rect.right > innerWidth + .5,
            visible: getComputedStyle(element).visibility !== 'hidden' && rect.width > 0 && rect.height > 0 };
        });
        assert.equal(metrics.horizontal_overflow, false);
        assert.equal(metrics.visible, true);
        if (width === 390 && mode === 'chapter' && index === 0) {
          const original = await node.innerHTML();
          await node.evaluate(element => { element.textContent = 'Deliberately missing expected passage'; });
          await assert.rejects(() => match(page, scope, expected), assert.AssertionError);
          await node.evaluate((element, html) => { element.innerHTML = html; }, original);
          await match(page, scope, expected);
          report.negative_controls.push({ control: 'actual displayed passage replaced', rejected: true, restored: true });
        }
        const capture = `${output}/ending-reader-${mode}-${index + 1}-${width}.png`;
        await node.screenshot({ path: capture });
        report.captures.push({ file: capture, sha256: createHash('sha256').update(await readFile(capture)).digest('hex'), edit: index + 1, mode, width });
        report.measurements.push({ edit: index + 1, file: edit.file, section: section.id, mode, width, ...metrics });
      }
    }
    await page.close();
  }
  for (const key of ['page_errors', 'console_errors', 'http_errors', 'failed_requests']) assert.deepEqual(report[key], []);
  report.status = 'pass';
} finally {
  await browser.close();
  await writeFile(`${output}/ending-reader.json`, JSON.stringify(report, null, 2) + '\n');
}
console.log(JSON.stringify({ status: report.status, measurements: report.measurements.length, captures: report.captures.length, negative_controls: report.negative_controls.length }));
