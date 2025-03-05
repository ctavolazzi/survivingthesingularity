<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { fade, slide, fly } from 'svelte/transition';
  import { Button, Card, Input, Badge } from 'flowbite-svelte';

  export let newsletters = [];
  export let selectedSlug = '';
  export let pagination = null;
  export const compact = false;

  const dispatch = createEventDispatcher();

  let searchTerm = '';
  let listContainer;
  let activeTab = 'recent';
  let searchVisible = false;
  let isNavExpanded = false;

  $: filteredNewsletters = newsletters.filter(newsletter =>
    newsletter.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    newsletter.date?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    newsletter.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  $: totalEditions = pagination ? pagination.totalItems : newsletters.length;
  $: newslettersByYear = groupByYear(filteredNewsletters);
  $: years = Object.keys(newslettersByYear).sort((a, b) => b.localeCompare(a));

  function groupByYear(newsletters) {
    const groups = {};

    newsletters.forEach(newsletter => {
      const year = newsletter.date?.split('-')[0] || 'Unknown';
      if (!groups[year]) {
        groups[year] = [];
      }
      groups[year].push(newsletter);
    });

    Object.keys(groups).forEach(year => {
      groups[year].sort((a, b) => b.editionNumber - a.editionNumber);
    });

    return groups;
  }

  function selectNewsletter(slug) {
    // Dispatch the selection event with the slug
    dispatch('select', slug);

    // Close the dropdown after selection
    isNavExpanded = false;

    // Hide search on mobile after selection
    if (window.innerWidth < 768) {
      searchVisible = false;
    }
  }

  function scrollToTop() {
    if (listContainer) {
      listContainer.scrollTop = 0;
    }
  }

  function setActiveTab(tab) {
    activeTab = tab;
    scrollToTop();
  }

  function toggleSearch() {
    searchVisible = !searchVisible;
    if (searchVisible) {
      setTimeout(() => {
        document.querySelector('.search-input')?.focus();
      }, 100);
    } else {
      searchTerm = '';
    }
  }

  onMount(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        searchVisible = true;
      } else if (!searchVisible) {
        searchVisible = false;
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => {
      window.removeEventListener('resize', handleResize);
      scrollToTop();
    };
  });
</script>

