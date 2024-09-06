<script>
  import { onMount } from 'svelte';

  export let currentEdition = null;
  let editions = [];

  onMount(async () => {
    try {
      const response = await fetch('/api/newsletters');
      if (!response.ok) throw new Error('Failed to fetch newsletters');
      const data = await response.json();
      editions = data.editions;
    } catch (error) {
      console.error('Error fetching newsletter editions:', error);
    }
  });
</script>

<nav class="mt-8">
  <h2 class="text-2xl font-semibold mb-4">Newsletter Editions</h2>
  <div class="flex flex-wrap gap-4">
    {#each editions as edition}
      <a
        href="/newsletter/{edition}"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 {edition === currentEdition ? 'bg-blue-700' : ''}"
      >
        Edition {edition}
      </a>
    {/each}
  </div>
</nav>