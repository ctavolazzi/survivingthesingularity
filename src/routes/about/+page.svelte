<!-- src/routes/about/index.svelte -->
<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import MailchimpSignup from '$lib/components/MailchimpSignup.svelte';

  function handleBackBook() {
    logBackBookClick();
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    alert("The Skool Community is launching next Friday 8/9 - please stay tuned.");
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
      <button class="btn" on:click={() => window.open('https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit?usp=sharing', '_blank')}>
        Read a Sample
      </button>
      <button class="btn" on:click={handleBackBook}>
        Back the Book
      </button>
      <button class="btn" on:click={handleJoinSkool}>
        Join the Skool Community
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
      <button class="btn full-width" on:click={handleBackBook}>Back the Book on Kickstarter</button>
    </div>
  </div>
</div>

<style>
  .container {
    max-width: 100%;
    padding: 1rem;
    color: #333;
  }

  .content {
    text-align: left;
  }

  .title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .description {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .button-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 2rem;
  }

  .btn {
    padding: 0.75rem 1rem;
    border: none;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    text-align: center;
    width: 100%;
    max-width: 300px;
    background-color: #333;
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  .btn:hover {
    background-color: #555;
  }

  .additional-content {
    margin-top: 2rem;
  }

  .section-title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .section-description {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .full-width {
    width: 100%;
    max-width: none;
  }

  @media (min-width: 768px) {
    .container {
      max-width: 768px;
      margin: 0 auto;
      padding: 2rem;
    }

    .title {
      font-size: 2.5rem;
    }

    .description {
      font-size: 1.1rem;
    }

    .button-group {
      flex-direction: row;
      justify-content: center;
      gap: 1rem;
    }

    .btn {
      width: auto;
      margin-bottom: 0;
    }
  }

  @media (min-width: 1024px) {
    .container {
      max-width: 1024px;
    }

    .title {
      font-size: 3rem;
    }

    .description {
      font-size: 1.2rem;
    }
  }
</style>