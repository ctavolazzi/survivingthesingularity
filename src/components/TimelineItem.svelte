<script>
  import { TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent, TimelineOppositeContent } from 'svelte-vertical-timeline';

  export let event;

  import { onMount, onDestroy } from 'svelte';

  let showModal = false;

  function toggleModal() {
    showModal = !showModal;
    if (showModal) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }

  // Optionally, ensure that scrolling is re-enabled if the component is destroyed while the modal is open
  onDestroy(() => {
    document.body.style.overflow = '';
  });

  function searchEvent(event) {
    const searchQuery = encodeURIComponent(event.title);
    const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
    window.open(searchUrl, '_blank');
  }
</script>

<TimelineItem>
  <TimelineOppositeContent slot="opposite-content" class="timeline-time">
    <h3>{event.published}</h3>
    <h4>Published by {event.authors}</h4>
    <p>{new Date(event.published).getHours() < 12 ? 'Morning' : 'Afternoon'}</p>
    <p>{new Date(event.published).getHours() < 12 ? '🌅' : '🌆'}</p>
  </TimelineOppositeContent>
  <TimelineSeparator>
    <TimelineDot />
    <TimelineConnector />
  </TimelineSeparator>
  <TimelineContent>
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">{event.title}</h2>
        <p>{event.abstract}</p>
        <button class="btn btn-primary" on:click={toggleModal}>View Details</button>
      </div>
    </div>
  </TimelineContent>
</TimelineItem>

{#if showModal}
  <div class="modal-overlay" on:click={toggleModal}>
    <div class="modal-content" on:click|stopPropagation>
      <div class="modal-header">
        {#if event.image}
          <img src="{event.image}" alt="{event.title}" class="modal-image">
        {/if}
        <h2>{event.title}</h2>
        <button class="close-button" on:click={toggleModal}>&times;</button>
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
  
{/if}

<style>
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
    background-color: white;
    padding: 20px;
    border-radius: 4px;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
  }

  .close-button {
    cursor: pointer;
    border: none;
    background: none;
    font-size: 1.5rem;
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
