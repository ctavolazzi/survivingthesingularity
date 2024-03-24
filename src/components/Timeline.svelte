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

<Timeline>
    <TimelineItem>
      <TimelineOppositeContent>
        <p class="text">2024</p>
      </TimelineOppositeContent>
      <TimelineSeparator>
        <TimelineDot />
        <TimelineConnector />
      </TimelineSeparator>
      <TimelineContent>
        <p>Event One - The beginning of something great.</p>
      </TimelineContent>
    </TimelineItem>
    <TimelineItem>
      <TimelineOppositeContent>
        <p class="text">2025</p>
      </TimelineOppositeContent>
      <TimelineSeparator>
        <TimelineDot />
        <TimelineConnector />
      </TimelineSeparator>
      <TimelineContent>
        <p>Event Two - Progress and development.</p>
      </TimelineContent>
    </TimelineItem>
    <!-- Continue adding TimelineItem blocks for more events -->
  </Timeline>
  
  <style>
    .text {
      /* Add any additional styling here */
    }
  </style>
  