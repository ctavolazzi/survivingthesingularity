// Layout-level comparison of two builds, immune to sub-pixel text rasterization.
// For each page and width: every element's box (to 0.01px, in document
// coordinates) and the computed styles that decide how it looks, before vs after.
// Usage: [BEFORE=url AFTER=url PAGES='/a /b'] node probe_geometry.mjs OUT_JSON [--control]
//   --control narrows one element by 3px in the AFTER page to prove a layout
//   change is reported.
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const OUT = process.argv[2];
const CONTROL = process.argv.includes('--control');
const PAGES = CONTROL ? ['/about'] : (process.env.PAGES ? process.env.PAGES.split(' ') : ['/blog', '/about', '/factcheck', '/', '/book', '/checklist', '/exclusive-friends-only', '/blog/robot-farm-bot', '/terms', '/early-access']);
const VIEWPORTS = CONTROL ? [{ name: 'phone', width: 390, height: 844 }] : [{ name: 'desktop', width: 1280, height: 800 }, { name: 'phone', width: 390, height: 844 }];
const BUILDS = [['before', process.env.BEFORE || 'http://127.0.0.1:4411'], ['after', process.env.AFTER || 'http://127.0.0.1:4412']];
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const report = [];

async function snapshot(base, path, vp, tamper) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1, timezoneId: 'America/Los_Angeles', reducedMotion: 'no-preference' });
  // Same two controls as the tile capture: no remote images, and every font
  // face loaded before anything is measured. Without them, identical text
  // measured 83.75px wide in one build and 79.36px in the other.
  await ctx.route((url) => !/^(127\.0\.0\.1|localhost)$/.test(url.hostname) && !/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname), (r) => r.abort());
  const page = await ctx.newPage();
  await page.goto(base + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(1500);
  await page.evaluate(async () => { await document.fonts.ready; await Promise.allSettled([...document.fonts].map((f) => f.load())); await document.fonts.ready; });
  await page.waitForTimeout(2000);
  await page.mouse.move(Math.round(vp.width / 2), Math.round(vp.height / 2));
  let last = -1;
  for (let i = 0; i < 200; i++) {                       // down, so every reveal and lazy image fires
    await page.mouse.wheel(0, 600); await page.waitForTimeout(70);
    const y = await page.evaluate(() => Math.max(window.scrollY, document.body.scrollTop, document.documentElement.scrollTop));
    if (y === last && i > 3) break; last = y;
  }
  await page.waitForTimeout(1500);
  for (let i = 0; i < 200 && last > 0; i++) {            // and back to the top
    await page.mouse.wheel(0, -900); await page.waitForTimeout(40);
    last = await page.evaluate(() => Math.max(window.scrollY, document.body.scrollTop, document.documentElement.scrollTop));
  }
  await page.waitForTimeout(1200);
  if (tamper) await page.evaluate(() => { const el = document.querySelector('.about-header'); el.style.width = (el.getBoundingClientRect().width - 3) + 'px'; });
  const rows = await page.evaluate(() => {
    const sx = Math.max(window.scrollX, document.body.scrollLeft), sy = Math.max(window.scrollY, document.body.scrollTop, document.documentElement.scrollTop);
    const r2 = (v) => Math.round(v * 100) / 100;
    const out = [];
    for (const el of document.querySelectorAll('body *')) {
      const tag = el.tagName.toLowerCase();
      if (/^(script|style|noscript|link|meta|template)$/.test(tag)) continue;
      const cs = getComputedStyle(el), r = el.getBoundingClientRect();
      const own = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').slice(0, 24);
      out.push({
        id: tag + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).filter((c) => !/^svelte-|^s-/.test(c)).join('.') : ''),
        text: own, box: [r2(r.x + sx), r2(r.y + sy), r2(r.width), r2(r.height)].join(' '),
        look: [cs.display, cs.visibility, cs.opacity, cs.color, cs.backgroundColor, cs.fontFamily.slice(0, 18), cs.fontSize, cs.fontWeight, cs.lineHeight, cs.letterSpacing, cs.textDecorationLine, cs.borderTopWidth, cs.borderRadius, cs.transform, cs.zIndex, cs.position].join('|'),
      });
    }
    return out;
  });
  await ctx.close();
  return rows;
}

for (const vp of VIEWPORTS) for (const path of PAGES) {
  const b = await snapshot(BUILDS[0][1], path, vp, false);
  const a = await snapshot(BUILDS[1][1], path, vp, CONTROL);
  const rec = { path, viewport: vp.name, elementsBefore: b.length, elementsAfter: a.length, structure: 0, text: [], box: [], look: [] };
  const n = Math.min(b.length, a.length);
  for (let i = 0; i < n; i++) {
    if (b[i].id !== a[i].id) { rec.structure++; continue; }
    if (b[i].text !== a[i].text) rec.text.push(`${b[i].id}: "${b[i].text}" -> "${a[i].text}"`);
    if (b[i].box !== a[i].box) rec.box.push(`${b[i].id} "${b[i].text}": ${b[i].box} -> ${a[i].box}`);
    if (b[i].look !== a[i].look) rec.look.push(`${b[i].id} "${b[i].text}": ${b[i].look} -> ${a[i].look}`);
  }
  report.push(rec);
  console.log(`${vp.name.padEnd(8)} ${path.padEnd(26)} elements ${b.length}/${a.length}  structure diffs ${rec.structure}  text ${rec.text.length}  box ${rec.box.length}  look ${rec.look.length}`);
}
await browser.close();
writeFileSync(OUT, JSON.stringify(report, null, 1));
