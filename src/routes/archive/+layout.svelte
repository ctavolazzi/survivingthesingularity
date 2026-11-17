<script>
  // Same gate as /book and /read, same store, same codes.
  import BookGate from '$lib/components/BookGate.svelte';
  import { bookUnlocked } from '$lib/stores/bookAccess.js';
</script>

<!-- Head in the layout so it is emitted above the gate, as on /read. -->
<svelte:head>
  <title>Archive: the earlier draft | Surviving the Singularity</title>
  <meta name="description" content="The earlier nonfiction draft of Surviving the Singularity, kept readable for the people who preordered it." />
  <meta name="robots" content="noindex" />
</svelte:head>

{#if $bookUnlocked}
  <slot />
{:else}
  <BookGate subtitle="Enter the password from your confirmation email to open the archive." />
{/if}
