<script>
  import { TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent, TimelineOppositeContent } from 'svelte-vertical-timeline';
  
  export let event;
  export let selectedEvent;

  function handleClick() {
    selectedEvent = event;
  }

  function closeModal() {
    selectedEvent = null;
  }

  function searchEvent(event) {
    const searchQuery = encodeURIComponent(event.title);
    const searchUrl = `https://www.google.com/search?q=${searchQuery}`;
    window.open(searchUrl, '_blank');
  }
</script>

<TimelineItem>
  <TimelineOppositeContent slot="opposite-content" class="timeline-time">
    <h3>{event.published}</h3> <!-- Adjusted to show the published date -->
    <p>{new Date(event.published).getHours() < 12 ? 'Morning' : 'Afternoon'}</p> <!-- Adjusted to calculate time of day -->
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
        <p>{event.abstract}</p> <!-- Using 'abstract' instead of 'description' -->
        <button class="btn btn-primary" on:click={handleClick}>View Details</button>
      </div>
    </div>
  </TimelineContent>
</TimelineItem>

{#if selectedEvent === event}
  <div class="modal-overlay" on:click={closeModal}>
    <div class="modal-content" on:click|stopPropagation>
      <div class="modal-header">
        {#if event.image}
          <img src="{event.image}" alt="{event.title}" class="modal-image">
        {/if}
        <h2>{event.title}</h2>
        <button class="close-button" on:click={closeModal}>&times;</button>
      </div>
      <div class="modal-body">
        <p><strong>Abstract:</strong> {event.abstract}</p>
        <p><strong>Authors:</strong> {event.authors.join(', ')}</p> <!-- Displaying authors -->
        <p><strong>Published:</strong> {event.published}</p>
        <p><strong>Updated:</strong> {event.updated}</p>
        <p><strong>Category:</strong> {event.category}</p>src/components/TimelineItem.svelte
        <a href={event.arxiv_url} target="_blank" class="btn btn-secondary">View arXiv Entry</a> <!-- Link to arXiv URL -->
        <a href={event.pdf_url} target="_blank" class="btn btn-secondary">Download PDF</a> <!-- Link to PDF URL -->
        <button class="btn btn-primary learn-more-button" on:click={() => searchEvent(event)}>
          Learn More
        </button>
      </div>
    </div>
  </div>
{/if}
