<script>
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import FAQ from '$lib/components/FAQ.svelte';
  import StSBookImage from '$lib/images/default-blog-image.png';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';
  import Countdown from '$lib/components/Countdown.svelte';
  
  const targetDate = new Date("2027-11-20T23:59:59").getTime();

  function handleReadSample() {
    window.location.href = 'https://survivingthesingularity.com/sample';
  }

  function handleJoinSkool() {
    console.log('Join Skool functionality not implemented yet');
  }
</script>

<div class="main-content">
  <div class="hero-section">
    <h1 class="title">What the f*** is going on?</h1>
    <p class="subtitle">AI seems to be taking over the world - are you on boarding the Singularity Express or will you be left behind at the station?</p>
    <!-- <button class="cta-button primary" on:click={handleJoinSkool}>JOIN THE MADNESS</button> -->
  </div>

  <div class="wtf-section">
    <h2 class="section-title">No, seriously, WTF?</h2>
    <p class="description">
      Remember when the scariest thing about AI was autocorrect? Those were the days. Now we've got:
    </p>
    <ul class="wtf-list">
      <li>AI writing your college essays (and probably doing a better job)</li>
      <li>Robots that can parkour better than you</li>
      <li>ChatGPT stealing your job while you're reading this</li>
    </ul>
    <p class="description">
      And that's just Tuesday. Welcome to the singularity, folks. It's weird, it's wild, and it's happening faster than you can say "artificial intelligence."
    </p>
  </div>

  <div class="survival-kit">
    <h2 class="section-title">Your Singularity Survival Kit</h2>
    <p>A book, a community, and a plan to survive the Singularity</p>
    <p>Author Chris Tavolazzi has been hard at work on building a resource to help you process the arrival of the future.</p>
    <div class="kit-item">
      <img src={StSBookImage} alt="Surviving the Singularity Book" class="StS-book-image" />
      <div class="kit-info">
        <p class="osm">The "Oh Sh*t" Manual</p>
        <p>Our book is for when Google can't help you navigate the AI apocalypse</p>
        <br>
        <button class="cta-button secondary" on:click={handleReadSample}>SNEAK A PEEK</button>
      </div>
    </div>
  </div>

  <div class="faq-section">
    <FAQ />
  </div>

  <div class="newsletter-section">
    <h2 class="section-title">Stay in the Loop (While You Still Can)</h2>
    <p class="description center-text">Sign up for our newsletter. It's like a time capsule, but for the future that's happening now.</p>
    <NewsletterSignup />
  </div>

  <div class="mission-statement">
    <h2 class="section-title">Our "Keep Calm and Carry On" Mission</h2>
    <p class="description">
      At Surviving the Singularity, we're not here to stop the AI tsunami. We're here to teach you how to surf it. With a mix of humor, panic, and actual useful information, we're building a community of humans trying to stay relevant in an increasingly robotic world.
    </p>
  </div>

  <SkoolGroup />

  <div class="testimonial-section">
    <h3 class="testimonial-header">What Our Members Say</h3>
    <div class="testimonial-grid">
      <div class="testimonial">
        <p>"This community has been my lifeline in understanding AI. It's like having a cheat code for the future!"</p>
        <span class="testimonial-author">- Sarah K., Software Dev</span>
      </div>
      <div class="testimonial">
        <p>"I thought I was doomed when AI started writing better code than me. This book gave me hope and a game plan!"</p>
        <span class="testimonial-author">- Mike R., Data Scientist</span>
      </div>
      <div class="testimonial">
        <p>"Finally, a resource that doesn't make me feel like a Luddite for being cautious about AI. Informative and hilarious!"</p>
        <span class="testimonial-author">- Emma L., Marketer</span>
      </div>
      <div class="testimonial">
        <p>"I thought I was doomed when AI started writing better code than me. This book gave me hope and a game plan!"</p>
        <span class="testimonial-author">- Mike G., Father</span>
      </div>
    </div>
  </div>

  <div class="countdown-section">
    <Countdown targetDate={targetDate} />
    <p class="countdown-cta">Don't let AI catch you unprepared.</p>
  </div>

  <div class="final-cta-section">
    <h2 class="section-title">Ready to Survive the Singularity?</h2>
    <p class="description">Join the Skool community to get access to our book, resources, and a community of like-minded individuals.</p>
    <button class="skool-button" on:click={handleJoinSkool}>JOIN THE MADNESS</button>
  </div>
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
    margin-top: 1rem;
    padding: 0.75rem 3rem;
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

  .community-intro,
  .resources-section,
  .book-preview,
  .mission-statement {
    margin-bottom: 2rem;
  }

  .community-intro .description,
  .resources-section .description,
  .book-preview .book-description,
  .mission-statement .description {
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--color-text-secondary);
    margin-bottom: 1rem;
  }

  .wtf-list {
    list-style-type: none;
    padding-left: 0;
  }

  .wtf-list li {
    padding-left: 1.5rem;
    position: relative;
    margin-bottom: 0.5rem;
  }

  .wtf-list li::before {
    content: "🤖";
    position: absolute;
    left: 0;
  }

  .kit-item {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }

  .kit-info {
    margin-left: 1rem;
  }

  .surfer-section {
    background-color: var(--color-background-secondary);
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 1.5rem;
    text-align: center;
  }

  .surfer-section h3 {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
    color: var(--color-text-primary);
  }

  .surfer-section p {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .surfer-section .cta-button {
    display: inline-block;
    margin-top: 0.5rem;
  }

  .osm {
    font-weight: bold;
    font-size: 1.1rem;
  }

  .final-cta-section {
    background-color: var(--color-background-secondary);
    padding: 2rem;
    border-radius: 8px;
    margin-top: 2rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .pulse-animation {
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

  .testimonial-section {
    margin-top: 2rem;
    text-align: center;
  }

  .testimonial-header {
    font-size: 1.8rem;
    color: var(--color-text-primary);
    margin-bottom: 1.5rem;
  }

  .testimonial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .testimonial {
    font-style: italic;
    background-color: var(--color-background-secondary);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
  }

  .testimonial:hover {
    transform: translateY(-5px);
  }

  .testimonial-author {
    display: block;
    margin-top: 0.5rem;
    font-weight: bold;
    color: var(--color-text-secondary);
  }

  .countdown-section {
    margin-top: 2rem;
    text-align: center;
    background-color: var(--color-background-secondary);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .countdown-header {
    font-size: 1.5rem;
    color: var(--color-text-primary);
    margin-bottom: 1rem;
  }

  .countdown-cta {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--color-text-primary);
    margin-top: 1rem;
  }

  .center-text {
    text-align: center;
  }
</style>