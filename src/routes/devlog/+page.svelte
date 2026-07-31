<script>
  // The devlog index. Deliberately reachable from the footer and nowhere else:
  // these are working notes about how the book gets built and verified, not
  // part of the reader funnel, so they do not belong in the main nav.
  //
  // Individual posts are self-contained static files under /devlog/, generated
  // by postforge rather than authored here. Each carries its own provenance
  // record naming the generator version, config hash and asset licences. This
  // page is the front door to them and matches the rest of the site's chrome.
  import posts from '$lib/data/devlog.json';

  const sorted = [...posts.entries].sort((a, b) => (a.date < b.date ? 1 : -1));
</script>

<svelte:head>
  <title>Devlog | Surviving the Singularity</title>
  <meta
    name="description"
    content="Working notes on building and verifying Surviving the Singularity: the fact-checking harness, the provenance trail, and what it still cannot prove."
  />
  <!-- Linked from the footer, kept out of search. These are working notes about
       unfinished work, not pages anyone should land on cold from a query. -->
  <meta name="robots" content="noindex, follow" />
</svelte:head>

<main class="devlog">
  <header class="head">
    <p class="kicker">Devlog</p>
    <h1>How this book gets checked</h1>
    <p class="lede">
      Working notes on the machinery behind <em>Surviving the Singularity</em>: the harness that
      traces every checkable claim back to the commit that wrote it, what it proves, and the parts
      it still cannot prove. Written for people who want the engineering, not the pitch.
    </p>
    <p class="meta">
      {sorted.length} {sorted.length === 1 ? 'post' : 'posts'} · linked from the footer only
    </p>
  </header>

  <ul class="list">
    {#each sorted as p (p.slug)}
      <li>
        <a class="card" href={p.href}>
          <div class="card-main">
            <p class="card-meta">
              <time datetime={p.date}>{p.date}</time>
              <span class="dot">·</span>
              <span>{p.readingMinutes} min read</span>
            </p>
            <h2>{p.title}</h2>
            <p class="dek">{p.dek}</p>
            <ul class="tags">
              {#each p.tags as t}<li>{t}</li>{/each}
            </ul>
          </div>
          <div class="card-side">
            <span class="go">Read <span aria-hidden="true">-&gt;</span></span>
            <span class="built">{p.builtBy}</span>
          </div>
        </a>
      </li>
    {/each}
  </ul>

  <section class="note">
    <h2>Why these read differently</h2>
    <p>
      Every post is a single self-contained page carrying a provenance block: the generator version
      that built it, a hash of its configuration, the git state of the repository at build time, and
      a licence line for every image. Figures are generated from real audit output at build time.
      Nothing on those pages is live, and each one says so.
    </p>
    <p class="note-sub">
      If a number in a post disagrees with something you were told earlier, the post is the one that
      was measured.
    </p>
  </section>
</main>

<style>
  .devlog {
    max-width: 52rem;
    margin: 0 auto;
    padding: clamp(2.5rem, 7vw, 4.5rem) 1.25rem 5rem;
    color: #f1f5f9;
  }
  .kicker {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0 0 0.7rem;
  }
  h1 {
    font-size: clamp(2rem, 6vw, 3rem);
    line-height: 1.06;
    letter-spacing: -0.03em;
    margin: 0 0 0.9rem;
  }
  .lede {
    color: #94a3b8;
    font-size: clamp(1rem, 2.2vw, 1.15rem);
    line-height: 1.65;
    margin: 0 0 1rem;
    max-width: 42rem;
  }
  .meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #475569;
    margin: 0;
  }
  .head {
    border-bottom: 1px solid #1e293b;
    padding-bottom: 1.8rem;
    margin-bottom: 2rem;
  }

  .list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 1rem;
  }
  .card {
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.4rem;
    text-decoration: none;
    color: inherit;
    transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease;
  }
  .card:hover {
    border-color: #f59e0b;
    background: rgba(20, 30, 50, 0.7);
    transform: translateY(-2px);
  }
  .card-main { min-width: 0; }
  .card-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #64748b;
    margin: 0 0 0.4rem;
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }
  .dot { color: #334155; }
  .card h2 {
    font-size: clamp(1.15rem, 2.6vw, 1.5rem);
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 0 0 0.5rem;
  }
  .dek {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0 0 0.8rem;
  }
  .tags {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin: 0;
    padding: 0;
  }
  .tags li {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    color: #38bdf8;
    border: 1px solid #1e3a5f;
    border-radius: 999px;
    padding: 0.12rem 0.5rem;
  }
  .card-side {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
    flex: 0 0 auto;
    text-align: right;
  }
  .go {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #f59e0b;
    white-space: nowrap;
  }
  .built {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #475569;
    white-space: nowrap;
  }
  @media (max-width: 640px) {
    .card { flex-direction: column; gap: 0.9rem; }
    .card-side { align-items: flex-start; text-align: left; flex-direction: row; gap: 0.9rem; }
  }

  .note {
    margin-top: 3rem;
    border-top: 1px solid #1e293b;
    padding-top: 1.6rem;
  }
  .note h2 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #94a3b8;
    margin: 0 0 0.7rem;
  }
  .note p {
    color: #94a3b8;
    font-size: 0.92rem;
    line-height: 1.65;
    margin: 0 0 0.7rem;
    max-width: 42rem;
  }
  .note-sub { color: #64748b; font-size: 0.86rem; }

  @media (prefers-reduced-motion: reduce) {
    .card:hover { transform: none; }
  }
</style>
