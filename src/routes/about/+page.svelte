<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';

  let visible = false;
  onMount(() => { visible = true; });
</script>

<svelte:head>
  <title>About — Surviving the Singularity</title>
  <meta name="description" content="Material independence through digital leverage, local AI, and minimalist infrastructure. We build the blueprint for sovereign living." />
</svelte:head>

{#if visible}
  <div class="about-page" in:fade={{ duration: 400 }}>
    <header class="about-header">
      <p class="about-label">About This Project</p>
      <h1 class="about-title">We're Building the Exit Strategy</h1>
      <p class="about-subtitle">
        Surviving the Singularity is a research project, a blueprint, and a call to action. We document the path to material independence for makers, builders, and anyone tired of the broken math of modern life.
      </p>
    </header>

    <section class="about-section">
      <h2>The Thesis</h2>
      <p>
        The traditional path to stability — 30-year mortgage, corporate career, retirement — is mathematically inaccessible for the maker class. The cost of housing has outpaced wages by orders of magnitude, and the social contract that once guaranteed security in exchange for compliance has collapsed.
      </p>
      <p>
        Our answer is the <strong>YouTube Shouse Blueprint</strong>: a comprehensive strategy that combines minimalist infrastructure (the shouse), digital leverage (YouTube and direct-to-consumer products), local AI sovereignty, and open-source robotics to create a life of genuine independence.
      </p>
    </section>

    <section class="about-section">
      <h2>What We Provide</h2>
      <div class="provides-grid">
        <div class="provide-item">
          <h3>The Blueprint</h3>
          <p>Eight chapters of tactical analysis covering everything from construction costs to GPU benchmarks for local LLMs.</p>
        </div>
        <div class="provide-item">
          <h3>The Blog</h3>
          <p>Deep dives into AI breakthroughs, robotics, synthetic biology, and the technologies reshaping the landscape.</p>
        </div>
        <div class="provide-item">
          <h3>The Book</h3>
          <p>A longer-form exploration of the singularity, its implications, and practical frameworks for navigating it.</p>
        </div>
        <div class="provide-item">
          <h3>The Data</h3>
          <p>Real numbers: purchasing power charts, construction cost tables, GPU benchmarks, crop yields, and ROI calculations.</p>
        </div>
      </div>
    </section>

    <section class="about-section">
      <h2>The Philosophy</h2>
      <p>
        We believe individuals are not consumables for the rich — they are self-determining entities with the right to autonomy. Material independence is not about isolation; it's about building from a position of strength. When your overhead is crushed, your time is reclaimed, and your tools are sovereign, you can finally contribute to a community from abundance rather than scarcity.
      </p>
      <p>
        This project is commentary, not financial advice. Build at your own risk. Think for yourself. The math proof exists — material independence is becoming more possible with every passing day as technology becomes cheaper, better, and faster.
      </p>
    </section>

    <section class="about-section about-cta">
      <h2>Start Here</h2>
      <p>Read the blueprint. Build your exit strategy. Hit record and speak with your full chest.</p>
      <div class="about-actions">
        <a href="/blueprint" class="btn-primary">Read the Blueprint</a>
        <a href="/blog" class="btn-secondary">Read the Blog</a>
      </div>
    </section>
  </div>
{/if}

<style>
  .about-page {
    max-width: 760px;
    margin: 0 auto;
    padding: 3rem 1.5rem 5rem;
  }

  .about-header {
    margin-bottom: 3.5rem;
  }

  .about-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #f59e0b;
    margin: 0 0 0.75rem 0;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
  }

  .about-title {
    font-size: clamp(1.75rem, 5vw, 2.5rem);
    font-weight: 900;
    color: #f1f5f9;
    margin: 0 0 1rem 0;
    letter-spacing: -0.03em;
  }

  .about-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0;
  }

  .about-section {
    margin-bottom: 3rem;
  }

  .about-section h2 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 1rem 0;
    letter-spacing: -0.02em;
  }

  .about-section p {
    font-size: 1.02rem;
    color: #94a3b8;
    line-height: 1.8;
    margin: 0 0 1rem 0;
  }

  .about-section strong {
    color: #f59e0b;
    font-weight: 600;
  }

  .provides-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    margin-top: 0.5rem;
  }

  .provide-item {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 14px;
    padding: 1.5rem;
  }

  .provide-item h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0 0 0.5rem 0;
  }

  .provide-item p {
    font-size: 0.88rem;
    color: #64748b;
    line-height: 1.5;
    margin: 0;
  }

  .about-cta {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(148, 163, 184, 0.08);
  }

  .about-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 1.5rem;
  }

  .btn-primary {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.75rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-weight: 600;
    font-size: 0.9rem;
    border-radius: 10px;
    text-decoration: none;
    transition: all 0.2s;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
  }

  .btn-secondary {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.75rem;
    background: rgba(255, 255, 255, 0.05);
    color: #cbd5e1;
    font-weight: 600;
    font-size: 0.9rem;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    text-decoration: none;
    transition: all 0.2s;
  }

  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
  }

  @media (max-width: 640px) {
    .about-page {
      padding: 2rem 1rem 4rem;
    }

    .about-actions {
      flex-direction: column;
      align-items: center;
    }
  }
</style>
