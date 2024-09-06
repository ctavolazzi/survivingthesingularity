<script>
  import { Card } from 'flowbite-svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import NewsletterPopup from '$lib/components/NewsletterPopup.svelte';
  import NewsletterNavigation from '$lib/components/NewsletterNavigation.svelte';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';

  export let data;
  const { latestNewsletter, error } = data;

  let edition, month, year;

  if (latestNewsletter && latestNewsletter.filename) {
    const match = latestNewsletter.filename.match(/newsletter_(\d+)_(\w+)_(\d{4})\.md/);
    if (match) {
      [, edition, month, year] = match;
    }
  }
</script>

<svelte:head>
  <title>Surviving the Singularity Newsletter {edition ? `- Edition ${edition}` : ''}</title>
</svelte:head>

<div class="spacer" />

<main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
  {#if error}
    <Card class="mb-8 max-w-4xl mx-auto bg-red-100 border-red-400">
      <p class="text-red-700">{error}</p>
    </Card>
  {:else if latestNewsletter}
    <Card class="mb-8 max-w-4xl mx-auto">
      <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-2 text-primary-600 dark:text-primary-400">
        Surviving the Singularity Newsletter
      </h1>
      {#if edition && month && year}
        <h2 class="text-xl sm:text-2xl md:text-3xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          Edition {edition} - {month} {year}
        </h2>
      {/if}

      {@html latestNewsletter.content}
    </Card>
  {:else}
    <Card class="mb-8 max-w-4xl mx-auto">
      <p class="text-gray-700 dark:text-gray-300">No newsletter available at this time.</p>
    </Card>
  {/if}
</main>

<style>
  .spacer {
    height: 50px;
  }

  @media (max-width: 640px) {
    .spacer {
      height: 30px;
    }
  }

  :global(.newsletter-signup) {
    margin-top: 2rem;
    margin-bottom: 2rem;
  }

  :global(.skool-group) {
    margin-top: 2rem;
    margin-bottom: 2rem;
  }
</style>