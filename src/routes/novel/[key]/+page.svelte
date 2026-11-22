<script>
  import { onMount } from 'svelte';
  import { novel, groupedSections } from '$lib/novel/novelContent.js';
  import { readPlace } from '$lib/novel/novelReader.js';
  import ReaderControls from './ReaderControls.svelte';

  export let data;

  const groups = groupedSections();
  const totalWords = novel.sections.reduce((n, s) => n + s.words, 0);
  let place = null;
  $: placeSection = place && novel.sections.find((s) => s.id === place.id);
  onMount(() => { place = readPlace(); });
</script>

<main class="novel-index">
  <div class="top"><ReaderControls /></div>

  <header class="title-page">
    <h1>{novel.title}</h1>
    <p class="subtitle"><em>{novel.subtitle}</em></p>
    <p class="author">{novel.author}</p>
    <p class="meta">Revised manuscript, version 2 · about {Math.round(totalWords / 1000)},000 words</p>
  </header>

  <div class="start">
    {#if placeSection}
      <a class="primary" href="{data.base}/{placeSection.id}?resume=1">Continue: {placeSection.title}</a>
      <a class="secondary" href="{data.base}/{novel.sections[0].id}">Start from the beginning</a>
    {:else}
      <a class="primary" href="{data.base}/{novel.sections[0].id}">Start reading</a>
    {/if}
    <a class="secondary" href="{data.base}/compendium">Compendium: the people, places and things</a>
  </div>

  <nav aria-label="Contents" class="toc">
    {#each groups as group}
      <section>
        <h2>{group.label}</h2>
        <ol>
          {#each group.items as item}
            <li>
              <a href="{data.base}/{item.id}" class:current={place?.id === item.id}>
                <span class="t">{item.title}</span>
                <span class="m">{Math.max(1, Math.round(item.words / 250))} min</span>
              </a>
            </li>
          {/each}
        </ol>
      </section>
    {/each}
  </nav>
</main>

<style>
  .novel-index {
    max-width: 640px;
    margin: 0 auto;
    padding: 8px 16px 64px;
    font-family: Inter, system-ui, sans-serif;
  }
  .top { display: flex; justify-content: flex-end; }
  .title-page { text-align: center; padding: 28px 0 20px; }
  h1 {
    font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    font-size: clamp(28px, 8vw, 40px);
    line-height: 1.15;
    letter-spacing: 0.02em;
    margin: 0 0 10px;
    color: var(--ink);
  }
  .subtitle { margin: 0 0 6px; color: var(--muted); font-size: 18px; font-family: Georgia, serif; }
  .author { margin: 0 0 12px; font-weight: 600; }
  .meta { margin: 0; color: var(--muted); font-size: 13px; }
  .start { display: flex; flex-direction: column; gap: 10px; margin: 12px 0 32px; }
  .primary, .secondary {
    display: block;
    text-align: center;
    padding: 14px 16px;
    border-radius: 10px;
    font-weight: 700;
    text-decoration: none;
  }
  .primary { background: var(--accent); color: var(--accent-ink); }
  .secondary { border: 1px solid var(--rule); color: var(--ink); }
  .toc h2 {
    font: 800 11px/1.2 'JetBrains Mono', ui-monospace, monospace;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--accent);
    margin: 24px 0 8px;
  }
  .toc ol { list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--rule); }
  .toc li { border-bottom: 1px solid var(--rule); }
  .toc a {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 13px 2px;
    color: var(--ink);
    text-decoration: none;
    font-size: 16px;
    line-height: 1.35;
  }
  .toc a.current .t { color: var(--accent); font-weight: 700; }
  .toc .m { color: var(--muted); font-size: 13px; white-space: nowrap; padding-top: 2px; }
</style>
