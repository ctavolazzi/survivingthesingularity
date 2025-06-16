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
    loading = false; // Trigger transition immediately
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

<div class="countdown-wrapper">
  <h3 class="countdown-header">{headerText}</h3>

  <div class="countdown-container">
    {#each timeUnits as { label, value }, i}
      <div class="countdown-item">
        <div class="countdown-box">
          {#if loading}
            <span class="countdown-value placeholder">-</span>
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
          {/if}
        </div>
        <span class="countdown-label">{label}</span>
      </div>
      {#if i < timeUnits.length - 1}
        <div class="countdown-separator">:</div>
      {/if}
    {/each}
  </div>
  <p class="estimate-note">Estimate based on predictions from industry leaders</p>
</div>

<style>
  .countdown-wrapper {
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .countdown-header {
    text-align: center;
    font-weight: bold;
    margin: 0.5rem 0 1.5rem 0;
    font-size: clamp(1.5rem, 5vw, 3rem);
    color: #FF9933;
    white-space: nowrap !important;
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    letter-spacing: -0.01em;
    display: block;
  }

  .countdown-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 0.25rem;
    height: auto;
    padding: 1.5rem 0.5rem;
    white-space: nowrap;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
  }

  .countdown-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.25rem;
    flex: 1;
  }

  .countdown-box {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 0.75rem 0.5rem;
    min-width: 70px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: transform 0.2s ease;
  }

  .countdown-box:hover {
    transform: translateY(-2px);
  }

  .countdown-value {
    font-family: 'Courier New', Courier, monospace;
    font-size: clamp(1.75rem, 4vw, 3rem);
    font-weight: 900;
    text-align: center;
    min-width: 1.2ch;
    color: #ffffff;
    letter-spacing: 0.02em;
    line-height: 1;
  }

  .countdown-separator {
    font-size: clamp(1.75rem, 4vw, 3rem);
    font-weight: bold;
    color: rgba(255, 255, 255, 0.5);
    margin-top: -1.5rem;
  }

  .countdown-label {
    font-size: clamp(0.7rem, 1vw, 0.875rem);
    text-transform: uppercase;
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 600;
    margin-top: 0.75rem;
    letter-spacing: 0.1em;
  }

  .countdown-value.placeholder {
    opacity: 0.5;
  }

  .estimate-note {
    font-size: 0.65rem;
    text-align: center;
    color: #9ca3af;
    margin-top: -0.25rem;
  }

  /* Media queries for responsive design */
  @media (max-width: 768px) {
    .countdown-container {
      padding: 1rem 0.5rem;
    }

    .countdown-header {
      margin-bottom: 1.5rem;
      font-size: clamp(1.25rem, 4.5vw, 2.5rem);
      letter-spacing: -0.02em;
    }

    .countdown-box {
      min-width: 50px;
      padding: 0.5rem 0.25rem;
    }

    .countdown-separator {
      margin-top: -1rem;
    }
  }

  @media (max-width: 480px) {
    .countdown-header {
      font-size: clamp(1.2rem, 4vw, 1.75rem);
      letter-spacing: -0.03em;
      white-space: nowrap !important;
      overflow: visible; /* Ensure text is visible */
      margin-bottom: 1.8rem; /* Add more space below the header */
    }

    .countdown-container {
      gap: 0.2rem;
      padding: 0.5rem 0.25rem;
    }

    .countdown-item {
      padding: 0.25rem 0.1rem;
      min-width: auto;
    }

    .countdown-box {
      min-width: 42px;
      padding: 0.6rem 0.25rem;
      border-radius: 8px;
    }

    .countdown-value {
      font-size: clamp(1.4rem, 3vw, 2rem);
    }

    .countdown-separator {
      font-size: clamp(1.25rem, 3vw, 2rem);
      margin-top: -0.75rem;
    }

    .countdown-label {
      font-size: clamp(0.5rem, 0.8vw, 0.75rem);
      margin-top: 0.25rem;
    }
  }
</style>