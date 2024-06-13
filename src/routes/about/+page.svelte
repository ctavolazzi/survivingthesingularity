<!-- src/routes/about/index.svelte -->
<script>
  // import BottomNav from '../../components/BottomNav.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import MailchimpSignup from '$lib/components/MailchimpSignup.svelte';
  // import BackBookButton from '../../components/BackBookButton.svelte';
  // import BuyBookButton from '../../components/BuyBookButton.svelte';
  // import { supabase } from '$lib/supabaseClient';

  // async function logBackBookClick() {
  //   console.log('Back Book Clicked');
  // }

  async function logBackBookClick() {
    await supabase.from('back_book_clicks').insert({
      timestamp: new Date(),
      referrer: window.location.href,
      user_agent: navigator.userAgent,
    });
  }

  function handleBackBook() {
    logBackBookClick();
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
  }
</script>

<div class="container">
  <div class="content">
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

    <div class="button-group">
      <button class="sample-button" on:click={() => window.open('https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit?usp=sharing', '_blank')}>
        Read a Sample
      </button>
      <!-- <BackBookButton class="back-button" on:click={() => window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank')}>
      </BackBookButton>
      <BuyBookButton class="buy-button" on:click={() => window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank')}>
      </BuyBookButton> -->
      <button class="back-button" on:click={() => handleBackBook()}>
        Back the Book
      </button>
    </div>

    <div class="additional-content">
      <div class="section">
        <h2 class="section-title">Our Mission</h2>
        <p class="section-description">
          Our mission is to help you understand the Singularity and its impact on our lives. Join our community of forward-thinkers, researchers, and innovators to navigate the challenges and opportunities of this rapidly changing world.
        </p>
      </div>

      <div class="section">
        <h2 class="section-title">Stay Updated</h2>
        <p class="section-description">
          Subscribe to our newsletter for regular updates, insights, and exclusive content about the technological Singularity.
        </p>
        <MailchimpSignup />
      </div>
      <p class="section-description">
        "Surviving the Singularity" is sponsored by AIECO, a humanity-focused organization.
      </p>
    </div>
  </div>
</div>

<!-- Spacer for bottom navigation -->
<Spacer height="4rem"/>

<!-- <BottomNav /> -->

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    color: #333;
  }

  .content {
    text-align: left;
  }

  .title {
    font-size: 3rem;
    margin-bottom: 2rem;
  }

  .description {
    font-size: 1.2rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .button-group {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .sample-button {
    padding: 1rem 2rem;
    background-color: #333;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .sample-button:hover {
    background-color: #555;
  }

  .back-button {
    padding: 1rem 2rem;
    background-color: #333;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .back-button:hover {
    background-color: #555;
  }

  .additional-content {
    margin-top: 3rem;
  }

  .section-title {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .section-description {
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }
</style>