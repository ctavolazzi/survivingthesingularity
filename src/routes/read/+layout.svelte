<script>
  // Same gate as /book, same store, same codes. Unlocking either one unlocks
  // the other for the rest of the page load.
  import BookGate from '$lib/components/BookGate.svelte';
  import { bookUnlocked } from '$lib/stores/bookAccess.js';
</script>

<!-- The head lives in the layout, not the page, because the page only renders
     once the gate is open. A crawler or a link unfurler never gets that far,
     so metadata inside +page.svelte reached nobody: /read was serving no
     title, no robots directive and no share card at all, and the `noindex`
     everyone believed was on this route has never actually been emitted. -->
<svelte:head>
  <title>Reader | Surviving the Singularity</title>
  <meta name="description" content="The full draft of Surviving the Singularity in one continuous, readable scroll." />
  <!-- Genuinely noindex: everything past this point is password-gated, so the
       only thing a crawler can index here is the gate itself. -->
  <meta name="robots" content="noindex" />

  <!-- noindex does not stop iMessage, Discord, Slack or WhatsApp unfurling the
       link - they read the og: tags, which is what we want when it gets sent
       to someone. Rebuild the card with `sts.py og --render`. -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:title" content="The whole book, one scroll." />
  <meta property="og:description" content="The full draft in one continuous, readable scroll. Your place is kept as you go." />
  <meta property="og:url" content="https://survivingthesingularity.com/read" />
  <meta property="og:image" content="https://survivingthesingularity.com/images/og/read.png" />
  <meta property="og:image:secure_url" content="https://survivingthesingularity.com/images/og/read.png" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="2400" />
  <meta property="og:image:height" content="1260" />
  <meta property="og:image:alt" content="Surviving the Singularity reader: the whole book in one continuous scroll." />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="The whole book, one scroll." />
  <meta name="twitter:description" content="The full draft in one continuous, readable scroll. Your place is kept as you go." />
  <meta name="twitter:image" content="https://survivingthesingularity.com/images/og/read.png" />
</svelte:head>

{#if $bookUnlocked}
  <slot />
{:else}
  <BookGate subtitle="Enter your password to open the reader." />
{/if}
