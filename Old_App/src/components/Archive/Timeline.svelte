<script>
  import { Timeline } from 'svelte-vertical-timeline';
  import TimelineItem from './TimelineItem.svelte';

  const events = [
    {
      id: 1,
      title: 'Event 1',
      description: 'This is the first event',
      time: '9:00 am',
    },
    {
      id: 2,
      title: 'Event 2',
      description: 'This is the second event',
      time: '10:00 am',
    },
    {
      id: 3,
      title: 'Event 3',
      description: 'This is the third event',
      time: '11:00 am',
    },
    {
      id: 4,
      title: 'Event 4',
      description: 'This is the fourth event',
      time: '12:00 pm',
    },
    {
      id: 5,
      title: 'Event 5',
      description: 'This is the fifth event',
      time: '1:00 pm',
    },
  ];

  let selectedEvent = null;

  function openModal(event) {
    selectedEvent = event;
  }

  function closeModal() {
    selectedEvent = null;
  }
</script>

<div class="timeline-container">
  <Timeline position="right">
    {#each events as event}
      <TimelineItem {event} on:click={() => openModal(event)} {selectedEvent} on:close={closeModal} />
    {/each}
  </Timeline>
</div>

<style>
  .timeline-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 0;
  }

  :global(.timeline-item) {
    margin-bottom: 40px;
  }

  :global(.timeline-item:last-child) {
    margin-bottom: 0;
  }
</style>