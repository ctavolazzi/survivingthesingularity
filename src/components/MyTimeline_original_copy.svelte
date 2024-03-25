<script>
  import { Timeline, TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent, TimelineOppositeContent } from 'svelte-vertical-timeline';

  const events = [
    {
      title: 'Event 1',
      date: 'June 1, 2023',
      time: '09:30 am',
      icon: 'https://img.icons8.com/nolan/64/taco.png',
      description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
      details: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    },
    {
      title: 'Event 2',
      date: 'June 5, 2023',
      time: '02:00 pm',
      icon: 'https://img.icons8.com/doodle/48/000000/svetle.png',
      description: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
      details: 'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    },
    // Add more events...
  ];
</script>

<Timeline position="vertical" style="border: solid 1px #dbdbdb; padding: 50px 0; border-radius: 2%;" class="timeline-vertical max-md:timeline-compact">
  {#each events as event}
    <TimelineItem>
      <TimelineOppositeContent slot="opposite-content">
        <div class="text-right">
          <h3 class="text-lg font-bold mb-2">{event.title}</h3>
          <p class="text-gray-500 italic mb-1">{event.date}</p>
          <p class="text-gray-500 italic">{event.time}</p>
        </div>
      </TimelineOppositeContent>
      <TimelineSeparator>
        <TimelineDot class="bg-white flex justify-center items-center border-transparent h-12 w-12">
          <img src={event.icon} alt={event.title} class="h-8 w-8" />
        </TimelineDot>
        <TimelineConnector />
      </TimelineSeparator>
      <TimelineContent class="mb-10">
        <p class="text-sm mb-4">{event.description}</p>
        <div class="collapse border border-base-300 bg-base-100 rounded-box">
          <input type="checkbox" class="peer" />
          <div class="collapse-title text-base font-medium">
            Read more
          </div>
          <div class="collapse-content">
            <p class="text-sm">{event.details}</p>
            <!-- Add more DaisyUI components for interaction and exploration -->
            <div class="rating mt-4">
              <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
              <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" checked />
              <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
              <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
              <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
            </div>
            <button class="btn btn-primary mt-4">Learn More</button>
          </div>
        </div>
      </TimelineContent>
    </TimelineItem>
  {/each}
</Timeline>