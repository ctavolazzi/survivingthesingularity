<script>
    import { goto } from '$app/navigation';
    import NewsletterList from './NewsletterList.svelte';
    import NewsletterSignup from './NewsletterSignup.svelte';
    import Divider from './Divider.svelte';

    export let newsletters = [];
    export let currentSlug = '';
    export let pagination = null;

    function handleSelectNewsletter(event) {
      const slug = event.detail;
      if (slug !== currentSlug) {
        goto(`/newsletter/${slug}`);
      }
    }
</script>

<div class="newsletter-container">
    <div class="flex flex-col gap-4">
      <!-- Tabbed Navigation Header -->
      <div class="w-full">
        <div class="bg-gray-50 dark:bg-gray-900 shadow rounded-lg overflow-hidden">
          <NewsletterList
            {newsletters}
            on:select={handleSelectNewsletter}
            selectedSlug={currentSlug}
            {pagination}
            compact={true}
          />
        </div>
      </div>

      <!-- Main Content -->
      <div class="w-full">
        <div class="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden p-2">
          <slot></slot>
        </div>
      </div>
    </div>

    <Divider />

    <NewsletterSignup />
</div>

<style>
    /* Global body styles */
    :global(body) {
      background-color: #f9fafb;
    }

    :global(body.dark) {
      background-color: #111827;
    }

    /* Newsletter Container */
    .newsletter-container {
      width: 100%;
      max-width: 1100px;
      margin: 0 auto;
      padding: 0.5rem;
      display: flex;
      flex-direction: column;
    }

    .newsletter-main {
      display: flex;
      flex-direction: column;
      width: 100%;
      padding: 1rem;
      background-color: white;
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    :global(.dark) .newsletter-main {
      background-color: #1f2937;
    }

    /* Media query for responsive behavior */
    @media (min-width: 1024px) {
      .newsletter-container {
        max-width: 90%;
        padding: 0.75rem;
      }

      .newsletter-main {
        padding: 1.25rem;
      }
    }
</style>