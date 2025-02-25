<script>
  /**
   * Checkbox component that provides consistent styling and behavior
   * @component
   */

  export let id = '';
  export let name = id;
  export let label = '';
  export let checked = false;
  export let disabled = false;
  export let required = false;
  export let error = '';

  // Generate a unique ID if none provided
  if (!id) {
    id = `checkbox-${Math.random().toString(36).substring(2, 11)}`;
    name = id;
  }

  // Import createEventDispatcher to dispatch events
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function handleChange(event) {
    checked = event.target.checked;
    dispatch('change', { checked });
  }
</script>

<div class="flex items-start mb-4">
  <div class="flex items-center h-5">
    <input
      type="checkbox"
      {id}
      {name}
      {disabled}
      {required}
      {checked}
      on:change={handleChange}
      class="w-4 h-4 bg-gray-50 rounded border
             focus:ring-3 focus:ring-blue-300
             dark:bg-gray-700 dark:border-gray-600
             dark:focus:ring-blue-600
             {error ? 'border-red-500' : 'border-gray-300 dark:border-gray-500'}"
      aria-invalid={error ? 'true' : 'false'}
      aria-describedby={error ? `${id}-error` : undefined}
    />
  </div>

  <div class="ml-3 text-sm">
    {#if label}
      <label for={id} class="font-medium text-gray-900 dark:text-gray-300 select-none">
        {label}
        {#if required}
          <span class="text-red-500">*</span>
        {/if}
      </label>
    {/if}

    {#if error}
      <p id="{id}-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>
    {/if}

    {#if $$slots.default}
      <div class="text-gray-500 dark:text-gray-400">
        <slot />
      </div>
    {/if}
  </div>
</div>