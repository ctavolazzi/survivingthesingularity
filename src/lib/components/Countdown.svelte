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
  
  <div class="countdown-header">
    Time Left Until the Singularity
  </div>
  
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
    .countdown-header {
      text-align: center;
      font-weight: bold;
      margin-bottom: 1rem;
      font-size: 2.4rem;
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
    }
  
    .countdown-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 0.2rem;
      color: #000000;
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
    }
  
    .countdown-label {
      font-size: 2vw;
      text-transform: uppercase;
      text-align: center;
    }
  
    .loading-container {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      width: 100%; /* Ensure the loading container takes full width */
      height: 100%; /* Ensure the loading container takes full height */
    }
  
    .loading-icon {
      animation: pulse 1s infinite;
      margin-right: 0.5rem;
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