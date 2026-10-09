/* probe_splash.mjs — verify the 1.56s splash boot sequence (SplashLoader.svelte).
 *
 * Run against a dev or preview server:
 *   npm run dev -- --port 5177
 *   node scripts/probe_splash.mjs                 # defaults to :5177
 *   BASE=http://localhost:4173 node scripts/probe_splash.mjs
 *
 * Writes frames to scripts/.probe-out/frames/ and a JSON verdict to
 * scripts/.probe-out/splash-report.json. Exits non-zero on any failure.
 *
 * Why one page load PER FRAME: a screenshot costs ~250ms, so sampling the
 * sequence in a single sequential loop drifts catastrophically (a frame
 * requested at t=520ms landed at t=1927ms on the first run). The animation is
 * CSS-driven from page load, so a fresh load per timestamp is the only honest
 * way to sample it.
 *
 * Every check here is a negative control as well as a positive one: the skip
 * path must prove the overlay is ABSENT, not merely that the happy path works.
 * The first run of this probe is what caught the CSP failure that had silently
 * made the gate a no-op.
 */
import { chromium } from 'playwright';
import sharp from 'sharp';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

/* Count amber pixels in a captured frame. This is the only check here that
 * looks at what was actually PAINTED rather than at what the DOM claims. It
 * exists because a revision in which two opaque panels covered the entire
 * sequence passed every DOM assertion while rendering a plain black screen.
 * The panel's rules, corners, bars and clock are all amber (#f59e0b), so a
 * frame mid-sequence must contain a meaningful count of them. */
async function amberPixels(file) {
  const { data, info } = await sharp(file).raw().toBuffer({ resolveWithObject: true });
  const ch = info.channels;
  let n = 0;
  for (let i = 0; i < data.length; i += ch) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    if (r > 190 && g > 110 && g < 205 && b < 90) n++;
  }
  return n;
}

const BASE = process.env.BASE || 'http://localhost:5177';
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '.probe-out');
const FRAMES_DIR = join(ROOT, 'frames');
mkdirSync(FRAMES_DIR, { recursive: true });

const HOLD = 1560; // ms — must match DURATION in SplashLoader.svelte
const FRAMES = [80, 260, 460, 660, 860, 1060, 1220, 1340, 1450, 1540, 1700];

const report = { base: BASE, frames: [], checks: {}, cspErrors: [], failures: [] };
const fail = (msg) => report.failures.push(msg);

const browser = await chromium.launch();

/** Snapshot of splash state, read from the live DOM. Runs in page context. */
function readState() {
  const doc = document.documentElement;
  const el = document.querySelector('[data-sts-splash]');
  if (!el) return { present: false, splashAttr: doc.dataset.splash ?? null };
  const countVisible = (sel) =>
    [...el.querySelectorAll(sel)].filter((n) => parseFloat(getComputedStyle(n).opacity) > 0.5).length;
  const bars = [...el.querySelectorAll('.bar i')].map((n) => {
    const m = new DOMMatrixReadOnly(getComputedStyle(n).transform);
    return m.a;
  });
  // What a HUMAN actually sees at the centre. elementFromPoint alone is not
  // enough — it happily returns fully transparent elements — so walk the hit
  // stack and take the first one that is actually painted.
  const stack = document.elementsFromPoint(window.innerWidth / 2, window.innerHeight / 2);
  const painted = stack.find((n) => {
    const c = getComputedStyle(n);
    return c.visibility !== 'hidden' && parseFloat(c.opacity) > 0.01;
  });
  return {
    present: true,
    splashAttr: doc.dataset.splash ?? null,
    topAtCentre: painted ? `${painted.tagName.toLowerCase()}.${painted.className}` : null,
    // True when the visitor is looking at the page underneath rather than at
    // the boot screen — i.e. the splash is not doing its job.
    seesPageBehind: !(el.contains(painted ?? null) || painted === el),
    display: getComputedStyle(el).display,
    clock: el.querySelector('.hud-clock')?.textContent ?? null,
    rowsVisible: countVisible('.stages li'),
    stagesReportingOk: countVisible('.ok'),
    barsFilled: bars.filter((v) => v >= 0.99).length,
    stampOpacity: getComputedStyle(el.querySelector('.stamp-box')).opacity,
    locked: doc.classList.contains('splash-locked')
  };
}

