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
  <hr class="my-8 border-t border-gray-300 dark:border-gray-700" />
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
  <hr class="my-8 border-t border-gray-300 dark:border-gray-700" />

</div>

<style>
  .timeline-container {
    padding: 2rem; /* Equivalent to p-4 in Tailwind CSS */
  }
  .timeline-header {
    text-align: center;
    font-weight: bold;
    font-size: 1.5rem;
    margin-bottom: .5rem; /* Add some spacing below the header */
  }
</style>
