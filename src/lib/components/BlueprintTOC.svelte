<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import { fade } from 'svelte/transition';

  export let content = [];

  let headings = [];
  let activeId = '';
  let visible = false;
  let tocOpen = false;

  // Extract heading content blocks
  $: headings = content
    .map((block, i) => {
      if (block.type === 'heading') {
        const id = `heading-${i}`;
        return { id, text: block.text, index: i };
      }
      return null;
    })
    .filter(Boolean);

  function handleScroll() {
    if (!browser) return;
    const headingEls = headings.map(h => document.getElementById(h.id)).filter(Boolean);

    for (let i = headingEls.length - 1; i >= 0; i--) {
      const rect = headingEls[i].getBoundingClientRect();
      if (rect.top <= 150) {
        activeId = headings[i].id;
        break;
      }
    }

    visible = window.scrollY > 400;
  }

  function scrollToHeading(id) {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      tocOpen = false;
    }
  }

  onMount(() => {
    if (browser) {
      window.addEventListener('scroll', handleScroll, { passive: true });
      handleScroll();
    }
  });

  onDestroy(() => {
    if (browser) {
      window.removeEventListener('scroll', handleScroll);
    }
  });
</script>

<!-- Assign IDs to heading blocks in the content -->
<!-- This component works alongside the section renderer -->
{#if headings.length > 1 && visible}
  <div class="toc-sidebar" transition:fade={{ duration: 200 }}>
    <button class="toc-toggle" on:click={() => tocOpen = !tocOpen} class:toc-toggle-open={tocOpen}>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="15" y2="12"/><line x1="3" y1="18" x2="9" y2="18"/>
      </svg>
    </button>

    {#if tocOpen}
      <div class="toc-panel" transition:fade={{ duration: 150 }}>
        <div class="toc-title">In this chapter</div>
        <nav class="toc-nav">
          {#each headings as heading}
            <button
              class="toc-link"
              class:toc-link-active={activeId === heading.id}
              on:click={() => scrollToHeading(heading.id)}
            >
              {heading.text}
            </button>
          {/each}
        </nav>
      </div>
    {/if}
  </div>
{/if}

<style>
  .toc-sidebar {
    position: fixed;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    z-index: 30;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .toc-toggle {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.1);
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s;
    backdrop-filter: blur(8px);
  }

  .toc-toggle:hover,
  .toc-toggle-open {
    color: #f59e0b;
    border-color: rgba(245, 158, 11, 0.2);
    background: rgba(15, 23, 42, 0.95);
  }

  .toc-panel {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 12px;
    padding: 0.75rem;
    backdrop-filter: blur(16px);
    min-width: 200px;
    max-width: 260px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  }

  .toc-title {
    font-size: 0.65rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.25rem 0.5rem;
    margin-bottom: 0.25rem;
  }

  .toc-nav {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
  }

  .toc-link {
    display: block;
    width: 100%;
    text-align: left;
    padding: 0.4rem 0.5rem;
    font-size: 0.78rem;
    color: #64748b;
    background: none;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s;
    line-height: 1.3;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .toc-link:hover {
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.04);
  }

  .toc-link-active {
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.08);
    font-weight: 600;
  }

  @media (max-width: 1200px) {
    .toc-sidebar {
      display: none;
    }
  }
</style>
