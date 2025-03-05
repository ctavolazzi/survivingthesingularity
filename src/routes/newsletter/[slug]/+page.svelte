<script>
  import NewsletterLayout from '$lib/components/NewsletterLayout.svelte';
  import NewsletterContent from '$lib/components/NewsletterContent.svelte';

  export let data;
</script>

<svelte:head>
  <title>{data.newsletter.title} | Surviving the Singularity</title>
  <meta name="description" content="Read {data.newsletter.title}, a newsletter about surviving the singularity." />
</svelte:head>

<NewsletterLayout newsletters={data.allNewsletters} currentSlug={data.newsletter.slug} pagination={null}>
  <NewsletterContent
    content={data.newsletter.content}
    metadata={{
      title: data.newsletter.title,
      date: data.newsletter.date
    }}
  />
</NewsletterLayout>
