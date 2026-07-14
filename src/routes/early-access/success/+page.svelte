<script>
  export let data;
</script>

<svelte:head>
  <title>You're in. Surviving the Singularity</title>
  <meta name="description" content="Your preorder is confirmed. Your research bundle is on its way." />
  <meta name="robots" content="noindex" />
</svelte:head>

<div class="success-page">

  {#if data.ok}

    <div class="success-hero">
      <div class="success-check" aria-hidden="true">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <circle cx="16" cy="16" r="16" fill="rgba(16,185,129,0.15)"/>
          <path d="M9 16.5l4.5 4.5 9-9" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>

      {#if data.mock}
        <span class="success-mode-badge">Dev mode</span>
      {/if}

      <h1 class="success-heading">You're in.</h1>
      <p class="success-sub">
        {#if data.email}
          Your research bundle and access links are on their way to <strong>{data.email}</strong>.
        {:else}
          Your research bundle is ready. Download it below.
        {/if}
      </p>
    </div>

    <!-- Download card -->
    <div class="download-card">
      <div class="download-card-header">
        <div class="download-icon" aria-hidden="true">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
        </div>
        <div>
          <p class="download-name">Research Bundle</p>
          <p class="download-meta">PDFs, papers, images, source documents</p>
        </div>
      </div>

      {#if data.bundleUrl}
        <a href={data.bundleUrl} class="download-btn" download>
          Download now
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
        </a>
        {#if data.email}
          <p class="download-email-note">Also sent to {data.email}. Link valid for 7 days.</p>
        {/if}
      {:else}
        <div class="download-pending">
          <p>Your bundle link is being prepared. Check your email in a moment, or <a href="mailto:ctavolazzi@gmail.com">contact us</a> if it doesn't arrive within 10 minutes.</p>
        </div>
      {/if}
    </div>

    <!-- What's included in early access -->
    <div class="success-kit">
      <p class="kit-label">Also in your early access</p>
      <div class="kit-grid">
        <a href="/book" class="kit-item">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>
          <span class="kit-item-text">
            <span class="kit-item-name">The Book</span>
            <span class="kit-item-desc">Full draft, open now</span>
          </span>
        </a>
        <a href="/checklist" class="kit-item">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
          <span class="kit-item-text">
            <span class="kit-item-name">Readiness Checklist</span>
            <span class="kit-item-desc">7 moves to get ready</span>
          </span>
        </a>
      </div>
    </div>

  {:else}

    <div class="success-hero">
      <div class="error-icon" aria-hidden="true">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <circle cx="16" cy="16" r="16" fill="rgba(239,68,68,0.12)"/>
          <path d="M12 12l8 8M20 12l-8 8" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      </div>
      <h1 class="success-heading">Something went wrong.</h1>
      <p class="success-sub">{data.error ?? 'We could not verify your payment.'}</p>
      <p class="success-sub">Email <a href="mailto:ctavolazzi@gmail.com" class="contact-link">ctavolazzi@gmail.com</a> with your order details and we will sort it out.</p>
      <a href="/early-access" class="back-link">Back to early access</a>
    </div>

  {/if}

</div>

<style>
  .success-page {
    max-width: 640px;
    margin: 0 auto;
    padding: clamp(80px, 14vw, 120px) clamp(20px, 5vw, 48px) clamp(64px, 10vw, 96px);
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  .success-hero {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }

  .success-check, .error-icon {
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.2);
  }

  .error-icon { background: rgba(239,68,68,0.06); border-color: rgba(239,68,68,0.18); }

  .success-mode-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #f59e0b;
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 999px;
    padding: 3px 10px;
  }

  .success-heading {
    font-size: clamp(2.4rem, 7vw, 3.6rem);
    font-weight: 900;
    color: #f8fafc;
    letter-spacing: -0.03em;
    line-height: 1;
    margin: 0;
  }

  .success-sub {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.7;
    max-width: 42ch;
    margin: 0;
  }
  .success-sub strong { color: #f1f5f9; font-weight: 600; }

  /* Download card */
  .download-card {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(245,158,11,0.2);
    border-left: 3px solid #f59e0b;
    border-radius: 16px;
    padding: clamp(20px, 3vw, 28px);
    display: flex;
    flex-direction: column;
    gap: 16px;
    box-shadow: 4px 4px 0 rgba(245,158,11,0.08);
  }

  .download-card-header {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .download-icon {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.18);
    border-radius: 10px;
  }

  .download-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 3px;
  }

  .download-meta {
    font-size: 0.86rem;
    color: #64748b;
    margin: 0;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
  }

  .download-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #f59e0b;
    color: #0a0a0a;
    font-weight: 800;
    font-size: 1rem;
    padding: 13px 22px;
    border-radius: 10px;
    text-decoration: none;
    align-self: flex-start;
    transition: filter 0.15s ease, transform 0.15s ease;
    box-shadow: 0 4px 16px rgba(245,158,11,0.3);
  }
  .download-btn:hover { filter: brightness(1.08); transform: translateY(-1px); }
  .download-btn:active { transform: scale(0.98); }

  .download-email-note {
    font-size: 0.82rem;
    color: #475569;
    margin: 0;
  }

  .download-pending {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 0.9rem;
    color: #64748b;
    line-height: 1.6;
  }
  .download-pending a { color: #f59e0b; text-decoration: underline; text-underline-offset: 2px; }

  /* Kit grid */
  .success-kit { display: flex; flex-direction: column; gap: 14px; }
  .kit-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #64748b;
  }

  .kit-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  @media (max-width: 480px) { .kit-grid { grid-template-columns: 1fr; } }

  .kit-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 16px;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    text-decoration: none;
    transition: border-color 0.15s ease, background 0.15s ease;
  }
  .kit-item:hover { border-color: rgba(245,158,11,0.25); background: rgba(245,158,11,0.04); }

  .kit-item svg { flex-shrink: 0; }
  .kit-item-text { display: flex; flex-direction: column; flex: 1; min-width: 0; }
  .kit-item-name { font-size: 0.92rem; font-weight: 700; color: #f1f5f9; }
  .kit-item-desc { font-size: 0.76rem; color: #64748b; display: block; margin-top: 1px; }

  .contact-link { color: #f59e0b; text-decoration: underline; text-underline-offset: 2px; }
  .back-link { font-size: 0.9rem; color: #f59e0b; text-decoration: underline; text-underline-offset: 2px; margin-top: 8px; }
</style>
