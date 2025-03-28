<script>
  import FAQ from '$lib/components/FAQ.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import BookSample from '$lib/components/BookSample.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import TreasureTavernAd from '$lib/components/ads/TreasureTavernAd.svelte';
</script>

<svelte:head>
  <title>About | Surviving the Singularity</title>
  <meta name="description" content="Navigate and thrive in the AI revolution with Surviving the Singularity - a companion for making sense of our rapidly changing world." />
</svelte:head>

<div class="about-page">
  <!-- Hero Section -->
  <header class="hero-section">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <div class="hero-badge">Surviving the Singularity</div>
      <h1 class="hero-title">Navigate and Thrive in the AI Revolution</h1>
      <div class="hero-tagline">
        <p class="hero-description">Expert insights to help you navigate the rapidly evolving world of artificial intelligence and technology.</p>
        <div class="hero-cta">
          <span class="rocket">🚀</span>
          <span class="cta-text">Prepare for the future. Gain valuable insights. Stay ahead of the curve.</span>
        </div>
      </div>
      <div class="hero-scroll">
        <a href="#singularity" class="scroll-btn">
          <span>Learn More</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 13l5 5 5-5"/></svg>
        </a>
      </div>
    </div>
    <div class="hero-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
      <div class="grid-pattern"></div>
    </div>
  </header>

  <!-- Section 1: What is the Singularity? -->
  <section id="singularity" class="singularity-explanation">
    <div class="container">
      <h2>What is the Singularity?</h2>
      <p class="lead">The Technological Singularity refers to a hypothetical future point when artificial intelligence surpasses human intelligence, potentially leading to rapid and unpredictable technological growth.</p>

      <div class="explanation-grid">
        <div class="explanation-card">
          <div class="icon">🧠</div>
          <h3>Beyond Human Intelligence</h3>
          <p>The moment when AI capabilities exceed human cognitive abilities across virtually all domains</p>
        </div>
        <div class="explanation-card">
          <div class="icon">📈</div>
          <h3>Accelerating Change</h3>
          <p>A period of exponential technological advancement that could fundamentally transform society</p>
        </div>
        <div class="explanation-card">
          <div class="icon">🔄</div>
          <h3>Self-Improving Systems</h3>
          <p>AI systems capable of redesigning themselves, creating a feedback loop of rapid enhancement</p>
        </div>
        <div class="explanation-card">
          <div class="icon">❓</div>
          <h3>Unpredictable Outcomes</h3>
          <p>A future that becomes increasingly difficult to predict as technology advances beyond our current understanding</p>
        </div>
        <div class="explanation-card">
          <div class="icon">⚠️</div>
          <h3>Existential Risk</h3>
          <p>The potential for advanced AI systems to pose fundamental challenges to human existence and civilization</p>
        </div>
        <div class="explanation-card">
          <div class="icon">🔗</div>
          <h3>Technological Convergence</h3>
          <p>The merging of AI with other advanced technologies like biotech, nanotech, and quantum computing</p>
        </div>
      </div>

      <p>The concept was popularized by mathematician and author Vernor Vinge and further developed by futurist Ray Kurzweil. While experts debate the timeline and exact nature of the Singularity, the rapid advancement of AI technologies has made these discussions increasingly relevant to our present reality.</p>
    </div>
  </section>

  <!-- Section 2: What is this page all about? -->
  <section class="about-project">
    <div class="container">
      <h2>What is this project all about?</h2>
      <p class="lead">Surviving the Singularity is a resource hub designed to help you navigate the AI revolution that's already underway.</p>

      <div class="project-description">
        <p>This project emerged from a simple observation: we are living through an unprecedented technological transformation, yet most of us lack the frameworks and tools to process these changes meaningfully.</p>

        <p>Our mission is to provide:</p>
        <ul class="mission-list">
          <li><span class="highlight">Clarity</span> — Cutting through the noise and hype around AI</li>
          <li><span class="highlight">Context</span> — Historical and philosophical perspectives on technological change</li>
          <li><span class="highlight">Frameworks</span> — Mental models to help you think about complex AI developments</li>
          <li><span class="highlight">Practical Tools</span> — Resources to help you adapt and thrive amid rapid change</li>
        </ul>

        <p>Whether you're a technologist, business leader, educator, parent, or simply a curious human, this project aims to be your companion through this transformative period.</p>
      </div>

      <!-- Book Preview -->
      <div class="book-preview-section">
        <BookSample />
      </div>
    </div>
  </section>

  <!-- Section 3: What do I need to know right now? -->
  <section class="need-to-know">
    <div class="container">
      <h2>What do I need to know right now?</h2>
      <p class="lead">The AI revolution isn't coming—it's already here, and it's accelerating rapidly.</p>

      <div class="key-insights">
        <div class="insight">
          <h3>AI is transforming every industry</h3>
          <p>From healthcare to education, finance to creative arts, AI is reshaping how we work, learn, and create. Understanding these changes is no longer optional—it's essential for navigating the future.</p>
        </div>

        <div class="insight">
          <h3>The pace of change is unprecedented</h3>
          <p>Unlike previous technological revolutions that unfolded over decades, AI capabilities are doubling every few months. This compressed timeline means we need new approaches to adaptation.</p>
        </div>

        <div class="insight">
          <h3>Critical thinking is more important than ever</h3>
          <p>As AI systems become more powerful and pervasive, developing your own frameworks for evaluating claims, assessing risks, and making decisions becomes increasingly valuable.</p>
        </div>

        <div class="insight">
          <h3>There are practical steps you can take</h3>
          <p>From understanding AI capabilities to developing complementary skills, there are concrete ways to position yourself advantageously amid these changes.</p>
        </div>
      </div>

      <div class="faq-section">
        <h3>Common Questions</h3>
        <FAQ />
      </div>
    </div>
  </section>

  <!-- Section 4: How can I support this project? -->
  <section class="support-section">
    <div class="container">
      <h2>How can I support this project?</h2>

      <div class="support-grid">
        <div class="support-card">
          <div class="support-icon">📚</div>
          <h3>Read and Share</h3>
          <p>Explore our free resources and share them with others who might benefit.</p>
        </div>

        <div class="support-card">
          <div class="support-icon">💬</div>
          <h3>Provide Feedback</h3>
          <p>Share your thoughts and suggestions to help shape future content.</p>
          <a href="/contact" class="contact-button" data-sveltekit-preload-data="hover">
            Contact Us
          </a>
        </div>

        <div class="support-card">
          <div class="support-icon">🤝</div>
          <h3>Collaborate</h3>
          <p>If you have expertise that could contribute to this project, reach out to discuss collaboration.</p>
        </div>
      </div>

      <div class="newsletter-section">
        <h3><span class="newsletter-icon">✉️</span> Join the Newsletter</h3>
        <NewsletterSignup />
        <DiscordButton />
      </div>
    </div>
  </section>

  <!-- Footer -->
  <section class="contact">
    <div class="container">
      <!-- Copyright notice removed -->
    </div>
  </section>

  <!-- Treasure Tavern Ad -->
  <section class="treasure-tavern-section">
    <div class="container">
      <TreasureTavernAd
        title="Discover Unique Treasures"
        subtitle="The Treasure Tavern"
        description="Curated gems from the far corners of the Internet."
        bulletPoints={[
          "Unique finds you won't see elsewhere",
          "Each item has a story to tell",
          "Fresh collections added monthly"
        ]}
        ctaText="Explore the Tavern"
        ctaUrl="https://treasuretavernhq.com/"
        badgeText="New Arrivals"
      />
    </div>
  </section>
