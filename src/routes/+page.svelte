<script>
	import Spacer from '$lib/components/Spacer.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	import Countdown from '$lib/components/Countdown.svelte';
	import MailchimpSignup from '$lib/components/MailchimpSignup.svelte';

	// Correct the import path for the JSON file
	import timelineItems from '$lib/data/timelineItems.json';
	// Define the target date for the countdown
	const targetDate = new Date("2027-11-20T23:59:59").getTime(); // Example target date
	// export let data;
	function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
    }
  </script>

  <button class="buy-button block" on:click={handleBackBook}>Back the Book on Kickstarter</button>
  <Spacer height="1.25rem"/>

  <!-- Pass the targetDate prop to the Countdown component -->
  <Countdown {targetDate} />



  <Timeline items={timelineItems.timelineItems} />

  <button class="buy-button block w-full" on:click={handleBackBook}>Back the Book on Kickstarter</button>
  <Spacer height="1rem"/>

  <MailchimpSignup />

  <Spacer height="1rem"/>

<style>
	.buy-button {
      font-weight: bold;
	    font-size: 1.5rem;
      background-color: #f8f9fa;
      border: 2px solid #000000;
      border-radius: 4px;
      padding: 1rem 1rem;
      cursor: pointer;
      transition: background-color 0.3s ease;
      text-align: center;
    }

    .buy-button:hover {
      background-color: #e2e6ea;
    }
</style>