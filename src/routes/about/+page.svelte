<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import AuthorBio from '$lib/components/AuthorBio.svelte';

  let visible = false;
  onMount(() => { visible = true; });
</script>

<svelte:head>
  <title>About: Surviving the Singularity</title>
  <meta name="description" content="Christopher Tavolazzi (The Coffee Jesus) is a developer, futurist, and founder of Johnny Autoseed. Surviving the Singularity is a living field guide written in real time as the world changes." />
</svelte:head>

{#if visible}
  <div class="about-page" in:fade={{ duration: 400 }}>
    <header class="about-header">
      <p class="about-label">About</p>
      <h1 class="about-title">I'm writing this in real time.</h1>
      <p class="about-subtitle">
        Developer, futurist, founder of Johnny Autoseed. I write to make sense of the AI shift as it happens. This book updates as the world does.
      </p>
    </header>

    <AuthorBio />

    <section class="about-section">
      <h2>Why this exists</h2>
      <p>
        The 2017 Transformer architecture crossed an event horizon most people missed. Intelligence now has a marginal cost near zero. The gap between people who understand that and people who don't is widening every quarter.
      </p>
      <p>
        I started writing this to work it out for myself. It became something I could share. The book grows as the situation develops. Nothing here is finished. Neither is the world.
      </p>
    </section>

    <section class="about-section">
      <h2>What's here</h2>
      <div class="provides-grid">
        <div class="provide-item">
          <h3>The Book</h3>
          <p>Three parts: what the singularity is, how people react, and what you can do. Updated as it's written.</p>
          <a href="/book" class="provide-link">Read the book</a>
        </div>
        <div class="provide-item">
          <h3>The Checklist</h3>
          <p>Seven moves to start where you are. Free, no signup required for the first three steps.</p>
          <a href="/checklist" class="provide-link">Start the checklist</a>
        </div>
        <div class="provide-item">
          <h3>Early Access</h3>
          <p>$5 gets you the full draft, the research bundle, and the Standard Edition when it ships. A hand-bound Author's Edition is also available.</p>
          <a href="/early-access" class="provide-link">Get early access</a>
        </div>
        <div class="provide-item">
          <h3>The Blog</h3>
          <p>Dispatches on AI breakthroughs, robotics, synthetic biology, and what's shifting week to week.</p>
          <a href="/blog" class="provide-link">Read the blog</a>
        </div>
      </div>
    </section>

    <section class="about-section about-note">
      <p>
        Everything here is commentary and informational only. Not financial, legal, medical, or any other professional advice. Verify anything you intend to rely on and consult the relevant licensed professionals before acting.
      </p>
    </section>

    <section class="about-section about-cta">
      <h2>Start here</h2>
      <p>Read the book as it's being written. Or start free with the checklist.</p>
      <div class="about-actions">
        <a href="/book" class="btn-primary">Read the Book</a>
        <a href="/checklist" class="btn-secondary">Start the Checklist</a>
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
    margin-bottom: 3rem;
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
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .provide-item h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0;
  }

  .provide-item p {
    font-size: 0.88rem;
    color: #dde4ef;
    line-height: 1.5;
    margin: 0;
    flex: 1;
  }

  .provide-link {
    font-size: 0.85rem;
    color: #f59e0b;
    text-decoration: none;
    font-weight: 600;
    margin-top: 0.25rem;
  }

  .provide-link:hover { color: #fbbf24; text-decoration: underline; }

  .about-note {
    border-top: 1px solid rgba(148, 163, 184, 0.08);
    padding-top: 2rem;
    margin-bottom: 2rem;
  }

  .about-note p {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.7;
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
    flex-direction: column;
    align-items: center;
  }

  @media (min-width: 640px) {
    .about-actions {
      flex-direction: row;
      align-items: center;
    }
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
</style>
