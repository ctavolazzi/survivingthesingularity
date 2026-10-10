<script>
  import EmailGate from '$lib/components/EmailGate.svelte';

  export let data;

  // The first three precedents are open to everyone; the rest unlock with an
  // email, using the same soft gate as /checklist.
  const FREE = 3;
  $: open = data.precedents.slice(0, FREE);
  $: gated = data.precedents.slice(FREE);
</script>

<svelte:head>
  <title>The Precedent Ledger: Surviving the Singularity</title>
  <meta
    name="description"
    content="Twenty-three times in history a new technology arrived and smart, respectable people got it wrong. Every case sourced. Free from the book Surviving the Singularity."
  />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:title" content="The Precedent Ledger: 23 times the experts got the future wrong" />
  <meta
    property="og:description"
    content="The novel panic of the 1790s, the robot ads of 1929, the internet as a passing fad. Every case sourced. Free."
  />
  <meta property="og:url" content="https://survivingthesingularity.com/ledger" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="The Precedent Ledger: 23 times the experts got the future wrong" />
</svelte:head>

<main class="lg">
  <header class="lg-hero">
    <p class="lg-eyebrow">Free from the book</p>
    <h1 class="lg-title">The Precedent Ledger</h1>
    <p class="lg-lede">
      {data.precedents.length} times a new technology arrived and smart, respectable people got it wrong.
      Each case is a short story, the mechanism behind it, and three things you can do this week.
      Every one is sourced in the book's bibliography.
    </p>
  </header>

  <nav class="lg-toc" aria-label="All precedents">
    <ol>
      {#each data.precedents as p, i}
        <li>
          <a href="#{p.id}">
            <span class="lg-toc-id">{p.id}</span>
            <span class="lg-toc-title">{p.title}</span>
            {#if i >= FREE}<span class="lg-toc-lock" aria-label="unlocks with email">free with email</span>{/if}
          </a>
        </li>
      {/each}
    </ol>
  </nav>

  <EmailGate
    storageKey="ledger"
    source="ledger"
    headline="Unlock all {data.precedents.length} precedents"
    sub="Free. Enter your email and the whole ledger opens right here. You'll also hear when the book launches. Unsubscribe anytime."
    buttonText="Unlock the Ledger"
  >
    {#each open as p}
      <article class="lg-case" id={p.id}>
        <p class="lg-case-meta">{p.id}{p.where ? ` · ${p.where}` : ''}</p>
        <h2 class="lg-case-title">{p.title}</h2>
        <div class="lg-prose">{@html p.html}</div>
        <p class="lg-case-src">From {p.chapter}</p>
      </article>
    {/each}

    <div slot="gated">
      {#each gated as p}
        <article class="lg-case" id={p.id}>
          <p class="lg-case-meta">{p.id}{p.where ? ` · ${p.where}` : ''}</p>
          <h2 class="lg-case-title">{p.title}</h2>
          <div class="lg-prose">{@html p.html}</div>
          <p class="lg-case-src">From {p.chapter}</p>
        </article>
      {/each}

      <aside class="lg-end">
        <h2>That's the whole ledger.</h2>
        <p>
          The book puts each of these next to the chapter it belongs to, with the full argument around it
          and every source listed.
        </p>
        <a class="lg-btn" href="/early-access">Get the book</a>
      </aside>
    </div>
  </EmailGate>
</main>

<style>
  .lg {
    box-sizing: border-box;
    width: 100%;
    max-width: 44rem;
    margin: 0 auto;
    padding: 6rem 1.25rem 4rem;
    color: #f1f5f9;
  }
  .lg-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0 0 0.75rem;
  }
  .lg-title {
    font-size: clamp(2rem, 6vw, 3rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 1rem;
  }
  .lg-lede {
    font-size: 1.1rem;
    line-height: 1.7;
    color: #94a3b8;
    margin: 0 0 2.5rem;
  }
  .lg-toc {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 0.75rem;
    padding: 1rem 1.25rem;
    margin: 0 0 3rem;
  }
  .lg-toc ol {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .lg-toc li + li {
    border-top: 1px solid rgba(148, 163, 184, 0.1);
  }
  .lg-toc a {
    display: flex;
    gap: 0.75rem;
    align-items: baseline;
    padding: 0.5rem 0;
    color: #e2e8f0;
    text-decoration: none;
  }
  .lg-toc a:hover .lg-toc-title {
    color: #f59e0b;
  }
  .lg-toc-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #f59e0b;
    min-width: 3rem;
  }
  .lg-toc-title {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
  }
  .lg-toc-lock {
    font-size: 0.75rem;
    color: #64748b;
    white-space: nowrap;
  }
  .lg-case {
    margin: 0 0 3.5rem;
    scroll-margin-top: 5rem;
  }
  .lg-case-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #f59e0b;
    margin: 0 0 0.5rem;
  }
  .lg-case-title {
    font-size: 1.6rem;
    font-weight: 800;
    line-height: 1.25;
    margin: 0 0 1.25rem;
  }
  .lg-prose :global(p) {
    font-size: 1.05rem;
    line-height: 1.8;
    color: #cbd5e1;
    margin: 0 0 1.1rem;
  }
  .lg-prose :global(strong) {
    color: #f1f5f9;
  }
  .lg-prose :global(ol),
  .lg-prose :global(ul) {
    color: #cbd5e1;
    line-height: 1.75;
    padding-left: 1.25rem;
    margin: 0 0 1.1rem;
  }
  .lg-prose :global(li) {
    margin: 0 0 0.6rem;
  }
  .lg-prose :global(img) {
    max-width: 100%;
    height: auto;
    border-radius: 0.5rem;
  }
  .lg-prose :global(em) {
    color: #94a3b8;
  }
  .lg-case-src {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
  }
  .lg-end {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 0.75rem;
    padding: 1.5rem;
  }
  .lg-end h2 {
    margin: 0 0 0.75rem;
    font-size: 1.4rem;
  }
  .lg-end p {
    color: #94a3b8;
    line-height: 1.7;
    margin: 0 0 1.25rem;
  }
  .lg-btn {
    display: inline-block;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 700;
    padding: 0.75rem 1.4rem;
    border-radius: 0.5rem;
    text-decoration: none;
  }
</style>
