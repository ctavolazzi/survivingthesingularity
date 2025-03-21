<script>
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  import { Input } from 'flowbite-svelte';

  const dispatch = createEventDispatcher();

  export let newsletters = [];
  export let selectedSlug = null;
  export let pagination = {
    currentPage: 1,
    totalPages: 1,
    perPage: 10
  };

  let searchQuery = '';
  let activeTab = 'recent';
  let listContainer;

  $: filteredNewsletters = newsletters
    .filter(newsletter =>
      newsletter.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      newsletter.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

  $: totalEditions = newsletters.length;

  function handleSelect(slug) {
    dispatch('select', { slug });
  }

  function handleSearch(event) {
    searchQuery = event.detail.target.value;
  }
</script>

<div class="newsletter-container">
  <div class="header">
    <div class="title-row">
      <h2>Newsletter Archive</h2>
      <div class="edition-count">{totalEditions} editions</div>
    </div>

    <div class="search-bar">
      <Input
        type="search"
        placeholder="Search newsletters..."
        bind:value={searchQuery}
        size="lg"
        class="search-input"
        on:input={handleSearch}
      />
    </div>
  </div>

  <div class="newsletter-list" bind:this={listContainer}>
    <div class="newsletters">
      {#each filteredNewsletters as newsletter}
        <button
          class="newsletter-item {newsletter.slug === selectedSlug ? 'selected' : ''}"
          on:click={() => handleSelect(newsletter.slug)}
        >
          <div class="newsletter-content">
            <div class="newsletter-title">{newsletter.title}</div>
            <div class="newsletter-meta">
              <span class="edition-number">Edition #{newsletter.editionNumber}</span>
            </div>
          </div>
        </button>
      {/each}
    </div>
  </div>
</div>

<style lang="postcss">
  .newsletter-container {
    @apply w-full max-w-3xl mx-auto bg-transparent;
  }

  .header {
    @apply p-4 sm:p-6 space-y-4;
  }

  .title-row {
    @apply flex items-center justify-between;
  }

  .title-row h2 {
    @apply text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white;
  }

  .edition-count {
    @apply px-3 py-1.5 text-sm font-medium text-blue-600 dark:text-blue-400
           bg-blue-50 dark:bg-blue-900/20 rounded-full;
  }

  .search-bar {
    @apply w-full;
  }

  :global(.search-input) {
    @apply w-full bg-gray-100/50 dark:bg-gray-800/50
           border-0 rounded-xl
           text-base placeholder:text-gray-500
           focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400
           transition-shadow duration-200;
  }

  .newsletters {
    @apply divide-y divide-gray-100 dark:divide-gray-800;
  }

  .newsletter-item {
    @apply w-full text-left px-4 sm:px-6 py-5 transition-colors
           hover:bg-gray-50 dark:hover:bg-gray-800/50
           active:bg-gray-100 dark:active:bg-gray-800
           touch-manipulation;
  }

  .newsletter-item.selected {
    @apply bg-blue-50 dark:bg-blue-900/20;
  }

  .newsletter-content {
    @apply flex flex-col gap-2;
  }

  .newsletter-title {
    @apply text-lg font-semibold text-gray-900 dark:text-white
           leading-tight;
  }

  .newsletter-meta {
    @apply flex flex-wrap items-center gap-2 text-sm text-gray-500 dark:text-gray-400;
  }

  .edition-number {
    @apply font-medium;
  }

  /* Hide scrollbar but keep functionality */
  .no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  .no-scrollbar::-webkit-scrollbar {
    display: none;
  }

  /* Optimize touch targets for mobile */
  @media (max-width: 640px) {
    .newsletter-item {
      @apply py-4;
    }
  }
</style>