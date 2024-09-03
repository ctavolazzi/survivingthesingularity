<script>
	import Spacer from '$lib/components/Spacer.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	import Countdown from '$lib/components/Countdown.svelte';
	import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
	import NewsletterPopup from '$lib/components/NewsletterPopup.svelte';
	import { post } from '$lib/data/blog-posts/singularity-express/index.js';
  import FAQ from '$lib/components/FAQ.svelte';
  import LatestNews from '$lib/components/LatestNews.svelte';
  import { onMount } from 'svelte';
  import MainPageBlurb from '$lib/components/MainPageBlurb.svelte';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';
  import BookSample from '$lib/components/BookSample.svelte';
  import CommunityIntakePopupForm from '$lib/components/CommunityIntakePopupForm.svelte';
  import welcomeImage from '$lib/images/sts-welcome.png';
  import { newsletterSubmitted } from '$lib/stores/newsletterSubmitted';

	export let data;

	import timelineItems from '$lib/data/timelineItems.json';
	const targetDate = new Date("2027-11-20T23:59:59").getTime();

	let navbarHeight = 0;
  const newsletterPopupDelay = 10000; // 10 seconds delay

	onMount(() => {
		navbarHeight = document.querySelector('nav').offsetHeight;
    console.log("Testing Supabase Connection");
    console.log(data);

    // Handle newsletter popup
    setTimeout(() => {
      newsletterSubmitted.reset();
    }, newsletterPopupDelay);
	});

	function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
    }

  function handleJoinSkool() {
      window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
    }

  function handleGetGuide() {
    window.location.href = '/download';
  }

  function handleReadSample() {
    window.location.href = 'https://survivingthesingularity.com/sample';  }
</script>

<div class="main-content" style="padding-top: {navbarHeight}px">
  <Countdown {targetDate} />

  <div class="quote-container">
    <p class="quote dark:text-gray-200">"I am patiently waiting for the Singularity."</p>
    <p class="attribution dark:text-gray-400">- Harper Reed</p>
  </div>
  
  
  <div class="book-container">
    <img src={welcomeImage} alt="Surviving the Singularity Book" />
  </div>  
  
  <MainPageBlurb />

  <div class="stylish-divider"></div>

  <div class="button-container">
    <button class="big-button" on:click={handleGetGuide}>Get the FREE Guide</button>
    <button class="big-button" on:click={handleJoinSkool}>Join the Skool Community</button>
    <button class="big-button" on:click={handleReadSample}>Read a Sample of the Book</button>
  </div>
  
  <div class="visual-content">
    <div class="book-sample-container">
      <BookSample />
    </div>
  </div>

  <div class="stylish-divider"></div>
  <FAQ />
  <div class="stylish-divider"></div>

  
  <div class="skool-group-container">
    <SkoolGroup />
  </div>
  
  <div class="stylish-divider"></div>
  <LatestNews {post} />

  <div class="quote-container">
    <p class="quote">The past is over, the present is fleeting - we live in the future.</p>
    <p class="attribution">- Ray Kurzweil</p>
  </div>

  <div class="community-intake-container">
    <div class="stylish-divider"></div>
    <CommunityIntakePopupForm 
      ctaText="Ready to join the rebellion against the singularity?"
      buttonText="Enlist Now"
    />
    <div class="stylish-divider"></div>
  </div>

  <div class="button-container orange-border">
    <button class="big-button" on:click={handleBackBook}>Back the Book on Kickstarter</button>
    <button class="big-button" on:click={handleReadSample}>Read a Sample of the Book</button>
    <button class="big-button" on:click={handleGetGuide}>Get the FREE Guide</button>
  </div>

  <div class="stylish-divider"></div>
  <NewsletterSignup />

  <div class="stylish-divider"></div>

  <Countdown {targetDate} />

  <div class="content-container">
    <Timeline items={timelineItems.timelineItems} />
  </div>

  <div class="stylish-divider"></div>
  <NewsletterSignup />

  <Spacer height="1rem"/>

</div>

{#if $newsletterSubmitted === false}
  <NewsletterPopup />
{/if}

<style>
  /* Layout */
  .main-content {
    transition: padding-top 0.3s ease-in-out;
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  /* Quote */
  .quote-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1rem 0;
    padding: 1rem;
    position: relative;
  }

  .quote {
    font-style: italic;
    font-size: 2rem;
    text-align: center;
    margin: 0;
    color: var(--color-text-primary);
    line-height: 1.4;
    font-weight: 500;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  }

  .attribution {
    font-weight: bold;
    margin-top: 1rem;
    font-size: 1.2rem;
    color: var(--color-text-secondary);
  }

  /* Buttons */
  .button-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 1rem 0;
  }

  .big-button {
    flex: 1;
    font-weight: 600;
    font-size: 1.1rem;
    background-color: #ffffff;
    border: 1px solid #2c3e50;
    border-radius: 6px;
    color: #2c3e50;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .big-button:hover {
    background-color: #f8f9fa;
    border-color: #34495e;
    color: #34495e;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }

  /* Dark mode styles */
  :global(.dark) .quote {
    color: #e5e7eb;
  }

  :global(.dark) .attribution {
    color: #9ca3af;
  }

  :global(.dark) .big-button {
    background-color: #2c3e50;
    color: #ffffff;
    border-color: #34495e;
  }

  :global(.dark) .big-button:hover {
    background-color: #34495e;
    border-color: #4a6785;
    color: #ffffff;
  }

  /* Responsive styles */
  @media (max-width: 768px) {
    .button-container {
      flex-direction: column;
    }

    .big-button {
      width: 100%;
    }
  }

  /* Global styles */
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

  :global(.dark-text) {
    color: #000000;
  }

  :global(.dark) :global(.dark-text) {
    color: #f3f4f6;
  }

  .stylish-divider {
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
    margin: 2rem auto;
    max-width: 80%;
  }

  :global(.dark) .stylish-divider {
    background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
  }

  .orange-border {
    border: 2px solid orange;
    border-radius: 8px;
    padding: 1rem;
  }

  @media (max-width: 768px) {
    .orange-border {
      padding: 0.5rem;
    }
  }

  .book-container {
    display: flex;
    justify-content: center;
    margin: 2rem auto;
    max-width: 80%;
  }

  .book-container img {
    width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
  }

  .skool-group-container {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 2rem 0;
  }

  .visual-content {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }

  /* New styles for the BookSample component */
  :global(.book-sample-container) {
    width: 90%;
    max-width: 600px;
    margin: 0 auto;
  }

  @media (min-width: 768px) {
    :global(.book-sample-container) {
      width: 80%;
    }
  }
</style>