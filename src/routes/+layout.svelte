<script>
  import '../app.css';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import FloatingProgressBar from '$lib/components/FloatingProgressBar.svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { base } from '$app/paths';

  onMount(() => {
    if (browser) {
      const savedDarkMode = localStorage.getItem('darkMode') === 'true';
      darkMode.set(savedDarkMode);
    }
  });

  $: if (browser) {
    document.documentElement.classList.toggle('dark', $darkMode);
  }
</script>

<svelte:head>
  <meta property="og:image" content="{base}/sts-welcome.png" />
  <meta property="og:image:width" content="1280" />
  <meta property="og:image:height" content="720" />
  <meta property="og:image:alt" content="Surviving the Singularity Welcome Image" />
  <meta property="og:title" content="Surviving the Singularity" />
  <meta property="og:description" content="Surviving the Singularity is a workbook that helps you navigate the future of humanity." />
  <meta property="og:url" content="https://survivingthesingularity.com" />
  <meta property="og:type" content="website" />
</svelte:head>

<div class="app bg-white dark:bg-gray-900 min-h-screen">
  <FloatingProgressBar />
  <Navbar />
  <main class="container mx-auto px-4 py-8">
    <slot />
  </main>
  <Footer />
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