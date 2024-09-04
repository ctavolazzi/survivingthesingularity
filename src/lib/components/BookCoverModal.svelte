<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import coverImage from '$lib/images/Surviving-the-Singularity-Cover.png';
  import PreorderButton from './PreorderButton.svelte';
  import CountdownTimer from './CountdownTimer.svelte';

  export let isOpen = false;
  const dispatch = createEventDispatcher();

  let modalContent;
  let imageElement;

  function closeModal() {
    dispatch('close');
  }

  onMount(() => {
    if (imageElement) {
      imageElement.onload = adjustModalSize;
    }
    window.addEventListener('resize', adjustModalSize);
    return () => window.removeEventListener('resize', adjustModalSize);
  });

  function adjustModalSize() {
    if (modalContent) {
      const viewportHeight = window.innerHeight;
      const viewportWidth = window.innerWidth;
      
      let modalHeight = viewportHeight * 0.9; // 90% of viewport height
      let modalWidth = viewportWidth * 0.9; // 90% of viewport width
      
      modalContent.style.height = `${modalHeight}px`;
      modalContent.style.width = `${modalWidth}px`;
    }
  }

  // Set the target date for the offer (adjust as needed)
  const offerEndDate = '2024-11-08T23:59:59';
</script>

<img src={coverImage} alt="Surviving the Singularity Book Cover" class="book-cover" on:click={() => dispatch('open')} />

{#if isOpen}
  <div class="modal-overlay" on:click={closeModal}>
    <div class="modal-content" bind:this={modalContent} on:click|stopPropagation>
      <div class="modal-inner">
        <div class="modal-image-container">
          <img src={coverImage} alt="Surviving the Singularity Book Cover" class="modal-image" />
        </div>
        <div class="modal-text">
          <h2 class="book-title">Surviving the Singularity</h2>
          <div class="book-subtitle">A Guide to Thriving in the AI Revolution</div>
          <div class="book-description">
            <p>
              Surviving the Singularity isn't just about fending off hordes of Terminator bots or finding food in the era of economic collapse and climate famines. It's about <span class="highlight">navigating a world where technology changes faster than we can keep up with</span>.
            </p>
            <p>
              This book is a primer on understanding and navigating the <span class="highlight">double exponential shift</span> in the way we get our needs met. From autonomous drone swarms to the possibility of robots doing <span class="highlight">all labor in the world</span>, we explore the potential realities of our rapidly changing world.
            </p>
            <p>
              Before you resign yourself to your new overlords, pause for a moment, breathe, and know it's already over. Now you just have to learn how to survive the Singularity. <span class="highlight">This book will teach you</span>.
            </p>
          </div>
          <div class="cta-container">
            <PreorderButton buttonText="Pre-order Now" />
          </div>
          <div class="lto-container">
            <CountdownTimer targetDate={offerEndDate} />
          </div>
        </div>
      </div>
      <button class="close-button" on:click={closeModal}>Close</button>
    </div>
  </div>
{/if}

<style>
  .book-cover {
    max-width: 300px;
    width: 100%;
    height: auto;
    margin: 2rem auto;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
  }

  .book-cover:hover {
    transform: scale(1.05);
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    background-color: white;
    border-radius: 8px;
    overflow-y: auto;
    max-width: 90vw;
    max-height: 90vh;
    position: relative;
  }

  .modal-inner {
    display: flex;
    flex-direction: column;
  }

  .modal-image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: white;
    padding: 1rem;
  }

  .modal-image {
    max-width: 100%;
    max-height: 50vh;
    object-fit: contain;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .modal-text {
    padding: 2rem;
    text-align: left;
    background: linear-gradient(135deg, #1a202c, #2d3748);
    color: #e2e8f0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .close-button {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: var(--text-accent);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    z-index: 10;
  }

  .close-button:hover {
    background-color: #4a5568;
  }

  .book-title {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: #fbd38d;
  }

  .book-subtitle {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #63b3ed;
  }

  .book-description {
    margin-bottom: 1rem;
  }

  .cta-container {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
  }

  .lto-container {
    margin-top: 1rem;
  }

  /* Scrollbar styling */
  .modal-text::-webkit-scrollbar {
    width: 8px;
  }

  .modal-text::-webkit-scrollbar-track {
    background: #2d3748;
  }

  .modal-text::-webkit-scrollbar-thumb {
    background-color: #63b3ed;
    border-radius: 4px;
  }

  :global(.dark) .modal-content {
    background-color: #2d3748;
    color: var(--text-primary);
  }

  @media (max-width: 768px) {
    .book-title {
      font-size: 1.8rem;
    }

    .book-subtitle {
      font-size: 1rem;
    }
  }

  @media (min-width: 768px) {
    .modal-inner {
      flex-direction: row;
    }

    .modal-image-container,
    .modal-text {
      width: 50%;
    }

    .modal-image {
      max-height: 80vh;
    }
  }
</style>