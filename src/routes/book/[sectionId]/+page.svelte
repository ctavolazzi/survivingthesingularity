<script>
  import { marked } from 'marked';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { safeGoto } from '$lib/utils/navigation';
  import { bookPage } from '$lib/stores/bookPage';
  import Pagination from '$lib/components/Pagination.svelte';
  import FloatingPopupProgressBar from '$lib/components/FloatingPopupProgressBar.svelte';
  import FloatingQuotePopup from '$lib/components/FloatingQuotePopup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import Markdown from '$lib/components/Markdown.svelte';
  import TableOfContents from '$lib/components/TableOfContents.svelte';
  export let data;

  let currentSection = 1;
  let totalSections = data.book.sections.length;

  // Convert markdown to HTML
  $: content = marked(data.content);

  $: {
    if (data && data.section) {
      currentSection = data.book.sections.findIndex(section => section.id === data.section.id) + 1;
    }
  }

  onMount(() => {
    currentSection = data.book.sections.findIndex(section => section.id === data.section.id) + 1;
    bookPage.setCurrentSection(data.section.id);
    bookPage.updateLastVisited();
  });

  function handleNavigation(event) {
    const { direction } = event.detail;
    const newIndex = currentSection + (direction === 'next' ? 1 : -1) - 1;
    if (newIndex >= 0 && newIndex < totalSections) {
      const newSection = data.book.sections[newIndex];
      if (newSection) {
        safeGoto(`/book/${newSection.id}`);
      }
    }
  }
</script>

<FloatingPopupProgressBar />
<FloatingQuotePopup />

<svelte:head>
  <title>{data.section.title} | Surviving the Singularity</title>
  <meta name="description" content="Read {data.section.title} from {data.book.title}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{data.section.title} | Surviving the Singularity" />
  <meta property="og:description" content="Read {data.section.title} from {data.book.title}" />
  <meta property="og:image" content="{$page.url.origin}/Surviving-the-Singularity-Cover.png" />
  <meta property="og:url" content="{$page.url.href}" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<Spacer height="50px" />

<div class="content-wrapper">
  <!-- Top link -->
  <div class="mt-4 mb-4 text-center">
    <a href="/book" class="toc-link">
      &larr; Table of Contents
    </a>
  </div>

  <!-- Existing Progress Bar -->
  <div class="progress-container mb-8">
    <div class="progress-bar" style="width: {(currentSection / totalSections) * 100}%"></div>
    <div class="progress-text">
      Part {currentSection} of {totalSections}
    </div>
  </div>

  <article class="prose prose-lg dark:prose-invert chapter-article">
    {@html content}
  </article>

  <!-- Add this anchor element right after the article content -->
  <div id="article-end-anchor"></div>

  <!-- Bottom link -->
  <div class="mt-8 mb-4 text-center">
    <a href="/book" class="toc-link">
      &larr; Table of Contents
    </a>
  </div>

  <Pagination
    {currentSection}
    {totalSections}
    on:navigate={handleNavigation}
  />
</div>

<style>
  .content-wrapper {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  @media (max-width: 840px) {
    .content-wrapper {
      max-width: 100%;
    }
  }

  .toc-link {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94a3b8;
    text-decoration: none;
    transition: color 0.2s ease;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
  }

  .toc-link:hover {
    color: #f59e0b;
    background-color: rgba(245, 158, 11, 0.08);
  }

  /* ── CHAPTER TYPOGRAPHY ── */
  :global(.chapter-article) {
    max-width: 100%;
    color: #cbd5e1;
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 1.05rem;
    line-height: 1.75;
  }

  /* Chapter title - the article's own H1 */
  :global(.chapter-article h1) {
    font-family: 'Outfit', 'Inter', system-ui, sans-serif;
    color: #f8fafc;
    font-weight: 900;
    font-size: clamp(1.9rem, 5vw, 3rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin: 0 0 1.5rem;
    text-align: left;
  }

  /* Chapter header image - first image, right after the H1 */
  :global(.chapter-article img) {
    display: block;
    width: 100%;
    height: auto;
    max-width: 100%;
    border-radius: 12px;
    margin: 0 0 2rem;
    box-shadow: 0 24px 60px rgba(0,0,0,0.45), 0 0 0 1px rgba(245,158,11,0.1);
  }

  /* Epigraph - the first blockquote, always right after the header image */
  :global(.chapter-article blockquote:first-of-type) {
    position: relative;
    margin: 0 0 2.5rem;
    padding: 0.25rem 0 0.25rem 1.5rem;
    border-left: 3px solid #f59e0b;
    font-style: italic;
  }
  :global(.chapter-article blockquote:first-of-type p) {
    color: #f1f5f9;
    font-size: 1.15rem;
    line-height: 1.6;
    margin: 0 0 0.6rem;
    text-shadow: none;
  }
  :global(.chapter-article blockquote:first-of-type p:last-child) {
    font-style: normal;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #f59e0b;
    margin: 0;
  }

  /* Any other in-body blockquote (callouts, pull-quotes) */
  :global(.chapter-article blockquote:not(:first-of-type)) {
    margin: 2rem 0;
    padding: 1.1rem 1.5rem;
    background: rgba(245,158,11,0.05);
    border-left: 3px solid rgba(245,158,11,0.5);
    border-radius: 0 10px 10px 0;
  }
  :global(.chapter-article blockquote:not(:first-of-type) p) {
    color: #e2e8f0;
    font-style: italic;
    margin: 0;
    text-shadow: none;
  }

  :global(.chapter-article h2) {
    font-family: 'Outfit', 'Inter', system-ui, sans-serif;
    color: #fbbf24;
    font-weight: 800;
    font-size: clamp(1.4rem, 3vw, 1.9rem);
    letter-spacing: -0.01em;
    line-height: 1.2;
    margin: 2.75rem 0 1rem;
    text-align: left;
  }

  :global(.chapter-article h3) {
    font-family: 'Outfit', 'Inter', system-ui, sans-serif;
    color: #f1f5f9;
    font-weight: 700;
    font-size: clamp(1.15rem, 2.2vw, 1.4rem);
    line-height: 1.3;
    margin: 2rem 0 0.85rem;
    text-align: left;
  }

  :global(.chapter-article p) {
    color: #cbd5e1;
    text-shadow: none;
    text-align: left;
    margin: 0 0 1.3rem;
  }

  :global(.chapter-article ul),
  :global(.chapter-article ol) {
    margin: 0 0 1.3rem;
    padding-left: 1.4rem;
    color: #cbd5e1;
  }
  :global(.chapter-article li) {
    margin-bottom: 0.5rem;
    line-height: 1.65;
  }

  :global(.chapter-article hr) {
    border: 0;
    border-top: 1px solid rgba(148,163,184,0.15);
    margin: 2.5rem 0;
  }

  :global(.chapter-article strong) { color: #f8fafc; }

  :global(.chapter-article a) {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 2px;
    transition: color 0.2s ease;
  }
  :global(.chapter-article a:hover) { color: #fbbf24; }

  @media (max-width: 640px) {
    :global(.chapter-article) { font-size: 1rem; }
  }
</style>
