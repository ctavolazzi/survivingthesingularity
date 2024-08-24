<script>
  import skoolClassImage from '$lib/images/skool-class.jpg';

  export let title = "AI Mastery Guild";
  export let subtitle = "Forge Your Future in the AI Revolution";
  export let skoolBenefit = "Join on Skool: Exclusive Community & Resources";
  export let description = "Connect with other forward-thinkers, researchers, and innovators. Navigate the challenges and opportunities of our rapidly changing world together.";
  export let buttonText = "SECURE YOUR SPOT NOW";
  export let imageSrc = skoolClassImage;
  export let imageAlt = "Community members";
  export let handleSkool = () => {};

  export let benefits = [
    "Exclusive AI Innovators Network",
    "Curated AI Tools",
    "Implementation Strategies",
    "Weekly Mastery Sessions",
    "Secret Content Available Nowhere Else"
  ];
  export let limitedOffer = "100 spots at current price. Lock in your lifetime membership now!";
</script>

<div class="skool-group">
  <div class="title-container" on:click={handleSkool} role="button" tabindex="0">
    <h2 class="title">{title}</h2>
    <p class="subtitle">{subtitle}</p>
  </div>
  <div class="content">
    <img src={imageSrc} alt={imageAlt} />
    <p class="skool-benefit" on:click={handleSkool} role="button" tabindex="0">{skoolBenefit}</p>
    <p class="tagline">Your Gateway to AI Mastery</p>
    <p>{description}</p>
    <ul class="benefits">
      {#each benefits as benefit}
        <li>{benefit}</li>
      {/each}
    </ul>
    <p class="limited-offer" on:click={handleSkool} role="button" tabindex="0">{limitedOffer}</p>
    <button on:click={handleSkool}>{buttonText}</button>
  </div>
</div>

<style>
  .skool-group {
    background-color: #ffffff;
    color: #2d3748;
    padding: 1rem;
    border-radius: 0.5rem;
    width: 100%;
    max-width: 800px;
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
    font-size: 1rem;
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
  }

  button {
    width: 100%;
    background: linear-gradient(135deg, #ff9933, #ff8000);
    border: none;
    color: #ffffff;
    padding: 0.75rem 1rem;
    font-weight: bold;
    font-size: 0.9rem;
    border-radius: 0.25rem;
    cursor: pointer;
    transition: opacity 0.3s, transform 0.1s;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
    100% {
      transform: scale(1);
    }
  }

  button:hover, button:focus {
    opacity: 0.9;
    outline: none;
  }

  button:active {
    transform: translateY(1px);
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

  :global(.dark) button {
    background: linear-gradient(135deg, #ff9933, #ff8000);
    color: #2d3748;
  }

  @media (min-width: 640px) {
    .skool-group {
      padding: 1.5rem;
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

    button {
      font-size: 1rem;
      padding: 0.75rem 1.5rem;
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
</style>