import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { marked } from 'marked';
import { sceneCatalog, sceneIds } from '../../../src/lib/bookScenes/catalog.js';

const base = 'http://127.0.0.1:5191';
const output = 'docs/v0.10.3/reader-proof';
const registryBytes = await readFile('src/lib/data/book/visuals.json');
const registry = JSON.parse(registryBytes);
const manifestBytes = await readFile('src/lib/data/book/book.json');
const manifest = JSON.parse(manifestBytes);
const allNames = Object.keys(registry.images);
const newNames = allNames.filter(name => name.startsWith('v103-'));
assert.equal(allNames.length, 62);
assert.equal(newNames.length, 8);
const sources = {};
for (const section of manifest.sections) {
  const text = await readFile(`src/lib/data/book/${section.file}`, 'utf8');
  for (const match of text.matchAll(/!\[([^\]]*)\]\(\/book-images\/([^)]+)\)\s*\n\s*\*([^\n]+)\*/g)) {
    if (registry.images[match[2]]) sources[match[2]] = { ...section, alt: match[1], caption: match[3], source_sha256: createHash('sha256').update(text).digest('hex') };
  }
}
assert.deepEqual(allNames.filter(name => !sources[name]), []);

const report = {
  base, version: manifest.version, registry_entries: allNames.length, new_figures: newNames.length,
  registry_sha256: createHash('sha256').update(registryBytes).digest('hex'),
  manifest_sha256: createHash('sha256').update(manifestBytes).digest('hex'),
  viewports: {}, negative_controls: {}, page_errors: [], console_errors: [], console_warnings: [], failed_requests: [], http_errors: [],
  scope: 'Live Vite reader pages in Chromium at 390px and 1280px, reduced motion. All 62 registered figures checked in /read; all eight new figures additionally checked in individual chapter routes. Three retained scene illustrations verified as stills with usable text details. This does not exercise 3D WebGL interaction, physical printing, an e-reader, or a deployed production server.'
};
const browser = await chromium.launch({ channel: 'chrome', headless: true });

async function unlock(page, path) {
  await page.goto(base + path);
  await page.waitForLoadState('networkidle');
  await page.evaluate(async () => { const { bookUnlocked } = await import('/src/lib/stores/bookAccess.js'); bookUnlocked.set(true); });
  await page.locator('.gate-form').waitFor({ state: 'detached' });
  const consent = page.getByRole('button', { name: 'I have read and agree to the Terms, Disclaimer, and Privacy', exact: true });
  if (await consent.isVisible()) await consent.click();
}

async function measure(image) {
  return image.evaluate(element => {
    const figure = element.closest('figure');
    const caption = figure?.querySelector('figcaption');
    const frame = figure?.getBoundingClientRect();
    const box = element.getBoundingClientRect();
    const captionBox = caption?.getBoundingClientRect();
    return {
      src: element.getAttribute('src'), alt: element.alt, caption: caption?.textContent.trim(),
      caption_links: [...(caption?.querySelectorAll('a') || [])].map(link => ({ text: link.textContent, href: link.getAttribute('href') })),
      loaded: element.complete && element.naturalWidth > 0,
      natural: [element.naturalWidth, element.naturalHeight],
      attributes: [Number(element.getAttribute('width')), Number(element.getAttribute('height'))],
      image: box.toJSON(), figure: frame?.toJSON(), caption_box: captionBox?.toJSON(),
      image_inside_viewport: box.left >= -.5 && box.right <= innerWidth + .5,
      figure_inside_viewport: frame && frame.left >= -.5 && frame.right <= innerWidth + .5,
      figure_horizontal_overflow: figure && figure.scrollWidth > figure.clientWidth + 1,
      page_horizontal_overflow: document.documentElement.scrollWidth > innerWidth + 1,
      aspect_error: Math.abs(box.width / box.height - element.naturalWidth / element.naturalHeight),
      caption_inside_figure: captionBox && captionBox.left >= frame.left - .5 && captionBox.right <= frame.right + .5 && captionBox.bottom <= frame.bottom + .5,
      caption_visible: !!caption && getComputedStyle(caption).display !== 'none' && getComputedStyle(caption).visibility !== 'hidden' && captionBox.height > 0,
    };
  });
}

function check(metrics, name) {
  assert.equal(metrics.loaded, true, `${name}: loaded`);
  assert.equal(metrics.alt, sources[name].alt, `${name}: canonical alt`);
  assert.equal(metrics.caption, sources[name].caption_text, `${name}: complete canonical caption`);
  assert.deepEqual(metrics.caption_links, sources[name].caption_links, `${name}: canonical caption links`);
  assert.equal(metrics.image_inside_viewport, true, `${name}: image bounds`);
  assert.equal(metrics.figure_inside_viewport, true, `${name}: figure bounds`);
  assert.equal(metrics.figure_horizontal_overflow, false, `${name}: figure overflow`);
  assert.equal(metrics.page_horizontal_overflow, false, `${name}: document overflow`);
  assert.ok(metrics.aspect_error < .02, `${name}: undistorted intrinsic aspect ratio`);
  assert.equal(metrics.caption_inside_figure, true, `${name}: caption bounds`);
  assert.equal(metrics.caption_visible, true, `${name}: caption visible`);
  assert.deepEqual(metrics.attributes, registry.images[name].pixels, `${name}: reserved dimensions`);
}

async function inspect(page, name, capture) {
  const image = page.locator(`img[src="/book-images/${name}"]`).first();
  await image.scrollIntoViewIfNeeded();
  await image.evaluate(async element => { if (!element.complete) await element.decode(); });
  const result = await measure(image);
  check(result, name);
  if (capture) await image.locator('xpath=ancestor::figure[1]').screenshot({ path: `${output}/${capture}` });
  return result;
}

