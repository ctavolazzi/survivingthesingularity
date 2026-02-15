<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { getSection, getNextSection, getPrevSection, sections } from '$lib/data/blueprint.js';
  import { blueprintProgress } from '$lib/stores/progress.js';
  import { toasts } from '$lib/stores/toasts.js';
  import ReadingPreferences from '$lib/components/ReadingPreferences.svelte';
  import BlueprintTOC from '$lib/components/BlueprintTOC.svelte';
  import { fade, fly } from 'svelte/transition';
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';

  let visible = false;
  let scrollPercent = 0;
  let markedRead = false;
  let showShareModal = false;
  let articleEl;
  let showPrefs = false;
  let prefsCssVars = {};

  function handlePrefsChange(e) {
    prefsCssVars = e.detail || {};
  }

  onMount(() => {
    visible = true;
    if (browser) {
      window.addEventListener('scroll', handleScroll);
      window.addEventListener('keydown', handleKeydown);
    }
  });

  onDestroy(() => {
    if (browser) {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('keydown', handleKeydown);
    }
  });

  function handleScroll() {
    if (!articleEl) return;
    const rect = articleEl.getBoundingClientRect();
    const total = articleEl.scrollHeight - window.innerHeight;
    const scrolled = -rect.top;
    scrollPercent = Math.min(100, Math.max(0, Math.round((scrolled / total) * 100)));

    // Auto-mark as read at 75%
    if (scrollPercent >= 75 && !markedRead && slug) {
      markedRead = true;
      blueprintProgress.markRead(slug);
      const idx = sections.findIndex(s => s.slug === slug);
      const completed = blueprintProgress.getCompletedCount();
      if (completed === sections.length) {
        toasts.success('You completed the entire blueprint!');
      } else {
        toasts.success(`Chapter ${idx + 1} complete! (${completed}/${sections.length})`);
      }
      // Show share modal after brief delay
      setTimeout(() => { showShareModal = true; }, 1500);
    }

    blueprintProgress.updateScroll(slug, scrollPercent);
  }

  function handleKeydown(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'ArrowRight' || e.key === 'j') {
      if (next) goto(`/blueprint/${next.slug}`);
    } else if (e.key === 'ArrowLeft' || e.key === 'k') {
      if (prev) goto(`/blueprint/${prev.slug}`);
    } else if (e.key === 'b' || e.key === 'Escape') {
      goto('/blueprint');
    } else if (e.key === 'h') {
      goto('/');
    }
  }

  function dismissShare() {
    showShareModal = false;
  }

  function shareToTwitter() {
    if (!section) return;
    const text = encodeURIComponent(`Just read "${section.title}" from the YouTube Shouse Blueprint. Building my exit strategy. #SurvivingTheSingularity`);
    window.open(`https://twitter.com/intent/tweet?text=${text}`, '_blank');
    showShareModal = false;
  }

  function copyLink() {
    if (browser) {
      navigator.clipboard.writeText(window.location.href);
      toasts.success('Link copied!');
      showShareModal = false;
    }
  }

  // Estimate reading time from content blocks
  function estimateReadingTime(content) {
    if (!content) return 0;
    let words = 0;
    for (const block of content) {
      if (block.text) words += block.text.split(/\s+/).length;
      if (block.title) words += block.title.split(/\s+/).length;
      if (block.rows) words += block.rows.length * 10; // estimate for tables
    }
    return Math.max(1, Math.round(words / 220));
  }

  $: slug = $page.params.section;
  $: section = getSection(slug);
  $: next = getNextSection(slug);
  $: prev = getPrevSection(slug);
  $: readingTime = section ? estimateReadingTime(section.content) : 0;
  $: isAlreadyRead = $blueprintProgress[slug]?.readAt;
  $: currentIndex = sections.findIndex(s => s.slug === slug);

  // Reset state on navigation
  $: if (slug) {
    markedRead = false;
    showShareModal = false;
    scrollPercent = 0;
  }
</script>

