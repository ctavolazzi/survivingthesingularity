<script>
  import { marked } from 'marked';
  import { page } from '$app/stores';
  import { safeGoto } from '$lib/utils/navigation';
  import { bookPage } from '$lib/stores/bookPage';
  import { sectionsWithMeta } from '$lib/bookContent';
  import Pagination from '$lib/components/Pagination.svelte';
  import FloatingPopupProgressBar from '$lib/components/FloatingPopupProgressBar.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  export let data;

  let currentSection = 1;
  let totalSections = data.book.sections.length;
  let navOpen = false;

  // Convert markdown to HTML
  $: content = marked(data.content);

  $: currentMeta = sectionsWithMeta.find(s => s.id === data.section.id);

  // Group the flat section list for the jump-to-chapter dropdown - same
  // grouping the /book table of contents uses, so the two stay consistent.
  const tocGroups = (() => {
    const groups = [];
    let current = { label: 'Front Matter', items: [] };
    for (const section of sectionsWithMeta) {
      if (section.id.startsWith('part-')) {
        if (current.items.length) groups.push(current);
        current = { label: section.title, items: [] };
      } else {
        current.items.push(section);
      }
    }
    if (current.items.length) groups.push(current);
    return groups;
  })();

  // Re-runs on every navigation between chapters, not just first mount -
  // SvelteKit reuses this same component instance across /book/[sectionId]
  // navigations (only `data` changes), so recording the last-visited
  // section has to live here rather than in onMount, which only fires once.
  $: if (data && data.section) {
    currentSection = data.book.sections.findIndex(section => section.id === data.section.id) + 1;
    bookPage.setCurrentSection(data.section.id);
    bookPage.updateLastVisited();
  }

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

  function jumpTo(sectionId) {
    navOpen = false;
    safeGoto(`/book/${sectionId}`);
  }
</script>

<FloatingPopupProgressBar />

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

<!-- ── CHAPTER NAV: collapsible jump-to-chapter dropdown, closed by default ── -->
<div class="chapter-nav">
  <div class="chapter-nav-pill">
    <a href="/book" class="chapter-nav-toc-link" aria-label="Table of contents">
      <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
        <path d="M9.5 2.5L2.5 6L9.5 9.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      TOC
    </a>
    <div class="chapter-nav-sep" aria-hidden="true"></div>
    <button
      type="button"
      class="chapter-nav-toggle"
      aria-expanded={navOpen}
      on:click={() => navOpen = !navOpen}
    >
      Chapters
      <svg class="chapter-nav-chevron" class:open={navOpen} width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
        <path d="M2.5 4.5L6 8L9.5 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>

  {#if navOpen}
    <div class="chapter-nav-dropdown">
      {#each tocGroups as group}
        <div class="chapter-nav-group">
          <p class="chapter-nav-group-label">{group.label}</p>
          <ul class="chapter-nav-list">
            {#each group.items as section}
              <li>
                <button
                  type="button"
                  class="chapter-nav-item"
                  class:is-current={section.id === data.section.id}
                  on:click={() => jumpTo(section.id)}
                >
                  <span>
                    {section.title}
                    {#if section.inProgress}<span class="chapter-nav-wip">🚧</span>{/if}
                  </span>
                  <span class="chapter-nav-time">{section.wordCount.toLocaleString()} words</span>
                </button>
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </div>
  {/if}
</div>

<Spacer height="24px" />

<div class="content-wrapper">
  {#if currentMeta}
    <p class="chapter-meta">
      {currentMeta.wordCount.toLocaleString()} words &middot; Part {currentSection} of {totalSections}
      {#if currentMeta.inProgress}&middot; <span class="chapter-meta-wip">🚧 Under Construction 🚧</span>{/if}
    </p>
  {/if}

  <!-- Existing Progress Bar -->
  <div class="progress-container mb-8">
    <div class="progress-bar" style="width: {(currentSection / totalSections) * 100}%"></div>
  </div>

  <article class="prose prose-lg dark:prose-invert chapter-article">
    {@html content}
  </article>

  <!-- Add this anchor element right after the article content -->
  <div id="article-end-anchor"></div>

  <Pagination
    {currentSection}
    {totalSections}
    on:navigate={handleNavigation}
  />

  <div class="mt-8 mb-4 text-center">
    <a href="/book" class="toc-link">
      &larr; Table of Contents
    </a>
  </div>
</div>

<style>
  /* ── CHAPTER NAV ──
     Floating pill, same visual language as the site's own nav-float/nav-pill
     (transparent sticky wrapper + a centered rounded pill), sitting directly
     beneath it rather than as a separate hard-edged full-width bar. */
  .chapter-nav {
    /* top matches the site nav-pill's measured height so the two floating
       pills sit stacked with a small gap instead of overlapping. */
    position: sticky;
    top: 74px;
    z-index: 20;
    padding: 0 16px 10px;
    pointer-events: none;
  }
  .chapter-nav-pill {
    pointer-events: all;
    display: flex;
    align-items: center;
    gap: 2px;
    max-width: max-content;
    margin: 0 auto;
    padding: 4px;
    background: rgba(9, 14, 32, 0.86);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 999px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
  }
  .chapter-nav-toc-link {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: rgba(203,213,225,0.8);
    text-decoration: none;
    white-space: nowrap;
    padding: 0.45rem 0.7rem;
    border-radius: 999px;
    transition: color 0.15s ease, background 0.15s ease;
  }
  .chapter-nav-toc-link:hover { color: #f59e0b; background: rgba(255,255,255,0.05); }
  .chapter-nav-sep {
    width: 1px;
    height: 16px;
    background: rgba(255,255,255,0.1);
    flex-shrink: 0;
  }
  .chapter-nav-toggle {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: transparent;
    border: none;
    color: #f1f5f9;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    white-space: nowrap;
    padding: 0.45rem 0.75rem;
    border-radius: 999px;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .chapter-nav-toggle:hover { background: rgba(245,158,11,0.12); color: #f59e0b; }
  .chapter-nav-chevron { transition: transform 0.2s ease; }
  .chapter-nav-chevron.open { transform: rotate(180deg); }

  .chapter-nav-dropdown {
    pointer-events: all;
    max-height: min(70vh, 560px);
    overflow-y: auto;
    max-width: 620px;
    margin: 8px auto 0;
    padding: 0.75rem 0.5rem 1rem;
    background: rgba(9, 14, 32, 0.92);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.05);
  }
  .chapter-nav-group { padding: 0 0.5rem; margin-top: 1rem; }
  .chapter-nav-group-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #f59e0b;
    margin: 0 0 0.5rem;
  }
  .chapter-nav-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }
  .chapter-nav-item {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    background: transparent;
    border: none;
    color: #cbd5e1;
    font-family: inherit;
    font-size: 0.88rem;
    text-align: left;
    padding: 0.55rem 0.6rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .chapter-nav-item:hover { background: rgba(245,158,11,0.06); color: #f8fafc; }
  .chapter-nav-item.is-current { color: #f59e0b; font-weight: 700; }
  .chapter-nav-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #64748b;
    flex-shrink: 0;
  }
  .chapter-nav-wip {
    margin-left: 0.4rem;
    font-size: 0.75rem;
  }

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

  .chapter-meta-wip {
    color: #fbbf24;
    font-weight: 700;
  }

  .chapter-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #64748b;
    text-align: center;
    margin: 0 0 1rem;
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
