<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import summary from '$lib/data/factcheck-summary.json';

  let visible = false;
  onMount(() => { visible = true; });

  // Nothing on this page is a typed-in number. Every figure comes from
  // factcheck-summary.json, which sts.py generates alongside the trace itself,
  // so the page cannot claim something the audit does not say.
  const n = (v) => (v ?? 0).toLocaleString('en-US');
  const pct = (a, b) => (b ? Math.round((a / b) * 100) : 0);

  const asOf = new Date(summary.generated + 'T00:00:00Z')
    .toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });

  const tiles = [
    { num: n(summary.claims), label: 'claims traced', tone: 'plain' },
    { num: n(summary.resolvable), label: 'linked to an exact commit', tone: 'good' },
    { num: n(summary.broken), label: 'no receipt yet', tone: 'warn' },
    { num: n(summary.by_verdict?.CONTRADICTED ?? 0), label: 'contradicted', tone: 'good' },
    { num: n(summary.urls), label: 'external citations', tone: 'plain' },
    { num: n(summary.internal_refs), label: 'internal cross references', tone: 'plain' }
  ];
</script>

<svelte:head>
  <title>Fact-check: audit every claim in Surviving the Singularity</title>
  <meta name="description" content="Every checkable claim in the book, traced back to the commit and source behind it. {n(summary.claims)} claims, {n(summary.resolvable)} with a permalink to the exact line on GitHub. Audit it yourself." />
  <link rel="canonical" href="https://survivingthesingularity.com/factcheck" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:title" content="Don't trust the book. Audit it." />
  <meta property="og:description" content="Every checkable claim traced back to the commit and the source behind it, including the places the trail breaks." />
  <meta property="og:url" content="https://survivingthesingularity.com/factcheck" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Don't trust the book. Audit it." />
  <meta name="twitter:description" content="Every checkable claim traced back to the commit and the source behind it, including the places the trail breaks." />
</svelte:head>

