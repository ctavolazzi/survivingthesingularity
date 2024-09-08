<script lang="ts">
    import { onMount } from 'svelte';
    import { Card, Badge } from 'flowbite-svelte';
    export let link;

    let fallbackTitle = '';

    onMount(async () => {
        if (!link.title) {
            fallbackTitle = await fetchPageTitle(link.url);
        }
    });

    async function fetchPageTitle(url) {
        try {
            const response = await fetch(`/api/fetch-title?url=${encodeURIComponent(url)}`);
            const data = await response.json();
            return data.title || new URL(url).hostname;
        } catch (error) {
            console.error('Error fetching page title:', error);
            return new URL(url).hostname;
        }
    }

    function formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }

    function handleClick() {
        window.open(link.url, '_blank', 'noopener,noreferrer');
    }

    function parseTags(tags) {
        if (typeof tags === 'string') {
            try {
                return JSON.parse(tags);
            } catch (e) {
                console.error('Error parsing tags:', e);
                return tags.split(',').map(tag => tag.trim());
            }
        }
        return Array.isArray(tags) ? tags : [];
    }
</script>



<Card class="mb-4 cursor-pointer hover:shadow-lg transition-shadow duration-300" on:click={handleClick}>
    <a href={link.url} target="_blank" rel="noopener noreferrer" class="block">
      <h3 class="text-xl font-semibold mb-2 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
          {link.title || fallbackTitle || 'Loading...'}
      </h3>
    </a>
    
    {#if link.description}
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
            {link.description}
        </p>
    {/if}
    
    <div class="flex flex-wrap items-center gap-2 mb-3">
        {#if link.author}
            <Badge color="dark">By {link.author}</Badge>
        {/if}
        {#if link.date_of_publication}
            <Badge color="purple">Published: {formatDate(link.date_of_publication)}</Badge>
        {/if}
    </div>
    
    {#if link.tags}
        <div class="flex flex-wrap gap-2 mb-3">
            {#each parseTags(link.tags) as tag}
                <Badge color="indigo">{tag}</Badge>
            {/each}
        </div>
    {/if}
    
    {#if link.notes}
        <p class="italic text-sm text-gray-600 dark:text-gray-300 border-l-4 border-gray-300 pl-3 mt-3">
            {link.notes}
        </p>
    {/if}
</Card>