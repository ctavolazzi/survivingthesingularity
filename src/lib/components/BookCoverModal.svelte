<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import coverImage from '$lib/images/Surviving-the-Singularity-Cover.png';

  export let isOpen = false;

  let modalContent;
  let triggerEl;
  let closeBtn;

  function openModal() {
    isOpen = true;
  }

  function closeModal() {
    isOpen = false;
    if (triggerEl) triggerEl.focus();
  }

  function handleTriggerKeydown(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      openModal();
    }
  }

  // Escape-to-close is handled at the window level (below) so the keydown
  // listener doesn't sit on the non-interactive dialog element.
  function handleWindowKeydown(e) {
    if (isOpen && e.key === 'Escape') {
      e.preventDefault();
      closeModal();
    }
  }

  function adjustModalSize() {
    if (modalContent) {
      modalContent.style.height = `${window.innerHeight * 0.9}px`;
      modalContent.style.width = `${window.innerWidth * 0.9}px`;
    }
  }

  onMount(() => {
    if (!browser) return;
    window.addEventListener('resize', adjustModalSize);
    window.addEventListener('keydown', handleWindowKeydown);
  });

  onDestroy(() => {
    if (browser) {
      window.removeEventListener('resize', adjustModalSize);
      window.removeEventListener('keydown', handleWindowKeydown);
    }
  });

  $: if (browser && isOpen) {
    // Move focus into the modal once it's open
    setTimeout(() => closeBtn?.focus(), 50);
    adjustModalSize();
  }
</script>

<button
  class="cover-trigger"
  bind:this={triggerEl}
  on:click={openModal}
  on:keydown={handleTriggerKeydown}
  aria-label="Open larger view of the Surviving the Singularity book cover"
  aria-haspopup="dialog"
>
  <img
    src={coverImage}
    alt="Surviving the Singularity book cover"
    class="book-cover"
    loading="lazy"
  />
</button>

{#if isOpen}
  <button
    type="button"
    class="modal-backdrop"
    on:click={closeModal}
    aria-label="Close book cover view"
  ></button>
  <div
    class="modal-content"
    bind:this={modalContent}
    role="dialog"
    aria-modal="true"
    aria-labelledby="book-cover-title"
    tabindex="-1"
  >
      <div class="modal-inner">
        <div class="modal-image-container">
          <img src={coverImage} alt="" class="modal-image" loading="lazy" />
        </div>
        <div class="modal-text">
          <h2 id="book-cover-title" class="book-title">Surviving the Singularity</h2>
          <div class="book-subtitle">A field manual for staying agentic as AI rewrites the world.</div>
          <div class="book-description">
            <p>
              The Singularity isn't just about fending off Terminator bots or finding food in the era of economic collapse and climate famines. It's about navigating a world where technology changes faster than we can keep up with.
            </p>
            <p>
              This book is a primer on understanding and navigating the <strong>double exponential shift</strong> in the way we get our needs met: from autonomous drone swarms to the possibility of robots doing all labor in the world.
            </p>
            <p>
              Before you resign yourself to your new overlords, pause for a moment, breathe, and know it's already over. Now you just have to learn how to survive the Singularity. <strong>This book will teach you.</strong>
            </p>
          </div>
          <div class="cta-container">
            <a class="cta-substack" href="https://thecoffeejesus.substack.com" target="_blank" rel="noopener noreferrer">
              Subscribe on Substack &rarr;
            </a>
          </div>
        </div>
      </div>
      <button
        class="close-button"
        bind:this={closeBtn}
        on:click={closeModal}
        aria-label="Close book cover dialog"
      >
        Close
      </button>
  </div>
{/if}

<style>
  .cover-trigger {
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    display: block;
    margin: 2rem auto;
  }
  .book-cover {
    max-width: 300px;
    width: 100%;
    height: auto;
    box-shadow: 4px 4px 0 rgba(245, 158, 11, 0.2);
    border-radius: 0;
    transition: box-shadow 0.2s ease;
  }
  .cover-trigger:hover .book-cover,
  .cover-trigger:focus-visible .book-cover {
    box-shadow: 6px 6px 0 rgba(245, 158, 11, 0.3);
  }
  .cover-trigger:hover .book-cover,
  .cover-trigger:focus-visible .book-cover {
    transform: scale(1.04);
  }

  .modal-backdrop {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.82);
    z-index: 1000;
    border: none;
    margin: 0;
    padding: 0;
    cursor: pointer;
  }

  .modal-content {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1001;
    background: #0f172a;
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-left: 3px solid rgba(245, 158, 11, 0.4);
    border-radius: 0;
    color: #e2e8f0;
    overflow: auto;
    max-width: calc(100vw - 2rem);
    max-height: calc(100vh - 2rem);
    padding: 1.5rem;
    box-shadow: 6px 6px 0 rgba(245, 158, 11, 0.1);
  }

  .modal-inner {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr);
    gap: 2rem;
    align-items: start;
  }

  .modal-image-container {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal-image {
    width: 100%;
    max-width: 360px;
    height: auto;
    border-radius: 0;
    box-shadow: 4px 4px 0 rgba(245, 158, 11, 0.2);
  }

  .book-title {
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 800;
    color: #fafafa;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.02em;
  }

  .book-subtitle {
    font-size: 1rem;
    color: #dde4ef;
    margin-bottom: 1.25rem;
  }

  .book-description p {
    color: #e9eef5;
    line-height: 1.7;
    margin: 0 0 0.9rem 0;
    font-size: 0.95rem;
  }
  .book-description strong {
    color: #fafafa;
  }

  .cta-container {
    margin-top: 1.25rem;
  }

  .cta-substack {
    display: inline-block;
    padding: 0.7rem 1.4rem;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 700;
    font-size: 0.92rem;
    border-radius: 0;
    text-decoration: none;
    box-shadow: 3px 3px 0 rgba(120, 53, 15, 0.4);
    transition: box-shadow 0.15s ease;
  }
  .cta-substack:hover {
    box-shadow: 4px 4px 0 rgba(120, 53, 15, 0.5);
  }

  .close-button {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    background: rgba(2, 6, 23, 0.6);
    color: #e2e8f0;
    border: 1px solid rgba(148, 163, 184, 0.2);
    padding: 0.4rem 0.85rem;
    border-radius: 0;
    font-size: 0.85rem;
    cursor: pointer;
  }
  .close-button:hover {
    background: rgba(2, 6, 23, 0.85);
    color: #fafafa;
  }

  @media (max-width: 768px) {
    .modal-inner {
      grid-template-columns: 1fr;
    }
  }
</style>
