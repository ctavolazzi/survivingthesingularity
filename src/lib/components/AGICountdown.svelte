<script>
  import { onMount, onDestroy } from 'svelte';

  // ── DISCLAIMER ──────────────────────────────────────────────────────────────
  // This is an ILLUSTRATIVE countdown to a *predicted* AGI horizon. The target
  // date is an aggregate framing of publicly stated expert predictions as of 2025
  // - it is NOT a forecast, guarantee, or claim that AGI will arrive on this date.
  // Expert predictions vary enormously and are frequently wrong.
  // ────────────────────────────────────────────────────────────────────────────

  // Illustrative "commonly predicted" horizon. Override via prop.
  export let targetDate = new Date('2027-11-25T00:00:00Z');
  export let label = 'The AGI horizon';
  // compact = slim variant for the home page
  export let compact = false;

  let now = new Date();
  let interval;

  let years = 0;
  let days = 0;
  let hours = 0;
  let minutes = 0;
  let seconds = 0;
  let mounted = false;

  onMount(() => {
    mounted = true;
    interval = setInterval(() => { now = new Date(); }, 1000);
  });

  onDestroy(() => { if (interval) clearInterval(interval); });

  $: diff = targetDate - now;
  $: {
    if (diff > 0) {
      let s = Math.floor(diff / 1000);
      seconds = s % 60;
      let m = Math.floor(s / 60);
      minutes = m % 60;
      let h = Math.floor(m / 60);
      hours = h % 24;
      let d = Math.floor(h / 24);
      // 365-day years, illustrative only
      years = Math.floor(d / 365);
      days = d % 365;
    } else {
      years = days = hours = minutes = seconds = 0;
    }
  }

  $: targetYear = targetDate.getUTCFullYear();
  $: elapsed = diff <= 0;

  // Lead with years. Days/hours/minutes/seconds follow and keep it ticking.
  $: units = [
    { value: years, label: years === 1 ? 'Year' : 'Years', pad: false, accent: true },
    { value: days, label: days === 1 ? 'Day' : 'Days', pad: false },
    { value: hours, label: 'Hrs', pad: true },
    { value: minutes, label: 'Min', pad: true },
    { value: seconds, label: 'Sec', pad: true, sec: true },
  ];
</script>

