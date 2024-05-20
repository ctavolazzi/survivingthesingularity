<script>
  import { Timeline, TimelineItem, Button } from 'flowbite-svelte';
  import { ArrowRightOutline } from 'flowbite-svelte-icons';
  import timelineItems from '../data/timelineItems.json'; // Adjust the path as necessary

  function searchGoogle(title) {
    const query = encodeURIComponent(title);
    window.open(`https://www.google.com/search?q=${query}`, '_blank');
  }
</script>

<div class="timeline-container">
  <div class="timeline-header">Timeline of Events</div>
  <Timeline>
    {#each timelineItems.timelineItems as item (item.id)}
      <TimelineItem title={item.title} date={item.date}>
        <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">{item.abstract}</p>
        <Button on:click={() => searchGoogle(item.title)} color="black" size="small">
          Learn More <ArrowRightOutline />
        </Button>
      </TimelineItem>
    {/each}
  </Timeline>
</div>

<style>
  .timeline-container {
    padding: 2rem; /* Equivalent to p-4 in Tailwind CSS */
  }
  .timeline-header {
    text-align: center;
    font-weight: bold;
    text-decoration: underline;
    margin-bottom: 1rem; /* Add some spacing below the header */
  }
</style>
