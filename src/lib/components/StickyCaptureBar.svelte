<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import { page } from '$app/stores';

  // Routes where an interrupting bar is unwelcome: legal pages, long-form
  // reading views, and the checklist page itself (it IS the destination).
  const SUPPRESS_PREFIXES = ['/policies', '/terms', '/disclaimer', '/accessibility', '/book', '/blueprint', '/checklist'];

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
    background: rgba(10, 15, 30, 0.97);
    border-top: 1px solid rgba(245, 158, 11, 0.25);
    box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
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
    border-radius: 4px;
  }
  .capture-copy strong { color: #f1f5f9; }
  .capture-copy-sub { color: #94a3b8; font-weight: 500; }

  .capture-btn {
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.6rem 1.2rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-weight: 700;
    font-size: 0.88rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none;
    transition: opacity 0.15s ease, transform 0.15s ease;
  }
  .capture-btn:hover { opacity: 0.92; transform: translateY(-1px); }

  .capture-close {
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 7px;
    color: #94a3b8;
    cursor: pointer;
    transition: color 0.15s ease, border-color 0.15s ease;
    margin-left: auto;
  }
  .capture-close:hover { color: #e2e8f0; border-color: rgba(148, 163, 184, 0.35); }

  @media (max-width: 560px) {
    .capture-copy-sub { display: none; }
    .capture-btn { flex: 1; justify-content: center; }
  }

  @media (prefers-reduced-motion: reduce) {
    .capture-bar { animation: none; }
  }
</style>
