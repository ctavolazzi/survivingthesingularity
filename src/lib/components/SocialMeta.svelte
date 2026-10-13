<script>
  import { page } from '$app/stores';
  import { canonicalShareUrl, SITE_URL } from '$lib/share.js';

  export let title;
  export let description;
  export let type = 'article';
  export let image = '/images/og/blog.png';
  export let imageAlt = 'Surviving the Singularity: essays and analysis.';

  $: canonical = canonicalShareUrl($page.url.pathname);
  $: imageUrl = new URL(image, SITE_URL).href;
</script>

<!-- A page renders this once. Share controls deliberately emit no head tags. -->
<svelte:head>
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:type" content={type} />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:url" content={canonical} />
  <meta property="og:image" content={imageUrl} />
  <meta property="og:image:secure_url" content={imageUrl} />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="2400" />
  <meta property="og:image:height" content="1260" />
  <meta property="og:image:alt" content={imageAlt} />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={imageUrl} />
  <meta name="twitter:image:alt" content={imageAlt} />
</svelte:head>
