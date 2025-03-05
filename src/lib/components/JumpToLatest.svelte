<script>
  import { onMount } from 'svelte';

  // Props
  export let targetSelector = '.timeline-container'; // Selector for the timeline container
  export let offset = 100; // Offset from the top in pixels
  export let showAfterScroll = 300; // Show button after scrolling this many pixels

  let visible = false;
  let timelineElement;

  function scrollToLatest() {
    if (!timelineElement) return;

    // Get the timeline element's position
    const timelineRect = timelineElement.getBoundingClientRect();

    // Scroll to the top of the timeline (where the latest events are now)
    window.scrollTo({
      top: window.scrollY + timelineRect.top - offset,
      behavior: 'smooth'
    });
  }

  function handleScroll() {
    // Show button after scrolling down a bit
    visible = window.scrollY > showAfterScroll;
  }

  onMount(() => {
    // Find the timeline element
    timelineElement = document.querySelector(targetSelector);

    // Set up scroll listener
    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  });
</script>

<button
  class="jump-button {visible ? 'visible' : ''}"
  on:click={scrollToLatest}
  aria-label="Jump to the latest events in the timeline"
>
  <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="17 11 12 6 7 11"></polyline>
    <polyline points="17 18 12 13 7 18"></polyline>
  </svg>
  <span class="text">Latest</span>
</button>

<style>
  .jump-button {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background-color: var(--color-primary, #ff7708);
    color: white;
    border: none;
    border-radius: 50%;
    width: 3.5rem;
    height: 3.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s, transform 0.3s;
    z-index: 100;
  }

  .jump-button.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .jump-button:hover {
    background-color: var(--color-primary-dark, #e66700);
  }

  .icon {
    width: 1.5rem;
    height: 1.5rem;
  }

  .text {
    font-size: 0.7rem;
    margin-top: 0.2rem;
  }

  /* Dark mode support */
  :global(.dark) .jump-button {
    background-color: #4b5563;
  }

  :global(.dark) .jump-button:hover {
    background-color: #374151;
  }

  /* Mobile optimization */
  @media (max-width: 640px) {
    .jump-button {
      width: 50px;
      height: 50px;
      bottom: 15px;
      right: 15px;
    }

    .icon {
      width: 20px;
      height: 20px;
    }

    .text {
      font-size: 9px;
    }
  }
</style>