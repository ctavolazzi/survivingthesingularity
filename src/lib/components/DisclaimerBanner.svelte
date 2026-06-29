<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { fly, fade } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  // Hybrid clickwrap consent. "I Agree" stores a versioned consent record
  // (timestamp + version) in localStorage. Banner re-shows if the version
  // string is bumped (e.g. when terms materially change).
  const CONSENT_VERSION = 'v2-2026-06-07';
  const CONSENT_KEY = 'sts:consent';

  let agreed = false;
  let agreedAt = '';
  // "Disagree" does NOT persist - it locks the current page session. A refresh
  // clears it and re-presents the banner so the user can accept.
  let disagreed = false;

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

  // Lock page scroll while the lockout overlay is up.
  $: if (browser) {
    document.body.style.overflow = disagreed ? 'hidden' : '';
  }

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
    disagreed = false;
  }

  function disagree() {
    disagreed = true;
  }

  function refresh() {
    if (browser) location.reload();
  }
</script>

{#if disagreed}
  <!-- Full-screen lockout. Covers everything; the only way forward is to
       refresh and accept. -->
  <div class="lockout" role="alertdialog" aria-modal="true" aria-label="Site locked" transition:fade={{ duration: 200 }}>
    <div class="lockout-card">
      <div class="lockout-icon" aria-hidden="true">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
          <rect x="5" y="11" width="14" height="9" rx="2" stroke="currentColor" stroke-width="1.6"/>
          <path d="M8 11V8a4 4 0 1 1 8 0v3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
      </div>
      <h2 class="lockout-title">Site locked</h2>
      <p class="lockout-text">
        You declined the terms. The site can't be used without agreeing.
        Refresh and accept to continue.
      </p>
      <button type="button" class="lockout-btn" on:click={refresh}>
        Refresh &amp; review terms
      </button>
    </div>
  </div>
{:else if !agreed}
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
        By using this site you agree to the
        <a href="/terms" class="dbnr-link-inline">Terms</a>,
        <a href="/disclaimer" class="dbnr-link-inline">Disclaimer</a>, and
        <a href="/policies" class="dbnr-link-inline">Privacy Policy</a>.
      </p>
      <div class="dbnr-actions">
        <button type="button" class="dbnr-agree" on:click={agree} aria-label="I have read and agree to the Terms, Disclaimer, and Privacy">
          I Agree
        </button>
        <button type="button" class="dbnr-disagree" on:click={disagree} aria-label="I do not agree to the terms">
          Disagree
        </button>
      </div>
    </div>
  </aside>
{/if}

<style>
  .disclaimer-popup {
    position: fixed;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    /* Must outrank the White Rabbit debug trigger (z-index 9999), which
       otherwise overlaps the buttons and swallows the tap, leaving
       the banner undismissable and permanently covering page content. */
    z-index: 10000;
    width: calc(100% - 2rem);
    max-width: 780px;
    /* Neutral slate surface with a subtle on-brand amber edge - no red. */
    background: #0a0f23;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-left: 3px solid rgba(245, 158, 11, 0.5);
    border-radius: 0;
    box-shadow: 4px 4px 0 rgba(245, 158, 11, 0.1);
  }

  .dbnr-inner {
    padding: 0.85rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #e2e8f0;
  }

  .dbnr-icon {
    flex-shrink: 0;
    color: #f59e0b;
  }

  .dbnr-text {
    margin: 0;
    font-size: 0.86rem;
    line-height: 1.5;
    flex: 1;
  }

  .dbnr-text strong {
    color: #f8fafc;
    font-weight: 700;
  }

  .dbnr-link-inline {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 2px;
    font-weight: 600;
  }

  .dbnr-link-inline:hover {
    color: #fbbf24;
  }

  .dbnr-actions {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .dbnr-agree {
    background: #f59e0b;
    color: #0a0a0a;
    border: 1px solid #f59e0b;
    padding: 0.5rem 1rem;
    border-radius: 0;
    font-size: 0.86rem;
    font-weight: 700;
    line-height: 1;
    cursor: pointer;
    transition: background 0.15s ease;
    white-space: nowrap;
    box-shadow: 2px 2px 0 rgba(120, 53, 15, 0.4);
  }

  .dbnr-agree:hover {
    background: #fbbf24;
    border-color: #fbbf24;
  }

  .dbnr-disagree {
    background: transparent;
    color: #cbd5e1;
    border: 1px solid rgba(148, 163, 184, 0.4);
    padding: 0.5rem 0.85rem;
    border-radius: 0;
    font-size: 0.86rem;
    font-weight: 600;
    line-height: 1;
    cursor: pointer;
    transition: border-color 0.15s ease, color 0.15s ease;
    white-space: nowrap;
  }

  .dbnr-disagree:hover {
    border-color: rgba(148, 163, 184, 0.7);
    color: #f8fafc;
  }

  .dbnr-agree:focus-visible,
  .dbnr-disagree:focus-visible,
  .lockout-btn:focus-visible {
    outline: 2px solid #f59e0b;
    outline-offset: 2px;
  }

  /* ── Lockout overlay ── */
  .lockout {
    position: fixed;
    inset: 0;
    z-index: 100000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    background: rgba(2, 6, 23, 0.95);
  }

  .lockout-card {
    max-width: 380px;
    width: 100%;
    text-align: center;
    background: #0a0f23;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-left: 3px solid rgba(245, 158, 11, 0.6);
    border-radius: 0;
    padding: 2rem 1.5rem;
    box-shadow: 6px 6px 0 rgba(245, 158, 11, 0.1);
  }

  .lockout-icon {
    color: #f59e0b;
    margin-bottom: 0.75rem;
  }

  .lockout-title {
    margin: 0 0 0.5rem;
    font-size: 1.25rem;
    font-weight: 800;
    color: #f8fafc;
  }

  .lockout-text {
    margin: 0 0 1.5rem;
    font-size: 0.92rem;
    line-height: 1.6;
    color: #dde4ef;
  }

  .lockout-btn {
    background: #f59e0b;
    color: #0a0a0a;
    border: none;
    padding: 0.7rem 1.4rem;
    border-radius: 0;
    font-size: 0.95rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s ease;
    box-shadow: 3px 3px 0 rgba(120, 53, 15, 0.4);
  }

  .lockout-btn:hover { background: #fbbf24; }

  @media (max-width: 640px) {
    .disclaimer-popup {
      bottom: 0.6rem;
      width: calc(100% - 1rem);
      border-radius: 0;
    }
    /* Compact: short text + inline buttons side by side to save height. */
    .dbnr-inner { padding: 0.5rem 0.65rem; gap: 0.5rem; align-items: center; }
    .dbnr-icon { display: none; }
    .dbnr-text { font-size: 0.76rem; line-height: 1.35; }
    .dbnr-actions { flex-direction: row; gap: 0.35rem; }
    .dbnr-agree, .dbnr-disagree {
      padding: 0.4rem 0.6rem;
      font-size: 0.76rem;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
</style>
