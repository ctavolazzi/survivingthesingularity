<script>
  import '../app.css';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import FloatingProgressBar from '$lib/components/FloatingProgressBar.svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { browser } from '$app/environment';
  import { afterNavigate } from '$app/navigation';
  import { onMount } from 'svelte';

  // Force dark mode on the document
  $: if (browser) {
    document.documentElement.classList.add('dark');
  }

  // Scroll to top after navigation - more forceful approach
  afterNavigate(({ from, to }) => {
    if (browser && from && to && from.url.pathname !== to.url.pathname) {
      // Use setTimeout to ensure this runs after the DOM is updated
      setTimeout(() => {
        window.scrollTo(0, 0);
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
      }, 0);
    }
  });

  // Also handle initial page load
  onMount(() => {
    if (browser) {
      window.scrollTo(0, 0);
    }
  });
</script>

<div class="app">
  <!-- Book Revival Banner -->
  <div class="construction-banner">
    <div class="banner-content">
      <span class="banner-pulse"></span>
      <span class="banner-text">
        The book is back. <a href="/sample" class="banner-link">Read the free sample</a> and prepare for what's next.
      </span>
      <span class="banner-pulse"></span>
    </div>
  </div>
  <Navbar />
  <main>
    <slot />
  </main>
  <Footer />
  <FloatingProgressBar />
</div>

<style>
  :global(html, body) {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    background-color: #020617;
    color: #e2e8f0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  .construction-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border-bottom: 1px solid rgba(99, 179, 237, 0.3);
    padding: 0.6rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    z-index: 60;
  }

  .construction-banner::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 200%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(99, 179, 237, 0.05), transparent);
    animation: banner-shimmer 8s infinite linear;
  }

  @keyframes banner-shimmer {
    0% { transform: translateX(-50%); }
    100% { transform: translateX(50%); }
  }

  .banner-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    position: relative;
    z-index: 1;
  }

  .banner-pulse {
    width: 8px;
    height: 8px;
    background: #63b3ed;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
    flex-shrink: 0;
  }

  @keyframes pulse-dot {
    0%, 100% { opacity: 0.4; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
  }

  .banner-text {
    font-size: 0.85rem;
    color: #94a3b8;
    letter-spacing: 0.03em;
    font-weight: 400;
  }

  .banner-text :global(.banner-link) {
    color: #63b3ed;
    text-decoration: underline;
    text-underline-offset: 2px;
    font-weight: 500;
    transition: color 0.2s;
  }

  .banner-text :global(.banner-link:hover) {
    color: #93c5fd;
  }

  .app {
    display: grid;
    grid-template-rows: auto auto 1fr auto;
    min-height: 100vh;
  }

  main {
    display: flex;
    flex-direction: column;
    padding: 1rem 0.5rem;
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  @media (min-width: 768px) {
    main {
      padding: 1.5rem 1rem;
    }
  }
</style>