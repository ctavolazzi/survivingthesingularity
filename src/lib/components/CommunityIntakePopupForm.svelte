<script>
  import HookEmPopup from './HookEmPopup.svelte';
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';

  export let ctaText = "Ready to join the rebellion against the singularity?";
  export let buttonText = "Enlist Now";

  let isPopupOpen = false;
  const dispatch = createEventDispatcher();

  function showPopup() {
    isPopupOpen = true;
  }

  function closePopup() {
    isPopupOpen = false;
    dispatch('close');
  }
</script>

<section class="cta-section" transition:fade={{duration: 800}}>
  <div class="cta-content">
    <h2>{ctaText}</h2>
    <p class="subtext">Join a community of forward-thinkers preparing for the future.</p>
    <button class="cta-button" on:click={showPopup}>
      {buttonText}
      <span class="arrow">→</span>
    </button>
    <p class="disclaimer">By enlisting, you agree to receive communications about joining our community and learning how to adapt and survive the singularity with like-minded individuals who are watching developments with curiosity and caution.</p>
  </div>
</section>

<HookEmPopup bind:isOpen={isPopupOpen} on:close={closePopup} />

<style>
  .cta-section {
    text-align: center;
    margin: 3rem 0;
    padding: 2rem;
    background: linear-gradient(135deg, var(--color-bg-accent, #e6f7ff), var(--color-bg-secondary, #f0f5fa));
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .cta-content {
    max-width: 600px;
    margin: 0 auto;
  }

  h2 {
    font-size: 2.25rem;
    line-height: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
    color: var(--color-text-primary, #1a202c);
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  }

  .subtext {
    font-size: 1.125rem;
    color: var(--color-text-secondary, #4a5568);
    margin-bottom: 1.5rem;
  }

  .cta-button {
    background-color: var(--color-primary, #3182ce);
    color: white;
    padding: 0.75rem 2rem;
    border-radius: 2rem;
    font-size: 1.25rem;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .cta-button:hover {
    background-color: var(--color-primary-dark, #2c5282);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .arrow {
    margin-left: 0.5rem;
    transition: transform 0.3s ease;
  }

  .cta-button:hover .arrow {
    transform: translateX(4px);
  }

  .disclaimer {
    font-size: 0.75rem;
    color: var(--color-text-secondary, #4a5568);
    margin-top: 1rem;
    max-width: 80%;
    margin-left: auto;
    margin-right: auto;
  }

  :global(.dark) .cta-section {
    background: linear-gradient(135deg, var(--color-bg-accent-dark, #1a365d), var(--color-bg-secondary-dark, #2d3748));
  }

  :global(.dark) h2 {
    color: var(--color-text-primary-dark, #f7fafc);
  }

  :global(.dark) .subtext {
    color: var(--color-text-secondary-dark, #a0aec0);
  }

  :global(.dark) .disclaimer {
    color: var(--color-text-secondary-dark, #a0aec0);
  }
</style>