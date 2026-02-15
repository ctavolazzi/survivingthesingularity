<script>
  import { sections } from '$lib/data/blueprint.js';
  import { blueprintProgress } from '$lib/stores/progress.js';
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';

  let visible = false;
  onMount(() => { visible = true; });

  $: progress = $blueprintProgress;
  $: completedCount = Object.values(progress).filter((v) => v.readAt).length;
  $: progressPercent = Math.round((completedCount / sections.length) * 100);

  function estimateReadingTime(content) {
    if (!content) return 0;
    let words = 0;
    for (const block of content) {
      if (block.text) words += block.text.split(/\s+/).length;
      if (block.title) words += block.title.split(/\s+/).length;
      if (block.rows) words += block.rows.length * 10;
    }
    return Math.max(1, Math.round(words / 220));
  }
</script>

<svelte:head>
  <title>The Blueprint — Surviving the Singularity</title>
  <meta name="description" content="The YouTube Shouse Blueprint: Eight chapters on material independence through digital leverage, local AI, and minimalist infrastructure." />
</svelte:head>

<div class="blueprint-page">
  {#if visible}
    <header class="bp-header" in:fade={{ duration: 600 }}>
      <p class="bp-label">The YouTube Shouse Blueprint</p>
      <h1 class="bp-title">The Complete Blueprint</h1>
      <p class="bp-subtitle">
        Eight chapters covering every layer of the exit strategy — from economic analysis to immediate execution. This is the full tactical breakdown.
      </p>

      {#if completedCount > 0}
        <div class="bp-progress" in:fade={{ delay: 200, duration: 300 }}>
          <div class="bp-progress-bar-bg">
            <div class="bp-progress-bar-fill" style="width: {progressPercent}%"></div>
          </div>
          <span class="bp-progress-text">
            {completedCount}/{sections.length} chapters complete
            {#if completedCount === sections.length}
              — Blueprint mastered
            {/if}
          </span>
        </div>
      {/if}
    </header>
  {/if}

  <div class="bp-toc">
    {#each sections as section, i}
      {@const isRead = !!progress[section.slug]?.readAt}
      {@const scrollPct = progress[section.slug]?.scrollPercent || 0}
      {@const readTime = estimateReadingTime(section.content)}
      <a href="/blueprint/{section.slug}" class="toc-card" class:toc-read={isRead} style="animation-delay: {(i + 1) * 80}ms">
        <div class="toc-left">
          <div class="toc-num-wrap" class:toc-num-done={isRead}>
            {#if isRead}
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8L6.5 11.5L13 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            {:else}
              <span class="toc-num">{section.number}</span>
            {/if}
          </div>
          <div class="toc-info">
            <h2 class="toc-title">{section.title}</h2>
            <p class="toc-subtitle">{section.subtitle}</p>
            <div class="toc-meta">
              <span class="toc-read-time">{readTime} min read</span>
              {#if !isRead && scrollPct > 0}
                <span class="toc-in-progress">{scrollPct}% read</span>
              {/if}
            </div>
          </div>
        </div>
        {#if !isRead && scrollPct > 0}
          <div class="toc-scroll-bar-bg">
            <div class="toc-scroll-bar-fill" style="width: {scrollPct}%"></div>
          </div>
        {/if}
        <svg class="toc-arrow" width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    {/each}
  </div>
</div>

<style>
  .blueprint-page {
    max-width: 860px;
    margin: 0 auto;
    padding: 3rem 1.5rem 5rem;
  }

  .bp-header {
    margin-bottom: 3rem;
  }

  .bp-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #f59e0b;
    margin: 0 0 0.75rem 0;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
  }

  .bp-title {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 900;
    color: #f1f5f9;
    margin: 0 0 1rem 0;
    letter-spacing: -0.03em;
  }

  .bp-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0;
    max-width: 640px;
  }

  /* Progress bar */
  .bp-progress {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .bp-progress-bar-bg {
    flex: 1;
    max-width: 240px;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    overflow: hidden;
  }

  .bp-progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #10b981);
    border-radius: 3px;
    transition: width 0.8s ease;
  }

  .bp-progress-text {
    font-size: 0.8rem;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
  }

  .bp-toc {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .toc-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 14px;
    text-decoration: none;
    transition: all 0.3s ease;
    animation: fadeUp 0.5s ease forwards;
    opacity: 0;
    position: relative;
    overflow: hidden;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .toc-card:hover {
    border-color: rgba(245, 158, 11, 0.25);
    background: rgba(30, 41, 59, 0.5);
    transform: translateX(4px);
  }

  .toc-read {
    border-color: rgba(16, 185, 129, 0.15);
    background: rgba(16, 185, 129, 0.03);
  }

  .toc-read:hover {
    border-color: rgba(16, 185, 129, 0.3);
  }

  .toc-left {
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
  }

  .toc-num-wrap {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.12);
    flex-shrink: 0;
    color: #f59e0b;
  }

  .toc-num-done {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }

  .toc-num {
    font-size: 0.8rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
  }

  .toc-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.3rem 0;
  }

  .toc-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
    line-height: 1.4;
  }

  .toc-meta {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.4rem;
  }

  .toc-read-time {
    font-size: 0.7rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
  }

  .toc-in-progress {
    font-size: 0.7rem;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
  }

  .toc-scroll-bar-bg {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: rgba(255, 255, 255, 0.03);
  }

  .toc-scroll-bar-fill {
    height: 100%;
    background: rgba(245, 158, 11, 0.4);
    transition: width 0.3s;
  }

  .toc-arrow {
    color: #475569;
    flex-shrink: 0;
    transition: all 0.2s;
  }

  .toc-card:hover .toc-arrow {
    color: #f59e0b;
    transform: translateX(4px);
  }

  @media (max-width: 640px) {
    .blueprint-page {
      padding: 2rem 1rem 4rem;
    }

    .toc-card {
      padding: 1.25rem;
    }

    .toc-arrow {
      display: none;
    }
  }
</style>
