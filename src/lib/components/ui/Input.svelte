<script>
  /**
   * Input component that provides consistent styling and behavior
   * @component
   */

  export let type = 'text';
  export let value = '';
  export let placeholder = '';
  export let label = '';
  export let id = '';
  export let name = id;
  export let required = false;
  export let disabled = false;
  export let error = '';
  export let helpText = '';
  export let autocomplete = '';

  // Generate a unique ID if none provided
  if (!id) {
    id = `input-${Math.random().toString(36).substring(2, 11)}`;
    name = id;
  }

  // Handle input changes manually instead of using bind:value
  function handleInput(event) {
    value = event.target.value;
    dispatch('input', event);
  }

  // Import createEventDispatcher to dispatch events
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
</script>

<div class="mb-4">
  {#if label}
    <label for={id} class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">
      {label}
      {#if required}
        <span class="text-red-500">*</span>
      {/if}
    </label>
  {/if}

  <input
    {type}
    {id}
    {name}
    {placeholder}
    {disabled}
    {required}
    {autocomplete}
    {value}
    on:input={handleInput}
    class="bg-gray-50 border text-gray-900 text-sm rounded-lg block w-full p-2.5
           dark:bg-gray-700 dark:text-white dark:placeholder-gray-400
           focus:ring-2 focus:outline-none focus:ring-opacity-50
           disabled:opacity-50 disabled:cursor-not-allowed
           {error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500 dark:border-gray-600'}"
    aria-invalid={error ? 'true' : 'false'}
    aria-describedby={error ? `${id}-error` : (helpText ? `${id}-help` : undefined)}
    on:focus
    on:blur
  />

  {#if error}
    <p id="{id}-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>
  {:else if helpText}
    <p id="{id}-help" class="mt-1 text-sm text-gray-500 dark:text-gray-400">{helpText}</p>
  {/if}
</div>