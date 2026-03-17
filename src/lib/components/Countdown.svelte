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
</div>

<style>
  .countdown-wrapper {
    width: 100%;
    padding: 2rem 0;
  }

  .countdown-header {
    text-align: center;
    font-weight: 700;
    margin: 0 0 2rem 0;
    font-size: clamp(1.1rem, 3vw, 1.5rem);
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    display: block;
  }

  .countdown-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    padding: 0;
    max-width: 100%;
    box-sizing: border-box;
  }

  .countdown-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    max-width: 120px;
  }

  .countdown-box {
    background: rgba(30, 41, 59, 0.6);
    border-radius: 14px;
    padding: 1rem 0.75rem;
    min-width: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid rgba(148, 163, 184, 0.08);
    transition: all 0.3s ease;
  }

  .countdown-box:hover {
    transform: translateY(-3px);
    border-color: rgba(99, 179, 237, 0.2);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  }

  .countdown-value {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 700;
    text-align: center;
    min-width: 1.5ch;
    color: #f1f5f9;
    letter-spacing: -0.02em;
    line-height: 1;
  }

  .countdown-separator {
    font-size: clamp(1.5rem, 3vw, 2.5rem);
    font-weight: 300;
    color: rgba(148, 163, 184, 0.3);
    margin-top: -1.5rem;
  }

  .countdown-label {
    font-size: clamp(0.6rem, 1vw, 0.75rem);
    text-transform: uppercase;
    text-align: center;
    color: #64748b;
    font-weight: 600;
    margin-top: 0.75rem;
    letter-spacing: 0.15em;
  }

  .countdown-value.placeholder {
    opacity: 0.3;
  }

  @media (max-width: 768px) {
    .countdown-box {
      min-width: 60px;
      padding: 0.75rem 0.5rem;
    }

    .countdown-separator {
      margin-top: -1rem;
    }
  }

  @media (max-width: 480px) {
    .countdown-header {
      font-size: clamp(0.85rem, 3vw, 1.1rem);
      margin-bottom: 1.5rem;
    }

    .countdown-container {
      gap: 0.3rem;
    }

    .countdown-box {
      min-width: 48px;
      padding: 0.6rem 0.3rem;
      border-radius: 10px;
    }

    .countdown-value {
      font-size: clamp(1.4rem, 4vw, 2rem);
    }

    .countdown-separator {
      font-size: clamp(1rem, 2.5vw, 1.5rem);
      margin-top: -0.75rem;
    }

    .countdown-label {
      font-size: 0.55rem;
      margin-top: 0.5rem;
    }
  }
</style>