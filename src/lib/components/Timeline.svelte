<script>
  import { onMount } from 'svelte';
  import PathToSingularity from './PathToSingularity.svelte';
  import Button from './ui/Button.svelte';
  import JumpToOrigins from './JumpToOrigins.svelte';

  let items = [];
  let showModal = [];
  let isLoading = true;
  let isLoadingMore = false;
  let isLoadingAll = false;
  let activeModalIndex = -1;
  let currentPage = 1;
  let totalPages = 0;
  let hasMore = false;
  let showShareOptions = []; // Track share dropdown visibility for each item
  let isMobile = false; // Track if device is mobile

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

      // Reverse the items array to show newest first
      const reversedItems = [...data.items].reverse();

      if (append) {
        items = [...items, ...reversedItems];
        showModal = [...showModal, ...Array(reversedItems.length).fill(false)];
        showShareOptions = [...showShareOptions, ...Array(reversedItems.length).fill(false)];
      } else {
        items = reversedItems;
        showModal = Array(reversedItems.length).fill(false);
        showShareOptions = Array(reversedItems.length).fill(false);
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

      // Reverse the items array to show newest first
      const reversedItems = [...data.items].reverse();

      items = reversedItems;
      showModal = Array(reversedItems.length).fill(false);
      showShareOptions = Array(reversedItems.length).fill(false);

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

  // Toggle share options dropdown
  function toggleShareOptions(index) {
    // Close all other dropdowns
    showShareOptions = showShareOptions.map((_, i) => i === index ? !showShareOptions[i] : false);
  }

  // Close share options when clicking outside
  function handleClickOutside(event) {
    if (!event.target.closest('.share-dropdown') && !event.target.closest('.share-btn')) {
      showShareOptions = showShareOptions.map(() => false);
    }
  }

  // Share timeline event using Web Share API (mobile)
  function nativeShare(item) {
    const title = `Timeline: ${item.title}`;
    const text = `${item.abstract} (${item.date})`;
    const url = window.location.href;

    navigator.share({
      title,
      text,
      url
    }).catch(error => {
      console.error('Error sharing:', error);
    });
  }

  // Copy to clipboard
  function copyToClipboard(item) {
    const title = `Timeline: ${item.title}`;
    const text = `${item.abstract} (${item.date})`;
    const url = window.location.href;
    const shareText = `${title}\n\n${text}\n\n${url}`;

    // Create a temporary textarea to copy the text
    const textarea = document.createElement('textarea');
    textarea.value = shareText;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);

    // Show a simple notification
    alert('Share text copied to clipboard!');

    // Close share options
    showShareOptions = showShareOptions.map(() => false);
  }

  // Share on Twitter/X
  function shareOnTwitter(item) {
    const title = item.title;
    const text = `Check out this timeline event: ${title}`;
    const url = window.location.href;
    const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
    window.open(shareUrl, '_blank', 'noopener,noreferrer,width=600,height=400');

    // Close share options
    showShareOptions = showShareOptions.map(() => false);
  }

  // Share on Facebook
  function shareOnFacebook(item) {
    const url = window.location.href;
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
    window.open(shareUrl, '_blank', 'noopener,noreferrer,width=600,height=400');

    // Close share options
    showShareOptions = showShareOptions.map(() => false);
  }

  // Share on LinkedIn
  function shareOnLinkedIn(item) {
    const title = item.title;
    const url = window.location.href;
    const shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`;
    window.open(shareUrl, '_blank', 'noopener,noreferrer,width=600,height=400');

    // Close share options
    showShareOptions = showShareOptions.map(() => false);
  }

  // Check if device is mobile using a more reliable approach
  function checkMobile() {
    // Primary check: Web Share API availability (mostly available on mobile)
    const hasWebShare = typeof navigator.share !== 'undefined';

    // Secondary checks (feature detection)
    const hasTouchScreen = (
      ('ontouchstart' in window) ||
      (navigator.maxTouchPoints > 0) ||
      (navigator.msMaxTouchPoints > 0)
    );

    // Screen size check (typical mobile viewport)
    const isSmallScreen = window.innerWidth <= 768;

    // Use a combination of checks for better accuracy
    isMobile = hasWebShare || (hasTouchScreen && isSmallScreen);

    // Add a window resize listener to update on orientation change
    window.addEventListener('resize', () => {
      const newIsSmallScreen = window.innerWidth <= 768;
      isMobile = hasWebShare || (hasTouchScreen && newIsSmallScreen);
    });
  }

  // Load first page of items on mount
  onMount(() => {
    loadTimelineItems();
    checkMobile();

    // Add click outside listener
    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
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

          <div class="flex flex-wrap gap-2">
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

            <!-- Share button with dropdown -->
            <div class="relative">
              {#if isMobile && navigator.share}
                <!-- Native share button for mobile -->
                <button
                  type="button"
                  class="share-btn inline-flex items-center px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:outline-none focus:ring-gray-200 focus:text-blue-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-gray-700"
                  on:click={() => nativeShare(item)}
                  aria-label={`Share ${item.title}`}
                >
                  Share
                  <svg class="w-3 h-3 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
                  </svg>
                </button>
              {:else}
                <!-- Desktop share button with dropdown -->
                <button
                  type="button"
                  class="share-btn inline-flex items-center px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:outline-none focus:ring-gray-200 focus:text-blue-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-gray-700"
                  on:click={() => toggleShareOptions(index)}
                  aria-expanded={showShareOptions[index]}
                  aria-haspopup="true"
                  aria-label={`Share ${item.title}`}
                >
                  Share
                  <svg class="w-3 h-3 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
                  </svg>
                </button>

                <!-- Share options dropdown -->
                {#if showShareOptions[index]}
                  <div class="share-dropdown absolute z-10 mt-2 w-48 bg-white rounded-md shadow-lg dark:bg-gray-700 ring-1 ring-black ring-opacity-5">
                    <div class="py-1" role="menu" aria-orientation="vertical">
                      <button
                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600"
                        on:click={() => copyToClipboard(item)}
                        role="menuitem"
                      >
                        <div class="flex items-center">
                          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
                          </svg>
                          Copy to clipboard
                        </div>
                      </button>
                      <button
                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600"
                        on:click={() => shareOnTwitter(item)}
                        role="menuitem"
                      >
                        <div class="flex items-center">
                          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path>
                          </svg>
                          Share on X (Twitter)
                        </div>
                      </button>
                      <button
                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600"
                        on:click={() => shareOnFacebook(item)}
                        role="menuitem"
                      >
                        <div class="flex items-center">
                          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"></path>
                          </svg>
                          Share on Facebook
                        </div>
                      </button>
                      <button
                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600"
                        on:click={() => shareOnLinkedIn(item)}
                        role="menuitem"
                      >
                        <div class="flex items-center">
                          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path>
                          </svg>
                          Share on LinkedIn
                        </div>
                      </button>
                    </div>
                  </div>
                {/if}
              {/if}
            </div>
          </div>

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

<!-- Add the JumpToOrigins component -->
<JumpToOrigins targetSelector=".timeline-container" />

<style>
  /* Add styles for the share dropdown */
  .share-dropdown {
    right: 0;
    transform-origin: top right;
    animation: dropdown-appear 0.2s ease-out;
  }

  @keyframes dropdown-appear {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
</style>
