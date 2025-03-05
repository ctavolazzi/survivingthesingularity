<script>
  import NewsletterLayout from '$lib/components/NewsletterLayout.svelte';
  import NewsletterContent from '$lib/components/NewsletterContent.svelte';
  import { getNewsletterComponent } from '$lib/utils/newsletterLoader';

  export let data;

  // Get the component for this newsletter
  const newsletterComponent = getNewsletterComponent(data.newsletter.slug);
</script>

<svelte:head>
  <title>{data.newsletter.title} | Surviving the Singularity</title>
  <meta name="description" content={data.newsletter.description || 'Read our newsletter about surviving the singularity.'} />
</svelte:head>

<NewsletterLayout newsletters={data.allNewsletters} currentSlug={data.newsletter.slug}>
  <NewsletterContent
    component={newsletterComponent}
    metadata={{
      title: data.newsletter.title,
      date: data.newsletter.date,
      description: data.newsletter.description
    }}
  />
</NewsletterLayout>
