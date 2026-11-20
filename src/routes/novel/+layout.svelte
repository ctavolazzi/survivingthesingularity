<script>
  // Private reader for the revised novel. Not linked from the navbar, the
  // footer or sitemap.xml, and noindex. It sits behind the same client-side
  // password gate as /book (BookGate + the in-memory bookUnlocked store), which
  // is friction, not authentication: see $lib/bookAccessCode.js.
  import { page } from '$app/stores';
  import { bookUnlocked } from '$lib/stores/bookAccess.js';
  import BookGate from '$lib/components/BookGate.svelte';
  import { novelPrefs } from '$lib/novel/novelReader.js';

  $: section = $page.data?.section;
</script>

<!-- Above the gate so the robots directive is always emitted. -->
<svelte:head>
  <title>{section ? `${section.title} | ` : ''}Surviving the Singularity, the novel</title>
  <meta name="robots" content="noindex, nofollow" />
</svelte:head>

{#if !$bookUnlocked}
  <BookGate subtitle="Enter the book password to read the novel." />
{:else}
  <div
    class="novel-shell theme-{$novelPrefs.theme}"
    style="--novel-size: {$novelPrefs.size}px"
  >
    <slot />
  </div>
{/if}

<style>
  .novel-shell {
    --bg: #0b1120;
    --ink: #e5e7eb;
    --muted: #94a3b8;
    --rule: rgba(148, 163, 184, 0.18);
    --card: rgba(30, 41, 59, 0.55);
    --accent: #f59e0b;
    --accent-ink: #0f172a;
    background: var(--bg);
    color: var(--ink);
    min-height: 100vh;
    width: 100%;
    /* Room for the site's floating navbar. */
    padding-top: 72px;
    box-sizing: border-box;
  }
  .novel-shell.theme-paper {
    --bg: #f6f1e7;
    --ink: #1f2328;
    --muted: #5b6470;
    --rule: rgba(31, 35, 40, 0.15);
    --card: rgba(255, 255, 255, 0.7);
    --accent: #b45309;
    --accent-ink: #fffaf0;
  }
</style>
