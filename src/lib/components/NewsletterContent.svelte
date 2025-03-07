<script>
  import { onMount } from 'svelte';
  import { generateTableOfContents } from '$lib/utils/newsletterLoader';
  import { darkMode } from '$lib/stores/darkMode';

  export let component = null; // The newsletter component to render
  export let metadata = { title: '', date: '', description: '' };

  let contentElement;
  let tableOfContents = [];
  let showTableOfContents = false;

  onMount(() => {
    // Generate table of contents after component is mounted
    setTimeout(() => {
      if (contentElement) {
        tableOfContents = generateTableOfContents(contentElement);
        showTableOfContents = tableOfContents.length > 1;
      }
    }, 100);
  });

  function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
      const yOffset = -100;
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({top: y, behavior: 'smooth'});
    }
  }
</script>

<div class="newsletter-content" class:dark={$darkMode}>
  {#if metadata.title && metadata.date}
    <div class="newsletter-header">
      <h1>{metadata.title}</h1>
      <div class="metadata">
        <span class="date">{metadata.date}</span>
      </div>

      {#if metadata.description}
        <p class="description">{metadata.description}</p>
      {/if}
    </div>
  {/if}

  {#if showTableOfContents}
    <div class="table-of-contents">
      <h2>In this issue:</h2>
      <ul>
        {#each tableOfContents as item}
          <li class="toc-item level-{item.level}">
            <button on:click={() => scrollToSection(item.id)} class="toc-link">
              {item.text}
            </button>
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  <div class="content" bind:this={contentElement}>
    {#if component}
      <svelte:component this={component} />
    {:else}
      <p class="no-content">No content available for this newsletter.</p>
    {/if}
  </div>
</div>

<style>
  .newsletter-content {
    max-width: 100%;
    margin: 0 auto;
    padding: 1.5rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #1f2937;
    background-color: #ffffff;
    border-radius: 0.5rem;
  }

  .newsletter-content.dark {
    color: #f3f4f6;
    background-color: #1f2937;
  }

  .newsletter-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
  }

  .newsletter-content.dark .newsletter-header {
    border-color: #374151;
  }

  h1 {
    font-size: 1.875rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
  }

  .metadata {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .newsletter-content.dark .metadata {
    color: #9ca3af;
  }

  .description {
    font-size: 1.1rem;
    margin: 0.5rem 0;
    color: #4b5563;
    line-height: 1.5;
  }

  .newsletter-content.dark .description {
    color: #d1d5db;
  }

  .table-of-contents {
    margin: 1.5rem 0 2rem 0;
    padding: 1rem 1.5rem;
    background-color: #f9fafb;
    border-radius: 0.5rem;
    border-left: 4px solid #3b82f6;
  }

  .newsletter-content.dark .table-of-contents {
    background-color: #111827;
    border-left-color: #60a5fa;
  }

  .table-of-contents h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 0.75rem 0;
  }

  .table-of-contents ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .toc-item {
    margin: 0.5rem 0;
  }

  .toc-item.level-3 {
    padding-left: 1.5rem;
    font-size: 0.95rem;
  }

  .toc-link {
    background: none;
    border: none;
    padding: 0;
    font-family: inherit;
    cursor: pointer;
    color: #3b82f6;
    text-align: left;
  }

  .newsletter-content.dark .toc-link {
    color: #60a5fa;
  }

  .toc-link:hover {
    text-decoration: underline;
  }

  .content {
    width: 100%;
  }

  .no-content {
    text-align: center;
    padding: 2rem 0;
    color: #6b7280;
    font-style: italic;
  }

  /* Responsive styles */
  @media (max-width: 768px) {
    .newsletter-content {
      padding: 1rem;
    }

    h1 {
      font-size: 1.5rem;
    }

    .table-of-contents {
      padding: 0.75rem 1rem;
    }
  }

  @media (max-width: 480px) {
    .newsletter-content {
      padding: 0.75rem;
    }

    .newsletter-header {
      margin-bottom: 1.5rem;
    }

    h1 {
      font-size: 1.35rem;
    }

    .description {
      font-size: 1rem;
    }
  }
</style>