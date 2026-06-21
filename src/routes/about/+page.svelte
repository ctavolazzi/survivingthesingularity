<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';

  let visible = false;
  onMount(() => { visible = true; });
</script>

<svelte:head>
  <title>About - Surviving the Singularity</title>
  <meta name="description" content="Material independence through digital leverage, local AI, and minimalist infrastructure. We build the blueprint for sovereign living." />
</svelte:head>

{#if visible}
  <div class="about-page" in:fade={{ duration: 400 }}>
    <header class="about-header">
      <p class="about-label">About This Project</p>
      <h1 class="about-title">A Research Notebook on What Comes Next</h1>
      <p class="about-subtitle">
        This project began as personal research into what material resilience looks like in a period of rapid AI deployment. It has grown into a reference for anyone (individuals, planners, or organizations) trying to update their frameworks before the window narrows. Material here is the author's commentary and supposition, not advice. Anything you might consider acting on should be evaluated with the relevant licensed professionals.
      </p>
    </header>

    <section class="about-section">
      <h2>The Thesis</h2>
      <p>
        For many people in many places, the costs of housing relative to wages have shifted significantly over recent decades. Whether the old playbook still works for any individual depends on geography, profession, family situation, and dozens of other factors. None of this is meant as a universal claim.
      </p>
      <p>
        One direction the author has been exploring is the <strong>YouTube Shouse Blueprint</strong>: a thought experiment combining minimalist infrastructure, public-facing creator work, local AI tools, and open-source automation. It is a hypothesis to think with, not a plan to follow.
      </p>
    </section>

    <section class="about-section">
      <h2>What's Here</h2>
      <div class="provides-grid">
        <div class="provide-item">
          <h3>The Blueprint</h3>
          <p>Eight chapters of tactical analysis covering everything from construction costs to GPU benchmarks for local LLMs. Organized to be useful at different scales: whether you're making decisions for yourself, your organization, or your community.</p>
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
          <p>Reference figures from public sources: purchasing-power indicators, construction cost ranges, GPU benchmarks, illustrative yield and ROI examples. Verify any number you intend to rely on.</p>
        </div>
      </div>
    </section>

    <section class="about-section">
      <h2>The Philosophy</h2>
      <p>
        The author values personal autonomy and lower fixed costs as a starting point for stronger civic and community participation. Whether any specific tactic discussed on this site is appropriate for you is a question for you and your professional advisors.
      </p>
      <p>
        This project is commentary and informational only. Not financial, legal, real-estate, medical, or any other professional advice. Always consult the relevant licensed professionals before making any decision based on anything published here.
      </p>
    </section>

    <section class="about-section about-cta">
      <h2>Start Here</h2>
      <p>Read the material as one author's commentary. Take what's useful for your own thinking. Always consult the relevant licensed professionals before acting.</p>
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
    padding: 2rem 1rem 3rem;
  }

  @media (min-width: 640px) {
    .about-page { padding: 3rem 1.5rem 5rem; }
  }

  .about-header {
    margin-bottom: 3.5rem;
  }

  .about-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #f59e0b;
    margin: 0 0 0.75rem 0;
    font-weight: 600;
    font-family: var(--font-primary);
  }

  .about-title {
    font-size: clamp(1.75rem, 5vw, 2.5rem);
    font-weight: 900;
    color: #f1f5f9;
    margin: 0 0 1rem 0;
    letter-spacing: -0.03em;
    text-wrap: balance;
  }

  .about-subtitle {
    font-size: 1.1rem;
    color: #dde4ef;
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
    color: #dde4ef;
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
    color: #dde4ef;
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
    color: #e9eef5;
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

  /* Base: stack actions on mobile */
  .about-actions {
    flex-direction: column;
    align-items: center;
  }

  @media (min-width: 640px) {
    .about-actions {
      flex-direction: row;
      align-items: center;
    }
  }
</style>
