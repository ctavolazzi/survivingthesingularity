<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import AuthorBio from '$lib/components/AuthorBio.svelte';

  // Set by LAUNCH.sh when the Gumroad product is ready. Empty = no buy button shown.
  const PURCHASE_URL = '';

  export let data;

  let visible = false;
  onMount(() => {
    visible = true;
    window.scrollTo({ top: 0, behavior: 'instant' });
  });
</script>

<svelte:head>
  <title>Surviving the Singularity. The Book.</title>
  <meta name="description" content="Surviving the Singularity by Christopher Tavolazzi. What is the Singularity, how humans react, and how to survive the transition. Open draft — read free or get early access." />
  <meta property="og:title" content="Surviving the Singularity. The Book." />
  <meta property="og:description" content="What is the Singularity. How humans react. How to survive the transition. Open draft by Christopher Tavolazzi." />
  <meta property="og:image" content="https://survivingthesingularity.com/images/surviving_the_singularity_cover_1200.png" />
  <meta property="og:url" content="https://survivingthesingularity.com/book" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="book-page">
{#if visible}

  <!-- ── HERO ── -->
  <section class="hero" in:fade={{ duration: 400 }}>
    <div class="hero-inner">

      <div class="cover-wrap">
        <picture>
          <source srcset="/images/optimized/surviving_the_singularity_cover_1200_original.webp" type="image/webp" />
          <img
            src="/images/surviving_the_singularity_cover_1200.png"
            alt="Surviving the Singularity book cover"
            class="cover-img"
            width="600"
            height="800"
          />
        </picture>
      </div>

      <div class="hero-copy">
        <p class="eyebrow">Open Draft · v0.2 · Reader Edition</p>
        <h1 class="book-title">Surviving the<br>Singularity</h1>
        <p class="byline">By Christopher Tavolazzi</p>
        <p class="hook">Intelligence now has a marginal cost of zero. The old systems haven't caught up yet. This book is about what to do in the gap — before the window closes.</p>

        <div class="hero-ctas">
          {#if PURCHASE_URL}
            <a href={PURCHASE_URL} class="btn-primary" target="_blank" rel="noopener noreferrer">Buy the Book</a>
          {:else}
            <a href="/early-access" class="btn-primary">Reserve Early Access</a>
          {/if}
          <a href="/StS-free-sample.pdf" class="btn-ghost" target="_blank" rel="noopener noreferrer">Read a free sample</a>
        </div>

        <p class="disclaimer-note">
          For informational purposes only. Not financial, legal, or professional advice.
          <a href="/disclaimer">Full disclaimer.</a>
        </p>
      </div>

    </div>
  </section>

  <!-- ── WHAT'S INSIDE ── -->
  <section class="section">
    <div class="inner">
      <p class="label">What's Inside</p>
      <h2 class="heading">Three parts. Everything you need to navigate what's coming.</h2>

      <div class="parts-grid">

        <div class="part part-1">
          <span class="part-num">Part I</span>
          <h3 class="part-title">What is the Singularity?</h3>
          <ul class="part-list">
            <li>Why the 2017 Transformer architecture crossed the event horizon</li>
            <li>Nine stages from narrow AI to AGI — and where we are right now</li>
            <li>The thermodynamic limits that shape everything in Parts II and III</li>
            <li>Why zero-cost intelligence changes the economics of survival</li>
          </ul>
        </div>

        <div class="part part-2">
          <span class="part-num">Part II</span>
          <h3 class="part-title">How Humans React</h3>
          <ul class="part-list">
            <li>The predictable behavioral patterns when disruption hits</li>
            <li>Why fear-based thinking makes the transition harder</li>
            <li>How to shift from reaction to observer status — and why it matters</li>
            <li>Why cooperation is the optimal strategy, not an ideology</li>
          </ul>
        </div>

        <div class="part part-3">
          <span class="part-num">Part III</span>
          <h3 class="part-title">How to Survive the Transition</h3>
          <ul class="part-list">
            <li>Local energy and food infrastructure — built before you need it</li>
            <li>The Shouse Grid: community-managed microgrids and local compute</li>
            <li>The new social contract: food, shelter, and care as engineering targets</li>
            <li>The 2027 tipping point and what to do on either side of it</li>
          </ul>
        </div>

      </div>
    </div>
  </section>

  <!-- ── THE TWO EDITIONS ── -->
  <section class="section section-alt">
    <div class="inner">
      <p class="label">Choose Your Edition</p>
      <h2 class="heading">Two ways to own this book.</h2>
      <p class="subhead">The Standard Edition ships worldwide through Amazon. The Author's Limited Edition is 100 hand-bound, signed, and numbered copies — and no two of them are alike.</p>

      <div class="editions">

        <!-- Standard Edition -->
        <div class="edition edition-standard">
          <p class="ed-badge">Standard Edition</p>
          <h3 class="ed-title">Surviving the Singularity</h3>
          <p class="ed-sub">The complete book, in paperback and on Kindle. Published on Amazon via Kindle Direct Publishing.</p>

          <ul class="ed-list">
            <li>Full three-part book, all chapters</li>
            <li>Paperback and Kindle editions</li>
            <li>Available worldwide on Amazon via KDP</li>
            <li>Print-on-demand — never sold out, never out of stock</li>
            <li>Price announced at launch · August 2026</li>
          </ul>

          <a href="https://thecoffeejesus.substack.com" class="btn-ghost" target="_blank" rel="noopener noreferrer">Get notified at launch</a>
        </div>

        <!-- Author's Limited Edition -->
        <div class="edition edition-authors">
          <p class="ed-badge ed-badge-special">
            <svg width="10" height="10" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 1l1.88 3.82L14 5.64l-3 2.93.71 4.12L8 10.77l-3.71 1.92L5 8.57 2 5.64l4.12-.82L8 1z"/></svg>
            Author's Limited Edition · 100 Copies Only
          </p>
          <h3 class="ed-title">One of one hundred.<br>One of a kind.</h3>
          <p class="ed-sub">100 numbered copies, and no two are the same. Every single one is hand-bound and signed by the author.</p>

          <ul class="ed-list ed-list-special">
            <li>Everything in the Standard Edition</li>
            <li>All 100 copies are different — each one is a unique, physical, one-of-a-kind object</li>
            <li>Hand-bound by Christopher Tavolazzi, one copy at a time</li>
            <li>Signed and numbered by hand — you own a specific number, 1 through 100, that exists nowhere else</li>
            <li>Exclusive content and margin notes in the author's hand, different in every copy</li>
            <li>$5 secures your number now · ships at launch, August 2026</li>
          </ul>

          <div class="ed-scarcity">
            <span class="ed-scarcity-num">100</span>
            <span class="ed-scarcity-text">copies will ever exist · when they're gone, they're gone</span>
          </div>

          <a href="/early-access?edition=authors" class="btn-primary">Claim your number</a>
        </div>

      </div>

      <p class="ed-footnote">Why is every copy different? Because they're made by hand, one at a time — the binding, the materials, and the handwritten notes vary from copy to copy. Mass production makes identical objects. Hands don't.</p>
    </div>
  </section>

  <!-- ── FREE SAMPLE ── -->
  <section class="section section-center">
    <div class="inner inner-narrow">
      <p class="label">Not sure yet?</p>
      <h2 class="heading">Read the first chapter free.</h2>
      <p class="subhead">Introduction plus Chapter 1. No signup. No email. About 10 minutes.</p>
      <a href="/StS-free-sample.pdf" class="btn-primary" target="_blank" rel="noopener noreferrer">Download the free sample</a>
      <p class="fine-print">PDF · No paywall · No strings</p>
    </div>
  </section>

  <!-- ── AUTHOR ── -->
  <section class="section section-alt">
    <div class="inner">
      <AuthorBio />
    </div>
  </section>

  <!-- ── SUBSCRIBE ── -->
  <section class="section section-center">
    <div class="inner inner-narrow">
      <p class="label">Stay in the loop</p>
      <h2 class="heading">Get the next chapter when it ships.</h2>
      <p class="subhead">Published on Substack. Subscribe once, get everything. Free tier covers all chapters and launch alerts.</p>
      <a href="https://thecoffeejesus.substack.com" class="btn-primary" target="_blank" rel="noopener noreferrer">Subscribe on Substack</a>
    </div>
  </section>

{/if}
</div>

<style>
  /* ── TOKENS ── */
  .book-page {
    font-family: 'Outfit', system-ui, sans-serif;
    --amber:      #f59e0b;
    --amber-dim:  rgba(245,158,11,0.08);
    --amber-glow: rgba(245,158,11,0.28);
    --surface:    #0f172a;
    --border:     rgba(255,255,255,0.07);
    --border-mid: rgba(255,255,255,0.11);
    --text-1:     #f8fafc;
    --text-2:     #cbd5e1;
    --text-3:     #64748b;
    --mono:       'JetBrains Mono', monospace;
    --ease-spring: cubic-bezier(0.34,1.56,0.64,1);
  }

  /* ── LAYOUT PRIMITIVES ── */
  .section {
    padding: clamp(48px, 8vw, 88px) clamp(20px, 5vw, 48px);
    border-top: 1px solid var(--border);
  }
  .section-alt {
    background: rgba(15,23,42,0.4);
  }
  .section-center {
    text-align: center;
  }
  .inner {
    max-width: 860px;
    margin: 0 auto;
  }
  .inner-narrow {
    max-width: 560px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  /* ── TYPE SCALE ── */
  .label {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--amber);
    margin: 0 0 0.6rem;
    display: block;
  }
  .heading {
    font-size: clamp(1.6rem, 4.5vw, 2.4rem);
    font-weight: 900;
    color: var(--text-1);
    margin: 0 0 0.6rem;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }
  .subhead {
    font-size: clamp(0.95rem, 2.2vw, 1.05rem);
    color: var(--text-2);
    line-height: 1.65;
    margin: 0 0 2rem;
    max-width: 56ch;
  }
  .section-center .subhead {
    margin-left: auto;
    margin-right: auto;
  }
  .eyebrow {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--text-3);
    margin: 0 0 0.6rem;
  }
  .fine-print {
    font-size: 0.78rem;
    color: var(--text-3);
    margin: 0.25rem 0 0;
  }

  /* ── BUTTONS ── */
  .btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.85rem 1.75rem;
    background: var(--amber);
    color: #0f172a;
    font-weight: 800;
    font-size: 0.95rem;
    text-decoration: none;
    border: none;
    border-radius: 999px;
    box-shadow: 0 4px 20px var(--amber-glow);
    transition: filter 0.2s ease, transform 0.2s var(--ease-spring), box-shadow 0.2s ease;
    white-space: nowrap;
    font-family: inherit;
    cursor: pointer;
  }
  .btn-primary:hover { filter: brightness(1.08); transform: translateY(-2px); box-shadow: 0 8px 28px rgba(245,158,11,0.42); }
  .btn-primary:active { transform: scale(0.97); }

  .btn-ghost {
    display: inline-flex;
    align-items: center;
    padding: 0.85rem 1.75rem;
    background: transparent;
    color: var(--text-2);
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;
    border: 1px solid var(--border-mid);
    border-radius: 999px;
    transition: color 0.2s ease, border-color 0.2s ease, background 0.2s ease;
    white-space: nowrap;
    font-family: inherit;
    cursor: pointer;
  }
  .btn-ghost:hover { color: var(--text-1); border-color: rgba(255,255,255,0.18); background: rgba(255,255,255,0.04); }

  /* ── HERO ── */
  .hero {
    padding: clamp(40px, 6vw, 80px) clamp(20px, 5vw, 48px) clamp(48px, 7vw, 80px);
    background: linear-gradient(160deg, rgba(245,158,11,0.06) 0%, transparent 55%);
  }
  .hero-inner {
    max-width: 960px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: clamp(28px, 5vw, 64px);
    align-items: center;
  }
  @media (max-width: 640px) {
    .hero-inner {
      grid-template-columns: 1fr;
    }
    .cover-wrap {
      display: flex;
      justify-content: center;
    }
  }
  .cover-img {
    width: 100%;
    max-width: 220px;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 28px 60px rgba(0,0,0,0.65), 0 0 0 1px rgba(245,158,11,0.1);
  }
  .hero-copy {
    display: flex;
    flex-direction: column;
    gap: 0;
  }
  .book-title {
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 900;
    color: var(--text-1);
    margin: 0 0 0.3rem;
    letter-spacing: -0.035em;
    line-height: 1.05;
  }
  .byline {
    font-size: 0.9rem;
    color: var(--text-3);
    margin: 0 0 1.2rem;
    font-family: var(--mono);
  }
  .hook {
    font-size: clamp(0.95rem, 2.2vw, 1.1rem);
    color: var(--text-2);
    line-height: 1.65;
    margin: 0 0 1.6rem;
    max-width: 52ch;
  }
  .hero-ctas {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
  }
  .disclaimer-note {
    font-size: 0.78rem;
    color: var(--text-3);
    margin: 0;
    line-height: 1.5;
  }
  .disclaimer-note a {
    color: var(--text-2);
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .disclaimer-note a:hover { color: var(--amber); }

  /* ── PARTS GRID ── */
  .parts-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 2rem;
  }
  @media (max-width: 680px) {
    .parts-grid { grid-template-columns: 1fr; }
  }
  .part {
    padding: 1.4rem;
    border: 1px solid var(--border);
    border-top: 3px solid var(--border-mid);
    border-radius: 14px;
  }
  .part-1 { border-top-color: var(--amber); }
  .part-2 { border-top-color: #3b82f6; }
  .part-3 { border-top-color: #10b981; }
  .part-num {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--text-3);
    display: block;
    margin-bottom: 0.4rem;
  }
  .part-title {
    font-size: 0.98rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 0 0 0.75rem;
    line-height: 1.25;
  }
  .part-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
  }
  .part-list li {
    font-size: 0.85rem;
    color: var(--text-2);
    line-height: 1.5;
    padding-left: 1.1rem;
    position: relative;
  }
  .part-list li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.55em;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--text-3);
  }
  .part-1 .part-list li::before { background: var(--amber); }
  .part-2 .part-list li::before { background: #60a5fa; }
  .part-3 .part-list li::before { background: #34d399; }

  /* ── EDITIONS ── */
  .editions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
    margin-top: 2rem;
    align-items: start;
  }
  @media (max-width: 660px) {
    .editions { grid-template-columns: 1fr; }
  }

  .edition {
    padding: 1.75rem;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .edition-standard {
    background: rgba(15,23,42,0.6);
    border: 1px solid var(--border-mid);
  }
  .edition-authors {
    background: rgba(245,158,11,0.04);
    border: 1px solid rgba(245,158,11,0.28);
    box-shadow: 0 0 48px rgba(245,158,11,0.06);
  }

  .ed-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--text-3);
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.3rem 0.7rem;
    margin: 0;
    width: fit-content;
  }
  .ed-badge-special {
    color: var(--amber);
    background: rgba(245,158,11,0.08);
    border-color: rgba(245,158,11,0.25);
  }

  .ed-title {
    font-size: clamp(1.1rem, 2.8vw, 1.35rem);
    font-weight: 900;
    color: var(--text-1);
    margin: 0;
    letter-spacing: -0.02em;
    line-height: 1.2;
  }
  .ed-sub {
    font-size: 0.9rem;
    color: var(--text-2);
    line-height: 1.6;
    margin: 0;
  }

  .ed-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
  }
  .ed-list li {
    font-size: 0.88rem;
    color: var(--text-2);
    line-height: 1.5;
    padding-left: 1.2rem;
    position: relative;
  }
  .ed-list li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.55em;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--text-3);
  }
  .ed-list-special li::before {
    background: var(--amber);
  }

  .ed-scarcity {
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    padding: 0.85rem 1rem;
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.18);
    border-radius: 10px;
  }
  .ed-scarcity-num {
    font-family: var(--mono);
    font-size: 1.5rem;
    font-weight: 900;
    color: var(--amber);
    line-height: 1;
    flex-shrink: 0;
  }
  .ed-scarcity-text {
    font-size: 0.82rem;
    color: var(--text-2);
    line-height: 1.45;
  }

  .ed-footnote {
    font-size: 0.85rem;
    color: var(--text-3);
    line-height: 1.6;
    margin: 1.5rem 0 0;
    max-width: 62ch;
  }
</style>
