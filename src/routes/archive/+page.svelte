<script>
  // THE ARCHIVE: the nonfiction draft (v0.11.0) the book was before it became
  // a novel. It is here because the preorder offer said, in writing, "you keep
  // everything already delivered and the archive stays readable."
  //
  // One page on purpose. This draft is finished changing, so it does not need
  // the novel's reader (reading position, progressive mounting, font controls).
  // A table of contents and the sections, each rendered when opened.
  import { renderMarkdown } from '$lib/utils/bookMarkdown.js';
  import { archiveBook, archiveSections, archiveExtras } from '$lib/archiveContent.js';
  import { downloadHref, releasedVersion } from '$lib/bookManifest.js';
  import { evolution } from '$lib/offer';
  import '$lib/styles/book-figures.css';
  import 'katex/dist/katex.min.css';

  const released = releasedVersion(archiveBook);
  const pdfHref = downloadHref(released, 'pdf');
  const epubHref = downloadHref(released, 'epub');
  const totalWords = archiveSections.reduce((sum, s) => sum + s.wordCount, 0);

  // Rendering 109,000 words of markdown up front would stall a phone. Each
  // section renders the first time it is opened and is kept after that.
  let open = {};
  const html = {};
  function toggle(section) {
    if (!html[section.id]) html[section.id] = renderMarkdown(section.raw);
    open = { ...open, [section.id]: !open[section.id] };
  }
</script>

<div class="archive">
  <header class="archive-head">
    <p class="eyebrow">Archive</p>
    <h1>The earlier draft.</h1>
    <p>{evolution.story}</p>
    <p>
      This is that nonfiction draft, version {archiveBook.version}, last updated
      {archiveBook.lastUpdated}, exactly as it was: {archiveSections.length} sections,
      {totalWords.toLocaleString()} words. It is no longer being revised.
      <a href="/book">The novel is here</a>.
    </p>
    <p class="files">
      <a href={pdfHref} download>Download the PDF</a>
      <a href={epubHref} download>Download the EPUB</a>
    </p>
  </header>

  <ol class="archive-list">
    {#each archiveSections as section}
      <li id={section.id}>
        <button type="button" class="row" aria-expanded={!!open[section.id]} on:click={() => toggle(section)}>
          <span class="row-title">{section.title}</span>
          <span class="row-meta">{section.wordCount.toLocaleString()} words</span>
        </button>
        {#if open[section.id]}
          <div class="prose">{@html html[section.id]}</div>
        {/if}
      </li>
    {/each}
  </ol>

  <h2 class="extras-heading">The Precedent File</h2>
  <p class="extras-sub">The bonus research file that came with the preorder of that draft.</p>
  <ol class="archive-list">
    {#each archiveExtras as section}
      <li id={section.id}>
        <button type="button" class="row" aria-expanded={!!open[section.id]} on:click={() => toggle(section)}>
          <span class="row-title">{section.title}</span>
          <span class="row-meta">{section.wordCount.toLocaleString()} words</span>
        </button>
        {#if open[section.id]}
          <div class="prose">{@html html[section.id]}</div>
        {/if}
      </li>
    {/each}
  </ol>
</div>

<style>
  .archive { max-width: 760px; margin: 0 auto; padding: clamp(28px, 6vw, 64px) 16px 96px; color: #cbd5e1; font-family: 'Outfit', system-ui, sans-serif; }
  .eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; letter-spacing: 0.14em; text-transform: uppercase; color: #f59e0b; margin: 0 0 10px; }
  h1 { font-size: clamp(2rem, 6vw, 3rem); font-weight: 900; color: #f8fafc; margin: 0 0 16px; letter-spacing: -0.02em; }
  .archive-head p { line-height: 1.7; margin: 0 0 14px; }
  .archive-head a { color: #f59e0b; }
  .files { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; }
  .files a { display: inline-block; padding: 10px 16px; border: 1px solid rgba(245,158,11,0.4); border-radius: 8px; text-decoration: none; font-weight: 700; }
  .extras-heading { margin: 56px 0 6px; font-size: 1.5rem; font-weight: 900; color: #f8fafc; }
  .extras-sub { margin: 0; line-height: 1.6; }
  .extras-sub + .archive-list { margin-top: 20px; }
  .archive-list { list-style: none; padding: 0; margin: 36px 0 0; border-top: 1px solid rgba(255,255,255,0.1); }
  .archive-list li { border-bottom: 1px solid rgba(255,255,255,0.1); }
  .row { width: 100%; display: flex; justify-content: space-between; align-items: baseline; gap: 16px; padding: 16px 4px; background: none; border: 0; color: #f8fafc; font: inherit; font-weight: 700; text-align: left; cursor: pointer; }
  .row:hover .row-title, .row:focus-visible .row-title { color: #f59e0b; }
  .row-meta { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b; white-space: nowrap; }
  .prose { padding: 4px 4px 32px; line-height: 1.8; font-size: 1.05rem; overflow-wrap: anywhere; }
  .prose :global(h1) { font-size: 1.6rem; color: #f8fafc; }
  .prose :global(h2) { font-size: 1.3rem; color: #f8fafc; margin-top: 2em; }
  .prose :global(a) { color: #f59e0b; }
  .prose :global(img) { max-width: 100%; height: auto; border-radius: 8px; }
  .prose :global(blockquote) { border-left: 3px solid rgba(245,158,11,0.5); margin: 1.2em 0; padding-left: 16px; color: #94a3b8; }
  .prose :global(table) { display: block; overflow-x: auto; max-width: 100%; }
</style>
