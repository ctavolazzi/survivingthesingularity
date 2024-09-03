<script>
    import { onMount } from 'svelte';
    import { fly } from 'svelte/transition';
    import { goto } from '$app/navigation';
    import quotes from '$lib/data/quotes.json';
    import moreQuotes from '$lib/data/more_quotes.json';

    export let initialDelay = 20000; // Minimum 20 seconds for the first quote
    
    let visible = false;
    let currentQuote = null;

    function getRandomQuote() {
        const allQuotes = [...quotes, ...moreQuotes];
        const index = Math.floor(Math.random() * allQuotes.length);
        return allQuotes[index];
    }

    function showNewQuote() {
        currentQuote = getRandomQuote();
        visible = true;
        setTimeout(() => {
            visible = false;
        }, 15000); // Hide quote after 15 seconds
    }

    function handleQuoteClick() {
        goto('/about');
    }

    function getRandomDelay() {
        return Math.floor(Math.random() * (30000 - 10000) + 10000); // Random between 10 and 30 seconds
    }

    onMount(() => {
        function scheduleNextQuote() {
            setTimeout(() => {
                showNewQuote();
                scheduleNextQuote();
            }, getRandomDelay());
        }
        
        const initialTimer = setTimeout(() => {
            showNewQuote();
            scheduleNextQuote();
        }, initialDelay);

        return () => clearTimeout(initialTimer);
    });
</script>

{#if visible && currentQuote}
    <div 
        class="floating-quote-popup" 
        transition:fly="{{ y: 50, duration: 500 }}"
        on:click={handleQuoteClick}
    >
        <button class="close-button" on:click|stopPropagation={() => visible = false}>×</button>
        <div class="quote-content">
            <svg class="quote-marks" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
            </svg>
            <p class="quote-text">{currentQuote.text}</p>
            <p class="quote-author">— {currentQuote.author}</p>
        </div>
    </div>
{/if}

<style>
    .floating-quote-popup {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 300px;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        padding: 25px;
        z-index: 1000;
        font-family: 'Georgia', serif;
        cursor: pointer;
        transition: transform 0.3s ease;
    }

    .floating-quote-popup:hover {
        transform: translateY(-5px);
    }

    .close-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: #888;
        transition: color 0.3s ease;
    }

    .close-button:hover {
        color: #333;
    }

    .quote-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }

    .quote-marks {
        width: 40px;
        height: 40px;
        opacity: 0.1;
        margin-bottom: 10px;
    }

    .quote-text {
        font-style: italic;
        text-align: center;
        margin-bottom: 15px;
        color: #333;
        font-size: 1.1em;
        line-height: 1.6;
    }

    .quote-author {
        font-weight: bold;
        color: #555;
        font-size: 0.9em;
        align-self: flex-end;
    }

    :global(.dark) .floating-quote-popup {
        background-color: rgba(30, 30, 30, 0.95);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    :global(.dark) .close-button {
        color: #aaa;
    }

    :global(.dark) .close-button:hover {
        color: #fff;
    }

    :global(.dark) .quote-text {
        color: #e0e0e0;
    }

    :global(.dark) .quote-author {
        color: #bbb;
    }

    :global(.dark) .quote-marks {
        opacity: 0.2;
    }
</style>