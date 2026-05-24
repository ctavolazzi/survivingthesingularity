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