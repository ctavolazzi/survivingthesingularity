<script>
  import { fade, fly } from 'svelte/transition';
  import AuthorBio from '$lib/components/AuthorBio.svelte';
  import coverImage from '$lib/images/Surviving-the-Singularity-Cover.png?url';
  import { parts } from '$lib/data/stages.js';

  export let data;

  const PURCHASE_URL = '';
</script>

<svelte:head>
  <title>Surviving the Singularity - The Book</title>
  <meta name="description" content="Surviving the Singularity by Christopher Tavolazzi. A field manual for the people who refuse to be passive cargo when AI rewrites the world." />
  <meta property="og:title" content="Surviving the Singularity - The Book" />
  <meta property="og:description" content="A field manual for the people who refuse to be passive cargo when AI rewrites the world." />
  <meta property="og:image" content="/Surviving-the-Singularity-Cover.png" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="not-prose book-page">

  <!-- HERO -->
  <section class="hero" in:fade={{ duration: 600 }}>
    <div class="hero-cover">
      <img src={coverImage} alt="Surviving the Singularity book cover" loading="eager" />
    </div>
    <div class="hero-text">
      <div class="hero-eyebrow">Open Draft · v0.1 · Reader Edition</div>
      <h1>Surviving the Singularity</h1>
      <p class="hero-subtitle">
        A field manual for the people who refuse to be passive cargo when AI rewrites the world.
      </p>
      <p class="hero-byline">By <strong>Christopher Tavolazzi</strong> &middot; <span class="mono">a.k.a. Coffee Jesus</span></p>
      <div class="hero-ctas">
        <a class="cta-primary" href="#roadmap">Read the roadmap &rarr;</a>
        <a class="cta-secondary" href="/StS-free-sample.pdf" download>Download free sample (PDF)</a>
      </div>
      {#if PURCHASE_URL}
        <div class="hero-preorder">
          <div class="preorder-label">Part I: A Manual for the Cracks, available now.</div>
          <a class="cta-primary subscribe-cta" href={PURCHASE_URL} target="_blank" rel="noopener noreferrer">
            Buy the book → $7.99 launch week
          </a>
          <p class="preorder-meta">Instant EPUB download. Updates included forever.</p>
        </div>
      {/if}
      <div class="hero-preorder">
        <div class="preorder-label">Updates are posted to Substack when posted at all.</div>
        <a class="cta-primary subscribe-cta" href="https://thecoffeejesus.substack.com" target="_blank" rel="noopener noreferrer">
          Subscribe on Substack →
        </a>
        <p class="preorder-meta">No content frequency, ship date, or completion guarantee.</p>
      </div>
    </div>
  </section>

  <!-- THESIS -->
  <section class="thesis" in:fly={{ y: 20, duration: 600, delay: 200 }}>
    <div class="eyebrow">The Thesis</div>
    <h2>The shovel is digging its own hole.</h2>
    <p>
      The Singularity isn't a future event. It's a current condition.
      Tools are leaping from <em>reacting to our input</em> to <em>acting on their own</em>,
      and the pace is doubling on a curve nobody is steering.
    </p>
    <p>
      This book is a primer on the double-exponential shift in <strong>how we get our needs met</strong>.
      Work, food, health, money, relationships, governance — all of it is being renegotiated
      in real time by systems that don't need your permission to participate.
    </p>
    <p class="thesis-kicker">
      You don't need to stop the wave. You need to learn to surf it.
    </p>
  </section>

  <!-- ROADMAP: 3 PARTS / 9 STAGES -->
  <section id="roadmap" class="roadmap" in:fly={{ y: 20, duration: 600, delay: 300 }}>
    <div class="eyebrow">The Roadmap</div>
    <h2>This isn't random. It's a predictable sequence.</h2>
    <p class="roadmap-lede">AI is moving through stages. Here's the map — where we've been, where we are, and where it goes from here.</p>

    <div class="stage-grid">
      {#each parts as part}
        <div class="part-block">
          <div class="part-heading">
            <span class="part-num">{part.num}</span>
            <span class="part-title">{part.title}</span>
            <span class="part-line" aria-hidden="true"></span>
          </div>
          <div class="stages">
            {#each part.stages as stage}
              <div class="stage" class:current={stage.current}>
                <span class="stage-n">{stage.num}</span>
                <span class="stage-t">{stage.title}</span>
                {#if stage.current}
                  <span class="stage-pill">we are here</span>
                {/if}
              </div>
            {/each}
          </div>
        </div>
      {/each}
    </div>
  </section>

  <!-- STAGE 4: TELEOPERATION -->
  <section class="teleop" in:fly={{ y: 20, duration: 600, delay: 350 }}>
    <div class="teleop-pill">Stage 04 · The Transitional Economy</div>
    <h2>What if your job was piloting a robot?</h2>
    <p class="teleop-intro">
      A human in the loop is necessary right now — for safety, for quality, for accountability.
      But the human doesn't have to be <em>there</em>.
      Instead of breaking your body on-site, you pilot the machine from home.
      You could do it from the beach.
    </p>

    <ol class="story-list">
      <li class="story-item">
        <span class="story-n" aria-hidden="true">01</span>
        <div>
          <div class="story-label">Real example</div>
          <p class="story-body">Custom robotic arms, fixed to the sides of a kitchen range in a care facility. A remote worker pilots them from home to cook breakfast for residents with physical disabilities. High-quality meal. No commute. No broken back.</p>
        </div>
      </li>
      <li class="story-item">
        <span class="story-n" aria-hidden="true">02</span>
        <div>
          <div class="story-label">Built for dignity</div>
          <p class="story-body">Each setup is engineered custom for the resident's specific disability — not a generic bolt-on. Maximum dignity. Maximum quality of life. For resident and worker alike.</p>
        </div>
      </li>
    </ol>

    <div class="lockout-block">
      <div class="lockout-label">Local Control — Absolute Safety Lockout</div>
      <p class="lockout-body">
        When the shift ends, the resident <strong>manually locks the robot and unplugs it</strong>.
        No algorithm decides when the machine comes back on.
        The resident controls the switch. Complete local <strong>Autonomy</strong>.
      </p>
    </div>
  </section>

  <!-- SAMPLE EXCERPT -->
  <section class="sample" in:fly={{ y: 20, duration: 600, delay: 400 }}>
    <div class="eyebrow">A Sample</div>
    <blockquote>
      <p>
        "So the robots have taken over. Congratulations — you've lost.
        Surviving the Singularity isn't just about fending off Terminator bots or finding
        food in the era of economic collapse and climate famines. It's about staying hidden
        from autonomous drone swarms and filtering nanobots out of the water.
      </p>
      <p>
        Ah, who am I kidding? You don't need to worry about the nanobots.
        You're just a disembodied brain in a jar.
        Every sensation you've ever had, every person you've ever known
        is a hallucination produced by neural-link electrodes."
      </p>
      <footer>&mdash; from the <a href="/book/introduction">Introduction</a></footer>
    </blockquote>
  </section>

  <!-- AUTHOR BIO -->
  <div in:fly={{ y: 20, duration: 600, delay: 420 }}>
    <AuthorBio />
  </div>

  <!-- OPEN DRAFT -->
  <section class="open-draft" in:fly={{ y: 20, duration: 600, delay: 440 }}>
    <div class="eyebrow">How This Book Works</div>
    <h2>Built in public. Revised by readers.</h2>
    <p>
      This is the <strong>open draft</strong> of <em>Surviving the Singularity</em>.
      Chapters land as they're written. Typos, edges, and works-in-progress are part of the deal —
      and so is your input. Spot a glitch? A passage that lands wrong?
      A topic you want covered? <a href="/about">Reach out</a> and it goes into the next revision.
    </p>
    <p class="text-muted">
      Final print/e-book editions will be released on Amazon. Open-draft readers get early access, signed credit, and first crack at the launch.
    </p>
  </section>

  <!-- AUTHOR'S EDITION CALLOUT -->
  <section class="authors-callout" in:fly={{ y: 20, duration: 600, delay: 460 }}>
    <div class="authors-callout-inner">
      <div class="authors-callout-badge">
        <svg width="11" height="11" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 1l1.88 3.82L14 5.64l-3 2.93.71 4.12L8 10.77l-3.71 1.92L5 8.57 2 5.64l4.12-.82L8 1z"/></svg>
        Author's Edition
      </div>
      <div class="authors-callout-body">
        <p class="authors-callout-headline">Want a hand-bound, signed copy numbered 1 through 100?</p>
        <p class="authors-callout-sub">100 copies. Each one bound and signed by the author, individually numbered, with exclusive content not in the standard edition. Payment collected at launch in August 2026.</p>
      </div>
      <a href="/launch#authors-edition" class="authors-callout-cta">Reserve yours →</a>
    </div>
  </section>

  <!-- FREE SAMPLE DOWNLOAD -->
  <section class="sample-dl" in:fly={{ y: 20, duration: 600, delay: 470 }}>
    <div class="sample-dl-inner">
      <div class="eyebrow">Try Before You Commit</div>
      <h2>Free PDF Sample</h2>
      <p>Introduction + Chapter 1. No email, no signup. Just open it and read.</p>
      <a class="cta-primary" href="/StS-free-sample.pdf" download>Download (PDF)</a>
      <p class="sample-dl-meta">~10-min read · plain PDF · sharable</p>
    </div>
  </section>

  <!-- NEWSLETTER -->
  <section id="stay-in-loop" class="newsletter" in:fly={{ y: 20, duration: 600, delay: 490 }}>
    <div class="eyebrow">Stay In The Loop</div>
    <h2>Get the next chapter in your inbox.</h2>
    <p>Published on Substack. Subscribe once, get everything.</p>
    <a class="cta-primary subscribe-cta-large" href="https://thecoffeejesus.substack.com" target="_blank" rel="noopener noreferrer">
      Subscribe on Substack →
    </a>
    <p class="subscribe-meta">Free tier covers chapters + launch alerts. Founding-tier readers get bonus drops + name in book acknowledgements.</p>
  </section>

</div>

<style>
  .book-page {
    color: var(--color-text-primary, #f1f5f9);
    font-family: var(--font-primary, 'Inter', sans-serif);
    max-width: 1100px;
    margin: 0 auto;
  }

  .eyebrow,
  .hero-eyebrow {
    display: inline-block;
    font-family: var(--font-mono, var(--font-primary));
    font-size: 0.85rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--color-primary, #f59e0b);
    margin-bottom: 0.75rem;
  }

  h1, h2, h3 {
    font-family: var(--font-primary, 'Inter', sans-serif);
    color: var(--color-text-primary, #f1f5f9);
    line-height: 1.15;
    margin: 0 0 1rem;
  }

  p { line-height: 1.7; margin: 0 0 1rem; color: var(--color-text-secondary, #dde4ef); }
  .mono { font-family: var(--font-mono, monospace); color: var(--color-text-secondary); }
  .text-muted { color: var(--color-text-muted, #94a3b8); font-size: 0.9rem; }

  /* === HERO === */
  .hero {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr);
    gap: 3rem;
    align-items: center;
    margin: 2rem 0 5rem;
  }
  .hero-cover img {
    width: 100%;
    max-width: 320px;
    height: auto;
    border: 1px solid var(--color-border, rgba(148,163,184,0.1));
    display: block;
    margin: 0 auto;
  }
  .hero h1 {
    font-size: clamp(2.25rem, 5vw, 3.75rem);
    font-weight: 800;
    color: var(--color-text-primary, #f1f5f9);
  }
  .hero-subtitle { font-size: 1.2rem; color: var(--color-text-primary); margin: 1rem 0; }
  .hero-byline { font-size: 0.95rem; }
  .hero-ctas { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.75rem; }

  .cta-primary, .cta-secondary {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    transition: background-color 150ms ease, color 150ms ease, box-shadow 150ms ease;
  }
  .cta-primary {
    background: var(--color-primary, #f59e0b);
    color: #1a0f00;
  }
  .cta-primary:hover { background: var(--color-primary-light, #fbbf24); box-shadow: var(--shadow-hard, 4px 4px 0 #f59e0b); }
  .cta-secondary {
    background: transparent;
    color: var(--color-text-primary);
    border: 1px solid rgba(148,163,184,0.25);
  }
  .cta-secondary:hover { background: var(--color-surface, rgba(30,41,59,0.5)); }

  .hero-preorder {
    margin-top: 1.75rem;
    padding-top: 1.5rem;
    border-top: 1px dashed rgba(148,163,184,0.15);
  }
  .preorder-label { font-size: 0.85rem; color: var(--color-text-muted, #94a3b8); margin-bottom: 0.65rem; font-family: var(--font-mono); }
  .preorder-meta { margin-top: 0.65rem !important; font-size: 0.86rem; color: var(--color-text-muted); font-family: var(--font-mono); }
  .subscribe-cta { display: inline-block; }
  .subscribe-cta-large { display: inline-block; font-size: 1.05rem; padding: 0.85rem 1.75rem; margin-top: 0.5rem; }
  .subscribe-meta { margin-top: 1rem !important; font-size: 0.82rem; color: var(--color-text-muted); max-width: 520px; margin-left: auto !important; margin-right: auto !important; }

  /* === SECTION CARDS === */
  .thesis, .sample, .open-draft, .newsletter, .sample-dl, .roadmap, .teleop {
    background: var(--color-surface, rgba(30,41,59,0.5));
    border: 1px solid rgba(148,163,184,0.1);
    padding: 2.5rem;
    margin-bottom: 2rem;
  }
  .thesis h2, .roadmap h2, .teleop h2, .open-draft h2, .newsletter h2, .sample-dl h2 {
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 700;
  }
  .thesis-kicker { font-size: 1.15rem; color: var(--color-primary, #f59e0b); font-weight: 600; margin-top: 1.5rem; }

  /* === ROADMAP === */
  .roadmap-lede { color: var(--color-text-muted, #94a3b8); margin: 0 0 2.5rem; }

  .stage-grid { display: flex; flex-direction: column; gap: 2.5rem; }

  .part-block {}
  .part-heading {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.875rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--color-primary, #f59e0b);
  }
  .part-num {
    font-family: var(--font-mono, monospace);
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--color-text-muted, #94a3b8);
    white-space: nowrap;
  }
  .part-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--color-text-primary, #f1f5f9);
  }
  .part-line { flex: 1; height: 1px; background: rgba(241,245,249,0.06); }

  .stages { display: flex; flex-direction: column; }
  .stage {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(241,245,249,0.07);
  }
  .stage:last-child { border-bottom: none; }
  .stage-n {
    font-family: var(--font-mono, monospace);
    font-size: 0.68rem;
    color: var(--color-text-muted, #94a3b8);
    min-width: 1.75rem;
    flex-shrink: 0;
  }
  .stage-t { font-size: 0.97rem; color: var(--color-text-primary, #f1f5f9); }

  .stage.current {
    background: rgba(245,158,11,0.07);
    margin: 0 -2.5rem;
    padding: 0.875rem 2.5rem;
    border-left: 3px solid var(--color-primary, #f59e0b);
  }
  .stage.current .stage-n { color: var(--color-primary, #f59e0b); }
  .stage.current .stage-t { color: var(--color-primary-light, #fbbf24); font-weight: 600; }
  .stage-pill {
    margin-left: auto;
    font-family: var(--font-mono, monospace);
    font-size: 0.56rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-primary, #f59e0b);
    border: 1px solid rgba(245,158,11,0.45);
    padding: 0.15rem 0.45rem;
    white-space: nowrap;
    flex-shrink: 0;
  }

  /* === TELEOP === */
  .teleop { border-left: 3px solid var(--color-primary, #f59e0b); }
  .teleop-pill {
    display: inline-block;
    font-family: var(--font-mono, monospace);
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: var(--color-primary, #f59e0b);
    color: #020617;
    padding: 0.22rem 0.6rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
  }
  .teleop h2 { color: var(--color-primary-light, #fbbf24); }
  .teleop-intro {
    border-left: 3px solid var(--color-primary, #f59e0b);
    padding-left: 1rem;
    margin: 0 0 2rem;
    font-size: 1rem;
    line-height: 1.75;
  }
  .story-list { list-style: none; margin: 0 0 2rem; padding: 0; display: flex; flex-direction: column; gap: 1.75rem; }
  .story-item { display: flex; gap: 1.25rem; align-items: flex-start; }
  .story-n {
    font-family: var(--font-mono, monospace);
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--color-primary, #f59e0b);
    min-width: 1.5rem;
    flex-shrink: 0;
    padding-top: 0.15rem;
  }
  .story-label {
    font-family: var(--font-mono, monospace);
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--color-text-muted, #94a3b8);
    margin-bottom: 0.3rem;
  }
  .story-body { font-size: 0.95rem; line-height: 1.7; margin: 0; }

  .lockout-block {
    border: 1px solid rgba(239,68,68,0.35);
    border-left: 3px solid #ef4444;
    background: rgba(239,68,68,0.04);
    padding: 1.25rem 1.5rem;
  }
  .lockout-label {
    font-family: var(--font-mono, monospace);
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ef4444;
    margin-bottom: 0.5rem;
  }
  .lockout-body { font-size: 0.93rem; line-height: 1.7; margin: 0; }
  .lockout-body strong { color: var(--color-primary-light, #fbbf24); }

  /* === SAMPLE === */
  .sample blockquote {
    margin: 1rem 0 0;
    padding: 1.5rem 1.5rem 1.5rem 2rem;
    border-left: 3px solid var(--color-primary, #f59e0b);
    background: var(--color-bg-secondary, #0f172a);
    font-style: italic;
    font-size: 1.05rem;
  }
  .sample blockquote p { color: var(--color-text-primary); }
  .sample blockquote footer { font-style: normal; font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.75rem; }
  .sample blockquote footer a { color: var(--color-primary, #f59e0b); text-decoration: none; border-bottom: 1px dashed currentColor; }
  .sample blockquote footer a:hover { color: var(--color-primary-light, #fbbf24); }

  /* === OPEN DRAFT === */
  .open-draft a { color: var(--color-primary, #f59e0b); text-decoration: none; border-bottom: 1px solid currentColor; }
  .open-draft a:hover { color: var(--color-primary-light, #fbbf24); }

  /* === FREE SAMPLE DL === */
  .sample-dl { text-align: center; border-color: rgba(245,158,11,0.2); }
  .sample-dl-inner { max-width: 540px; margin: 0 auto; }
  .sample-dl h2 { margin-top: 0; }
  .sample-dl p { color: var(--color-text-secondary); margin: 0 0 1.5rem; }
  .sample-dl .cta-primary { font-size: 1.05rem; padding: 0.85rem 1.75rem; }
  .sample-dl-meta { margin-top: 1rem !important; font-size: 0.86rem; color: var(--color-text-muted); font-family: var(--font-mono); }

  /* === NEWSLETTER === */
  .newsletter { text-align: center; }
  .newsletter h2, .newsletter p { text-align: center; }
  .newsletter p { max-width: 500px; margin: 0 auto 1.5rem; }

  /* === AUTHOR'S EDITION === */
  .authors-callout { padding: 2rem 1.5rem; }
  .authors-callout-inner {
    max-width: 760px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 1.5rem 1.75rem;
    position: relative;
    overflow: hidden;
  }
  .authors-callout-inner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #f59e0b, transparent);
  }
  @media (min-width: 600px) {
    .authors-callout-inner { flex-direction: row; align-items: center; gap: 1.5rem; }
  }
  .authors-callout-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.65rem;
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.3);
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #f59e0b;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .authors-callout-body { flex: 1; min-width: 0; }
  .authors-callout-headline { font-size: 0.97rem; font-weight: 700; color: #f1f5f9; margin: 0 0 0.3rem; line-height: 1.3; }
  .authors-callout-sub { font-size: 0.82rem; color: #64748b; margin: 0; line-height: 1.55; }
  .authors-callout-cta {
    font-size: 0.87rem;
    font-weight: 700;
    color: #f59e0b;
    text-decoration: none;
    white-space: nowrap;
    flex-shrink: 0;
    padding: 0.55rem 1.1rem;
    border: 1px solid rgba(245, 158, 11, 0.35);
    transition: background 0.15s ease, color 0.15s ease;
  }
  .authors-callout-cta:hover { background: rgba(245, 158, 11, 0.1); color: #fbbf24; }

  /* === RESPONSIVE === */
  @media (max-width: 960px) {
    .hero { gap: 2rem; grid-template-columns: minmax(0, 1fr) minmax(0, 1.6fr); }
    .hero-cover img { max-width: 260px; }
  }
  @media (max-width: 768px) {
    .hero { grid-template-columns: 1fr; gap: 1.75rem; text-align: center; margin: 1rem 0 3rem; }
    .hero-cover img { max-width: 240px; }
    .hero-ctas { justify-content: center; }
    .hero-preorder { text-align: left; }
    .thesis, .sample, .open-draft, .newsletter, .sample-dl, .roadmap, .teleop { padding: 1.5rem; }
    .stage.current { margin: 0 -1.5rem; padding: 0.875rem 1.5rem; }
  }
  @media (max-width: 480px) {
    .hero { gap: 1.25rem; margin: 0.5rem 0 2rem; }
    .hero-cover img { max-width: 200px; }
    .hero-ctas { flex-direction: column; align-items: stretch; }
    .cta-primary, .cta-secondary { text-align: center; }
    .thesis, .sample, .open-draft, .newsletter, .sample-dl, .roadmap, .teleop { padding: 1.25rem; }
    .stage.current { margin: 0 -1.25rem; padding: 0.875rem 1.25rem; }
  }
</style>