// ---------------------------------------------------------------------------
// Pass 1: sample the sequence, one fresh load per timestamp.
// ---------------------------------------------------------------------------
for (const at of FRAMES) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  page.on('console', (m) => {
    if (m.type() === 'error' && /Content Security Policy/i.test(m.text())) {
      report.cspErrors.push(m.text().slice(0, 200));
    }
  });
  await page.goto(`${BASE}/?splash=force`, { waitUntil: 'domcontentloaded' });
  // Sample in ANIMATION time, read off the progress rule's own currentTime.
  // Wall-clock sampling measures the render-blocking stylesheet as if it were
  // part of the sequence, which is how an earlier revision of this probe
  // reported a clipped stamp that was really just a late first paint.
  const driftMs = await page.evaluate(async (target) => {
    const deadline = performance.now() + 10000;
    while (performance.now() < deadline) {
      const rule = document.querySelector('[data-sts-splash] .rule i');
      if (!rule) return null; // overlay already gone
      const ct = rule.getAnimations?.()[0]?.currentTime ?? null;
      if (ct !== null && ct >= target) return Math.round(ct - target);
      await new Promise((r) => requestAnimationFrame(r));
    }
    return -1;
  }, at);
  const state = await page.evaluate(readState);
  const shot = join(FRAMES_DIR, `t${String(at).padStart(4, '0')}.png`);
  await page.screenshot({ path: shot, animations: 'allow' });
  report.frames.push({ at, driftMs, ...state, amber: await amberPixels(shot) });
  await ctx.close();
}

// The sequence must actually progress: early frames partial, late frames complete.
const f = (at) => report.frames.find((x) => x.at === at);
if (!(f(260)?.rowsVisible > 0 && f(260).rowsVisible < 9))
  fail(`t=260ms should show a PARTIAL stage list, saw ${f(260)?.rowsVisible} rows`);
if (f(1220)?.rowsVisible !== 9) fail(`t=1220ms should show all 9 rows, saw ${f(1220)?.rowsVisible}`);
if (f(1220)?.stagesReportingOk !== 9)
  fail(`t=1220ms should have 9 stages reporting OK, saw ${f(1220)?.stagesReportingOk}`);
if (f(1220)?.barsFilled !== 9) fail(`t=1220ms should have 9 filled bars, saw ${f(1220)?.barsFilled}`);
if (!(parseFloat(f(1450)?.stampOpacity ?? 0) > 0.9))
  fail('SIGNAL ACQUIRED stamp not visible by t=1450ms');
if (f(1700)?.present) fail('overlay still present at t=1700ms — it should be gone');

