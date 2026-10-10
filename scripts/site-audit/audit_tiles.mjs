// Screenshot a page as a stack of viewport-sized tiles, scrolling with real
// wheel events between them.
// Usage: [DESKTOP_PAGES='/a /b' PHONE_PAGES='/a'] node audit_tiles.mjs BASE_URL OUT_DIR LABEL
//
// Why not fullPage screenshots: this site scrolls an inner box (html and body
// both set overflow-y:auto), and a fullPage capture painted only the first
// 800px of every page, with blank background below. Two blank halves compare
// as "identical", so that comparison could not see a change below the fold.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [BASE, OUT, LABEL] = process.argv.slice(2);

const DESKTOP = (process.env.DESKTOP_PAGES || '/blog /about /factcheck /').split(' ').filter(Boolean);
const PHONE = (process.env.PHONE_PAGES || '/blog /about /factcheck').split(' ').filter(Boolean);
const PLAN = [
  { vp: { name: 'desktop', width: 1280, height: 800 }, paths: DESKTOP },
  { vp: { name: 'phone', width: 390, height: 844 }, paths: PHONE },
];
const slug = (p) => (p === '/' ? 'home' : p.replace(/^\//, '').replace(/[^a-z0-9]+/gi, '-'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const index = [];

for (const { vp, paths } of PLAN) {
  const context = await browser.newContext({
    viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1,
    timezoneId: 'America/Los_Angeles', reducedMotion: 'no-preference',
  });
  // Remote images and video thumbnails arrive at a different moment on every
  // run and change page height. Block them in BOTH builds so what is compared
  // is markup and CSS, not the network.
  await context.route((url) => !/^(127\.0\.0\.1|localhost)$/.test(url.hostname) && !/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname), (r) => r.abort());
  for (const path of paths) {
    const dir = `${OUT}/${LABEL}/${vp.name}/${slug(path)}`;
    mkdirSync(dir, { recursive: true });
    const page = await context.newPage();
    await page.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(1500);
    // Every declared font face loaded before the first tile: a font that swaps
    // in mid-capture moved three small text runs by a pixel in the first run.
    await page.evaluate(async () => { await document.fonts.ready; await Promise.allSettled([...document.fonts].map((f) => f.load())); await document.fonts.ready; });
    await page.waitForTimeout(2500);
    await page.mouse.move(Math.round(vp.width / 2), Math.round(vp.height / 2));
    const settle = path === '/' ? 1400 : 800;
    const step = vp.height - 220;          // overlap, so the fixed banner never hides a strip for good
    const tiles = [];
    let last = -1;
    for (let i = 0; i < 40; i++) {
      const y = await page.evaluate(() => Math.max(window.scrollY, document.body.scrollTop, document.documentElement.scrollTop));
      if (y === last) break;               // the wheel moved nothing: bottom reached
      last = y;
      // Lazy images are fetched as they near the viewport, and headless Chrome
      // can take a second or two after the bytes arrive to draw them, even when
      // the element already reports complete and decoded. A tile taken in that
      // gap shows an empty box, and whether it does is a coin toss from run to
      // run. So: wait for every image in view to finish loading, then hold the
      // tile until three seconds after the last of them arrived. A blocked image
      // counts as finished.
      await page.evaluate(async () => {
        const inView = [...document.images].filter((img) => {
          const r = img.getBoundingClientRect();
          return r.bottom > 0 && r.top < innerHeight && r.width > 0;
        });
        await Promise.race([
          Promise.allSettled(inView.map((img) => (img.complete ? null : new Promise((res) => {
            img.addEventListener('load', res, { once: true });
            img.addEventListener('error', res, { once: true });
          })))),
          new Promise((res) => setTimeout(res, 6000)),
        ]);
        const arrived = Math.max(0, ...inView.map((img) => {
          const e = performance.getEntriesByName(img.currentSrc || img.src).pop();
          return e ? e.responseEnd : 0;
        }));
        const hold = Math.min(3000, Math.max(0, arrived + 3000 - performance.now()));
        if (hold > 0) await new Promise((res) => setTimeout(res, hold));
      });
      // Keep the tile only once two frames in a row are byte-identical. A
      // lazily loaded image reports itself complete, and even decoded, a second
      // or two before headless Chrome draws it, and a tile taken in that gap
      // shows an empty box where a slower run shows the picture. Something
      // that never stops moving (a countdown, a pulsing dot) never settles, so
      // the tries are bounded.
      let shot = await page.screenshot();
      for (let k = 0; k < 6; k++) {
        await page.waitForTimeout(450);
        const next = await page.screenshot();
        const same = next.equals(shot);
        shot = next;
        if (same) break;
      }
      writeFileSync(`${dir}/${String(i).padStart(2, '0')}.png`, shot);
      tiles.push(y);
      await page.mouse.wheel(0, step);
      await page.waitForTimeout(settle);
    }
    index.push({ path, viewport: vp.name, tiles });
    await page.close();
  }
  await context.close();
}
await browser.close();
writeFileSync(`${OUT}/${LABEL}/index.json`, JSON.stringify(index, null, 1));
console.log(`${LABEL}: ${index.reduce((n, r) => n + r.tiles.length, 0)} tiles over ${index.length} page views`);
