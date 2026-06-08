<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import Spacer from '$lib/components/Spacer.svelte';
    import SimpleBookCallout from '$lib/components/SimpleBookCallout.svelte';
    import { page } from '$app/stores';
    import Navbar from '$lib/components/Navbar.svelte';
    import Footer from '$lib/components/Footer.svelte';


    let showLowerSections = false;

    onMount(() => {
        setTimeout(() => {
            showLowerSections = true;
        }, 1000);
    });
</script>

<main class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="max-w-4xl mx-auto" in:fade="{{ duration: 800 }}">
            <aside class="book-info-only-banner not-prose">
                <p class="bb-title">Informational & educational use only</p>
                <p class="bb-body">
                    Always consult the relevant licensed professionals before making any decision based on content in this book. Material here is the author's commentary, speculation, and supposition - not financial, legal, tax, medical, real-estate, construction, or any other professional advice. References to specific products or individuals are editorial and do not imply endorsement.
                    <a href="/disclaimer" class="bb-link">Full disclaimer →</a>
                </p>
            </aside>
            <div class="prose prose-lg dark:prose-invert mx-auto text-justify">
                <slot></slot>
            </div>

            {#if showLowerSections}
                <Spacer height="50px" />

                <SimpleBookCallout
                    title="Navigate the Path to Singularity"
                    description="Get the insights and strategies you need to prepare for the technological changes that will reshape our world."
                    buttonText="Explore the Book"
                    buttonLink="/book"
                />

                <div class="newsletter-container">
                    <!-- Discord removed -->
                </div>
            {/if}
        </div>
    </div>
</main>

<style>
    .container {
        width: 100%;
        max-width: 1280px;
    }
    .book-info-only-banner {
        margin: 0 auto 2rem;
        max-width: 720px;
        padding: 1rem 1.25rem;
        background: rgba(120, 53, 15, 0.18);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 10px;
    }
    .bb-title {
        font-family: var(--font-primary);
        font-size: 0.82rem;
        font-weight: 700;
        color: #fcd34d;
        letter-spacing: 0.08em;
        margin: 0 0 0.5rem 0;
    }
    .bb-body {
        font-size: 0.85rem;
        color: #fde9c8;
        line-height: 1.6;
        margin: 0;
    }
    .bb-link {
        color: #fcd34d;
        text-decoration: underline;
        text-underline-offset: 2px;
        font-weight: 600;
        white-space: nowrap;
    }
    .bb-link:hover { color: #fdf6ec; }
    :global(.prose) {
        max-width: none;
    }
    :global(.toc-link) {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        background: var(--color-surface, rgba(30, 41, 59, 0.5));
        color: var(--color-text-primary, #f1f5f9);
        border: 1px solid var(--color-border, rgba(148, 163, 184, 0.1));
        border-radius: var(--radius-sm, 6px);
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        transition: border-color 150ms ease, background 150ms ease;
    }
    :global(.toc-link:hover) {
        background: var(--color-surface-hover, rgba(30, 41, 59, 0.8));
        border-color: var(--color-primary, #f59e0b);
        color: var(--color-primary, #f59e0b);
    }
</style>