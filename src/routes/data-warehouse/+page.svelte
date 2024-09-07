<script>
    import { dataResources } from '$lib/data/dataResources.js';
    import Spacer from '$lib/components/Spacer.svelte';
    import { Card, Button, Badge, Tooltip } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    function handleViewDataset(link) {
        goto(link);
    }

    function handleDownloadCSV(csvUrl) {
        window.open(csvUrl, '_blank');
    }

    let csvSizes = {};

    async function calculateCSVSize(resource) {
        if (!csvSizes[resource.csvUrl]) {
            csvSizes[resource.csvUrl] = resource.getCSVSize 
                ? await resource.getCSVSize() 
                : resource.csvSize;
            csvSizes = csvSizes; // Trigger reactivity
        }
    }

    onMount(() => {
        dataResources.forEach(calculateCSVSize);
    });
</script>

<svelte:head>
    <title>Data Resources | Surviving the Singularity</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <Spacer height="3rem" />

    <h1 class="text-4xl sm:text-5xl font-extrabold mb-4 text-gray-900 dark:text-gray-100">
        Explore Our <span class="text-blue-600 dark:text-blue-400">Data Resources</span>
    </h1>
    <p class="text-xl mb-12 text-gray-600 dark:text-gray-300 max-w-3xl">
        Dive into our curated collection of AI and robotics datasets. These resources provide valuable insights into the rapidly evolving world of technology.
    </p>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each dataResources as resource}
            <Card class="hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <div class="flex flex-col h-full">
                    <div class="flex items-center mb-4">
                        <span class="icon-container mr-4 text-blue-600 dark:text-blue-400 p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
                            {@html resource.icon.svg}
                        </span>
                        <h2 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{resource.title}</h2>
                    </div>
                    <p class="mb-6 text-gray-700 dark:text-gray-300 flex-grow">
                        {resource.description}
                    </p>
                    <div class="flex flex-wrap gap-2 mb-4">
                        {#each resource.tags as tag}
                            <Badge color="blue" class="text-xs font-semibold">{tag}</Badge>
                        {/each}
                    </div>
                    <div class="flex justify-between items-center text-sm text-gray-600 dark:text-gray-400 mb-6">
                        <span>Updated: {resource.lastEdited}</span>
                        <span class="font-medium">{resource.entries.toLocaleString()} entries</span>
                    </div>
                    <div class="mt-4 space-y-2">
                        <Button on:click={() => handleViewDataset(resource.link)} class="w-full bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600">
                            {resource.buttonText}
                            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                            </svg>
                        </Button>
                        <Button 
                            on:click={() => handleDownloadCSV(resource.csvUrl)} 
                            class="w-full bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300"
                        >
                            Download CSV 
                            {#if csvSizes[resource.csvUrl]}
                                ({csvSizes[resource.csvUrl]})
                            {:else}
                                (Calculating...)
                            {/if}
                            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                            </svg>
                        </Button>
                    </div>
                </div>
            </Card>
        {/each}
    </div>
</div>

<style>
    .icon-container :global(svg) {
        @apply w-8 h-8;
    }
</style>