<div class="relative w-full max-w-full overflow-hidden">
    <!-- Compact Modern Navigation for Newsletter Header -->
  <div class="newsletter-header flex flex-col gap-2 px-1 py-2 border-b border-gray-200 dark:border-gray-700">
    <!-- Top Row with Title and Controls -->
    <div class="flex justify-between items-center">
      <div class="flex items-center gap-2">
        <h2 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white">Newsletters</h2>
        <Badge color="blue" size="sm" class="font-medium">{totalEditions}</Badge>
      </div>

      <!-- Search and Nav Toggle for Mobile -->
      <div class="flex items-center gap-1">
        <button
          class="md:hidden flex items-center justify-center w-7 h-7 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
          on:click={toggleSearch}
          aria-label="Toggle search"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>

        <!-- Search Input -->
        {#if searchVisible}
          <div class="search-container" transition:slide={{duration: 200, axis: 'y'}}>
            <Input
              type="text"
              placeholder="Search newsletters..."
              bind:value={searchTerm}
              size="sm"
              class="w-full md:w-40 search-input text-xs"
            />
          </div>
        {/if}
      </div>
    </div>

    <!-- Newsletter Navigation Dropdown -->
    <div class="newsletter-nav relative">
        <button
        class="w-full flex items-center justify-between px-3 py-2 text-sm bg-gray-50 dark:bg-gray-800 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        on:click={() => isNavExpanded = !isNavExpanded}
      >
        <div class="flex items-center gap-2">
          <span class="text-orange-600 dark:text-orange-400 font-medium">Currently Reading:</span>
          <span class="font-medium truncate">
            {#if selectedSlug && newsletters.length > 0}
              {newsletters.find(n => n.slug === selectedSlug)?.title || 'Select a newsletter'}
            {:else}
              Latest Edition
            {/if}
          </span>
        </div>
        <svg
          class="w-4 h-4 transition-transform {isNavExpanded ? 'rotate-180' : ''}"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {#if isNavExpanded}
        <div
          class="absolute top-full left-0 right-0 mt-1 max-h-[70vh] overflow-y-auto bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 z-50"
          transition:slide={{duration: 200}}
        >
          <!-- Quick Navigation Tabs -->
          <div class="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-2">
            <div class="flex gap-1">
              <button
                class="px-2 py-1 text-xs rounded {activeTab === 'recent' ? 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300' : 'hover:bg-gray-100 dark:hover:bg-gray-700'}"
                on:click={() => setActiveTab('recent')}
              >
                Recent
              </button>
              {#each years as year}
                <button
                  class="px-2 py-1 text-xs rounded {activeTab === year ? 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300' : 'hover:bg-gray-100 dark:hover:bg-gray-700'}"
                  on:click={() => setActiveTab(year)}
                >
                  {year}
                </button>
              {/each}
            </div>
          </div>

          <!-- Newsletter List -->
          <div class="p-1">
            {#if activeTab === 'recent'}
              {#each newsletters.slice(0, 5) as newsletter}
                <button
                  class="w-full text-left p-2 hover:bg-gray-50 dark:hover:bg-gray-700 rounded {newsletter.slug === selectedSlug ? 'bg-orange-50 dark:bg-orange-900/20' : ''}"
                  on:click={() => selectNewsletter(newsletter.slug)}
                >
                  <div class="flex items-center justify-between">
                    <div>
                      <div class="font-medium">{newsletter.title}</div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">Edition #{newsletter.editionNumber}</div>
                    </div>
                    <div class="text-xs text-gray-500 dark:text-gray-400">{newsletter.date}</div>
                  </div>
                </button>
              {/each}
              <div class="px-2 py-1 border-t border-gray-200 dark:border-gray-700">
                <button
                  class="w-full text-center text-sm text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300"
                  on:click={() => setActiveTab('all')}
                >
                  View All Editions
                </button>
              </div>
            {:else}
              {#each newslettersByYear[activeTab] || [] as newsletter}
                <button
                  class="w-full text-left p-2 hover:bg-gray-50 dark:hover:bg-gray-700 rounded {newsletter.slug === selectedSlug ? 'bg-orange-50 dark:bg-orange-900/20' : ''}"
                  on:click={() => selectNewsletter(newsletter.slug)}
                >
                  <div class="flex items-center justify-between">
                    <div>
                      <div class="font-medium">{newsletter.title}</div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">Edition #{newsletter.editionNumber}</div>
                    </div>
                    <div class="text-xs text-gray-500 dark:text-gray-400">{newsletter.date}</div>
                  </div>
                </button>
              {/each}
            {/if}
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Currently Reading Content -->
  <div class="newsletter-content mt-4">
    {#if selectedSlug && newsletters.length > 0}
      {#each filteredNewsletters.filter(n => n.slug === selectedSlug) as newsletter (newsletter.slug)}
        <div
          class="newsletter-card-large px-4 py-3 border-l-2 border-orange-500 bg-white dark:bg-gray-800 rounded-md shadow-sm"
          transition:fade={{ duration: 150 }}
        >
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-sm font-semibold">#{newsletter.editionNumber}</h3>
            <p class="text-xs text-gray-600 dark:text-gray-400">{newsletter.date}</p>
          </div>
          <h2 class="text-xl font-bold mb-2">{newsletter.title}</h2>
          {#if newsletter.description}
            <p class="text-gray-700 dark:text-gray-300 text-sm">{newsletter.description}</p>
          {/if}
        </div>
      {:else}
        <!-- No matching newsletter found -->
        <div class="text-center py-8 text-gray-500 dark:text-gray-400">
          <p>Newsletter not found. Selected slug: {selectedSlug}</p>
        </div>
      {/each}
    {:else}
      <div class="text-center py-8 text-gray-500 dark:text-gray-400">
        <p>Select a newsletter to start reading</p>
      </div>
    {/if}
  </div>
</div>

<style lang="postcss">
  /* Newsletter card styles */
  .newsletter-card-large {
    @apply transition-all duration-200;
  }

  :global(.dark) .newsletter-card-large {
    @apply border-opacity-15;
  }

  /* Mobile optimizations */
  @media (max-width: 768px) {
    .search-container {
      @apply w-full;
    }
  }
</style>