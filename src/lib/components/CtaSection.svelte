<!-- src/lib/components/CtaSection.svelte -->
<script>
  import { fade } from 'svelte/transition';
  import { createEventDispatcher } from 'svelte';

  export let text = "Ready to face the future? Join our newsletter to begin your journey!";
  export let buttonText = "Start Now";
  export let useFade = true;
  export let buttonClass = "cta-button";

  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch('click');
  }
</script>

<div class="cta-section" class:fade-in={useFade} use:fade="{{ duration: 1000, delay: 900 }}">
  <p>{text}</p>
  <button 
    class={buttonClass} 
    on:click={handleClick}
    aria-label={buttonText}
  >
    <slot>{buttonText}</slot>
  </button>
</div>

<style>
  .cta-section {
    text-align: center;
    margin-top: 3rem;
  }

  .cta-section p {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
  }

  .cta-button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
    background: none;
    border: none;
    color: inherit;
    font: inherit;
  }

  .cta-button:hover {
    text-decoration: underline;
  }

  .cta-button:focus {
    outline: 2px solid currentColor;
    outline-offset: 2px;
  }
</style>
