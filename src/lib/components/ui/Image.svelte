<!--
  Image.svelte
  A simplified image component that builds on top of SafeResponsiveImage.
  This component makes it easy to use optimized images with minimal props.
-->

<script lang="ts">
  import SafeResponsiveImage from '../SafeResponsiveImage.svelte';

  // Main image source (required)
  export let src = "";

  // Alt text for accessibility (required for non-decorative images)
  export let alt = "";

  // Optional props
  export let width: number | undefined = undefined;
  export let height: number | undefined = undefined;
  export let loading: "lazy" | "eager" = "lazy";

  // Additional styling
  let cssClass = "";
  export { cssClass as class };

  // Optional caption text
  export let caption = "";

  // Border options
  export let border = false;
  export let rounded = true;

  // Hover effects
  export let hoverEffect = false; // Scale on hover

  // Shadow options
  export let shadow = false;

  // WebP version - DO NOT auto-generate to prevent 404 errors
  export let srcWebp = "";

  // Combine classes
  $: combinedClass = [
    cssClass,
    rounded ? 'rounded' : '',
    border ? 'border border-gray-200 dark:border-gray-700' : '',
    shadow ? 'shadow-md' : '',
    hoverEffect ? 'transition-transform hover:scale-[1.02]' : ''
  ].filter(Boolean).join(' ');
</script>

<figure class="image-container">
  <SafeResponsiveImage
    {src}
    {srcWebp}
    {alt}
    {width}
    {height}
    {loading}
    class={combinedClass}
  />

  {#if caption}
    <figcaption class="text-sm text-gray-600 dark:text-gray-400 mt-2 text-center">
      {caption}
    </figcaption>
  {/if}
</figure>

<style>
  .image-container {
    display: block;
    max-width: 100%;
    position: relative;
  }
</style>