// The panel must actually be ON SCREEN while the sequence plays — not merely
// present in the DOM. Two independent checks, because the DOM one alone was
// what let a black screen through: nothing opaque may cover the centre, AND
// the frame must contain real amber pixels.
for (const at of [260, 460, 660, 860, 1060, 1220]) {
  if (f(at)?.seesPageBehind)
    fail(`t=${at}ms: the page is showing through the boot screen (saw ${f(at).topAtCentre})`);
  if ((f(at)?.amber ?? 0) < 300)
    fail(`t=${at}ms: only ${f(at)?.amber} amber pixels painted — the sequence is not visible on screen`);
}
// ---------------------------------------------------------------------------
// The exit invariant, sampled every frame in-page.
//
// Screenshot sampling is too jittery to pin the cut: the full-cover window is
// tens of milliseconds and a ~30ms round-trip lands outside it, which read as
// "the wipe never covers" when it demonstrably did. Watching computed style
// per animation frame has no such latency.
//
// The invariant that actually matters: the site must never be exposed before
// the halves part. Concretely, there must be no frame where .veil is hidden
// while the wipes are not yet fully opaque — that frame would show the page
// popping in behind a half-finished cut.
// ---------------------------------------------------------------------------
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/?splash=force`, { waitUntil: 'domcontentloaded' });
  const exit = await page.evaluate(async (DURATION_GUARD) => {
    // Parse the clip-path inset the veil is currently at. 0% = fully covering,
    // 50% = fully parted.
    const insetPct = (cp) => {
      const m = /inset\(([\d.]+)(%|px)/.exec(cp);
      if (!m) return cp === 'none' ? 0 : null;
      return m[2] === '%' ? parseFloat(m[1]) : (parseFloat(m[1]) / window.innerHeight) * 100;
    };
    const violations = [];
    let partStartAt = null, partDoneAt = null, splashHiddenAt = null, coverAt = null;
    const deadline = performance.now() + 9000;
    while (performance.now() < deadline) {
      const rule = document.querySelector('[data-sts-splash] .rule i');
      const veil = document.querySelector('[data-sts-splash] .veil');
      const splash = document.querySelector('[data-sts-splash]');
      if (!rule || !veil || !splash) break;
      const ct = Math.round(rule.getAnimations()[0]?.currentTime ?? 0);
      const pct = insetPct(getComputedStyle(veil).clipPath);
      if (pct !== null) {
        if (pct < 1 && coverAt === null) coverAt = ct;
        if (pct > 1 && partStartAt === null) partStartAt = ct;
        if (pct >= 49 && partDoneAt === null) partDoneAt = ct;
        // The site must not start showing before the sequence is over.
        if (pct > 1 && ct < DURATION_GUARD) violations.push(ct);
      }
      if (splashHiddenAt === null && getComputedStyle(splash).visibility === 'hidden')
        splashHiddenAt = ct;
      await new Promise((r) => requestAnimationFrame(r));
    }
    return { coverAt, partStartAt, partDoneAt, splashHiddenAt, violations: violations.slice(0, 5) };
  }, HOLD - 260); // the exit may legitimately begin one transition before the end
  Object.assign(report.checks, { exit });
  await ctx.close();

  if (exit.violations.length)
    fail(`exit: veil started parting mid-sequence, at ct=${exit.violations.join(',')}ms`);
  if (exit.coverAt === null) fail('exit: the veil never fully covered the page');
  if (exit.partStartAt === null) fail('exit: the veil never parted — the site is never revealed');
  if (exit.partStartAt !== null && exit.partStartAt < HOLD * 0.8)
    fail(`exit: veil began parting at ${exit.partStartAt}ms, far ahead of the ${HOLD}ms budget`);
  // The CSS escape hatch must not fire until the part has finished, or it
  // clips the tail off the animation it is meant to be a backstop for.
  if (exit.splashHiddenAt !== null && exit.splashHiddenAt < HOLD)
    fail(`exit: overlay hid itself at ${exit.splashHiddenAt}ms, cutting the exit short of ${HOLD}ms`);
}

// ---------------------------------------------------------------------------
// Pass 2: when does the overlay actually leave, and does scroll unlock?
// ---------------------------------------------------------------------------
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/?splash=force`, { waitUntil: 'domcontentloaded' });
  report.checks.lockedDuringHold = await page.evaluate(() =>
    document.documentElement.classList.contains('splash-locked')
  );
  // Two clocks, both reported, because they answer different questions:
  //   sequenceMs — how long the visible boot sequence ran (animation time)
  //   totalWaitMs — how long the visitor waited from page load (gate time),
  //                 i.e. sequence + time-to-first-paint
  Object.assign(
    report.checks,
    await page.evaluate(async () => {
      const gate = window.__stsSplash?.t0 ?? performance.now();
      // Latch the animation origin while the rule still exists.
      let animOrigin = null;
      const deadline = performance.now() + 8000;
      while (performance.now() < deadline) {
        const rule = document.querySelector('[data-sts-splash] .rule i');
        if (!rule) {
          const now = performance.now();
          return {
            sequenceMs: animOrigin === null ? -1 : Math.round(now - animOrigin),
            totalWaitMs: Math.round(now - gate),
            firstPaintOffsetMs: animOrigin === null ? -1 : Math.round(animOrigin - gate)
          };
        }
        const ct = rule.getAnimations?.()[0]?.currentTime ?? null;
        if (ct !== null && animOrigin === null) animOrigin = performance.now() - ct;
        await new Promise((r) => requestAnimationFrame(r));
      }
      return { sequenceMs: -1, totalWaitMs: -1, firstPaintOffsetMs: -1 };
    })
  );
  report.checks.scrollUnlockedAfter = await page.evaluate(
    () => !document.documentElement.classList.contains('splash-locked')
  );
  // The site underneath must be real content, not a blank shell.
  report.checks.headingVisibleAfter = await page
    .locator('h1, h2')
    .first()
    .isVisible()
    .catch(() => false);
  await page.screenshot({ path: join(FRAMES_DIR, 'after-reveal.png') });
  await ctx.close();

  const seq = report.checks.sequenceMs;
  if (seq < HOLD - 60) fail(`visible sequence ran ${seq}ms — shorter than the ${HOLD}ms budget`);
  if (seq > HOLD + 300) fail(`visible sequence ran ${seq}ms — longer than ${HOLD}ms + 300ms slack`);
  if (!report.checks.lockedDuringHold) fail('scroll was not locked during the hold');
  if (!report.checks.scrollUnlockedAfter) fail('scroll stayed locked after the hold');
  if (!report.checks.headingVisibleAfter) fail('no heading visible after the reveal');
}

