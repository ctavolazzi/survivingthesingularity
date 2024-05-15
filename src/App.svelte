<script>
  import { fade } from 'svelte/transition';
  import Navbar from './components/Navbar.svelte';
  import About from './components/About.svelte';
  import Contact from './components/Contact.svelte';
  import MyTimeline from './components/MyTimeline.svelte';
  import Countdown from './components/Countdown.svelte';
  import Chat from './components/Chat.svelte';
  let activeTab = 'Home'; // This will ensure 'Home' content is visible on initial load
  const targetDate = new Date('2028-11-06').getTime();
</script>

<Navbar on:tabChange="{e => (activeTab = e.detail.tab)}" />

<!-- Direct use of activeTab for conditional rendering and animation -->
{#if activeTab === 'Home'}
  <div class="home-content" in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <h1 class="text-center mt-8 font-bold text-4xl">Time Left Until the Singularity:</h1>
    <div class="countdown-container">
      <Countdown {targetDate} />
    </div>
    <h2 class="text-center text-2xl mt-4">Timeline of Events</h2>
    <MyTimeline />
  </div>
{/if}
{#if activeTab === 'About'}
  <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <About />
  </div>
{/if}
{#if activeTab === 'Contact'}
  <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <Contact />
  </div>
{/if}
{#if activeTab === 'Chat'}
  <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <Chat />
  </div>
{/if}

<style>
  h1 {
    text-align: center;
    margin-top: 2rem;
    font-size: 4rem;
  }
  h2 {
    text-align: center;
    font-size: 2.1rem;
  }
  h3 {
    text-align: center;
    font-size: 1.25rem;
  }
  .home-content {
    padding: 1rem;
  }
  .countdown-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
    margin: 0 auto;
    max-width: 100%;
  }
  @media (max-width: 768px) {
    h1 {
      font-size: 2.5rem;
    }
    h2 {
      font-size: 1.5rem;
    }
    .countdown-container {
      padding: 0.5rem;
    }
  }
  @media (max-width: 480px) {
    h1 {
      font-size: 2rem;
    }
    h2 {
      font-size: 1.25rem;
    }
    .countdown-container {
      padding: 0.25rem;
    }
  }
</style>
