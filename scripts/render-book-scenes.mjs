#!/usr/bin/env node
/** Deterministic Three.js SVG export. Usage: node scripts/render-book-scenes.mjs [--check] [--proof] */
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { chromium } from '@playwright/test';
import { sceneCatalog, sceneIds } from '../src/lib/bookScenes/catalog.js';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const check = process.argv.includes('--check');
const proof = process.argv.includes('--proof');
const OUT = resolve(ROOT, 'docs/v0.10.1/scenes');
await mkdir(OUT, { recursive: true });
const sha = value => createHash('sha256').update(value).digest('hex');
const html = `<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#020617}svg{display:block}</style><script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js","three/addons/":"/node_modules/three/examples/jsm/"}}</script></head><body><script type="module">import {renderSceneSvg} from '/src/lib/bookScenes/svg.js'; window.renderSceneSvg = renderSceneSvg;</script></body></html>`;
const server = createServer(async (req, res) => {
  if (req.url === '/') { res.setHeader('Content-Type', 'text/html'); res.end(html); return; }
  const path = resolve(ROOT, '.' + decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
  if (!path.startsWith(ROOT + '/')) { res.statusCode = 403; res.end(); return; }
  try { const body = await readFile(path); res.setHeader('Content-Type', ({ '.js': 'text/javascript', '.svg': 'image/svg+xml' })[extname(path)] || 'application/octet-stream'); res.end(body); }
  catch { res.statusCode = 404; res.end(); }
});
await new Promise(ok => server.listen(0, '127.0.0.1', ok));
let browser;
try {
  browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 960, height: 800 }, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:${server.address().port}/`);
  await page.waitForFunction(() => typeof window.renderSceneSvg === 'function');
  const manifest = {
    generator: 'scripts/render-book-scenes.mjs',
    renderer: 'Three.js 0.168.0 SVGRenderer',
    dimensions: [960, 800],
    camera: 'Shared orthographic camera and geometry with live WebGL scene; no clock, randomness, textures, or GPU export.',
    minimum_label_size: 24,
    inputs: {}, figures: {}
  };
  for (const name of ['catalog.js', 'geometry.js', 'svg.js']) manifest.inputs[`src/lib/bookScenes/${name}`] = sha(await readFile(resolve(ROOT, `src/lib/bookScenes/${name}`)));
  for (const id of sceneIds) {
    const record = { id, source: `static/book-images/${sceneCatalog[id].file}`, print: `static/book-images/print/${sceneCatalog[id].file}` };
    for (const theme of ['dark', 'light']) {
      const result = await page.evaluate(({ id, theme }) => window.renderSceneSvg(id, theme), { id, theme });
      const file = record[theme === 'dark' ? 'source' : 'print'];
      const text = '<?xml version="1.0" encoding="UTF-8"?>\n' + result + '\n';
      if (check) {
        if (await readFile(resolve(ROOT, file), 'utf8') !== text) throw new Error(`Stale generated scene: ${file}`);
      } else await writeFile(resolve(ROOT, file), text);
      record[theme === 'dark' ? 'source_sha256' : 'print_sha256'] = sha(text);
      if (proof) {
        await page.evaluate(svg => { document.body.innerHTML = svg; }, result);
        await page.screenshot({ path: resolve(OUT, `${id}-${theme}.png`) });
      }
    }
    manifest.figures[sceneCatalog[id].file] = record;
  }
  if (!check) await writeFile(resolve(OUT, 'render-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  console.log(`${check ? 'Verified' : 'Rendered'} ${sceneIds.length} Three.js scenes in dark and light palettes.`);
} finally { await browser?.close(); await new Promise(ok => server.close(ok)); }
