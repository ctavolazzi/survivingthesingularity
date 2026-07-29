#!/usr/bin/env node
/**
 * Screenshot at a TRUE narrow viewport, and measure overflow for real.
 *
 * Usage:
 *   node scripts/shot-narrow.mjs <url> <out.png> <width> [height]
 *
 * Why this is Node and Playwright instead of the Chrome CLI:
 *
 *   Chrome's --window-size clamps to a 500px minimum on this macOS
 *   (Darwin 21.6 / macOS 12.6). Asking for 390 silently gives you 500, so a
 *   layout that breaks at 390 photographs clean, and a layout that is fine at
 *   390 can appear broken at the clamped width. Either way the screenshot lies.
 *
 *   The iframe trick gets a true inner width but cannot measure it: a file://
 *   harness wrapping an http://localhost page is cross-origin, so reading
 *   scrollWidth from the parent throws. An overflow check that cannot read the
 *   document is not a check.
 *
 *   Playwright sets an exact viewport with no clamp AND can evaluate inside the
 *   page, so the number it reports is the number the browser actually has.
 *
 * Playwright is loaded from the sts-v0.7.3 install rather than duplicated here.
 */

import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { join, dirname } from 'node:path';
import { mkdirSync } from 'node:fs';

const PW_HOST = join(homedir(), 'Code/active/sts-v0.7.3/package.json');

const [, , url, out, widthArg, heightArg] = process.argv;

if (!url || !out || !widthArg) {
  console.error('usage: node scripts/shot-narrow.mjs <url> <out.png> <width> [height]');
  process.exit(2);
}

const width = Number(widthArg);
const height = Number(heightArg ?? 1600);

if (!Number.isFinite(width) || width < 200) {
  console.error(`refusing: width ${widthArg} is not a plausible viewport`);
  process.exit(2);
}

let chromium;
try {
  chromium = createRequire(PW_HOST)('playwright').chromium;
} catch (err) {
  console.error(`FAIL: could not load playwright from ${PW_HOST}`);
  console.error(err.message);
  console.error('Install playwright, or point PW_HOST at a project that has it.');
  process.exit(1);
}

mkdirSync(dirname(out), { recursive: true });

const browser = await chromium.launch();

try {
  const page = await browser.newPage({
    viewport: { width, height },
    deviceScaleFactor: 1
  });

  const response = await page.goto(url, { waitUntil: 'load', timeout: 20000 });
  const status = response ? response.status() : 'n/a';

  // Let layout settle without waiting on networkidle, which flakes on a dev
  // server holding an open HMR socket.
  await page.waitForTimeout(600);

  await page.screenshot({ path: out, fullPage: true });

  // The measurement. scrollWidth beyond clientWidth means the document scrolls
  // sideways, which is the defect a screenshot hides best.
  const metrics = await page.evaluate(() => {
    const d = document.documentElement;

    // Find the widest offender so the report names a culprit, not just a number.
    let worst = null;
    let worstRight = d.clientWidth;
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) continue;
      if (r.right > worstRight + 0.5) {
        worstRight = r.right;
        worst = {
          tag: el.tagName.toLowerCase(),
          cls: (el.className || '').toString().slice(0, 60),
          right: Math.round(r.right)
        };
      }
    }

    return {
      clientWidth: d.clientWidth,
      scrollWidth: d.scrollWidth,
      scrollHeight: d.scrollHeight,
      worst
    };
  });

  const overflow = metrics.scrollWidth - metrics.clientWidth;

  console.log(`shot: ${out}`);
  console.log(`  url        ${url}  (HTTP ${status})`);
  console.log(`  viewport   ${metrics.clientWidth}px wide, ${metrics.scrollHeight}px tall`);

  if (overflow > 0) {
    console.log(`  OVERFLOW   FAIL. scrollWidth ${metrics.scrollWidth} exceeds clientWidth ${metrics.clientWidth} by ${overflow}px`);
    if (metrics.worst) {
      console.log(`  culprit    <${metrics.worst.tag} class="${metrics.worst.cls}"> reaches x=${metrics.worst.right}`);
    }
    process.exitCode = 1;
  } else {
    console.log('  OVERFLOW   PASS. No horizontal page scroll.');
  }
} finally {
  await browser.close();
}
