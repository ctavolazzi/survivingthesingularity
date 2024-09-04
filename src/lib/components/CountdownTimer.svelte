<script>
    import { onMount, onDestroy } from 'svelte';

    // Accept custom text and end date as props, with defaults
    export let countdownText = "Limited Time Offer Ends In:";
    export let endDate = new Date('2023-12-31T23:59:59'); // Default to end of year

    let days, hours, minutes, seconds;
    let intervalId;

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = endDate.getTime() - now;

        if (distance < 0) {
            days = hours = minutes = seconds = 0;
        } else {
            days = Math.floor(distance / (1000 * 60 * 60 * 24));
            hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            seconds = Math.floor((distance % (1000 * 60)) / 1000);
        }
    }

    onMount(() => {
        updateCountdown();
        intervalId = setInterval(updateCountdown, 1000);
    });

    onDestroy(() => {
        if (intervalId) clearInterval(intervalId);
    });
</script>

<div class="countdown-container">
    <div class="countdown-text">{countdownText}</div>
    <div class="countdown-timer">
        <div class="countdown-item">
            <span class="countdown-value">{days}</span>
            <span class="countdown-label">Days</span>
        </div>
        <div class="countdown-item">
            <span class="countdown-value">{hours}</span>
            <span class="countdown-label">Hours</span>
        </div>
        <div class="countdown-item">
            <span class="countdown-value">{minutes}</span>
            <span class="countdown-label">Minutes</span>
        </div>
        <div class="countdown-item">
            <span class="countdown-value">{seconds}</span>
            <span class="countdown-label">Seconds</span>
        </div>
    </div>
</div>

<style>
    .countdown-container {
        background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 4px 6px var(--shadow-color);
    }

    .countdown-text {
        font-size: 1rem;
        color: var(--text-accent);
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .countdown-timer {
        display: flex;
        justify-content: space-around;
    }

    .countdown-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .countdown-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--text-primary);
    }

    .countdown-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
    }

    :global(:root) {
        --bg-gradient-start: #f7fafc;
        --bg-gradient-end: #edf2f7;
        --text-accent: #ed8936;
        --shadow-color: rgba(0, 0, 0, 0.1);
    }

    :global(.dark) {
        --bg-gradient-start: #2d3748;
        --bg-gradient-end: #1a202c;
        --text-accent: #fbd38d;
        --shadow-color: rgba(0, 0, 0, 0.3);
    }
</style>