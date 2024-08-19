<!-- src/routes/about/index.svelte -->
<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import MailchimpSignup from '$lib/components/MailchimpSignup.svelte';
  import { onMount } from 'svelte';

  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    alert("The Skool Community is launching next Friday 8/9 - please stay tuned.");
  }

  function handleReadSample() {
    window.open('https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit?usp=sharing', '_blank');
  }
</script>

<Spacer height=".1rem"/>

<div class="main-content" style="padding-top: {navbarHeight}px">
  <div class="content-container">
    <h1 class="title">What is this all about?</h1>
    <p class="description">
      Are you ready for a future where AI outpaces human intelligence, where your kids' tech-savvy isn't just about mastering the latest app, but surviving in a world that looks more like The Matrix and Blade Runner had a mutant baby with the Terminator?
    </p>
    <p class="description">
      This book isn't just about understanding technology; it's about preparing you and your family for the rapid changes ahead.
    </p>
    <p class="description">
      What will you do when machines can think, feel, and even outsmart us? How will you protect your family in a world where the lines between human and machine are increasingly blurred? "Surviving the Singularity" provides the insights and strategies to help you navigate the cognitive dissonance ahead as you learn to survive AND thrive in this new era.
    </p>

    <div class="button-container">
      <button class="big-button" on:click={handleReadSample}>Read a Sample</button>
      <button class="big-button" on:click={handleBackBook}>Back the Book</button>
      <button class="big-button" on:click={handleJoinSkool}>Join the Skool Community</button>
    </div>

    <div class="quote-container">
      <p class="quote dark:text-gray-200">"The future is already here — it's just not very evenly distributed."</p>
      <p class="attribution dark:text-gray-400">- William Gibson</p>
    </div>

    <div class="section">
      <h2 class="section-title">Our Mission</h2>
      <p class="description">
        Our mission is to help you understand the Singularity and its impact on our lives. Join our community of forward-thinkers, researchers, and innovators to navigate the challenges and opportunities of this rapidly changing world.
      </p>
    </div>

    <div class="section">
      <h2 class="section-title">Stay Updated</h2>
      <p class="description">
        Subscribe to our newsletter for regular updates, insights, and exclusive content about the technological Singularity.
      </p>
      <MailchimpSignup />
    </div>

    <p class="description">
      "Surviving the Singularity" is sponsored by AIECO, a humanity-focused organization.
    </p>

    <div class="button-container">
      <button class="big-button" on:click={handleBackBook}>Back the Book on Kickstarter</button>
    </div>
  </div>
</div>

<style>
  .main-content {
    transition: padding-top 0.3s ease-in-out;
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  .title {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    color: var(--color-text-primary);
    text-align: center;
  }

  .section-title {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  .description {
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .button-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
    flex-wrap: wrap;
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
    min-width: 200px;
  }

  .big-button:hover {
    background-color: #f8f9fa;
    border-color: #34495e;
    color: #34495e;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transform: translateY(-2px);
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

  .section {
    margin-top: 3rem;
  }

  @media (max-width: 768px) {
    .title {
      font-size: 2rem;
    }

    .section-title {
      font-size: 1.5rem;
    }

    .description {
      font-size: 1rem;
    }

    .quote {
      font-size: 1.5rem;
    }

    .attribution {
      font-size: 1rem;
    }

    .big-button {
      width: 100%;
    }
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

  :global(.dark) .quote {
    color: #e5e7eb;
  }

  :global(.dark) .attribution {
    color: #9ca3af;
  }
</style>