<svelte:head>
  {#if section}
    <title>{section.title} — The Blueprint — Surviving the Singularity</title>
    <meta name="description" content={section.subtitle} />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{section.title} — The Blueprint" />
    <meta property="og:description" content={section.subtitle} />
    <meta property="og:url" content="https://survivingthesingularity.com/blueprint/{slug}" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{section.title} — The Blueprint" />
    <meta name="twitter:description" content={section.subtitle} />
    {@html `<script type="application/ld+json">${JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": section.title,
      "description": section.subtitle,
      "isPartOf": { "@type": "Book", "name": "The YouTube Shouse Blueprint" },
      "position": currentIndex + 1
    })}</script>`}
  {/if}
</svelte:head>

<!-- Reading progress bar -->
{#if section}
  <div class="progress-bar-fixed">
    <div class="progress-fill" style="width: {scrollPercent}%"></div>
  </div>
{/if}

{#if section}
  <BlueprintTOC content={section.content} />
  <article class="section-page" bind:this={articleEl} in:fade={{ duration: 300 }}>
    <header class="section-header">
      <div class="header-top">
        <a href="/blueprint" class="back-link">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M13 8H3M3 8L7 4M3 8L7 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          All Chapters
        </a>
        <div class="header-meta">
          <span class="reading-time">{readingTime} min read</span>
          {#if isAlreadyRead}
            <span class="read-badge">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6L4.5 8.5L10 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              Read
            </span>
          {/if}
          <div class="prefs-trigger-wrap">
            <button class="prefs-trigger" on:click={() => showPrefs = !showPrefs} title="Reading preferences">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            </button>
            <ReadingPreferences open={showPrefs} on:close={() => showPrefs = false} on:change={handlePrefsChange} />
          </div>
        </div>
      </div>

      <!-- Chapter dots navigation -->
      <div class="chapter-dots">
        {#each sections as s, i}
          <a
            href="/blueprint/{s.slug}"
            class="dot"
            class:dot-active={s.slug === slug}
            class:dot-read={$blueprintProgress[s.slug]?.readAt}
            title="Ch. {s.number}: {s.title}"
          >
            <span class="dot-inner"></span>
          </a>
        {/each}
      </div>

      <span class="section-num">Chapter {section.number}</span>
      <h1 class="section-title">{section.title}</h1>
      <p class="section-subtitle">{section.subtitle}</p>
    </header>

    <div class="section-body">
      {#each section.content as block, blockIdx}
        {#if block.type === 'prose'}
          <p class="prose-text">{@html block.text}</p>
        {:else if block.type === 'heading'}
          <h2 class="content-heading" id="heading-{blockIdx}">{block.text}</h2>
        {:else if block.type === 'callout'}
          <div class="callout">
            <div class="callout-bar"></div>
            <p class="callout-text">{block.text}</p>
          </div>
        {:else if block.type === 'directive'}
          <div class="directive">
            <span class="directive-num">{block.number}</span>
            <div class="directive-content">
              <h3 class="directive-title">{block.title}</h3>
              <p class="directive-text">{block.text}</p>
            </div>
          </div>
        {:else if block.type === 'table'}
          <div class="data-table-wrapper">
            {#if block.title}
              <h3 class="table-title">{block.title}</h3>
            {/if}
            <div class="table-scroll">
              <table class="data-table">
                <thead>
                  <tr>
                    {#each block.headers as header}
                      <th>{header}</th>
                    {/each}
                  </tr>
                </thead>
                <tbody>
                  {#each block.rows as row}
                    <tr>
                      {#each row as cell, ci}
                        <td class={ci === 0 ? 'cell-primary' : ''}>{cell}</td>
                      {/each}
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        {/if}
      {/each}
    </div>

    <nav class="section-nav">
      {#if prev}
        <a href="/blueprint/{prev.slug}" class="nav-prev">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M13 8H3M3 8L7 4M3 8L7 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <div>
            <span class="nav-label">Previous</span>
            <span class="nav-title">{prev.title}</span>
          </div>
        </a>
      {:else}
        <div></div>
      {/if}
      {#if next}
        <a href="/blueprint/{next.slug}" class="nav-next">
          <div>
            <span class="nav-label">Next</span>
            <span class="nav-title">{next.title}</span>
          </div>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      {:else}
        <div></div>
      {/if}
    </nav>

    <div class="keyboard-hint">
      <span><kbd>&larr;</kbd><kbd>&rarr;</kbd> navigate</span>
      <span><kbd>b</kbd> all chapters</span>
      <span><kbd>h</kbd> home</span>
    </div>
  </article>
{:else}
  <div class="not-found">
    <h1>Chapter not found</h1>
    <p>This blueprint section doesn't exist.</p>
    <a href="/blueprint">Back to The Blueprint</a>
  </div>
{/if}

<!-- Share modal -->
{#if showShareModal}
  <div class="share-overlay" on:click={dismissShare} transition:fade={{ duration: 200 }}>
    <div class="share-modal" on:click|stopPropagation in:fly={{ y: 20, duration: 300 }}>
      <div class="share-header">
        <span class="share-celebration">Chapter complete!</span>
        <h3 class="share-title">Share Your Progress</h3>
        <p class="share-desc">{blueprintProgress.getCompletedCount()} of {sections.length} chapters done</p>
      </div>
      <div class="share-actions">
        <button class="share-btn share-twitter" on:click={shareToTwitter}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          Share on X
        </button>
        <button class="share-btn share-copy" on:click={copyLink}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          Copy Link
        </button>
      </div>
      <button class="share-dismiss" on:click={dismissShare}>Continue reading</button>
    </div>
  </div>
{/if}

<style>
  /* Progress bar */
  .progress-bar-fixed {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: rgba(255, 255, 255, 0.05);
    z-index: 100;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #10b981);
    transition: width 0.15s ease;
  }

  .section-page {
    max-width: 780px;
    margin: 0 auto;
    padding: 2rem 1.5rem 5rem;
  }

  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: #64748b;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    transition: color 0.2s;
  }

  .back-link:hover {
    color: #f59e0b;
  }

  .header-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .reading-time {
    font-size: 0.75rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
  }

  .read-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.7rem;
    font-weight: 600;
    color: #10b981;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 12px;
    padding: 0.2rem 0.6rem;
  }

  /* Reading preferences trigger */
  .prefs-trigger-wrap {
    position: relative;
  }

  .prefs-trigger {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.08);
    color: #475569;
    cursor: pointer;
    transition: all 0.2s;
  }

  .prefs-trigger:hover {
    color: #f59e0b;
    border-color: rgba(245, 158, 11, 0.2);
    background: rgba(30, 41, 59, 0.8);
  }

  /* Chapter dots */
  .chapter-dots {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    justify-content: center;
  }

  .dot {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
  }

  .dot-inner {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    border: 1.5px solid rgba(255, 255, 255, 0.15);
    transition: all 0.2s;
  }

  .dot-active .dot-inner {
    background: #f59e0b;
    border-color: #f59e0b;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.4);
    transform: scale(1.2);
  }

  .dot-read .dot-inner {
    background: #10b981;
    border-color: #10b981;
  }

  .dot:hover .dot-inner {
    border-color: #f59e0b;
    transform: scale(1.3);
  }

  .section-header {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
  }

  .section-num {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
  }

  .section-title {
    font-size: clamp(1.75rem, 5vw, 2.75rem);
    font-weight: 900;
    color: #f1f5f9;
    margin: 0 0 0.75rem 0;
    letter-spacing: -0.03em;
  }

  .section-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
  }

  /* Content blocks */
  .section-body {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .prose-text {
    color: #cbd5e1;
    font-size: 1.05rem;
    line-height: 1.85;
    margin: 0;
  }

  :global(.prose-text strong) {
    color: #e2e8f0;
    font-weight: 600;
  }

  :global(.prose-text em) {
    color: #fbbf24;
  }

  .content-heading {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 1.5rem 0 0 0;
    letter-spacing: -0.02em;
  }

  .callout {
    display: flex;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    background: rgba(245, 158, 11, 0.06);
    border-radius: 12px;
    margin: 0.5rem 0;
  }

  .callout-bar {
    width: 3px;
    background: #f59e0b;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .callout-text {
    color: #fbbf24;
    font-size: 1rem;
    line-height: 1.7;
    margin: 0;
    font-weight: 500;
  }

  .directive {
    display: flex;
    gap: 1.25rem;
    padding: 1.5rem;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 14px;
  }

  .directive-num {
    font-size: 1.5rem;
    font-weight: 900;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(245, 158, 11, 0.1);
    border-radius: 10px;
  }

  .directive-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.4rem 0;
  }

  .directive-text {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
  }

  .data-table-wrapper {
    margin: 0.5rem 0;
  }

  .table-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0 0 0.75rem 0;
  }

  .table-scroll {
    overflow-x: auto;
    border-radius: 12px;
    border: 1px solid rgba(148, 163, 184, 0.08);
  }

  .data-table {
    display: table;
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
  }

  .data-table thead {
    background: rgba(30, 41, 59, 0.6);
  }

  .data-table th {
    padding: 0.85rem 1rem;
    text-align: left;
    font-weight: 600;
    color: #94a3b8;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    white-space: nowrap;
  }

  .data-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.04);
    color: #cbd5e1;
    vertical-align: top;
  }

  .data-table tbody tr:hover {
    background: rgba(245, 158, 11, 0.03);
  }

  .cell-primary {
    font-weight: 600;
    color: #e2e8f0;
  }

  /* Navigation */
  .section-nav {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(148, 163, 184, 0.08);
  }

  .nav-prev, .nav-next {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 12px;
    text-decoration: none;
    transition: all 0.2s;
    max-width: 48%;
  }

  .nav-prev:hover, .nav-next:hover {
    border-color: rgba(245, 158, 11, 0.2);
    background: rgba(30, 41, 59, 0.5);
    transform: translateY(-2px);
  }

  .nav-next {
    text-align: right;
    margin-left: auto;
  }

  .nav-label {
    display: block;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    font-weight: 600;
  }

  .nav-title {
    display: block;
    font-size: 0.9rem;
    color: #e2e8f0;
    font-weight: 600;
  }

  .nav-prev svg, .nav-next svg {
    color: #475569;
    flex-shrink: 0;
  }

  /* Keyboard hints */
  .keyboard-hint {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(148, 163, 184, 0.04);
  }

  .keyboard-hint span {
    font-size: 0.7rem;
    color: #334155;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }

  .keyboard-hint kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    height: 20px;
    padding: 0 4px;
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 4px;
    background: rgba(30, 41, 59, 0.3);
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
  }

  /* Share modal */
  .share-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
  }

  .share-modal {
    background: #0f172a;
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 20px;
    padding: 2rem;
    max-width: 400px;
    width: 100%;
    text-align: center;
  }

  .share-celebration {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #10b981;
    font-family: 'JetBrains Mono', monospace;
  }

  .share-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0.5rem 0;
  }

  .share-desc {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0 0 1.5rem 0;
  }

  .share-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    margin-bottom: 1rem;
  }

  .share-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.65rem 1.25rem;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
  }

  .share-twitter {
    background: rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
  }

  .share-twitter:hover {
    background: rgba(255, 255, 255, 0.15);
  }

  .share-copy {
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.2);
  }

  .share-copy:hover {
    background: rgba(245, 158, 11, 0.15);
  }

  .share-dismiss {
    background: none;
    border: none;
    color: #475569;
    font-size: 0.8rem;
    cursor: pointer;
    padding: 0.5rem;
    font-family: inherit;
    transition: color 0.2s;
  }

  .share-dismiss:hover {
    color: #94a3b8;
  }

  /* 404 */
  .not-found {
    text-align: center;
    padding: 6rem 2rem;
  }

  .not-found h1 {
    color: #f1f5f9;
    margin-bottom: 0.5rem;
  }

  .not-found p {
    color: #64748b;
    margin-bottom: 2rem;
  }

  .not-found a {
    color: #f59e0b;
  }

  @media (max-width: 640px) {
    .section-page {
      padding: 1.5rem 1rem 4rem;
    }

    .section-nav {
      flex-direction: column;
    }

    .nav-prev, .nav-next {
      max-width: 100%;
    }

    .keyboard-hint {
      display: none;
    }

    .header-top {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
  }
</style>
