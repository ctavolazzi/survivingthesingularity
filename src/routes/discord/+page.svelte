<script>
  import DiscordInvite from '$lib/components/DiscordInvite.svelte';
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';

  let showComponent = false;
  let loading = true;

  onMount(() => {
    // Delay to show the component for a more dramatic entrance
    setTimeout(() => {
      showComponent = true;
      loading = false;
    }, 600);
  });
</script>

<style>
  .container {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #050510 0%, #0a0a20 100%);
    padding: 20px;
    position: relative;
  }

  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 30px;
    width: 100%;
    max-width: 800px;
    padding: 2rem;
    border-radius: 8px;
    background-color: rgba(15, 15, 30, 0.6);
    backdrop-filter: blur(5px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }

  h1 {
    color: #00ffff;
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    text-align: center;
    font-size: clamp(2rem, 5vw, 3rem);
    margin: 0;
    font-weight: 700;
  }

  p {
    color: #cccccc;
    text-align: center;
    max-width: 600px;
    line-height: 1.6;
    font-size: clamp(1rem, 2vw, 1.1rem);
  }

  .back-link {
    color: #00ffff;
    text-decoration: none;
    position: absolute;
    top: 20px;
    left: 20px;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0.2);
  }

  .back-link:hover {
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
    background-color: rgba(0, 0, 0, 0.4);
    transform: translateX(-2px);
  }

  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0, 255, 255, 0.1);
    border-left-color: #00ffff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .privacy-notice {
    position: absolute;
    bottom: 10px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 0.7rem;
    color: rgba(204, 204, 204, 0.4);
    padding: 0 20px;
    max-width: 600px;
    margin: 0 auto;
    letter-spacing: 0.02em;
  }

  .privacy-notice a {
    color: rgba(0, 255, 255, 0.4);
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .privacy-notice a:hover {
    color: rgba(0, 255, 255, 0.9);
    text-decoration: underline;
  }

  @media (max-width: 600px) {
    .content {
      padding: 1.5rem;
    }

    .privacy-notice {
      font-size: 0.65rem;
      bottom: 5px;
    }
  }
</style>

<svelte:head>
  <title>Join Our Discord - Surviving the Singularity</title>
  <meta name="description" content="Connect with our community preparing for technological singularity through our Discord server." />
</svelte:head>

<div class="container">
  <a href="/" class="back-link" transition:fade={{ duration: 300 }}>
    <span>←</span> <span>Back to Home</span>
  </a>

  <div class="content" in:fly={{ y: 20, duration: 500, delay: 200 }}>
    <h1 in:fly={{ y: -20, duration: 600, delay: 300 }}>Join Our Community</h1>
    <p in:fly={{ y: 20, duration: 600, delay: 400 }}>
      Connect with like-minded individuals who are preparing for technological singularity.
      Share insights, strategies, and build a network that will help you navigate the future.
    </p>

    {#if loading}
      <div class="loading">
        <div class="spinner"></div>
      </div>
    {:else if showComponent}
      <div in:fade={{ duration: 400 }}>
        <DiscordInvite />
      </div>
    {/if}
  </div>

  <div class="privacy-notice" in:fade={{ duration: 300, delay: 800 }}>
    By joining, you accept Discord's <a href="https://discord.com/privacy" target="_blank" rel="noopener noreferrer">Privacy Policy</a> and our <a href="/terms" rel="noopener noreferrer">Terms</a>.
  </div>
</div>