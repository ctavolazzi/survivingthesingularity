<script lang="ts">
  import { onMount } from 'svelte';
  import Papa from 'papaparse';
  import ResearchLinkItem from '$lib/components/ResearchLinkItem.svelte';
  import { Button } from 'flowbite-svelte';
  import { goto } from '$app/navigation';

  let researchLinks = [];
  let uniqueAuthors = new Set();
  let uniqueTags = new Set();

  onMount(async () => {
    const response = await fetch('/data/research_links.csv');
    const csvText = await response.text();
    const result = Papa.parse(csvText, { header: true });
    researchLinks = result.data.filter(link => link.title && link.title.trim() !== '');
    
    // Reset sets before recalculating
    uniqueAuthors = new Set();
    uniqueTags = new Set();
    
    researchLinks.forEach(link => {
      if (link.author) {
        // Split authors if there are multiple and add each
        link.author.split(',').forEach(author => uniqueAuthors.add(author.trim()));
      }
      if (link.tags) {
        try {
          // Parse tags and add each to the set
          JSON.parse(link.tags).forEach(tag => uniqueTags.add(tag.trim()));
        } catch (e) {
          console.error('Error parsing tags for link:', link.title, e);
        }
      }
    });

    // Force reactivity update
    uniqueAuthors = uniqueAuthors;
    uniqueTags = uniqueTags;
  });
</script>

<main class="container mx-auto px-4 py-8 max-w-4xl">
  <div class="text-center mb-12">
    <h1 class="text-4xl font-bold mb-4">Research Links Database</h1>
    <p class="text-gray-700 dark:text-gray-300 mb-6">
      Welcome to our curated collection of research links. This database contains valuable resources
      related to surviving the singularity and other cutting-edge topics in technology and AI.
    </p>
    <Button color="blue" on:click={() => goto('/data-warehouse/research-links/contribute')}>Contribute a Link</Button>
  </div>

  <div class="rounded-lg mb-8 px-4">
    <h2 class="text-2xl font-bold mb-4 border-b border-gray-700 pb-2">Database Summary</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="text-center">
        <p class="text-3xl font-semibold text-blue-400">{researchLinks.length}</p>
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

  <div class="flex flex-wrap justify-center gap-6">
    {#each researchLinks as link (link.id)}
      {#if link.title && link.title.trim() !== ''}
        <div class="w-full max-w-sm">
          <ResearchLinkItem {link} />
        </div>
      {/if}
    {/each}
  </div>

  {#if researchLinks.length === 0}
    <div class="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <p class="text-gray-700 dark:text-gray-300">
        {researchLinks === null ? 'Loading research links...' : 'No research links found.'}
      </p>
    </div>
  {/if}
</main>

<style>
  :global(body) {
    background-color: #f0f4f8;
  }
</style>
