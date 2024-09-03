<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import TableOfContents from '$lib/components/TableOfContents.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import HookEmPopup from '$lib/components/HookEmPopup.svelte';
  import CtaSection from '$lib/components/CtaSection.svelte';
  import coverImage from '$lib/images/Surviving-the-Singularity-Cover.png';
  import AdventureButton from '$lib/components/AdventureButton.svelte';

  export let data;

  let isPopupOpen = false;
  let showLowerSections = false;

  function showPopup() {
    isPopupOpen = true;
  }

  onMount(() => {
    // Delay showing lower sections for performance
    setTimeout(() => {
      showLowerSections = true;
    }, 1000);
  });
</script>

<svelte:head>
  <title>Surviving the Singularity - Book Preview</title>
  <meta name="description" content="Preview the first draft of 'Surviving the Singularity' and join our community of future-ready individuals.">
</svelte:head>

<main>
  <div class="container" in:fade="{{ duration: 800 }}">
    <section class="book-cover">
      <img src={coverImage} alt="Surviving the Singularity Book Cover" loading="eager">
    </section>

    <section class="disclaimer" in:fade="{{ duration: 1000, delay: 600 }}">
      <h1>First Draft Disclaimer</h1>
      <p>
        Welcome, brave explorer of the future! You're about to dive into the raw, unfiltered first draft of "Surviving the Singularity." 
        This version is offered on a trial, as-is basis. Expect typos, plot holes, and possibly some AI-generated jokes that didn't quite compute.
      </p>
      <p>
        Your feedback is crucial for our survival! If you spot any glitches in the matrix (or just have thoughts to share), 
        please transmit a signal to <a href="https://twitter.com/thecoffeejesus" target="_blank" rel="noopener noreferrer">@thecoffeejesus</a> on any social media platform.
      </p>
      <p>Together, we can make this book as singularity-proof as possible!</p>
    </section>

    <section class="table-of-contents">
      <h2>Table of Contents</h2>
      <TableOfContents sections={data.book.sections} />
    </section>

    <CtaSection 
      text="Ready to embark on your singularity survival journey?"
      buttonClass="adventure-button"
    >
      <AdventureButton on:click={showPopup}>Begin Your Adventure</AdventureButton>
    </CtaSection>

    {#if showLowerSections}
      <Spacer height="50px" />

      <section class="community">
        <h2>Join Our Community</h2>
        <SkoolGroup />
      </section>

      <Spacer height="50px" />

      <section class="newsletter">
        <h2>Stay Updated</h2>
        <NewsletterSignup />
      </section>
    {/if}
  </div>
</main>

<HookEmPopup bind:isOpen={isPopupOpen} />

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  .book-cover {
    text-align: center;
    margin-bottom: 3rem;
  }

  .book-cover img {
    max-width: 100%;
    height: auto;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
  }

  .disclaimer {
    background-color: #ffffff;
    border-left: 4px solid #ff7708;
    padding: 1.5rem;
    margin-bottom: 3rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 0.5rem;
  }

  .disclaimer h1 {
    font-family: 'Orbitron', sans-serif;
    color: #ff7708;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }

  .disclaimer p {
    margin-bottom: 1rem;
    line-height: 1.6;
  }

  .disclaimer a {
    color: #ff7708;
    text-decoration: none;
    font-weight: bold;
    transition: all 0.3s ease;
  }

  .disclaimer a:hover {
    color: #ff9933;
    text-decoration: underline;
  }

  h2 {
    font-family: 'Orbitron', sans-serif;
    color: #ff7708;
    margin-bottom: 1rem;
    font-size: 1.3rem;
  }

  /* Dark mode styles */
  :global(.dark) .disclaimer {
    background-color: #2d3748;
    border-left-color: #ff9933;
  }

  :global(.dark) .disclaimer h1,
  :global(.dark) h2 {
    color: #ff9933;
  }

  :global(.dark) .disclaimer a {
    color: #ff9933;
  }

  :global(.dark) .disclaimer a:hover {
    color: #ffb366;
  }

  @media (max-width: 600px) {
    .container {
      padding: 1rem;
    }

    .disclaimer {
      padding: 1rem;
    }
  }
</style>
