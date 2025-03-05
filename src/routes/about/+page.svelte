<script>
  import FAQ from '$lib/components/FAQ.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import BookSample from '$lib/components/BookSample.svelte';
</script>

<svelte:head>
  <title>About | Surviving the Singularity</title>
  <meta name="description" content="Navigate and thrive in the AI revolution with Surviving the Singularity - a companion for making sense of our rapidly changing world." />
</svelte:head>

<div class="about-page">
  <!-- Hero Section -->
  <header class="hero">
    <div class="hero-background">
      <div class="grid-lines"></div>
      <div class="glow-orb"></div>
    </div>
    <div class="container">
      <div class="hero-content">
        <h1 class="title">Surviving the Singularity</h1>
        <div class="subtitle-container">
          <p class="subtitle">Navigate and Thrive in the AI Revolution</p>
          <div class="animated-bar"></div>
        </div>
        <div class="hero-cta">
          <a href="#singularity" class="scroll-btn">
            <span>Learn More</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 13l5 5 5-5"/></svg>
          </a>
        </div>
      </div>
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
          <a href="mailto:hello@survivingthesingularity.com" class="contact-button">
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
      </div>
    </div>
  </section>

  <!-- Footer -->
  <section class="contact">
    <div class="container">
      <p class="copyright">© {new Date().getFullYear()} Surviving the Singularity. All rights reserved.</p>
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
    padding: 3rem 1.5rem;
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
  .hero {
    background-color: #0a0a1a;
    position: relative;
    overflow: hidden;
    height: 70vh;
    max-height: 600px;
    min-height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 20px;
    margin: 0 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }

  .hero-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    padding: 20px;
    box-sizing: border-box;
  }

  .grid-lines {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      linear-gradient(rgba(124, 58, 237, 0.08) 1px, transparent 1px),
      linear-gradient(90deg, rgba(124, 58, 237, 0.08) 1px, transparent 1px);
    background-size: 50px 50px;
    perspective: 1000px;
    transform-style: preserve-3d;
    transform: rotateX(60deg) scale(1.5);
    animation: grid-move 60s linear infinite;
    opacity: 0.8;
    border-radius: 40px;
    overflow: hidden;
    border: 1px solid rgba(124, 58, 237, 0.15);
    box-shadow: 0 0 30px rgba(124, 58, 237, 0.1);
    margin: 20px;
    mask-image: radial-gradient(circle at center, black 80%, transparent 100%);
    -webkit-mask-image: radial-gradient(circle at center, black 80%, transparent 100%);
  }

  .glow-orb {
    position: absolute;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 40%, rgba(139, 92, 246, 0) 70%);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    filter: blur(60px);
    opacity: 0.6;
    animation: pulse 15s ease-in-out infinite alternate;
  }

  .hero-content {
    text-align: center;
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
  }

  .title {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 0 15px rgba(167, 139, 250, 0.2);
    transition: text-shadow 0.5s ease;
  }

  .title:hover {
    text-shadow: 0 0 20px rgba(167, 139, 250, 0.4);
  }

  .subtitle-container {
    position: relative;
    display: inline-block;
    margin-bottom: 2.5rem;
  }

  .subtitle {
    font-size: 1.5rem;
    color: #e5e7eb;
    margin-bottom: 0.75rem;
    font-weight: 300;
    letter-spacing: 0.05em;
  }

  .animated-bar {
    height: 1px;
    width: 0;
    background: linear-gradient(90deg, transparent, rgba(167, 139, 250, 0.5), transparent);
    margin: 0 auto;
    animation: expand 3s ease-out forwards;
  }

  .hero-cta {
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

  /* Animations */
  @keyframes grid-move {
    0% {
      background-position: 0 0;
    }
    100% {
      background-position: 50px 50px;
    }
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 0.4;
      transform: translate(-50%, -50%) scale(1);
    }
    50% {
      opacity: 0.6;
      transform: translate(-50%, -50%) scale(1.1);
    }
  }

  @keyframes expand {
    0% {
      width: 0;
    }
    100% {
      width: 100%;
    }
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

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .hero {
      height: 60vh;
    }

    .title {
      font-size: 2.5rem;
    }

    .subtitle {
      font-size: 1.2rem;
    }
  }

  /* Singularity Explanation Section */
  .singularity-explanation {
    background-color: #1a1a2e;
  }

  .singularity-explanation .lead {
    line-height: 1.7;
    margin-bottom: 2rem;
    color: rgba(229, 231, 235, 0.95);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .singularity-explanation p {
    line-height: 1.7;
  }

  .explanation-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2.5rem 0;
  }

  .explanation-card {
    background-color: rgba(30, 30, 50, 0.5);
    background-image: linear-gradient(to bottom, rgba(30, 30, 60, 0.5), rgba(20, 20, 40, 0.5));
    border: 1px solid rgba(124, 58, 237, 0.2);
    border-radius: 12px;
    padding: 1.75rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .explanation-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    border-color: rgba(124, 58, 237, 0.4);
  }

  .icon {
    font-size: 2.25rem;
    margin-bottom: 1.25rem;
    opacity: 0.9;
  }

  .explanation-card h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
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
    margin-bottom: 2.5rem;
    max-width: 900px;
  }

  .mission-list {
    list-style: none;
    padding: 0;
    margin: 1.75rem 0;
  }

  .mission-list li {
    margin-bottom: 1rem;
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
    margin-top: 3rem;
  }

  /* Need to Know Section */
  .need-to-know {
    background-color: #1a1a2e;
    background-image: linear-gradient(to bottom, #1a1a2e, #181830);
  }

  .key-insights {
    margin: 2.5rem 0;
  }

  .insight {
    background-color: rgba(30, 30, 50, 0.5);
    border-left: 3px solid #8b5cf6;
    padding: 1.75rem;
    border-radius: 0 12px 12px 0;
    margin-bottom: 1.75rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .insight:hover {
    transform: translateX(3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }

  .insight h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: #a78bfa;
  }

  .insight p {
    color: rgba(229, 231, 235, 0.85);
    line-height: 1.7;
  }

  @media (max-width: 768px) {
    .insight {
      padding: 1.5rem;
      border-left: none;
      border-top: 3px solid #8b5cf6;
      border-radius: 0 0 12px 12px;
    }

    .insight:hover {
      transform: translateY(-3px);
      transform: translateX(0);
    }
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
    gap: 1.5rem;
    margin: 2rem 0;
  }

  .support-card {
    background-color: rgba(30, 30, 50, 0.5);
    border-radius: 12px;
    padding: 1.5rem;
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
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }

  .support-card h3 {
    font-size: 1.4rem;
    margin-bottom: 0.75rem;
    color: #a78bfa;
  }

  .support-card p {
    margin-bottom: 1.25rem;
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
    margin-top: 3rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .newsletter-section h3 {
    text-align: center;
    margin-bottom: 1.5rem;
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
    padding-bottom: 3rem;
    background-color: #0f0f23;
  }

  .copyright {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
  }
</style>