<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import { page } from '$app/stores';

  // Routes where an interrupting bar is unwelcome: legal pages, long-form
  // reading views, and the checklist page itself (it IS the destination).
  const SUPPRESS_PREFIXES = ['/policies', '/terms', '/disclaimer', '/accessibility', '/book', '/checklist'];

  const STORAGE_KEY = 'sts_capture_v2'; // 'dismissed'
  const SCROLL_TRIGGER = 700; // px scrolled before it can appear

  // Mirror of DisclaimerBanner's consent record. The bar must not appear until
  // the bottom consent banner is accepted (both are bottom-fixed — would collide).
  const CONSENT_KEY = 'sts:consent';
  const CONSENT_VERSION = 'v2-2026-06-07';

  let visible = false;
  let resolved = false;  // dismissed this device
  let consented = false; // disclaimer accepted

  $: suppressedRoute = SUPPRESS_PREFIXES.some((p) => $page.url.pathname.startsWith(p));
  $: showBar = visible && consented && !resolved && !suppressedRoute;

  function hasConsent() {
    try {
      const raw = localStorage.getItem(CONSENT_KEY);
      if (!raw) return false;
      const p = JSON.parse(raw);
      return !!(p && p.version === CONSENT_VERSION && p.at);
    } catch {
      return false;
    }
  }

  // This site scrolls on <body>, not window, and document.scrollingElement
  // points at <html> (which is fixed-height here and reports 0). Take the max
  // of every scroll source so we read the real position regardless of setup.
  function scrollTop() {
    return Math.max(
      window.scrollY || 0,
      document.documentElement?.scrollTop || 0,
      document.body?.scrollTop || 0
    );
  }

  function onScroll() {
    if (resolved) return;
    if (!consented) {
      consented = hasConsent();
      if (!consented) return;
    }
    if (scrollTop() > SCROLL_TRIGGER) visible = true;
  }

  function dismiss() {
    resolved = true;
    if (browser) localStorage.setItem(STORAGE_KEY, 'dismissed');
  }

  onMount(() => {
    if (!browser) return;
    if (localStorage.getItem(STORAGE_KEY)) { resolved = true; return; }
    consented = hasConsent();
    // capture:true so we also catch scroll from the <body> scroll container.
    window.addEventListener('scroll', onScroll, { passive: true, capture: true });
    onScroll();
  });

  onDestroy(() => {
    if (browser) window.removeEventListener('scroll', onScroll, { capture: true });
  });
</script>

{#if showBar}
  <div class="capture-bar" role="region" aria-label="Free Singularity Readiness Checklist">
    <div class="capture-inner">
      <p class="capture-copy">
        <span class="capture-tag">Free</span>
        <strong>The Singularity Readiness Checklist</strong>
        <span class="capture-copy-sub">12 moves to make before AGI.</span>
      </p>
      <a href="/checklist" class="capture-btn" on:click={dismiss}>
        Get the Checklist
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <button class="capture-close" on:click={dismiss} aria-label="Dismiss" type="button">
        <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
          <path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
  </div>
{/if}

<style>
  .capture-bar {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 120;
    background: #090e20;
    border-top: 2px solid rgba(245, 158, 11, 0.35);
    box-shadow: 0 -3px 0 rgba(245, 158, 11, 0.1);
    padding: 0.7rem 1rem;
    padding-bottom: max(0.7rem, env(safe-area-inset-bottom));
    animation: capture-up 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes capture-up {
    from { transform: translateY(100%); opacity: 0; }
    to   { transform: translateY(0); opacity: 1; }
  }

  .capture-inner {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    padding-right: 44px;
  }

  .capture-copy {
    margin: 0;
    color: #f1f5f9;
    font-size: 0.92rem;
    flex: 1 1 auto;
    min-width: 200px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  .capture-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #0f172a;
    background: #f59e0b;
    padding: 0.1rem 0.45rem;
    border-radius: 0;
  }
  .capture-copy strong { color: #f1f5f9; }
  .capture-copy-sub { color: #94a3b8; font-weight: 500; }

  .capture-btn {
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.6rem 1.2rem;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 700;
    font-size: 0.88rem;
    border: none;
    border-radius: 0;
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none;
    box-shadow: 3px 3px 0 rgba(245, 158, 11, 0.3);
    transition: box-shadow 0.12s ease;
  }
  .capture-btn:hover { box-shadow: 4px 4px 0 rgba(245, 158, 11, 0.4); }

  .capture-close {
    position: absolute;
    top: 10px;
    right: 28px;
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    color: #cbd5e1;
    cursor: pointer;
    transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
    padding: 0;
  }
  .capture-close:hover {
    color: #f1f5f9;
    border-color: rgba(255, 255, 255, 0.6);
    background: rgba(255, 255, 255, 0.14);
  }

  @media (max-width: 560px) {
    .capture-inner { flex-direction: column; align-items: stretch; padding-right: 12px; gap: 0.6rem; }
    .capture-copy-sub { display: none; }
    .capture-btn { width: 100%; justify-content: center; text-align: center; }
  }

  @media (prefers-reduced-motion: reduce) {
    .capture-bar { animation: none; }
  }
</style>