<div class="agi-countdown" class:compact>
  <div class="ac-glow"></div>

  <div class="ac-eyebrow">
    <span class="ac-dot"></span>
    <span>The Clock Is Running</span>
  </div>

  <h2 class="ac-heading">
    Countdown to <span class="ac-highlight">AGI</span>
  </h2>

  {#if !elapsed}
    <div class="ac-display" class:ac-ready={mounted}>
      {#each units as u, i}
        <div class="ac-block" class:ac-block-sec={u.sec} class:ac-block-accent={u.accent}>
          <span class="ac-value">{u.pad ? String(u.value).padStart(2, '0') : u.value.toLocaleString()}</span>
          <span class="ac-label">{u.label}</span>
        </div>
        {#if i < units.length - 1}
          <div class="ac-sep" aria-hidden="true">:</div>
        {/if}
      {/each}
    </div>

    {#if compact}
      <a class="ac-learn" href="/why">Read why {targetYear} →</a>
    {:else}
      <p class="ac-target">Counting down to <strong>{targetYear}</strong>: {label}</p>
    {/if}
  {:else}
    <div class="ac-elapsed">
      <span class="ac-value">0</span>
      <p>The horizon has passed.</p>
    </div>
  {/if}
</div>

<style>
  .agi-countdown {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.06) 0%, rgba(15, 23, 42, 0.85) 55%, rgba(2, 6, 23, 0.95) 100%);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 20px;
    padding: clamp(1.5rem, 4vw, 2.75rem) clamp(1rem, 3vw, 2rem);
    text-align: center;
  }

  .ac-glow {
    position: absolute;
    top: -40%;
    left: 50%;
    transform: translateX(-50%);
    width: 700px;
    max-width: 130%;
    height: 400px;
    background: radial-gradient(ellipse, rgba(245, 158, 11, 0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .agi-countdown > :not(.ac-glow) { position: relative; z-index: 1; }

  .ac-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: clamp(0.5rem, 1.6vw, 0.6rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #f59e0b;
    font-family: var(--font-primary);
    margin-bottom: 0.9rem;
  }

  .ac-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #f59e0b;
    box-shadow: 0 0 8px #f59e0b;
    animation: ac-pulse 2s ease-in-out infinite;
    flex-shrink: 0;
  }

  @keyframes ac-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.75); }
  }

  @media (prefers-reduced-motion: reduce) {
    .ac-dot { animation: none; }
  }

  .ac-heading {
    font-size: clamp(1.25rem, 4.5vw, 2.2rem);
    font-weight: 900;
    color: #f8fafc;
    letter-spacing: -0.04em;
    margin: 0 0 1.5rem;
    line-height: 1.12;
  }

  .ac-highlight { color: #f59e0b; }

  /* Countdown display - always a single line; scales with viewport */
  .ac-display {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    flex-wrap: nowrap;
    width: 100%;
    gap: clamp(0.15rem, 1.2vw, 0.9rem);
    margin: 0 0 1.35rem;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .ac-display.ac-ready { opacity: 1; transform: none; }

  .ac-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    flex: 0 1 auto;
    min-width: 0;
  }

  .ac-value {
    font-size: clamp(1.1rem, 7vw, 4rem);
    font-weight: 900;
    color: #fbbf24;
    font-family: var(--font-primary);
    line-height: 0.95;
    letter-spacing: -0.04em;
    font-variant-numeric: tabular-nums;
    text-shadow: 0 0 30px rgba(245, 158, 11, 0.25);
    white-space: nowrap;
  }

  /* Years block gets the spotlight */
  .ac-block-accent .ac-value {
    font-size: clamp(1.4rem, 8.5vw, 5rem);
    color: #fcd34d;
  }
  .ac-block-sec .ac-value { color: #f59e0b; opacity: 0.8; }

  .ac-label {
    font-size: clamp(0.4rem, 1.4vw, 0.7rem);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #e9eef5;
    font-family: var(--font-primary);
    font-weight: 600;
    white-space: nowrap;
  }

  .ac-sep {
    font-size: clamp(0.9rem, 5vw, 3rem);
    font-weight: 700;
    color: rgba(245, 158, 11, 0.3);
    font-family: var(--font-primary);
    line-height: 1;
    padding-top: 0.1em;
    align-self: flex-start;
    flex: 0 0 auto;
  }

  .ac-target {
    font-size: clamp(0.82rem, 2.2vw, 0.95rem);
    color: #e9eef5;
    margin: 0 0 1.35rem;
    line-height: 1.5;
  }
  .ac-target strong {
    color: #fbbf24;
    font-family: var(--font-primary);
    font-weight: 800;
  }

  .ac-elapsed { margin: 1rem 0 1.35rem; }
  .ac-elapsed .ac-value { font-size: 3rem; display: block; }
  .ac-elapsed p { color: #dde4ef; font-size: 0.95rem; margin: 0.5rem 0 0; }

  .ac-compact-links {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 0.75rem;
  }

  .ac-learn {
    display: inline-block;
    font-size: 0.86rem;
    font-weight: 700;
    color: #fbbf24;
    text-decoration: none;
    font-family: var(--font-primary);
    margin-bottom: 0;
    transition: opacity 0.15s;
  }
  .ac-learn:hover { opacity: 0.75; }

  .ac-learn-timeline {
    color: #e2e8f0;
  }

  .ac-disclaimer {
    font-size: clamp(0.66rem, 1.8vw, 0.72rem);
    color: #dde4ef;
    line-height: 1.6;
    max-width: 520px;
    margin: 0 auto;
    font-style: italic;
    border-top: 1px solid rgba(245, 158, 11, 0.1);
    padding-top: 1rem;
  }
  .ac-disclaimer strong { color: #dde4ef; font-style: normal; }
  .ac-disclaimer a {
    color: #dde4ef;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .ac-disclaimer a:hover { color: #f59e0b; }

  .ac-disclaimer-mini {
    border-top: none;
    padding-top: 0;
    max-width: none;
  }

  /* ─── Compact variant (home page) - boxed cards like the existing site ─── */
  .agi-countdown.compact {
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 0;
    overflow: visible;
  }
  .compact .ac-glow { display: none; }
  .compact .ac-eyebrow { margin-bottom: 0.6rem; }
  .compact .ac-heading {
    font-size: clamp(0.9rem, 3vw, 1.25rem);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #e9eef5;
    margin-bottom: 1.25rem;
  }
  .compact .ac-display { gap: clamp(0.3rem, 1.5vw, 0.7rem); margin-bottom: 0.6rem; }
  .compact .ac-block { min-width: 0; gap: 0.55rem; }
  .compact .ac-value {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(46px, 13vw, 84px);
    height: clamp(46px, 13vw, 84px);
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: clamp(10px, 2.5vw, 16px);
    font-size: clamp(1.2rem, 5vw, 2.3rem);
    color: #f1f5f9;
    text-shadow: none;
  }
  .compact .ac-block-accent .ac-value {
    font-size: clamp(1.2rem, 5vw, 2.3rem);
    color: #f59e0b;
    border-color: rgba(245, 158, 11, 0.25);
    background: rgba(245, 158, 11, 0.06);
  }
  .compact .ac-block-sec .ac-value { color: #f1f5f9; opacity: 1; }
  .compact .ac-sep {
    font-size: clamp(0.9rem, 3vw, 1.4rem);
    color: rgba(148, 163, 184, 0.3);
    align-self: center;
    padding-top: 0;
    margin-bottom: 1.5rem;
  }
  .compact .ac-label { font-size: clamp(0.45rem, 1.4vw, 0.6rem); color: #dde4ef; }
  .compact .ac-target { font-size: clamp(0.72rem, 2vw, 0.82rem); margin-bottom: 0.75rem; }

  /* Tighten the full (non-compact) card on phones so the page's value
     prop sits closer to the fold. */
  @media (max-width: 640px) {
    .agi-countdown:not(.compact) { padding: 1.25rem 1rem; }
    .agi-countdown:not(.compact) .ac-eyebrow { margin-bottom: 0.6rem; }
    .agi-countdown:not(.compact) .ac-heading { margin-bottom: 0.9rem; }
    .agi-countdown:not(.compact) .ac-display { margin-bottom: 0.9rem; }
    .agi-countdown:not(.compact) .ac-target { margin-bottom: 0.85rem; }
    .agi-countdown:not(.compact) .ac-disclaimer { padding-top: 0.75rem; }
  }

  /* Stays on one line at every width; tighten spacing on small screens */
  @media (max-width: 380px) {
    .ac-display { gap: 0.1rem; }
    .ac-label { letter-spacing: 0.04em; }
  }
</style>
