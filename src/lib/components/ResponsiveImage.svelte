<!--
  ResponsiveImage.svelte
  A utility component for rendering responsive images with WebP support and proper srcset

  Features:
  - WebP support with automatic fallback
  - Multiple sizes for different viewport widths
  - Lazy loading by default with option to load eagerly
  - Alt text for accessibility
-->

<script lang="ts">
  // Image sources
  export let src = ""; // Original/fallback image path

  // Optional WebP version for better performance
  export let srcWebp = "";

  // Responsive image sizes (can be empty for non-responsive images)
  export let srcset = "";
  export let srcsetWebp = "";

  // How the browser should choose which image to load
  export let sizes = ""; // e.g. "(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"

  // Standard image attributes
  export let alt = "";
  export let width: number | undefined = undefined;
  export let height: number | undefined = undefined;

  // Define valid loading and decoding values
  type LoadingType = "lazy" | "eager";
  type DecodingType = "async" | "sync" | "auto";

  export let loading: LoadingType = "lazy"; // Use "eager" for above-the-fold images
  export let decoding: DecodingType = "async";

  // Handle class properly - In Svelte, we use class directly
  let cssClass = "";
  export { cssClass as class };

  // Determine what type of image to render based on available props
  const hasWebP = srcWebp !== "";
  const hasSrcset = srcset !== "";
  const hasSrcsetWebP = srcsetWebp !== "";
</script>

{#if hasWebP || hasSrcsetWebP}
  <!-- If we have WebP versions, use the picture element for format fallback -->
  <picture>
    {#if hasSrcsetWebP}
      <source type="image/webp" {sizes} srcset={srcsetWebp} />
    {:else if hasWebP}
      <source type="image/webp" srcset={srcWebp} />
    {/if}

    {#if hasSrcset}
      <img
        {src}
        srcset={srcset}
        {sizes}
        {alt}
        {width}
        {height}
        {loading}
        {decoding}
        class={cssClass}
      />
    {:else}
      <img
        {src}
        {alt}
        {width}
        {height}
        {loading}
        {decoding}
        class={cssClass}
      />
    {/if}
  </picture>
{:else}
  <!-- Standard image without WebP -->
  {#if hasSrcset}
    <img
      {src}
      srcset={srcset}
      {sizes}
      {alt}
      {width}
      {height}
      {loading}
      {decoding}
      class={cssClass}
    />
  {:else}
    <!-- Regular non-responsive image -->
    <img
      {src}
      {alt}
      {width}
      {height}
      {loading}
      {decoding}
      class={cssClass}
    />
  {/if}
{/if}