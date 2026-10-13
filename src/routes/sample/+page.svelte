<script>
  import { offer } from '$lib/offer.js';
  import 'katex/dist/katex.min.css';
  import '$lib/styles/book-figures.css';
  export let data;
</script>

<svelte:head>
  <title>Free sample & reading guide | Surviving the Singularity</title>
  <meta name="description" content="Read the introduction and choose a path through Surviving the Singularity. A free sample from the current draft, with no email or password required." />
</svelte:head>

<div class="sample-page">
  <header>
    <p class="eyebrow">FREE SAMPLE · DRAFT v{data.version}</p>
    <h1>Start with the book.</h1>
    <p>Read the introduction, then use the reading guide to choose a path for your work, household, or community. These excerpts come from the current draft.</p>
    <nav aria-label="Sample sections">
      {#each data.excerpts as excerpt}
        <a href={'#' + excerpt.id}>{excerpt.title}</a>
      {/each}
    </nav>
  </header>

  {#each data.excerpts as excerpt}
    <section id={excerpt.id} aria-label={excerpt.title} class="sample-prose">
      {@html excerpt.html}
    </section>
  {/each}

  <aside aria-label="Continue reading">
    <h2>Continue with the full draft</h2>
    <p>The full reader uses the draft access code supplied with your purchase. This sample stays open to everyone.</p>
    <div class="actions">
      <a href="/early-access">See the {offer.price} book offer</a>
      <a href="/book">Open the full reader</a>
      <a href="/checklist">Try the free checklist</a>
    </div>
  </aside>
</div>

<style>
  .sample-page { max-width: 780px; margin: 0 auto; padding: 3rem 1.5rem 5rem; color: #cbd5e1; line-height: 1.8; }
  header, aside { padding-bottom: 2rem; }
  h1 { font-size: clamp(2.2rem, 6vw, 3.5rem); color: #f1f5f9; line-height: 1.15; font-weight: 800; margin: 1rem 0; }
  h2, .sample-prose :global(h1), .sample-prose :global(h2), .sample-prose :global(h3) { color: #f1f5f9; line-height: 1.3; }
  .sample-prose :global(h2) { font-size: 1.65rem; font-weight: 700; margin: 1.5rem 0 1rem; }
  .sample-prose :global(h3) { font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem; }
  .eyebrow { font-family: monospace; color: #fbbf24; letter-spacing: .08em; }
  nav, .actions { display: flex; flex-wrap: wrap; gap: .8rem 1.5rem; margin-top: 1.5rem; }
  a, .sample-prose :global(a) { color: #fbbf24; text-decoration: underline; text-underline-offset: .2em; }
  a:focus-visible, .sample-prose :global(a:focus-visible) { outline: 2px solid #fbbf24; outline-offset: 5px; }
  .sample-prose { border-top: 1px solid #334155; padding: 2rem 0; scroll-margin-top: 7rem; overflow-wrap: anywhere; }
  .sample-prose :global(img) { max-width: 100%; height: auto; }
  .sample-prose :global(p), .sample-prose :global(ul), .sample-prose :global(ol) { margin: 1.25rem 0; }
  .sample-prose :global(ul), .sample-prose :global(ol) { padding-left: 1.5rem; }
  .sample-prose :global(ul) { list-style: disc; }
  .sample-prose :global(ol) { list-style: decimal; }
  .sample-prose :global(blockquote) { border-left: 3px solid #f59e0b; padding-left: 1rem; }
  .sample-prose :global(table) { display: block; overflow-x: auto; max-width: 100%; }
  aside { border-top: 1px solid #334155; padding-top: 2rem; }
</style>
