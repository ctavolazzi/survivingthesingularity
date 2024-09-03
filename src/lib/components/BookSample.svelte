<script>
    import { fade } from 'svelte/transition';
    import { onMount } from 'svelte';
    import StSBookImage from '$lib/images/Surviving-the-Singularity-Cover.png';

    let readerCount = 4921;

    function handleReadSample() {
        window.location.href = '/sample';
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

<section class="book-sample" in:fade="{{ duration: 1000 }}">
    <div class="content">
        <h2 class="heading-text">Surviving the Singularity: A Sneak Peek</h2>
        <p class="subheading">Get a taste of the AI revolution with our free sample</p>
        
        <div class="book-preview">
            <div class="image-container">
                <img src={StSBookImage} alt="Surviving the Singularity Book Cover" class="book-image" on:click={handleReadSample} />
            </div>
            <div class="preview-highlights">
                <h3>In this free sample, you'll find:</h3>
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
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: var(--color-text-primary);
    }

    .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .heading-text {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #333333;
    }

    .subheading {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 1.5rem;
        max-width: 600px;
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
        background-color: #f8f8f8;
        padding: 1rem;
        border-radius: 8px;
        text-align: left;
        flex-grow: 1;
    }

    .preview-highlights h3 {
        color: #333333;
        margin-bottom: 0.5rem;
    }

    .preview-highlights ul {
        list-style-type: none;
        padding-left: 0;
        margin-left: 0;
    }

    .preview-highlights li {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }

    .preview-highlights li::before {
        content: attr(data-emoji);
        margin-right: 0.5rem;
        font-size: 1.2em;
    }

    .spoof-disclaimer {
        font-style: italic;
        max-width: 600px;
        margin-bottom: 1.5rem;
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed #3498db;
    }

    .spoof-disclaimer blockquote {
        font-size: 1rem;
        color: #555555;
        margin-bottom: 0.5rem;
    }

    .spoof-disclaimer cite {
        font-size: 0.9rem;
        color: #777777;
    }

    .spoof-disclaimer-text {
        font-size: 0.8rem;
        color: #888888;
        margin-top: 0.5rem;
    }

    .cta-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1rem;
    }

    .cta-button {
        font-weight: bold;
        background-color: #3498db;
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
        background-color: #2980b9;
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    .reader-count {
        font-size: 0.9rem;
        color: #666666;
        margin-bottom: 0.5rem;
    }

    .trust-indicators {
        font-size: 0.8rem;
        color: #888888;
    }

    .data-policy {
        margin-top: 0.5rem;
        font-style: italic;
    }

    :global(.dark) .book-sample {
        background-color: #2c3e50;
        color: #e5e7eb;
    }

    :global(.dark) .heading-text {
        color: #e5e7eb;
    }

    :global(.dark) .subheading,
    :global(.dark) .spoof-disclaimer blockquote {
        color: #b0b0b0;
    }

    :global(.dark) .preview-highlights {
        background-color: #34495e;
    }

    :global(.dark) .preview-highlights h3,
    :global(.dark) .preview-highlights ul {
        color: #e5e7eb;
    }

    :global(.dark) .spoof-disclaimer {
        background-color: #2c3e50;
        border-color: #3498db;
    }

    :global(.dark) .spoof-disclaimer cite,
    :global(.dark) .reader-count,
    :global(.dark) .trust-indicators,
    :global(.dark) .spoof-disclaimer-text {
        color: #a0a0a0;
    }

    :global(.dark) .cta-button {
        background-color: #3498db;
    }

    :global(.dark) .cta-button:hover {
        background-color: #2980b9;
    }

    @media (max-width: 768px) {
        .book-sample {
            padding: 1.5rem;
        }

        .heading-text {
            font-size: 1.75rem;
        }

        .subheading {
            font-size: 1rem;
        }

        .book-preview {
            flex-direction: column;
            align-items: center;
        }

        .book-image {
            max-width: 150px;
            margin-bottom: 1rem;
        }

        .cta-button {
            font-size: 1.1rem;
            padding: 0.8rem 1.6rem;
        }
    }
</style>