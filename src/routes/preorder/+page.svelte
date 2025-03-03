<script>
  import { Button, Card, P, Heading } from 'flowbite-svelte';
  import { goto } from '$app/navigation';
</script>

<svelte:head>
  <title>Campaign Concluded | Surviving the Singularity</title>
  <meta name="description" content="The Surviving the Singularity Kickstarter campaign has concluded. Learn more about the book and other resources." />
</svelte:head>

<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
  <Card class="p-8 bg-white dark:bg-gray-800">
    <div class="text-center mb-8">
      <svg class="w-16 h-16 mx-auto mb-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>

      <Heading tag="h1" class="mb-4">Campaign Concluded</Heading>

      <div class="mb-6">
        <P size="xl" class="mb-4">
          Thank you for your interest in the <span class="font-semibold">Surviving the Singularity</span> book.
        </P>

        <P class="mb-4">
          Our crowdfunding campaign has concluded. We're now focused on delivering high-quality resources to help you prepare for the coming technological changes.
        </P>

        <P>
          Please explore our other resources and consider signing up for our newsletter to stay updated on new developments.
        </P>
      </div>

      <div class="flex flex-col sm:flex-row justify-center gap-4 mt-8">
        <Button color="blue" on:click={() => goto('/newsletter')}>
          Subscribe to Updates
        </Button>
        <Button color="light" on:click={() => goto('/sample')}>
          Read Sample Content
        </Button>
        <Button color="light" on:click={() => goto('/data-warehouse')}>
          Explore Data Warehouse
        </Button>
      </div>
    </div>
  </Card>
</div>