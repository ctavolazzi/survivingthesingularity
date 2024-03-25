<script>
<<<<<<< HEAD
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
		{ title: 'Eat', time: '09:30 am' },
		{ title: 'Sleep', time: '10:00 am' },
		{ title: 'Code', time: '11:00 am' },
		{ title: 'Eat', time: '01:00 pm' }
	];

import CustomTimeline from './components/CustomTimeline.svelte';
=======
  import MyTimeline from './components/MyTimeline.svelte';
>>>>>>> origin/main
</script>

<h1>Surviving the Singularity</h1>
<MyTimeline />

<CustomTimeline />

<style>
	  h1 {
	text-align: center;
	margin-top: 2rem;
  }
</style>