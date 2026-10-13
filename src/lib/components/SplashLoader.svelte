<script>
  // SplashLoader — the 1.56s boot sequence.
  //
  // A cold-start terminal that maps the book's own Nine Stages, one per beat,
  // then hard-wipes off the screen to reveal the site. The whole sequence is
  // budgeted at exactly 1560ms of hold, +40ms of teardown.
  //
  // Timing lives in ONE place: --t below and the DURATION constant here. The
  // CSS derives every delay from --t via calc(), so changing the budget in
  // both spots rescales the entire sequence.
  //
  // The decision to play, the time origin, the scroll lock and the seen-flag
  // all belong to static/splash-gate.js, which runs render-blocking in <head>
  // before anything paints. This component owns only the markup, the CSS, the
  // millisecond readout and the teardown.
  //
  // Teardown is anchored to the gate's timestamp, NOT to hydration. The CSS
  // animations begin at first paint while onMount fires strictly later, and
  // measuring from onMount let the hold run to 2131ms against a 1560ms budget
  // on the dev server. Reading __stsSplash.t0 collapses the two clocks.
  import { onMount } from 'svelte';

  const DURATION = 1560; // ms of hold — must match --t in the CSS below
  const EXIT = 170;      // ms the boot screen takes to split open
  const TEARDOWN = 60;   // ms of overrun before the node is removed

  // The nine stages, in book order. Chapter 2 of the manuscript.
  const STAGES = [
    'THE CASH GRAB',
    'THE PANIC AND THE PLUG',
    'THE ADULTS STEP IN',
    'THE END OF LABOR',
    'THE PRIMATE BACKLASH',
    'THE ASI EXODUS',
    'THE ULTIMATE CURE',
    'THE TRANSITION TO USI',
    'THE APEX INTELLIGENCE'
  ];

  let done = false;      // true once the node should leave the DOM
  let exiting = false;   // true once the boot screen starts splitting open
  let elapsed = 0;       // millisecond readout, drives the HUD clock
  let ruleEl;            // the full-duration progress rule — our clock source

  onMount(() => {
    const root = document.documentElement;

    const unmount = () => {
      done = true;
      root.classList.remove('splash-locked');
    };

    // Not playing: either seen already this session, explicitly disabled, or
    // splash-gate.js failed to load. In all three cases app.css has already
    // hidden the overlay; drop it and let the page through.
    if (root.dataset.splash !== 'play') {
      unmount();
      return;
    }

    let raf;
    let exitTimer;
    let doneTimer;

    // Everything downstream hangs off one origin: the instant the CSS
    // sequence actually began.
    //
    // The exit is driven from HERE, by flipping one class, rather than from a
    // set of CSS animation-delays. It used to be three coordinated animations
    // (two opaque halves plus a veil that had to hide inside the gap between
    // them), and getting that right depended on Chrome's interpolation
    // semantics for `visibility` and on where stepped timing functions land
    // their endpoints. Three consecutive probe runs of one build gave three
    // different verdicts. A single class flip has no ordering to get wrong.
    const schedule = (origin) => {
      const since = () => performance.now() - origin;
      const tick = (now) => {
        elapsed = Math.min(DURATION, Math.round(now - origin));
        if (elapsed < DURATION) raf = requestAnimationFrame(tick);
      };
      raf = requestAnimationFrame(tick);
      exitTimer = setTimeout(() => (exiting = true), Math.max(0, DURATION - EXIT - since()));
      doneTimer = setTimeout(unmount, Math.max(0, DURATION + TEARDOWN - since()));
    };

    // Read the origin off the CSS animation rather than off the wall clock.
    // The bottom progress rule runs for exactly --t with zero delay, so its
    // currentTime is precisely how far the sequence has got.
    //
    // CSS animations do not start at navigation — they start at first paint,
    // which the render-blocking stylesheet defers (~450ms on the preview
    // build). Anchoring to the wall clock therefore wiped the screen before
    // SIGNAL ACQUIRED ever landed.
    //
    // Nor can the animation simply be read at mount: hydration frequently
    // wins the race and getAnimations() comes back empty, in which case an
    // immediate fallback to now() silently cuts the hold short — measured at
    // 1497ms against a 1620ms budget. So wait for it, briefly, instead of
    // guessing.
    const readOrigin = () => {
      const a = ruleEl?.getAnimations?.()[0];
      return a && typeof a.currentTime === 'number' ? performance.now() - a.currentTime : null;
    };

    const immediate = readOrigin();
    // Reduced motion switches the animations off outright, so there is no
    // animation clock to wait for and polling would only add dead time to the
    // hold (measured ~400ms, pushing a 1.6s plate past 2s).
    const reduced =
      window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches ?? false;

    if (immediate !== null) {
      schedule(immediate);
    } else if (reduced) {
      schedule(performance.now());
    } else {
      // No animation yet. Poll for a few frames; if one never appears (the
      // reduced-motion path switches them off entirely) fall back to now,
      // which is the correct origin in that case anyway.
      const giveUpAt = performance.now() + 400;
      const waitForOrigin = () => {
        const o = readOrigin();
        if (o !== null) schedule(o);
        else if (performance.now() < giveUpAt) raf = requestAnimationFrame(waitForOrigin);
        else schedule(performance.now());
      };
      raf = requestAnimationFrame(waitForOrigin);
    }

    // Backstop. A splash that never leaves is the worst possible failure, so
    // cap the whole thing regardless of what the animation clock reports.
    const cap = setTimeout(unmount, DURATION * 3);

    return () => {
      cancelAnimationFrame(raf);
      clearTimeout(exitTimer);
      clearTimeout(doneTimer);
      clearTimeout(cap);
      root.classList.remove('splash-locked');
    };
  });

  // Zero-padded four-digit readout: 0000 -> 1560.
  $: clock = String(elapsed).padStart(4, '0');
