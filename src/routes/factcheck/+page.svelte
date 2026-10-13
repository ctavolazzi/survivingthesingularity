<script>
  import summary from '$lib/data/factcheck-summary.json';
  import book from '$lib/data/book/book.json';

  // Nothing on this page is a typed-in number. Every figure comes from
  // factcheck-summary.json, which sts.py generates alongside the trace itself,
  // so the page cannot claim something the audit does not say.
  const n = (v) => (v ?? 0).toLocaleString('en-US');
  const pct = (a, b) => (b ? Math.round((a / b) * 100) : 0);

  const asOf = new Date(summary.generated + 'T00:00:00Z')
    .toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });

  const tiles = [
    { num: n(summary.claims), label: 'detected records', tone: 'plain' },
    { num: n(summary.resolvable), label: 'linked to an exact commit', tone: 'good' },
    { num: n(summary.broken), label: 'no receipt yet', tone: 'warn' },
    { num: n(summary.by_verdict?.UNCHECKED ?? 0), label: 'unchecked records', tone: 'warn' },
    { num: n(summary.urls), label: 'external citations', tone: 'plain' },
    { num: n(summary.internal_refs), label: 'internal cross references', tone: 'plain' }
  ];
</script>

<svelte:head>
  <title>Evidence and historical audit: Surviving the Singularity</title>
  <meta name="description" content="A historical mechanical audit of book version {summary.book_version}, with explicit coverage limits and sources for current homepage claims. This is not a certification of the current manuscript." />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:title" content="Don't trust the book. Audit it." />
  <meta property="og:description" content="Historical source tracing, current homepage sources, and the limits of automated checks." />
  <meta property="og:url" content="https://survivingthesingularity.com/factcheck" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Don't trust the book. Audit it." />
  <meta name="twitter:description" content="Historical source tracing, current homepage sources, and the limits of automated checks." />
</svelte:head>

