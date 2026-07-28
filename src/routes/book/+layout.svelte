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

    // Chapter metadata comes through $page.data because the chapter page's own
    // <svelte:head> sits inside the gate and therefore never renders for a
    // crawler or a link unfurler.
    $: section = $page.data?.section;
</script>

<!-- The head lives here, above the gate, not in the page components. Everything
     below renders only when `unlocked` is true, and that store is in-memory and
     starts false on every load - so a crawler, an iMessage preview or a Discord
     unfurl never reached the metadata in +page.svelte. In production /book,
     /read and every /book/[sectionId] were serving no title, no share card, and
     crucially no robots directive: the `noindex` this route was believed to
     carry has never once been emitted, while /book was also listed in
     sitemap.xml and robots.txt allows everything. -->
<svelte:head>
  {#if isBookRoot}
    <title>Read the Book | Surviving the Singularity</title>
    <meta name="description" content="The full current draft of Surviving the Singularity, navigable chapter by chapter." />
    <meta property="og:title" content="Read the book, chapter by chapter." />
    <meta property="og:description" content="The complete current draft of Surviving the Singularity, navigable chapter by chapter." />
    <meta property="og:url" content="https://survivingthesingularity.com/book" />
  {:else if section}
    <title>{section.title} | Surviving the Singularity</title>
    <meta name="description" content="Read {section.title} from Surviving the Singularity." />
    <meta property="og:title" content="{section.title} | Surviving the Singularity" />
    <meta property="og:description" content="Read {section.title} from Surviving the Singularity." />
    <meta property="og:url" content="https://survivingthesingularity.com{$page.url.pathname}" />
  {/if}

  <!-- Genuinely noindex, and now actually emitted. Every route under /book is
       password-gated, so the only thing a crawler can ever see here is the
       gate; an indexed gate is a worse search result than no result. The SEO
       doors are the pages that render real content to a crawler: /, /blog,
       /about, /checklist, /signals, /early-access. `sts.py sitemap` keeps
       these routes out of sitemap.xml to match. -->
  <meta name="robots" content="noindex" />

  <!-- noindex does not suppress link previews - iMessage, Discord, Slack and
       WhatsApp read the og: tags, which is what we want when a chapter link
       gets sent to someone. Rebuild the card with `sts.py og --render`. -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:image" content="https://survivingthesingularity.com/images/og/book.png" />
  <meta property="og:image:secure_url" content="https://survivingthesingularity.com/images/og/book.png" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="2400" />
  <meta property="og:image:height" content="1260" />
  <meta property="og:image:alt" content="Surviving the Singularity: read the full draft, chapter by chapter." />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://survivingthesingularity.com/images/og/book.png" />
</svelte:head>

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
