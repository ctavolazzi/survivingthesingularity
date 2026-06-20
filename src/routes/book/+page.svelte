<script>
  import { fade, fly } from 'svelte/transition';
  import TableOfContents from '$lib/components/TableOfContents.svelte';
  import AuthorBio from '$lib/components/AuthorBio.svelte';
  import ChapterPreviewCard from '$lib/components/ChapterPreviewCard.svelte';
  import coverImage from '$lib/images/Surviving-the-Singularity-Cover.png?url';
  import { chaptersWithMeta } from '$lib/bookContent.js';

  export let data;

  // Set to the Gumroad URL on launch day — the Buy CTA below renders
  // automatically when this is non-empty. Empty string = no change to site.
  const PURCHASE_URL = '';

  const pillars = [
    {
      icon: '🧭',
      title: 'Understand',
      desc: 'What the Singularity actually is, why it’s arriving faster than anyone tells you, and what it means for the way you get your needs met.'
    },
    {
      icon: '🔍',
      title: 'Navigate',
      desc: 'How AI is rewiring jobs, healthcare, education, art, relationships, politics, and money - right now, not in 2050.'
    },
    {
      icon: '🛠️',
      title: 'Thrive',
      desc: 'Practical patterns for staying agentic in a world where the tools are starting to act on their own.'
    }
  ];
</script>

