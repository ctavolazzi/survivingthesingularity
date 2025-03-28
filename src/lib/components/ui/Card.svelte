<!--
  Card.svelte
  A reusable card component for displaying content in a consistent way
-->

<script>
  // Card variants
  export let variant = "default"; // default, elevated, outline, feature

  // Card dimensions
  export let padding = "md"; // sm, md, lg, none
  export let fullWidth = false;

  // Card styling
  export let rounded = true;
  export let elevation = "md"; // none, sm, md, lg
  export let hoverable = false;
  export let clickable = false;

  // If href is provided, the card becomes a link
  export let href = "";

  // Determine CSS classes based on props
  const paddings = {
    none: "p-0",
    sm: "p-3",
    md: "p-4",
    lg: "p-6"
  };

  const elevations = {
    none: "shadow-none",
    sm: "shadow-sm",
    md: "shadow-md",
    lg: "shadow-lg"
  };

  const variants = {
    default: "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700",
    elevated: "bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700",
    outline: "bg-transparent border border-gray-200 dark:border-gray-700",
    feature: "bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 border border-gray-200 dark:border-gray-700"
  };

  // Combine all classes
  $: classList = [
    variants[variant] || variants.default,
    paddings[padding] || paddings.md,
    elevations[elevation] || elevations.md,
    rounded ? "rounded-lg" : "",
    hoverable ? "transition-transform hover:-translate-y-1 hover:shadow-lg" : "",
    clickable ? "cursor-pointer" : "",
    fullWidth ? "w-full" : "",
    $$props.class || ""
  ].filter(Boolean).join(" ");
</script>

{#if href}
  <a {href} class={classList}>
    <slot />
  </a>
{:else}
  <div class={classList}>
    <slot />
  </div>
{/if}

<style>
  /* Ensure proper nesting of cards */
  :global(.card > .card) {
    margin: 0;
  }
</style>