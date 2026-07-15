<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import { sectionsWithMeta } from '$lib/bookContent';
  import { bookPage } from '$lib/stores/bookPage';

  let visible = false;
  let lastVisitedId = null;

  onMount(() => {
    visible = true;
    window.scrollTo({ top: 0, behavior: 'instant' });
    const unsubscribe = bookPage.subscribe(state => {
      lastVisitedId = state.lastVisitedSectionId;
    });
    return unsubscribe;
  });

  $: lastVisitedSection = sectionsWithMeta.find(s => s.id === lastVisitedId) ?? null;

  // Group the flat section list into Front Matter / Part I / II / III / Back
  // Matter for the table of contents, using the "part-N" divider entries
  // already in book.json as the group boundaries.
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

  const totalWords = sectionsWithMeta.reduce((sum, s) => sum + s.wordCount, 0);
</script>

<svelte:head>
  <title>Read the Book | Surviving the Singularity</title>
  <meta name="description" content="The full current draft of Surviving the Singularity, navigable chapter by chapter." />
  <meta name="robots" content="noindex" />
</svelte:head>

<div class="book-page">
{#if visible}

  <!-- ── PREFACE ── -->
  <section class="preface" in:fade={{ duration: 400 }}>
    <div class="inner-narrow">
      <p class="eyebrow">Surviving the Singularity</p>
      <p class="preface-text">
        A practical field guide for staying agentic as AI rewrites work, money, medicine, and
        meaning. Written in public, updated as it's finished. What follows is the complete
        current draft: every chapter, in order, free to read for as long as you have this page.
      </p>
      <p class="preface-meta">{sectionsWithMeta.length} sections &middot; {totalWords.toLocaleString()} words total</p>
    </div>
  </section>

  {#if lastVisitedSection}
    <section class="continue">
      <a href="/book/{lastVisitedSection.id}" class="continue-card">
        <span class="continue-label">Continue reading</span>
        <span class="continue-title">{lastVisitedSection.title}</span>
        <span class="continue-arrow" aria-hidden="true">&rarr;</span>
      </a>
    </section>
  {/if}

  <!-- ── TABLE OF CONTENTS ── -->
  <section class="toc-section">
    <div class="inner">
      {#each tocGroups as group}
        <div class="toc-group">
          <p class="toc-group-label">{group.label}</p>
          <ul class="toc-list">
            {#each group.items as section}
              <li>
                <a href="/book/{section.id}" class="toc-item" class:is-current={section.id === lastVisitedId}>
                  <span class="toc-item-title">
                    {section.title}
                    {#if section.inProgress}<span class="toc-item-wip">🚧 Under Construction 🚧</span>{/if}
                  </span>
                  <span class="toc-item-meta">
                    {#if section.id === lastVisitedId}<span class="toc-item-badge">Last read</span>{/if}
                    <span class="toc-item-time">{section.wordCount.toLocaleString()} words</span>
                    <span class="toc-item-arrow" aria-hidden="true">&rarr;</span>
                  </span>
                </a>
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </div>
  </section>

{/if}
</div>

<style>
  /* ── TOKENS ── */
  .book-page {
    font-family: 'Outfit', system-ui, sans-serif;
    --amber:      #f59e0b;
    --amber-dim:  rgba(245,158,11,0.08);
    --surface:    #0f172a;
    --border:     rgba(255,255,255,0.07);
    --border-mid: rgba(255,255,255,0.11);
    --text-1:     #f8fafc;
    --text-2:     #cbd5e1;
    --text-3:     #64748b;
    --mono:       'JetBrains Mono', monospace;
  }

  .inner-narrow {
    max-width: 640px;
    margin: 0 auto;
  }
  .inner {
    max-width: 860px;
    margin: 0 auto;
  }

  /* ── PREFACE ── */
  .preface {
    padding: clamp(48px, 8vw, 80px) clamp(20px, 5vw, 48px) clamp(32px, 5vw, 48px);
    text-align: center;
  }
  .eyebrow {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--amber);
    margin: 0 0 1rem;
  }
  .preface-text {
    font-size: clamp(1.05rem, 2.4vw, 1.25rem);
    color: var(--text-2);
    line-height: 1.7;
    margin: 0 0 1rem;
  }
  .preface-meta {
    font-family: var(--mono);
    font-size: 0.8rem;
    color: var(--text-3);
    margin: 0;
  }

  /* ── CONTINUE READING ── */
  .continue {
    padding: 0 clamp(20px, 5vw, 48px);
    max-width: 860px;
    margin: 0 auto clamp(24px, 4vw, 40px);
  }
  .continue-card {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.4rem;
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 14px;
    text-decoration: none;
    transition: border-color 0.15s ease, background 0.15s ease;
  }
  .continue-card:hover {
    background: rgba(245,158,11,0.1);
    border-color: rgba(245,158,11,0.5);
  }
  .continue-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--amber);
    flex-shrink: 0;
  }
  .continue-title {
    flex: 1;
    color: var(--text-1);
    font-weight: 700;
    font-size: 0.98rem;
  }
  .continue-arrow { color: var(--amber); flex-shrink: 0; }

  /* ── TABLE OF CONTENTS ── */
  .toc-section {
    padding: 0 clamp(20px, 5vw, 48px) clamp(64px, 9vw, 100px);
  }
  .toc-group { margin-bottom: 2rem; }
  .toc-group-label {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--amber);
    margin: 0 0 0.85rem;
  }
  .toc-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }
  .toc-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid transparent;
    background: rgba(255,255,255,0.015);
    text-decoration: none;
    color: var(--text-2);
    font-size: 0.95rem;
    line-height: 1.4;
    transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease;
  }
  .toc-item-wip {
    display: inline-block;
    margin-left: 0.6rem;
    font-family: var(--mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: #fbbf24;
    white-space: nowrap;
  }
  .toc-item:hover,
  .toc-item.is-current {
    color: var(--text-1);
    background: rgba(245,158,11,0.06);
    border-color: rgba(245,158,11,0.25);
  }
  .toc-item-meta {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-shrink: 0;
  }
  .toc-item-badge {
    font-family: var(--mono);
    font-size: 0.62rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #0f172a;
    background: var(--amber);
    padding: 0.15rem 0.45rem;
    border-radius: 999px;
  }
  .toc-item-time {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--text-3);
    white-space: nowrap;
  }
  .toc-item-arrow {
    opacity: 0;
    transform: translateX(-4px);
    color: var(--amber);
    transition: opacity 0.15s ease, transform 0.15s ease;
  }
  .toc-item:hover .toc-item-arrow { opacity: 1; transform: translateX(0); }

  @media (max-width: 640px) {
    .toc-item-badge { display: none; }
  }
</style>
