<script>
  import timelineItems from '../data/timelineItems.json'; // Adjust the path as necessary

  let showModal = Array(timelineItems.timelineItems.length).fill(false);

  function toggleModal(index) {
    showModal[index] = !showModal[index];
    showModal = [...showModal]; // Trigger reactivity
  }

  function handleModalClick(event, index) {
    if (event.target === event.currentTarget) {
      toggleModal(index);
    }
  }

  function searchGoogle(title) {
    const query = encodeURIComponent(title);
    window.open(`https://www.google.com/search?q=${query}`, '_blank');
  }

  function openWikipedia(url) {
    window.open(url, '_blank');
  }
</script>

<div class="timeline-container p-4 bg-white dark:bg-gray-800 shadow-md rounded-lg max-w-3xl mx-auto">
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
          class="learn-more-btn inline-flex items-center px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:outline-none focus:ring-gray-200 focus:text-blue-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-gray-700"
          on:click={() => toggleModal(index)}
        >
          Learn More
          <svg class="w-3 h-3 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </button>

        {#if showModal[index]}
          <div
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center z-50"
            on:click={(e) => handleModalClick(e, index)}
            role="dialog"
            aria-modal="true"
          >
            <div class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 m-4 max-w-xl w-full">
              <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">{item.title}</h2>
              <p class="mb-4 text-gray-700 dark:text-gray-300">{item.description}</p>
              <p class="mb-4 text-gray-700 dark:text-gray-300"><strong>Significance:</strong> {item.significance}</p>
              <div class="flex justify-end space-x-2">
                <button
                  on:click={() => openWikipedia(item.urls.wikipedia)}
                  class="px-4 py-2 bg-white text-black border border-black rounded hover:bg-gray-100 dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:hover:bg-gray-600"
                >
                  Wikipedia
                </button>
                <button
                  on:click={() => searchGoogle(item.title)}
                  class="px-4 py-2 bg-white text-black border border-black rounded hover:bg-gray-100 dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:hover:bg-gray-600"
                >
                  Search Google
                </button>
              </div>
              <button
                on:click={() => toggleModal(index)}
                class="absolute top-2 right-2 text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100"
                aria-label="Close modal"
              >
                ×
              </button>
            </div>
          </div>
        {/if}
      </li>
    {/each}
  </ol>
</div>