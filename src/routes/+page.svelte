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
</script>

<!-- Icons from: https://icons8.com/pricing -->
<Timeline position="alternate">
	<TimelineItem>
		<TimelineOppositeContent slot="opposite-content">
			<p>09:30 am</p>
		</TimelineOppositeContent>
		<TimelineSeparator>
			<TimelineDot
				style={'width: 45px; height: 45px; background-color: #fff; display: flex; justify-content: center; border-color: transparent; '}
			>
				<img src="https://img.icons8.com/nolan/64/taco.png" />
			</TimelineDot>
			<TimelineConnector />
		</TimelineSeparator>
		<TimelineContent style={'height: 150px;'}>
			<h3>Eat</h3>
			<p>You need to eat.</p>
		</TimelineContent>
	</TimelineItem>

	<TimelineItem>
		<TimelineOppositeContent slot="opposite-content">
			<p style={'margin-top: -1px;'}>10:30 am</p>
		</TimelineOppositeContent>
		<TimelineSeparator>
			<TimelineDot style={'background-color: #FEC048;'} />
			<TimelineConnector />
		</TimelineSeparator>
		<TimelineContent>
			<h3 style={'margin-top: -2px;'}>Sleep</h3>
			<p style={'margin-top: -2px;'}>You need to take a nap.</p>
		</TimelineContent>
	</TimelineItem>

	<TimelineItem>
		<TimelineOppositeContent slot="opposite-content">
			<p>11:00 am</p>
		</TimelineOppositeContent>
		<TimelineSeparator>
			<TimelineDot
				style={'width: 45px; height: 45px; background-color: #fff; display: flex; justify-content: center; border-color: transparent; '}
			>
				<img src="https://img.icons8.com/doodle/48/000000/svetle.png" />
			</TimelineDot>
			<TimelineConnector />
		</TimelineSeparator>
		<TimelineContent style={'height: 200px;'}>
			<h3>Code</h3>
			<p>Svelte is Awesome.</p>
		</TimelineContent>
	</TimelineItem>

	<TimelineItem>
		<TimelineOppositeContent slot="opposite-content">
			<p>01:00 am</p>
		</TimelineOppositeContent>
		<TimelineSeparator>
			<TimelineDot
				style={'width: 45px; height: 65px; background-color: #fff; display: flex; justify-content: center; border-color: transparent; '}
			>
				<img src="https://img.icons8.com/nolan/64/birthday-cake.png" />
			</TimelineDot>
		</TimelineSeparator>
		<TimelineContent style={'height: 200px;'}>
			<h3>Snack</h3>
			<p>You need to treat yourself.</p>
		</TimelineContent>
	</TimelineItem>
</Timeline>

<style>
	p {
		margin: px 0;
		color: grey;
	}
</style>