try {
  for (const width of [390, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: width === 390 ? 844 : 1000 }, reducedMotion: 'reduce' });
    page.on('pageerror', error => report.page_errors.push({ width, message: error.message }));
    page.on('console', message => {
      if (message.type() === 'error') report.console_errors.push({ width, message: message.text() });
      if (message.type() === 'warning') report.console_warnings.push({ width, message: message.text() });
    });
    page.on('requestfailed', request => report.failed_requests.push({ width, url: request.url(), failure: request.failure()?.errorText }));
    page.on('response', response => { if (response.status() >= 400) report.http_errors.push({ width, url: response.url(), status: response.status() }); });
    const result = { continuous_reader: {}, chapter_reader: {}, scenes: {}, urls: [base + '/read'] };
    report.viewports[width] = result;
    await unlock(page, '/read');
    for (const name of allNames) {
      const expected = await page.evaluate(html => {
        const doc = new DOMParser().parseFromString(html, 'text/html');
        return { caption_text: doc.body.textContent.trim(), caption_links: [...doc.querySelectorAll('a')].map(link => ({ text: link.textContent, href: link.getAttribute('href') })) };
      }, marked.parseInline(sources[name].caption));
      Object.assign(sources[name], expected);
    }
    await page.getByRole('button', { name: 'Chapters', exact: true }).click();
    const last = manifest.sections.at(-1);
    await page.locator('#reader-toc').getByRole('button', { name: new RegExp('^' + last.title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')) }).click();
    await page.locator(`#s-${last.id}`).waitFor();
    result.mounted_sections = await page.locator('main.prose-wrap > section.section').count();
    assert.equal(result.mounted_sections, manifest.sections.length);

    if (width === 390) {
      const name = newNames[0];
      const image = page.locator(`img[src="/book-images/${name}"]`).first();
      await image.scrollIntoViewIfNeeded();
      await image.evaluate(async element => { if (!element.complete) await element.decode(); });
      const mutations = {
        horizontal_overflow: el => { el.style.width = '1400px'; el.style.maxWidth = 'none'; },
        distorted_aspect: el => { el.style.height = '30px'; },
        missing_caption: el => { el.closest('figure').querySelector('figcaption').style.display = 'none'; },
        missing_alt: el => { el.alt = ''; },
      };
      for (const [control, mutate] of Object.entries(mutations)) {
        const restore = await image.evaluate(el => ({ style: el.getAttribute('style'), alt: el.alt, captionStyle: el.closest('figure').querySelector('figcaption').getAttribute('style') }));
        await image.evaluate(mutate);
        const metrics = await measure(image);
        assert.throws(() => check(metrics, name), assert.AssertionError, `${control}: must fail`);
        const expected = { horizontal_overflow: !metrics.image_inside_viewport, distorted_aspect: metrics.aspect_error >= .02, missing_caption: !metrics.caption_visible, missing_alt: metrics.alt === '' };
        assert.equal(expected[control], true, `${control}: intended failure observed`);
        report.negative_controls[control] = { rejected: true, intended_failure_observed: true };
        await image.evaluate((el, saved) => { saved.style === null ? el.removeAttribute('style') : el.setAttribute('style', saved.style); el.alt = saved.alt; const cap = el.closest('figure').querySelector('figcaption'); saved.captionStyle === null ? cap.removeAttribute('style') : cap.setAttribute('style', saved.captionStyle); }, restore);
      }
      check(await measure(image), name);
    }

    for (const name of allNames) {
      result.continuous_reader[name] = await inspect(page, name, newNames.includes(name) ? `continuous-${width}-${name.replace(/\.(svg|png)$/, '.png')}` : null);
    }
    for (const id of sceneIds) {
      const scene = page.locator(`[data-book-scene="${id}"]`);
      await scene.scrollIntoViewIfNeeded();
      assert.equal(await scene.locator('[data-scene-state]').getAttribute('data-scene-state'), 'still');
      assert.equal(await scene.locator('canvas').count(), 0);
      assert.equal(await scene.getByRole('button', { name: 'Explore in 3D', exact: true }).getAttribute('aria-expanded'), 'false');
      await scene.locator('summary').click();
      assert.equal(await scene.locator('tbody tr').count(), 4);
      assert.equal(await scene.locator('details').getAttribute('open'), '');
      assert.equal(await scene.locator('details > p').innerText(), sceneCatalog[id].description);
      await scene.screenshot({ path: `${output}/scene-${width}-${id}-still.png` });
      result.scenes[id] = { reduced_motion: true, state: 'still', no_canvas: true, complete_caption: true, text_details_open: true, text_rows: 4 };
      await scene.locator('summary').click();
    }

    for (const name of newNames) {
      const route = `/book/${sources[name].id}`;
      await unlock(page, route);
      result.urls.push(base + route);
      result.chapter_reader[name] = await inspect(page, name, `chapter-${width}-${name.replace(/\.(svg|png)$/, '.png')}`);
    }
    await page.close();
  }
  report.unexpected_console_warnings = report.console_warnings.filter(({ message }) => !/^<(Layout|Page)> was created with unknown prop 'params'$/.test(message));
  assert.deepEqual(report.page_errors, []);
  assert.deepEqual(report.console_errors, []);
  assert.deepEqual(report.unexpected_console_warnings, []);
  assert.deepEqual(report.failed_requests, []);
  assert.deepEqual(report.http_errors, []);
  report.passed = true;
} finally {
  await browser.close();
  await writeFile(`${output}/reader-smoke.json`, JSON.stringify(report, null, 2) + '\n');
}
console.log(JSON.stringify({ passed: report.passed, continuous_figures: 124, individual_new_figures: 16, scene_still_checks: 6, negative_controls: Object.keys(report.negative_controls).length, captures: 38 }));
