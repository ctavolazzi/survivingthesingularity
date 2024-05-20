<script>
  import Navbar from '../components/Navbar.svelte';
  import BottomNav from '../components/BottomNav.svelte';
  import Spacer from '../components/Spacer.svelte';
  import Timeline from '../components/Timeline.svelte';
  import Countdown from '../components/Countdown.svelte';
  import MailchimpSignup from '../components/MailchimpSignup.svelte';

  // Correct the import path for the JSON file
  import timelineItems from '../data/timelineItems.json';

  // Define the target date for the countdown
  const targetDate = new Date("2027-11-20T23:59:59").getTime(); // Example target date
</script>

<Navbar />

<!-- Pass the targetDate prop to the Countdown component -->
<Countdown {targetDate} />

<Timeline items={timelineItems.timelineItems} />

<MailchimpSignup />

<Spacer height="6rem"/>

<BottomNav />
