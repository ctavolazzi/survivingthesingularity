<script>
    import { onDestroy } from 'svelte';
  
    export let targetDate;
  
    let years = 0;
    let days = 0;
    let hours = 0;
    let minutes = 0;
    let seconds = 0;
  
    let countdownInterval;
  
    function startCountdown() {
      countdownInterval = setInterval(updateCountdown, 1000);
    }
  
    function updateCountdown() {
        if (!targetDate || isNaN(targetDate)) {
            clearInterval(countdownInterval);
            years = 0;
            days = 0;
            hours = 0;
            minutes = 0;
            seconds = 0;
            years = 0;
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
            years = 0;
            return;
        }

        const totalDays = Math.floor(difference / (1000 * 60 * 60 * 24));
        years = Math.floor(totalDays / 365);
        days = totalDays % 365;
        hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        seconds = Math.floor((difference % (1000 * 60)) / 1000);
        }
  
    onDestroy(() => {
      clearInterval(countdownInterval);
    });
  
    startCountdown();
  </script>
  
  <div class="countdown-container">
    <div class="countdown-item">
      <span class="countdown-value">{years}</span>
      <span class="countdown-label">years</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{days}</span>
      <span class="countdown-label">days</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{hours}</span>
      <span class="countdown-label">hours</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{minutes}</span>
      <span class="countdown-label">min</span>
    </div>
    <div class="countdown-item">
      <span class="countdown-value">{seconds}</span>
      <span class="countdown-label">sec</span>
    </div>
  </div>
  
  <style>
    .countdown-container {
      display: flex;
      justify-content: center;
      gap: 1rem;
    }
  
    .countdown-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 0.5rem;
      /* background-color: #333; */
      color: #000000;
      border-radius: 4px;
    }
  
    .countdown-value {
      font-size: 2rem;
      font-weight: bold;
    }
  
    .countdown-label {
      font-size: 0.8rem;
      text-transform: uppercase;
    }
  </style>