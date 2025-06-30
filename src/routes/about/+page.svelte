<script>
  import FAQ from '$lib/components/FAQ.svelte';
  import BookSample from '$lib/components/BookSample.svelte';


</script>

<svelte:head>
  <title>About | Surviving the Singularity</title>
  <meta name="description" content="Explore the exciting possibilities of AI and technological advancement with Surviving the Singularity - opening minds to the transformative potential ahead." />
</svelte:head>

<div class="about-page">
  <!-- Hero Section -->
  <header class="hero-section">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <div class="hero-badge">Surviving the Singularity</div>
      <h1 class="hero-title">Embrace the Age of Possibility</h1>
      <div class="hero-tagline">
        <p class="hero-description">Thoughtful perspectives on the extraordinary technological transformation unfolding around us.</p>
        <div class="hero-cta">
          <span class="rocket">✨</span>
          <span class="cta-text">Discover new perspectives. Explore possibilities. Expand your understanding.</span>
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
      <p class="lead">The Technological Singularity represents a fascinating concept: a future point where artificial intelligence could unlock unprecedented possibilities for human flourishing and understanding.</p>

      <div class="explanation-grid">
        <div class="explanation-card">
          <div class="icon">🧠</div>
          <h3>Enhanced Intelligence</h3>
          <p>AI capabilities that complement and amplify human intelligence, opening new frontiers of knowledge and creativity</p>
        </div>
        <div class="explanation-card">
          <div class="icon">📈</div>
          <h3>Accelerating Progress</h3>
          <p>A period of rapid technological advancement that could solve longstanding challenges and unlock new opportunities</p>
        </div>
        <div class="explanation-card">
          <div class="icon">🔄</div>
          <h3>Self-Improving Systems</h3>
          <p>AI systems that learn and evolve, potentially leading to breakthroughs we can barely imagine today</p>
        </div>
        <div class="explanation-card">
          <div class="icon">🌟</div>
          <h3>Emerging Possibilities</h3>
          <p>A future rich with potential discoveries, innovations, and ways of understanding our world</p>
        </div>
        <div class="explanation-card">
          <div class="icon">🤝</div>
          <h3>Human-AI Partnership</h3>
          <p>The opportunity for meaningful collaboration between human creativity and artificial intelligence</p>
        </div>
        <div class="explanation-card">
          <div class="icon">🔗</div>
          <h3>Technological Convergence</h3>
          <p>The beautiful intersection of AI with biotech, nanotech, and quantum computing, creating new possibilities</p>
        </div>
      </div>

      <p>First described by mathematician Vernor Vinge and explored by futurist Ray Kurzweil, the Singularity invites us to consider how technology might transform human potential. While we can't predict exactly how this will unfold, we can approach these changes with curiosity and thoughtful consideration.</p>
    </div>
  </section>

  <!-- Section 2: What is this project all about? -->
  <section class="about-project">
    <div class="container">
      <h2>What is this project all about?</h2>
      <p class="lead">Surviving the Singularity is a space for curious minds to explore the fascinating world of AI and technological possibility.</p>

      <div class="project-description">
        <p>This project began with a sense of wonder: we're living through an extraordinary moment in human history, where technology is opening doors we never knew existed. Rather than feeling overwhelmed, we can approach these changes with curiosity and openness.</p>

        <p>Our approach focuses on:</p>
        <ul class="mission-list">
          <li><span class="highlight">Wonder</span> — Appreciating the remarkable nature of current technological developments</li>
          <li><span class="highlight">Understanding</span> — Exploring the broader context and meaning of these changes</li>
          <li><span class="highlight">Perspective</span> — Offering thoughtful viewpoints on what these developments might mean</li>
          <li><span class="highlight">Inspiration</span> — Highlighting the positive potential and exciting possibilities ahead</li>
        </ul>

        <p>Whether you're fascinated by technology, curious about the future, or simply interested in new ideas, this project invites you to explore these topics with an open mind and a sense of possibility.</p>
      </div>

      <!-- Book Preview -->
      <div class="book-preview-section">
        <BookSample />
      </div>
    </div>
  </section>

  <!-- Section 3: What makes this moment special? -->
  <section class="need-to-know">
    <div class="container">
      <h2>What makes this moment special?</h2>
      <p class="lead">We're witnessing something remarkable: technology that's expanding what it means to be human and creative.</p>

      <div class="key-insights">
        <div class="insight">
          <h3>AI is unlocking human potential</h3>
          <p>Across every field—from healthcare to education, science to the arts—AI is becoming a powerful tool that amplifies human creativity and problem-solving. It's fascinating to see how this partnership is evolving.</p>
        </div>

        <div class="insight">
          <h3>We're experiencing accelerated discovery</h3>
          <p>The pace of innovation is breathtaking. What once took years to develop now happens in months. This acceleration means we get to witness and participate in unprecedented breakthroughs.</p>
        </div>

        <div class="insight">
          <h3>Curiosity and openness matter more than ever</h3>
          <p>In a world of rapid change, the most valuable qualities are curiosity, adaptability, and the willingness to learn. These human traits become even more precious as technology advances.</p>
        </div>

        <div class="insight">
          <h3>There are endless opportunities to explore</h3>
          <p>From learning about AI capabilities to discovering new ways of thinking and creating, there are countless paths to explore and ways to engage with these emerging possibilities.</p>
        </div>
      </div>

      <div class="faq-section">
        <h3>Common Questions</h3>
        <FAQ />
      </div>
    </div>
  </section>

  <!-- Section 4: How can you explore further? -->
  <section class="support-section">
    <div class="container">
      <h2>How can you explore further?</h2>

      <div class="support-grid">
        <div class="support-card">
          <div class="support-icon">📚</div>
          <h3>Dive into the Content</h3>
          <p>Explore our articles and resources at your own pace. Share what resonates with others who might find it interesting.</p>
        </div>

        <div class="support-card">
          <div class="support-icon">💭</div>
          <h3>Reflect and Consider</h3>
          <p>Take time to think about these ideas and how they might relate to your own interests and experiences.</p>
        </div>

        <div class="support-card">
          <div class="support-icon">🌱</div>
          <h3>Stay Curious</h3>
          <p>Keep an open mind about technological developments and their potential to enhance human creativity and understanding.</p>
        </div>
      </div>

    </div>
  </section>

  <!-- Footer -->
  <section class="contact">
    <div class="container">
      <!-- Copyright notice removed -->
    </div>
  </section>

  <!-- Treasure Tavern Ad removed -->
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



  /* Responsive adjustments */
  @media (min-width: 768px) {
    .support-grid {
      grid-template-columns: repeat(3, 1fr);
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


</style>