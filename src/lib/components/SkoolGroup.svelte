<script>
  import stsWelcomeImage from '$lib/images/sts-welcome.png';
  import { onMount } from 'svelte';

  export let title = "AI Mastery Guild: Surviving the Singularity";
  export let subtitle = "Join Our Exclusive Community & Accelerate Your AI Journey";
  export let skoolBenefit = "Exclusive Skool Community: Your Gateway to AI Mastery";
  export let description = "Become part of the 'Surviving the Singularity' program - a comprehensive AI learning experience that includes our book, exclusive Skool community, and much more!";
  export let buttonText = "SECURE YOUR SPOT NOW";
  export let imageSrc = stsWelcomeImage;
  export let imageAlt = "Surviving the Singularity Welcome";

  const programBenefits = [
    "Exclusive access to our innovative thinkers' network",
    "Connect with peers, from curious beginners to seasoned professionals",
    "Early insights into groundbreaking research and technologies",
    "Digital and physical copies of 'Surviving the Singularity'",
    "Lifetime updates to keep you at the forefront of innovation"
  ];

  let spotsLeft = 100;
  let countdownInterval;

  function randomDelay() {
    return Math.floor(Math.random() * 10000) + 1000; // Random delay between 1 and 10 seconds
  }

  function decrementSpots() {
    if (spotsLeft > 0) {
      spotsLeft--;
      countdownInterval = setTimeout(decrementSpots, randomDelay());
    }
  }

  onMount(() => {
    countdownInterval = setTimeout(decrementSpots, randomDelay());
    return () => clearTimeout(countdownInterval);
  });

  $: limitedOffer = `${spotsLeft} spots left at current price. Lock in your lifetime membership now!`;

  $: isUrgent = spotsLeft <= 20;

  export let testimonials = [
    {
      text: "I've learned more about AI in the last month than I did in the last year on my own. This community is amazing!",
      author: "Emily W., AI Enthusiast"
    },
    {
      text: "The weekly mastery sessions alone are worth the price of admission. Highly recommended for anyone serious about the future.",
      author: "Michael T., Tech Entrepreneur"
    }
  ];

  function handleSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }
</script>

