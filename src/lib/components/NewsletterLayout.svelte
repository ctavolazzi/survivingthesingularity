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
        // Use direct window.location navigation to ensure a full page reload
        // This is more reliable than goto() for ensuring content updates
        window.location.href = `/newsletter/${slug}`;
      }
    }
</script>

<div class="newsletter-container">
    <div class="flex flex-col gap-4">
      <!-- Tabbed Navigation Header -->
      <div class="w-full">
        <div class="bg-gray-50 dark:bg-gray-900 shadow rounded-lg">
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
        <div class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-2">
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
      width: 100%;
    }

    :global(body.dark) {
      background-color: #111827;
    }

    /* Newsletter Container */
    .newsletter-container {
      width: 100%;
      max-width: min(1400px, 100% - 1rem);
      margin: 0 auto;
      padding: 0.5rem;
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
      gap: 0.75rem;
    }

    /* Ensure all content stays within bounds */
    :global(.newsletter-container *) {
      max-width: 100%;
      word-wrap: break-word;
      overflow-wrap: break-word;
    }

    /* Media query for responsive behavior */
    @media (min-width: 1024px) {
      .newsletter-container {
        max-width: min(95%, 1400px);
        padding: 0.75rem;
      }
    }

    @media (max-width: 768px) {
      .newsletter-container {
        padding: 0.5rem;
        margin: 0 auto;
      }
    }

    @media (max-width: 480px) {
      .newsletter-container {
        padding: 0.25rem;
        margin: 0 auto;
      }
    }

    /* Ensure images and media stay within bounds */
    :global(.newsletter-container img),
    :global(.newsletter-container video),
    :global(.newsletter-container iframe) {
      max-width: 100%;
      height: auto;
    }

    /* Ensure tables don't overflow */
    :global(.newsletter-container table) {
      width: 100%;
      max-width: 100%;
      display: block;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }
</style>