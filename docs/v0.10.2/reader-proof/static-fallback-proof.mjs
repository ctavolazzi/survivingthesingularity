import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from 'vite';
import { realpathSync } from 'node:fs';
import { chromium } from '@playwright/test';
import { sceneCatalog, sceneIds } from '../../../src/lib/bookScenes/catalog.js';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const OUT = resolve(ROOT, 'docs/v0.10.2/reader-proof');
const server = await createServer({ root: ROOT, server: { middlewareMode: true, hmr: false, fs: { allow: ['src/lib/data', realpathSync('node_modules')] } }, appType: 'custom' });
let html = '', css = '';
try {
  const { default: BookFigure } = await server.ssrLoadModule('/src/lib/components/interactives/BookFigure.svelte');
  for (const id of sceneIds) {
    const data = sceneCatalog[id];
    const render = BookFigure.render({ id, src: '../../../static/book-images/' + data.file, alt: data.alt, caption: data.caption });
    assert.doesNotMatch(render.html, /<canvas|<button|<script/);
    assert.match(render.html, /<img/); assert.match(render.html, /<details/);
    html += render.html; css = render.css.code;
  }
} finally { await server.close(); }
await writeFile(resolve(OUT, 'static-fallback.html'), `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Scene fallback proof</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{max-width:700px;margin:40px auto;padding:20px;background:#020617;color:#f1f5f9;font-family:Arial,sans-serif}${css}</style></head><body>${html}</body></html>\n`);
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ javaScriptEnabled: false, viewport: { width: 1100, height: 1300 } });
  await page.goto('file://' + resolve(OUT, 'static-fallback.html'));
  assert.equal(await page.locator('[data-book-scene]').count(), sceneIds.length);
  assert.equal(await page.locator('canvas,button').count(), 0);
  const figures = [];
  for (const id of sceneIds) {
    const figure = page.locator(`[data-book-scene="${id}"]`);
    assert.ok(await figure.locator('img').evaluate(el => el.complete && el.naturalWidth === 960));
    await figure.locator('summary').click();
    assert.equal(await figure.locator('tbody tr').count(), 4);
    await figure.screenshot({ path: resolve(OUT, `${id}-no-javascript.png`) });
    figures.push({ id, image_loaded: true, native_details_work: true, table_rows: 4 });
  }
  await writeFile(resolve(OUT, 'static-fallback-proof.json'), JSON.stringify({ javascript: false, component_ssr: true, figures, note: 'The existing full-reader password gate requires JavaScript; this verifies the new components and their offline fallback without changing that gate.' }, null, 2) + '\n');
} finally { await browser.close(); }
console.log('Server-rendered stills, captions, and native text details work with JavaScript disabled.');
