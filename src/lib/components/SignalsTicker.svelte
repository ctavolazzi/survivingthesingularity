<script>
  import { onMount } from 'svelte';
  import signalsData from '$lib/data/signals.json';

  const items = signalsData.items.slice(0, 16);
  const generatedAt = signalsData.generated_at;

  $: staleHours = generatedAt
    ? Math.floor((Date.now() - new Date(generatedAt).getTime()) / 3600000)
    : null;
  $: isStale = staleHours !== null && staleHours > 48;

  let paused = false;
  let reducedMotion = false;

  onMount(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    reducedMotion = mq.matches;
    mq.addEventListener('change', e => { reducedMotion = e.matches; });
  });

  function formatDate(iso) {
    if (!iso) return '';
    return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
</script>

{#if !isStale && items.length > 0}
<section class="signals-section">
  <div class="signals-header">
    <div class="header-left">
      <span class="live-dot" aria-hidden="true"></span>
      <div class="header-text">
        <h2 class="section-heading">What researchers are working on right now</h2>
        <p class="section-sub">Papers published this week, ranked by relevance to AI acceleration and the singularity.</p>
      </div>
    </div>
    <a href="/signals" class="all-link">See all &rarr;</a>
  </div>

  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div
    class="carousel-viewport"
    on:mouseenter={() => { paused = true; }}
    on:mouseleave={() => { paused = false; }}
  >
    {#if reducedMotion}
      <div class="static-grid">
        {#each items.slice(0, 4) as item}
          <a href={item.url} target="_blank" rel="noopener noreferrer" class="card">
            <div class="card-top">
              <span class="card-tag">{item.tag}</span>
              <span class="card-date">{formatDate(item.published_at)}</span>
            </div>
            <p class="card-title">{item.title}</p>
          </a>
        {/each}
      </div>
    {:else}
      <div
        class="carousel-track"
        style="animation-play-state: {paused ? 'paused' : 'running'}"
        aria-label="Scrolling research articles"
      >
        {#each [...items, ...items] as item, i}
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            class="card"
            aria-hidden={i >= items.length ? 'true' : undefined}
            tabindex={i >= items.length ? -1 : 0}
          >
            <div class="card-top">
              <span class="card-tag">{item.tag}</span>
              <span class="card-date">{formatDate(item.published_at)}</span>
            </div>
            <p class="card-title">{item.title}</p>
          </a>
        {/each}
      </div>
    {/if}
  </div>

  <div class="signals-footer">
    <span class="footer-note">Pulled daily from arXiv · ranked algorithmically · <a href="/disclaimer#signals" class="footer-link">how it works</a></span>
    <a href="/signals" class="rss-link">Full feed &rarr;</a>
  </div>
</section>
{/if}

<style>
  .signals-section {
    width: 100%;
    padding: 3rem 0 2.5rem;
    background: #040d1a;
    border-top: 1px solid rgba(245, 158, 11, 0.1);
    border-bottom: 1px solid rgba(245, 158, 11, 0.1);
    overflow: hidden;
  }

  /* ── Header ── */
  .signals-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 0 1.5rem 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
    gap: 1.5rem;
  }

  .header-left {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .live-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #f59e0b;
    box-shadow: 0 0 8px #f59e0baa;
    flex-shrink: 0;
    margin-top: 0.45rem;
    animation: blink 2s ease-in-out infinite;
  }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }

  .header-text {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .section-heading {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0;
    line-height: 1.3;
  }

  .section-sub {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0;
    line-height: 1.4;
  }

  .all-link {
    font-size: 0.8rem;
    font-weight: 500;
    color: #f59e0b;
    text-decoration: none;
    white-space: nowrap;
    margin-top: 0.35rem;
    flex-shrink: 0;
    transition: color 0.14s;
  }
  .all-link:hover { color: #fbbf24; }

  /* ── Carousel ── */
  .carousel-viewport {
    width: 100%;
    overflow: hidden;
    cursor: default;
  }

  .carousel-track {
    display: flex;
    align-items: stretch; /* all cards match the tallest one */
    gap: 1rem;
    padding: 0.5rem 1.5rem 0.75rem;
    animation: scroll-left 120s linear infinite;
    width: max-content;
  }

  @keyframes scroll-left {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
  }

  /* ── Card ── */
  .card {
    flex-shrink: 0;
    width: 320px;
    /* No fixed height — cards grow to their content; flex stretch equalises all */
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(51, 65, 85, 0.6);
    border-radius: 8px;
    padding: 1rem 1.1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    text-decoration: none;
    transition: border-color 0.2s, background 0.2s;
    box-sizing: border-box;
  }
  .card:hover {
    border-color: rgba(245, 158, 11, 0.4);
    background: rgba(245, 158, 11, 0.04);
  }
  .card:focus-visible {
    outline: 2px solid #f59e0b;
    outline-offset: 2px;
  }

  .card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    flex-shrink: 0;
  }

  .card-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.22);
    border-radius: 3px;
    padding: 0.1rem 0.4rem;
    white-space: nowrap;
  }

  .card-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #334155;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .card-title {
    font-size: 0.82rem;
    font-weight: 500;
    color: #cbd5e1;
    line-height: 1.45;
    margin: 0;
    flex: 1;
    /* Let the title wrap fully — the tallest card sets the row height */
    white-space: normal;
    word-break: break-word;
  }
  .card:hover .card-title { color: #f1f5f9; }

  /* ── Static grid (reduced motion) ── */
  .static-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem;
    padding: 0.25rem 1.5rem 0.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  /* ── Footer ── */
  .signals-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 1.5rem 0;
    max-width: 1200px;
    margin: 0 auto;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .rss-link {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #3b82f6;
    text-decoration: none;
    transition: color 0.14s;
  }
  .rss-link:hover { color: #60a5fa; }

  .footer-note {
    font-size: 0.72rem;
    color: #334155;
  }

  .footer-link {
    color: #475569;
    text-decoration: none;
    transition: color 0.14s;
  }
  .footer-link:hover { color: #94a3b8; }
</style>
