<script>
	import Spacer from '$lib/components/Spacer.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	import Countdown from '$lib/components/Countdown.svelte';
	import MailchimpSignup from '$lib/components/MailchimpSignup.svelte';
	import { Accordion, AccordionItem } from 'flowbite-svelte';

	import timelineItems from '$lib/data/timelineItems.json';
	const targetDate = new Date("2027-11-20T23:59:59").getTime();

	function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
    }

  function handleJoinSkool() {
      window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
    }

  function handleGetGuide() {
      window.open('https://tavolazzi.gumroad.com/l/singularitychecklist', '_blank');
    }

  function handleReadSample() {
    window.location.href = 'https://survivingthesingularity.com/sample';  }
</script>

<Spacer height="1.25rem"/>

<Countdown {targetDate} />

<div class="button-container">
  <button class="big-button" on:click={handleGetGuide}>Get the FREE Guide</button>
  <button class="big-button" on:click={handleJoinSkool}>Join the Skool Community</button>
</div>

<div class="sample-button-container">
  <button class="big-button" on:click={handleReadSample}>Read a Sample</button>
</div>

<div class="quote-container">
  <p class="quote">"I am patiently waiting for the Singularity."</p>
  <p class="attribution">- Harper Reed</p>
</div>

<div class="content-container">
  <Accordion class="full-width-accordion">
    <AccordionItem>
      <span slot="header" class="text-lg font-semibold">What is the Singularity?</span>
      <p class="mb-2 text-gray-500 dark:text-gray-400">
        The Singularity is that mind-bending point where AI surpasses human intelligence. Imagine your smartphone suddenly deciding it's smarter than you - and being right. It's when our tech takes the wheel and starts driving us into uncharted territory. Whether that's a utopia or a "rise of the machines" scenario is anyone's guess. Buckle up!
      </p>
    </AccordionItem>
    
    <AccordionItem>
      <span slot="header" class="text-lg font-semibold">When is the Singularity expected to occur?</span>
      <p class="mb-2 text-gray-500 dark:text-gray-400">
        Here's the thing about the Singularity - it's not a single "boom" moment, but more like a rollercoaster that's already left the station and is picking up speed. Check out our timeline below for our best educated guess on when things will really start to feel like they're taking off. But remember, we're already on this ride. Each day, technology gets more sophisticated, cheaper, and easier to access. The pace of change is accelerating, and before you know it, we'll be in a world that makes today look like the Stone Age. So when is the Singularity? In many ways, it's already begun.
      </p>
    </AccordionItem>
    
    <AccordionItem>
      <span slot="header" class="text-lg font-semibold">What are the potential impacts of the Singularity?</span>
      <p class="mb-2 text-gray-500 dark:text-gray-400">
        As our timeline shows, the impacts of the Singularity will be far-reaching and mind-boggling:
        <ul class="list-disc pl-5 mt-2">
          <li>Medicine: We might cure death before we cure the common cold. Immortality, anyone?</li>
          <li>Economy: When AI can do any job, what happens to human work? Universal Basic Income or universal poverty?</li>
          <li>Education: Forget studying - just download knowledge directly to your brain. Hope you like pop-up ads in your dreams.</li>
          <li>Ethics: When machines can think and feel, do they deserve rights? And who gets to decide?</li>
        </ul>
        Each advancement on our timeline isn't just a cool new gadget - it's a step towards a fundamentally different world. The Singularity isn't just a tech revolution - it's a redefinition of what it means to be human.
    </AccordionItem>
    
    <AccordionItem>
      <span slot="header" class="text-lg font-semibold">How can one prepare for the Singularity?</span>
      <p class="mb-2 text-gray-500 dark:text-gray-400">
        Preparing for the Singularity is like trying to pack for a trip where the destination keeps changing. But don't panic - here's your survival kit:
        <ul class="list-disc pl-5 mt-2">
          <li>Stay informed: Keep an eye on our timeline. Today's sci-fi is tomorrow's reality.</li>
          <li>Embrace adaptability: The only constant will be change, so get comfortable with being uncomfortable.</li>
          <li>Develop a growth mindset: Learning won't stop when you leave school. In fact, it'll be more important than ever.</li>
          <li>Engage in the conversation: The future's coming whether we like it or not. Might as well have a say in shaping it.</li>
        </ul>
        Remember, surviving the Singularity isn't just about keeping up with the latest tech - it's about staying human in a world that's evolving faster than we can comprehend. Keep an eye on our timeline, but more importantly, keep an eye on what makes us human.
    </AccordionItem>
  </Accordion>
</div>

<div class="content-container">
  <Timeline items={timelineItems.timelineItems} />
</div>

<Spacer height="2rem"/>

<div class="button-container">
  <button class="big-button" on:click={handleBackBook}>Back the Book on Kickstarter</button>
  <button class="big-button" on:click={handleReadSample}>Read a Sample</button>
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

    .sample-button-container {
      display: flex;
      justify-content: center;
      margin: 1rem 0;
    }

  .sample-button-container .big-button {
    max-width: 50%;
  }

  @media (max-width: 768px) {
    .sample-button-container .big-button {
      max-width: none;
      width: 100%;
    }
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  :global(.full-width-accordion) {
    width: 100%;
  }

  :global(.full-width-accordion > *) {
    width: 100%;
  }

  :global(.full-width-accordion button) {
    width: 100%;
    justify-content: space-between;
    padding: 1rem;
    font-size: 1.125rem;
    font-weight: 600;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
  }

  :global(.full-width-accordion button:hover) {
    background-color: #f3f4f6;
  }
</style>