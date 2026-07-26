<script>
  // Same gate as /book, same store, same codes. Unlocking either one unlocks
  // the other for the rest of the page load.
  import BookGate from '$lib/components/BookGate.svelte';
  import { bookUnlocked } from '$lib/stores/bookAccess.js';
</script>

{#if $bookUnlocked}
  <slot />
{:else}
  <BookGate subtitle="Enter your password to open the reader." />
{/if}
