<script>
  import { offer } from '$lib/offer.js';
  import { stats, eyebrow } from '$lib/stats.js';
  import BuyButton from './BuyButton.svelte';

  // CSS handles the smooth scroll. What CSS cannot do is move keyboard focus,
  // and an anchor that moves the viewport without moving focus strands anyone
  // navigating by keyboard.
  function onExplore() {
    setTimeout(() => {
      /** @type {HTMLElement | null} */
      const tab = document.querySelector('#precedent .tab');
      tab?.focus({ preventScroll: true });
    }, 500);
  }
</script>

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">
      <span class="dot" aria-hidden="true"></span>
      {eyebrow}
    </p>

    <h1 class="hero-h1">
      Most books about AI are wrong within a year.<br />
      <em>This one gets corrected.</em>
    </h1>

    <!-- Verbatim from the offer object. Never retyped here. -->
    <p class="hero-offer">{offer.sentence}</p>

    <div class="hero-actions">
      <BuyButton />
      <a class="btn btn-ghost" href="#precedent" onclick={onExplore}>
        Explore the Precedent File
        <span class="arrow" aria-hidden="true">&rarr;</span>
      </a>
    </div>

    <p class="hero-foot">No subscription. No tiers. No upsell after this one.</p>

    <ul class="stats" aria-label="Verifiable project statistics">
      {#each stats as s (s.key)}
        <li class="stat">
          <span class="stat-n">{s.value}</span>
          <span class="stat-l">{s.label}</span>
          <!-- Provenance is rendered, not hidden in a tooltip. -->
          <span class="stat-src">{s.source}</span>
        </li>
      {/each}
    </ul>
  </div>
</section>

<style>
  .hero {
    padding: clamp(56px, 9vw, 104px) 0 clamp(40px, 6vw, 72px);
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    font: 500 13px/1 var(--mono);
    letter-spacing: 0.03em;
    color: var(--text-3);
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 8px 14px;
    margin: 0 0 26px;
  }
  .dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--ok);
    box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.15);
  }

  .hero-h1 {
    font: 600 clamp(34px, 6.2vw, 62px)/1.08 var(--serif);
    letter-spacing: -0.025em;
    margin: 0 0 24px;
    max-width: 19ch;
    text-wrap: balance;
  }
  .hero-h1 em {
    color: var(--accent);
    font-style: italic;
  }

  .hero-offer {
    font-size: clamp(17px, 2vw, 20px);
    line-height: 1.6;
    color: var(--text-2);
    max-width: 62ch;
    margin: 0 0 32px;
  }

  .hero-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 14px;
  }

  .hero-foot {
    font: 400 14px/1.5 var(--sans);
    color: var(--text-3);
    margin: 0 0 48px;
  }

  .stats {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: var(--r);
    overflow: hidden;
  }

  .stat {
    background: var(--surface);
    padding: 20px 20px 18px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .stat-n {
    font: 600 clamp(26px, 3.2vw, 34px)/1 var(--mono);
    letter-spacing: -0.02em;
    color: var(--text);
  }
  .stat-l {
    font-size: 14.5px;
    color: var(--text-2);
  }
  .stat-src {
    font: 400 12px/1.4 var(--mono);
    color: var(--text-3);
    margin-top: 4px;
  }

  @media (max-width: 940px) {
    .stats { grid-template-columns: repeat(2, 1fr); }
  }
  @media (max-width: 700px) {
    .hero-actions :global(.btn) { width: 100%; }
  }
  @media (max-width: 460px) {
    .stats { grid-template-columns: 1fr; }
  }
</style>
