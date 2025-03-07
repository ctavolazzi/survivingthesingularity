<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import bookCover from '$lib/images/Surviving-the-Singularity-Cover.png';
  import chessImage from '$lib/images/sts-chess.jpg';

  let showNextSteps = true;
  let activeSection = 0;
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
      <div class="hero-badge">Welcome</div>
      <h1 class="hero-title">Your Journey Begins Here</h1>
      <p class="hero-description">
        This guide will help you navigate the singularity and the resources available on this site.
      </p>
      <div class="hero-scroll">
        <a href="#singularity-intro" class="scroll-btn">
          <span>Get Started</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 13l5 5 5-5"/></svg>
        </a>
      </div>
    </div>
    <div class="hero-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="grid-pattern"></div>
    </div>
  </header>

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
  }

  h2 {
    font-size: clamp(1.5rem, 4vw, 2rem);
    color: #a78bfa;
    margin-bottom: 1.25rem;
    text-align: center;
  }

  h3 {
    font-size: clamp(1.1rem, 3vw, 1.25rem);
    color: #a78bfa;
    margin-bottom: 0.5rem;
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
    max-width: 600px;
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
    line-height: 1.2;
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
  }

  .primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 10px -1px rgba(99, 102, 241, 0.4);
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
    }

    .book-cover {
      max-width: 150px;
    }

    h2 {
      margin-bottom: 1rem;
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
</style>