<script>
  import { onMount } from 'svelte';

  // Props
  export let targetSelector = '.timeline-container'; // Selector for the timeline container
  export let offset = 100; // Offset from the bottom in pixels
  export let showAfterScroll = 300; // Show button after scrolling this many pixels

  let visible = false;
  let timelineElement;

  function scrollToOrigins() {
    if (!timelineElement) return;

    // Get the timeline element's position
    const timelineRect = timelineElement.getBoundingClientRect();
    const targetPosition = window.scrollY + timelineRect.bottom - offset;

    // Scroll to the bottom of the timeline (where the oldest events are now)
    window.scrollTo({
      top: targetPosition,
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
  on:click={scrollToOrigins}
  aria-label="Jump to the beginning of the timeline"
>
  <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="7 13 12 18 17 13"></polyline>
    <polyline points="7 6 12 11 17 6"></polyline>
  </svg>
  <span class="text">Origins</span>
</button>

<style>
  .jump-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    z-index: 50;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s ease, transform 0.3s ease, background-color 0.2s ease;
    padding: 0;
  }

  .jump-button.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .jump-button:hover {
    background-color: #2563eb;
  }

  .jump-button:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
  }

  .icon {
    width: 24px;
    height: 24px;
    margin-bottom: 2px;
  }

  .text {
    font-size: 10px;
    font-weight: 500;
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