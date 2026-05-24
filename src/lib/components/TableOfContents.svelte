<!-- src/lib/components/TableOfContents.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { bookPage } from '$lib/stores/bookPage';

  export let sections = [];
  // Optional: hide the internal heading when the parent page already provides one.
  export let showHeading = false;

  let hoveredIndex = -1;
  let currentSectionId;

  bookPage.subscribe(state => {
    currentSectionId = state.currentSectionId;
  });

  function handleClick(sectionId) {
    bookPage.setCurrentSection(sectionId);
    goto(`/book/${sectionId}`);
  }
</script>

<nav class="table-of-contents" aria-label="Book table of contents">
  {#if showHeading}
    <div class="title-container">
      <h2>Table of Contents</h2>
    </div>
  {/if}
  <ul>
    {#each sections as section, index}
      <li
        class:active={section.id === currentSectionId}
        on:mouseenter={() => hoveredIndex = index}
        on:mouseleave={() => hoveredIndex = -1}
      >
        <button on:click={() => handleClick(section.id)}>
          <span class="section-number">{(index + 1).toString().padStart(2, '0')}</span>
          <span class="section-title">{section.title}</span>
          <span class="arrow" aria-hidden="true">→</span>
        </button>
      </li>
    {/each}
  </ul>
</nav>

<style>
  .table-of-contents {
    width: 100%;
    color: var(--color-text-primary, #f1f5f9);
    font-family: var(--font-primary, 'Inter', sans-serif);
  }

  .title-container {
    margin-bottom: 1.5rem;
  }

  h2 {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--color-primary, #f59e0b);
    letter-spacing: -0.025em;
    margin: 0;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  li { margin: 0; }

  button {
    width: 100%;
    background: var(--color-bg-secondary, #0f172a);
    border: 1px solid var(--color-border, rgba(148, 163, 184, 0.1));
    color: var(--color-text-primary, #f1f5f9);
    cursor: pointer;
    font-family: inherit;
    font-size: 0.95rem;
    text-align: left;
    padding: 0.85rem 1rem;
    border-radius: var(--radius-sm, 6px);
    transition: border-color 150ms ease, background-color 150ms ease, transform 150ms ease;
    display: flex;
    align-items: center;
    gap: 0.85rem;
  }

  button:hover,
  button:focus-visible {
    border-color: var(--color-primary, #f59e0b);
    background: var(--color-surface-hover, rgba(30, 41, 59, 0.8));
    outline: none;
  }

  .section-number {
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    font-weight: 700;
    color: var(--color-primary, #f59e0b);
    font-size: 0.85rem;
    min-width: 2rem;
    letter-spacing: 0.05em;
  }

  .section-title {
    flex-grow: 1;
    line-height: 1.4;
  }

  .arrow {
    color: var(--color-text-muted, #64748b);
    opacity: 0;
    transform: translateX(-4px);
    transition: opacity 150ms ease, transform 150ms ease, color 150ms ease;
    font-size: 1rem;
  }

  button:hover .arrow,
  button:focus-visible .arrow,
  .active button .arrow {
    opacity: 1;
    transform: translateX(0);
    color: var(--color-primary, #f59e0b);
  }

  .active button {
    border-color: var(--color-primary, #f59e0b);
    background: var(--color-surface-hover, rgba(30, 41, 59, 0.8));
  }
  .active .section-title { font-weight: 600; }

  @media (max-width: 640px) {
    button {
      font-size: 0.9rem;
      padding: 0.75rem 0.85rem;
    }
    .section-number {
      font-size: 0.8rem;
      min-width: 1.75rem;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    button, .arrow { transition: none; }
  }
</style>
