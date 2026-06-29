<script>
  import { onMount } from 'svelte';

  const AUTHORS_LIMIT = 100;
  let authorsClaimed = null; // null = loading

  onMount(async () => {
    try {
      const res = await fetch('/api/preorder-count');
      if (res.ok) {
        const data = await res.json();
        authorsClaimed = data.authors ?? 0;
      }
    } catch {
      // silent: badge just won't show
    }
  });

  $: remaining = authorsClaimed === null ? null : AUTHORS_LIMIT - authorsClaimed;
</script>

<div class="lpc-wrap">
  <div class="lpc-card">

    <div class="lpc-left">
      <div class="lpc-eyebrow">
        <span class="lpc-dot" aria-hidden="true"></span>
        Book Launch &amp; Mission
      </div>
      <h2 class="lpc-title">Imagine your job was piloting a robot.</h2>
      <p class="lpc-body">
        Real jobs. Real hardware. A distributed workforce of robot pilots working from home, providing elder care, maintaining public infrastructure, and doing heavy labor from the safety of their own living rooms. This is one of the concrete futures this project is building toward.
      </p>
      <p class="lpc-body">
        See where the book is going, what we're doing with the proceeds, and how the community retraining program fits into the larger plan.
      </p>
      {#if remaining !== null && remaining < AUTHORS_LIMIT}
        <p class="lpc-scarcity">
          {#if remaining <= 0}
            Author's Edition sold out.
          {:else}
            <strong>{remaining}</strong> of {AUTHORS_LIMIT} Author's Edition copies remaining.
          {/if}
          <a href="/launch#authors-edition">Reserve yours →</a>
        </p>
      {/if}

      <div class="lpc-actions">
        <a href="/launch" class="lpc-btn-primary">
          See the Plan
          <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <a href="https://johnnyautoseed.com" class="lpc-btn-secondary" target="_blank" rel="noopener noreferrer">
          Johnny Autoseed →
        </a>
      </div>
    </div>

    <div class="lpc-right" aria-hidden="true">
      <div class="lpc-jobs">
        <div class="lpc-job lpc-job--1">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          <span>Home Care</span>
        </div>
        <div class="lpc-job lpc-job--2">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span>Infrastructure</span>
        </div>
        <div class="lpc-job lpc-job--3">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>Hazmat Response</span>
        </div>
        <div class="lpc-job lpc-job--4">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          <span>Elder Care</span>
        </div>
        <div class="lpc-job lpc-job--5">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
          <span>Heavy Demolition</span>
        </div>
        <div class="lpc-job lpc-job--6">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3h18v18H3z"/><path d="M3 9h18M9 21V9"/></svg>
          <span>Agriculture</span>
        </div>
      </div>
    </div>

  </div>
</div>

<style>
  .lpc-wrap {
    padding: 0 1rem;
  }

  @media (min-width: 640px) {
    .lpc-wrap { padding: 0 1.5rem; }
  }

  @media (min-width: 1024px) {
    .lpc-wrap { padding: 0 2rem; }
  }

  .lpc-card {
    max-width: 1100px;
    margin: 0 auto;
    background: rgba(30, 41, 59, 0.35);
    border: 1px solid rgba(245, 158, 11, 0.14);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
  }

  .lpc-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.4), transparent);
  }

  .lpc-card:hover {
    border-color: rgba(245, 158, 11, 0.25);
  }

  @media (min-width: 768px) {
    .lpc-card {
      flex-direction: row;
      align-items: center;
      padding: 3rem 2.5rem;
    }
  }

  /* ── LEFT ── */
  .lpc-left {
    flex: 1;
    min-width: 0;
  }

  .lpc-eyebrow {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #f59e0b;
    margin-bottom: 0.85rem;
    font-family: var(--font-primary, 'Inter', sans-serif);
  }

  .lpc-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #f59e0b;
    flex-shrink: 0;
    animation: lpc-pulse 2.4s ease-in-out infinite;
  }

  @keyframes lpc-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.45; transform: scale(0.75); }
  }

  .lpc-title {
    font-size: clamp(1.4rem, 4vw, 1.9rem);
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 0.9rem;
    letter-spacing: -0.025em;
    line-height: 1.2;
    text-wrap: balance;
  }

  .lpc-body {
    font-size: 0.93rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0 0 0.75rem;
    max-width: 480px;
  }

  .lpc-body:last-of-type { margin-bottom: 0.75rem; }

  .lpc-scarcity {
    font-size: 0.82rem;
    color: #f59e0b;
    margin: 0 0 1.1rem;
    line-height: 1.5;
  }

  .lpc-scarcity strong {
    font-variant-numeric: tabular-nums;
  }

  .lpc-scarcity a {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 3px;
    margin-left: 0.3rem;
    white-space: nowrap;
  }

  /* ── ACTIONS ── */
  .lpc-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    align-items: center;
  }

  .lpc-btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.6rem 1.2rem;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 700;
    font-size: 0.875rem;
    border-radius: 8px;
    text-decoration: none;
    transition: background 0.15s ease, transform 0.15s ease;
  }

  .lpc-btn-primary:hover {
    background: #fbbf24;
    transform: translateY(-1px);
  }

  .lpc-btn-secondary {
    display: inline-flex;
    align-items: center;
    padding: 0.6rem 1.2rem;
    background: transparent;
    color: #64748b;
    font-weight: 600;
    font-size: 0.875rem;
    border-radius: 8px;
    text-decoration: none;
    border: 1px solid rgba(100, 116, 139, 0.25);
    transition: color 0.15s ease, border-color 0.15s ease;
  }

  .lpc-btn-secondary:hover {
    color: #94a3b8;
    border-color: rgba(100, 116, 139, 0.5);
  }

  /* ── RIGHT: JOB GRID ── */
  .lpc-right {
    display: none;
    flex-shrink: 0;
  }

  @media (min-width: 768px) {
    .lpc-right { display: block; }
  }

  .lpc-jobs {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.65rem;
    width: 280px;
  }

  .lpc-job {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    background: rgba(2, 6, 23, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 10px;
    padding: 0.75rem 0.5rem;
    font-size: 0.68rem;
    font-weight: 600;
    color: #64748b;
    text-align: center;
    letter-spacing: 0.01em;
    transition: border-color 0.2s ease, color 0.2s ease;
    animation: lpc-float 6s ease-in-out infinite;
  }

  .lpc-job:hover {
    border-color: rgba(245, 158, 11, 0.2);
    color: #94a3b8;
  }

  .lpc-job svg {
    width: 18px;
    height: 18px;
    color: rgba(245, 158, 11, 0.5);
    flex-shrink: 0;
  }

  /* Stagger float animation */
  .lpc-job--1 { animation-delay: 0s; }
  .lpc-job--2 { animation-delay: 0.8s; }
  .lpc-job--3 { animation-delay: 1.6s; }
  .lpc-job--4 { animation-delay: 0.4s; }
  .lpc-job--5 { animation-delay: 1.2s; }
  .lpc-job--6 { animation-delay: 2s; }

  @keyframes lpc-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
  }

  @media (prefers-reduced-motion: reduce) {
    .lpc-dot { animation: none; }
    .lpc-job { animation: none; }
  }
</style>
