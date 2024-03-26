<script>
  import { TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent, TimelineOppositeContent } from 'svelte-vertical-timeline';
  import ItemModal from './ItemModal.svelte';

  export let event;

  let showModal = false;

  function openModal() {
    showModal = true;
  }

  function closeModal() {
    showModal = false;
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
        <button class="btn btn-primary" on:click={openModal}>View Details</button>
      </div>
    </div>
  </TimelineContent>
</TimelineItem>

{#if showModal}
  <ItemModal {event} on:close={closeModal} />
{/if}