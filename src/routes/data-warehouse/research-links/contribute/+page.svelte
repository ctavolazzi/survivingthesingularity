<script>
    import { Card, Button, Heading, P } from 'flowbite-svelte';
    import { ArrowLeftSolid } from 'flowbite-svelte-icons';
    import { goto } from '$app/navigation';
</script>

<svelte:head>
    <title>Contribute Research | Surviving the Singularity</title>
</svelte:head>

<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <Button class="mb-6" color="light" on:click={() => goto('/data-warehouse/research-links')}>
        <ArrowLeftSolid class="mr-2 h-5 w-5" />
        Back to Research Links
    </Button>

    <Card class="p-6 bg-white dark:bg-gray-800">
        <Heading tag="h1" class="mb-6 text-center">Feature Update</Heading>

        <div class="mb-8 text-center">
            <svg class="w-16 h-16 mx-auto mb-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>

            <P size="xl" class="mb-4 font-medium">Direct Research Contributions Have Been Disabled</P>

            <P class="mb-4">
                To ensure the highest quality and security of our data warehouse, we have moved to a curated model where all data is now:
            </P>

            <div class="flex flex-col items-start text-left max-w-xl mx-auto mb-6">
                <div class="flex items-center mb-3">
                    <span class="flex-shrink-0 w-5 h-5 mr-2 text-green-500">✓</span>
                    <span>Algorithmically generated using verified sources</span>
                </div>
                <div class="flex items-center mb-3">
                    <span class="flex-shrink-0 w-5 h-5 mr-2 text-green-500">✓</span>
                    <span>Manually reviewed by our research team</span>
                </div>
                <div class="flex items-center">
                    <span class="flex-shrink-0 w-5 h-5 mr-2 text-green-500">✓</span>
                    <span>Securely uploaded by administrators</span>
                </div>
            </div>

            <P class="mb-6">
                We appreciate your interest in contributing to our knowledge base. If you have research you believe should be included, please contact us through our standard channels with your suggestion.
            </P>

            <div class="flex flex-col sm:flex-row justify-center gap-4">
                <Button on:click={() => goto('/contact')} color="blue">
                    Contact Us
                </Button>
                <Button on:click={() => goto('/data-warehouse')} color="light">
                    Explore Data Warehouse
                </Button>
            </div>
        </div>
    </Card>
</div>

<style>
    /* don't put global styles here for now */
</style>