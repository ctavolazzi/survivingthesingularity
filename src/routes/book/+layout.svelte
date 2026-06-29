<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import Spacer from '$lib/components/Spacer.svelte';
    import SimpleBookCallout from '$lib/components/SimpleBookCallout.svelte';
    import { page } from '$app/stores';

    let showLowerSections = false;

    $: isBookRoot = $page.url.pathname === '/book';

    onMount(() => {
        setTimeout(() => {
            showLowerSections = true;
        }, 1000);
    });
</script>

{#if isBookRoot}
  <!-- Main /book page has its own full-width layout — no wrapper needed -->
  <slot />
{:else}
  <!-- Section sub-pages (/book/[sectionId]) need the prose reader layout -->
  <main class="bg-gray-950 text-gray-100 reader-main">
    <div class="reader-container" in:fade="{{ duration: 500 }}">
      <div class="prose prose-lg dark:prose-invert reader-prose">
        <slot />
      </div>

      {#if showLowerSections}
        <Spacer height="48px" />
        <SimpleBookCallout
          title="Navigate the Path to Singularity"
          description="Get the insights and strategies you need to prepare for the technological changes that will reshape our world."
          buttonText="Explore the Book"
          buttonLink="/book"
        />
      {/if}
    </div>
  </main>
{/if}

<style>
  .reader-main {
    width: 100%;
    min-height: 60vh;
  }
  .reader-container {
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
    padding: clamp(32px, 5vw, 64px) clamp(20px, 5vw, 40px);
    box-sizing: border-box;
  }
  :global(.reader-prose) {
    max-width: none;
  }
  :global(.toc-link) {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    background: rgba(30, 41, 59, 0.5);
    color: #f1f5f9;
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1rem;
    transition: border-color 150ms ease, background 150ms ease;
  }
  :global(.toc-link:hover) {
    background: rgba(30, 41, 59, 0.8);
    border-color: #f59e0b;
    color: #f59e0b;
  }
</style>