</div>

<style>
  /* Base Styles */
  .about-page {
    width: 100%;
    color: #e5e7eb;
  }

  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
    position: relative;
    z-index: 2;
  }

  h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
    margin: 0 0 1.5rem 0;
  }

  h1 {
    font-size: 3rem;
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-align: center;
  }

  h2 {
    font-size: 2rem;
    color: #a78bfa;
    margin-bottom: 1.5rem;
  }

  h3 {
    font-size: 1.25rem;
    color: #a78bfa;
    margin-bottom: 0.75rem;
  }

  p {
    margin: 0 0 1rem 0;
    line-height: 1.6;
  }

  .lead {
    font-size: 1.25rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
  }

  /* Hero Section */
  .hero-section {
    position: relative;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 1.5rem;
    overflow: hidden;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    margin-bottom: 3rem;
  }

  .hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.15), transparent 50%);
    z-index: 1;
  }

  .hero-content {
    position: relative;
    max-width: 900px;
    width: 100%;
    text-align: center;
    z-index: 2;
    animation: fadeIn 1s ease-out forwards;
  }

  .hero-badge {
    display: inline-block;
    background: rgba(124, 58, 237, 0.15);
    color: #a78bfa;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(124, 58, 237, 0.2);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(10px);
    opacity: 1;
    animation: none;
  }

  .hero-title {
    font-size: clamp(3rem, 8vw, 4.5rem);
    margin-bottom: 1.5rem;
    color: white;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
    background: linear-gradient(120deg, #f0f9ff, #e0f2fe, #bae6fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    transform: translateY(10px);
    opacity: 1;
    animation: none;
  }

  .hero-tagline {
    max-width: 700px;
    margin: 0 auto;
    transform: translateY(10px);
    opacity: 1;
    animation: none;
  }

  .hero-description {
    font-size: clamp(1.1rem, 2vw, 1.25rem);
    line-height: 1.6;
    margin-bottom: 1rem;
    color: #e2e8f0;
  }

  .hero-cta {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin: 2rem auto;
    padding: 1rem 1.5rem;
    background: rgba(30, 41, 59, 0.6);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    max-width: max-content;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }

  .rocket {
    font-size: 1.8rem;
    display: inline-block;
    animation: rocketShake 2s infinite ease-in-out;
  }

  .cta-text {
    font-size: clamp(0.95rem, 2vw, 1.05rem);
    font-weight: 500;
    color: #f8fafc;
    font-style: italic;
  }

  .hero-decoration {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    overflow: hidden;
  }

  .circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
  }

  .circle-1 {
    width: 400px;
    height: 400px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    top: -120px;
    right: -100px;
    animation: float 15s infinite ease-in-out;
  }

  .circle-2 {
    width: 300px;
    height: 300px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    bottom: -80px;
    left: -80px;
    animation: float 18s infinite ease-in-out reverse;
  }

  .circle-3 {
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(124, 58, 237, 0.1), transparent);
    top: 20%;
    left: 10%;
    animation: pulse 8s infinite alternate;
  }

  .grid-pattern {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    z-index: -1;
  }

  /* Animations */
  @keyframes float {
    0%, 100% {
      transform: translateY(0) rotate(0deg);
    }
    50% {
      transform: translateY(-20px) rotate(5deg);
    }
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 0.4;
      transform: scale(1);
    }
    50% {
      opacity: 0.6;
      transform: scale(1.1);
    }
  }

  @keyframes rocketShake {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-5px);
    }
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .hero-section {
      padding: 3rem 1rem;
      min-height: 450px;
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .hero-description {
      font-size: 1rem;
    }

    .hero-cta {
      padding: 0.75rem 1rem;
    }

    .rocket {
      font-size: 1.5rem;
    }

    .cta-text {
      font-size: 0.9rem;
    }
  }

  @media (max-width: 480px) {
    .hero-section {
      min-height: 400px;
    }

    .hero-badge {
      font-size: 0.8rem;
    }

    .hero-title {
      font-size: 2rem;
    }

    .hero-cta {
      flex-direction: column;
      gap: 0.5rem;
    }
  }

  /* Singularity Explanation Section */
  .singularity-explanation {
    background-color: #1a1a2e;
  }

  .singularity-explanation .lead {
    line-height: 1.6;
    margin-bottom: 1.5rem;
    color: rgba(229, 231, 235, 0.95);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .singularity-explanation p {
    line-height: 1.7;
  }

  .explanation-grid {
    display: grid;
    grid-template-columns: repeat(1, minmax(250px, 1fr));
    gap: 1rem;
    margin: 2rem auto;
    max-width: 1200px;
    justify-content: center;
  }

  @media (min-width: 640px) {
    .explanation-grid {
      grid-template-columns: repeat(2, minmax(250px, 1fr));
    }
  }

  @media (min-width: 1024px) {
    .explanation-grid {
      grid-template-columns: repeat(3, minmax(250px, 1fr));
    }
  }

  .explanation-card {
    background-color: rgba(30, 30, 50, 0.5);
    background-image: linear-gradient(to bottom, rgba(30, 30, 60, 0.5), rgba(20, 20, 40, 0.5));
    border: 1px solid rgba(124, 58, 237, 0.2);
    border-radius: 12px;
    padding: 1.25rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    max-width: 400px;
    margin: 0 auto;
    width: 100%;
  }

  .explanation-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    border-color: rgba(124, 58, 237, 0.4);
  }

  .icon {
    font-size: 2rem;
    margin-bottom: 1rem;
    opacity: 0.9;
  }

  .explanation-card h3 {
    font-size: 1.3rem;
    margin-bottom: 0.75rem;
    color: #a78bfa;
  }

  .explanation-card p {
    margin-bottom: 0;
    color: rgba(229, 231, 235, 0.85);
    line-height: 1.6;
  }

  /* About Project Section */
  .about-project {
    background-color: #0f0f23;
    background-image: linear-gradient(to bottom, #0f0f23, #0d0d1f);
  }

  .project-description {
    margin-bottom: 2rem;
    max-width: 900px;
  }

  .mission-list {
    list-style: none;
    padding: 0;
    margin: 1.25rem 0;
  }

  .mission-list li {
    margin-bottom: 0.75rem;
    padding-left: 1.75rem;
    position: relative;
  }

  .mission-list li:before {
    content: "→";
    position: absolute;
    left: 0;
    color: #a78bfa;
    font-weight: bold;
  }

  .highlight {
    color: #a78bfa;
    font-weight: 600;
    text-shadow: 0 0 10px rgba(167, 139, 250, 0.2);
  }

  .book-preview-section {
    margin-top: 2rem;
  }

  /* Need to Know Section */
  .need-to-know {
    background-color: #1a1a2e;
    background-image: linear-gradient(to bottom, #1a1a2e, #181830);
  }

  .key-insights {
    margin: 2rem 0;
  }

  .insight {
    padding: 1.25rem;
    margin-bottom: 1.25rem;
  }

  .faq-section {
    margin-top: 3.5rem;
  }

  /* Support Section */
  .support-section {
    background-color: #0f0f23;
    padding: 2rem 0;
  }

  .support-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .support-card {
    background-color: rgba(30, 30, 50, 0.5);
    border-radius: 12px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid rgba(124, 58, 237, 0.1);
  }

  .support-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    border-color: rgba(124, 58, 237, 0.3);
  }

  .support-icon {
    font-size: 2.25rem;
    margin-bottom: 0.75rem;
  }

  .support-card h3 {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    color: #a78bfa;
  }

  .support-card p {
    margin-bottom: 1rem;
    line-height: 1.5;
  }

  .contact-button {
    display: inline-block;
    background-color: rgba(124, 58, 237, 0.2);
    color: #a78bfa;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
    text-align: center;
    width: 100%;
  }

  .contact-button:hover {
    background-color: rgba(124, 58, 237, 0.3);
    transform: translateY(-2px);
  }

  .newsletter-section {
    margin-top: 2rem;
    margin-bottom: 0.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .newsletter-section h3 {
    text-align: center;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }

  .newsletter-icon {
    font-size: 1.2em;
    vertical-align: middle;
    margin-right: 0.5rem;
  }

  /* Responsive adjustments */
  @media (min-width: 768px) {
    .support-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .contact-button {
      width: auto;
    }

    .support-card {
      padding: 2rem;
    }
  }

  /* Contact Section */
  .contact {
    text-align: center;
    padding-bottom: 0;
    background-color: #0f0f23;
  }

  .hero-scroll {
    margin-top: 2rem;
  }

  .scroll-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.75rem;
    background-color: rgba(124, 58, 237, 0.1);
    border: 1px solid rgba(124, 58, 237, 0.3);
    border-radius: 30px;
    color: #a78bfa;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.5s ease;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
  }

  .scroll-btn:hover {
    background-color: rgba(124, 58, 237, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }

  .scroll-btn svg {
    animation: gentle-bounce 4s ease-in-out infinite;
    opacity: 0.8;
  }

  @keyframes gentle-bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(3px);
    }
    60% {
      transform: translateY(2px);
    }
  }

  /* Treasure Tavern Section */
  .treasure-tavern-section {
    background-color: #0f0f23;
    padding-bottom: 3rem;
    margin-top: -4rem;
  }

  @media (max-width: 768px) {
    .treasure-tavern-section {
      padding-bottom: 2rem;
      margin-top: -3rem;
    }
  }

  @media (max-width: 480px) {
    .treasure-tavern-section {
      margin-top: -2.5rem;
    }
  }
</style>