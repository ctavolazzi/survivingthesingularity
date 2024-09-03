<script>
  import '../app.css';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import FloatingProgressBar from '$lib/components/FloatingProgressBar.svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  function initDarkMode() {
    if (browser) {
      const savedDarkMode = localStorage.getItem('darkMode');
      if (savedDarkMode === 'true') {
        darkMode.set(true);
      } else {
        darkMode.set(false);
      }
    }
  }

  onMount(initDarkMode);

  $: if (browser) {
    if ($darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('darkMode', 'true');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('darkMode', 'false');
    }
  }
</script>

<div class:dark={$darkMode}>
  <div class="app bg-white dark:bg-gray-900 min-h-screen">
    <FloatingProgressBar />
    <Navbar />
    <main class="container mx-auto px-4 py-8">
      <slot />
    </main>
    <Footer />
  </div>
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  main {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    width: 100%;
    max-width: 64rem;
    margin: 0 auto;
    box-sizing: border-box;
  }
</style>