<script>
  import Navbar from './components/Navbar.svelte';
  import About from './components/About.svelte';
  import Contact from './components/Contact.svelte';
  let activeTab = 'Home';
  import MyTimeline from './components/MyTimeline.svelte';
  import Countdown from './components/Countdown.svelte';
  const targetDate = new Date('2028-11-06').getTime();
  // Optionally import TypingEffect if needed later
  // import TypingEffect from './components/TypingEffect.svelte';
</script>

<Navbar on:tabChange="{e => activeTab = e.detail.tab}" />

{#if activeTab === 'Home'}
  <div>
    <h1 class="text-center mt-8 font-bold text-4xl">Surviving the Singularity</h1>
    <h3 class="text-center text-xl mt-4">Time Left Until the Singularity:</h3>
    <Countdown {targetDate} />
    <h2 class="text-center text-2xl mt-4">Timeline of Events</h2>
    <MyTimeline />
  </div>
{:else if activeTab === 'About'}
  <About />
{:else if activeTab === 'Contact'}
  <Contact />
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