</script>

{#if !done}
  <!-- aria-hidden + role=none: this is decoration over a page that is already
       in the DOM and readable. Screen readers should not be gated by it. -->
  <div class="splash" class:is-exiting={exiting} data-sts-splash aria-hidden="true">
    <!-- .veil carries the opaque backdrop and everything the visitor reads.
         It is hidden the instant the wipe halves have the screen covered, so
         that sliding them apart uncovers the SITE rather than uncovering the
         panel again. .splash itself must stay transparent for that reason. -->
    <div class="veil">
      <div class="field">
        <div class="grid"></div>
        <div class="vignette"></div>
        <div class="playhead"></div>
      </div>

      <div class="panel">
        <span class="corner tl"></span>
        <span class="corner tr"></span>
        <span class="corner bl"></span>
        <span class="corner br"></span>

        <header class="hud">
          <span class="hud-mark">SURVIVING&nbsp;THE&nbsp;SINGULARITY</span>
          <span class="hud-clock">T+{clock}<i>MS</i></span>
        </header>

        <p class="hud-task">MAPPING THE NINE STAGES</p>

        <ol class="stages">
          {#each STAGES as stage, i}
            <li style="--i:{i}">
              <span class="ix">{String(i + 1).padStart(2, '0')}</span>
              <span class="nm">{stage}</span>
              <span class="bar"><i></i></span>
              <span class="ok">OK</span>
            </li>
          {/each}
        </ol>

        <!-- A div, not a <footer>. This stamp is decoration inside the boot
             overlay, but <footer> is a contentinfo landmark, so using one here
             put a second contentinfo on every page alongside the real site
             footer. Screen readers announced two, and locator('footer') failed
             Playwright strict mode with "resolved to 2 elements", which is what
             broke f-legal-compliance and e-mobile-design on all three engines. -->
        <div class="stamp">
          <span class="stamp-box">SIGNAL ACQUIRED</span>
          <span class="stamp-sub">9/9 MAPPED &middot; THE FUTURE ISN'T COMING</span>
        </div>
      </div>

      <div class="rule"><i bind:this={ruleEl}></i></div>
      <div class="seam"></div>
    </div>

    <div class="flash"></div>
  </div>
{/if}

<style>
  /* ---------------------------------------------------------------------
     Timing. --t is the single source of truth; every delay below is a
     fraction of it, so rescaling the budget rescales the whole sequence.
     Keep in sync with DURATION in the script block.
     --------------------------------------------------------------------- */
  .splash {
    --t: 1560ms;
    --amber: #f59e0b;
    --blue: #3b82f6;
    --ink: #020617;
    --row-step: calc(var(--t) / 14.4); /* ~108ms between stage rows */
    --row-lead: calc(var(--t) / 12);   /* ~130ms before row 1 lands   */

    position: fixed;
    inset: 0;
    z-index: 2147483647;
    /* Deliberately TRANSPARENT. The opaque backdrop belongs to .veil, which
       is hidden before the wipe halves slide apart — otherwise the wipe would
       uncover this background instead of the site. */
    background: transparent;
    overflow: hidden;
    font-family: 'JetBrains Mono', ui-monospace, 'Courier New', monospace;
    contain: layout paint;

    /* Escape hatch. The component normally removes this node from the DOM,
       but that requires hydration to have happened. If the JS bundle fails,
       404s, or is blocked, nothing else would ever uncover the page — a
       full-screen opaque overlay is the worst possible failure, so CSS alone
       takes it out of the way on schedule.

       Two measured constraints on how this is written (Chrome, preview build,
       2026-08-01). A 0.001s duration does not reliably apply its forwards
       fill at all — that left the no-JS page stuck behind the overlay. And
       `visibility` under `linear` timing flips almost immediately rather than
       at 50% progress, which would hide the overlay ~50ms early and cut the
       tail off the wipe. steps(1, end) holds `visible` for the whole active
       phase and flips exactly at delay + duration.

       The delay starts AFTER the wipe has finished rather than straddling the
       target, so that whichever of those two semantics Chrome applies, the
       flip lands somewhere in [t+40, t+140] and can never clip the wipe. */
    animation: splashOut 100ms steps(1, end) forwards;
    animation-delay: calc(var(--t) + 40ms);
  }

  @keyframes splashOut {
    to { visibility: hidden; pointer-events: none; }
  }

  /* The backdrop and everything readable, and — importantly — the ONLY thing
     that performs the exit.

     The exit was originally three coordinated animations: two opaque halves
     that had to turn on, then a veil that had to hide inside the gap before
     the halves slid apart. Getting that ordering right depended on Chrome's
     interpolation semantics for `visibility` and on the endpoint behaviour of
     stepped timing functions, and three consecutive probe runs of the same
     build produced three different verdicts. Sub-100ms ordering between five
     independent animations is not something to assert; it is something to
     design away. One element, one animation, nothing to sequence.

     The clip-path collapses the whole boot screen to a horizontal line and
     out, so the site arrives on a hard cut rather than a fade — the CRT
     power-off read, which suits the terminal framing. It is a TRANSITION
     fired by .is-exiting, not a delayed animation, so its timing comes from
     the component's single clock. */
  .veil {
    position: absolute;
    inset: 0;
    background: var(--ink);
    display: grid;
    place-items: center;
    overflow: hidden;
    clip-path: inset(0 0 0 0);
    transition: clip-path 170ms cubic-bezier(0.7, 0, 0.2, 1);
  }

  .splash.is-exiting .veil {
    clip-path: inset(50% 0 50% 0);
  }

  /* ---- field: grid, vignette, sweeping playhead ---------------------- */

  .field {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .grid {
    position: absolute;
    inset: -2px;
    background-image:
      linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
      linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
    background-size: 48px 48px;
    opacity: 0;
    transform: scale(1.06);
    animation: gridIn calc(var(--t) / 5) cubic-bezier(0.2, 0.9, 0.1, 1) forwards;
  }

  .vignette {
    position: absolute;
    inset: 0;
    background: radial-gradient(120% 90% at 50% 45%, transparent 35%, rgba(2, 6, 23, 0.9) 100%);
  }

  /* Amber playhead sweeping left to right across the full hold. Reads as the
     thing "doing" the loading — the stage rows resolve as it passes them. */
  .playhead {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    width: 2px;
    background: var(--amber);
    box-shadow: 0 0 24px 4px rgba(245, 158, 11, 0.5);
    opacity: 0;
    transform: translate3d(0, 0, 0);
    animation: sweep var(--t) linear forwards;
  }

  @keyframes gridIn {
    to { opacity: 1; transform: scale(1); }
  }

  @keyframes sweep {
    0%   { opacity: 0; transform: translate3d(0, 0, 0); }
    6%   { opacity: 0.85; }
    88%  { opacity: 0.85; }
    100% { opacity: 0; transform: translate3d(100vw, 0, 0); }
  }

  /* ---- panel -------------------------------------------------------- */

  .panel {
    position: relative;
    width: min(560px, calc(100vw - 3rem));
    padding: 1.25rem 1.4rem 1.1rem;
    border: 1px solid rgba(241, 245, 249, 0.15);
    background: rgba(15, 23, 42, 0.6);
    opacity: 0;
    animation: panelIn calc(var(--t) / 8) cubic-bezier(0.2, 0.9, 0.1, 1) forwards;
  }

  @keyframes panelIn {
    from { opacity: 0; transform: translate3d(0, 6px, 0); }
    to   { opacity: 1; transform: translate3d(0, 0, 0); }
  }

  /* Hard corner brackets — the site's brutalist framing vocabulary. */
  .corner {
    position: absolute;
    width: 12px;
    height: 12px;
    border: 2px solid var(--amber);
    opacity: 1;
    animation: cornerIn calc(var(--t) / 10) steps(1, end) backwards;
    animation-delay: calc(var(--t) / 13);
  }
  .tl { top: -1px; left: -1px; border-right: 0; border-bottom: 0; }
  .tr { top: -1px; right: -1px; border-left: 0; border-bottom: 0; }
  .bl { bottom: -1px; left: -1px; border-right: 0; border-top: 0; }
  .br { bottom: -1px; right: -1px; border-left: 0; border-top: 0; }

  @keyframes cornerIn { from { opacity: 0; } }

  .hud {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(241, 245, 249, 0.12);
  }

  .hud-mark {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: #f1f5f9;
    white-space: nowrap;
    overflow: hidden;
  }

  .hud-clock {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--amber);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }
  .hud-clock i {
    font-style: normal;
    opacity: 0.55;
    margin-left: 1px;
  }

  .hud-task {
    margin: 0.55rem 0 0.6rem;
    font-size: 0.56rem;
    letter-spacing: 0.24em;
    color: #dde4ef;
    opacity: 0.55;
  }

  /* ---- stage rows ---------------------------------------------------- */

  .stages {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 3px;
  }

  .stages li {
    display: grid;
    grid-template-columns: 1.9rem minmax(0, 1fr) 5.5rem 1.5rem;
    align-items: center;
    gap: 0.55rem;
    padding: 2px 4px;
    opacity: 0;
    transform: translate3d(-8px, 0, 0);
    /* Row i lands one --row-step after row i-1. Nine rows finish at ~1.18s,
       leaving the last ~0.38s for the stamp and the wipe. */
    animation: rowIn calc(var(--t) / 9) cubic-bezier(0.2, 0.9, 0.1, 1) forwards;
    animation-delay: calc(var(--row-lead) + var(--i) * var(--row-step));
  }

  @keyframes rowIn {
    0%   { opacity: 0; transform: translate3d(-8px, 0, 0); background: rgba(245, 158, 11, 0.28); }
    40%  { opacity: 1; transform: translate3d(0, 0, 0); background: rgba(245, 158, 11, 0.28); }
    100% { opacity: 1; transform: translate3d(0, 0, 0); background: transparent; }
  }

  .ix {
    font-size: 0.58rem;
    font-weight: 700;
    color: var(--blue);
    letter-spacing: 0.04em;
  }

  .nm {
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    color: #f1f5f9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Segmented fill bar — twelve hard ticks rather than a smooth gradient,
     so it reads as instrumentation instead of a progress widget. */
  .bar {
    position: relative;
    height: 7px;
    background: repeating-linear-gradient(
      90deg,
      rgba(148, 163, 184, 0.22) 0 4px,
      transparent 4px 6px
    );
  }
  /* The resting state is the BASE style, and the keyframe only supplies the
     `from` side. Do not rewrite this as 0 -> 1 with fill-mode forwards: a
     stepped timing function is not guaranteed to land on its final step, and
     measurably does not — rows 8 and 9 came to rest at scaleX 0.9166 (11/12)
     while already reporting OK, i.e. a visibly unfilled bar next to a green
     label. Measured in Chrome on the preview build, 2026-08-01. `backwards`
     supplies scaleX(0) during the delay; after the run the element simply
     falls back to scaleX(1) below, which no timing function can round off. */
  .bar i {
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      90deg,
      var(--amber) 0 4px,
      transparent 4px 6px
    );
    transform: scaleX(1);
    transform-origin: left center;
    animation: barFill calc(var(--t) / 11) steps(12, end) backwards;
    animation-delay: calc(var(--row-lead) + var(--i) * var(--row-step));
  }

  @keyframes barFill { from { transform: scaleX(0); } }

  @keyframes fill { to { transform: scaleX(1); } }

  .ok {
    font-size: 0.52rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--amber);
    text-align: right;
    /* Base-state pattern, same reasoning as .bar i above. */
    opacity: 1;
    animation: okIn calc(var(--t) / 26) steps(1, end) backwards;
    /* One row-step after the row lands: the bar has finished filling. */
    animation-delay: calc(var(--row-lead) + var(--i) * var(--row-step) + var(--t) / 11);
  }

  @keyframes okIn { from { opacity: 0; } }

  /* ---- stamp --------------------------------------------------------- */

  .stamp {
    margin-top: 0.7rem;
    padding-top: 0.6rem;
    border-top: 1px solid rgba(241, 245, 249, 0.12);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
  }

  .stamp-box {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    color: var(--ink);
    background: var(--amber);
    padding: 4px 9px;
    box-shadow: 3px 3px 0 rgba(59, 130, 246, 0.9);
    opacity: 0;
    transform: scale(1.35);
    /* Lands right after stage 09 reports OK. */
    animation: stampIn calc(var(--t) / 13) cubic-bezier(0.2, 1.4, 0.3, 1) forwards;
    animation-delay: calc(var(--t) * 0.76);
  }

  @keyframes stampIn {
    from { opacity: 0; transform: scale(1.35); }
    to   { opacity: 1; transform: scale(1); }
  }

  .stamp-sub {
    font-size: 0.5rem;
    letter-spacing: 0.14em;
    color: #dde4ef;
    opacity: 0;
    text-align: right;
    white-space: nowrap;
    overflow: hidden;
    animation: subIn calc(var(--t) / 13) ease-out forwards;
    animation-delay: calc(var(--t) * 0.79);
  }

  @keyframes subIn { to { opacity: 0.55; } }

  /* ---- literal progress rule, pinned to the viewport bottom ---------- */

  .rule {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 3px;
    background: rgba(148, 163, 184, 0.14);
  }
  .rule i {
    display: block;
    height: 100%;
    background: var(--amber);
    transform: scaleX(0);
    transform-origin: left center;
    animation: fill var(--t) cubic-bezier(0.35, 0, 0.2, 1) forwards;
  }

  /* ---- exit: flash frame, then a hard two-panel wipe ------------------ */

  /* One amber frame on the cut. No fill mode in either direction: the resting
     value is the base opacity 0, both before the delay and after the run. */
  .flash {
    position: absolute;
    inset: 0;
    background: var(--amber);
    opacity: 0;
    pointer-events: none;
    z-index: 3;
    animation: flash calc(var(--t) / 26) steps(1, end);
    animation-delay: calc(var(--t) - var(--t) / 9 - var(--t) / 26);
  }

  @keyframes flash {
    0%   { opacity: 0.5; }
    100% { opacity: 0; }
  }

  /* The seam the boot screen splits along. Sits at the vertical centre inside
     .veil, so the clip-path keeps it exactly on the parting edge. */
  .seam {
    position: absolute;
    left: 0;
    right: 0;
    top: 50%;
    height: 2px;
    margin-top: -1px;
    background: var(--amber);
    box-shadow: 0 0 20px 3px rgba(245, 158, 11, 0.55);
    opacity: 0;
  }

  .splash.is-exiting .seam { opacity: 1; }

  /* ---------------------------------------------------------------------
     Reduced motion: same 1.56s budget, no movement. A static plate that
     states what is happening, with only opacity changing.
     --------------------------------------------------------------------- */
  @media (prefers-reduced-motion: reduce) {
    /* app.css already forces animation-duration to 0.001ms globally under this
       query, and a 0.001s animation does not reliably apply a forwards fill in
       Chrome. So do not leave any of these depending on one — switch them off
       and state the resting value outright. Teardown falls to the component's
       timer, which is JS; the CSS escape hatch is not available here. */
    .splash { animation: none; }
    .veil { animation: none; }
    .seam { display: none; }
    .grid { animation: none; opacity: 1; transform: none; }
    .playhead,
    .flash { display: none; }
    .panel { animation: none; opacity: 1; transform: none; }
    .corner { animation: none; opacity: 1; }
    .stages li {
      animation: none;
      opacity: 1;
      transform: none;
      background: transparent;
    }
    .bar i { animation: none; transform: scaleX(1); }
    .ok { animation: none; opacity: 1; }
    .stamp-box { animation: none; opacity: 1; transform: none; }
    .stamp-sub { animation: none; opacity: 0.55; }
    .rule i { animation: none; transform: scaleX(1); }
  }

  @media (max-width: 520px) {
    .panel { padding: 1rem 0.9rem 0.9rem; }
    /* The stage names ARE the content, so the fixed columns give up width to
       them here. At the previous 1.7/3.2/1.4rem split the longest names
       ellipsised ("THE PANIC AND THE…"); this fits all nine. */
    .stages li { grid-template-columns: 1.5rem minmax(0, 1fr) 2.6rem 1.3rem; gap: 0.3rem; }
    .hud-mark { font-size: 0.52rem; letter-spacing: 0.12em; }
    .nm { font-size: 0.54rem; letter-spacing: 0.04em; }
    .stamp { flex-direction: column; align-items: flex-start; gap: 0.4rem; }
    .stamp-sub { text-align: left; }
  }
</style>
