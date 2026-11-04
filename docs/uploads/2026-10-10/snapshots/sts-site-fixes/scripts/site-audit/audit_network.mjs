// What does a page ask other hosts for when it loads?
// Usage: [PAGES="/ /blog"] node audit_network.mjs BASE_URL OUT_JSON
//
// For each page: load it in real Chrome, scroll to the bottom with wheel events
// so lazy images and embeds fire, wait, and record every request by host, with
// bytes received. Nothing is clicked, so this is the load a visitor causes just
// by arriving and reading. Requests to the site itself are "first party";
// everything else is listed by host.
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [BASE, OUT] = process.argv.slice(2);
const PAGES = (process.env.PAGES || '/ /blog /about /checklist /early-access /blog/robot-farm-bot').split(' ').filter(Boolean);
const self = new URL(BASE).host;
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const report = [];

for (const path of PAGES) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  const hosts = {};
  const done = [];
  page.on('requestfinished', (req) => done.push((async () => {
    const host = new URL(req.url()).host;
    let bytes = 0;
    try { bytes = (await req.sizes()).responseBodySize; } catch { /* aborted or cached */ }
    const h = (hosts[host] ||= { requests: 0, bytes: 0, types: {} });
    h.requests++; h.bytes += Math.max(0, bytes);
    h.types[req.resourceType()] = (h.types[req.resourceType()] || 0) + 1;
  })()));
  page.on('requestfailed', (req) => {
    const host = new URL(req.url()).host;
    const h = (hosts[host] ||= { requests: 0, bytes: 0, types: {} });
    h.failed = (h.failed || 0) + 1;
  });
  await page.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(3000);
  await page.mouse.move(640, 400);
  let last = -1;
  for (let i = 0; i < 200; i++) {
    await page.mouse.wheel(0, 600);
    await page.waitForTimeout(120);
    const y = await page.evaluate(() => Math.max(window.scrollY, document.body.scrollTop, document.documentElement.scrollTop));
    if (y === last && i > 3) break;
    last = y;
  }
  await page.waitForTimeout(6000);            // let late embeds finish their own requests
  await Promise.allSettled(done);
  const iframes = await page.evaluate(() => [...document.querySelectorAll('iframe')].map((f) => new URL(f.src, location.href).host));
  const cookies = (await ctx.cookies()).map((c) => c.domain.replace(/^\./, ''));
  const third = Object.entries(hosts).filter(([h]) => h !== self);
  report.push({
    path,
    firstParty: hosts[self] || { requests: 0, bytes: 0 },
    thirdParty: Object.fromEntries(third),
    thirdPartyRequests: third.reduce((n, [, v]) => n + v.requests, 0),
    thirdPartyBytes: third.reduce((n, [, v]) => n + v.bytes, 0),
    iframes,
    cookieDomains: [...new Set(cookies)].sort(),
  });
  await ctx.close();
}
await browser.close();
writeFileSync(OUT, JSON.stringify(report, null, 1));
for (const r of report) {
  const kb = (n) => (n / 1024).toFixed(0).padStart(6) + ' KB';
  console.log(`${r.path.padEnd(34)} own ${String(r.firstParty.requests).padStart(3)} req ${kb(r.firstParty.bytes)} | other hosts ${String(r.thirdPartyRequests).padStart(3)} req ${kb(r.thirdPartyBytes)} | iframes ${r.iframes.length} | cookies from: ${r.cookieDomains.join(', ') || 'none'}`);
}
