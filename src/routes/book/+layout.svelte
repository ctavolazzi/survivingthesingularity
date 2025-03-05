<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import Spacer from '$lib/components/Spacer.svelte';
    import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
    import SimpleBookCallout from '$lib/components/SimpleBookCallout.svelte';

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

                <section class="newsletter">
                    <NewsletterSignup />
                </section>
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
        display: inline-block !important;
        padding: 0.6rem 1.2rem !important;
        background-color: #808080 !important;
        color: #FFFFFF !important;
        border-radius: 0.4rem !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        transition: none !important;
    }
    :global(.toc-link:hover) {
        background-color: #FF6600 !important;
        color: #FFFFFF !important;
    }
</style>