// ---------------------------------------------------------------------------
// Negative control: ?splash=off and repeat visits must leave NO visible overlay.
// ---------------------------------------------------------------------------
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/?splash=off`, { waitUntil: 'domcontentloaded' });
  report.checks.skipModeAttr = await page.evaluate(
    () => document.documentElement.dataset.splash ?? null
  );
  report.checks.skipModeVisible = await page.evaluate(() => {
    const el = document.querySelector('[data-sts-splash]');
    return el ? getComputedStyle(el).display !== 'none' : false;
  });
  await page.screenshot({ path: join(FRAMES_DIR, 'negative-control-splash-off.png') });

  // Same session, second navigation: must skip on its own.
  await page.goto(`${BASE}/?splash=force`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(HOLD + 300);
  await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });
  report.checks.secondVisitAttr = await page.evaluate(
    () => document.documentElement.dataset.splash ?? null
  );
  report.checks.secondVisitVisible = await page.evaluate(() => {
    const el = document.querySelector('[data-sts-splash]');
    return el ? getComputedStyle(el).display !== 'none' : false;
  });
  await ctx.close();

  if (report.checks.skipModeAttr !== 'skip')
    fail(`?splash=off set data-splash=${report.checks.skipModeAttr}, expected "skip"`);
  if (report.checks.skipModeVisible) fail('?splash=off still rendered a VISIBLE overlay');
  if (report.checks.secondVisitAttr !== 'skip')
    fail(`second visit set data-splash=${report.checks.secondVisitAttr}, expected "skip"`);
  if (report.checks.secondVisitVisible)
    fail('second visit in the same session still showed the overlay');
}

// ---------------------------------------------------------------------------
// Reduced motion: static plate, same budget, no movement.
// ---------------------------------------------------------------------------
{
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    reducedMotion: 'reduce'
  });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/?splash=force`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(700);
  await page.screenshot({ path: join(FRAMES_DIR, 'reduced-motion-t0700.png') });
  report.checks.reducedMotionRowsAt700 = await page.evaluate(
    () => document.querySelectorAll('[data-sts-splash] .stages li').length
  );
  report.checks.reducedMotionTotalMs = await page.evaluate(async () => {
    const t0 = window.__stsSplash?.t0 ?? performance.now();
    const deadline = performance.now() + 8000;
    while (performance.now() < deadline) {
      if (!document.querySelector('[data-sts-splash]')) return Math.round(performance.now() - t0);
      await new Promise((r) => requestAnimationFrame(r));
    }
    return -1;
  });
  await ctx.close();

  if (report.checks.reducedMotionRowsAt700 !== 9)
    fail(`reduced motion should show the full static plate, saw ${report.checks.reducedMotionRowsAt700} rows`);
  if (report.checks.reducedMotionTotalMs < HOLD)
    fail(`reduced-motion overlay left at ~${report.checks.reducedMotionTotalMs}ms — shorter than ${HOLD}ms`);
}

// ---------------------------------------------------------------------------
// PASSTHROUGH — the whole point of the splash.
//
// It exists to cover slow assets (the hero video above all) while the site
// loads underneath, then drop the visitor straight in. So the page must be
// loading DURING the hold, not after it. If the overlay were deferring work —
// blocking hydration, or sitting in front of a page that only starts fetching
// once it is gone — the sequence would be pure added latency instead of
// cover. Measure what actually finished before the overlay lifted.
// ---------------------------------------------------------------------------
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const finished = [];
  page.on('requestfinished', (r) => finished.push({ url: r.url(), type: r.resourceType() }));
  await page.goto(`${BASE}/?splash=force`, { waitUntil: 'domcontentloaded' });

  // Snapshot the moment the overlay leaves — not later.
  const atLift = await page.evaluate(async () => {
    const deadline = performance.now() + 8000;
    while (performance.now() < deadline) {
      if (!document.querySelector('[data-sts-splash]')) break;
      await new Promise((r) => requestAnimationFrame(r));
    }
    const v = document.querySelector('video');
    const imgs = [...document.querySelectorAll('img')];
    return {
      readyState: document.readyState,
      hydrated: !!document.querySelector('[data-sts-hydrated], main'),
      videoPresent: !!v,
      videoReadyState: v ? v.readyState : null,
      imgTotal: imgs.length,
      imgComplete: imgs.filter((i) => i.complete).length
    };
  });
  report.checks.passthrough = {
    ...atLift,
    requestsFinishedBeforeLift: finished.length,
    mediaFinishedBeforeLift: finished.filter((r) => /media|image|font/.test(r.type)).length
  };
  await ctx.close();

  const p = report.checks.passthrough;
  // A page that had done nothing by the time the overlay lifted would mean the
  // splash was blocking rather than covering.
  if (p.requestsFinishedBeforeLift < 5)
    fail(`passthrough: only ${p.requestsFinishedBeforeLift} requests finished before the overlay lifted — the site is not loading underneath`);
  if (p.readyState === 'loading')
    fail('passthrough: document still in "loading" when the overlay lifted');
  if (p.imgTotal > 0 && p.imgComplete === 0)
    fail(`passthrough: none of ${p.imgTotal} images had loaded when the overlay lifted`);
  if (p.videoPresent && p.videoReadyState === 0)
    fail('passthrough: hero video had buffered nothing when the overlay lifted — it is not being covered');
}

