<script>
  import { onMount } from 'svelte';
  import { generateTableOfContents } from '$lib/utils/newsletterLoader';

  export let component = null; // The newsletter component to render
  export const metadata = { title: '', date: '' };

  let contentElement;

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
</style>