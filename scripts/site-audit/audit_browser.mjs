// Real-browser pass over a locally served build.
// Usage: node audit_browser.mjs BASE_URL OUT_DIR LABEL [--control]
//
// For each page, at desktop and phone widths, records console errors, page
// errors, failed and 4xx/5xx requests, horizontal overflow measured from
// element boxes (not scrollWidth, which overflow-x:hidden pins), cumulative
// layout shift, and a full-page screenshot.
//
// DO NOT COMPARE THE SCREENSHOTS THIS WRITES. This site scrolls an inner box
// (html and body both set overflow-y:auto), so a fullPage capture paints the
// first 800px and blank background below it. Two blank halves compare as
// identical. Use audit_tiles.mjs for any before/after picture comparison.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const [BASE, OUT, LABEL] = process.argv.slice(2);
const CONTROL = process.argv.includes('--control');
const PATHS = CONTROL ? ['/about'] : [
  '/', '/book', '/early-access', '/about', '/blog', '/checklist', '/signals', '/factcheck',
  '/devlog', '/devlog/the-easier-question', '/workshop', '/policies', '/terms', '/disclaimer',
  '/accessibility', '/read', '/unsubscribe', '/blog/singularity-express',
  '/blog/farm-bot-deep-dive', '/blog/algae-saves-us', '/blog/whispers-of-the-future',
  '/this-route-does-not-exist',
];
const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 800 },
  { name: 'phone', width: 390, height: 844 },
];

const slug = (p) => (p === '/' ? 'home' : p.replace(/^\//, '').replace(/[^a-z0-9]+/gi, '-'));
const results = [];
const browser = await chromium.launch({ channel: 'chrome', headless: true });

for (const vp of VIEWPORTS) {
  mkdirSync(`${OUT}/${LABEL}/${vp.name}`, { recursive: true });
  const context = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: 1,
    reducedMotion: 'no-preference',
  });
  // Count layout shift from the first frame, before any page script runs.
  await context.addInitScript(() => {
    window.__cls = 0;
    try {
      new PerformanceObserver((list) => {
        for (const e of list.getEntries()) if (!e.hadRecentInput) window.__cls += e.value;
      }).observe({ type: 'layout-shift', buffered: true });
    } catch (_) { /* unsupported */ }
  });

  for (const path of PATHS) {
    const page = await context.newPage();
    const rec = { path, viewport: vp.name, console: [], pageErrors: [], failed: [], bad: [] };
    page.on('console', (m) => {
      if (m.type() === 'error' || m.type() === 'warning') {
        rec.console.push(`${m.type()}: ${m.text().slice(0, 200)}`);
      }
    });
    page.on('pageerror', (e) => rec.pageErrors.push(String(e).slice(0, 200)));
    page.on('requestfailed', (r) => {
      const u = r.url();
      if (!/youtube|ytimg|doubleclick|google|gstatic/.test(u)) {
        rec.failed.push(`${r.failure()?.errorText} ${u.slice(0, 120)}`);
      }
    });
    page.on('response', (r) => {
      if (r.status() >= 400 && r.url().startsWith(BASE) && r.url() !== BASE + path) {
        rec.bad.push(`${r.status()} ${r.url().replace(BASE, '').slice(0, 100)}`);
      }
    });
    try {
      const resp = await page.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
      rec.status = resp?.status();
      await page.waitForTimeout(2500);
      if (CONTROL) {
        // Known defects of each class this pass claims to catch.
        await page.evaluate(() => {
          console.error('CONTROL console error');
          const wide = document.createElement('div');
          wide.id = 'control-wide';
          wide.style.cssText = 'width:3000px;height:10px;background:red';
          document.body.prepend(wide);
        });
        await page.waitForTimeout(300);
      }
      rec.after = await page.evaluate(() => {
        const cw = document.documentElement.clientWidth;
        const over = [];
        for (const el of document.querySelectorAll('body *')) {
          if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0) continue;
          if (r.right < 0 || r.left > cw + 2000) continue; // parked off-screen by design
          // Clipped by an ancestor that hides overflow: not visible, not a defect.
          let clipped = false;
          for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
            const s = getComputedStyle(a);
            if (/(hidden|clip|auto|scroll)/.test(s.overflowX)) {
              const ar = a.getBoundingClientRect();
              if (ar.right <= cw + 1 && ar.left >= -1) { clipped = true; break; }
            }
          }
          if (clipped) continue;
          if (r.right > cw + 1 || r.left < -1) {
            over.push({
              el: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
                (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''),
              right: Math.round(r.right), left: Math.round(r.left),
              text: (el.textContent || '').trim().slice(0, 40),
            });
          }
        }
        return {
          clientWidth: cw,
          scrollWidth: document.documentElement.scrollWidth,
          overflowX: getComputedStyle(document.documentElement).overflowX + '/' + getComputedStyle(document.body).overflowX,
          over: over.slice(0, 8), overCount: over.length,
          cls: Math.round((window.__cls || 0) * 1000) / 1000,
          title: document.title,
          h1: [...document.querySelectorAll('h1')].map((h) => h.textContent.trim().slice(0, 70)),
          mainWords: (document.querySelector('main')?.innerText || document.body.innerText).split(/\s+/).length,
          postCards: document.querySelectorAll('.post-card, .featured-card').length,
        };
      });
      if (!CONTROL) {
        await page.screenshot({ path: `${OUT}/${LABEL}/${vp.name}/${slug(path)}.png`, fullPage: true });
      }
    } catch (e) {
      rec.error = String(e).slice(0, 200);
    }
    results.push(rec);
    await page.close();
  }
  await context.close();
}
await browser.close();
writeFileSync(`${OUT}/${LABEL}${CONTROL ? '-control' : ''}.json`, JSON.stringify(results, null, 1));
console.log(`${LABEL}: ${results.length} page loads recorded`);
