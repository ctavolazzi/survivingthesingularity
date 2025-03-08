<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import bookCover from '$lib/images/Surviving-the-Singularity-Cover.png';
  import chessImage from '$lib/images/sts-chess.jpg';

  let showNextSteps = true;
  let activeSection = 0;
  let heroVisible = false;

  onMount(() => {
    // Add a small delay before showing hero elements
    setTimeout(() => {
      heroVisible = true;
    }, 300);
  });
</script>

<svelte:head>
  <title>Start Here | Surviving the Singularity</title>
  <meta name="description" content="Begin your journey to understanding and preparing for the technological singularity with this introduction to the key concepts and resources." />
</svelte:head>

<div class="start-here-page">
  <!-- Hero Section -->
  <header class="hero-section">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      {#if heroVisible}
        <div class="hero-badge" in:fly={{y: -20, duration: 600, delay: 100}}>Welcome</div>
        <h1 class="hero-title" in:fly={{y: 20, duration: 700, delay: 400}}>AI is already reshaping careers. Will yours survive the next 5 years?</h1>
        <p class="hero-description" in:fade={{duration: 600, delay: 700}}>
          Learn the critical skills and mindsets that will keep you relevant in the AI revolution. Our resources help you prepare for what's coming.
        </p>
        <div class="hero-scroll" in:fade={{duration: 500, delay: 1000}}>
          <a href="#singularity-intro" class="scroll-btn">
            <span>Get Started</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 13l5 5 5-5"/></svg>
          </a>
        </div>
      {/if}
    </div>
    <div class="hero-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="grid-pattern"></div>
    </div>
  </header>

  <!-- Social Proof Banner -->
  <div class="social-proof-banner">
    <div class="container">
      <div class="social-proof-content">
        {#if heroVisible}
          <p class="social-proof-text" in:fly={{y: 10, duration: 600, delay: 1200}}>
            Join our growing community of forward-thinkers preparing for the AI revolution. Connect with professionals from various tech industries and backgrounds.
          </p>
        {/if}
      </div>
    </div>
  </div>

  <!-- Section 1: Introduction to the Singularity -->
  <section id="singularity-intro" class="content-section singularity-intro">
    <div class="container">
      <h2>Understanding the Singularity</h2>
      <div class="section-content">
        <div class="text-content">
          <p class="lead">
            The technological singularity represents a point when artificial intelligence surpasses human intelligence, leading to unprecedented and potentially rapid technological advancement.
          </p>
          <div class="key-points">
            <div class="point">
              <span class="point-icon">🧠</span>
              <span class="point-text">AI systems developing capabilities that match or exceed human intelligence</span>
            </div>
            <div class="point">
              <span class="point-icon">⚙️</span>
              <span class="point-text">Self-improving AI leading to recursive technological development</span>
            </div>
            <div class="point">
              <span class="point-icon">📈</span>
              <span class="point-text">Acceleration of progress beyond what we can currently predict</span>
            </div>
          </div>
        </div>
        <div class="image-container">
          <img src={chessImage} alt="Strategic thinking about the singularity" class="section-image" />
        </div>
      </div>
    </div>
  </section>

  <!-- Section 2: Why Preparation Matters -->
  <section class="content-section preparation-section">
    <div class="container">
      <h2>Why Preparation Matters</h2>
      <div class="preparation-grid">
        <div class="prep-card">
          <div class="prep-icon">🔍</div>
          <h3>Awareness</h3>
          <p>Recognizing patterns and trajectories of technological advancement</p>
        </div>

        <div class="prep-card">
          <div class="prep-icon">🛠️</div>
          <h3>Adaptation</h3>
          <p>Developing skills that remain valuable in a rapidly changing world</p>
        </div>

        <div class="prep-card">
          <div class="prep-icon">🔄</div>
          <h3>Resilience</h3>
          <p>Building systems that can withstand and thrive amid disruption</p>
        </div>

        <div class="prep-card">
          <div class="prep-icon">🌱</div>
          <h3>Opportunity</h3>
          <p>Positioning yourself to benefit from emerging possibilities</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 3: Resource Guide -->
  <section class="content-section resources-section">
    <div class="container">
      <h2>Essential Resources</h2>
      <div class="resources-timeline">
        <div class="resource-item">
          <div class="resource-number">1</div>
          <div class="resource-content">
            <h3>Explore the Timeline</h3>
            <p>Understand the history and future trajectory of technological development</p>
            <a href="/" class="resource-link">View Timeline</a>
          </div>
        </div>

        <div class="resource-item">
          <div class="resource-number">2</div>
          <div class="resource-content">
            <h3>Read Latest Articles</h3>
            <p>Stay current with emerging technologies and their implications</p>
            <a href="/blog" class="resource-link">Visit Blog</a>
          </div>
        </div>

        <div class="resource-item">
          <div class="resource-number">3</div>
          <div class="resource-content">
            <h3>Get the Book</h3>
            <p>Dive deeper with our comprehensive guide to the singularity</p>
            <a href="/sample" class="resource-link">Read a Sample</a>
          </div>
        </div>

        <div class="resource-item">
          <div class="resource-number">4</div>
          <div class="resource-content">
            <h3>Join the Community</h3>
            <p>Connect with others navigating these changes</p>
            <div class="community-links">
              <a href="/newsletter" class="resource-link">Newsletter</a>
              <a href="/discord" class="resource-link">Discord</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Book Preview Section -->
  <section class="content-section book-section">
    <div class="container">
      <div class="book-preview">
        <div class="book-cover">
          <img src={bookCover} alt="Surviving the Singularity book cover" />
        </div>
        <div class="book-content">
          <h2>The Definitive Guide</h2>
          <p>
            "Surviving the Singularity" equips you with the mental models and actionable knowledge to navigate this period of unprecedented change.
          </p>
          <div class="book-cta">
            <a href="/sample" class="primary-button">Read a Sample</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Next Steps Section - No transition animation -->
  <section class="content-section next-steps-section">
    <div class="container">
      <h2>Your Next Steps</h2>
      <div class="next-steps-grid">
        <div class="next-step">
          <div class="step-number">1</div>
          <h3>Sign Up</h3>
          <p>Join our newsletter for regular insights</p>
          <div class="action-container">
            <NewsletterSignup />
          </div>
        </div>

        <div class="next-step">
          <div class="step-number">2</div>
          <h3>Connect</h3>
          <p>Join our community of forward-thinking individuals</p>
          <div class="action-container">
            <DiscordButton />
          </div>
        </div>

        <div class="next-step">
          <div class="step-number">3</div>
          <h3>Explore</h3>
          <p>Dive into our most important resources</p>
          <div class="action-container explore-links">
            <a href="/blog" class="secondary-button">Blog</a>
            <a href="/sample" class="secondary-button">Book Preview</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Enhanced Explore Content Section -->
  <section class="content-section explore-content-section">
    <div class="container">
      <div class="explore-header">
        <h2>Explore Our Content</h2>
        <p class="explore-subtitle">Dive deeper into our best resources with these previews</p>
      </div>

      <div class="explore-grid">
        <!-- Blog Post Preview Card -->
        <div class="explore-card blog-card">
          <div class="card-overlay"></div>
          <div class="card-badge">Latest Blog Post</div>
          <div class="card-content">
            <h3>DARPA Seeks Plans for 'Large Bio-Mechanical Space Structures'</h3>
            <p class="card-excerpt">
              DARPA has issued a request for information on building massive biological structures in space, exploring a sci-fi future where space infrastructure might be grown rather than assembled.
            </p>
            <div class="card-meta">
              <span class="card-date">March 4, 2024</span>
              <span class="card-author">Christopher Tavolazzi</span>
            </div>
            <a href="/blog/darpa-biomechanical-space-structures" class="explore-button">
              <span>Read Post</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
          </div>
        </div>

        <!-- Newsletter Preview Card -->
        <div class="explore-card newsletter-card">
          <div class="card-overlay"></div>
          <div class="card-badge">Latest Newsletter</div>
          <div class="card-content">
            <h3>Surviving the Singularity Newsletter</h3>
            <p class="card-excerpt">
              Welcome to the AI Revolution: Your guide to navigating the rapidly evolving world of artificial intelligence. Stay informed, prepared, and ahead of the curve.
            </p>
            <div class="newsletter-highlights">
              <div class="highlight-item">
                <span class="highlight-icon">🌟</span>
                <span class="highlight-text">This Week in AI</span>
              </div>
              <div class="highlight-item">
                <span class="highlight-icon">📊</span>
                <span class="highlight-text">Tech Trends</span>
              </div>
              <div class="highlight-item">
                <span class="highlight-icon">🧠</span>
                <span class="highlight-text">AI Insights</span>
              </div>
            </div>
            <a href="/newsletter" class="explore-button">
              <span>Subscribe</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
          </div>
        </div>

        <!-- Book Sample Preview Card -->
        <div class="explore-card book-card">
          <div class="card-overlay"></div>
          <div class="book-cover-preview">
            <img src={bookCover} alt="Surviving the Singularity book cover" />
          </div>
          <div class="card-badge">Book Preview</div>
          <div class="card-content">
            <h3>Surviving the Singularity</h3>
            <p class="card-quote">
              "The unfolding Singularity is a deeply personal process - the way you get your needs met is changing. You don't know what's about to happen; no one does."
            </p>
            <p class="card-excerpt">
              A primer on understanding and navigating the double exponential shift in the way we get our needs met in the age of AI.
            </p>
            <a href="/sample" class="explore-button">
              <span>Read Sample</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>

<style>
  /* Base Styles */
  .start-here-page {
    width: 100%;
    color: #e5e7eb;
    overflow: hidden;
  }

  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 1.25rem;
    position: relative;
    z-index: 2;
  }

  h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
    margin: 0 0 1rem 0;
  }

  h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-align: center;
    white-space: normal;
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: none;
    -webkit-hyphens: none;
    -ms-hyphens: none;
    width: 100%;
    line-height: 1.3;
  }

  h2 {
    font-size: clamp(1.5rem, 4vw, 2rem);
    color: #a78bfa;
    margin-bottom: 1.25rem;
    text-align: center;
    white-space: normal;
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: none;
    -webkit-hyphens: none;
    -ms-hyphens: none;
  }

  h3 {
    font-size: clamp(1.1rem, 3vw, 1.25rem);
    color: #a78bfa;
    margin-bottom: 0.5rem;
    white-space: normal;
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: none;
    -webkit-hyphens: none;
    -ms-hyphens: none;
  }

  p {
    margin: 0 0 0.75rem 0;
    line-height: 1.5;
  }

  .lead {
    font-size: clamp(1rem, 2.5vw, 1.15rem);
    font-weight: 500;
    margin-bottom: 1.25rem;
  }

  /* Content Section Standard Styles */
  .content-section {
    padding: 0;
    position: relative;
  }

  /* Hero Section */
  .hero-section {
    position: relative;
    min-height: 85vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem 3rem;
    overflow: hidden;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    margin-bottom: 0;
  }

  .hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(15, 23, 42, 0.6);
    z-index: 1;
  }

  .hero-content {
    position: relative;
    z-index: 3;
    text-align: center;
    max-width: 90%;
    width: 90%;
    padding: 1.5rem 1rem;
  }

  .hero-badge {
    display: inline-block;
    padding: 0.4rem 1rem;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    border-radius: 2rem;
    color: white;
    font-weight: bold;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
  }

  .hero-title {
    margin-bottom: 1rem;
    line-height: 1.3;
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    width: 100%;
    white-space: normal;
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: none;
    -webkit-hyphens: none;
    -ms-hyphens: none;
    max-width: 100%;
  }

  .hero-description {
    font-size: clamp(1rem, 2.5vw, 1.15rem);
    max-width: 500px;
    margin: 0 auto 1.5rem;
    color: #d1d5db;
  }

  .hero-scroll {
    margin-top: 2rem;
  }

  .scroll-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border-radius: 2rem;
    text-decoration: none;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
  }

  .scroll-btn::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 50%);
    opacity: 0;
    animation: ripple 2.5s infinite;
  }

  @keyframes ripple {
    0% {
      transform: scale(0.5);
      opacity: 0;
    }
    25% {
      opacity: 0.3;
    }
    100% {
      transform: scale(1);
      opacity: 0;
    }
  }

  .scroll-btn:hover {
    background-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .scroll-btn svg {
    animation: bounce 2s infinite;
  }

  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-5px);
    }
    60% {
      transform: translateY(-3px);
    }
  }

  .hero-decoration {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
  }

  .circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
  }

  .circle-1 {
    width: 300px;
    height: 300px;
    background: radial-gradient(#a78bfa, transparent);
    top: -100px;
    left: -100px;
    animation: float 10s ease-in-out infinite;
  }

  .circle-2 {
    width: 200px;
    height: 200px;
    background: radial-gradient(#6366f1, transparent);
    bottom: -50px;
    right: 20px;
    animation: float 7s ease-in-out infinite;
  }

  .grid-pattern {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      linear-gradient(rgba(99, 102, 241, 0.1) 1px, transparent 1px),
      linear-gradient(90deg, rgba(99, 102, 241, 0.1) 1px, transparent 1px);
    background-size: 20px 20px;
    z-index: 0;
  }

  @keyframes float {
    0%, 100% {
      transform: translateY(0) translateX(0);
    }
    50% {
      transform: translateY(-15px) translateX(5px);
    }
  }

  /* Social Proof Banner */
  .social-proof-banner {
    background: linear-gradient(90deg, rgba(79, 70, 229, 0.2) 0%, rgba(137, 66, 255, 0.2) 100%);
    border-top: 1px solid rgba(99, 102, 241, 0.3);
    border-bottom: 1px solid rgba(99, 102, 241, 0.3);
    padding: 0.75rem 0;
    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 5;
  }

  .social-proof-banner .container {
    padding: 0.5rem 1.25rem;
  }

  .social-proof-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }

  .social-proof-text {
    font-size: 0.95rem;
    font-weight: 500;
    text-align: center;
    color: #e5e7eb;
    margin: 0;
    line-height: 1.5;
  }

  .highlight {
    font-weight: 700;
    color: #a78bfa;
  }

  .company-badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    background: rgba(99, 102, 241, 0.2);
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.9rem;
    color: #a78bfa;
    margin: 0 0.15rem;
    border: 1px solid rgba(99, 102, 241, 0.4);
  }

  @media (min-width: 768px) {
    .social-proof-text {
      font-size: 1.05rem;
    }
  }

  /* Singularity Introduction Section */
  .singularity-intro {
    background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    position: relative;
    padding: 1rem 0;
  }

  .section-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .text-content {
    flex: 1;
  }

  .image-container {
    flex: 1;
    text-align: center;
  }

  .section-image {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
  }

  .key-points {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1rem;
  }

  .point {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .point-icon {
    font-size: 1.5rem;
  }

  .point-text {
    font-size: 0.95rem;
    line-height: 1.4;
  }

  /* Preparation Section */
  .preparation-section {
    background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
    position: relative;
  }

  .preparation-grid {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .prep-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.25rem;
    border-radius: 8px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .prep-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  }

  .prep-icon {
    font-size: 1.75rem;
    margin-bottom: 0.75rem;
  }

  /* Resources Section */
  .resources-section {
    background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    position: relative;
  }

  .resources-timeline {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }

  .resource-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  .resource-number {
    flex-shrink: 0;
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    border-radius: 50%;
    font-size: 1.25rem;
    font-weight: bold;
    color: white;
    box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
  }

  .resource-content {
    flex: 1;
  }

  .resource-link, .primary-button, .secondary-button {
    display: inline-block;
    padding: 0.5rem 1rem;
    font-weight: 500;
    text-decoration: none;
    border-radius: 4px;
    transition: all 0.3s ease;
    margin-top: 0.5rem;
    margin-right: 0.5rem;
  }

  .resource-link {
    background: rgba(99, 102, 241, 0.1);
    color: #a78bfa;
    border: 1px solid #4f46e5;
  }

  .resource-link:hover {
    background: rgba(99, 102, 241, 0.2);
    transform: translateY(-2px);
  }

  .community-links {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 0.5rem;
  }

  /* Book Section */
  .book-section {
    background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
    position: relative;
  }

  .book-preview {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    align-items: center;
  }

  .book-cover {
    flex-shrink: 0;
    max-width: 180px;
  }

  .book-cover img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  }

  .book-content {
    flex: 1;
    text-align: center;
  }

  .book-cta {
    margin-top: 1rem;
  }

  .primary-button {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: white;
    box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
    padding: 0.6rem 1.25rem;
    border-radius: 30px;
    position: relative;
  }

  .primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 10px -1px rgba(99, 102, 241, 0.4);
  }

  /* Add pulsing glow effect to primary buttons */
  .primary-button::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 30px;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    z-index: -1;
    opacity: 0.5;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
      opacity: 0.5;
    }
    50% {
      transform: scale(1.05);
      opacity: 0.2;
    }
    100% {
      transform: scale(1);
      opacity: 0.5;
    }
  }

  /* Next Steps Section */
  .next-steps-section {
    background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
    position: relative;
    padding-bottom: 4rem;
  }

  .next-steps-grid {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 2rem;
    margin-top: 1.5rem;
  }

  .next-step {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.75rem 1.5rem 1.75rem;
    border-radius: 8px;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .next-step:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  }

  .step-number {
    position: absolute;
    top: -15px;
    left: -15px;
    width: 35px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    border-radius: 50%;
    font-size: 1.1rem;
    font-weight: bold;
    color: white;
    box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
  }

  .secondary-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    background: rgba(99, 102, 241, 0.1);
    color: #a78bfa;
    border: 1px solid #4f46e5;
    border-radius: 30px;
    text-decoration: none;
    transition: all 0.3s ease;
    min-width: 120px;
    height: 40px;
  }

  .secondary-button:hover {
    background: rgba(99, 102, 241, 0.2);
    transform: translateY(-2px);
  }

  .explore-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 1rem;
  }

  .action-container {
    margin-top: auto;
    padding-top: 1.5rem;
  }

  /* Adjust DiscordButton styling within this section */
  :global(.next-step .discord-button) {
    width: 100%;
    max-width: 100%;
    padding: 0.6rem 0.75rem;
    justify-content: center;
    height: 40px;
  }

  /* Adjust newsletter form styling within this section */
  :global(.next-step .newsletter-form) {
    margin: 0;
    width: 100%;
  }

  :global(.next-step .newsletter-input) {
    font-size: 0.95rem;
    padding: 0.5rem 0.75rem;
    height: 40px;
  }

  :global(.next-step .newsletter-submit) {
    font-size: 0.95rem;
    padding: 0.5rem 0.75rem;
    height: 40px;
  }

  @media (min-width: 768px) {
    .container {
      padding: 4rem 2.5rem;
    }

    .section-content {
      flex-direction: row;
      align-items: center;
      gap: 2.5rem;
    }

    .hero-content {
      padding: 2.5rem;
    }

    .book-preview {
      flex-direction: row;
      text-align: left;
      gap: 2.5rem;
    }

    .book-content {
      text-align: left;
    }

    .resource-item {
      gap: 1.5rem;
    }
  }

  /* Specific Mobile Optimizations */
  @media (max-width: 639px) {
    .container {
      padding-left: 1rem;
      padding-right: 1rem;
    }

    .hero-section {
      min-height: 80vh;
    }

    .hero-content {
      padding: 1rem 0.5rem;
      width: 100%;
      max-width: 100%;
    }

    h1, .hero-title {
      font-size: clamp(1.8rem, 4vw, 2.5rem);
      line-height: 1.3;
    }

    h2 {
      font-size: clamp(1.5rem, 3vw, 1.8rem);
    }

    h3 {
      font-size: clamp(1.1rem, 2.5vw, 1.2rem);
    }

    .book-cover {
      max-width: 150px;
    }

    .resource-item p {
      margin-bottom: 0.5rem;
    }
  }

  /* Responsive Design - Mobile First, then medium screens, then large screens */
  @media (min-width: 640px) {
    .container {
      padding: 3.5rem 2rem;
    }

    .hero-section {
      padding: 2rem 2rem 4rem;
    }

    .hero-content {
      padding: 2rem;
    }

    .point {
      padding: 0.75rem 1rem;
    }

    .preparation-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 1.25rem;
    }
  }

  @media (min-width: 1024px) {
    .preparation-grid {
      grid-template-columns: repeat(4, 1fr);
    }

    .container {
      padding: 5rem 3rem;
    }
  }

  /* Accessibility - Respect user preferences for reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .scroll-btn svg,
    .circle-1,
    .circle-2,
    .primary-button::after,
    .scroll-btn::after {
      animation: none !important;
    }

    .scroll-btn:hover,
    .primary-button:hover,
    .resource-link:hover,
    .secondary-button:hover,
    .prep-card:hover,
    .next-step:hover {
      transform: none !important;
    }
  }

  /* Enhanced Explore Content Section */
  .explore-content-section {
    background: linear-gradient(135deg, #0c0e17 0%, #1a1d33 100%);
    position: relative;
    padding: 4rem 0;
    overflow: hidden;
  }

  .explore-content-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
      radial-gradient(circle at 80% 70%, rgba(124, 58, 237, 0.1) 0%, transparent 50%);
    z-index: 1;
  }

  .explore-header {
    text-align: center;
    position: relative;
    z-index: 2;
    margin-bottom: 3rem;
  }

  .explore-subtitle {
    font-size: 1.1rem;
    color: #a78bfa;
    margin-top: 0.5rem;
    opacity: 0.8;
  }

  .explore-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2.5rem;
    position: relative;
    z-index: 2;
  }

  .explore-card {
    background: rgba(20, 24, 42, 0.5);
    border-radius: 12px;
    overflow: hidden;
    position: relative;
    backdrop-filter: blur(10px);
    box-shadow:
      0 20px 25px -5px rgba(0, 0, 0, 0.5),
      0 10px 10px -5px rgba(0, 0, 0, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.1);
    transform: translateY(0);
    transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .explore-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow:
      0 25px 50px -12px rgba(0, 0, 0, 0.6),
      0 0 0 1px rgba(255, 255, 255, 0.15),
      0 0 20px 5px rgba(167, 139, 250, 0.2);
  }

  .explore-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167, 139, 250, 0.5), transparent);
  }

  .card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
  }

  .blog-card .card-overlay {
    background:
      linear-gradient(to bottom, rgba(20, 24, 42, 0) 0%, rgba(20, 24, 42, 0.8) 60%, rgba(20, 24, 42, 0.95) 100%),
      url("/lib/images/sts-chess.jpg") no-repeat center top;
    background-size: cover;
    opacity: 0.8;
  }

  .newsletter-card .card-overlay {
    background:
      linear-gradient(to bottom, rgba(20, 24, 42, 0) 0%, rgba(20, 24, 42, 0.8) 60%, rgba(20, 24, 42, 0.95) 100%),
      url('/lib/images/sts-welcome.png') no-repeat center;
    background-size: cover;
    opacity: 0.6;
  }

  .book-card .card-overlay {
    background:
      linear-gradient(to bottom, rgba(20, 24, 42, 0) 0%, rgba(20, 24, 42, 0.7) 50%, rgba(20, 24, 42, 0.95) 100%),
      linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(79, 70, 229, 0.1) 100%);
  }

  .card-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    padding: 0.4rem 1rem;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 600;
    color: white;
    z-index: 2;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
  }

  .card-content {
    position: relative;
    z-index: 1;
    padding: 2rem;
    min-height: 280px;
    display: flex;
    flex-direction: column;
    padding-top: 8rem;
  }

  .explore-card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    line-height: 1.3;
    color: white;
    white-space: normal;
  }

  .card-excerpt {
    font-size: 1rem;
    line-height: 1.6;
    color: #d1d5db;
    margin-bottom: 1.5rem;
  }

  .card-meta {
    display: flex;
    font-size: 0.85rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
    gap: 1rem;
  }

  .card-date::before {
    content: '📅';
    margin-right: 0.5rem;
  }

  .card-author::before {
    content: '✍️';
    margin-right: 0.5rem;
  }

  .card-quote {
    font-style: italic;
    font-size: 1.1rem;
    line-height: 1.6;
    color: #a78bfa;
    margin-bottom: 1rem;
    padding-left: 1rem;
    border-left: 3px solid #6366f1;
  }

  .explore-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.5rem;
    background: rgba(99, 102, 241, 0.2);
    color: #a78bfa;
    border: 1px solid #4f46e5;
    border-radius: 30px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    margin-top: auto;
    width: fit-content;
    position: relative;
    overflow: hidden;
  }

  .explore-button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent);
    transition: all 0.8s ease;
  }

  .explore-button:hover {
    background: rgba(99, 102, 241, 0.3);
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.5);
  }

  .explore-button:hover::after {
    left: 100%;
  }

  .newsletter-highlights {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .highlight-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    font-size: 0.9rem;
  }

  .highlight-icon {
    font-size: 1.1rem;
  }

  .book-cover-preview {
    position: absolute;
    top: 2rem;
    right: 2rem;
    width: 90px;
    height: 120px;
    z-index: 2;
    transform: rotate(8deg);
    transition: all 0.5s ease;
    box-shadow:
      0 15px 25px rgba(0, 0, 0, 0.5),
      0 5px 10px rgba(0, 0, 0, 0.3);
  }

  .book-cover-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
  }

  .book-card:hover .book-cover-preview {
    transform: rotate(0deg) scale(1.1);
  }

  /* Add glowing effect to the cards */
  @keyframes glow {
    0%, 100% {
      box-shadow:
        0 20px 25px -5px rgba(0, 0, 0, 0.5),
        0 10px 10px -5px rgba(0, 0, 0, 0.2),
        0 0 0 1px rgba(255, 255, 255, 0.1);
    }
    50% {
      box-shadow:
        0 20px 25px -5px rgba(0, 0, 0, 0.5),
        0 10px 10px -5px rgba(0, 0, 0, 0.2),
        0 0 0 1px rgba(255, 255, 255, 0.1),
        0 0 15px 2px rgba(167, 139, 250, 0.4);
    }
  }

  .explore-card {
    animation: glow 4s infinite alternate;
  }

  .blog-card {
    animation-delay: 0s;
  }

  .newsletter-card {
    animation-delay: 1s;
  }

  .book-card {
    animation-delay: 2s;
  }

  @media (min-width: 768px) {
    .explore-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .book-card {
      grid-column: span 2;
    }

    .card-content {
      min-height: 350px;
    }
  }

  @media (min-width: 1024px) {
    .explore-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .book-card {
      grid-column: auto;
    }
  }

  /* Adjust hero content specifically for different screen sizes */
  @media (max-width: 768px) {
    .hero-title {
      font-size: clamp(1.7rem, 3.5vw, 2.3rem);
      hyphens: none;
      -webkit-hyphens: none;
      -ms-hyphens: none;
      word-break: normal;
    }

    .hero-content {
      padding: 1rem;
      width: 100%;
      max-width: 100%;
    }
  }

  @media (max-width: 480px) {
    .hero-title {
      font-size: 1.6rem;
      line-height: 1.4;
      hyphens: none;
      -webkit-hyphens: none;
      -ms-hyphens: none;
      word-break: normal;
    }
  }
</style>