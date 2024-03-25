<script>
  export let event;
  export let onClose;
  console.log("EventModal initialized");
  function searchEvent(event) {
    const searchQuery = encodeURIComponent(event.title);
    const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
    window.open(searchUrl, '_blank');
  }
  console.log("EventModal event: ", event);
</script>

<div class="modal-overlay" on:click={onClose}>
  <div class="modal-content" on:click|stopPropagation>
    <div class="modal-header">
      {#if event.image}
        <img src={event.image} alt={event.title} class="modal-image">
      {/if}
      <h2>{event.title}</h2>
      <button class="close-button" on:click={onClose}>&times;</button>
    </div>
    <div class="modal-body">
      <p><strong>Date Published:</strong> {event.published}</p>
      <p><strong>Authors:</strong> {event.authors}</p>
      <p><strong>Abstract:</strong> {event.abstract}</p>
      <!-- Additional event details can be included here -->
      <button class="btn btn-primary learn-more-button" on:click={() => searchEvent(event)}>
        Learn More
      </button>
    </div>
  </div>
</div>

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

  .close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
    border: none;
    background: none;
    font-size: 1.5rem;
  }

  .modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 4px;
  max-width: 500px; /* Adjusts based on screen size */
  max-height: 90vh;
  overflow-y: auto;
  margin: 2%; /* Provides a slight offset from screen edges */
}

@media (max-width: 768px) {
  .modal-content {
    max-width: 90%; /* Allows more space around the modal on smaller screens */
    margin: 5%; /* Increased margin for smaller devices */
  }
}
</style>
