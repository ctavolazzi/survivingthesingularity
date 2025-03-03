<script>
  import { onMount } from 'svelte';
  import PathToSingularity from './PathToSingularity.svelte';
  import Button from './ui/Button.svelte';

  let items = [];
  let showModal = [];
  let isLoading = true;
  let isLoadingMore = false;
  let isLoadingAll = false;
  let activeModalIndex = -1;
  let currentPage = 1;
  let totalPages = 0;
  let hasMore = false;

  // Load timeline items from API with pagination
  async function loadTimelineItems(page = 1, append = false) {
    try {
      if (append) {
        isLoadingMore = true;
      } else {
        isLoading = true;
      }

      const response = await fetch(`/api/timeline?page=${page}&limit=5`);
      if (!response.ok) throw new Error('Failed to load timeline data');

      const data = await response.json();

      if (append) {
        items = [...items, ...data.items];
        showModal = [...showModal, ...Array(data.items.length).fill(false)];
      } else {
        items = data.items;
        showModal = Array(data.items.length).fill(false);
      }

      currentPage = data.pagination.currentPage;
      totalPages = data.pagination.totalPages;
      hasMore = data.pagination.hasMore;
    } catch (error) {
      console.error('Error loading timeline:', error);
    } finally {
      isLoading = false;
      isLoadingMore = false;
    }
  }

  // Load all timeline items
  async function loadAllTimelineItems() {
    try {
      isLoadingAll = true;

      const response = await fetch(`/api/timeline?limit=100`);
      if (!response.ok) throw new Error('Failed to load all timeline data');

      const data = await response.json();

      items = data.items;
      showModal = Array(data.items.length).fill(false);

      currentPage = data.pagination.currentPage;
      totalPages = data.pagination.totalPages;
      hasMore = data.pagination.hasMore;
    } catch (error) {
      console.error('Error loading all timeline items:', error);
    } finally {
      isLoadingAll = false;
    }
  }

  function loadMore() {
    if (hasMore && !isLoadingMore) {
      loadTimelineItems(currentPage + 1, true);
    }
  }

  function loadAll() {
    if (!isLoadingAll) {
      loadAllTimelineItems();
    }
  }

  function toggleModal(index) {
    showModal[index] = !showModal[index];
    showModal = [...showModal];
    activeModalIndex = showModal[index] ? index : -1;
    if (showModal[index]) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Escape' && activeModalIndex !== -1) {
      toggleModal(activeModalIndex);
    }
  }

  function searchGoogle(title) {
    const query = encodeURIComponent(title);
    window.open(`https://www.google.com/search?q=${query}`, '_blank', 'noopener noreferrer');
  }

  function openWikipedia(url) {
    window.open(url, '_blank', 'noopener noreferrer');
  }

  // Load first page of items on mount
  onMount(() => {
    loadTimelineItems();
  });
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="timeline-container p-4 bg-white dark:bg-gray-800 shadow-md rounded-lg max-w-3xl mx-auto">
  <PathToSingularity />
  <h1 class="text-3xl font-bold text-center text-gray-900 dark:text-white mb-6">Timeline of Events</h1>
  <hr class="mb-8 border-gray-200 dark:border-gray-700" />

  {#if isLoading || isLoadingAll}
    <div class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <ol class="relative border-l border-gray-200 dark:border-gray-700 pl-4">
      {#each items as item, index (item.id)}
        <li class="mb-10">
          <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -left-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
          <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{item.date}</time>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{item.title}</h3>
          <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">{item.abstract}</p>
          <button
            type="button"
            class="learn-more-btn inline-flex items-center px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:outline-none focus:ring-gray-200 focus:text-blue-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-gray-700"
            on:click={() => toggleModal(index)}
            aria-expanded={showModal[index]}
            aria-controls={`modal-${item.id}`}
          >
            Learn More
            <svg class="w-3 h-3 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </button>

          {#if showModal[index]}
            <!-- Modal implementation remains the same -->
            <div
              id={`modal-backdrop-${item.id}`}
              class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-40"
              aria-hidden="true"
            />

            <button
              type="button"
              class="sr-only"
              on:click={() => toggleModal(index)}
            >
              Close modal
            </button>

            <div
              id={`modal-${item.id}`}
              class="fixed inset-0 overflow-y-auto h-full w-full flex justify-center items-center z-50"
              role="dialog"
              aria-labelledby={`modal-title-${item.id}`}
              aria-modal="true"
            >
              <div
                class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 m-4 max-w-xl w-full"
                role="document"
              >
                <button
                  type="button"
                  on:click={() => toggleModal(index)}
                  class="absolute top-2 right-2 text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100"
                  aria-label="Close modal"
                >
                  ×
                </button>

                <h2
                  id={`modal-title-${item.id}`}
                  class="text-2xl font-bold mb-4 text-gray-900 dark:text-white"
                >
                  {item.title}
                </h2>

                <p class="mb-4 text-gray-700 dark:text-gray-300">
                  {item.description}
                </p>

                <p class="mb-4 text-gray-700 dark:text-gray-300">
                  <strong>Significance:</strong> {item.significance}
                </p>

                <div class="flex justify-end space-x-2">
                  <button
                    type="button"
                    on:click={() => openWikipedia(item.urls.wikipedia)}
                    class="px-4 py-2 bg-white text-black border border-black rounded hover:bg-gray-100 dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:hover:bg-gray-600"
                  >
                    Wikipedia
                  </button>
                  <button
                    type="button"
                    on:click={() => searchGoogle(item.title)}
                    class="px-4 py-2 bg-white text-black border border-black rounded hover:bg-gray-100 dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:hover:bg-gray-600"
                  >
                    Search Google
                  </button>
                </div>
              </div>
            </div>
          {/if}
        </li>
      {/each}
    </ol>

    {#if hasMore}
      <div class="flex justify-center mt-8 gap-4">
        <Button
          variant="secondary"
          on:click={loadMore}
          loading={isLoadingMore}
          disabled={isLoadingMore || isLoadingAll}
          class="min-w-[160px]"
        >
          {isLoadingMore ? 'Loading...' : 'Load More Events'}
        </Button>

        {#if currentPage >= 2}
          <Button
            variant="secondary"
            on:click={loadAll}
            loading={isLoadingAll}
            disabled={isLoadingAll || isLoadingMore}
            class="min-w-[160px]"
          >
            {isLoadingAll ? 'Loading...' : 'Load All Events'}
          </Button>
        {/if}
      </div>
    {/if}
  {/if}
</div>
