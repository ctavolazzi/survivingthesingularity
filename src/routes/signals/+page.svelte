<script>
  export let data;

  const { items, generatedAt, itemCount } = data;

  // Group items by published_at date
  function groupByDate(items) {
    const groups = new Map();
    for (const item of items) {
      const date = item.published_at || 'Unknown date';
      if (!groups.has(date)) groups.set(date, []);
      groups.get(date).push(item);
    }
    return [...groups.entries()].sort((a, b) => b[0].localeCompare(a[0]));
  }

  $: grouped = groupByDate(items);

  function formatDate(dateStr) {
    try {
      return new Date(dateStr + 'T00:00:00Z').toLocaleDateString('en-US', {
        year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC'
      });
    } catch {
      return dateStr;
    }
  }

  function updatedAgo(isoStr) {
    if (!isoStr) return '';
    const hours = Math.floor((Date.now() - new Date(isoStr).getTime()) / 3600000);
    if (hours < 1) return 'just now';
    if (hours < 24) return `${hours}h ago`;
    return `${Math.floor(hours / 24)}d ago`;
  }

  function flaggedFor(keywords) {
    if (!keywords || keywords.length === 0) return '';
    return 'Flagged for: ' + keywords.slice(0, 4).join(', ');
  }

  function shortAuthors(authors) {
    if (!authors || authors.length === 0) return '';
    if (authors.length === 1) return authors[0];
    if (authors.length === 2) return authors.join(', ');
    return authors[0] + ', ' + authors[1] + ', et al.';
  }

  const TAG_COLORS = {
    Robotics: 'tag-robotics',
    Agents: 'tag-agents',
    Research: 'tag-research',
  };
</script>

<svelte:head>
  <title>Research Signals: Surviving the Singularity</title>
  <meta name="description" content="Algorithmically swept arXiv research ranked by singularity relevance. Auto-updated daily. Not hand-curated." />
  <link rel="alternate" type="application/rss+xml" title="Research Signals RSS" href="/signals.xml" />
</svelte:head>