<svelte:head>
  <title>Surviving the Singularity - The Book</title>
  <meta name="description" content="Surviving the Singularity by Christopher Tavolazzi. An open-draft field manual for the people who refuse to be passive cargo when AI rewrites the world." />
  <meta property="og:title" content="Surviving the Singularity - The Book" />
  <meta property="og:description" content="An open-draft field manual for the people who refuse to be passive cargo when AI rewrites the world." />
  <meta property="og:image" content="/Surviving-the-Singularity-Cover.png" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="not-prose book-page">

  <!-- HERO -->
  <section class="hero" in:fade={{ duration: 600 }}>
    <div class="hero-cover">
      <img src={coverImage} alt="Surviving the Singularity book cover" loading="eager" />
      <div class="hero-cover-glow" aria-hidden="true"></div>
    </div>
    <div class="hero-text">
      <div class="hero-eyebrow">Open Draft · v0.1 · Reader Edition</div>
      <h1>Surviving the Singularity</h1>
      <p class="hero-subtitle">
        A field manual for the people who refuse to be passive cargo when AI rewrites the world.
      </p>
      <p class="hero-byline">By <strong>Christopher Tavolazzi</strong> &middot; <span class="mono">a.k.a. The Coffee Jesus</span></p>
      <div class="hero-ctas">
        <a class="cta-primary" href="#chapter-previews">Read free chapters &rarr;</a>
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
      <!-- Substack funnel stays as secondary path once PURCHASE_URL is live. -->
      <div class="hero-preorder">
        <div class="preorder-label">Updates are posted to Substack when posted at all.</div>
        <a class="cta-primary subscribe-cta" href="https://thecoffeejesus.substack.com" target="_blank" rel="noopener noreferrer">
          Subscribe on Substack →
        </a>
        <p class="preorder-meta">Substack subscription. No content frequency, ship date, or completion guarantee. Subject to Substack's own terms.</p>
      </div>
    </div>
  </section>

  <!-- THESIS -->
  <section class="thesis" in:fly={{ y: 20, duration: 600, delay: 200 }}>
    <div class="eyebrow">The Thesis</div>
    <h2>The shovel is digging its own hole.</h2>
    <p>
      The Singularity isn’t a future event. It’s a current condition.
      Tools are leaping from <em>reacting to our input</em> to <em>acting on their own</em>,
      and the pace is doubling on a curve nobody is steering.
    </p>
    <p>
      This book is a primer on the double-exponential shift in <strong>how we get our needs met</strong>.
      Work, food, health, money, relationships, governance - all of it is being renegotiated
      in real time by systems that don’t need your permission to participate.
    </p>
    <p class="thesis-kicker">
      You don’t need to stop the wave. You need to learn to surf it.
    </p>
  </section>

  <!-- 3 PILLARS -->
  <section class="pillars" in:fly={{ y: 20, duration: 600, delay: 300 }}>
    <div class="eyebrow">What You’ll Get</div>
    <h2>Three things, in order.</h2>
    <div class="pillar-grid">
      {#each pillars as p}
        <div class="pillar">
          <div class="pillar-icon">{p.icon}</div>
          <h3>{p.title}</h3>
          <p>{p.desc}</p>
        </div>
      {/each}
    </div>
  </section>

  <!-- AUTHOR BIO -->
  <div in:fly={{ y: 20, duration: 600, delay: 350 }}>
    <AuthorBio />
  </div>

  <!-- SAMPLE EXCERPT -->
  <section class="sample" in:fly={{ y: 20, duration: 600, delay: 400 }}>
    <div class="eyebrow">A Sample</div>
    <blockquote>
      <p>
        “So the robots have taken over. Congratulations - you’ve lost.
        Surviving the Singularity isn’t just about fending off Terminator bots or finding
        food in the era of economic collapse and climate famines. It’s about staying hidden
        from autonomous drone swarms and filtering nanobots out of the water.
      </p>
      <p>
        Ah, who am I kidding? You don’t need to worry about the nanobots.
        You’re just a disembodied brain in a jar.
        Every sensation you’ve ever had, every person you’ve ever known
        is a hallucination produced by neural-link electrodes.”
      </p>
      <footer>&mdash; from the <a href="/book/introduction">Introduction</a></footer>
    </blockquote>
  </section>

  <!-- OPEN DRAFT - reframed disclaimer -->
  <section class="open-draft" in:fly={{ y: 20, duration: 600, delay: 450 }}>
    <div class="eyebrow">How This Book Works</div>
    <h2>Built in public. Revised by readers.</h2>
    <p>
      This is the <strong>open draft</strong> of <em>Surviving the Singularity</em>.
      Chapters land as they’re written. Typos, edges, and works-in-progress are part of the deal -
      and so is your input. Spot a glitch in the matrix? A passage that lands wrong?
      A topic you want covered? <a href="/about">Reach out</a> and it goes into the next revision.
    </p>
    <p class="text-muted">
      Final print/e-book editions will be released on Amazon. Open-draft readers get early access, signed credit, and first crack at the launch.
    </p>
  </section>

  <!-- FREE SAMPLE DOWNLOAD -->
  <section class="sample-dl" in:fly={{ y: 20, duration: 600, delay: 470 }}>
    <div class="sample-dl-inner">
      <div class="eyebrow">Try Before You Commit</div>
      <h2>Free PDF Sample</h2>
      <p>Introduction + Chapter 1. No email, no signup. Just open it and read.</p>
      <a class="cta-primary" href="/StS-free-sample.pdf" download>📥 Download (PDF)</a>
      <p class="sample-dl-meta">~10-min read · plain PDF · sharable</p>
    </div>
  </section>

  <!-- CHAPTER PREVIEW GRID - replaces the old plain TOC link list -->
  <section id="chapter-previews" class="chapter-previews" in:fly={{ y: 20, duration: 600, delay: 500 }}>
    <div class="eyebrow">Read Now</div>
    <h2>Chapters</h2>
    <p class="chapter-previews-lede">
      All chapters are free. Pick one that calls you.
    </p>
    <div class="chapter-grid">
      {#each chaptersWithMeta as section, i}
        <ChapterPreviewCard {section} index={i} />
      {/each}
    </div>
  </section>

  <!-- FULL TABLE OF CONTENTS - kept for completeness (front + back matter) -->
  <section id="table-of-contents" class="toc" in:fly={{ y: 20, duration: 600, delay: 520 }}>
    <div class="eyebrow">Full Contents</div>
    <h2>Everything in the book</h2>
    <p class="toc-lede">Including front matter, epilogue, glossary, and further reading.</p>
    <div class="toc-wrap">
      <TableOfContents sections={data.book.sections} />
    </div>
  </section>

  <!-- SUBSCRIBE - single funnel into Substack. No competing forms. -->
  <section id="stay-in-loop" class="newsletter" in:fly={{ y: 20, duration: 600, delay: 550 }}>
    <div class="eyebrow">Stay In The Loop</div>
    <h2>Get the next chapter in your inbox.</h2>
    <p>I publish chapters, essays, and project updates on Substack. Subscribe once, get everything.</p>
    <a class="cta-primary subscribe-cta-large" href="https://thecoffeejesus.substack.com" target="_blank" rel="noopener noreferrer">
      📬 Subscribe on Substack →
    </a>
    <p class="subscribe-meta">Free tier covers chapters + launch alerts. Founding-tier readers get bonus drops + name in book acknowledgements.</p>
  </section>

</div>

<style>
  /* === SCOPED TO BOOK PAGE - uses theme tokens from theme.css === */

  .book-page {
    color: var(--color-text-primary, #f1f5f9);
    font-family: var(--font-primary, 'Inter', sans-serif);
    max-width: 1100px;
    margin: 0 auto;
  }

  /* Shared section eyebrow */
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
  .text-muted { color: var(--color-text-muted, #dde4ef); font-size: 0.9rem; }

  /* === HERO === */
  .hero {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr);
    gap: 3rem;
    align-items: center;
    margin: 2rem 0 5rem;
  }
  .hero-cover { position: relative; }
  .hero-cover img {
    width: 100%;
    max-width: 320px;
    height: auto;
    border-radius: var(--radius-md, 12px);
    box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.7), 0 0 0 1px var(--color-border, rgba(148,163,184,0.1));
    position: relative;
    z-index: 1;
    display: block;
    margin: 0 auto;
  }
  .hero-cover-glow {
    position: absolute;
    inset: 10% 5%;
    background: radial-gradient(circle, var(--color-primary, #f59e0b) 0%, transparent 70%);
    filter: blur(40px);
    opacity: 0.35;
    z-index: 0;
    pointer-events: none;
  }
  .hero h1 {
    font-size: clamp(2.25rem, 5vw, 3.75rem);
    font-weight: 800;
    color: var(--color-text-primary, #f1f5f9);
    background: linear-gradient(135deg, var(--color-text-primary) 0%, var(--color-primary) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  @supports not (-webkit-background-clip: text) {
    .hero h1 {
      background: none;
      color: var(--color-text-primary, #f1f5f9);
    }
  }
  .hero-subtitle {
    font-size: 1.2rem;
    color: var(--color-text-primary);
    margin: 1rem 0;
  }
  .hero-byline { font-size: 0.95rem; }
  .hero-ctas { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.75rem; }
  .cta-primary, .cta-secondary {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-sm, 6px);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    transition: transform 150ms ease, background-color 150ms ease, color 150ms ease;
  }
  .cta-primary {
    background: var(--color-primary, #f59e0b);
    color: #1a0f00;
  }
  .cta-primary:hover { background: var(--color-primary-light, #fbbf24); transform: translateY(-1px); }
  .cta-secondary {
    background: transparent;
    color: var(--color-text-primary);
    border: 1px solid var(--color-border-hover, rgba(148,163,184,0.2));
  }
  .cta-secondary:hover { background: var(--color-surface, rgba(30,41,59,0.5)); }

  /* === SECTION CARDS === */
  .thesis, .pillars, .sample, .open-draft, .toc, .newsletter,
  .sample-dl, .chapter-previews {
    background: var(--color-surface, rgba(30,41,59,0.5));
    border: 1px solid var(--color-border, rgba(148,163,184,0.1));
    border-radius: var(--radius-lg, 16px);
    padding: 2.5rem;
    margin-bottom: 2rem;
  }
  .thesis h2, .pillars h2, .open-draft h2, .toc h2, .newsletter h2,
  .sample-dl h2, .chapter-previews h2 {
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 700;
  }

  /* === HERO PREORDER (under primary CTAs) === */
  .hero-preorder {
    margin-top: 1.75rem;
    padding-top: 1.5rem;
    border-top: 1px dashed var(--color-border, rgba(148,163,184,0.15));
  }
  .preorder-label {
    font-size: 0.85rem;
    color: var(--color-text-muted, #dde4ef);
    margin-bottom: 0.65rem;
    font-family: var(--font-mono, var(--font-primary));
  }
  .preorder-meta {
    margin-top: 0.65rem !important;
    font-size: 0.86rem;
    color: var(--color-text-muted, #dde4ef);
    font-family: var(--font-mono, var(--font-primary));
  }
  .subscribe-cta { display: inline-block; }
  .subscribe-cta-large {
    display: inline-block;
    font-size: 1.05rem;
    padding: 0.85rem 1.75rem;
    margin-top: 0.5rem;
  }
  .subscribe-meta {
    margin-top: 1rem !important;
    font-size: 0.82rem;
    color: var(--color-text-muted, #dde4ef);
    max-width: 520px;
    margin-left: auto !important;
    margin-right: auto !important;
  }

  /* === FREE SAMPLE DOWNLOAD === */
  .sample-dl {
    text-align: center;
    background: linear-gradient(135deg, rgba(30,41,59,0.6), rgba(245,158,11,0.06));
    border-color: rgba(245,158,11,0.25);
  }
  .sample-dl-inner { max-width: 540px; margin: 0 auto; }
  .sample-dl h2 { margin-top: 0; }
  .sample-dl p { color: var(--color-text-secondary, #dde4ef); margin: 0 0 1.5rem; }
  .sample-dl .cta-primary { font-size: 1.05rem; padding: 0.85rem 1.75rem; }
  .sample-dl-meta {
    margin-top: 1rem !important;
    font-size: 0.86rem;
    color: var(--color-text-muted, #dde4ef);
    font-family: var(--font-mono, var(--font-primary));
  }

  /* === CHAPTER PREVIEWS === */
  .chapter-previews-lede {
    color: var(--color-text-secondary, #dde4ef);
    margin: 0 0 1.5rem;
  }
  .chapter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
  }

  /* === FULL TOC === */
  .toc-lede {
    color: var(--color-text-muted, #dde4ef);
    margin: 0 0 1.5rem;
    font-size: 0.92rem;
  }
  .thesis-kicker {
    font-size: 1.15rem;
    color: var(--color-primary, #f59e0b);
    font-weight: 600;
    margin-top: 1.5rem;
  }

  /* === PILLARS === */
  .pillar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    margin-top: 1.5rem;
  }
  .pillar {
    background: var(--color-bg-secondary, #0f172a);
    border: 1px solid var(--color-border, rgba(148,163,184,0.1));
    border-radius: var(--radius-md, 12px);
    padding: 1.5rem;
    transition: border-color 200ms ease, transform 200ms ease;
  }
  .pillar:hover { border-color: var(--color-primary, #f59e0b); transform: translateY(-2px); }
  .pillar-icon { font-size: 1.75rem; margin-bottom: 0.5rem; }
  .pillar h3 {
    font-size: 1.1rem;
    color: var(--color-primary, #f59e0b);
    margin-bottom: 0.5rem;
  }
  .pillar p { font-size: 0.9rem; margin: 0; }

  /* === SAMPLE === */
  .sample blockquote {
    margin: 1rem 0 0;
    padding: 1.5rem 1.5rem 1.5rem 2rem;
    border-left: 3px solid var(--color-primary, #f59e0b);
    background: var(--color-bg-secondary, #0f172a);
    border-radius: 0 var(--radius-md, 12px) var(--radius-md, 12px) 0;
    font-style: italic;
    font-size: 1.05rem;
  }
  .sample blockquote p { color: var(--color-text-primary); }
  .sample blockquote footer {
    font-style: normal;
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin-top: 0.75rem;
  }
  .sample blockquote footer a {
    color: var(--color-primary, #f59e0b);
    text-decoration: none;
    border-bottom: 1px dashed currentColor;
  }
  .sample blockquote footer a:hover { color: var(--color-primary-light, #fbbf24); }

  /* === OPEN DRAFT === */
  .open-draft a {
    color: var(--color-primary, #f59e0b);
    text-decoration: none;
    border-bottom: 1px solid currentColor;
  }
  .open-draft a:hover { color: var(--color-primary-light, #fbbf24); }

  /* === TOC === */
  .toc-wrap { margin-top: 1.5rem; }

  /* === NEWSLETTER === */
  .newsletter { text-align: center; }
  .newsletter h2 { text-align: center; }
  .newsletter p { text-align: center; max-width: 500px; margin: 0 auto 1.5rem; }

  /* === RESPONSIVE === */

  /* Tablet landscape / small desktop */
  @media (max-width: 960px) {
    .hero {
      gap: 2rem;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1.6fr);
    }
    .hero-cover img { max-width: 260px; }
  }

  /* Mobile */
  @media (max-width: 768px) {
    .hero {
      grid-template-columns: 1fr;
      gap: 1.75rem;
      text-align: center;
      margin: 1rem 0 3rem;
    }
    .hero-cover img { max-width: 240px; }
    .hero-ctas { justify-content: center; }
    .hero-preorder { text-align: left; }
    .thesis, .pillars, .sample, .open-draft, .toc, .newsletter,
    .sample-dl, .chapter-previews {
      padding: 1.5rem;
    }
  }

  /* Small phones */
  @media (max-width: 480px) {
    .hero {
      gap: 1.25rem;
      margin: 0.5rem 0 2rem;
    }
    .hero-cover img { max-width: 200px; }
    .hero-ctas {
      flex-direction: column;
      align-items: stretch;
    }
    .cta-primary, .cta-secondary { text-align: center; }
    .thesis, .pillars, .sample, .open-draft, .toc, .newsletter,
    .sample-dl, .chapter-previews {
      padding: 1.25rem;
    }
    .chapter-grid {
      grid-template-columns: 1fr;
    }
    .pillar-grid {
      grid-template-columns: 1fr;
    }
  }

  /* === REDUCED MOTION === */
  @media (prefers-reduced-motion: reduce) {
    .pillar:hover, .cta-primary:hover { transform: none; }
  }
</style>
