<script>
  import NewsletterLayout from '$lib/components/NewsletterLayout.svelte';
  import NewsletterContent from '$lib/components/NewsletterContent.svelte';

  export let data;
</script>

<svelte:head>
  <title>Surviving the Singularity Newsletters</title>
  <meta name="description" content="Browse our collection of newsletters about surviving the singularity." />
</svelte:head>

<NewsletterLayout newsletters={data.newsletters} currentSlug={data.latestNewsletter.slug}>
  <NewsletterContent 
    content={data.latestNewsletter.content}
    metadata={{
      title: data.latestNewsletter.title,
      date: data.latestNewsletter.date,
      description: data.latestNewsletter.description
    }}
  />
</NewsletterLayout>