<div class="fc">

  <header class="fc-header">
    <p class="fc-label">Provenance</p>
    <h1 class="fc-title">Don't trust the book. Audit it.</h1>
    <p class="fc-sub">
      Follow the sources, inspect the manuscript, and distinguish what the tools
      check from what still needs human judgment. A reference resolving is useful;
      it does not establish that a sentence is true.
    </p>
    <p class="fc-asof">
      Historical snapshot: {asOf} · book version {summary.book_version} ·
      {n(summary.words)} words across {summary.sections} sections · stored results, not a live audit
    </p>
  </header>

  <section class="fc-section fc-honest" aria-labelledby="coverage-heading">
    <h2 id="coverage-heading">This snapshot covers an older edition</h2>
    <p>
      The current manuscript is version <strong>{book.version}</strong>, updated
      {book.lastUpdated}. The trace below covers <strong>{summary.book_version}</strong>.
      Its counts and GitHub links describe that historical source, not the present
      text. A new whole-manuscript audit has not been published here.
    </p>
    <p>
      Automated statuses describe mechanical checks. <strong>SUPPORTED</strong>
      can mean an internal chapter reference resolves or an image exists.
      <strong>UNCHECKED</strong> means a needed check was not run;
      <strong>UNCHECKABLE</strong> means this tool cannot adjudicate it.
      A working URL or matching page title would establish source availability,
      not that the source supports the wording, quantity, or causal inference.
      These results are not a human fact-check or a certification of accuracy.
    </p>
  </section>

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
      This stored run walks mechanically detected records through a chain:
      the quoted sentence, its location and block identifier, its git receipt,
      a public permalink where resolvable, source information, and a mechanical
      status. It finds some URLs, figures, references, dates, statistics, and
      attribution or causal wording. It does not detect every factual claim,
      and it does not adjudicate the meaning of the external evidence.
    </p>
    <p>
      <strong>{n(summary.resolvable)} of {n(summary.claims)} historical records</strong>
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
        <strong>{n(summary.broken)} records lacked a resolvable public receipt
        in this run.</strong> A receipt proves where the text was recorded, not
        whether its claim is correct. Its line numbers belong to the linked
        historical revision.
      </li>
      <li>
        <strong>No source was fetched in this pass.</strong> Nothing here tells you
        whether a cited page is still live, paywalled, or gone. A claim marked
        UNCHECKED means this tool did not complete the relevant check in this
        run. It says nothing about checks someone may have performed elsewhere.
      </li>
      <li>
        <strong>{n(summary.wikipedia)} of {n(summary.urls)} citations are Wikipedia</strong>
        ({pct(summary.wikipedia, summary.urls)}%), and {n(summary.not_in_works_cited)}
        cited links never made it into the Works Cited appendix. Both are worth
        knowing before you weigh a claim.
      </li>
      <li>
        <strong>{n(summary.comparison_claims)} claims use comparison language</strong>
        ("more than", "the first", "larger than"). Such comparisons need matching
        populations, measures, and time periods; detection alone does not verify
        that the comparison is valid.
      </li>
    </ul>
    <p class="fc-note">
      The full coverage limits also appear in the historical trace. Zero
      contradictions detected by a limited checker is not proof of zero errors.
      Homepage copy is outside this manuscript extraction.
    </p>
  </section>

  <section class="fc-section" aria-labelledby="homepage-sources">
    <h2 id="homepage-sources">Sources for the homepage claims</h2>
    <p>
      <a href="https://www.goldmansachs.com/insights/articles/generative-ai-could-raise-global-gdp-by-7-percent" target="_blank" rel="noopener noreferrer">Goldman Sachs (2023)</a>
      estimates that generative AI could expose the equivalent of 300 million
      full-time jobs to automation. It does not count 300 million eliminated jobs.
    </p>
    <p>
      <a href="https://www.mercer.com/en-gb/insights/talent-and-transformation/skill-based-talent-management/ai-and-early-career/" target="_blank" rel="noopener noreferrer">Mercer (2026)</a>
      reports that 99% of executives in its survey expect AI-related reductions
      affecting 1–20% of roles over two years. Expectations in a surveyed group
      are not observed outcomes or a measurement of all employers.
    </p>
    <p>
      <a href="https://arxiv.org/abs/2401.02843" target="_blank" rel="noopener noreferrer">Grace et al. (2024), surveying 2,778 AI researchers in 2023</a>
      reports aggregate estimates of a 10% chance of high-level machine
      intelligence by 2027 and a 50% chance by 2047. The author's specific
      November 2027 prediction is separate from this survey and may be wrong.
    </p>
    <p>
      <a href="https://github.com/huggingface/lerobot" target="_blank" rel="noopener noreferrer">LeRobot</a>
      provides open-source robotics tools and supported hardware documentation.
      Affordable experimental hardware does not establish equivalent capability,
      safety, or reliability to a more expensive industrial system.
    </p>
    <p>
      Found an error? Send the passage, edition, and a source to
      <a href="mailto:info@survivingthesingularity.com">info@survivingthesingularity.com</a>.
    </p>
  </section>

  <section class="fc-cta">
    <h2>Open the historical trace</h2>
    <p>
      Search or filter the stored version {summary.book_version} records by
      chapter, detected type, and mechanical status. Click a record to inspect
      the available links and unresolved steps.
    </p>
    <!-- rel="external": the trace is a static document under static/, not a
         route of this app. Without it the prerenderer follows the link, cannot
         resolve a static directory URL, and fails the build on a 404 for a page
         that exists. -->
    <a class="fc-button" href="/factcheck-trace/" rel="external">
      Open the historical audit
      <span aria-hidden="true">-&gt;</span>
    </a>
    <p class="fc-fine">
      Opens the standalone historical audit page. It works offline and can be
      saved or shared as a single file. Source:
      <a href="{summary.repo}" target="_blank" rel="noopener">the public repository</a>.
    </p>
  </section>

</div>

<style>
  /* Fades in over 400ms with CSS, not `{#if visible}` + in:fade. The gate kept
     this whole page out of the served HTML until JavaScript ran. See the note in
     src/routes/blog/+page.svelte. */
  .fc {
    max-width: 940px;
    margin: 0 auto;
    padding: 4rem 1.5rem 6rem;
    animation: page-fade 400ms linear;
  }

  @keyframes page-fade {
    from { opacity: 0; }
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
    color: #94a3b8;
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
    color: #94a3b8;
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
    color: #94a3b8;
    margin: 1rem 0 0;
  }

  .fc-fine a,
  .fc-section a {
    color: #fbbf24;
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  @media (max-width: 640px) {
    .fc { padding: 2.5rem 1.1rem 4rem; }
    .fc-honest { padding-left: 1rem; }
    .fc-cta { padding: 1.5rem; }
  }
</style>
