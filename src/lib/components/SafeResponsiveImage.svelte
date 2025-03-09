<!--
  SafeResponsiveImage.svelte
  A safer wrapper for ResponsiveImage component that ensures all values are
  properly converted to strings before being passed down.
-->

<script lang="ts">
  import ResponsiveImage from './ResponsiveImage.svelte';

  // Image sources - ensure all are strings
  export let src = "";
  export let srcWebp = "";
  export let srcset = "";
  export let srcsetWebp = "";
  export let sizes = "";

  // Standard image attributes
  export let alt = "";
  export let width: number | undefined = undefined;
  export let height: number | undefined = undefined;
  export let loading: "lazy" | "eager" = "lazy";
  export let decoding: "async" | "sync" | "auto" = "async";

  // Handle class properly
  let cssClass = "";
  export { cssClass as class };

  // Ensure all values are strings
  $: safeProps = {
    src: String(src || ""),
    srcWebp: String(srcWebp || ""),
    srcset: String(srcset || ""),
    srcsetWebp: String(srcsetWebp || ""),
    sizes: String(sizes || ""),
    alt: String(alt || ""),
    width,
    height,
    loading,
    decoding,
    class: cssClass
  };
</script>

<ResponsiveImage
  src={safeProps.src}
  srcWebp={safeProps.srcWebp}
  srcset={safeProps.srcset}
  srcsetWebp={safeProps.srcsetWebp}
  sizes={safeProps.sizes}
  alt={safeProps.alt}
  width={safeProps.width}
  height={safeProps.height}
  loading={safeProps.loading}
  decoding={safeProps.decoding}
  class={safeProps.class}
/>