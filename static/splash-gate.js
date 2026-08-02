/* splash-gate.js — the pre-paint half of the 1.56s boot sequence
 * (see src/lib/components/SplashLoader.svelte for the visual half).
 *
 * This runs render-blocking from <head>, before anything paints, and owns
 * three things the Svelte component cannot own because it does not exist yet:
 *
 *   1. THE DECISION. Stamps html[data-splash="play"|"skip"] so app.css can
 *      hide the SSR'd overlay before it flashes for a returning visitor.
 *   2. THE SCROLL LOCK, and its release. Both belong here rather than in the
 *      component: the lock has to be true from the first frame rather than
 *      from hydration, and whatever applies a lock must be able to release it
 *      without depending on a bundle that might never load.
 *   3. THE SEEN-FLAG, written immediately so a visitor who navigates away
 *      mid-sequence still counts as having seen it.
 *
 * It also records window.__stsSplash.t0 at head-parse time. Nothing depends on
 * that for correctness — the component derives its clock from the CSS
 * animation's own currentTime — but scripts/probe_splash.mjs uses it to
 * separate time-to-first-paint from the length of the visible sequence.
 *
 * It has to be an external file rather than an inline <script>: the site ships
 * `script-src 'self'` with a SvelteKit nonce (svelte.config.js for SSR routes,
 * static/_headers for prerendered ones), and a hand-written inline block in
 * app.html is blocked outright.
 *
 *   ?splash=force  replay it (demos, screenshots)
 *   ?splash=off    skip it entirely
 *   otherwise      once per browser session
 *
 * If this file ever fails to load, data-splash is never set, SplashLoader
 * unmounts itself on hydration and the site renders normally. The failure mode
 * is "no splash", never "stuck behind a splash".
 */
(function () {
  var KEY = 'sts:splash';
  var doc = document.documentElement;
  var mode = 'play';

  try {
    var q = new URLSearchParams(location.search).get('splash');
    if (q === 'off') mode = 'skip';
    else if (q === 'force') sessionStorage.removeItem(KEY);
    else if (sessionStorage.getItem(KEY)) mode = 'skip';
  } catch (e) {
    // Storage blocked (private mode, strict cookie policy). Playing is the
    // safe default; it just replays each navigation rather than throwing.
  }

  doc.setAttribute('data-splash', mode);

  if (mode !== 'play') return;

  // Navigation-time reference point. Informational; see the header note.
  window.__stsSplash = { t0: performance.now() };

  // Locked from the first frame, not from hydration.
  doc.classList.add('splash-locked');

  // Written now rather than at teardown so a visitor who navigates away
  // mid-sequence is still counted as having seen it.
  try {
    sessionStorage.setItem(KEY, 'seen');
  } catch (e) {
    // See above — a replaying splash beats a thrown error during head parsing.
  }

  // Failsafe release. SplashLoader normally lifts the lock when it unmounts,
  // which is the path that runs in practice — this only matters when
  // hydration never happens (bundle 404, JS disabled after the gate ran, a
  // throwing sibling component). Paired with the splashOut keyframe, which
  // hides the overlay on the same schedule, it guarantees no visitor is left
  // staring at an unscrollable boot screen. Generous margin so it never
  // races the normal path; removing an absent class is a no-op either way.
  setTimeout(function () {
    doc.classList.remove('splash-locked');
  }, 4000);
})();
