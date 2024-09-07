<script>
    import { onMount } from 'svelte';
    import { fade, fly } from 'svelte/transition';
    import YouTubeResourceCard from '$lib/components/YouTubeResourceCard.svelte';
    import Spacer from '$lib/components/Spacer.svelte';
    import { Button } from 'flowbite-svelte';
    import { fetchAndParseCSV } from '$lib/utils/csvParser.js';

    const csvUrl = "/data/ai_singularity_videos.csv";
    let csvSize = "Calculating...";

    let youtubeResources = [];
    let selectedTags = [];
    let filteredVideos = [];
    let showFilters = false;
    let allTags = [];
    let topTags = [];
    let showAllTags = false;

    onMount(async () => {
        youtubeResources = await fetchAndParseCSV(csvUrl);
        processTagsAlgorithmically();
        showFilters = true;
        calculateCSVSize();
    });

    async function calculateCSVSize() {
        try {
            const response = await fetch(csvUrl, { method: 'HEAD' });
            const size = response.headers.get('Content-Length');
            csvSize = size ? `${(size / 1024).toFixed(2)} KB` : "Unknown";
        } catch (error) {
            console.error("Error calculating CSV size:", error);
            csvSize = "Unknown";
        }
    }

    function processTagsAlgorithmically() {
        const tagCounts = {};
        youtubeResources.forEach(video => {
            video.Tags.split(',').forEach(tag => {
                tag = tag.trim();
                tagCounts[tag] = (tagCounts[tag] || 0) + 1;
            });
        });

        allTags = Object.entries(tagCounts)
            .sort((a, b) => b[1] - a[1])
            .map(([tag, count]) => ({ tag, count }));

        topTags = allTags.slice(0, 5);
    }

    $: {
        filteredVideos = youtubeResources.filter(video => 
            selectedTags.length === 0 || selectedTags.some(tag => video.Tags.includes(tag))
        );
    }

    function handleDownloadCSV() {
        window.open(csvUrl, '_blank');
    }

    function toggleTag(tag) {
        selectedTags = selectedTags.includes(tag) 
            ? selectedTags.filter(t => t !== tag)
            : [...selectedTags, tag];
    }

    function toggleShowAllTags() {
        showAllTags = !showAllTags;
    }
</script>

<svelte:head>
    <title>AI and Singularity Videos | Surviving the Singularity</title>
</svelte:head>

<div class="container mx-auto px-4 sm:px-6 lg:px-8 py-12 min-h-screen">
    <Spacer height="50px" />

    <div class="text-center mb-12" in:fly="{{ y: -50, duration: 1000 }}">
        <h1 class="text-4xl sm:text-5xl font-extrabold mb-6">
            AI and Singularity <span class="text-blue-400">Videos</span>
        </h1>
        <p class="text-xl mb-8 max-w-3xl mx-auto" in:fly="{{ y: 50, duration: 1000, delay: 300 }}">
            Explore our curated collection of informative videos about AI, technological singularity, and related topics.
        </p>
        <Button on:click={handleDownloadCSV} class="bg-blue-500 hover:bg-blue-600 text-white transition-all duration-300">
            <div class="flex flex-col items-center">
                <span>Download CSV</span>
                <span class="text-sm">({csvSize})</span>
            </div>
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
            </svg>
        </Button>
    </div>

    {#if showFilters}
        <div class="mb-8 text-center" in:fade="{{ duration: 1000, delay: 600 }}">
            <h2 class="text-2xl font-bold mb-4">Filter by Tags</h2>
            <div class="flex flex-wrap justify-center gap-2 mb-4">
                {#each showAllTags ? allTags : topTags as { tag, count }}
                    <button
                        class="px-3 py-1 rounded-full text-sm font-semibold transition-all duration-300 {selectedTags.includes(tag) ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}"
                        on:click={() => toggleTag(tag)}
                    >
                        {tag} ({count})
                    </button>
                {/each}
            </div>
            <button
                class="text-blue-500 hover:text-blue-600 transition-colors duration-300"
                on:click={toggleShowAllTags}
            >
                {showAllTags ? 'Show Less' : 'Show More'}
            </button>
        </div>
    {/if}

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each filteredVideos as video, i}
            <div in:fly="{{ y: 50, duration: 500, delay: i * 100 }}">
                <YouTubeResourceCard {video} />
            </div>
        {/each}
    </div>

    {#if filteredVideos.length === 0}
        <p class="text-center text-2xl mt-12" in:fade>No videos match the selected filters.</p>
    {/if}
</div>

<style>
    /* Remove all background and text color styles */
</style>