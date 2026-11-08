// Three checks the first passes could not make.
// Usage: node audit_extra.mjs BASE_URL OUT_DIR LABEL
//
//  1. Dates on /blog as a visitor in Los Angeles and one in Berlin see them,
//     next to the dates as written in the post list.
//  2. What a browser with JavaScript switched off shows: visible words, whether
//     an overlay covers the middle of the screen, and a screenshot.
//  3. Meta tags in the served HTML (before any script runs): description,
//     canonical, title and h1 counts.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [BASE, OUT, LABEL] = process.argv.slice(2);
mkdirSync(`${OUT}/${LABEL}/nojs`, { recursive: true });
const out = { base: BASE, dates: {}, nojs: [], served: [] };
const browser = await chromium.launch({ channel: 'chrome', headless: true });

// 1. Dates, in two time zones.
for (const tz of ['America/Los_Angeles', 'Europe/Berlin']) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, timezoneId: tz });
  const page = await ctx.newPage();
  await page.goto(BASE + '/blog', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  out.dates[tz] = await page.evaluate(() =>
    [...document.querySelectorAll('.featured-card, .post-card')].slice(0, 5).map((c) => ({
      href: c.getAttribute('href'), shown: c.querySelector('time')?.textContent.trim(),
    })));
  await ctx.close();
}

// 2. JavaScript off.
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, javaScriptEnabled: false });
for (const path of ['/', '/blog', '/about', '/factcheck', '/checklist', '/early-access', '/blog/algae-saves-us']) {
  const page = await ctx.newPage();
  await page.goto(BASE + path, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  const rec = await page.evaluate(() => {
    const shown = (el) => {
      for (let a = el; a; a = a.parentElement) {
        const cs = getComputedStyle(a);
        if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return false;
      }
      return true;
    };
    let visibleWords = 0, hiddenWords = 0;
    const main = document.querySelector('main') || document.body;
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const w = n.textContent.trim().split(/\s+/).filter(Boolean).length;
      if (!w || !n.parentElement || /^(script|style|noscript)$/i.test(n.parentElement.tagName)) continue;
      if (shown(n.parentElement)) visibleWords += w; else hiddenWords += w;
    }
    const mid = document.elementFromPoint(innerWidth / 2, innerHeight / 2);
    const cover = mid && (() => { const r = mid.getBoundingClientRect(); const cs = getComputedStyle(mid);
      return { el: mid.tagName.toLowerCase() + (mid.className && typeof mid.className === 'string' ? '.' + mid.className.split(/\s+/)[0] : ''),
        fixed: cs.position === 'fixed', fullScreen: r.width >= innerWidth - 2 && r.height >= innerHeight - 2 }; })();
    return { visibleWords, hiddenWords, h1: document.querySelectorAll('h1').length, cover,
      bodyOverflow: getComputedStyle(document.body).overflow + '/' + getComputedStyle(document.documentElement).overflow };
  });
  await page.screenshot({ path: `${OUT}/${LABEL}/nojs/${path === '/' ? 'home' : path.slice(1).replace(/\W+/g, '-')}.png` });
  out.nojs.push({ path, ...rec });
  await page.close();
}
await ctx.close();
await browser.close();

// 3. Served HTML, no browser at all.
const PATHS = (process.env.PAGES || '').split(/\s+/).filter(Boolean);
for (const path of PATHS) {
  const html = await (await fetch(BASE + path)).text();
  const count = (re) => (html.match(re) || []).length;
  const descs = [...html.matchAll(/<meta name="description"(?: content="([^"]*)")?/gi)].map((m) => m[1] ?? '(empty)');
  const body = html.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, ' ').replace(/<[^>]+>/g, ' ');
  out.served.push({ path, descriptions: descs.length, firstDesc: (descs[0] || '').slice(0, 60),
    emptyDesc: descs.filter((d) => d === '(empty)' || d === '').length,
    canonicals: count(/<link rel="canonical"/gi), titles: count(/<title>/gi), h1: count(/<h1[\s>]/gi),
    words: body.split(/\s+/).filter(Boolean).length });
}
writeFileSync(`${OUT}/${LABEL}-extra.json`, JSON.stringify(out, null, 1));
console.log(`${LABEL}: dates for ${Object.keys(out.dates).length} zones, ${out.nojs.length} no-JS pages, ${out.served.length} served pages`);
