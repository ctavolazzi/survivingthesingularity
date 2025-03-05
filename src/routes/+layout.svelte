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
    background-color: #111827; /* Dark background */
    color: #e5e7eb; /* Light text */
  }

  .app {
    display: grid;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
  }

  main {
    display: flex;
    flex-direction: column;
    padding: 2rem 1rem;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    box-sizing: border-box;
  }
</style>