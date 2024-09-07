<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';
  import { Button, Card, Input, Badge } from 'flowbite-svelte';

  export let newsletters = [];
  export let selectedSlug = '';
  
  const dispatch = createEventDispatcher();

  let searchTerm = '';
  let visibleCount = 12; // Increased initial visible count
  let listContainer;
  let showBackToTop = false;
  let isLoading = false;

  $: filteredNewsletters = newsletters.filter(newsletter => 
    newsletter.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    newsletter.date?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    newsletter.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  $: visibleNewsletters = filteredNewsletters.slice(0, visibleCount);

  $: totalEditions = newsletters.length;

  function selectNewsletter(slug) {
    dispatch('select', slug);
  }

  async function loadMore() {
    if (isLoading) return;
    isLoading = true;
    await new Promise(resolve => setTimeout(resolve, 300)); // Simulate network delay
    visibleCount += 12; // Load more items
    isLoading = false;
  }

  function handleScroll() {
    showBackToTop = listContainer?.scrollTop > 300;
    if (listContainer?.scrollHeight - listContainer?.scrollTop <= listContainer?.clientHeight + 200) {
      loadMore();
    }
  }

  onMount(() => {
    listContainer?.addEventListener('scroll', handleScroll);
    return () => {
      listContainer?.removeEventListener('scroll', handleScroll);
    };
  });
</script>

<div class="newsletter-list p-4 w-full min-w-[320px] lg:w-[80%] xl:w-[70%] mx-auto">
  <h2 class="text-3xl font-bold mb-6 flex items-center justify-between">
    Editions 
    <Badge color="blue" size="xl">{totalEditions} total</Badge>
  </h2>
  
  <Input
    type="text"
    placeholder="Search newsletters..."
    bind:value={searchTerm}
    class="mb-6 w-full"
  />
  
  <div class="space-y-6">
    {#each visibleNewsletters as newsletter (newsletter.slug)}
      <div 
        class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow hover:shadow-md transition-shadow w-full cursor-pointer"
        class:border-blue-500={newsletter.slug === selectedSlug}
        on:click={() => selectNewsletter(newsletter.slug)}
      >
        <div class="flex flex-wrap justify-between items-start mb-4">
          <h3 class="text-2xl font-semibold">Edition {newsletter.editionNumber}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">{newsletter.date}</p>
        </div>
        <p class="text-xl mb-4">{newsletter.title}</p>
        <p class="text-gray-700 dark:text-gray-300 mb-6">{newsletter.description}</p>
        <button 
          class="text-blue-600 dark:text-blue-400 font-medium text-lg"
          on:click|stopPropagation={() => selectNewsletter(newsletter.slug)}
        >
          Read More
        </button>
      </div>
    {/each}
  </div>
  
  {#if visibleNewsletters.length < filteredNewsletters.length}
    <button 
      class="mt-8 w-full py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-lg font-semibold"
      on:click={loadMore}
    >
      Load More
    </button>
  {/if}
</div>

<style>
  .newsletter-list {
    display: flex;
    flex-direction: column;
  }
</style>