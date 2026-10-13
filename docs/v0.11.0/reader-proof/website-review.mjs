import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { marked } from 'marked';
import { BOOK_ACCESS_PASSWORD } from '../../../src/lib/bookAccessCode.js';
import { expandRefs } from '../../../src/lib/bookManifest.js';

const base = 'http://127.0.0.1:5193';
const output = 'docs/v0.11.0/reader-proof';
const normalize = value => value.replace(/\s+/g, ' ').trim();
const hash = value => createHash('sha256').update(value).digest('hex');
const homeSource = await readFile('src/routes/+page.svelte', 'utf8');
const homeHtml = homeSource.match(/<section class="reality-section"[\s\S]*?<\/section>/)?.[0];
assert.ok(homeHtml, 'canonical changed landing section exists');
const manifest = JSON.parse(await readFile('src/lib/data/book/book.json', 'utf8'));
const targets = [
  { id: 'chapter6', file: '08-chapter6.md', heading: 'Whose robots?' },
  { id: 'conclusion', file: '21-conclusion.md', heading: 'A future called solarpunk' },
  { id: 'chapter19', file: '27-chapter19.md', heading: 'Get involved' },
];
const report = {
  base, source_version: manifest.version, released_version: manifest.released,
  scope: 'Landing revision and three new manuscript sections at 390px and 1280px. Real gate interaction, canonical text, horizontal bounds, and readable paragraph sizing checked. Browser DOM mutations prove missing text and overflow detection.',
  home_sha256: hash(homeSource), checks: [], negative_controls: {}, page_errors: [],
};
const browser = await chromium.launch({ channel: 'chrome', headless: true });

async function htmlText(page, html) {
  return page.evaluate(value => new DOMParser().parseFromString(value, 'text/html').body.textContent, html);
}

async function measure(locator) {
  return locator.evaluate(el => {
    const rect = el.getBoundingClientRect();
    const nodes = [el, ...el.querySelectorAll('h1,h2,h3,p,li')];
    return {
      text: el.textContent,
      box: rect.toJSON(),
      horizontal_overflow: document.documentElement.scrollWidth > innerWidth + 1,
      outside_horizontal_bounds: nodes.filter(node => {
        const box = node.getBoundingClientRect();
        return box.width && (box.left < -1 || box.right > innerWidth + 1);
      }).map(node => ({ tag: node.tagName, text: node.textContent.slice(0, 80) })),
    };
  });
}

function checkBounds(state) {
  assert.equal(state.horizontal_overflow, false, 'document fits viewport width');
  assert.deepEqual(state.outside_horizontal_bounds, [], 'prose stays within horizontal bounds');
}

async function unlock(page) {
  await page.locator('.gate-form').waitFor();
  if (!report.negative_controls.invalid_password) {
    await page.locator('input[type=password]').fill('proof-invalid-password');
    await page.getByRole('button', { name: 'Unlock', exact: true }).click();
    await page.getByRole('alert').filter({ hasText: 'Incorrect password.' }).waitFor();
    report.negative_controls.invalid_password = { rejected: true };
  }
  await page.locator('input[type=password]').fill(BOOK_ACCESS_PASSWORD);
  await page.getByRole('button', { name: 'Unlock', exact: true }).click();
  await page.locator('.gate-form').waitFor({ state: 'detached' });
  await dismissConsent(page);
}

async function dismissConsent(page) {
  const consent = page.getByRole('button', { name: 'I have read and agree to the Terms, Disclaimer, and Privacy', exact: true });
  if (await consent.isVisible()) await consent.click();
  else {
    const visibleLabel = page.getByRole('button', { name: 'I Agree', exact: true });
    if (await visibleLabel.isVisible()) await visibleLabel.click();
  }
}

async function placeBelowNavigation(locator) {
  await locator.evaluate(el => {
    el.scrollIntoView({ block: 'start' });
    const scroller = document.scrollingElement?.scrollTop ? document.scrollingElement : document.body;
    scroller.scrollTop = Math.max(0, scroller.scrollTop - 130);
  });
}

