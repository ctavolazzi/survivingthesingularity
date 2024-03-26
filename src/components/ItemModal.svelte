<script>
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  export let event;
  export let buttonPosition = { x: 0, y: 0 };

  const dispatch = createEventDispatcher();

  let scrollY = 0;

  function openModal() {
    scrollY = window.scrollY;
    document.body.classList.add('modal-open');
    document.body.style.top = `-${scrollY}px`;
  }

  function closeModal() {
    document.body.classList.remove('modal-open');
    document.body.style.top = '';
    window.scrollTo(0, scrollY);
    dispatch('close');
  }

  onMount(() => {
    openModal();
  });

  onDestroy(() => {
    closeModal();
  });

  function searchEvent(event) {
    const searchQuery = encodeURIComponent(event.title);
    const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
    window.open(searchUrl, '_blank');
  }

  function swingUp(node, { duration, easing }) {
    return {
        duration,
        easing,
        css: (t, u) => {
            const eased = easing(t);
            // Adjust translateYStart if you need the modal to start from further below
            const translateYStart = 100; // Starting from below the view
            const translateYEnd = 0; // Ending at its natural position

            return `
                transform: translateY(${(1 - eased) * translateYStart + translateYEnd}vh) scale(${eased});
                opacity: ${t};
            `;
        }
    };
}


</script>

<div class="modal-overlay" on:click={closeModal} transition:fade={{ duration: 300 }}>
  <div class="modal-content" on:click|stopPropagation
    in:swingUp={{ duration: 500, easing: cubicOut }}
    out:fade={{ duration: 300 }}
  >
    <div class="modal-header">
      {#if event.image}
        <img src="{event.image}" alt="{event.title}" class="modal-image">
      {/if}
      <h2>{event.title}</h2>
      <button class="close-button" on:click={closeModal}>&times;</button>
    </div>
    <div class="modal-body">
      <h4>Authors</h4>
      <p>{event.authors}</p>
      <h4><strong>Details:</strong></h4>
      <p>{event.details}</p>
      <button class="btn btn-primary learn-more-button" on:click={() => searchEvent(event)}>
        Learn More
      </button>
      <button class="btn btn-primary learn-more-button" on:click={() => searchEvent(event)}>
        arXiv Link
      </button>
      <button class="btn btn-primary learn-more-button" on:click={() => searchEvent(event)}>
        PDF Link
      </button>
    </div>
  </div>
</div>

<style>
  :global(body.modal-open) {
    overflow: hidden;
    position: fixed;
    width: 100%;
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    position: relative;
    background-color: white;
    padding: 20px;
    border-radius: 4px;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    margin: 2% auto;
  }

  @media (max-width: 768px) {
    .modal-content {
      margin: 10% auto;
      max-width: 90%;
    }
  }

  .close-button {
    cursor: pointer;
    border: none;
    background: none;
    font-size: 1.5rem;
    position: absolute;
    top: 10px;
    right: 10px;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .modal-image {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
    margin-right: 20px;
  }

  .modal-body {
    margin-top: 20px;
  }

  .learn-more-button {
    display: block;
    margin-top: 20px;
  }
</style>