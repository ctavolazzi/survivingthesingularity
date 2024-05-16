<script>
  import { Timeline } from 'svelte-vertical-timeline';
  import TimelineItem from './TimelineItem.svelte';
  import { events } from '../events.js';

  function parseDate(dateStr) {
    const bcMatch = dateStr.match(/-(\d+)-(\d+)-(\d+)/);
    if (bcMatch) {
      return { year: -parseInt(bcMatch[1]), month: parseInt(bcMatch[2]), day: parseInt(bcMatch[3]) };
    }
    const adMatch = dateStr.match(/(\d+)-(\d+)-(\d+)/);
    if (adMatch) {
      return { year: parseInt(adMatch[1]), month: parseInt(adMatch[2]), day: parseInt(adMatch[3]) };
    }
    return { year: 0, month: 0, day: 0 };
  }

  function compareDates(a, b) {
    if (a.year !== b.year) return b.year - a.year;
    if (a.month !== b.month) return b.month - a.month;
    return b.day - a.day;
  }

  events.sort((a, b) => compareDates(parseDate(a.published), parseDate(b.published)));
</script>

<div class="timeline-container">
  <Timeline position="right">
    {#each events as event (event.id)}
      <TimelineItem {event} />
    {/each}
  </Timeline>
</div>

<style>
  .timeline-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 0;
    padding-top: 0px;
  }

  :global(.timeline-item) {
    margin-bottom: 40px;
  }

  :global(.timeline-item:last-child) {
    margin-bottom: 0;
  }

  @media (max-width: 768px) {
    .timeline-container {
      padding: 20px 0;
    }
  }

  @media (max-width: 480px) {
    .timeline-container {
      padding: 10px 0;
    }
  }
</style>
