<script>
  import { onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';
  export let targetDate;

  let isLoading = true;
  let currentYears = 0;
  let currentDays = 0;
  let currentHours = 0;
  let currentMinutes = 0;
  let currentSeconds = 0;
  let years = 0;
  let days = 0;
  let hours = 0;
  let minutes = 0;
  let seconds = 0;
  let countdownInterval;

  function startCountdown() {
    countdownInterval = setInterval(() => {
      updateCountdown();
      isLoading = false; // Set isLoading to false after the first update
    }, 1000);
  }

  function updateCountdown() {
    if (!targetDate || isNaN(targetDate)) {
      clearInterval(countdownInterval);
      years = 0;
      days = 0;
      hours = 0;
      minutes = 0;
      seconds = 0;
      console.error('Invalid targetDate provided to Countdown component');
      return;
    }

    const currentTime = new Date().getTime();
    const difference = targetDate - currentTime;

    if (difference <= 0) {
      clearInterval(countdownInterval);
      years = 0;
      days = 0;
      hours = 0;
      minutes = 0;
      seconds = 0;
      return;
    }

    const totalDays = Math.floor(difference / (1000 * 60 * 60 * 24));
    years = Math.floor(totalDays / 365);
    days = totalDays % 365;
    hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    seconds = Math.floor((difference % (1000 * 60)) / 1000);

    // Update the current values
    currentYears = years;
    currentDays = days;
    currentHours = hours;
    currentMinutes = minutes;
    currentSeconds = seconds;
  }

  onDestroy(() => {
    clearInterval(countdownInterval);
  });

  startCountdown();
</script>

{#if isLoading}
  <div class="loading-container">
    <span class="loading-icon">&#9679;</span> Loading...
  </div>
{:else}
  <div in:fade={{ duration: 500 }} out:fade={{ duration: 300 }} class="countdown-container">
    <div class="countdown-item">
      <span class="countdown-value">{currentYears}</span>
      <span class="countdown-label">years</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{currentDays}</span>
      <span class="countdown-label">days</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{currentHours}</span>
      <span class="countdown-label">hours</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{currentMinutes}</span>
      <span class="countdown-label">min</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{currentSeconds}</span>
      <span class="countdown-label">sec</span>
    </div>
  </div>
{/if}

<style>
  .countdown-container, .loading-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    height: auto; /* Adjust this value to match the desired height */
    padding: 1rem; /* Add padding to give more room on the sides */
    flex-wrap: wrap; /* Allow items to wrap on smaller screens */
  }

  .countdown-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center; /* Center items vertically */
    padding: 0.5rem;
    color: #000000;
    border-radius: 4px;
    flex: 1; /* Allow items to grow and shrink */
    max-width: 100px; /* Limit the maximum width of each item */
  }

  .countdown-value {
    font-size: 3rem; /* Increased font size for better readability */
    font-weight: bold;
    width: 100%; /* Use 100% width for better scaling */
    text-align: center;
  }

  .countdown-label {
    font-size: 1rem; /* Increased font size for labels */
    text-transform: uppercase;
    text-align: center;
  }

  .loading-container {
    align-items: center;
    font-size: 1.2rem;
  }

  .loading-icon {
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 0.2;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.2;
    }
  }

  /* Media queries for responsive design */
  @media (max-width: 600px) {
    .countdown-value {
      font-size: 2.5rem; /* Adjusted font size for smaller screens */
    }

    .countdown-label {
      font-size: 0.8rem; /* Adjust label size for smaller screens */
    }

    .countdown-item {
      max-width: 80px; /* Further limit the max width on small screens */
    }
  }

  @media (max-width: 400px) {
    .countdown-value {
      font-size: 2rem; /* Further reduce font size for very small screens */
    }

    .countdown-label {
      font-size: 0.7rem; /* Further adjust label size for very small screens */
    }

    .countdown-item {
      max-width: 60px; /* Further limit the max width on very small screens */
    }
  }
</style>