<div class="skool-group">
  <div class="title-container" on:click={handleSkool} role="button" tabindex="0">
    <h2 class="title">{title}</h2>
    <p class="subtitle">{subtitle}</p>
  </div>
  <div class="content">
    <img src={imageSrc} alt={imageAlt} />
    <p class="skool-benefit" on:click={handleSkool} role="button" tabindex="0">{skoolBenefit}</p>
    <p class="tagline">Your Complete AI Mastery Program</p>
    <p>{description}</p>
    <h3>What You'll Get:</h3>
    <ul class="benefits">
      {#each programBenefits as benefit}
        <li>{benefit}</li>
      {/each}
    </ul>

    <div class="testimonials">
      {#each testimonials as testimonial}
      <div class="testimonial">
        <svg class="quote-icon" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"></path>
          <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"></path>
        </svg>
        <p class="testimonial-text">{testimonial.text}</p>
        <p class="testimonial-author">{testimonial.author}</p>
      </div>
      {/each}
    </div>

    <button on:click={handleSkool}>{buttonText}</button>
    <p class="dont-wait">Don't miss out on this opportunity to future-proof your skills!</p>
    <p class="limited-offer" class:urgent={isUrgent} on:click={handleSkool} role="button" tabindex="0">{limitedOffer}</p>
    <button class="final-cta" on:click={handleSkool}>Start Your AI Mastery Journey Today</button>
    <p class="cta-explanation">By clicking this button, you'll be directed to our Skool community page where you can join the AI Mastery Guild and gain access to all program benefits.</p>
    <button class="community-cta" on:click={handleSkool}>Join the Skool Community</button>
  </div>
</div>

<style>
  .skool-group {
    max-width: 800px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
    background-color: #ffffff;
    color: #2d3748;
    border-radius: 0.5rem;
    width: 100%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .title-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 1.5rem 1.5rem 1.75rem;
    border-radius: 0.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
  }

  .title-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #ff9933, #ff7708);
  }

  .title {
    font-size: 2.25rem;
    font-weight: 800;
    text-align: center;
    margin: 0;
    line-height: 1.2;
    color: #2d3748;
    letter-spacing: -0.025em;
  }

  .subtitle {
    font-size: 1.25rem;
    text-align: center;
    margin: 0.75rem 0 0;
    color: #4a5568;
    font-weight: 500;
    letter-spacing: 0.025em;
  }

  .skool-benefit {
    font-size: 0.9rem;
    text-align: center;
    margin-bottom: 1rem;
    color: #ff7708;
    font-weight: 600;
    letter-spacing: 0.025em;
    text-transform: uppercase;
    background-color: rgba(255, 153, 51, 0.1);
    padding: 0.5rem;
    border-radius: 0.25rem;
  }

  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  img {
    width: 100%;
    height: auto;
    border-radius: 0.25rem;
    margin-bottom: 0.75rem;
  }

  p {
    text-align: center;
    margin-bottom: 0.75rem;
    line-height: 1.4;
    font-size: 0.9rem;
  }

  .tagline {
    font-weight: bold;
    font-size: 1.5rem !important;
    color: #ff7708;
    margin-bottom: 0.5rem;
  }

  .benefits {
    list-style-type: none;
    padding: 0;
    margin-bottom: 1rem;
    text-align: left;
    width: 100%;
  }

  .benefits li {
    margin-bottom: 0.5rem;
    padding-left: 1.5rem;
    position: relative;
  }

  .benefits li::before {
    content: "✅";
    position: absolute;
    left: 0;
  }

  .limited-offer {
    font-weight: bold;
    color: #d03050;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 2px solid currentColor;
    border-radius: 0.25rem;
    transition: background-color 0.3s ease;
  }

  .limited-offer:global(.urgent) {
    background-color: rgba(208, 48, 80, 0.1);
  }

  button, .final-cta {
    width: 100%;
    background: linear-gradient(135deg, #ff9933, #ff8000);
    border: none;
    color: #ffffff;
    padding: 1rem 1.5rem;
    font-weight: bold;
    font-size: 1.1rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: opacity 0.3s, transform 0.1s;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 6px rgba(255, 128, 0, 0.3);
    margin-bottom: 0.25rem;
  }

  button:hover, button:focus,
  .final-cta:hover, .final-cta:focus {
    opacity: 0.9;
    outline: none;
  }

  button:active, .final-cta:active {
    transform: translateY(2px);
  }

  .final-cta {
    margin-top: 1rem;
    animation: none; /* Ensures no flashing effect */
  }

  .community-cta {
    width: 50%;
    margin: 1rem auto 0;
    background: linear-gradient(135deg, #20B2AA, #008B8B);
    border: none;
    color: #ffffff;
    padding: 0.75rem 1rem;
    font-weight: bold;
    font-size: 0.9rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: opacity 0.3s, transform 0.1s;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    box-shadow: 0 2px 4px rgba(0, 139, 139, 0.3);
    display: block;
  }

  .community-cta:hover, .community-cta:focus {
    opacity: 0.9;
    outline: none;
  }

  .community-cta:active {
    transform: translateY(2px);
  }

  :global(.dark) .skool-group {
    background-color: #2d3748;
    color: #f7fafc;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  }

  :global(.dark) .title-container {
    background: linear-gradient(135deg, #2d3748, #4a5568);
    border: none;
  }

  :global(.dark) .title {
    color: #ffffff;
  }

  :global(.dark) .subtitle {
    color: #e2e8f0;
  }

  :global(.dark) .skool-benefit {
    color: #ffb366;
    background-color: rgba(255, 179, 102, 0.1);
  }

  :global(.dark) .tagline {
    color: #ffb366;
  }

  :global(.dark) .limited-offer {
    color: #ff9999;
  }

  :global(.dark) button, :global(.dark) .final-cta {
    color: #2d3748;
  }

  :global(.dark) .community-cta {
    background: linear-gradient(135deg, #5F9EA0, #008B8B);
    color: #ffffff;
  }

  @media (min-width: 640px) {
    .skool-group {
      padding: 2rem 1.5rem;
    }

    .title {
      font-size: 2.75rem;
    }

    .subtitle {
      font-size: 1.5rem;
    }

    .skool-benefit {
      font-size: 1rem;
    }

    p {
      font-size: 1rem;
      margin-bottom: 1rem;
    }

    .tagline {
      font-size: 1.2rem;
    }

    button, .final-cta {
      font-size: 1.2rem;
      padding: 1.25rem 2rem;
    }

    .community-cta {
      font-size: 1rem;
      padding: 0.875rem 1.25rem;
    }
  }

  .title-container,
  .skool-benefit,
  .limited-offer {
    cursor: pointer;
  }

  .title-container:hover,
  .skool-benefit:hover,
  .limited-offer:hover {
    opacity: 0.8;
  }

  .title-container:focus,
  .skool-benefit:focus,
  .limited-offer:focus {
    outline: 2px solid #ff7708;
    outline-offset: 2px;
  }

  .testimonials {
    width: 100%;
    margin: 1rem 0;
    display: grid;
    gap: 1rem;
  }

  .testimonial {
    background-color: #ffffff;
    border-radius: 1rem;
    padding: 1rem;
    position: relative;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    overflow: hidden;
  }

  .testimonial::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #ff9933, #ff7708);
  }

  .testimonial:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  .quote-icon {
    position: absolute;
    top: 1rem;
    left: 1rem;
    color: #ff9933;
    opacity: 0.2;
    width: 48px;
    height: 48px;
  }

  .testimonial-text {
    font-style: italic;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
    line-height: 1.8;
    color: #4a5568;
    position: relative;
    z-index: 1;
  }

  .testimonial-author {
    font-weight: 600;
    text-align: right;
    font-size: 1rem;
    color: #2d3748;
  }

  :global(.dark) .testimonial {
    background-color: #2d3748;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
  }

  :global(.dark) .testimonial::before {
    background: linear-gradient(90deg, #ffb366, #ff9933);
  }

  :global(.dark) .quote-icon {
    color: #ffb366;
  }

  :global(.dark) .testimonial-text {
    color: #e2e8f0;
  }

  :global(.dark) .testimonial-author {
    color: #f7fafc;
  }

  @media (min-width: 640px) {
    .testimonials {
      grid-template-columns: repeat(2, 1fr);
    }

    .testimonial-text {
      font-size: 1.2rem;
    }

    .testimonial-author {
      font-size: 1.1rem;
    }
  }

  .dont-wait {
    font-size: 0.9rem;
    font-weight: 600;
    color: #d03050;
    text-align: center;
    margin-bottom: 0.5rem;
  }

  :global(.dark) .dont-wait {
    color: #ff9999;
  }

  @media (min-width: 640px) {
    .dont-wait {
      font-size: 1rem;
    }
  }

  .skool-group {
    max-width: 800px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  h2 {
    margin-bottom: 0.5rem;
  }

  p {
    margin-bottom: 0.5rem;
  }

  .testimonials {
    margin: 1rem 0;
  }

  .testimonial {
    margin-bottom: 1rem;
    padding: 1rem;
  }

  .testimonial-text {
    margin-bottom: 0.5rem;
  }

  button {
    margin-bottom: 0.25rem;
  }

  .dont-wait {
    font-size: 1.2rem;
    font-weight: 600;
    color: #d03050;
    text-align: center;
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
  }

  .limited-offer {
    margin-top: 0.5rem;
    padding: 0.5rem;
  }

  @media (min-width: 640px) {
    .skool-group {
      padding: 2rem 1.5rem;
    }

    .testimonials {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
    }

    .testimonial {
      margin-bottom: 0;
    }
  }

  .cta-explanation {
    font-size: 0.9rem;
    color: #4a5568;
    text-align: center;
    margin-top: 0.5rem;
  }

  :global(.dark) .cta-explanation {
    color: #e2e8f0;
  }
</style>