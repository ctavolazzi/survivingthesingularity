<script>
  import '../app.css';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import CookieConsent from '$lib/components/CookieConsent.svelte';
  import ToastContainer from '$lib/components/ToastContainer.svelte';
  import CommandPalette from '$lib/components/CommandPalette.svelte';
  import WhiteRabbitPanel from '$lib/components/WhiteRabbitPanel.svelte';
  import { createRabbit } from '$lib/debug/white-rabbit.js';
  import { browser } from '$app/environment';
  import { afterNavigate, beforeNavigate } from '$app/navigation';
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';

  // Release the session rabbit — tracks the entire user session
  let sessionRabbit = null;

  export let data;

  let commandPaletteOpen = false;
  let navigating = false;

  // Force dark mode
  $: if (browser) {
    document.documentElement.classList.add('dark');
  }

  beforeNavigate(() => {
    navigating = true;
  });

  afterNavigate(({ from, to }) => {
    navigating = false;
    if (browser && from && to && from.url.pathname !== to.url.pathname) {
      if (sessionRabbit) {
        sessionRabbit.watchNavigation(from.url.pathname, to.url.pathname);
      }
      setTimeout(() => {
        window.scrollTo(0, 0);
      }, 0);
    }
  });

  onMount(() => {
    if (browser) {
      sessionRabbit = createRabbit('session', { userAgent: navigator.userAgent });
      sessionRabbit.mark('app-mounted');
      sessionRabbit.info('Session started', { path: window.location.pathname });
      window.scrollTo(0, 0);
    }
  });
</script>

<div class="app">
  <Navbar user={data?.user} />

  <!-- Page transition loading bar -->
  {#if navigating}
    <div class="page-loading-bar" in:fade={{ duration: 100 }}>
      <div class="page-loading-fill"></div>
    </div>
  {/if}

  <main>
    <slot />
  </main>
  <Footer />
  <CookieConsent />
  <ToastContainer />
  <CommandPalette bind:open={commandPaletteOpen} />
  <WhiteRabbitPanel />
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

  .app {
    display: grid;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
  }

  main {
    display: flex;
    flex-direction: column;
    width: 100%;
    box-sizing: border-box;
  }

  /* Page loading bar */
  .page-loading-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    z-index: 9999;
    background: transparent;
  }

  .page-loading-fill {
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #f97316, #f59e0b);
    background-size: 200% 100%;
    animation: loading-shimmer 1s ease-in-out infinite, loading-grow 2s ease forwards;
    border-radius: 0 1px 1px 0;
    box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
  }

  @keyframes loading-grow {
    0% { width: 0%; }
    20% { width: 30%; }
    50% { width: 60%; }
    80% { width: 85%; }
    100% { width: 95%; }
  }

  @keyframes loading-shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }

  /* Global micro-interaction utilities */
  :global(.magnetic-hover) {
    transition: transform 0.2s ease;
  }

  :global(.magnetic-hover:hover) {
    transform: translateY(-2px);
  }

  /* Global button ripple effect */
  :global(.ripple) {
    position: relative;
    overflow: hidden;
  }

  :global(.ripple::after) {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at var(--ripple-x, 50%) var(--ripple-y, 50%), rgba(255,255,255,0.15) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.3s;
  }

  :global(.ripple:active::after) {
    opacity: 1;
  }

  /* Smooth link underline animation */
  :global(.link-fancy) {
    text-decoration: none;
    background-image: linear-gradient(#f59e0b, #f59e0b);
    background-size: 0% 1px;
    background-repeat: no-repeat;
    background-position: left bottom;
    transition: background-size 0.3s ease;
  }

  :global(.link-fancy:hover) {
    background-size: 100% 1px;
  }

  /* Card tilt effect */
  :global(.tilt-card) {
    transition: transform 0.3s ease;
    transform-style: preserve-3d;
    perspective: 800px;
  }

  :global(.tilt-card:hover) {
    transform: perspective(800px) rotateX(2deg) rotateY(-2deg) translateY(-4px);
    box-shadow: 8px 8px 30px rgba(0, 0, 0, 0.3);
  }

  /* Focus ring */
  :global(*:focus-visible) {
    outline: 2px solid rgba(245, 158, 11, 0.5);
    outline-offset: 2px;
    border-radius: 4px;
  }

  /* Selection color */
  :global(::selection) {
    background: rgba(245, 158, 11, 0.25);
    color: #f1f5f9;
  }

  /* Scrollbar styling */
  :global(::-webkit-scrollbar) {
    width: 6px;
  }

  :global(::-webkit-scrollbar-track) {
    background: transparent;
  }

  :global(::-webkit-scrollbar-thumb) {
    background: rgba(148, 163, 184, 0.1);
    border-radius: 3px;
  }

  :global(::-webkit-scrollbar-thumb:hover) {
    background: rgba(148, 163, 184, 0.2);
  }
</style>
