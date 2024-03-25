<script>
  import { Timeline } from 'svelte-vertical-timeline';
  import TimelineItem from './TimelineItem.svelte';

  import { events } from '../events.js';
</script>

<div class="timeline-container">
  <Timeline position="right">
    {#each events as event}
      <TimelineItem {event} />
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