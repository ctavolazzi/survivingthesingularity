<script>
  import { onMount, onDestroy, tick } from 'svelte';
  import { fade, scale } from 'svelte/transition';

  let years = 0, days = 0, hours = 0, minutes = 0, seconds = 0;
  let countdownInterval;
  let loading = true;
  export let headerText = "Time Left Until the Singularity";
  export let targetDate = new Date("2027-11-20T23:59:59").getTime();

  function calculateTimeLeft() {
    const currentTime = new Date().getTime();
    const difference = targetDate - currentTime;

    if (difference <= 0) {
      return { years: 0, days: 0, hours: 0, minutes: 0, seconds: 0 };
    }

    const totalDays = Math.floor(difference / (1000 * 60 * 60 * 24));
    return {
      years: Math.floor(totalDays / 365),
      days: totalDays % 365,
      hours: Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
      minutes: Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60)),
      seconds: Math.floor((difference % (1000 * 60)) / 1000)
    };
  }

  function updateCountdown() {
    const timeLeft = calculateTimeLeft();
    years = timeLeft.years;
    days = timeLeft.days;
    hours = timeLeft.hours;
    minutes = timeLeft.minutes;
    seconds = timeLeft.seconds;
  }

  async function initializeCountdown() {
    updateCountdown(); // Set initial values
    await tick(); // Ensure DOM is updated
    await new Promise(resolve => setTimeout(resolve, 500)); // Brief delay for effect
    loading = false; // Trigger transition
    countdownInterval = setInterval(updateCountdown, 1000);
  }

  onMount(initializeCountdown);

  onDestroy(() => {
    clearInterval(countdownInterval);
  });

  $: timeUnits = [
    { label: 'years', value: years },
    { label: 'days', value: days },
    { label: 'hours', value: hours },
    { label: 'minutes', value: minutes },
    { label: 'seconds', value: seconds }
  ];
</script>

<div class="countdown-header">
  {headerText}
</div>

<div class="countdown-container">
  {#each timeUnits as { label, value }, i}
    <div class="countdown-item">
      {#if loading}
        <span class="countdown-value placeholder">-</span>
        <span class="countdown-label">{label}</span>
      {:else}
        <span
          class="countdown-value"
          in:scale={{
            duration: 300,
            delay: i * 100,
            start: 0.5,
            opacity: 0
          }}
        >{value}</span>
        <span class="countdown-label">{label}</span>
      {/if}
    </div>
  {/each}
</div>

<style>
  .countdown-header {
    text-align: center;
    font-weight: bold;
    margin: 0 0 0.5rem 0;
    font-size: 2rem;
    color: var(--color-text-primary);
    text-shadow: 0 0 15px rgba(255, 255, 255, 0.15);
  }

  .countdown-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    height: auto;
    padding: 0.5rem;
    white-space: nowrap;
    max-width: 100vw;
    box-sizing: border-box;
    overflow: hidden;
  }

  .countdown-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.2rem;
    flex: 1;
    min-width: 0;
  }

  .countdown-value {
    font-family: 'Courier New', Courier, monospace;
    font-size: 5.5vw;
    font-weight: 900;
    text-align: center;
    min-width: 5vw;
    color: #ffffff;
    text-shadow:
      0 0 25px rgba(255, 255, 255, 0.3),
      0 0 50px rgba(255, 255, 255, 0.15);
    letter-spacing: 0.02em;
    line-height: 1;
  }

  .countdown-value:not(.placeholder) {
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0% {
      text-shadow:
        0 0 25px rgba(255, 255, 255, 0.3),
        0 0 50px rgba(255, 255, 255, 0.15);
    }
    50% {
      text-shadow:
        0 0 35px rgba(255, 255, 255, 0.4),
        0 0 70px rgba(255, 255, 255, 0.2);
    }
    100% {
      text-shadow:
        0 0 25px rgba(255, 255, 255, 0.3),
        0 0 50px rgba(255, 255, 255, 0.15);
    }
  }

  .countdown-label {
    font-size: 1.2vw;
    text-transform: uppercase;
    text-align: center;
    color: var(--color-text-secondary);
    font-weight: bold;
    opacity: 0.9;
    margin-top: 0.15rem;
    letter-spacing: 0.05em;
  }

  .countdown-value.placeholder {
    opacity: 0.5;
  }

  /* Media queries for responsive design */
  @media (max-width: 600px) {
    .countdown-container {
      gap: 0.75rem;
    }

    .countdown-value {
      font-size: 7.5vw;
      min-width: 7vw;
    }

    .countdown-label {
      font-size: 2vw;
      margin-top: 0.1rem;
    }
  }

  @media (max-width: 400px) {
    .countdown-container {
      gap: 0.5rem;
    }

    .countdown-value {
      font-size: 8.5vw;
      min-width: 8vw;
    }

    .countdown-label {
      font-size: 2.8vw;
    }
  }
</style>