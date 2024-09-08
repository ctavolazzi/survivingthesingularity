<script lang="ts">
    import { onMount } from 'svelte';
    import { supabase } from '$lib/utils/supabaseClient';
    import { Button } from 'flowbite-svelte';
    import ResearchLinkItem from '$lib/components/ResearchLinkItem.svelte';

    let researchLinks = [];

    async function fetchResearchLinks() {
      console.log('Fetching research links');
      const { data, error } = await supabase
        .from('research_links')
        .select('*');

      if (error) {
        console.error('Error fetching research links:', error);
      } else {
        researchLinks = data;
      }
      console.log(researchLinks);
    }

    onMount(() => {
      fetchResearchLinks();
    });
  </script>
  
  <svelte:head>
    <title>Research Links | Surviving the Singularity</title>
  </svelte:head>
  
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl sm:text-5xl font-extrabold mb-2 text-gray-900 dark:text-gray-100">
      Research Links
    </h1>
    <p class="text-xl mb-6 text-gray-600 dark:text-gray-300 max-w-3xl">
      Explore our curated collection of research links.
    </p>
    <div class="flex space-x-4 mb-8">
      <Button color="light" href="/data-warehouse/research-links/contribute" class="flex items-center">
        Add Research Link
      </Button>
    </div>
  
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {#each researchLinks as link}
        <ResearchLinkItem {link} />
      {/each}
    </div>
  </div>