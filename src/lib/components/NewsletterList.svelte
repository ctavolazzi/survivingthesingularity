<script>
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  import { Select } from 'flowbite-svelte';

  const dispatch = createEventDispatcher();

  export let newsletters = [];
  export let selectedSlug = null;

  let searchQuery = '';

  $: newsletterOptions = newsletters.map(newsletter => ({
    value: newsletter.slug,
    name: `#${newsletter.editionNumber} - ${newsletter.title}`
  }));

  function handleSelect(event) {
    const slug = event.target.value;
    dispatch('select', { slug });
  }
</script>

<div class="newsletter-container">
  <div class="select-wrapper">
    <Select
      class="newsletter-select"
      items={newsletterOptions}
      placeholder="Select a newsletter"
      value={selectedSlug}
      on:change={handleSelect}
    />
  </div>
</div>

<style lang="postcss">
  .newsletter-container {
    @apply w-full max-w-xl mx-auto px-4;
  }

  .select-wrapper {
    @apply w-full;
  }

  :global(.newsletter-select) {
    @apply w-full bg-gray-100/50 dark:bg-gray-800/50
           border-0 rounded-xl
           text-base
           focus:ring-1 focus:ring-blue-400;
  }

  :global(.newsletter-select select) {
    @apply py-3 px-4 font-medium
           bg-transparent
           text-gray-900 dark:text-white
           placeholder:text-gray-400;
  }

  @media (max-width: 640px) {
    .newsletter-container {
      @apply px-3;
    }
  }
</style>