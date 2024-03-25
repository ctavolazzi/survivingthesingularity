<script>
  import { Timeline } from 'svelte-vertical-timeline';
  import TimelineItem from './TimelineItem.svelte';

  const events = [
    {
      id: 1,
      title: 'Eat',
      time: '09:30 am',
      description: 'Enjoy a delicious breakfast.',
      details: 'Start your day with a nutritious meal consisting of fresh fruits, whole grain toast, and a protein source like eggs or yogurt.'
    },
    {
      id: 2,
      title: 'Sleep',
      time: '10:00 am',
      description: 'Take a refreshing morning nap.',
      details: 'Give your body and mind a chance to recharge with a short power nap. Find a quiet and comfortable spot, set an alarm, and relax.'
    },
    {
      id: 3,
      title: 'Code',
      time: '11:00 am',
      description: 'Start coding and building amazing things.',
      details: 'Open up your favorite code editor and dive into your projects. Break down tasks, write clean and efficient code, and don\'t forget to take breaks when needed.'
    },
    {
      id: 4,
      title: 'Eat',
      time: '01:00 pm',
      description: 'Enjoy a tasty lunch.',
      details: 'Refuel your body with a balanced meal. Consider options like a colorful salad, a hearty sandwich, or a light stir-fry. Stay hydrated and enjoy your food.'
    }
  ];
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