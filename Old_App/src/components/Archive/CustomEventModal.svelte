<script>
  export let event;
  export let onClose;

  function searchEvent(event) {
    const searchQuery = encodeURIComponent(event.title);
    const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
    window.open(searchUrl, '_blank');
  }
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
      <p><strong>Authors:</strong> {event.authors.join(', ')}</p>
      <p><strong>Abstract:</strong> {event.abstract}</p>
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

  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 4px;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    margin: 2%;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .modal-body {
    margin-top: 20px;
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

  .btn {
    background-color: #000;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-align: center;
  }

  .btn:hover {
    background-color: #333;
  }
</style>
