<script>
  import { fade, fly, scale } from 'svelte/transition';
  import { onMount } from 'svelte';
  import FAQ from '$lib/components/FAQ.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import BookSample from '$lib/components/BookSample.svelte';
  import Spacer from '$lib/components/Spacer.svelte';

  // For intersection observer animations
  let sections = [];
  let visibleSections = new Set();

  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          visibleSections.add(entry.target.id);
        }
      });
    }, { threshold: 0.2 });

    sections.forEach(section => {
      if (section) observer.observe(section);
    });

    return () => sections.forEach(section => {
      if (section) observer.unobserve(section);
    });
  });
</script>

<div class="main-content">
  <header in:fade={{ duration: 800, delay: 200 }} class="hero">
    <div class="hero-content">
      <h1 class="title">Surviving the Singularity</h1>
      <p class="subtitle">Navigate and Thrive in the AI Revolution</p>
      <p class="tagline">A companion for making sense of our rapidly changing world</p>
    </div>
  </header>

  <section class="book-showcase container">
    <div in:scale={{ duration: 600, delay: 300, start: 0.9 }}>
      <BookSample />
    </div>
  </section>

  <section
    bind:this={sections[0]}
    id="intro"
    class="intro-section container"
    class:visible={visibleSections.has('intro')}
  >
    <div class="section-inner">
      <h2 class="accent-left">The Future Is Now</h2>
      <p class="large-text">The future is approaching faster than you think.</p>
      <p>This book is being actively written as a companion to help you process the rapid technological changes we're experiencing. It aims to provide you with tools for thinking more clearly about our collective future.</p>
    </div>
  </section>

  <section
    bind:this={sections[1]}
    id="writing"
    class="writing-section container"
    class:visible={visibleSections.has('writing')}
  >
    <div class="section-inner">
      <h2 class="accent-right">A Book Being Actively Written</h2>
      <div class="two-column">
        <div class="column">
          <p>This book is being written in real-time as we all navigate these unprecedented technological changes together. Rather than rush to conclusions, I'm taking the time to:</p>
        </div>
        <div class="column feature-list-container">
          <ul class="feature-list">
            <li><span class="icon">📝</span> Document the unfolding AI revolution as it happens</li>
            <li><span class="icon">🔍</span> Research and analyze emerging patterns</li>
            <li><span class="icon">🧠</span> Develop thoughtful frameworks for understanding these changes</li>
            <li><span class="icon">🌐</span> Build a community of thoughtful participants in this journey</li>
          </ul>
        </div>
      </div>
      <p class="highlight-text">Your patience and participation are valuable parts of this process.</p>
    </div>
  </section>

  <section
    bind:this={sections[2]}
    id="benefits"
    class="benefits-section container"
    class:visible={visibleSections.has('benefits')}
  >
    <div class="section-inner">
      <h2 class="accent-left">What You Might Gain</h2>
      <div class="cards-grid">
        <div class="benefit-card">
          <div class="card-icon">🧠</div>
          <h3>Deep Understanding</h3>
          <p>Deeper understanding of AI and its societal impacts</p>
        </div>
        <div class="benefit-card">
          <div class="card-icon">🛠️</div>
          <h3>Practical Frameworks</h3>
          <p>Frameworks for thinking about an AI-driven world</p>
        </div>
        <div class="benefit-card">
          <div class="card-icon">🧭</div>
          <h3>Navigation Skills</h3>
          <p>Strategies for navigating uncertainty</p>
        </div>
        <div class="benefit-card">
          <div class="card-icon">🔧</div>
          <h3>Processing Tools</h3>
          <p>Tools for processing complex technological shifts</p>
        </div>
        <div class="benefit-card">
          <div class="card-icon">🔍</div>
          <h3>Personal Perspective</h3>
          <p>Confidence in forming your own view on emerging technologies</p>
        </div>
      </div>
    </div>
  </section>

  <section
    bind:this={sections[3]}
    id="bookInfo"
    class="book-info-section container"
    class:visible={visibleSections.has('bookInfo')}
  >
    <div class="section-inner">
      <h2 class="accent-center">More Than Just a Book</h2>
      <div class="two-column aligned-items">
        <div class="column">
          <p class="intro-text">"Surviving the Singularity" is designed as an evolving resource to guide you through the AI revolution:</p>
        </div>
        <div class="column">
          <div class="features-grid">
            <div class="feature">
              <strong>Interactive Workbook</strong>
              <p>Engage with thought-provoking exercises and scenarios</p>
            </div>
            <div class="feature">
              <strong>Personal AI Journal</strong>
              <p>Document your journey and insights</p>
            </div>
            <div class="feature">
              <strong>Digital Resources</strong>
              <p>Access additional materials as they're developed</p>
            </div>
            <div class="feature">
              <strong>Self-Guided Research</strong>
              <p>Embark on your own AI exploration</p>
            </div>
            <div class="feature">
              <strong>Future-Proofing</strong>
              <p>Develop frameworks for an AI-driven world</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section
    bind:this={sections[4]}
    id="future"
    class="evolving-section container"
    class:visible={visibleSections.has('future')}
  >
    <div class="section-inner">
      <h2 class="accent-right">An Evolving Resource</h2>
      <div class="evolution-timeline">
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <p>Content evolves with new AI developments</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <p>Resources expand to include different perspectives</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <p>Community insights inform future directions</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <p>Practical frameworks refined based on real-world applications</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <p>Final book reflects our journey through this pivotal period</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section
    bind:this={sections[5]}
    id="audience"
    class="audience-section container"
    class:visible={visibleSections.has('audience')}
  >
    <div class="section-inner">
      <h2 class="accent-left">Who Is This For?</h2>
      <div class="audience-grid">
        <div class="audience-card">
          <div class="audience-icon">👩‍💼</div>
          <p>Thoughtful individuals processing rapid technological change</p>
        </div>
        <div class="audience-card">
          <div class="audience-icon">👨‍💻</div>
          <p>Professionals seeking to understand AI's potential impacts</p>
        </div>
        <div class="audience-card">
          <div class="audience-icon">🤔</div>
          <p>Anyone feeling overwhelmed by the pace of technological advancement</p>
        </div>
        <div class="audience-card">
          <div class="audience-icon">🔍</div>
          <p>Those curious about the societal implications of AI</p>
        </div>
      </div>
    </div>
  </section>

  <section
    bind:this={sections[6]}
    id="testimonials"
    class="testimonials-section container"
    class:visible={visibleSections.has('testimonials')}
  >
    <div class="section-inner">
      <h2 class="accent-center">What Early Readers Are Saying</h2>
      <div class="testimonials-grid">
        <div class="testimonial-card">
          <div class="quote-mark">"</div>
          <p>This isn't just a book, it's a personal AI revolution in your hands. The interactive elements make learning about AI an exciting journey of discovery.</p>
          <div class="testimonial-author">
            <span class="author-name">Emma Rodriguez</span>
            <span class="author-title">Tech Entrepreneur</span>
          </div>
        </div>
        <div class="testimonial-card">
          <div class="quote-mark">"</div>
          <p>The workbook and journal aspects helped me apply AI concepts to my own life and career in ways I never imagined. A truly transformative experience!</p>
          <div class="testimonial-author">
            <span class="author-name">Dr. James Lee</span>
            <span class="author-title">Futurist</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section
    bind:this={sections[7]}
    id="scenarios"
    class="scenarios-section container"
    class:visible={visibleSections.has('scenarios')}
  >
    <div class="section-inner">
      <h2 class="accent-right">Making Sense of Rapid Change</h2>
      <p class="large-text">The pace of technological change can be overwhelming.</p>
      <p>This book helps you think through scenarios like:</p>

      <div class="scenarios-grid">
        <div class="scenario-card">
          <div class="scenario-number">01</div>
          <p>How AI might transform everyday tasks and routines</p>
        </div>
        <div class="scenario-card">
          <div class="scenario-number">02</div>
          <p>The potential evolution of AI in healthcare, education, and work</p>
        </div>
        <div class="scenario-card">
          <div class="scenario-number">03</div>
          <p>Ethical considerations as AI becomes more integrated into society</p>
        </div>
        <div class="scenario-card">
          <div class="scenario-number">04</div>
          <p>Ways to maintain human agency and meaning in an AI-rich world</p>
        </div>
        <div class="scenario-card">
          <div class="scenario-number">05</div>
          <p>How to prepare mentally and practically for continuing technological shifts</p>
        </div>
      </div>

      <p class="emphasis-text">Don't just witness the future—develop tools to understand it.</p>
    </div>
  </section>

  <section class="faq-section container">
    <div class="section-inner">
      <FAQ />
    </div>
  </section>

  <section
    bind:this={sections[8]}
    id="newsletter"
    class="newsletter-section container"
    class:visible={visibleSections.has('newsletter')}
  >
    <div class="section-inner">
      <h2 class="accent-center">Stay Informed</h2>
      <p>Join our newsletter to receive updates as the book develops and new insights emerge.</p>
      <div class="newsletter-container">
        <NewsletterSignup />
      </div>
    </div>
  </section>

  <Spacer height="50px" />

  <footer class="site-footer">
    <div class="footer-content">
      <h2>Get In Touch</h2>
      <p>Have questions or thoughts about the project?</p>
      <a href="mailto:info@survivingthesingularity.com" class="email-link">
        info@survivingthesingularity.com
      </a>
      <div class="social-links">
        <a href="https://twitter.com" aria-label="Twitter profile" rel="noopener noreferrer" target="_blank" class="social-icon">Twitter</a>
        <a href="https://linkedin.com" aria-label="LinkedIn profile" rel="noopener noreferrer" target="_blank" class="social-icon">LinkedIn</a>
        <a href="https://instagram.com" aria-label="Instagram profile" rel="noopener noreferrer" target="_blank" class="social-icon">Instagram</a>
      </div>
      <p class="copyright">© {new Date().getFullYear()} Surviving the Singularity</p>
    </div>
  </footer>

  <Spacer height="1rem"/>
