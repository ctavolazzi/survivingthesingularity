<script>
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import FAQ from '$lib/components/FAQ.svelte';
  import Divider from '$lib/components/Divider.svelte';
  import StSBookImage from '$lib/images/default-blog-image.png';
  import SkoolClassImage from '$lib/images/skool-class.jpg';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  function handleReadSample() {
    window.location.href = 'https://survivingthesingularity.com/sample';
  }
</script>

<div class="main-content">
  <div class="hero-section">
    <h1 class="title">Your Guide to Thriving Through the AI Revolution</h1>
    <Divider />
    <p class="subtitle">Forge your place in the rapidly changing future.</p>
  </div>

  <div class="content-container">
    <h2 class="section-title">What is this all about?</h2>
    <p class="description">
      "Surviving the Singularity" isn't just another tech bro book. It's your family's survival guide for the AI revolution. We're preparing you for a future where:
    </p>
    <ul class="feature-list">
      <li>AI overtakes human intelligence</li>
      <li>Your tech-savvy influences your survival</li>
      <li>The world looks more like science fiction than reality</li>
    </ul>
  </div>

  <div class="cta-container">
    <button class="cta-button primary" on:click={handleBackBook}>BACK THE BOOK</button>
    <button class="cta-button secondary" on:click={handleReadSample}>READ A SAMPLE</button>
  </div>

  <Divider />

  <img src={StSBookImage} alt="Surviving the Singularity Book" class="StS-book-image"  loading="lazy" \/>

  <div class="quote-container">
    <p class="quote">"The future is already here — it's just not very evenly distributed."</p>
    <p class="attribution">- William Gibson</p>
  </div>
  
  <div>
    <button class="sample-button" on:click={handleReadSample}>READ A SAMPLE OF THE BOOK</button>
  </div>
  <FAQ />
  
  <Divider />
  
  <NewsletterSignup />

  <Divider />

  <SkoolGroup />
</div>

<style>
  .main-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .hero-section {
    text-align: center;
    margin-bottom: 2rem;
  }

  .title {
    font-size: 3rem;
    color: var(--color-text-primary);
    margin-bottom: 0.5rem;
  }

  .subtitle {
    font-size: 1.5rem;
    color: var(--color-text-secondary);
    font-style: italic;
  }

  .quote-container {
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }

  .quote {
    font-style: italic;
    font-size: 1.5rem;
    color: var(--color-text-primary);
    margin-bottom: 0.5rem;
  }

  .attribution {
    font-weight: bold;
    color: var(--color-text-secondary);
  }

  .section-title {
    font-size: 2rem;
    color: var(--color-text-primary);
    margin-bottom: 1rem;
    border-bottom: 2px solid #FF9933; /* Lighter orange */
    padding-bottom: 0.5rem;
  }

  .description {
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--color-text-secondary);
    margin-bottom: 1rem;
  }

  .feature-list {
    list-style-type: none;
    padding-left: 0;
    margin-bottom: 2rem;
  }

  .feature-list li {
    padding-left: 1.5rem;
    position: relative;
    margin-bottom: 0.5rem;
  }

  .feature-list li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #FF9933; /* Lighter orange */
    font-weight: bold;
  }

  .cta-container {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
    margin: 2rem 0;
  }

  .cta-button {
    flex: 1;
    padding: 0.75rem 1rem;
    border-radius: 5px;
    font-size: 1rem;
    font-weight: bold;
    text-transform: uppercase;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .cta-button.primary {
    background-color: #FF9933;
    color: white;
    border: none;
  }

  .cta-button.secondary {
    background-color: white;
    color: #FF9933;
    border: 2px solid #FF9933;
  }

  .cta-button:hover {
    opacity: 0.9;
  }

  @media (max-width: 350px) {
    .cta-button {
      font-size: 0.8rem;
      padding: 0.5rem 0.25rem;
    }
  }

  :global(.dark) .quote-container {
    background-color: #2c3e50;
  }

  :global(.dark) .cta-button.primary {
    background: linear-gradient(135deg, #FF9933, #FF6600); /* Orange gradient */
    color: #ffffff;
  }

  :global(.dark) .cta-button.secondary {
    background-color: #2c3e50;
    color: #FF9933; /* Lighter orange */
    border-color: #FF9933; /* Lighter orange */
  }

  :global(.dark) .cta-button.primary:hover {
    background: linear-gradient(135deg, #FFB366, #FF8533); /* Lighter orange gradient on hover */
  }

  :global(.dark) .cta-button.secondary:hover {
    background-color: #34495e;
    border-color: #FFB366; /* Lighter orange on hover */
    color: #FFB366; /* Lighter orange on hover */
  }

  .skool-button {
    width: 100%;
    padding: 0.75rem 1rem;
    margin-top: 1rem;
    background-color: transparent;
    color: #FF9933;
    border: 2px solid #FF9933;
    border-radius: 5px;
    font-size: 1rem;
    font-weight: bold;
    text-transform: uppercase;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  .skool-button:hover {
    background-color: #FF9933;
    color: white;
  }

  :global(.dark) .skool-button {
    color: #FFB366;
    border-color: #FFB366;
  }

  :global(.dark) .skool-button:hover {
    background-color: #FFB366;
    color: #2c3e50;
  }

  .StS-book-image {
    display: block;
    margin: 1rem auto;
    max-width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .community-section {
    margin-bottom: 2rem;
  }

  .community-content {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 2rem;  /* Add some space between the content and the SkoolGroup component */
  }

  .community-text {
    flex: 1;
  }

  .community-image {
    flex: 1;
    max-width: 50%;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  @media (max-width: 768px) {
    .community-content {
      flex-direction: column;
    }

    .community-image {
      max-width: 100%;
      order: -1;
    }
  }
</style>
