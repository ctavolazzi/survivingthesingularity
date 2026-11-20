<script>
  import { onMount, tick } from 'svelte';
  import { afterNavigate } from '$app/navigation';
  import { page } from '$app/stores';
  import { readPlace, savePlace } from '$lib/novel/novelReader.js';
  import ReaderControls from '../ReaderControls.svelte';

  export let data;

  let article;
  let progress = 0;
  let saveTimer;

  function measure() {
    if (!article) return 0;
    const top = article.getBoundingClientRect().top + window.scrollY;
    const span = Math.max(1, article.offsetHeight - window.innerHeight * 0.6);
    return Math.min(1, Math.max(0, (window.scrollY - top + window.innerHeight * 0.3) / span));
  }

  function onScroll() {
    progress = measure();
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => savePlace(data.section.id, measure()), 250);
  }

  // SvelteKit reuses this component between sections, so place handling runs
  // after every navigation, not only on mount.
  afterNavigate(async () => {
    await tick();
    const place = readPlace();
    const resume = $page.url.searchParams.has('resume');
    if (resume && place && place.id === data.section.id && place.ratio > 0.01 && article) {
      const top = article.getBoundingClientRect().top + window.scrollY;
      const span = Math.max(1, article.offsetHeight - window.innerHeight * 0.6);
      window.scrollTo(0, top + place.ratio * span - window.innerHeight * 0.3);
    } else {
      savePlace(data.section.id, 0);
    }
    progress = measure();
  });

  onMount(() => {
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => {
      window.removeEventListener('scroll', onScroll);
      clearTimeout(saveTimer);
      if (article) savePlace(data.section.id, measure());
    };
  });
</script>

<div class="progress" aria-hidden="true"><span style="transform: scaleX({progress})"></span></div>

<main class="reader">
  <div class="bar">
    <a class="contents" href="/novel">
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M8 2L4 6l4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
      Contents
    </a>
    <ReaderControls />
  </div>

  <header class="head">
    <p class="group">{data.section.group}</p>
    <h1>{data.section.title}</h1>
  </header>

  <article class="prose-novel" bind:this={article}>
    {@html data.html}
  </article>

  <nav class="pager" aria-label="Chapters">
    {#if data.next}
      <a class="next" href="/novel/{data.next.id}">
        <span class="k">Next</span>
        <span class="v">{data.next.title}</span>
      </a>
    {:else}
      <a class="next" href="/novel"><span class="k">The end</span><span class="v">Back to contents</span></a>
    {/if}
    {#if data.prev}
      <a class="prev" href="/novel/{data.prev.id}">
        <span class="k">Previous</span>
        <span class="v">{data.prev.title}</span>
      </a>
    {/if}
    <p class="count">{data.position} of {data.total}</p>
  </nav>
</main>

<style>
  .progress {
    position: fixed;
    left: 0; right: 0; bottom: 0;
    height: 3px;
    z-index: 40;
    pointer-events: none;
  }
  .progress span {
    display: block;
    height: 100%;
    background: var(--accent);
    transform-origin: left;
  }
  .reader {
    max-width: 38em;
    margin: 0 auto;
    padding: 8px 18px 72px;
    box-sizing: border-box;
  }
  .bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    font-family: Inter, system-ui, sans-serif;
  }
  .contents {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-height: 40px;
    color: var(--muted);
    text-decoration: none;
    font-weight: 600;
    font-size: 15px;
  }
  .head { margin: 28px 0 24px; text-align: center; }
  .group {
    margin: 0 0 10px;
    font: 800 11px/1.3 'JetBrains Mono', ui-monospace, monospace;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--accent);
  }
  h1 {
    margin: 0;
    font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    font-weight: 700;
    font-size: calc(var(--novel-size) * 1.45);
    line-height: 1.2;
    color: var(--ink);
  }
  .prose-novel {
    font-family: Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Times New Roman', serif;
    font-size: var(--novel-size);
    line-height: 1.7;
    color: var(--ink);
    overflow-wrap: break-word;
    hyphens: auto;
    -webkit-text-size-adjust: 100%;
  }
  .prose-novel :global(p) { margin: 0 0 1em; }
  .prose-novel :global(em) { font-style: italic; }
  .prose-novel :global(strong) { font-weight: 700; }
  .prose-novel :global(h2) {
    font-size: 1.15em;
    line-height: 1.3;
    margin: 1.8em 0 0.7em;
    color: var(--ink);
  }
  .prose-novel :global(hr) {
    border: 0;
    height: 1.2em;
    margin: 1.6em 0;
    text-align: center;
    overflow: visible;
  }
  .prose-novel :global(hr)::after {
    content: '\00B7\2003\00B7\2003\00B7';
    color: var(--muted);
    font-size: 1.1em;
    line-height: 1;
  }
  .prose-novel :global(figure.novel-figure) { margin: 1.8em -18px; }
  .prose-novel :global(figure.novel-figure img) {
    display: block;
    width: 100%;
    height: auto;
    border-radius: 0;
  }
  .prose-novel :global(figcaption) {
    margin: 0.7em 18px 0;
    text-align: center;
    font-size: 0.85em;
    line-height: 1.45;
    color: var(--muted);
  }
  @media (min-width: 640px) {
    .prose-novel :global(figure.novel-figure) { margin: 2em 0; }
    .prose-novel :global(figure.novel-figure img) { border-radius: 8px; }
    .prose-novel :global(figcaption) { margin: 0.7em 0 0; }
  }
  .pager {
    margin-top: 48px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-family: Inter, system-ui, sans-serif;
  }
  .pager a {
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding: 14px 16px;
    border-radius: 10px;
    text-decoration: none;
    border: 1px solid var(--rule);
    color: var(--ink);
  }
  .pager a.next { background: var(--accent); color: var(--accent-ink); border-color: transparent; }
  .pager .k { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.8; }
  .pager .v { font-size: 16px; font-weight: 700; line-height: 1.3; }
  .count { text-align: center; color: var(--muted); font-size: 13px; margin: 6px 0 0; }
</style>
