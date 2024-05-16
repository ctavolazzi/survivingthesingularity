<script>
  import { fade } from 'svelte/transition';
  import Navbar from './components/Navbar.svelte';
  import About from './components/About.svelte';
  import Contact from './components/Contact.svelte';
  import MyTimeline from './components/MyTimeline.svelte';
  import Countdown from './components/Countdown.svelte';
  import Chat from './components/Chat.svelte';
  import ProgressBar from './components/ProgressBar.svelte';

  let activeTab = 'Home';
  const targetDate = new Date('2027-11-20').getTime();

  const startDate = new Date('1888-11-20').getTime();
  let progressPercentage = 0;
  let countdownInterval;

  function startProgressUpdate() {
    countdownInterval = setInterval(() => {
      updateProgress();
    }, 1000);
  }

  function updateProgress() {
    const currentTime = new Date().getTime();
    const totalDuration = targetDate - startDate;
    progressPercentage = ((currentTime - startDate) / totalDuration) * 100;
    if (progressPercentage >= 100) {
      clearInterval(countdownInterval);
      progressPercentage = 100;
    }
  }

  startProgressUpdate();
</script>

<Navbar on:tabChange="{e => (activeTab = e.detail.tab)}" />

{#if activeTab === 'Home'}
  <div class="home-content" in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
    <h1 class="text-center font-bold text-4xl mt-4 mb-2">Time Left Until the Singularity:</h1>
    <div class="countdown-container mt-1">
      <Countdown {targetDate} />
      <ProgressBar progress={progressPercentage} />
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
    font-size: 4rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
  h2 {
    text-align: center;
    font-size: 2.1rem;
    margin-top: 1rem;
  }

  .home-content {
    padding: 1rem;
  }
  .countdown-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    margin: 0 auto;
    max-width: 600px;
    width: 100%;
    margin-top: 0.25rem;
  }

  .progress-bar-container {
    width: 100%;
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 2.5rem;
    }
    h2 {
      font-size: 1.5rem;
      margin-top: 0.5rem;
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
      margin-top: 0.5rem;
    }
    .countdown-container {
      padding: 0.25rem;
    }
  }
</style>
