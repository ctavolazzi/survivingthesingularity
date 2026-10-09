import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { marked } from 'marked';

const base = 'http://127.0.0.1:5192';
const output = 'docs/v0.10.4/reader-proof';
const reviewBytes = await readFile('docs/v0.10.4/middle-review.json');
const edits = JSON.parse(reviewBytes).edits;
const manifestBytes = await readFile('src/lib/data/book/book.json');
const manifest = JSON.parse(manifestBytes);
const result = {
  base, version: manifest.version,
  scope: 'Six revised paragraphs in Chapters 6, 7, 9, 10, 12, and 14, compared to canonical revised Markdown in individual chapter routes at 390px and 1280px. Paragraph text, readable viewport placement, and horizontal bounds checked. Existing scenes and artwork retained.',
  review_sha256: createHash('sha256').update(reviewBytes).digest('hex'),
  manifest_sha256: createHash('sha256').update(manifestBytes).digest('hex'),
  checks: [], negative_controls: {}, page_errors: [],
};
const normalize = text => text.replace(/\s+/g, ' ').trim();
const browser = await chromium.launch({ channel: 'chrome', headless: true });
function check(state, expected) {
  assert.equal(normalize(state.text), normalize(expected), 'exact revised paragraph text');
  assert.equal(state.visible, true, 'paragraph readable inside viewport');
  assert.equal(state.horizontal_overflow, false, 'no document horizontal overflow');
}
async function measure(locator) {
  return locator.evaluate(el => {
    const box = el.getBoundingClientRect();
    return {
      text: el.textContent,
      box: box.toJSON(),
      visible: box.top >= 56 && box.bottom <= innerHeight + 1 && box.left >= 0 && box.right <= innerWidth + 1,
      horizontal_overflow: document.documentElement.scrollWidth > innerWidth + 1,
    };
  });
}
try {
  for (const width of [390, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 1000 }, reducedMotion: 'reduce' });
    page.on('pageerror', error => result.page_errors.push({ width, message: error.message }));
    for (const edit of edits) {
      const section = manifest.sections.find(section => section.file === edit.file);
      assert.ok(section, edit.file);
      const route = `/book/${section.id}`;
      await page.goto(base + route);
      await page.waitForLoadState('networkidle');
      await page.evaluate(async () => {
        const { bookUnlocked } = await import('/src/lib/stores/bookAccess.js');
        bookUnlocked.set(true);
      });
      await page.locator('.gate-form').waitFor({ state: 'detached' });
      const consent = page.getByRole('button', { name: 'I have read and agree to the Terms, Disclaimer, and Privacy', exact: true });
      if (await consent.isVisible()) await consent.click();
      const expected = await page.evaluate(html => new DOMParser().parseFromString(html, 'text/html').body.textContent.trim(), marked.parse(edit.after));
      const matched = await page.evaluate(({ expected, id }) => {
        const normalize = text => text.replace(/\s+/g, ' ').trim();
        const matches = [...document.querySelectorAll('main p, main li')].filter(el => normalize(el.textContent) === normalize(expected));
        if (matches.length !== 1) return matches.length;
        matches[0].setAttribute('data-revision-proof', id);
        return matches.length;
      }, { expected, id: section.id });
      assert.equal(matched, 1, `${edit.file}: one canonical paragraph`);
      const paragraph = page.locator(`[data-revision-proof="${section.id}"]`);
      await paragraph.scrollIntoViewIfNeeded();
      await paragraph.evaluate(el => el.scrollIntoView({ block: 'center' }));
      const state = await measure(paragraph);
      check(state, expected);
      if (!result.negative_controls.missing_revised_text) {
        const saved = await paragraph.innerHTML();
        await paragraph.evaluate(el => { el.textContent = 'The revision is missing.'; });
        const mutated = await measure(paragraph);
        assert.throws(() => check(mutated, expected), assert.AssertionError);
        assert.notEqual(normalize(mutated.text), normalize(expected));
        result.negative_controls.missing_revised_text = { rejected: true, intended_failure_observed: true };
        await paragraph.evaluate((el, html) => { el.innerHTML = html; }, saved);
        check(await measure(paragraph), expected);
      }
      const screenshot = `prose-${width}-${section.id}.png`;
      await page.screenshot({ path: `${output}/${screenshot}` });
      result.checks.push({ file: edit.file, route, width, source_sha256: createHash('sha256').update(await readFile(`src/lib/data/book/${edit.file}`)).digest('hex'), expected, screenshot, ...state });
    }
    await page.close();
  }
  assert.deepEqual(result.page_errors, []);
  result.passed = true;
} finally {
  await browser.close();
  await writeFile(`${output}/prose-review.json`, JSON.stringify(result, null, 2) + '\n');
}
console.log(JSON.stringify({ passed: result.passed, paragraphs: edits.length, viewport_checks: result.checks.length, negative_controls: Object.keys(result.negative_controls).length }));