// ---------------------------------------------------------------------------
// No-JS: the escape hatch. With scripting off, neither the gate nor the
// component runs, so nothing can remove the overlay or lift a scroll lock.
// The splashOut keyframe has to carry it alone. A visitor must never be left
// behind an opaque, unscrollable boot screen.
// ---------------------------------------------------------------------------
{
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    javaScriptEnabled: false
  });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2600);
  await page.screenshot({ path: join(FRAMES_DIR, 'no-js-t2600.png') });
  const el = page.locator('[data-sts-splash]');
  report.checks.noJsOverlayVisible = (await el.count()) ? await el.isVisible() : false;
  report.checks.noJsScrollLocked = await page
    .locator('html.splash-locked')
    .count()
    .then((n) => n > 0);
  await ctx.close();

  if (report.checks.noJsOverlayVisible) fail('no-JS: overlay still visible at t=2600ms');
  if (report.checks.noJsScrollLocked) fail('no-JS: scroll left locked');
}

// ---------------------------------------------------------------------------
// Mobile viewport: no horizontal overflow, panel fits on screen.
// ---------------------------------------------------------------------------
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/?splash=force`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1150);
  await page.screenshot({ path: join(FRAMES_DIR, 'mobile-390-t1150.png') });
  report.checks.mobileHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth
  );
  // Truncated stage names would defeat the point of the sequence.
  report.checks.mobileTruncatedNames = await page.evaluate(() =>
    [...document.querySelectorAll('[data-sts-splash] .nm')]
      .filter((n) => n.scrollWidth > n.clientWidth + 1)
      .map((n) => n.textContent)
  );
  report.checks.mobilePanelFits = await page.evaluate(() => {
    const p = document.querySelector('[data-sts-splash] .panel');
    if (!p) return false;
    const r = p.getBoundingClientRect();
    return r.left >= 0 && r.right <= window.innerWidth && r.top >= 0 && r.bottom <= window.innerHeight;
  });
  await ctx.close();

  if (report.checks.mobileHorizontalOverflow) fail('horizontal overflow at 390px');
  if (!report.checks.mobilePanelFits) fail('splash panel does not fit inside a 390x844 viewport');
  if (report.checks.mobileTruncatedNames.length)
    fail(`stage names ellipsised at 390px: ${report.checks.mobileTruncatedNames.join(', ')}`);
}

await browser.close();

// A blocked gate script is the failure mode that started all this.
const inlineBlocked = report.cspErrors.filter((e) => /inline script/i.test(e));
if (inlineBlocked.length)
  fail(`CSP blocked ${inlineBlocked.length} inline script(s) — the splash gate may be a no-op`);

report.verdict = report.failures.length ? 'FAIL' : 'PASS';
writeFileSync(join(ROOT, 'splash-report.json'), JSON.stringify(report, null, 2));

console.log(
  report.frames
    .map(
      (x) =>
        `t=${String(x.at).padStart(4)}ms drift=${String(x.driftMs).padStart(3)} ` +
        `present=${x.present ? 'Y' : 'n'} rows=${x.rowsVisible ?? '-'}/9 ` +
        `ok=${x.stagesReportingOk ?? '-'} bars=${x.barsFilled ?? '-'} ` +
        `stamp=${x.stampOpacity ?? '-'} amber=${String(x.amber).padStart(5)} ` +
        `top=${x.topAtCentre ?? '-'}`
    )
    .join('\n')
);
console.log('\nchecks: ' + JSON.stringify(report.checks, null, 2));
console.log(`\nverdict: ${report.verdict}`);
if (report.failures.length) console.log('failures:\n - ' + report.failures.join('\n - '));
process.exit(report.failures.length ? 1 : 0);
