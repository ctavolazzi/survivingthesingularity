<script>
  import { onMount, onDestroy, tick } from 'svelte';
  import { fade, scale } from 'svelte/transition';
  export let targetDate;

  let years = 0, days = 0, hours = 0, minutes = 0, seconds = 0;
  let countdownInterval;
  let loading = true;

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
  Time Left Until the Singularity
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
    margin-bottom: 1rem;
    font-size: 2.4rem;
    color: var(--color-text-primary);
  }

  .countdown-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    height: auto;
    padding: 1rem;
    white-space: nowrap;
    max-width: 100vw;
    box-sizing: border-box;
    overflow: hidden;
    background-color: var(--color-surface);
    border-radius: 4px;
  }

  .countdown-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.2rem;
    color: var(--color-text-secondary);
    border-radius: 4px;
    flex: 1; /* Ensure items are evenly spaced */
    min-width: 0; /* Prevent flex items from overflowing */
  }

  .countdown-value {
    font-family: 'Courier New', Courier, monospace;
    font-size: 5vw;
    font-weight: bold;
    text-align: center;
    min-width: 5vw; /* Ensure consistent width to prevent shifting */
    color: var(--color-text-primary);
  }

  .countdown-label {
    font-size: 2vw;
    text-transform: uppercase;
    text-align: center;
    color: var(--color-text-secondary);
  }

  .countdown-value.placeholder {
    opacity: 0.5;
  }

  /* Media queries for responsive design */
  @media (max-width: 600px) {
    .countdown-value {
      font-size: 7vw;
      min-width: 7vw;
    }

    .countdown-label {
      font-size: 3vw;
    }
  }

  @media (max-width: 400px) {
    .countdown-value {
      font-size: 8vw;
      min-width: 8vw;
    }

    .countdown-label {
      font-size: 4vw;
    }
  }
</style>