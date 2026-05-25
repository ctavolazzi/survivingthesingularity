<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import { fly } from 'svelte/transition';

  const STORAGE_KEY = 'kofi-floater-dismissed';
  const DELAY_MS = 30000;

  let visible = false;
  let timer = null;

  onMount(() => {
    if (!browser) return;
    if (localStorage.getItem(STORAGE_KEY) === '1') return;
    timer = setTimeout(() => { visible = true; }, DELAY_MS);
  });

  onDestroy(() => {
    if (timer) clearTimeout(timer);
  });

  function dismiss() {
    visible = false;
    if (browser) localStorage.setItem(STORAGE_KEY, '1');
  }
</script>

{#if visible}
  <div class="kofi-wrap" in:fly={{ y: 20, duration: 300 }} out:fly={{ y: 20, duration: 200 }}>
    <a
      class="kofi-pill"
      href="https://ko-fi.com/thecoffeejesus"
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Buy me a coffee on Ko-fi"
    >
      <span class="kofi-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 8h1a4 4 0 0 1 0 8h-1" />
          <path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4z" />
          <line x1="6" y1="2" x2="6" y2="4" />
          <line x1="10" y1="2" x2="10" y2="4" />
          <line x1="14" y1="2" x2="14" y2="4" />
        </svg>
      </span>
      <span class="kofi-label">Buy me a coffee</span>
    </a>
    <button class="kofi-close" type="button" on:click={dismiss} aria-label="Dismiss support button">
      <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </button>
  </div>
{/if}

<style>
  .kofi-wrap {
    position: fixed;
    bottom: 1.25rem;
    right: 1.25rem;
    z-index: 9998;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  .kofi-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.7rem 1.1rem;
    background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
    color: #0f172a;
    font-size: 0.85rem;
    font-weight: 700;
    text-decoration: none;
    border-radius: 999px;
    box-shadow: 0 8px 24px rgba(245, 158, 11, 0.35), 0 2px 6px rgba(0, 0, 0, 0.3);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    white-space: nowrap;
  }

  .kofi-pill:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(245, 158, 11, 0.45), 0 3px 8px rgba(0, 0, 0, 0.35);
  }

  .kofi-icon {
    display: inline-flex;
    align-items: center;
  }

  .kofi-close {
    width: 26px;
    height: 26px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.85);
    color: #94a3b8;
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 999px;
    cursor: pointer;
    padding: 0;
    transition: color 0.15s ease, background 0.15s ease;
  }

  .kofi-close:hover {
    color: #f1f5f9;
    background: rgba(30, 41, 59, 0.95);
  }

  @media (max-width: 480px) {
    .kofi-wrap {
      bottom: 0.9rem;
      right: 0.9rem;
    }

    .kofi-label {
      display: none;
    }

    .kofi-pill {
      padding: 0.75rem;
    }
  }
</style>