<div class="signals-page">
  <div class="page-inner">

    <!-- How this feed works banner -->
    <div class="how-banner" id="how-it-works">
      <div class="how-header">
        <span class="how-badge">ALGORITHMIC FEED</span>
        <h1 class="page-title">Research Signals</h1>
        <p class="how-desc">
          This feed is discovered and ranked automatically, not hand-picked. A daily script fetches recent
          preprints from the <a href="https://arxiv.org" target="_blank" rel="noopener noreferrer">arXiv API</a>
          across AI, robotics, and multi-agent categories, then scores each paper by how closely its title and
          abstract match keywords relevant to the singularity thesis. Papers must exceed a minimum relevance
          threshold to appear here. Presence is not an endorsement and does not imply accuracy or importance.
          Every item links directly to its source. Read the <a href="/disclaimer#signals">full disclaimer</a>.
        </p>
        <div class="how-links">
          <a href="/book" class="how-link">The book →</a>
          <a href="/checklist" class="how-link">Readiness checklist →</a>
          <a href="/signals.xml" class="how-link rss-link">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <circle cx="6.18" cy="17.82" r="2.18"/>
              <path d="M4 4.44v2.83c7.03 0 12.73 5.7 12.73 12.73h2.83c0-8.59-6.97-15.56-15.56-15.56zm0 5.66v2.83c3.9 0 7.07 3.17 7.07 7.07h2.83c0-5.47-4.43-9.9-9.9-9.9z"/>
            </svg>
            RSS feed
          </a>
        </div>
      </div>
      <div class="how-meta">
        <span class="meta-count">{itemCount} signals</span>
        <span class="meta-sep">·</span>
        <span class="meta-updated">Updated {updatedAgo(generatedAt)}</span>
      </div>
    </div>

    <!-- Feed -->
    <div class="feed">
      {#each grouped as [date, dateItems]}
        <div class="date-group">
          <div class="date-header">
            <span class="date-label">{formatDate(date)}</span>
            <span class="date-count">{dateItems.length} signal{dateItems.length !== 1 ? 's' : ''}</span>
          </div>
          <div class="cards">
            {#each dateItems as item}
              <article class="signal-card">
                <div class="card-top">
                  <span class="card-tag {TAG_COLORS[item.tag] || 'tag-research'}">{item.tag}</span>
                  <span class="card-score" title="Relevance score">
                    <span class="score-val">{item.score.toFixed(1)}</span>
                    <span class="score-label">score</span>
                  </span>
                  <span class="card-category">{item.category}</span>
                </div>

                <h2 class="card-title">
                  <a href={item.url} target="_blank" rel="noopener noreferrer" class="card-link">
                    {item.title}
                  </a>
                </h2>

                {#if item.authors && item.authors.length > 0}
                  <p class="card-authors">{shortAuthors(item.authors)}</p>
                {/if}

                {#if item.matched_keywords && item.matched_keywords.length > 0}
                  <p class="card-flagged">{flaggedFor(item.matched_keywords)}</p>
                  <div class="card-keywords">
                    {#each item.matched_keywords.slice(0, 6) as kw}
                      <span class="kw-chip">{kw}</span>
                    {/each}
                  </div>
                {/if}

                {#if item.summary}
                  <p class="card-summary">{item.summary.slice(0, 200)}{item.summary.length > 200 ? '...' : ''}</p>
                {/if}

                <div class="card-foot">
                  <a href={item.url} target="_blank" rel="noopener noreferrer" class="card-source-link">
                    arXiv:{item.id} &rarr;
                  </a>
                </div>
              </article>
            {/each}
          </div>
        </div>
      {/each}
    </div>

    <footer class="page-foot">
      <p>
        Signals are swept daily from arXiv by an automated script. Rankings are algorithmic and may surface
        irrelevant, low-quality, or off-thesis papers. This is not curation. See the
        <a href="/disclaimer#signals">disclaimer</a> for details.
      </p>
      <p>
        <a href="/signals.xml" class="rss-link-foot">Subscribe via RSS</a>
        &middot;
        <a href="/book">The book</a>
        &middot;
        <a href="/checklist">Readiness checklist</a>
      </p>
    </footer>

  </div>
</div>

<style>
  .signals-page {
    padding: 3rem 1.5rem 6rem;
    background: #020617;
    color: #e2e8f0;
    min-height: 100vh;
  }

  .page-inner {
    max-width: 860px;
    margin: 0 auto;
  }

  /* How-it-works banner */
  .how-banner {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 14px;
    padding: 2rem;
    margin-bottom: 3rem;
  }

  .how-header {
    margin-bottom: 1rem;
  }

  .how-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    color: #f59e0b;
    text-transform: uppercase;
    background: rgba(245, 158, 11, 0.07);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 4px;
    padding: 0.25rem 0.6rem;
    margin-bottom: 1rem;
    font-family: var(--font-mono, monospace);
  }

  .page-title {
    font-size: clamp(1.8rem, 4vw, 2.6rem);
    font-weight: 900;
    color: #f1f5f9;
    margin: 0 0 1rem;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }

  .how-desc {
    font-size: 0.92rem;
    color: #94a3b8;
    line-height: 1.75;
    margin: 0 0 1rem;
    max-width: 680px;
  }

  .how-desc a {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  .how-desc a:hover {
    color: #fbbf24;
  }

  .how-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1.25rem;
    margin-top: 0.75rem;
  }

  .how-link {
    font-size: 0.85rem;
    color: #64748b;
    text-decoration: none;
    transition: color 0.15s;
  }

  .how-link:hover {
    color: #f59e0b;
  }

  .rss-link {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    color: #f97316;
  }

  .rss-link:hover {
    color: #fb923c;
  }

  .how-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.78rem;
    font-family: var(--font-mono, monospace);
    color: #475569;
    border-top: 1px solid rgba(148, 163, 184, 0.08);
    padding-top: 0.85rem;
  }

  .meta-count {
    color: #f59e0b;
    font-weight: 700;
  }

  .meta-sep {
    color: #1e293b;
  }

  /* Date groups */
  .date-group {
    margin-bottom: 2.5rem;
  }

  .date-header {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
  }

  .date-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
    font-family: var(--font-mono, monospace);
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .date-count {
    font-size: 0.72rem;
    color: #475569;
    font-family: var(--font-mono, monospace);
  }

  /* Cards */
  .cards {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .signal-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 10px;
    padding: 1.25rem 1.35rem;
    transition: border-color 0.2s;
  }

  .signal-card:hover {
    border-color: rgba(245, 158, 11, 0.2);
  }

  .card-top {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.65rem;
    flex-wrap: wrap;
  }

  .card-tag {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-radius: 3px;
    padding: 0.15rem 0.45rem;
    font-family: var(--font-mono, monospace);
  }

  .tag-agents {
    color: #60a5fa;
    background: rgba(96, 165, 250, 0.08);
    border: 1px solid rgba(96, 165, 250, 0.2);
  }

  .tag-robotics {
    color: #34d399;
    background: rgba(52, 211, 153, 0.08);
    border: 1px solid rgba(52, 211, 153, 0.2);
  }

  .tag-research {
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.07);
    border: 1px solid rgba(245, 158, 11, 0.18);
  }

  .card-score {
    display: flex;
    align-items: baseline;
    gap: 0.2rem;
    margin-left: auto;
  }

  .score-val {
    font-size: 0.82rem;
    font-weight: 700;
    color: #f59e0b;
    font-family: var(--font-mono, monospace);
  }

  .score-label {
    font-size: 0.62rem;
    color: #475569;
    font-family: var(--font-mono, monospace);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .card-category {
    font-size: 0.68rem;
    color: #475569;
    font-family: var(--font-mono, monospace);
  }

  .card-title {
    font-size: 0.98rem;
    font-weight: 600;
    line-height: 1.5;
    margin: 0 0 0.4rem;
    color: #f1f5f9;
  }

  .card-link {
    color: inherit;
    text-decoration: none;
    transition: color 0.15s;
  }

  .card-link:hover {
    color: #f59e0b;
  }

  .card-link:focus-visible {
    outline: 2px solid #f59e0b;
    outline-offset: 2px;
    border-radius: 2px;
  }

  .card-authors {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0 0 0.5rem;
    font-style: italic;
  }

  .card-flagged {
    font-size: 0.75rem;
    color: #64748b;
    margin: 0 0 0.4rem;
    font-family: var(--font-mono, monospace);
  }

  .card-keywords {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin-bottom: 0.65rem;
  }

  .kw-chip {
    font-size: 0.65rem;
    font-family: var(--font-mono, monospace);
    color: #94a3b8;
    background: rgba(148, 163, 184, 0.07);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 3px;
    padding: 0.1rem 0.4rem;
  }

  .card-summary {
    font-size: 0.83rem;
    color: #64748b;
    line-height: 1.65;
    margin: 0 0 0.75rem;
  }

  .card-foot {
    border-top: 1px solid rgba(148, 163, 184, 0.06);
    padding-top: 0.6rem;
  }

  .card-source-link {
    font-size: 0.75rem;
    color: #3b82f6;
    text-decoration: none;
    font-family: var(--font-mono, monospace);
    transition: color 0.15s;
  }

  .card-source-link:hover {
    color: #60a5fa;
  }

  /* Footer */
  .page-foot {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(148, 163, 184, 0.08);
  }

  .page-foot p {
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.7;
    margin: 0 0 0.5rem;
  }

  .page-foot a {
    color: #64748b;
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  .page-foot a:hover {
    color: #94a3b8;
  }

  .page-foot .rss-link-foot {
    color: #f97316;
  }

  .page-foot .rss-link-foot:hover {
    color: #fb923c;
  }
</style>
