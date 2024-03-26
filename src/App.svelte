<script>
  import { fade } from 'svelte/transition';
  import Navbar from './components/Navbar.svelte';
  import About from './components/About.svelte';
  import Contact from './components/Contact.svelte';
  import MyTimeline from './components/MyTimeline.svelte';
  import Countdown from './components/Countdown.svelte';
  let activeTab = 'Home'; // This will ensure 'Home' content is visible on initial load
  const targetDate = new Date('2028-11-06').getTime();
</script>

<Navbar on:tabChange="{e => (activeTab = e.detail.tab)}" />

<!-- Direct use of activeTab for conditional rendering and animation -->
{#if activeTab === 'Home'}
  <div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <h1 class="text-center mt-8 font-bold text-4xl">Time Left Until the Singularity:</h1>
    <Countdown {targetDate} />
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
</style>
