<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

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
  <aside
    class="disclaimer-popup"
    role="region"
    aria-label="Site disclaimer and acceptance"
    transition:fly={{ y: 80, duration: 300, easing: cubicOut }}
  >
    <div class="dbnr-inner">
      <div class="dbnr-icon" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M9 1L1 16H17L9 1Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
          <path d="M9 7V11" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          <circle cx="9" cy="13.5" r="0.7" fill="currentColor"/>
        </svg>
      </div>
      <p class="dbnr-text">
        <strong>For informational and educational purposes only.</strong>
        Not professional advice. By using this site you agree to the
        <a href="/terms" class="dbnr-link-inline">Terms</a>,
        <a href="/disclaimer" class="dbnr-link-inline">Disclaimer</a>, and
        <a href="/policies" class="dbnr-link-inline">Privacy Policy</a>.
      </p>
      <button type="button" class="dbnr-agree" on:click={agree} aria-label="I have read and agree to the Terms, Disclaimer, and Privacy">
        I Agree
      </button>
    </div>
  </aside>
{/if}

<style>
  .disclaimer-popup {
    position: fixed;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9998;
    width: calc(100% - 2rem);
    max-width: 780px;
    background: rgba(40, 10, 10, 0.97);
    border: 1px solid rgba(248, 113, 113, 0.35);
    border-radius: 12px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(248, 113, 113, 0.1);
  }

  .dbnr-inner {
    padding: 0.85rem 1rem;
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
    padding: 0.5rem 1rem;
    border-radius: 8px;
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

  @media (max-width: 640px) {
    .disclaimer-popup {
      bottom: 0.6rem;
      width: calc(100% - 1rem);
      border-radius: 10px;
    }
    /* Keep a single compact row on mobile: short text + inline button.
       No wrap, no full-width button — that was doubling the banner height. */
    .dbnr-inner { padding: 0.6rem 0.7rem; gap: 0.6rem; align-items: center; }
    .dbnr-icon { display: none; }
    .dbnr-text { font-size: 0.68rem; line-height: 1.4; }
    .dbnr-agree {
      padding: 0.55rem 0.85rem;
      font-size: 0.72rem;
      align-self: stretch;
      display: flex;
      align-items: center;
    }
  }
</style>