{#if visible}
<div class="fc" in:fade={{ duration: 400 }}>

  <header class="fc-header">
    <p class="fc-label">Provenance</p>
    <h1 class="fc-title">Don't trust the book. Audit it.</h1>
    <p class="fc-sub">
      Most books ask you to take their word for it. This one hands you the receipts.
      Every checkable claim in the manuscript is traced back to the sentence in the
      source, the commit that wrote it, and the evidence behind it. Pick any claim
      and follow the trail yourself.
    </p>
    <p class="fc-asof">
      As of {asOf} . book version {summary.book_version} . {n(summary.words)} words
      across {summary.sections} sections . generated at build time, not live
    </p>
  </header>

  <div class="fc-tiles">
    {#each tiles as t}
      <div class="fc-tile {t.tone}">
        <div class="fc-num">{t.num}</div>
        <div class="fc-lab">{t.label}</div>
      </div>
    {/each}
  </div>

  <section class="fc-section">
    <h2>What you can actually check</h2>
    <p>
      The audit walks each claim through ten hops: the sentence quoted word for word,
      where it sits in the book source, the stable block id, the commit that last
      touched that line, a GitHub permalink pinned to that exact commit, the source
      behind the claim, and a verdict. The repository is public and the audit runs
      against the same source the book is built from, so every link goes to the real
      thing rather than a screenshot of it.
    </p>
    <p>
      <strong>{n(summary.resolvable)} of {n(summary.claims)} claims</strong>
      ({pct(summary.resolvable, summary.claims)}%) carry a permalink you can click
      through to the exact line on GitHub.
    </p>
  </section>

  <section class="fc-section fc-honest">
    <h2>And where it breaks</h2>
    <p>
      This is the part worth trusting. An audit that only shows its wins is marketing.
    </p>
    <ul>
      <li>
        <strong>{n(summary.broken)} claims have no receipt yet.</strong> They live in
        book files that have not been committed, so there is no commit to link to.
        The page says so rather than inventing a link that would break for you.
      </li>
      <li>
        <strong>No source was fetched in this pass.</strong> Nothing here tells you
        whether a cited page is still live, paywalled, or gone. A claim marked
        UNCHECKED is not a claim that failed. It is a claim nobody has checked yet.
      </li>
      <li>
        <strong>{n(summary.wikipedia)} of {n(summary.urls)} citations are Wikipedia</strong>
        ({pct(summary.wikipedia, summary.urls)}%), and {n(summary.not_in_works_cited)}
        cited links never made it into the Works Cited appendix. Both are worth
        knowing before you weigh a claim.
      </li>
      <li>
        <strong>{n(summary.comparison_claims)} claims use comparison language</strong>
        ("more than", "the first", "larger than"). That is the exact shape of the one
        error this project has already caught and cut from the book, so those get
        flagged for extra scrutiny rather than assumed correct.
      </li>
    </ul>
    <p class="fc-note">
      The full list of what the audit cannot see sits above the statistics on the
      trace itself, not buried under them.
    </p>
  </section>

  <section class="fc-cta">
    <h2>Open the trace</h2>
    <p>
      Searchable and filterable by chapter, claim type, and verdict. Click any claim
      and the chain of custody draws itself hop by hop, and stops dead where the
      evidence does.
    </p>
    <a class="fc-button" href="/factcheck-trace.html">
      Open the full audit
      <span aria-hidden="true">-&gt;</span>
    </a>
    <p class="fc-fine">
      Opens the standalone audit page. It works offline and can be saved or shared as
      a single file. Source:
      <a href="{summary.repo}" target="_blank" rel="noopener">the public repository</a>.
    </p>
  </section>

</div>
{/if}

<style>
  .fc {
    max-width: 940px;
    margin: 0 auto;
    padding: 4rem 1.5rem 6rem;
  }

  .fc-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0 0 0.75rem;
  }

  .fc-title {
    font-size: clamp(2rem, 5vw, 3.25rem);
    line-height: 1.08;
    letter-spacing: -0.02em;
    margin: 0 0 1rem;
    color: #f1f5f9;
  }

  .fc-sub {
    font-size: 1.125rem;
    color: #94a3b8;
    max-width: 62ch;
    margin: 0 0 1.25rem;
  }

  .fc-asof {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #64748b;
    margin: 0;
  }

  .fc-tiles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(172px, 1fr));
    gap: 0.75rem;
    margin: 2.5rem 0 3rem;
  }

  .fc-tile {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;
    padding: 1rem 1.1rem;
  }

  .fc-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #f1f5f9;
  }

  .fc-tile.good .fc-num { color: #34d399; }
  .fc-tile.warn .fc-num { color: #f59e0b; }

  .fc-lab {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94a3b8;
    margin-top: 0.2rem;
    /* A label must never break mid-word. "CONTRADICTED" splitting across two
       lines reads as a typo on a page whose whole job is looking rigorous. */
    word-break: normal;
    overflow-wrap: normal;
    hyphens: none;
  }

  .fc-section {
    margin-bottom: 3rem;
  }

  .fc-section h2,
  .fc-cta h2 {
    font-size: 1.5rem;
    color: #f1f5f9;
    margin: 0 0 0.75rem;
  }

  .fc-section p,
  .fc-cta p {
    color: #94a3b8;
    max-width: 68ch;
    margin: 0 0 1rem;
  }

  .fc-section strong,
  .fc-honest strong {
    color: #f1f5f9;
  }

  .fc-honest {
    border-left: 3px solid #f59e0b;
    padding-left: 1.5rem;
  }

  .fc-honest ul {
    list-style: none;
    padding: 0;
    margin: 0 0 1rem;
  }

  .fc-honest li {
    color: #94a3b8;
    max-width: 68ch;
    margin-bottom: 0.9rem;
    padding-left: 1.1rem;
    position: relative;
  }

  .fc-honest li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.6em;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #f59e0b;
  }

  .fc-note {
    font-size: 0.9rem;
    color: #64748b;
  }

  .fc-cta {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 16px;
    padding: 2rem;
  }

  .fc-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #f59e0b;
    color: #020617;
    font-weight: 700;
    text-decoration: none;
    padding: 0.85rem 1.5rem;
    border-radius: 10px;
    transition: background 0.18s ease, transform 0.18s ease;
  }

  .fc-button:hover {
    background: #fbbf24;
    transform: translateY(-1px);
  }

  .fc-fine {
    font-size: 0.85rem;
    color: #64748b;
    margin: 1rem 0 0;
  }

  .fc-fine a {
    color: #3b82f6;
  }

  @media (max-width: 640px) {
    .fc { padding: 2.5rem 1.1rem 4rem; }
    .fc-honest { padding-left: 1rem; }
    .fc-cta { padding: 1.5rem; }
  }
</style>
