<script>
  import { onMount } from 'svelte';
  import { generateTableOfContents } from '$lib/utils/newsletterLoader';

  export let component = null; // The newsletter component to render
  export let showTableOfContents = true;
  export const metadata = { title: '', date: '' };

  let contentElement;
  let toc = [];

  onMount(() => {
    if (showTableOfContents && contentElement) {
      toc = generateTableOfContents(contentElement);
    }
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

<div class="newsletter-content">
  {#if showTableOfContents && toc.length > 0}
    <div class="table-of-contents">
      <h2>Table of Contents</h2>
      <ul>
        {#each toc as item}
          <li class="toc-item-{item.level}">
            <a href="#{item.id}" on:click|preventDefault={() => scrollToSection(item.id)}>{item.text}</a>
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  <div class="content" bind:this={contentElement}>
    {#if component}
      <svelte:component this={component} />
    {:else}
      <p>No content available for this newsletter.</p>
    {/if}
  </div>
</div>

<style>
  .newsletter-content {
    max-width: 100%;
    margin: 0 auto;
    padding: 0.75rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
  }

  .table-of-contents {
    border-left: 3px solid #3498db;
    padding: 0.75rem;
    margin-bottom: 1.25rem;
    background-color: rgba(52, 152, 219, 0.1);
    border-radius: 0 4px 4px 0;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .table-of-contents:hover {
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
  }

  .table-of-contents ul {
    list-style-type: none;
    padding-left: 0;
    position: relative;
  }

  .table-of-contents ul::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 1px;
    background-color: rgba(52, 152, 219, 0.3);
  }

  .table-of-contents li {
    position: relative;
    padding-left: 0.75rem;
  }

  .table-of-contents li::before {
    content: '';
    position: absolute;
    left: -4px;
    top: 50%;
    width: 8px;
    height: 8px;
    background-color: #3498db;
    border-radius: 50%;
    transform: translateY(-50%);
  }

  .toc-item-2 {
    margin-left: 0;
    margin-bottom: 0.35rem;
  }

  .toc-item-3 {
    margin-left: 0.75rem;
    margin-bottom: 0.35rem;
  }

  .table-of-contents a {
    text-decoration: none;
    transition: color 0.3s ease;
  }

  .table-of-contents a:hover {
    text-decoration: underline;
    border-bottom-color: #3498db;
  }

  /* Keep the global styles for the newsletter content */
  /* These will apply to the content inside the svelte:component */
</style>