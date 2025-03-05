# Test MDsveX Integration

<script>
  import { onMount } from 'svelte';
  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

This is a test of our new MDsveX integration. It allows us to:

1. Write markdown content
2. Use Svelte components
3. Include dynamic content

<div>
{#if mounted}
The page has loaded successfully!
{:else}
Loading the page...
{/if}
</div>

## Features

- **Markdown Support**: Regular markdown works
- **Svelte Components**: We can use Svelte components
- **Dynamic Content**: We can include reactive variables