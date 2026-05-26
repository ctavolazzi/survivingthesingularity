<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  let dismissed = false;

  onMount(() => {
    if (!browser) return;
    try {
      dismissed = localStorage.getItem('sts:disclaimer-dismissed-v1') === '1';
    } catch {}
  });

  function dismiss() {
    dismissed = true;
    try { localStorage.setItem('sts:disclaimer-dismissed-v1', '1'); } catch {}
  }
</script>

{#if !dismissed}
  <aside class="disclaimer-banner" role="region" aria-label="Site disclaimer">
    <div class="dbnr-inner">
      <div class="dbnr-icon" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M9 1L1 16H17L9 1Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
          <path d="M9 7V11" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          <circle cx="9" cy="13.5" r="0.7" fill="currentColor"/>
        </svg>
      </div>
      <p class="dbnr-text">
        <strong>INFORMATIONAL PURPOSES ONLY — ALWAYS CONSULT THE RELEVANT PROFESSIONALS BEFORE MAKING ANY DECISIONS.</strong>
        <a href="/disclaimer" class="dbnr-link">Full disclaimer →</a>
      </p>
      <button type="button" class="dbnr-dismiss" on:click={dismiss} aria-label="Dismiss disclaimer">×</button>
    </div>
  </aside>
{/if}

<style>
  .disclaimer-banner {
    position: sticky;
    top: 0;
    z-index: 9998;
    background: linear-gradient(180deg, rgba(127, 29, 29, 0.95) 0%, rgba(91, 16, 16, 0.95) 100%);
    border-bottom: 1px solid rgba(248, 113, 113, 0.4);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }

  .dbnr-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0.55rem 1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    color: #fee2e2;
  }

  .dbnr-icon {
    flex-shrink: 0;
    color: #fca5a5;
    margin-top: 0.1rem;
  }

  .dbnr-text {
    margin: 0;
    font-size: 0.78rem;
    line-height: 1.45;
    flex: 1;
  }

  .dbnr-text strong {
    color: #fef2f2;
    font-weight: 700;
  }

  .dbnr-link {
    color: #fca5a5;
    text-decoration: underline;
    text-underline-offset: 2px;
    font-weight: 600;
    white-space: nowrap;
    margin-left: 0.25rem;
  }

  .dbnr-link:hover {
    color: #fef2f2;
  }

  .dbnr-dismiss {
    flex-shrink: 0;
    background: transparent;
    border: 1px solid rgba(252, 165, 165, 0.3);
    color: #fca5a5;
    width: 26px;
    height: 26px;
    border-radius: 6px;
    font-size: 1rem;
    line-height: 1;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    transition: all 0.15s ease;
  }

  .dbnr-dismiss:hover {
    background: rgba(252, 165, 165, 0.12);
    color: #fef2f2;
    border-color: rgba(252, 165, 165, 0.6);
  }

  @media (max-width: 640px) {
    .dbnr-text { font-size: 0.72rem; }
    .dbnr-inner { padding: 0.5rem 0.75rem; gap: 0.5rem; }
  }
</style>