try {
  for (const width of [390, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 1000 }, reducedMotion: 'reduce' });
    page.on('pageerror', error => report.page_errors.push({ width, message: error.message }));
    await page.goto(base, { waitUntil: 'domcontentloaded' });
    await page.locator('section.reality-section').waitFor();
    await dismissConsent(page);
    await page.evaluate(() => document.fonts.ready);
    const section = page.locator('section.reality-section');
    await section.scrollIntoViewIfNeeded();
    const expected = normalize(await htmlText(page, homeHtml));
    let state = await measure(section);
    assert.equal(normalize(state.text), expected, 'landing matches canonical changed section');
    checkBounds(state);
    if (!report.negative_controls.missing_text) {
      const heading = section.locator('h2');
      const saved = await heading.textContent();
      await heading.evaluate(el => { el.textContent = 'The revision is missing.'; });
      state = await measure(section);
      assert.throws(() => assert.equal(normalize(state.text), expected), assert.AssertionError);
      report.negative_controls.missing_text = { rejected: true, intended_failure_observed: true };
      await heading.evaluate((el, text) => { el.textContent = text; }, saved);
      const savedStyle = await section.getAttribute('style');
      await section.evaluate(el => { el.style.minWidth = `${innerWidth + 320}px`; });
      const wideState = await measure(section);
      assert.throws(() => checkBounds(wideState), assert.AssertionError);
      report.negative_controls.horizontal_overflow = { rejected: true, intended_failure_observed: true };
      await section.evaluate((el, style) => {
        if (style === null) el.removeAttribute('style'); else el.setAttribute('style', style);
      }, savedStyle);
      state = await measure(section);
      checkBounds(state);
    }
    await placeBelowNavigation(section.locator('h2'));
    await page.screenshot({ path: `${output}/landing-${width}-revision.png` });
    await section.locator('.reality-cols').evaluate(el => el.scrollIntoView({ block: 'center' }));
    await page.screenshot({ path: `${output}/landing-${width}-actions.png` });
    await page.screenshot({ path: `${output}/landing-${width}-full.png`, fullPage: true });
    report.checks.push({ kind: 'landing', width, expected, screenshot: `landing-${width}-revision.png`, ...await measure(section) });

    for (const target of targets) {
      const source = await readFile(`src/lib/data/book/${target.file}`, 'utf8');
      const start = source.indexOf(`## ${target.heading}\n`);
      assert.ok(start >= 0, `${target.heading} exists in canonical source`);
      const following = source.indexOf('\n## ', start + 4);
      const insertion = source.slice(start, following < 0 ? source.length : following);
      await page.goto(`${base}/book/${target.id}`, { waitUntil: 'domcontentloaded' });
      await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
      await unlock(page);
      await page.evaluate(() => document.fonts.ready);
      const heading = page.getByRole('heading', { name: target.heading, exact: true });
      await heading.waitFor();
      const actual = await heading.evaluate(el => {
        const blocks = [el];
        let next = el.nextElementSibling;
        while (next && !/^H[12]$/.test(next.tagName)) { blocks.push(next); next = next.nextElementSibling; }
        blocks.forEach((node, index) => node.setAttribute('data-v110-proof', String(index)));
        return blocks.map(node => node.textContent).join(' ');
      });
      const expectedText = normalize(await htmlText(page, marked.parse(expandRefs(manifest, insertion))));
      assert.equal(normalize(actual), expectedText, `${target.id}: canonical section text rendered`);
      const blocks = page.locator('[data-v110-proof]');
      for (const block of await blocks.all()) checkBounds(await measure(block));
      const prose = page.locator('[data-v110-proof="1"]');
      await prose.scrollIntoViewIfNeeded();
      await prose.evaluate(el => el.scrollIntoView({ block: 'center' }));
      const legibility = await prose.evaluate(el => {
        const box = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return { font_px: parseFloat(style.fontSize), line_height: style.lineHeight, fully_in_viewport: box.top >= 0 && box.bottom <= innerHeight + 1, box: box.toJSON() };
      });
      assert.ok(legibility.font_px >= 16, 'body type is at least 16px');
      assert.equal(legibility.fully_in_viewport, true, 'opening paragraph readable in viewport');
      await placeBelowNavigation(heading);
      const screenshot = `${target.id}-${width}-addition.png`;
      await page.screenshot({ path: `${output}/${screenshot}` });
      report.checks.push({ kind: 'reader', route: `/book/${target.id}`, width, file: target.file, source_sha256: hash(source), heading: target.heading, canonical_text_matches: true, paragraph_legibility: legibility, screenshot, paragraph_blocks: await blocks.count() });
    }
    await page.close();
  }
  assert.deepEqual(report.page_errors, []);
  report.passed = true;
} finally {
  await browser.close();
  await writeFile(`${output}/website-review.json`, JSON.stringify(report, null, 2) + '\n');
}
console.log(JSON.stringify({ passed: report.passed, checks: report.checks.length, negative_controls: Object.keys(report.negative_controls), page_errors: report.page_errors.length }));
