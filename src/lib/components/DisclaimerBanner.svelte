<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  // Hybrid clickwrap consent. "I Agree" stores a versioned consent record
  // (timestamp + version) in localStorage. Banner re-shows if the version
  // string is bumped (e.g. when terms materially change).
  const CONSENT_VERSION = 'v1-2026-05-26';
  const CONSENT_KEY = 'sts:consent';

  let agreed = false;
  let agreedAt = '';

  onMount(() => {
    if (!browser) return;
    try {
      const raw = localStorage.getItem(CONSENT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && parsed.version === CONSENT_VERSION && parsed.at) {
          agreed = true;
          agreedAt = parsed.at;
        }
      }
    } catch {}
  });

  function agree() {
    const at = new Date().toISOString();
    try {
      localStorage.setItem(
        CONSENT_KEY,
        JSON.stringify({ version: CONSENT_VERSION, at })
      );
    } catch {}
    agreedAt = at;
    agreed = true;
  }
</script>

{#if !agreed}
  <aside class="disclaimer-banner" role="region" aria-label="Site disclaimer and acceptance">
    <div class="dbnr-inner">
      <div class="dbnr-icon" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M9 1L1 16H17L9 1Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
          <path d="M9 7V11" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          <circle cx="9" cy="13.5" r="0.7" fill="currentColor"/>
        </svg>
      </div>
      <p class="dbnr-text">
        <strong>This site is for informational and educational purposes only.</strong>
        It is not professional advice and should not be used in place of professional advice. Please consult all relevant professionals before making any decisions. Site is offered AS-IS with no warranties of any kind. By using this site, you agree to the
        <a href="/terms" class="dbnr-link-inline">Terms</a>,
        <a href="/disclaimer" class="dbnr-link-inline">Disclaimer</a>, and
        <a href="/policies" class="dbnr-link-inline">Privacy</a>.
      </p>
      <button type="button" class="dbnr-agree" on:click={agree} aria-label="I have read and agree to the Terms, Disclaimer, and Privacy">
        I Agree
      </button>
    </div>
  </aside>
{:else if agreedAt}
  <div class="consent-stamp" aria-hidden="true">
    Acceptance recorded · {agreedAt.slice(0, 10)} · <a href="/terms">Terms</a> · <a href="/disclaimer">Disclaimer</a>
  </div>
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
    padding: 0.7rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #fee2e2;
  }

  .dbnr-icon {
    flex-shrink: 0;
    color: #fca5a5;
  }

  .dbnr-text {
    margin: 0;
    font-size: 0.78rem;
    line-height: 1.5;
    flex: 1;
  }

  .dbnr-text strong {
    color: #fef2f2;
    font-weight: 700;
  }

  .dbnr-link-inline {
    color: #fca5a5;
    text-decoration: underline;
    text-underline-offset: 2px;
    font-weight: 600;
  }

  .dbnr-link-inline:hover {
    color: #fef2f2;
  }

  .dbnr-agree {
    flex-shrink: 0;
    background: #fee2e2;
    color: #7f1d1d;
    border: 1px solid #fecaca;
    padding: 0.45rem 0.85rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    line-height: 1;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
  }

  .dbnr-agree:hover {
    background: #fef2f2;
    color: #450a0a;
  }

  .dbnr-agree:focus-visible {
    outline: 2px solid #fef2f2;
    outline-offset: 2px;
  }

  .consent-stamp {
    background: rgba(15, 23, 42, 0.85);
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    font-size: 0.66rem;
    color: #64748b;
    text-align: center;
    padding: 0.35rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
  }

  .consent-stamp a {
    color: #94a3b8;
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  .consent-stamp a:hover {
    color: #f59e0b;
  }

  @media (max-width: 640px) {
    .dbnr-text { font-size: 0.72rem; }
    .dbnr-inner { padding: 0.6rem 0.75rem; gap: 0.5rem; flex-wrap: wrap; }
    .dbnr-agree { width: 100%; padding: 0.55rem 0.85rem; }
  }
</style>