</div>

<style>
  /* Base Layout */
  .main-content {
    width: 100%;
    margin: 0 auto;
    box-sizing: border-box;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 5rem 1.5rem;
    scroll-margin-top: 2rem;
  }

  .section-inner {
    max-width: 1000px;
    margin: 0 auto;
  }

  /* Typography */
  .title {
    font-size: clamp(2.5rem, 8vw, 5rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1rem;
    background: linear-gradient(120deg, var(--color-text-primary), var(--color-accent, #7c3aed));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: -0.03em;
  }

  h2 {
    font-size: clamp(2rem, 6vw, 3.5rem);
    font-weight: 700;
    margin-bottom: 2rem;
    line-height: 1.1;
    letter-spacing: -0.02em;
    position: relative;
  }

  .accent-left {
    padding-left: 1.5rem;
    border-left: 6px solid var(--color-accent, #7c3aed);
    margin-left: -1.5rem;
  }

  .accent-right {
    padding-right: 1.5rem;
    border-right: 6px solid var(--color-accent, #7c3aed);
    margin-right: -1.5rem;
    text-align: right;
  }

  .accent-center {
    position: relative;
    text-align: center;
  }

  .accent-center::after {
    content: '';
    position: absolute;
    width: 80px;
    height: 4px;
    background-color: var(--color-accent, #7c3aed);
    bottom: -15px;
    left: calc(50% - 40px);
  }

  h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }

  p, li {
    font-size: clamp(1rem, 2vw, 1.1rem);
    line-height: 1.6;
    margin-bottom: 1.5rem;
    color: var(--color-text-secondary, #4b5563);
  }

  .large-text {
    font-size: clamp(1.25rem, 3vw, 1.8rem);
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 1.5rem;
    color: var(--color-text-primary);
  }

  .subtitle {
    font-size: clamp(1.2rem, 3vw, 2rem);
    margin-bottom: 0.75rem;
    color: var(--color-text-secondary, #4b5563);
    font-weight: 500;
  }

  .tagline {
    font-size: clamp(1rem, 2vw, 1.3rem);
    color: var(--color-text-secondary, #4b5563);
    margin-bottom: 2rem;
    font-weight: 400;
  }

  /* Header/Hero Section */
  .hero {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 3rem 1.5rem;
    background: radial-gradient(circle at center, rgba(124, 58, 237, 0.1) 0%, rgba(0, 0, 0, 0) 70%);
  }

  .hero-content {
    max-width: 800px;
  }

  /* Grid Layouts */
  .two-column {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .aligned-items {
    align-items: center;
  }

  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
  }

  .testimonials-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
    margin: 3rem 0;
  }

  .scenarios-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }

  .audience-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }

  /* Card Components */
  .benefit-card, .feature, .testimonial-card, .scenario-card, .audience-card {
    background-color: var(--color-bg-card, #f9fafb);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .benefit-card:hover, .scenario-card:hover, .audience-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.09);
  }

  .card-icon, .audience-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .testimonial-card {
    padding: 2rem;
    position: relative;
  }

  .quote-mark {
    font-size: 4rem;
    position: absolute;
    top: -10px;
    left: 10px;
    color: var(--color-accent, #7c3aed);
    opacity: 0.2;
    font-family: serif;
  }

  .testimonial-author {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
  }

  .author-name {
    font-weight: 600;
    color: var(--color-text-primary);
  }

  .author-title {
    font-size: 0.9rem;
    color: var(--color-text-secondary, #6b7280);
  }

  .scenario-number {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-accent, #7c3aed);
    opacity: 0.4;
    margin-bottom: 0.5rem;
  }

  /* Feature List */
  .feature-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  .feature-list li {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1.25rem;
    font-size: 1.1rem;
  }

  .icon {
    margin-right: 1rem;
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  /* Timeline */
  .evolution-timeline {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin: 2rem 0;
    position: relative;
  }

  .evolution-timeline::after {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    left: 15px;
    width: 2px;
    background-color: var(--color-accent, #7c3aed);
    opacity: 0.3;
  }

  .timeline-item {
    display: flex;
    align-items: flex-start;
    position: relative;
    z-index: 1;
    padding-left: 2.5rem;
  }

  .timeline-marker {
    position: absolute;
    left: 0;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: var(--color-bg-card, #f9fafb);
    border: 2px solid var(--color-accent, #7c3aed);
    z-index: 2;
  }

  .timeline-content {
    flex: 1;
  }

  .timeline-content p {
    margin-bottom: 0;
  }

  /* Highlight Elements */
  .highlight-text {
    display: inline-block;
    background-color: rgba(124, 58, 237, 0.1);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    margin: 1rem 0;
    font-weight: 500;
    color: var(--color-text-primary);
  }

  .emphasis-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--color-accent, #7c3aed);
    margin: 2rem 0 1rem;
    text-align: center;
  }

  /* Newsletter */
  .newsletter-container {
    max-width: 500px;
    margin: 2rem auto 0;
  }

  /* Footer */
  .site-footer {
    background-color: var(--color-bg-secondary, #f3f4f6);
    padding: 4rem 1.5rem;
    text-align: center;
  }

  .footer-content {
    max-width: 600px;
    margin: 0 auto;
  }

  .social-links {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin: 1.5rem 0;
  }

  .social-icon {
    color: var(--color-text-secondary, #4b5563);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
  }

  .social-icon:hover {
    color: var(--color-accent, #7c3aed);
  }

  .email-link {
    color: var(--color-accent, #7c3aed);
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.2s ease;
    display: inline-block;
    margin: 0.5rem 0 1rem;
  }

  .email-link:hover {
    opacity: 0.8;
  }

  .copyright {
    font-size: 0.9rem;
    margin-top: 2rem;
    color: var(--color-text-secondary, #6b7280);
  }

  /* Animations */
  section {
    opacity: 0.5;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  section.visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* Media Queries */
  @media (min-width: 768px) {
    .two-column {
      grid-template-columns: 1fr 1fr;
    }

    .testimonials-grid {
      grid-template-columns: 1fr 1fr;
    }

    .evolution-timeline::after {
      left: 40px;
    }

    .timeline-marker {
      width: 40px;
      height: 40px;
      left: 20px;
    }

    .timeline-item {
      padding-left: 5rem;
    }
  }

  /* Dark mode styles */
  :global(.dark) {
    --color-bg-card: #2a2a2a;
    --color-bg-secondary: #1a1a1a;
    --color-text-primary: #e5e7eb;
    --color-text-secondary: #9ca3af;
    --color-accent: #a78bfa;
  }

  :global(.dark) .testimonial-card,
  :global(.dark) .benefit-card,
  :global(.dark) .scenario-card,
  :global(.dark) .audience-card,
  :global(.dark) .feature {
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
  }

  :global(.dark) .timeline-marker {
    background-color: #2a2a2a;
  }
</style>