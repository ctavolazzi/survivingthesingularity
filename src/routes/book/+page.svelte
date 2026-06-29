<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import AuthorBio from '$lib/components/AuthorBio.svelte';
  import { bookParts, mathematicalMap } from '$lib/data/stages.js';

  export let data;

  let visible = false;
  onMount(() => {
    visible = true;
    window.scrollTo({ top: 0, behavior: 'instant' });
  });
</script>

<svelte:head>
  <title>Surviving the Singularity. The Book.</title>
  <meta name="description" content="Surviving the Singularity by Christopher Tavolazzi. Three parts: What is the Singularity, How Humans React, How to Survive the Transition. Open draft. Read free." />
  <meta property="og:title" content="Surviving the Singularity. The Book." />
  <meta property="og:description" content="What is the Singularity. How humans react. How to survive the transition. Open draft by Christopher Tavolazzi." />
  <meta property="og:image" content="/images/surviving_the_singularity_cover_1200.png" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="book-page">

  {#if visible}

  <!-- ── HERO ── -->
  <section class="bk-hero" in:fade={{ duration: 500 }}>
    <div class="bk-hero-inner">
      <div class="bk-cover-col">
        <img
          src="/images/surviving_the_singularity_cover_1200.png"
          alt="Surviving the Singularity book cover"
          class="bk-cover"
          width="600"
          height="800"
        />
      </div>
      <div class="bk-hero-copy">
        <p class="bk-eyebrow">Open Draft · v0.1 · Reader Edition</p>
        <h1 class="bk-title">Surviving the Singularity</h1>
        <p class="bk-byline">By Christopher Tavolazzi</p>
        <p class="bk-hook">The singularity is not a future event. It is an active, structural condition. Intelligence now has a marginal cost of zero. The old systems haven't caught up yet. This book is about what to do in the gap.</p>
        <div class="bk-hero-actions">
          <a href="/StS-free-sample.pdf" class="bk-btn-primary" target="_blank" rel="noopener noreferrer">
            Download free sample (PDF)
          </a>
          <a href="/early-access" class="bk-btn-secondary">Get Early Access. $5.</a>
        </div>
        <p class="bk-hero-note">No content frequency, ship date, or completion guarantee. Read it as it gets built.</p>
      </div>
    </div>
  </section>

  <!-- ── INTRODUCTION: THE EVENT HORIZON ── -->
  <section class="bk-section">
    <div class="bk-section-inner">
      <p class="bk-label">Introduction</p>
      <h2 class="bk-section-heading">The Event Horizon</h2>

      <div class="bk-intro-blocks">
        <div class="bk-intro-block">
          <div class="bk-intro-num">01</div>
          <div class="bk-intro-body">
            <p class="bk-intro-title">The Premise</p>
            <p class="bk-intro-text">The singularity is an active, structural reality. The 2017 Transformer architecture crossed the event horizon by introducing parallel self-attention: a mechanism that allows a model to process its own architecture. This made recursive self-improvement not just possible but inevitable given sufficient compute.</p>
          </div>
        </div>
        <div class="bk-intro-block">
          <div class="bk-intro-num">02</div>
          <div class="bk-intro-body">
            <p class="bk-intro-title">The Core Conflict</p>
            <p class="bk-intro-text">Intelligence is now a resource with a marginal cost of zero. Current systems meter this resource anyway, creating artificial scarcity. The conflict between zero-cost intelligence and metered access is the defining economic tension of the next decade.</p>
          </div>
        </div>
        <div class="bk-intro-block">
          <div class="bk-intro-num">03</div>
          <div class="bk-intro-body">
            <p class="bk-intro-title">The Ultimatum</p>
            <p class="bk-intro-text">We must secure local survival and establish a new social contract to align our infrastructure with the reality of this transition. Not as an ideological position. As an engineering problem.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ── THREE PARTS ── -->
  <section class="bk-section bk-section-alt">
    <div class="bk-section-inner">
      <p class="bk-label">The Book</p>
      <h2 class="bk-section-heading">Three parts. The complete picture.</h2>

      <div class="bk-parts">
        {#each bookParts as part, i}
          <div class="bk-part bk-part-{i + 1}">
            <span class="bk-part-num">{part.num}</span>
            <h3 class="bk-part-title">{part.title}</h3>
            <p class="bk-part-sub">{part.subtitle}</p>
            <p class="bk-part-desc">{part.desc}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ── PART I: MATHEMATICAL MAP ── -->
  <section class="bk-section">
    <div class="bk-section-inner">
      <p class="bk-label">Part I. The Mathematical Map</p>
      <h2 class="bk-section-heading">Nine stages. A predictable sequence.</h2>
      <p class="bk-section-sub">AI is moving through stages. Here is the map: where we have been, where we are, and where it goes from here. Stage 04 is where we are now.</p>

      <div class="bk-map">
        {#each mathematicalMap as group}
          <div class="bk-era">
            <div class="bk-era-header">
              <span class="bk-era-label">{group.era}</span>
              <span class="bk-era-nums">{group.eraNum}</span>
            </div>
            <div class="bk-stages">
              {#each group.stages as stage}
                <div class="bk-stage" class:bk-stage-current={stage.current}>
                  <span class="bk-stage-n">{stage.num}</span>
                  <span class="bk-stage-t">{stage.title}</span>
                  {#if stage.current}
                    <span class="bk-stage-pill">we are here</span>
                  {/if}
                </div>
              {/each}
            </div>
          </div>
        {/each}
      </div>

      <div class="bk-thermo">
        <p class="bk-thermo-label">The Thermodynamic Reality</p>
        <p class="bk-thermo-text">The machine is a massive heat engine bound by physical limits. It requires either high-grade energy or the reduction of energy costs to maintain AGI. This constraint shapes everything in Part III.</p>
      </div>
    </div>
  </section>

  <!-- ── PART II ── -->
  <section class="bk-section bk-section-alt">
    <div class="bk-section-inner">
      <p class="bk-label">Part II</p>
      <h2 class="bk-section-heading">How Humans React: Cooperative Transition</h2>

      <div class="bk-reaction-grid">
        <div class="bk-reaction-card">
          <p class="bk-reaction-title">Transition Dynamics</p>
          <p class="bk-reaction-text">The shift from fear-based systems to the observer status required for high-level problem solving. Most people start in fear. The ones who move to observer status first gain the most time to act.</p>
        </div>
        <div class="bk-reaction-card">
          <p class="bk-reaction-title">Behavioral Analysis</p>
          <p class="bk-reaction-text">The tendency toward rigid hierarchical behavior under threat. The transition requires a deliberate shift toward openness and nuance. Not because it is morally better. Because it is functionally necessary.</p>
        </div>
        <div class="bk-reaction-card">
          <p class="bk-reaction-title">The Egalitarian Pivot</p>
          <p class="bk-reaction-text">Moving toward collective self-actualization through egalitarian participation. The zero-marginal-cost of intelligence means hoarding it is inefficient. Sharing it is the optimal strategy.</p>
        </div>
        <div class="bk-reaction-card">
          <p class="bk-reaction-title">Relational Autonomy</p>
          <p class="bk-reaction-text">The framework for operating on openness. The inevitable shift toward collective problem-solving is not ideological. It is what the economics of intelligence demand.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ── PART III ── -->
  <section class="bk-section">
    <div class="bk-section-inner">
      <p class="bk-label">Part III</p>
      <h2 class="bk-section-heading">How to Survive the Transition</h2>

      <div class="bk-survival-list">
        <div class="bk-survival-item">
          <span class="bk-survival-n">01</span>
          <div class="bk-survival-body">
            <p class="bk-survival-title">The Horizon</p>
            <p class="bk-survival-text">Globalized logistics networks have created a structural liability. Dependency on monolithic systems leads to failure when the power is severed. The answer is not panic. It is local infrastructure built before it is needed.</p>
          </div>
        </div>
        <div class="bk-survival-item">
          <span class="bk-survival-n">02</span>
          <div class="bk-survival-body">
            <p class="bk-survival-title">Hyper-Local Systems</p>
            <p class="bk-survival-text">The necessity of moving toward self-sustaining local energy and resource grids. Not off-grid survivalism. Cooperative, community-managed infrastructure designed to stay online when the macro systems fail.</p>
          </div>
        </div>
        <div class="bk-survival-item">
          <span class="bk-survival-n">03</span>
          <div class="bk-survival-body">
            <p class="bk-survival-title">The Shouse Grid</p>
            <p class="bk-survival-text">Engineering semi-independent local microgrids and air-gapped infrastructure that integrate local compute capacity, cooperatively managed at the community level. The physical form of resilience.</p>
          </div>
        </div>
        <div class="bk-survival-item">
          <span class="bk-survival-n">04</span>
          <div class="bk-survival-body">
            <p class="bk-survival-title">The Local Biological Hub</p>
            <p class="bk-survival-text">Engineering regenerative circular production of food, shelter, and medicine. A mechanical transducer system refines local waste into high-quality materials for production. This decouples individual survival from globalized supply chains.</p>
          </div>
        </div>
        <div class="bk-survival-item">
          <span class="bk-survival-n">05</span>
          <div class="bk-survival-body">
            <p class="bk-survival-title">The Protocol</p>
            <p class="bk-survival-text">Coordinating community activities through transparent, face-to-face trust circles. Resilience that does not depend on external networks or algorithms. The oldest technology is also the most robust.</p>
          </div>
        </div>
        <div class="bk-survival-item">
          <span class="bk-survival-n">06</span>
          <div class="bk-survival-body">
            <p class="bk-survival-title">The New Social Contract</p>
            <p class="bk-survival-text">Implementing the Abundance Quotient and Adequate Level of Care. Replacing labor-for-survival models with egalitarian, cooperative participation. Food, shelter, and care as locally-secured human rights. Not a utopia. An engineering target.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ── CONCLUSION ── -->
  <section class="bk-section bk-section-alt">
    <div class="bk-section-inner">
      <p class="bk-label">Conclusion</p>
      <h2 class="bk-section-heading">The 2027 Tipping Point</h2>
      <div class="bk-conclusion-blocks">
        <div class="bk-conclusion-block">
          <p class="bk-conclusion-title">The Ignition Point</p>
          <p class="bk-conclusion-text">2027 serves as the analytical anchor for unassisted recursive self-improvement, enabled by the rapid scaling of human-level intellectual and physical labor. This is not a deadline. It is a waypoint. The preparation happens before it, not after.</p>
        </div>
        <div class="bk-conclusion-block">
          <p class="bk-conclusion-title">The Call to Action</p>
          <p class="bk-conclusion-text">The tools are on the table. The old world is gone. The transition is the current reality. The move is to cooperate as peers and build the future together, starting with the infrastructure you can touch right now.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ── SAMPLE ── -->
  <section class="bk-section">
    <div class="bk-section-inner bk-sample-inner">
      <p class="bk-label">Free Sample</p>
      <h2 class="bk-section-heading">Introduction + Chapter 1. No signup.</h2>
      <p class="bk-sample-sub">Read the opening of the book before you commit to anything. Plain PDF. About 10 minutes.</p>
      <a href="/StS-free-sample.pdf" class="bk-btn-primary" target="_blank" rel="noopener noreferrer">
        Download the free sample
      </a>
      <p class="bk-sample-note">No email. No paywall. Just open it and read.</p>
    </div>
  </section>

  <!-- ── AUTHOR'S EDITION CALLOUT ── -->
  <section class="bk-section bk-section-alt">
    <div class="bk-section-inner">
      <div class="bk-ae-card">
        <div class="bk-ae-badge">
          <svg width="11" height="11" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 1l1.88 3.82L14 5.64l-3 2.93.71 4.12L8 10.77l-3.71 1.92L5 8.57 2 5.64l4.12-.82L8 1z"/></svg>
          Author's Edition
        </div>
        <h3 class="bk-ae-title">Want the hand-bound, signed, annotated copy?</h3>
        <p class="bk-ae-text">100 copies. Each one bound and signed by the author, individually numbered, with exclusive content not in the standard edition: findings, observations, margin notes in my own hand. Payment collected at launch in August 2026.</p>
        <a href="/launch#authors-edition" class="bk-btn-secondary">Reserve your copy</a>
      </div>
    </div>
  </section>

  <!-- ── AUTHOR BIO ── -->
  <section class="bk-section">
    <div class="bk-section-inner">
      <AuthorBio />
    </div>
  </section>

  <!-- ── SUBSCRIBE ── -->
  <section class="bk-section bk-section-alt bk-subscribe">
    <div class="bk-section-inner bk-subscribe-inner">
      <p class="bk-label">Stay in the loop</p>
      <h2 class="bk-subscribe-heading">Get the next chapter when it ships.</h2>
      <p class="bk-subscribe-sub">Published on Substack. Subscribe once, get everything. Free tier covers chapters and launch alerts.</p>
      <a href="https://thecoffeejesus.substack.com" class="bk-btn-primary" target="_blank" rel="noopener noreferrer">
        Subscribe on Substack
      </a>
    </div>
  </section>

  {/if}
</div>

<style>
  .book-page {
    font-family: 'Outfit', system-ui, sans-serif;
    --amber: #f59e0b;
    --amber-dim: rgba(245,158,11,0.1);
    --surface: #0f172a;
    --border: rgba(255,255,255,0.06);
    --border-mid: rgba(255,255,255,0.1);
    --text-1: #f8fafc;
    --text-2: #cbd5e1;
    --text-3: #64748b;
    --mono: 'JetBrains Mono', monospace;
  }

  /* ── SHARED ── */
  .bk-section {
    padding: clamp(56px, 8vw, 96px) clamp(20px, 5vw, 60px);
    border-top: 1px solid var(--border);
  }
  .bk-section-alt {
    background: rgba(15, 23, 42, 0.35);
  }
  .bk-section-inner {
    max-width: 900px;
    margin: 0 auto;
  }
  .bk-label {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--amber);
    margin: 0 0 0.6rem;
    font-family: var(--mono);
  }
  .bk-section-heading {
    font-size: clamp(1.6rem, 4.5vw, 2.5rem);
    font-weight: 900;
    color: var(--text-1);
    margin: 0 0 0.75rem;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }
  .bk-section-sub {
    font-size: 1rem;
    color: var(--text-2);
    line-height: 1.6;
    margin: 0 0 2.5rem;
    max-width: 620px;
  }
  .bk-eyebrow {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--text-3);
    margin: 0 0 0.75rem;
    font-family: var(--mono);
  }

  /* ── BUTTONS ── */
  .bk-btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.8rem 1.6rem;
    background: var(--amber);
    color: #0f172a;
    font-weight: 800;
    font-size: 0.92rem;
    text-decoration: none;
    border: none;
    box-shadow: 3px 3px 0 rgba(120, 53, 15, 0.4);
    transition: opacity 0.15s ease;
    white-space: nowrap;
    font-family: inherit;
  }
  .bk-btn-primary:hover { opacity: 0.88; }

  .bk-btn-secondary {
    display: inline-flex;
    align-items: center;
    padding: 0.8rem 1.6rem;
    background: transparent;
    color: var(--text-2);
    font-weight: 700;
    font-size: 0.9rem;
    text-decoration: none;
    border: 1px solid var(--border-mid);
    transition: border-color 0.15s ease, color 0.15s ease;
    white-space: nowrap;
    font-family: inherit;
  }
  .bk-btn-secondary:hover { border-color: var(--amber); color: var(--amber); }

  /* ── HERO ── */
  .bk-hero {
    padding: clamp(40px, 6vw, 80px) clamp(20px, 5vw, 60px) clamp(56px, 8vw, 80px);
    background: linear-gradient(180deg, rgba(245,158,11,0.04) 0%, transparent 60%);
  }
  .bk-hero-inner {
    max-width: 1040px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: clamp(32px, 6vw, 72px);
    align-items: center;
  }
  @media (max-width: 680px) {
    .bk-hero-inner { grid-template-columns: 1fr; }
    .bk-cover-col { display: flex; justify-content: center; }
  }
  .bk-cover {
    width: 100%;
    max-width: 260px;
    height: auto;
    border-radius: 6px;
    box-shadow: 0 32px 72px rgba(0,0,0,0.6), 0 0 0 1px rgba(245,158,11,0.12);
  }
  .bk-title {
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 900;
    color: var(--text-1);
    margin: 0 0 0.35rem;
    letter-spacing: -0.035em;
    line-height: 1.05;
  }
  .bk-byline {
    font-size: 0.95rem;
    color: var(--text-3);
    margin: 0 0 1.25rem;
    font-family: var(--mono);
  }
  .bk-hook {
    font-size: clamp(0.95rem, 2.5vw, 1.1rem);
    color: var(--text-2);
    line-height: 1.65;
    margin: 0 0 1.75rem;
    max-width: 560px;
  }
  .bk-hero-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
  }
  .bk-hero-note {
    font-size: 0.78rem;
    color: var(--text-3);
    margin: 0;
    line-height: 1.5;
  }

  /* ── INTRODUCTION BLOCKS ── */
  .bk-intro-blocks {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin-top: 2rem;
  }
  .bk-intro-block {
    display: grid;
    grid-template-columns: 56px 1fr;
    gap: 1.25rem;
    padding: 1.5rem 0;
    border-bottom: 1px solid var(--border);
  }
  .bk-intro-block:first-child { border-top: 1px solid var(--border); }
  .bk-intro-num {
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--amber);
    font-family: var(--mono);
    letter-spacing: 0.06em;
    padding-top: 0.15rem;
  }
  .bk-intro-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 0 0 0.5rem;
  }
  .bk-intro-text {
    font-size: 0.92rem;
    color: var(--text-2);
    line-height: 1.65;
    margin: 0;
  }

  /* ── THREE PARTS ── */
  .bk-parts {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin-top: 2rem;
  }
  @media (max-width: 720px) {
    .bk-parts { grid-template-columns: 1fr; }
  }
  .bk-part {
    padding: 1.5rem;
    border: 1px solid var(--border);
    border-top: 3px solid var(--border-mid);
  }
  .bk-part-1 { border-top-color: var(--amber); }
  .bk-part-2 { border-top-color: #3b82f6; }
  .bk-part-3 { border-top-color: #10b981; }
  .bk-part-num {
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--text-3);
    font-family: var(--mono);
    display: block;
    margin-bottom: 0.5rem;
  }
  .bk-part-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 0 0 0.35rem;
    line-height: 1.2;
  }
  .bk-part-sub {
    font-size: 0.78rem;
    color: var(--amber);
    font-weight: 600;
    margin: 0 0 0.6rem;
    line-height: 1.4;
  }
  .bk-part-2 .bk-part-sub { color: #60a5fa; }
  .bk-part-3 .bk-part-sub { color: #34d399; }
  .bk-part-desc {
    font-size: 0.85rem;
    color: var(--text-2);
    line-height: 1.55;
    margin: 0;
  }

  /* ── MATHEMATICAL MAP ── */
  .bk-map {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }
  .bk-era {
    border: 1px solid var(--border);
    overflow: hidden;
  }
  .bk-era-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.65rem 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid var(--border);
  }
  .bk-era-label {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-2);
    font-family: var(--mono);
  }
  .bk-era-nums {
    font-size: 0.65rem;
    color: var(--text-3);
    font-family: var(--mono);
  }
  .bk-stages {
    display: flex;
    flex-direction: column;
  }
  .bk-stage {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 1rem;
    border-bottom: 1px solid var(--border);
    transition: background 0.15s ease;
  }
  .bk-stage:last-child { border-bottom: none; }
  .bk-stage:hover { background: rgba(255,255,255,0.02); }
  .bk-stage-current {
    background: rgba(245, 158, 11, 0.06);
    border-left: 3px solid var(--amber);
  }
  .bk-stage-n {
    font-size: 0.7rem;
    font-weight: 800;
    color: var(--text-3);
    font-family: var(--mono);
    flex-shrink: 0;
    width: 22px;
  }
  .bk-stage-current .bk-stage-n { color: var(--amber); }
  .bk-stage-t {
    font-size: 0.88rem;
    color: var(--text-2);
    flex: 1;
  }
  .bk-stage-current .bk-stage-t { color: var(--text-1); font-weight: 600; }
  .bk-stage-pill {
    font-size: 0.63rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #0f172a;
    background: var(--amber);
    padding: 0.2rem 0.55rem;
    white-space: nowrap;
    font-family: var(--mono);
  }
  .bk-thermo {
    padding: 1.25rem;
    background: rgba(245, 158, 11, 0.04);
    border: 1px solid rgba(245, 158, 11, 0.18);
    border-left: 3px solid rgba(245, 158, 11, 0.5);
  }
  .bk-thermo-label {
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--amber);
    margin: 0 0 0.4rem;
    font-family: var(--mono);
  }
  .bk-thermo-text {
    font-size: 0.88rem;
    color: var(--text-2);
    line-height: 1.6;
    margin: 0;
  }

  /* ── PART II: REACTION GRID ── */
  .bk-reaction-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 2rem;
  }
  @media (max-width: 600px) {
    .bk-reaction-grid { grid-template-columns: 1fr; }
  }
  .bk-reaction-card {
    padding: 1.25rem;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border);
    border-left: 3px solid rgba(59, 130, 246, 0.4);
  }
  .bk-reaction-title {
    font-size: 0.88rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 0 0 0.45rem;
  }
  .bk-reaction-text {
    font-size: 0.85rem;
    color: var(--text-2);
    line-height: 1.6;
    margin: 0;
  }

  /* ── PART III: SURVIVAL LIST ── */
  .bk-survival-list {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin-top: 2rem;
  }
  .bk-survival-item {
    display: grid;
    grid-template-columns: 48px 1fr;
    gap: 1rem;
    padding: 1.25rem 0;
    border-bottom: 1px solid var(--border);
  }
  .bk-survival-item:first-child { border-top: 1px solid var(--border); }
  .bk-survival-n {
    font-size: 0.72rem;
    font-weight: 800;
    color: #10b981;
    font-family: var(--mono);
    padding-top: 0.15rem;
  }
  .bk-survival-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 0 0 0.4rem;
  }
  .bk-survival-text {
    font-size: 0.88rem;
    color: var(--text-2);
    line-height: 1.6;
    margin: 0;
  }

  /* ── CONCLUSION ── */
  .bk-conclusion-blocks {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
    margin-top: 2rem;
  }
  @media (max-width: 600px) {
    .bk-conclusion-blocks { grid-template-columns: 1fr; }
  }
  .bk-conclusion-block {
    padding: 1.5rem;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border);
  }
  .bk-conclusion-title {
    font-size: 0.88rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 0 0 0.5rem;
  }
  .bk-conclusion-text {
    font-size: 0.88rem;
    color: var(--text-2);
    line-height: 1.65;
    margin: 0;
  }

  /* ── SAMPLE ── */
  .bk-sample-inner {
    text-align: center;
  }
  .bk-sample-sub {
    font-size: 0.95rem;
    color: var(--text-2);
    line-height: 1.6;
    margin: 0 auto 1.5rem;
    max-width: 480px;
  }
  .bk-sample-note {
    font-size: 0.78rem;
    color: var(--text-3);
    margin: 0.75rem 0 0;
  }

  /* ── AUTHOR'S EDITION CALLOUT ── */
  .bk-ae-card {
    padding: 2rem;
    background: rgba(245, 158, 11, 0.04);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-left: 3px solid rgba(245, 158, 11, 0.6);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-width: 640px;
  }
  .bk-ae-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--amber);
    font-family: var(--mono);
  }
  .bk-ae-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text-1);
    margin: 0;
    line-height: 1.3;
  }
  .bk-ae-text {
    font-size: 0.88rem;
    color: var(--text-2);
    line-height: 1.65;
    margin: 0;
  }

  /* ── SUBSCRIBE ── */
  .bk-subscribe { text-align: center; }
  .bk-subscribe-inner { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; }
  .bk-subscribe-heading {
    font-size: clamp(1.4rem, 4vw, 2rem);
    font-weight: 900;
    color: var(--text-1);
    margin: 0;
    letter-spacing: -0.025em;
  }
  .bk-subscribe-sub {
    font-size: 0.92rem;
    color: var(--text-2);
    line-height: 1.6;
    margin: 0;
    max-width: 460px;
  }
</style>
