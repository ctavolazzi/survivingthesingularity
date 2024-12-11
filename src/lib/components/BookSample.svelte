<script>
    import { fade } from 'svelte/transition';
    import { onMount } from 'svelte';
    import StSBookImage from '$lib/images/Surviving-the-Singularity-Cover.png';
    import { goto } from '$app/navigation';
    import { darkMode } from '$lib/stores/darkMode';

    let readerCount = 4921;
    let isLoading = false;
    let error = null;

    function handleReadSample() {
        goto('/sample');
    }

    async function handlePreorder() {
        isLoading = true;
        error = null;

        try {
            const response = await fetch('/api/create-checkout-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const { url } = await response.json();
            window.location.href = url;
        } catch (err) {
            console.error('Preorder error:', err);
            error = 'An error occurred. Please try again.';
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        const countInterval = setInterval(() => {
            readerCount += 1;
        }, 10000);

        return () => {
            clearInterval(countInterval);
        };
    });
</script>

<section class="book-sample" class:dark={$darkMode} in:fade="{{ duration: 1000 }}">
    <div class="content">
        <h1 class="heading-text">Surviving the Singularity: Workbook</h1>
        <h2 class="subheading-1">Learn how to thrive in the age of AI</h2>
        <h2 class="subheading-2">A guided workbook for processing AI anxiety and cognitive dissonance</h2>

        <div class="book-preview">
            <div class="image-container">
                <img src={StSBookImage} alt="Surviving the Singularity Book Cover" class="book-image" on:click={handleReadSample} />
            </div>
            <div class="preview-highlights">
                <h3>In this free sample of the book, you'll find:</h3>
                <ul>
                    <li>🔮 A glimpse into AI's potential impact on your future</li>
                    <li>🚀 Teasers of key strategies for thriving in an AI world</li>
                    <li>🤖 A sneak peek at the book's approach to ethical AI considerations</li>
                    <li>🧠 Just enough to make you curious for more!</li>
                </ul>
            </div>
        </div>

        <div class="spoof-disclaimer">
            <blockquote>"This book is so good, it made my neural networks tingle!" </blockquote>
            <cite>- Definitely Not A Real AI, Fictional Endorsement Bot</cite>
            <p class="spoof-disclaimer-text">(Just kidding! We don't need fake endorsements. Read the sample and judge for yourself!)</p>
        </div>

        <div class="cta-container">
            <button on:click={handleReadSample} class="cta-button">
                Read the Free Sample Now
            </button>
            <p class="or">or</p>
            <button
                on:click={handlePreorder}
                disabled={isLoading}
                class="preorder-button"
            >
                {#if isLoading}
                    <span class="loader"></span>
                {:else}
                    PREORDER NOW
                {/if}
            </button>
            <p class="preorder-info">
                <span class="urgent">Limited copies remain at this price!</span>
                <span class="non-urgent">Secure your copy now. The book is set to release the first week of November.</span>
            </p>
            <p class="reader-count">{readerCount} curious minds have peeked at the sample</p>
        </div>

        <div class="trust-indicators">
            <p class="no-signup">✓ No sign-up required &nbsp;&nbsp; ✓ Instant access &nbsp;&nbsp; ✓ 10-minute read</p>
            <p class="data-policy">We respect your privacy. It's just a sample page - no strings attached!</p>
        </div>
    </div>
</section>

<style>
    .book-sample {
        --bg-color: #ffffff;
        --text-color: #1a202c;
        --subheading-color: #718096;
        --highlight-bg: #f0f8ff;
        --highlight-border: #3498db;
        --button-bg: #3498db;
        --button-hover-bg: #2980b9;
        --reader-count-bg: rgba(52, 152, 219, 0.1);

        background-color: var(--bg-color);
        color: var(--text-color);
        padding: 2rem;
        border-radius: 1rem;
    }

    .book-sample.dark {
        --bg-color: #1a202c;
        --text-color: #e5e7eb;
        --subheading-color: #a0aec0;
        --highlight-bg: #2c3e50;
        --highlight-border: #3498db;
        --button-bg: #3498db;
        --button-hover-bg: #2980b9;
        --reader-count-bg: rgba(52, 152, 219, 0.2);
    }

    .content {
        text-align: center;
        padding: 1rem 1.5rem;
    }

    .heading-text {
        font-size: clamp(2.5rem, 5vw, 3.5rem);
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }

    .subheading-1 {
        font-size: clamp(1.25rem, 2.5vw, 1.5rem);
        font-weight: 500;
        color: var(--subheading-color);
        margin-top: 0;
        margin-bottom: 0.5rem;
    }

    .subheading-2 {
        font-size: clamp(1rem, 2vw, 1.25rem);
        font-weight: 400;
        color: var(--subheading-color);
        max-width: 90%;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }

    .book-preview {
        display: flex;
        align-items: flex-start;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1.5rem;
    }

    .image-container {
        flex-shrink: 0;
    }

    .book-image {
        max-width: 200px;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }

    .book-image:hover {
        transform: scale(1.05);
    }

    .preview-highlights {
        background-color: var(--highlight-bg);
        padding: 1rem 0;
        border-radius: 8px;
        text-align: left;
    }

    .preview-highlights h3 {
        color: var(--text-color);
        margin-bottom: 0.5rem;
        padding: 0 1rem;
    }

    .preview-highlights ul {
        list-style-type: none;
        padding-left: 1rem;
        padding-right: 1rem;
        margin: 0;
    }

    .preview-highlights li {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        color: var(--text-color);
    }

    .spoof-disclaimer {
        font-style: italic;
        max-width: 600px;
        margin-bottom: 1.5rem;
        background-color: var(--highlight-bg);
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed var(--highlight-border);
    }

    .spoof-disclaimer blockquote {
        font-size: 1rem;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }

    .spoof-disclaimer cite {
        font-size: 0.9rem;
        color: var(--subheading-color);
    }

    .spoof-disclaimer-text {
        font-size: 0.8rem;
        color: var(--subheading-color);
        margin-top: 0.5rem;
    }

    .cta-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1rem;
        gap: 1rem;
    }

    .cta-button {
        font-weight: bold;
        background-color: var(--button-bg);
        color: #ffffff;
        border: none;
        padding: 1rem 2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.25rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .cta-button:hover {
        background-color: var(--button-hover-bg);
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    .reader-count {
        font-size: 0.9rem;
        color: var(--text-color);
        margin: 1rem 0;
        padding: 0.5rem 1rem;
        position: relative;
        overflow: hidden;
        background: var(--reader-count-bg);
        background-size: 200% 100%;
        animation: gradientShift 8s ease-in-out infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .trust-indicators {
        font-size: 0.8rem;
        color: var(--subheading-color);
    }

    .data-policy {
        margin-top: 0.5rem;
        font-style: italic;
    }

    .or {
        position: relative;
        font-size: 1rem;
        color: var(--subheading-color);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1rem 0;
        text-align: center;
        width: 100%;
    }

    .or::before,
    .or::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 40%;
        height: 1px;
        background: linear-gradient(to var(--direction, right), var(--subheading-color), transparent);
    }

    .or::before {
        left: 0;
        --direction: right;
    }

    .or::after {
        right: 0;
        --direction: left;
    }

    .preorder-info {
        font-size: 0.9rem;
        color: var(--text-color);
        margin-top: 0.5rem;
        text-align: center;
        max-width: 300px;
        line-height: 1.4;
        padding: 0.75rem;
        border-radius: 8px;
        background-color: var(--reader-count-bg);
        transition: all 0.3s ease;
        border: 1px solid var(--highlight-border);
    }

    .preorder-info:hover {
        background-color: var(--highlight-bg);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .urgent {
        display: block;
        color: #e74c3c;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }

    @media (max-width: 768px) {
        .book-sample {
            padding: 1.5rem 0;
            padding-top: 0;
        }

        .content {
            padding: 1rem 0;
        }

        .book-preview {
            flex-direction: column;
            align-items: center;
            gap: 1rem;
            padding: 0;
        }

        .preview-highlights {
            width: 100%;
            border-radius: 8px;
            margin: 0 -1.5rem;
        }

        .image-container {
            width: 100%;
            display: flex;
            justify-content: center;
        }

        .book-image {
            max-width: 150px;
            margin-top: 1rem;
        }
    }

    @media (max-width: 640px) {
        .content {
            padding: 2rem 1rem;
        }

        .heading-text {
            margin-bottom: 1.5rem;
        }

        .subheading-2 {
            max-width: 100%;
        }
    }

    .heading-text {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }

    .subheading-1,
    .subheading-2 {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }

    :global(.countdown-container) {
        margin-bottom: 0;
    }

    .preorder-button {
        width: 100%;
        background: linear-gradient(135deg, #ff8a00, #ff5e03);
        border: none;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.9rem 2rem;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 94, 3, 0.2);
    }

    .preorder-button:hover {
        background: linear-gradient(135deg, #ff5e03, #ff8a00);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 94, 3, 0.3);
    }

    .preorder-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .loader {
        display: inline-block;
        width: 22px;
        height: 22px;
        border: 4px solid #ffffff;
        border-radius: 50%;
        border-top: 4px solid transparent;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
