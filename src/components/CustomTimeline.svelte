<script>
  import {
    Timeline,
    TimelineItem,
    TimelineSeparator,
    TimelineDot,
    TimelineConnector,
    TimelineContent,
    TimelineOppositeContent
  } from 'svelte-vertical-timeline';

  const options = [
    { title: 'Eat', time: '09:30 am', icon: 'https://img.icons8.com/nolan/64/taco.png', description: 'Enjoy a delicious breakfast taco.' },
    { title: 'Sleep', time: '10:00 am', icon: 'https://img.icons8.com/doodle/48/000000/svetle.png', description: 'Take a refreshing morning nap.' },
    { title: 'Code', time: '11:00 am', icon: 'https://img.icons8.com/nolan/64/code.png', description: 'Start coding and building amazing things.' },
    { title: 'Eat', time: '01:00 pm', icon: 'https://img.icons8.com/nolan/64/birthday-cake.png', description: 'Treat yourself to a tasty lunch.' }
  ];
</script>

<Timeline position="vertical" style="border: solid 1px #dbdbdb; padding: 50px 0; border-radius: 2%;" class="timeline-vertical max-md:timeline-compact">
  {#each options as option}
    <TimelineItem>
      <TimelineOppositeContent slot="opposite-content">
        <p class="text-gray-500 italic">{option.time}</p>
      </TimelineOppositeContent>
      <TimelineSeparator>
        <TimelineDot class="bg-white flex justify-center items-center border-transparent h-12 w-12">
          <img src={option.icon} alt={option.title} class="h-8 w-8" />
        </TimelineDot>
        <TimelineConnector />
      </TimelineSeparator>
      <TimelineContent class="mb-10">
        <h3 class="text-lg font-bold mb-2">{option.title}</h3>
        <div class="collapse">
          <input type="checkbox" />
          <div class="collapse-title text-base font-medium">
            Read more
          </div>
          <div class="collapse-content">
            <p class="text-sm">{option.description}</p>
          </div>
        </div>
      </TimelineContent>
    </TimelineItem>
  {/each}
</Timeline>

<style>
  /* Add any custom styles here */
</style>