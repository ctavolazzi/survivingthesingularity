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

<section class="book-sample" class:dark={$darkMode}>
    <div class="content">
        <h1 class="heading-text">Surviving the Singularity: Workbook</h1>
        <h2 class="subheading-1">A guide for thinking about AI and our changing world</h2>
        <h2 class="subheading-2">A companion for processing technological change and developing clarity</h2>

        <div class="book-preview">
            <div class="image-container">
                <button class="book-image-button" on:click={handleReadSample} on:keydown={e => e.key === 'Enter' && handleReadSample()}>
                    <img src={StSBookImage} alt="Surviving the Singularity Book Cover" class="book-image" loading="lazy" />
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

    <div class="decorative-element">
        <div class="tech-circle"></div>
        <div class="tech-circle"></div>
        <div class="tech-circle"></div>
        <div class="tech-dots"></div>
    </div>
</section>

<style>
    .book-sample {
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
        padding: 1.5rem;
        background-color: rgba(25, 25, 35, 0.6);
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(124, 58, 237, 0.1);
        position: relative;
        overflow: hidden;
    }

    .book-sample.dark {
        background-color: rgba(25, 25, 35, 0.6);
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
        color: #ffffff;
    }

    .book-sample.dark .heading-text {
        color: #ffffff;
    }

    .subheading-1, .subheading-2 {
        font-size: 1.25rem;
        text-align: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }

    .book-sample.dark .subheading-1,
    .book-sample.dark .subheading-2 {
        color: #ffffff;
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
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    .preview-highlights {
        flex: 1;
    }

    .preview-highlights h3 {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #ffffff;
    }

    .book-sample.dark .preview-highlights h3 {
        color: #ffffff;
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
        color: #ffffff;
    }

    .book-sample.dark .preview-highlights li {
        color: #ffffff;
    }

    .cta-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 2rem;
    }

    .cta-button {
        padding: 0.75rem 1.5rem;
        background-color: #7c3aed;
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.3);
    }

    .cta-button:hover {
        background-color: #6d28d9;
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.5);
    }

    .book-sample.dark .cta-button {
        background-color: #7c3aed;
    }

    .book-sample.dark .cta-button:hover {
        background-color: #6d28d9;
    }

    .spoof-disclaimer {
        margin: 2rem 0;
        text-align: center;
        font-style: italic;
        color: #ffffff;
    }

    .book-sample.dark .spoof-disclaimer {
        color: #ffffff;
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

    .decorative-element {
        position: absolute;
        bottom: 20px;
        right: 20px;
        width: 120px;
        height: 120px;
        opacity: 0.6;
        pointer-events: none;
    }

    .tech-circle {
        position: absolute;
        border-radius: 50%;
        border: 1px dashed rgba(124, 58, 237, 0.4);
    }

    .tech-circle:nth-child(1) {
        width: 100%;
        height: 100%;
        animation: rotate 20s linear infinite;
    }

    .tech-circle:nth-child(2) {
        width: 70%;
        height: 70%;
        top: 15%;
        left: 15%;
        animation: rotate 15s linear infinite reverse;
    }

    .tech-circle:nth-child(3) {
        width: 40%;
        height: 40%;
        top: 30%;
        left: 30%;
        animation: rotate 10s linear infinite;
    }

    .tech-dots {
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(circle, rgba(124, 58, 237, 0.5) 1px, transparent 1px);
        background-size: 10px 10px;
        opacity: 0.3;
    }

    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>
