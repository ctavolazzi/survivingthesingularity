<script>
    import { fade } from 'svelte/transition';
    import { page } from '$app/stores';
    import { bookUnlocked } from '$lib/stores/bookAccess.js';
    import BookGate from '$lib/components/BookGate.svelte';

    // The unlock lives in a store that is deliberately in-memory only, never
    // persisted to storage: it resets on any full page load (refresh,
    // closed-and-reopened tab, new tab), not just on demand. Keeping it in a
    // store rather than a local means /exclusive-friends-only and /read share
    // the same unlock, so a reader types one password instead of three.
    // Reading position is stored separately in localStorage, so it keeps
    // surviving a re-lock even though the gate itself doesn't.
    $: unlocked = $bookUnlocked;

    $: isBookRoot = $page.url.pathname === '/book';
</script>

{#if !unlocked}
  <BookGate />
{:else if isBookRoot}
  <!-- /book (unlocked): the reader's own layout - preface + table of
       contents, no wrapper needed. -->
  <slot />
{:else}
  <!-- Chapter pages (/book/[sectionId]) get the prose reader layout -->
  <main class="bg-gray-950 text-gray-100 reader-main">
    <div class="reader-container" in:fade="{{ duration: 500 }}">
      <div class="prose prose-lg dark:prose-invert reader-prose">
        <slot />
      </div>
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
