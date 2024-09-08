<script>
    import { onMount } from 'svelte';
    import Papa from 'papaparse';
    import ProjectionCard from '$lib/components/ProjectionCard.svelte';

    let projections = [];

    onMount(async () => {
        const response = await fetch('/data/future_projections.csv');
        const csv = await response.text();
        const result = Papa.parse(csv, { header: true });
        projections = result.data;
    });
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-4xl font-bold mb-8">Future Projections</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each projections as projection}
            <ProjectionCard
                title={projection.Title}
                description={projection.Description}
                publicationDate={projection.PublicationDate}
                organization={projection.Organization}
                link={projection.Link}
            />
        {/each}
    </div>
</div>