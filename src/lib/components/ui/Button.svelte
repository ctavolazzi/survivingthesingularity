<script>
  /**
   * Button component that provides consistent styling and behavior
   * @component
   */

  export let variant = 'primary'; // primary, secondary, outline, text
  export let size = 'md'; // sm, md, lg
  export let type = 'button';
  export let disabled = false;
  export let fullWidth = false;
  export let loading = false;
  export let icon = null; // Optional icon name

  // Style configurations for different variants
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white border-transparent',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800 border-transparent dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-white',
    outline: 'bg-transparent border-current hover:bg-gray-100 text-blue-600 dark:text-blue-400 dark:hover:bg-gray-800',
    text: 'bg-transparent hover:bg-gray-100 text-blue-600 border-transparent dark:text-blue-400 dark:hover:bg-gray-800'
  };

  // Size configurations
  const sizes = {
    sm: 'py-1 px-3 text-sm',
    md: 'py-2 px-4 text-base',
    lg: 'py-3 px-6 text-lg'
  };

  // Base classes that apply to all buttons
  const baseClasses = 'rounded font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed border';

  // Classes for width
  const widthClass = fullWidth ? 'w-full' : '';

  // Combined classes based on props
  const classes = `${baseClasses} ${variants[variant]} ${sizes[size]} ${widthClass} ${$$props.class || ''}`;
</script>

<button
  {type}
  {disabled}
  class={classes}
  on:click
  on:mouseover
  on:focus
  aria-disabled={disabled || loading}
>
  {#if loading}
    <span class="inline-block animate-spin mr-2">&#8635;</span>
  {/if}

  {#if icon && !loading}
    <span class="inline-block mr-2">{icon}</span>
  {/if}

  <slot />
</button>