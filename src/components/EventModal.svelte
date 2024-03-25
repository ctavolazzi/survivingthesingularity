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
      <p><strong>Year:</strong> {event.time}</p>
      <p><strong>Details:</strong> {event.description}</p>
      <button class="btn btn-primary learn-more-button" on:click={() => searchEvent(event)}>
        Learn More
      </button>
    </div>
  </div>
</div>

<style>
  /* Add your CSS here */
</style>
