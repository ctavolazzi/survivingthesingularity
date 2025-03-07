<script>
  import { page } from '$app/stores';
</script>

<svelte:head>
  <!-- Default Open Graph tags that will be overridden by individual blog posts if needed -->
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:type" content="article" />

  <!-- Twitter Card default tags -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@survivingthesingularity" />
</svelte:head>

<slot />