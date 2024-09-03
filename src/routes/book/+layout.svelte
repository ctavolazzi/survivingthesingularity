<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import Spacer from '$lib/components/Spacer.svelte';
    import SkoolGroup from '$lib/components/SkoolGroup.svelte';
    import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
    import CommunityIntakePopupForm from '$lib/components/CommunityIntakePopupForm.svelte';

    let showLowerSections = false;

    onMount(() => {
        setTimeout(() => {
            showLowerSections = true;
        }, 1000);
    });
</script>

<main class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <div class="max-w-3xl mx-auto px-4 py-8" in:fade="{{ duration: 800 }}">
        <slot></slot>

        {#if showLowerSections}
            <Spacer height="50px" />

            <section class="community">
                <SkoolGroup />
            </section>

            <Spacer height="50px" />

            <CommunityIntakePopupForm 
                ctaText="Ready to join the rebellion against the singularity?" 
                buttonText="Enlist Now"
            />

            <Spacer height="50px" />

            <section class="newsletter">
                <NewsletterSignup />
            </section>
        {/if}
    </div>
</main>

<style>
    /* Any additional styles */
</style>