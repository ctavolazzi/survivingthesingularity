<script>
    import { Card, Button, Badge } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
    export let tactic;

    function navigateToTactic() {
        console.log('Navigating to:', `/tactics/${tactic.slug}`);
        goto(`/tactics/${tactic.slug}`);
    }
</script>

<Card img={tactic.image_url} horizontal>
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        {tactic.title}
    </h5>
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
        {tactic.summary}
    </p>
    <p class="mb-3 text-sm text-gray-600 dark:text-gray-300">
        {tactic.description}
    </p>
    <p class="mb-2"><span class="font-semibold">Category:</span> {tactic.category}</p>
    <div class="mb-3">
        {#each tactic.tags as tag}
            <Badge color="blue" class="mr-2">{tag}</Badge>
        {/each}
    </div>
    {#if tactic.resources}
        <div class="mb-3">
            <h6 class="mb-2 font-semibold">Resources:</h6>
            {#each JSON.parse(tactic.resources) as resource}
                <a href={resource.url} class="text-blue-600 hover:underline dark:text-blue-500" target="_blank" rel="noopener noreferrer">
                    {resource.description} ({resource.type})
                </a>
            {/each}
        </div>
    {/if}
    <p class="mb-3"><span class="font-semibold">Status:</span> {tactic.status}</p>
    <Button on:click={navigateToTactic}>
        Learn more
        <svg class="w-3.5 h-3.5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </Button>
</Card>