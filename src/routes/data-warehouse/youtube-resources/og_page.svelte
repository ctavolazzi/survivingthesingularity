<script>
    import { youtubeResources } from '$lib/data/youtubeResources.js';
    import YouTubeResourceCard from '$lib/components/YouTubeResourceCard.svelte';
    import Spacer from '$lib/components/Spacer.svelte';
    import { Button } from 'flowbite-svelte';

    const csvUrl = "/data/ai_singularity_videos.csv";
    const csvSize = "2 KB"; // Update this with the actual file size

    function handleDownloadCSV() {
        window.open(csvUrl, '_blank');
    }
</script>

<svelte:head>
    <title>AI and Singularity Videos | Surviving the Singularity</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <Spacer height="50px" />

    <div class="flex items-center justify-between mb-6">
        <h1 class="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-gray-100">
            AI and Singularity <span class="text-blue-600 dark:text-blue-400">Videos</span>
        </h1>
        <Button on:click={handleDownloadCSV} class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300">
            <div class="flex flex-col items-center">
                <span>Download CSV</span>
                <span class="text-sm">({csvSize})</span>
            </div>
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
            </svg>
        </Button>
    </div>

    <p class="text-xl mb-12 text-gray-600 dark:text-gray-300 max-w-3xl">
        Explore our curated collection of informative videos about AI, technological singularity, and related topics.
    </p>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        {#each youtubeResources as video}
            <YouTubeResourceCard {video} />
        {/each}
    </div>
</div>