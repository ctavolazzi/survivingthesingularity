<!-- <script>
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
</style> -->

<script>
  import { Button } from 'flowbite-svelte';
  import { ArrowRightOutline } from 'flowbite-svelte-icons';
  import timelineItems from '../data/timelineItems.json'; // Adjust the path as necessary

  function searchGoogle(title) {
    const query = encodeURIComponent(title);
    window.open(`https://www.google.com/search?q=${query}`, '_blank');
  }
</script>

<div class="timeline-container p-4 md:p-8 bg-white shadow-lg rounded-lg">
  <h1 class="text-3xl font-bold text-center text-gray-900 mb-6">Timeline of Events</h1>
  <hr class="mb-8 border-gray-300" />

  <ol class="relative border-l border-gray-200 dark:border-gray-700">
    {#each timelineItems.timelineItems as item (item.id)}
      <li class="mb-10 ml-4 pl-4">
        <div class="absolute w-3 h-3 bg-black rounded-full mt-1.5 -left-1.5 border border-white dark:border-gray-900"></div>
        <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{item.date}</time>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-black">{item.title}</h3>
        <p class="text-base font-normal text-gray-500 dark:text-gray-600 mb-4">{item.abstract}</p>
        <Button on:click={() => searchGoogle(item.title)} color="blue" size="sm">
          Learn More <ArrowRightOutline class="ml-2 h-5 w-4" />
        </Button>
      </li>
    {/each}
  </ol>

  <hr class="mt-8 mb-4 border-gray-300" />

</div>

<style>
  .timeline-container {
    max-width: 800px;
    margin: auto;
  }
</style>
