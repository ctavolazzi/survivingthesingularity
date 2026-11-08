// Accessibility-oriented browser pass: form controls and buttons with no
// accessible name, text contrast, and which elements cause layout shift.
// Usage: node audit_a11y.mjs BASE_URL OUT_JSON [--control]
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [BASE, OUT] = process.argv.slice(2);
const CONTROL = process.argv.includes('--control');
const PATHS = CONTROL ? ['/about'] : ['/', '/book', '/early-access', '/about', '/blog', '/checklist',
  '/signals', '/factcheck', '/policies', '/terms', '/devlog', '/exclusive-friends-only', '/read',
  '/workshop', '/blog/farm-bot-deep-dive', '/blog/algae-saves-us'];

const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
await context.addInitScript(() => {
  window.__shifts = [];
  try {
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) {
        if (e.hadRecentInput) continue;
        window.__shifts.push({
          value: e.value, t: Math.round(e.startTime),
          nodes: (e.sources || []).map((s) => {
            const n = s.node;
            if (!n || !n.tagName) return '?';
            return n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') +
              (typeof n.className === 'string' && n.className ? '.' + n.className.trim().split(/\s+/)[0] : '');
          }).slice(0, 3),
        });
      }
    }).observe({ type: 'layout-shift', buffered: true });
  } catch (_) { /* unsupported */ }
});

const results = [];
for (const path of PATHS) {
  const page = await context.newPage();
  await page.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(2500);
  let scrolledTo = null;
  if (process.argv.includes('--scroll')) {
    // Sections that reveal on scroll sit at opacity 0 until they enter the
    // viewport, and text at opacity 0 measures as contrast 1:1. Walk the page
    // top to bottom first so every reveal has fired, then measure.
    // Real wheel events, not window.scrollTo: html and body both set
    // overflow-y:auto here, so the window is not necessarily what scrolls, and
    // scrollTo moved nothing on the first attempt (100 elements stayed hidden).
    await page.mouse.move(640, 400);
    let last = -1;
    for (let i = 0; i < 160; i++) {
      await page.mouse.wheel(0, 480);
      await page.waitForTimeout(90);
      const y = await page.evaluate(() => Math.max(window.scrollY, document.body.scrollTop, document.documentElement.scrollTop));
      if (y === last && i > 3) break;      // reached the bottom
      last = y;
    }
    await page.waitForTimeout(1000);
    scrolledTo = last;
  }
  if (CONTROL) {
    await page.evaluate(() => {
      const box = document.createElement('div');
      box.innerHTML = '<p id="ctl-contrast" style="color:#777;background:#888;font-size:14px">CONTROL low contrast text</p>' +
        '<input id="ctl-input" type="text"><button id="ctl-button" style="display:inline-block;width:24px;height:24px"></button>';
      // Inside <main>, where the contrast scan looks. (prepend() returns undefined,
      // so chaining it with ?? moved the box out to <body> and hid it from the scan.)
      (document.querySelector('main') || document.body).prepend(box);
    });
  }
  const rec = await page.evaluate(() => {
    const visible = (el) => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    };
    const sel = (el) => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
      (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
    const inDrawer = (el) => !!el.closest('[inert]');

    // 1. Form controls with no accessible name.
    const unnamedControls = [];
    for (const el of document.querySelectorAll('input:not([type=hidden]), textarea, select')) {
      if (inDrawer(el)) continue;
      const named = (el.labels && el.labels.length) || el.getAttribute('aria-label') ||
        el.getAttribute('aria-labelledby') || el.getAttribute('title');
      if (!named) {
        unnamedControls.push({ el: sel(el), type: el.type, placeholder: el.placeholder || '',
          hiddenFromAT: el.getAttribute('aria-hidden') === 'true' || el.tabIndex === -1, visible: visible(el) });
      }
    }
    // 2. Buttons and links with no accessible name.
    const unnamedActions = [];
    for (const el of document.querySelectorAll('button, a[href], [role=button]')) {
      if (inDrawer(el) || !visible(el)) continue;
      const name = (el.getAttribute('aria-label') || el.getAttribute('title') || el.textContent || '').trim() ||
        [...el.querySelectorAll('img[alt]')].map((i) => i.alt).join('').trim() ||
        [...el.querySelectorAll('svg title')].map((t) => t.textContent).join('').trim();
      if (!name) unnamedActions.push({ el: sel(el), href: el.getAttribute('href') || '' });
    }
    // 3. Text contrast.
    const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
      const p = m[1].split(/[,\s/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p[3] === undefined ? 1 : p[3] }; };
    const lum = ({ r, g, b }) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
    const over = (top, bottom) => ({ r: top.r * top.a + bottom.r * (1 - top.a), g: top.g * top.a + bottom.g * (1 - top.a),
      b: top.b * top.a + bottom.b * (1 - top.a), a: 1 });
    const pageBg = parse(getComputedStyle(document.body).backgroundColor) || { r: 2, g: 6, b: 23, a: 1 };
    const bgOf = (el) => {
      const layers = []; let unknown = false;
      for (let a = el; a; a = a.parentElement) {
        const cs = getComputedStyle(a);
        if (cs.backgroundImage && cs.backgroundImage !== 'none') unknown = true;
        const c = parse(cs.backgroundColor);
        if (c && c.a > 0) { layers.push(c); if (c.a === 1) break; }
      }
      let bg = pageBg.a === 1 ? pageBg : { r: 2, g: 6, b: 23, a: 1 };
      for (const l of layers.reverse()) bg = over(l, bg);
      return { bg, unknown };
    };
    const low = {};
    let checked = 0;
    for (const el of document.querySelectorAll('main *, footer *, header *, nav *')) {
      if (inDrawer(el) || !visible(el)) continue;
      const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
      if (!own.length) continue;
      const cs = getComputedStyle(el);
      let op = 1; for (let a = el; a; a = a.parentElement) op *= +getComputedStyle(a).opacity;
      const fg0 = parse(cs.color); if (!fg0) continue;
      const { bg, unknown } = bgOf(el);
      if (unknown) continue;                       // text over an image or gradient: not judged here
      const fg = over({ ...fg0, a: fg0.a * op }, bg);
      const L1 = lum(fg), L2 = lum(bg);
      const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
      const size = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
      const large = size >= 24 || (bold && size >= 18.66);
      checked++;
      if (ratio < (large ? 3 : 4.5)) {
        const key = `${cs.color}|op${op.toFixed(2)}|${Math.round(size)}px|${sel(el).replace(/\.svelte-[a-z0-9]+/g, '')}`;
        low[key] = low[key] || { ratio: Math.round(ratio * 100) / 100, n: 0, text: own[0].textContent.trim().slice(0, 50), need: large ? 3 : 4.5 };
        low[key].n++;
      }
    }
    return { unnamedControls, unnamedActions, contrastChecked: checked, lowContrast: low,
      shifts: (window.__shifts || []).sort((a, b) => b.value - a.value).slice(0, 4)
        .map((s) => ({ value: Math.round(s.value * 1000) / 1000, t: s.t, nodes: s.nodes })) };
  });
  results.push({ path, scrolledTo, ...rec });
  await page.close();
}
await browser.close();
writeFileSync(OUT, JSON.stringify(results, null, 1));
console.log(`${results.length} pages checked`);
