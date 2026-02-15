<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';

  // Target: The window of maximum leverage — before AI fully commoditizes content creation
  const TARGET_DATE = new Date('2030-01-01T00:00:00Z');

  let now = new Date();
  let interval;

  onMount(() => {
    interval = setInterval(() => {
      now = new Date();
    }, 1000);
  });

  onDestroy(() => {
    if (interval) clearInterval(interval);
  });

  $: diff = TARGET_DATE.getTime() - now.getTime();
  $: days = Math.max(0, Math.floor(diff / (1000 * 60 * 60 * 24)));
  $: hours = Math.max(0, Math.floor((diff / (1000 * 60 * 60)) % 24));
  $: minutes = Math.max(0, Math.floor((diff / (1000 * 60)) % 60));
  $: seconds = Math.max(0, Math.floor((diff / 1000) % 60));

  function pad(n) { return String(n).padStart(2, '0'); }
</script>

<div class="urgency-banner">
  <div class="banner-inner">
    <div class="banner-left">
      <span class="banner-pulse"></span>
      <span class="banner-label">Opportunity Window</span>
    </div>
    <div class="banner-countdown">
      <div class="count-block">
        <span class="count-num">{days}</span>
        <span class="count-unit">days</span>
      </div>
      <span class="count-sep">:</span>
      <div class="count-block">
        <span class="count-num">{pad(hours)}</span>
        <span class="count-unit">hrs</span>
      </div>
      <span class="count-sep">:</span>
      <div class="count-block">
        <span class="count-num">{pad(minutes)}</span>
        <span class="count-unit">min</span>
      </div>
      <span class="count-sep">:</span>
      <div class="count-block">
        <span class="count-num count-seconds">{pad(seconds)}</span>
        <span class="count-unit">sec</span>
      </div>
    </div>
    <div class="banner-right">
      <span class="banner-note">Best time to start is now</span>
    </div>
  </div>
</div>

<style>
  .urgency-banner {
    background: linear-gradient(90deg, #0a0a0a 0%, #0f0a00 50%, #0a0a0a 100%);
    border-bottom: 1px solid rgba(245, 158, 11, 0.12);
    padding: 0.5rem 1rem;
    position: relative;
    overflow: hidden;
  }

  .urgency-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.03), transparent);
    animation: sweep 4s ease-in-out infinite;
  }

  @keyframes sweep {
    0%, 100% { transform: translateX(-100%); }
    50% { transform: translateX(100%); }
  }

  .banner-inner {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    position: relative;
  }

  .banner-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .banner-pulse {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #f59e0b;
    animation: pulse 1.5s ease-in-out infinite;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
  }

  @keyframes pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
  }

  .banner-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: #f59e0b;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-family: 'JetBrains Mono', monospace;
  }

  .banner-countdown {
    display: flex;
    align-items: center;
    gap: 0.15rem;
  }

  .count-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 36px;
  }

  .count-num {
    font-size: 1.1rem;
    font-weight: 800;
    color: #fafafa;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
    line-height: 1;
  }

  .count-seconds {
    color: #f59e0b;
  }

  .count-unit {
    font-size: 0.5rem;
    color: #525252;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
  }

  .count-sep {
    color: #404040;
    font-size: 1rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    margin-top: -0.6rem;
  }

  .banner-right {
    display: flex;
    align-items: center;
  }

  .banner-note {
    font-size: 0.6rem;
    color: #525252;
    font-weight: 500;
    white-space: nowrap;
  }

  @media (max-width: 640px) {
    .banner-left, .banner-right {
      display: none;
    }

    .banner-inner {
      gap: 0.5rem;
    }
  }
</style>
