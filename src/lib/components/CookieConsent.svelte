<script>
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';

  let showBanner = false;

  onMount(() => {
    if (browser) {
      const consent = localStorage.getItem('sts-cookie-consent');
      if (!consent) {
        // Small delay so it doesn't flash on load
        setTimeout(() => { showBanner = true; }, 1500);
      }
    }
  });

  function accept() {
    if (browser) {
      localStorage.setItem('sts-cookie-consent', JSON.stringify({
        accepted: true,
        timestamp: new Date().toISOString(),
        version: '1.0'
      }));
    }
    showBanner = false;
  }

  function decline() {
    if (browser) {
      localStorage.setItem('sts-cookie-consent', JSON.stringify({
        accepted: false,
        timestamp: new Date().toISOString(),
        version: '1.0'
      }));
    }
    showBanner = false;
  }
</script>

{#if showBanner}
  <div class="consent-wrapper" transition:slide={{ duration: 300 }}>
    <div class="consent-inner">
      <div class="consent-text">
        <p class="consent-title">This site uses cookies</p>
        <p class="consent-desc">
          We use essential cookies for authentication and preferences. No tracking, no ads, no third-party data sharing. Your data stays yours.
          <a href="/policies" class="consent-link">Read our privacy policy</a>
        </p>
      </div>
      <div class="consent-actions">
        <button class="consent-btn consent-btn-accept" on:click={accept}>Accept</button>
        <button class="consent-btn consent-btn-decline" on:click={decline}>Decline</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .consent-wrapper {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 100;
    padding: 1rem;
    pointer-events: none;
  }

  .consent-inner {
    max-width: 680px;
    margin: 0 auto;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 -4px 40px rgba(0, 0, 0, 0.4);
    pointer-events: all;
  }

  .consent-text {
    flex: 1;
  }

  .consent-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0 0 0.25rem 0;
  }

  .consent-desc {
    font-size: 0.8rem;
    color: #94a3b8;
    line-height: 1.5;
    margin: 0;
  }

  .consent-link {
    color: #f59e0b;
    text-decoration: none;
  }

  .consent-link:hover {
    text-decoration: underline;
  }

  .consent-actions {
    display: flex;
    gap: 0.5rem;
    flex-shrink: 0;
  }

  .consent-btn {
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
  }

  .consent-btn-accept {
    background: #f59e0b;
    color: #0f172a;
  }

  .consent-btn-accept:hover {
    background: #fbbf24;
  }

  .consent-btn-decline {
    background: rgba(255, 255, 255, 0.05);
    color: #94a3b8;
    border: 1px solid rgba(148, 163, 184, 0.1);
  }

  .consent-btn-decline:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
  }

  @media (max-width: 640px) {
    .consent-inner {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }

    .consent-actions {
      justify-content: flex-end;
    }
  }
</style>
