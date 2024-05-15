<script>
  import { fade } from 'svelte/transition';
  import Navbar from './components/Navbar.svelte';
  import About from './components/About.svelte';
  import Contact from './components/Contact.svelte';
  import MyTimeline from './components/MyTimeline.svelte';
  import Countdown from './components/Countdown.svelte';
<<<<<<< HEAD
  import Chat from './components/Chat.svelte';
=======
>>>>>>> 14b9fbe9146cdd5bd3fa3ef8f1194d4bb09b6695
  let activeTab = 'Home'; // This will ensure 'Home' content is visible on initial load
  const targetDate = new Date('2028-11-06').getTime();
</script>

<Navbar on:tabChange="{e => (activeTab = e.detail.tab)}" />

<!-- Direct use of activeTab for conditional rendering and animation -->
{#if activeTab === 'Home'}
<<<<<<< HEAD
  <div class="home-content" in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <h1 class="text-center mt-8 font-bold text-4xl">Time Left Until the Singularity:</h1>
    <div class="countdown-container">
      <Countdown {targetDate} />
    </div>
=======
  <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <h1 class="text-center mt-8 font-bold text-4xl">Time Left Until the Singularity:</h1>
    <Countdown {targetDate} />
>>>>>>> 14b9fbe9146cdd5bd3fa3ef8f1194d4bb09b6695
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
<<<<<<< HEAD
{#if activeTab === 'Chat'}
  <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <Chat />
  </div>
{/if}
=======


>>>>>>> 14b9fbe9146cdd5bd3fa3ef8f1194d4bb09b6695

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
<<<<<<< HEAD
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
=======
>>>>>>> 14b9fbe9146cdd5bd3fa3ef8f1194d4bb09b6695
</style>
