<script>
    import { fade } from 'svelte/transition';
    import { onMount } from 'svelte';
    import StSBookImage from '$lib/images/Surviving-the-Singularity-Cover.png';
    import { goto } from '$app/navigation';
    import { darkMode } from '$lib/stores/darkMode';

    function handleReadSample() {
        goto('/sample');
    }
</script>

<section class="book-sample" class:dark={$darkMode} in:fade="{{ duration: 1000 }}">
    <div class="content">
        <h1 class="heading-text">Surviving the Singularity: Workbook</h1>
        <h2 class="subheading-1">A guide for thinking about AI and our changing world</h2>
        <h2 class="subheading-2">A companion for processing technological change and developing clarity</h2>

        <div class="book-preview">
            <div class="image-container">
                <button class="book-image-button" on:click={handleReadSample} on:keydown={e => e.key === 'Enter' && handleReadSample()}>
                    <img src={StSBookImage} alt="Surviving the Singularity Book Cover" class="book-image" />
                </button>
            </div>
            <div class="preview-highlights">
                <h3>In this free sample, you'll find:</h3>
                <ul>
                    <li>🔮 Perspectives on AI's potential impacts</li>
                    <li>🚀 Frameworks for thinking about technological change</li>
                    <li>🤖 Ethical considerations around emerging technologies</li>
                    <li>🧠 Tools for processing complex changes</li>
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
                Read the Free Sample
            </button>
        </div>
    </div>
</section>

<style>
    .book-sample {
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
        padding: 1.5rem;
        background-color: var(--color-bg-secondary, #f7f9fc);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }

    .book-sample.dark {
        background-color: var(--color-bg-secondary-dark, #1a1e2d);
    }

    .content {
        max-width: 800px;
        margin: 0 auto;
    }

    .heading-text {
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        color: var(--color-text-primary, #333);
    }

    .book-sample.dark .heading-text {
        color: var(--color-text-primary-dark, #e2e8f0);
    }

    .subheading-1, .subheading-2 {
        font-size: 1.25rem;
        text-align: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--color-text-secondary, #666);
    }

    .book-sample.dark .subheading-1,
    .book-sample.dark .subheading-2 {
        color: var(--color-text-secondary-dark, #a0aec0);
    }

    .book-preview {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        margin: 2rem 0;
        align-items: center;
    }

    .image-container {
        max-width: 300px;
    }

    .book-image-button {
        background: none;
        border: none;
        padding: 0;
        cursor: pointer;
        transition: transform 0.3s ease;
    }

    .book-image-button:hover {
        transform: scale(1.05);
    }

    .book-image-button:focus {
        outline: none;
    }

    .book-image {
        width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    .preview-highlights {
        flex: 1;
    }

    .preview-highlights h3 {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--color-text-primary, #333);
    }

    .book-sample.dark .preview-highlights h3 {
        color: var(--color-text-primary-dark, #e2e8f0);
    }

    .preview-highlights ul {
        list-style: none;
        padding: 0;
    }

    .preview-highlights li {
        display: flex;
        align-items: flex-start;
        margin-bottom: 0.75rem;
        font-size: 1rem;
        color: var(--color-text-secondary, #555);
    }

    .book-sample.dark .preview-highlights li {
        color: var(--color-text-secondary-dark, #cbd5e0);
    }

    .cta-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 2rem;
    }

    .cta-button {
        padding: 0.75rem 1.5rem;
        background-color: var(--color-primary, #3182ce);
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .cta-button:hover {
        background-color: var(--color-primary-hover, #2b6cb0);
        transform: translateY(-2px);
    }

    .book-sample.dark .cta-button {
        background-color: var(--color-primary-dark, #4299e1);
    }

    .book-sample.dark .cta-button:hover {
        background-color: var(--color-primary-hover-dark, #3182ce);
    }

    .spoof-disclaimer {
        margin: 2rem 0;
        text-align: center;
        font-style: italic;
        color: var(--color-text-secondary, #666);
    }

    .book-sample.dark .spoof-disclaimer {
        color: var(--color-text-secondary-dark, #a0aec0);
    }

    .spoof-disclaimer blockquote {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .spoof-disclaimer cite {
        font-size: 0.9rem;
        display: block;
        margin-bottom: 0.5rem;
    }

    .spoof-disclaimer-text {
        font-size: 0.8rem;
    }

    @media (min-width: 768px) {
        .book-preview {
            flex-direction: row;
            align-items: flex-start;
        }

        .image-container {
            flex: 0 0 250px;
        }
    }
</style>
