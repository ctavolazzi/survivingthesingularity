<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import TreasureTavernAd from '$lib/components/ads/TreasureTavernAd.svelte';
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

    // Add smooth scrolling for the explore step link
    const scrollToExploreLinks = document.querySelectorAll('.scroll-to-explore');
    scrollToExploreLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop - 50,
            behavior: 'smooth'
          });
        }
      });
    });
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

        <div class="next-step explore-step" id="explore-step">
          <div class="step-number step-number-explore">3</div>
          <h3 class="explore-step-title">Explore</h3>
          <p>Dive into our resource library</p>
          <div class="action-container explore-links">
            <a href="#resource-library" class="secondary-button explore-btn scroll-to-explore">
              <span class="btn-text">View Resources</span>
              <span class="btn-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
              </span>
              <span class="btn-glow"></span>
            </a>
          </div>
          <div class="explore-decoration">
            <div class="explore-glow-circle"></div>
            <div class="explore-particles">
              <span class="particle"></span>
              <span class="particle"></span>
              <span class="particle"></span>
              <span class="particle"></span>
              <span class="particle"></span>
            </div>
            <div class="connection-line"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Resource Showcase Section -->
  <section class="content-section resource-showcase-section" id="resource-library">
    <div class="container">
      <div class="section-header">
        <div class="section-connector">
          <div class="connector-line"></div>
        </div>
        <h2 class="section-title">Resource Library</h2>
        <p class="section-subtitle">Essential content to help you navigate the AI revolution</p>
      </div>

      <div class="resource-grid">
        <!-- Blog Post Preview Card -->
        <div class="resource-card blog-card">
          <div class="card-inner">
            <div class="card-overlay"></div>
            <div class="card-badge">Featured Blog Post</div>
            <div class="card-content">
              <h3>DARPA Seeks Plans for 'Large Bio-Mechanical Space Structures'</h3>
              <p class="card-excerpt">
                DARPA has issued a request for information on building massive biological structures in space, exploring a sci-fi future where space infrastructure might be grown rather than assembled.
              </p>
              <div class="card-meta">
                <span class="card-date">March 4, 2024</span>
                <span class="card-author">Christopher Tavolazzi</span>
              </div>
              <a href="/blog/darpa-biomechanical-space-structures" class="resource-button">
                <span>Read Post</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                <span class="button-glow"></span>
              </a>
            </div>
          </div>
        </div>

        <!-- Newsletter Preview Card -->
        <div class="resource-card newsletter-card">
          <div class="card-inner">
            <div class="card-overlay"></div>
            <div class="card-badge">Newsletter Insights</div>
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
              <a href="/newsletter" class="resource-button">
                <span>Subscribe</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                <span class="button-glow"></span>
              </a>
            </div>
          </div>
        </div>

        <!-- Book Sample Preview Card -->
        <div class="resource-card book-card">
          <div class="card-inner">
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
              <a href="/sample" class="resource-button">
                <span>Read Sample</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                <span class="button-glow"></span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="resource-cta">
        <a href="/blog" class="primary-button resource-primary-button">
          <span>View All Blog Posts</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
        <a href="/sample" class="primary-button resource-primary-button">
          <span>Full Book Preview</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      </div>
    </div>
    <div class="resource-decoration">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
      <div class="floating-lines"></div>
    </div>
  </section>

  <!-- Treasure Tavern Ad Section -->
  <section class="content-section treasure-tavern-section">
    <div class="container">
      <TreasureTavernAd />
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
    background: linear-gradient(180deg, #111827 0%, #0c0e17 100%);
    position: relative;
    padding-bottom: 4rem;
    position: relative;
    z-index: 3;
    overflow: visible;
  }

  .next-steps-section::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100px;
    background: linear-gradient(to bottom, #0c0e17, transparent);
    z-index: 1;
    opacity: 0.7;
  }

  .next-steps-grid {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 2rem;
    margin-top: 1.5rem;
    position: relative;
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
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    border-radius: 50%;
    font-size: 1.2rem;
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

  /* Resource Showcase Section */
  .resource-showcase-section {
    background: linear-gradient(135deg, #0c0e17 0%, #1a1d33 100%);
    position: relative;
    padding: 6rem 0;
    padding-top: 4rem;
    overflow: hidden;
    margin: 0;
    margin-top: 0;
    perspective: 1000px;
    z-index: 4;
  }

  .section-connector {
    position: absolute;
    top: -30px;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    height: 30px;
    overflow: visible;
    z-index: 6;
  }

  .connector-line {
    width: 3px;
    height: 30px;
    background: linear-gradient(to top, rgba(167, 139, 250, 0), rgba(167, 139, 250, 0.9));
    box-shadow: 0 0 15px rgba(167, 139, 250, 0.3);
    animation: pulse-line-top 3s infinite alternate;
  }

  @keyframes pulse-line-top {
    0%, 100% {
      opacity: 0.7;
      height: 30px;
    }
    50% {
      opacity: 1;
      height: 40px;
    }
  }

  .section-header {
    text-align: center;
    position: relative;
    z-index: 10;
    margin-bottom: 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 1rem;
  }

  .section-title {
    font-size: clamp(2.5rem, 6vw, 3.5rem);
    background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: 2px;
    position: relative;
    text-shadow: 0 0 15px rgba(167, 139, 250, 0.4);
    text-transform: none;
    animation: title-glow 3s infinite alternate;
  }

  @keyframes title-glow {
    0%, 100% {
      text-shadow: 0 0 15px rgba(167, 139, 250, 0.4);
    }
    50% {
      text-shadow: 0 0 25px rgba(167, 139, 250, 0.6);
    }
  }

  .section-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 2px;
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.1), rgba(167, 139, 250, 0.8), rgba(99, 102, 241, 0.1));
    border-radius: 2px;
  }

  /* Section transitions */
  .resource-showcase-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.25) 0%, transparent 50%),
      radial-gradient(circle at 80% 70%, rgba(124, 58, 237, 0.2) 0%, transparent 50%);
    z-index: 1;
  }

  /* Responsive adjustments */
  @media (min-width: 768px) {
    /* Add scrolling indicator animation */
    .scroll-to-explore .btn-icon {
      animation: pulse-down 2s ease-in-out infinite;
      opacity: 1;
      transform: rotate(90deg) translateY(0);
    }

    .explore-step {
      transform: scale(1.05);
      box-shadow:
        0 10px 25px -5px rgba(0, 0, 0, 0.3),
        0 0 20px rgba(167, 139, 250, 0.25);
    }

    .explore-step:hover {
      transform: translateY(-5px) scale(1.05);
      box-shadow:
        0 20px 35px -5px rgba(0, 0, 0, 0.4),
        0 0 25px rgba(167, 139, 250, 0.35);
    }
  }

  @keyframes pulse-down {
    0%, 100% {
      transform: rotate(90deg) translateY(0);
    }
    50% {
      transform: rotate(90deg) translateY(5px);
    }
  }

  @keyframes pulse-glow {
    0%, 100% {
      box-shadow:
        0 0 10px rgba(99, 102, 241, 0.5),
        0 0 20px rgba(167, 139, 250, 0.3);
    }
    50% {
      box-shadow:
        0 0 20px rgba(99, 102, 241, 0.7),
        0 0 30px rgba(167, 139, 250, 0.5);
    }
  }

  @keyframes rotate-border {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  @keyframes pulse-button {
    0%, 100% {
      opacity: 0.6;
      transform: scale(1);
    }
    50% {
      opacity: 0.8;
      transform: scale(1.1);
    }
  }

  .resource-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 3rem;
    position: relative;
    z-index: 5;
  }

  .resource-card {
    position: relative;
    transform-style: preserve-3d;
    transform: translateZ(0px) rotateX(0deg) rotateY(0deg);
    transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    animation: fade-in-up 0.8s ease-out forwards;
    opacity: 0;
  }

  .resource-card:nth-child(1) {
    animation-delay: 0.1s;
  }

  .resource-card:nth-child(2) {
    animation-delay: 0.3s;
  }

  .resource-card:nth-child(3) {
    animation-delay: 0.5s;
  }

  .card-inner {
    background: rgba(20, 24, 42, 0.5);
    border-radius: 16px;
    overflow: hidden;
    position: relative;
    backdrop-filter: blur(10px);
    box-shadow:
      0 20px 25px -5px rgba(0, 0, 0, 0.5),
      0 10px 10px -5px rgba(0, 0, 0, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.1);
    transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
    height: 100%;
    z-index: 1;
  }

  .resource-card:hover {
    transform: translateZ(10px) rotateX(2deg) rotateY(-2deg);
  }

  .resource-card:hover .card-inner {
    box-shadow:
      0 25px 50px -12px rgba(0, 0, 0, 0.6),
      0 0 0 1px rgba(255, 255, 255, 0.15),
      0 0 20px 5px rgba(167, 139, 250, 0.2),
      0 0 40px rgba(99, 102, 241, 0.2);
  }

  .card-inner::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg,
      rgba(167, 139, 250, 0.5),
      rgba(99, 102, 241, 0.2),
      rgba(167, 139, 250, 0),
      rgba(99, 102, 241, 0.3));
    border-radius: 16px;
    z-index: -1;
    animation: border-flow 6s linear infinite;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .resource-card:hover .card-inner::before {
    opacity: 1;
  }

  .card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    transition: all 0.5s ease;
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

  .resource-card:hover .card-overlay {
    transform: scale(1.05);
    opacity: 1;
  }

  .card-badge {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    padding: 0.5rem 1.25rem;
    border-radius: 30px;
    font-size: 0.9rem;
    font-weight: 600;
    color: white;
    z-index: 2;
    box-shadow:
      0 4px 6px -1px rgba(0, 0, 0, 0.3),
      0 0 10px rgba(124, 58, 237, 0.5);
    transform: translateY(0);
    transition: all 0.3s ease;
  }

  .resource-card:hover .card-badge {
    transform: translateY(-5px);
    box-shadow:
      0 6px 10px -1px rgba(0, 0, 0, 0.4),
      0 0 15px rgba(124, 58, 237, 0.6);
  }

  .card-content {
    position: relative;
    z-index: 1;
    padding: 2.5rem;
    min-height: 350px;
  }

  .resource-card h3 {
    font-size: 1.75rem;
    margin-bottom: 1.25rem;
    line-height: 1.3;
    color: white;
    white-space: normal;
    transition: all 0.3s ease;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .resource-card:hover h3 {
    color: #a78bfa;
    text-shadow: 0 0 8px rgba(167, 139, 250, 0.3);
  }

  .card-excerpt {
    font-size: 1.05rem;
    line-height: 1.6;
    color: #d1d5db;
    margin-bottom: 1.5rem;
  }

  .card-meta {
    display: flex;
    font-size: 0.9rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
    gap: 1.25rem;
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
    font-size: 1.15rem;
    line-height: 1.6;
    color: #a78bfa;
    margin-bottom: 1.25rem;
    padding-left: 1.25rem;
    border-left: 3px solid #6366f1;
    position: relative;
  }

  .card-quote::before, .card-quote::after {
    font-family: 'Georgia', serif;
    position: absolute;
    font-size: 1.75rem;
    line-height: 1;
    color: rgba(167, 139, 250, 0.4);
  }

  .card-quote::before {
    content: '"';
    left: -5px;
    top: -5px;
  }

  .card-quote::after {
    content: '"';
    right: 0;
    bottom: -15px;
  }

  .resource-button {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.8rem 1.75rem;
    background: rgba(99, 102, 241, 0.2);
    color: #a78bfa;
    border: 1px solid #4f46e5;
    border-radius: 30px;
    font-weight: 600;
    font-size: 1.05rem;
    text-decoration: none;
    transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    margin-top: auto;
    width: fit-content;
    position: relative;
    overflow: hidden;
    z-index: 1;
  }

  .button-glow {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at center, rgba(167, 139, 250, 0.4) 0%, transparent 70%);
    opacity: 0;
    z-index: -1;
    transition: opacity 0.4s ease;
  }

  .resource-button:hover {
    background: rgba(99, 102, 241, 0.3);
    transform: translateY(-3px);
    box-shadow:
      0 6px 15px rgba(99, 102, 241, 0.4),
      0 0 20px rgba(167, 139, 250, 0.2);
    color: white;
  }

  .resource-button:hover .button-glow {
    opacity: 1;
    animation: pulse-button 1.5s infinite;
  }

  .resource-button:hover svg {
    transform: translateX(5px);
  }

  .newsletter-highlights {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.75rem;
  }

  .highlight-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 0.9rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    font-size: 0.95rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
  }

  .resource-card:hover .highlight-item {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-2px);
  }

  .highlight-icon {
    font-size: 1.2rem;
  }

  .book-cover-preview {
    position: absolute;
    top: 2.5rem;
    right: 2.5rem;
    width: 100px;
    height: 130px;
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
    transform: rotate(0deg) scale(1.15) translateY(-5px);
    box-shadow:
      0 20px 30px rgba(0, 0, 0, 0.6),
      0 10px 15px rgba(0, 0, 0, 0.4),
      0 0 20px rgba(167, 139, 250, 0.3);
  }

  /* Floating elements for main resource section */
  .floating-shape {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle at center, rgba(167, 139, 250, 0.3) 0%, transparent 70%);
    filter: blur(20px);
  }

  .shape-1 {
    width: 300px;
    height: 300px;
    top: -100px;
    left: 10%;
    animation: float-shape 15s ease-in-out infinite;
  }

  .shape-2 {
    width: 200px;
    height: 200px;
    bottom: 10%;
    right: 15%;
    animation: float-shape 12s ease-in-out infinite reverse;
  }

  .shape-3 {
    width: 150px;
    height: 150px;
    top: 30%;
    left: 5%;
    animation: float-shape 10s ease-in-out infinite 2s;
  }

  .floating-lines {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      linear-gradient(90deg, rgba(99, 102, 241, 0.05) 1px, transparent 1px),
      linear-gradient(rgba(99, 102, 241, 0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    animation: move-grid 10s linear infinite;
  }

  /* CTA Buttons */
  .resource-cta {
    margin-top: 4rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    position: relative;
    z-index: 10;
  }

  .resource-primary-button {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    min-width: 200px;
    justify-content: center;
    position: relative;
  }

  .resource-primary-button svg {
    transition: transform 0.3s ease;
  }

  .resource-primary-button:hover svg {
    transform: translateX(5px);
  }

  /* Enhanced Explore Step within Next Steps */
  .explore-step {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.7));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(99, 102, 241, 0.2);
    position: relative;
    overflow: hidden;
    z-index: 5;
    transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .explore-step::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      radial-gradient(circle at 30% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
      radial-gradient(circle at 70% 80%, rgba(167, 139, 250, 0.1) 0%, transparent 50%);
    z-index: -1;
  }

  .step-number-explore {
    width: 50px;
    height: 50px;
    font-size: 1.4rem;
    background: linear-gradient(135deg, #6366f1, #a78bfa);
    box-shadow:
      0 0 10px rgba(99, 102, 241, 0.5),
      0 0 20px rgba(167, 139, 250, 0.3);
    animation: pulse-glow 3s infinite alternate;
    position: relative;
    z-index: 2;
  }

  .step-number-explore::after {
    content: '';
    position: absolute;
    top: -5px;
    left: -5px;
    right: -5px;
    bottom: -5px;
    border-radius: 50%;
    border: 2px solid rgba(167, 139, 250, 0.3);
    animation: rotate-border 10s linear infinite;
  }

  .explore-step-title {
    font-size: 1.75rem;
    color: transparent;
    background: linear-gradient(135deg, #a78bfa, #6366f1);
    -webkit-background-clip: text;
    background-clip: text;
    text-shadow: 0 0 10px rgba(167, 139, 250, 0.3);
    position: relative;
  }

  .explore-btn {
    position: relative;
    overflow: hidden;
    padding: 0.65rem 1.5rem;
    transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .btn-text {
    position: relative;
    z-index: 2;
    transition: all 0.3s ease;
  }

  .explore-btn:hover {
    background: rgba(99, 102, 241, 0.25);
    transform: translateY(-3px);
    box-shadow:
      0 6px 15px rgba(99, 102, 241, 0.3),
      0 0 20px rgba(167, 139, 250, 0.2);
    color: white;
  }

  .explore-btn:hover .btn-glow {
    opacity: 1;
    animation: pulse-button 1.5s infinite;
  }

  .explore-btn:hover .btn-text {
    transform: translateX(0);
  }

  .explore-glow-circle {
    position: absolute;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: radial-gradient(circle at center, rgba(167, 139, 250, 0.1) 0%, transparent 70%);
    bottom: -80px;
    right: -50px;
    filter: blur(20px);
    animation: float-circle 8s ease-in-out infinite;
  }

  .explore-particles {
    position: absolute;
    width: 100%;
    height: 100%;
  }

  .particle {
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: rgba(167, 139, 250, 0.5);
    box-shadow: 0 0 10px rgba(167, 139, 250, 0.3);
    animation: float-particle 10s ease-in-out infinite;
  }

  .particle:nth-child(1) {
    top: 20%;
    left: 10%;
    width: 4px;
    height: 4px;
    animation-duration: 12s;
    animation-delay: 0s;
  }

  .particle:nth-child(2) {
    top: 50%;
    right: 15%;
    width: 5px;
    height: 5px;
    animation-duration: 15s;
    animation-delay: 1s;
  }

  .particle:nth-child(3) {
    bottom: 30%;
    left: 20%;
    width: 3px;
    height: 3px;
    animation-duration: 10s;
    animation-delay: 2s;
  }

  .particle:nth-child(4) {
    top: 35%;
    right: 25%;
    width: 4px;
    height: 4px;
    animation-duration: 14s;
    animation-delay: 3s;
  }

  .particle:nth-child(5) {
    bottom: 10%;
    left: 40%;
    width: 5px;
    height: 5px;
    animation-duration: 13s;
    animation-delay: 4s;
  }

  /* Accessibility and responsive styles */
  @media (prefers-reduced-motion: reduce) {
    .step-number-explore,
    .step-number-explore::after,
    .explore-btn .btn-glow,
    .button-glow,
    .explore-glow-circle,
    .particle,
    .floating-shape,
    .floating-lines,
    .card-inner::before,
    .resource-card {
      animation: none !important;
    }
  }

  /* Responsive adjustments */
  @media (min-width: 768px) {
    .resource-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .book-card {
      grid-column: span 2;
    }

    .explore-step {
      transform: scale(1.05);
      box-shadow:
        0 10px 25px -5px rgba(0, 0, 0, 0.3),
        0 0 15px rgba(167, 139, 250, 0.2);
    }

    .explore-step:hover {
      transform: translateY(-5px) scale(1.05);
      box-shadow:
        0 15px 35px -5px rgba(0, 0, 0, 0.4),
        0 0 20px rgba(167, 139, 250, 0.3);
    }

    /* Add scrolling indicator animation */
    .scroll-to-explore .btn-icon {
      animation: pulse-down 2s ease-in-out infinite;
      opacity: 1;
      transform: rotate(90deg) translateY(0);
    }
  }

  @media (min-width: 1024px) {
    .resource-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .book-card {
      grid-column: auto;
    }

    .resource-card:nth-child(1) {
      transform: perspective(1000px) rotateY(2deg);
    }

    .resource-card:nth-child(2) {
      transform: perspective(1000px) rotateY(0deg);
    }

    .resource-card:nth-child(3) {
      transform: perspective(1000px) rotateY(-2deg);
    }

    .resource-card:hover {
      transform: perspective(1000px) rotateY(0deg) translateZ(30px);
    }
  }

  @media (max-width: 767px) {
    .section-title {
      font-size: 2.2rem;
    }

    .card-content {
      padding: 2rem;
      padding-top: 8rem;
      min-height: 300px;
    }

    .resource-card h3 {
      font-size: 1.5rem;
    }
  }

  /* Create visual connection between sections */
  .connection-line {
    position: absolute;
    bottom: -80px;
    left: 50%;
    width: 3px;
    height: 80px;
    background: linear-gradient(to bottom, rgba(167, 139, 250, 0.9), rgba(167, 139, 250, 0));
    z-index: 6;
    animation: pulse-line 3s infinite alternate;
    box-shadow: 0 0 10px rgba(167, 139, 250, 0.3);
    margin-left: -1.5px;
  }

  @keyframes pulse-line {
    0%, 100% {
      opacity: 0.7;
      height: 80px;
    }
    50% {
      opacity: 1;
      height: 100px;
    }
  }

  .connector-line {
    animation: pulse-line-top 3s infinite alternate;
  }

  @keyframes pulse-line-top {
    0%, 100% {
      opacity: 0.7;
      height: 60px;
    }
    50% {
      opacity: 1;
      height: 70px;
    }
  }

  @keyframes pulse-button {
    0%, 100% {
      opacity: 0.6;
      transform: scale(1);
    }
    50% {
      opacity: 0.8;
      transform: scale(1.1);
    }
  }

  @keyframes float-circle {
    0%, 100% {
      transform: translateY(0) translateX(0);
    }
    50% {
      transform: translateY(-10px) translateX(5px);
    }
  }

  @keyframes float-particle {
    0%, 100% {
      transform: translateY(0) translateX(0);
    }
    25% {
      transform: translateY(-10px) translateX(5px);
    }
    50% {
      transform: translateY(5px) translateX(10px);
    }
    75% {
      transform: translateY(10px) translateX(-5px);
    }
  }

  @keyframes float-shape {
    0%, 100% {
      transform: translateY(0) translateX(0);
    }
    50% {
      transform: translateY(-20px) translateX(10px);
    }
  }

  @keyframes move-grid {
    0% {
      background-position: 0 0;
    }
    100% {
      background-position: 40px 40px;
    }
  }

  @keyframes border-flow {
    0% {
      background-position: 0% 0%;
    }
    100% {
      background-position: 300% 0%;
    }
  }

  @keyframes fade-in-up {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes pulse-down {
    0%, 100% {
      transform: rotate(90deg) translateY(0);
    }
    50% {
      transform: rotate(90deg) translateY(5px);
    }
  }

  /* Resource decoration */
  .resource-decoration {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
  }

  /* Treasure Tavern Ad Section */
  .treasure-tavern-section {
    background: linear-gradient(180deg, #1a1d33 0%, #0c0e17 100%);
    padding: 4rem 0;
    position: relative;
    overflow: hidden;
    border-top: 1px solid rgba(167, 139, 250, 0.2);
    border-bottom: 1px solid rgba(167, 139, 250, 0.2);
  }

  .treasure-tavern-ad {
    position: relative;
    background: rgba(20, 24, 42, 0.5);
    border-radius: 16px;
    padding: 2.5rem;
    backdrop-filter: blur(10px);
    box-shadow:
      0 20px 25px -5px rgba(0, 0, 0, 0.5),
      0 10px 10px -5px rgba(0, 0, 0, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.1),
      0 0 30px rgba(167, 139, 250, 0.15);
    overflow: hidden;
    transform-style: preserve-3d;
    transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .treasure-tavern-ad:hover {
    transform: translateY(-5px);
    box-shadow:
      0 25px 50px -12px rgba(0, 0, 0, 0.6),
      0 0 0 1px rgba(255, 255, 255, 0.15),
      0 0 30px rgba(167, 139, 250, 0.3);
  }

  .treasure-tavern-ad::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg,
      rgba(255, 215, 0, 0.5),
      rgba(167, 139, 250, 0.2),
      rgba(255, 215, 0, 0),
      rgba(167, 139, 250, 0.3));
    border-radius: 16px;
    z-index: -1;
    animation: treasure-border-flow 8s linear infinite;
    opacity: 0.7;
  }

  .treasure-tavern-glow {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
      radial-gradient(circle at 30% 40%, rgba(255, 215, 0, 0.2) 0%, transparent 50%),
      radial-gradient(circle at 70% 60%, rgba(167, 139, 250, 0.15) 0%, transparent 50%);
    opacity: 0.6;
    z-index: -1;
    animation: treasure-glow-pulse 4s ease-in-out infinite alternate;
  }

  .treasure-tavern-content {
    position: relative;
    z-index: 1;
    text-align: center;
    max-width: 700px;
    margin: 0 auto;
  }

  .treasure-title {
    font-size: clamp(2rem, 5vw, 3rem);
    background: linear-gradient(135deg, #FFD700, #a78bfa);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 1rem;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
  }

  .treasure-description {
    font-size: clamp(1.1rem, 2.5vw, 1.25rem);
    color: #e5e7eb;
    margin-bottom: 2rem;
    line-height: 1.6;
  }

  .treasure-features {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .treasure-feature {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.25rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 100px;
    font-size: 1.05rem;
    border: 1px solid rgba(255, 215, 0, 0.2);
    transition: all 0.3s ease;
  }

  .treasure-tavern-ad:hover .treasure-feature {
    background: rgba(255, 215, 0, 0.1);
    border-color: rgba(255, 215, 0, 0.4);
    transform: translateY(-2px);
  }

  .treasure-button {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(167, 139, 250, 0.2) 100%);
    color: #FFD700;
    border: 1px solid rgba(255, 215, 0, 0.5);
    border-radius: 30px;
    font-weight: 600;
    font-size: 1.1rem;
    text-decoration: none;
    transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    position: relative;
    overflow: hidden;
    z-index: 1;
  }

  .treasure-button-glow {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at center, rgba(255, 215, 0, 0.4) 0%, transparent 70%);
    opacity: 0;
    z-index: -1;
    transition: opacity 0.4s ease;
  }

  .treasure-button:hover {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.3) 0%, rgba(167, 139, 250, 0.3) 100%);
    transform: translateY(-3px);
    box-shadow:
      0 6px 15px rgba(255, 215, 0, 0.4),
      0 0 20px rgba(167, 139, 250, 0.2);
    color: white;
  }

  .treasure-button:hover .treasure-button-glow {
    opacity: 1;
    animation: treasure-pulse-button 1.5s infinite;
  }

  .treasure-button:hover svg {
    transform: translateX(5px);
  }

  .treasure-decoration {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
  }

  .treasure-sparkle {
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: rgba(255, 215, 0, 0.8);
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    animation: treasure-sparkle 4s ease-in-out infinite;
  }

  .treasure-sparkle-1 {
    top: 25%;
    left: 15%;
    width: 8px;
    height: 8px;
    animation-delay: 0s;
  }

  .treasure-sparkle-2 {
    top: 35%;
    right: 10%;
    width: 6px;
    height: 6px;
    animation-delay: 1s;
  }

  .treasure-sparkle-3 {
    bottom: 20%;
    left: 25%;
    width: 4px;
    height: 4px;
    animation-delay: 1.5s;
  }

  .treasure-sparkle-4 {
    bottom: 40%;
    right: 20%;
    width: 5px;
    height: 5px;
    animation-delay: 0.5s;
  }

  @keyframes treasure-border-flow {
    0% {
      background-position: 0% 0%;
    }
    100% {
      background-position: 300% 0%;
    }
  }

  @keyframes treasure-glow-pulse {
    0%, 100% {
      opacity: 0.6;
    }
    50% {
      opacity: 0.8;
    }
  }

  @keyframes treasure-pulse-button {
    0%, 100% {
      opacity: 0.6;
      transform: scale(1);
    }
    50% {
      opacity: 0.8;
      transform: scale(1.1);
    }
  }

  @keyframes treasure-sparkle {
    0%, 100% {
      opacity: 0.5;
      transform: scale(1);
    }
    50% {
      opacity: 1;
      transform: scale(1.5);
    }
  }

  @media (max-width: 767px) {
    .treasure-tavern-section {
      padding: 3rem 0;
    }

    .treasure-tavern-ad {
      padding: 2rem 1.5rem;
    }

    .treasure-features {
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }
  }
</style>