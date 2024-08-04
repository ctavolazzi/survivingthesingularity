<script>
	import Spacer from '$lib/components/Spacer.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	import Countdown from '$lib/components/Countdown.svelte';
	import MailchimpSignup from '$lib/components/MailchimpSignup.svelte';

	import timelineItems from '$lib/data/timelineItems.json';
	const targetDate = new Date("2027-11-20T23:59:59").getTime();

	function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
    }

  function handleJoinSkool() {
      // window.open('https://www.skool.com/surviving-the-singularity', '_blank');
      alert("The Skool Community is coming soon! We'll notify you when it's ready.");
    }

  function handleGetGuide() {
      window.open('https://tavolazzi.gumroad.com/l/singularitychecklist', '_blank');
    }
</script>

<Spacer height="1.25rem"/>

<Countdown {targetDate} />

<div class="button-container">
  <button class="big-button" on:click={handleGetGuide}>Get the FREE Guide</button>
  <button class="big-button" on:click={handleJoinSkool}>Join the Skool Community</button>
</div>

<div class="quote-container">
  <p class="quote">"I am patiently waiting for the Singularity."</p>
  <p class="attribution">- Harper Reed</p>
</div>

<Timeline items={timelineItems.timelineItems} />

<Spacer height="2rem"/>

<div class="button-container">
  <button class="big-button" on:click={handleBackBook}>Back the Book on Kickstarter</button>
  <button class="big-button" on:click={handleGetGuide}>Get the FREE Guide</button>
</div>

<Spacer height="1rem"/>

<MailchimpSignup />

<Spacer height="1rem"/>

<style>
    .button-container {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin: 1rem 0;
    }

    .action-button {
      font-weight: bold;
      background-color: #f8f9fa;
      border: 1px solid #000000;
      border-radius: 4px;
      color: #000000;
      padding: 1rem 5rem;
      cursor: pointer;
      transition: background-color 0.3s ease, color 0.3s ease;
    }

    .action-button:hover {
      background-color: #000000;
      color: #ffffff;
    }

    .big-button {
      flex: 1;
      font-weight: bold;
      font-size: 1.25rem;
      background-color: #f8f9fa;
      border: 2px solid #000000;
      border-radius: 4px;
      padding: 1rem 0.5rem;
      cursor: pointer;
      transition: background-color 0.3s ease, color 0.3s ease;
      text-align: center;
    }

    .big-button:hover {
      background-color: #000000;
      color: #ffffff;
    }

    .quote-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 4rem 0;
      padding: 1rem;
      position: relative;
    }

    .quote {
      font-style: italic;
      font-size: 2rem;
      text-align: center;
      margin: 0;
      color: #000;
      line-height: 1.4;
      font-weight: 500;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .attribution {
      font-weight: bold;
      margin-top: 1rem;
      font-size: 1.2rem;
      color: #555;
    }
</style>