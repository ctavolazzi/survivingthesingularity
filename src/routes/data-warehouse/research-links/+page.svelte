<script>
  import { onMount } from 'svelte';
  import ResearchLinkItem from '$lib/components/ResearchLinkItem.svelte';
  import { Button, Input } from 'flowbite-svelte';
  import { researchLinksStore } from '$lib/stores/researchLinksStore';

  let uniqueAuthors = new Set();
  let uniqueTags = new Set();
  let searchTerm = '';
  let isSummaryExpanded = false;

  $: {
    uniqueAuthors = new Set();
    uniqueTags = new Set();
    $researchLinksStore.links.forEach(link => {
      if (link.author) {
        link.author.split(',').forEach(author => uniqueAuthors.add(author.trim()));
      }
      if (link.tags) {
        try {
          JSON.parse(link.tags).forEach(tag => uniqueTags.add(tag.trim()));
        } catch (e) {
          console.error('Error parsing tags for link:', link.title, e);
        }
      }
    });
  }

  function handleSearch() {
    researchLinksStore.setSearchTerm(searchTerm);
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }

  function toggleSummary() {
    isSummaryExpanded = !isSummaryExpanded;
  }

  onMount(() => {
    researchLinksStore.fetchLinks();
  });
</script>

<main class="container mx-auto px-4 py-8 max-w-4xl">
  <div class="text-center mb-12">
    <h1 class="text-4xl font-bold mb-4">Research Links Database</h1>
    <p class="text-gray-700 dark:text-gray-300 mb-6">
      Welcome to our curated collection of research links. This database contains valuable resources
      related to surviving the singularity and other cutting-edge topics in technology and AI.
    </p>
    <Button color="blue" on:click={() => {researchLinksStore.setSearchTerm('')}}>Contribute a Link</Button>
  </div>

  <div class="mb-8 flex">
    <Input 
      type="text" 
      placeholder="Search links..." 
      bind:value={searchTerm}
      on:keydown={handleKeyDown}
      class="flex-grow"
    />
    <button class="ml-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600" on:click={handleSearch}>Search</button>
  </div>

  <div class="mb-8">
    <button 
      class="w-full text-left"
      on:click={toggleSummary}
    >
      <div class="flex items-center justify-between border-b border-gray-300 dark:border-gray-700 pb-2">
        <h2 class="text-xl font-semibold text-gray-700 dark:text-gray-300">Database Summary</h2>
        <svg 
          class="w-5 h-5 transition-transform duration-200" 
          class:rotate-180={isSummaryExpanded}
          fill="currentColor" 
          viewBox="0 0 20 20"
        >
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </div>
    </button>
    
    {#if isSummaryExpanded}
      <div class="mt-4 rounded-lg px-4 py-6 bg-white dark:bg-gray-800 shadow-md">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="text-center">
            <p class="text-3xl font-semibold text-blue-400">{$researchLinksStore.links.length}</p>
            <p class="text-sm uppercase tracking-wide">Research Links</p>
          </div>
          <div class="text-center">
            <p class="text-3xl font-semibold text-green-400">{uniqueAuthors.size}</p>
            <p class="text-sm uppercase tracking-wide">Unique Authors</p>
          </div>
          <div class="text-center">
            <p class="text-3xl font-semibold text-purple-400">{uniqueTags.size}</p>
            <p class="text-sm uppercase tracking-wide">Unique Tags</p>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <div class="flex flex-wrap justify-center gap-6">
    {#each $researchLinksStore.links as link (link.id)}
      <div class="w-full max-w-sm">
        <ResearchLinkItem {link} />
      </div>
    {/each}
  </div>

  {#if $researchLinksStore.isLoading}
    <div class="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <p class="text-gray-700 dark:text-gray-300">Loading research links...</p>
    </div>
  {:else if $researchLinksStore.links.length === 0}
    <div class="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <p class="text-gray-700 dark:text-gray-300">No research links found.</p>
    </div>
  {/if}

  {#if $researchLinksStore.error}
    <div class="text-center p-6 bg-red-100 dark:bg-red-900 rounded-lg shadow-md">
      <p class="text-red-700 dark:text-red-300">{$researchLinksStore.error}</p>
    </div>
  {/if}
</main>

<style>
  :global(body) {
    background-color: #f0f4f8;
  }
</style>
