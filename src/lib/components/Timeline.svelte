<script>
  import timelineItems from '../data/timelineItems.json'; // Adjust the path as necessary
  import PathToSingularity from './PathToSingularity.svelte';

  let showModal = Array(timelineItems.timelineItems.length).fill(false);
  let activeModalIndex = -1;

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
</script>

<!-- Single svelte:window tag at root level -->
<svelte:window on:keydown={handleKeydown} />

<div class="timeline-container p-4 bg-white dark:bg-gray-800 shadow-md rounded-lg max-w-3xl mx-auto">
  <PathToSingularity />
  <h1 class="text-3xl font-bold text-center text-gray-900 dark:text-white mb-6">Timeline of Events</h1>
  <hr class="mb-8 border-gray-200 dark:border-gray-700" />

  <ol class="relative border-l border-gray-200 dark:border-gray-700 pl-4">
    {#each timelineItems.timelineItems as item, index (item.id)}
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
          <!-- Backdrop -->
          <div
            id={`modal-backdrop-${item.id}`}
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-40"
            aria-hidden="true"
          />
          
          <!-- Modal -->
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
              <!-- Close button at the top -->
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
</div>
