<script>
  import { fade } from 'svelte/transition';
  import FAQ from '$lib/components/FAQ.svelte';
  import Countdown from '$lib/components/Countdown.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import BookSample from '$lib/components/BookSample.svelte';
  import Spacer from '$lib/components/Spacer.svelte';

  const targetDate = new Date("2027-11-20T23:59:59").getTime();
</script>

<Spacer height="50px" />

<div class="main-content">
  <header>
    <h1 class="title">About Surviving the Singularity</h1>
    <p class="subtitle">Navigate the AI Revolution Together</p>
  </header>

  <section class="book-info">
    <h2>More Than Just a Book</h2>
    <div class="content-grid">
      <div class="ul-centered-left">
        <p>"Surviving the Singularity" is a revolutionary multi-format experience designed to guide you through the AI revolution:</p>
        <ul>
          <li><strong>Interactive Workbook:</strong> Engage with thought-provoking exercises and scenarios.</li>
          <li><strong>Personal AI Journal:</strong> Document your journey and insights.</li>
          <li><strong>Exclusive Digital Content:</strong> Access additional resources via QR codes.</li>
          <li><strong>Self-Guided Research Tool:</strong> Embark on your own AI exploration.</li>
          <li><strong>Future-Proofing Strategies:</strong> Develop practical skills for an AI-driven world.</li>
        </ul>
      </div>
      <div class="visual-content">
        <div class="book-sample-wrapper">
          <BookSample />
        </div>
      </div>
    </div>
  </section>

  <div class="stylish-divider"></div>

  <section class="future-learning">
    <h2 class="text-center">Experience the Future of Learning</h2>
    <div class="content-grid">
      <div class="ul-centered-left">
        <p>Our innovative QR code system allows you to:</p>
        <ul>
          <li>Access exclusive online content updated in real-time</li>
          <li>Dive deep into AI topics with curated resources</li>
          <li>Participate in community discussions and expert Q&As</li>
          <li>Track your progress and unlock achievements</li>
        </ul>
      </div>
    </div>
  </section>

  <div class="stylish-divider"></div>

  <section class="testimonials">
    <h2 class="text-center">What Early Adopters Are Saying</h2>
    <div class="content-grid">
      <blockquote>
        <p>"This isn't just a book, it's a personal AI revolution in your hands. The interactive elements and QR codes make learning about AI an exciting journey of discovery."</p>
        <footer>- Emma Rodriguez, Tech Entrepreneur</footer>
      </blockquote>
      <blockquote>
        <p>"The workbook and journal aspects helped me apply AI concepts to my own life and career in ways I never imagined. A truly transformative experience!"</p>
        <footer>- Dr. James Lee, Futurist</footer>
      </blockquote>
    </div>
  </section>

  <div class="stylish-divider"></div>

  <FAQ />

  <div class="stylish-divider"></div>

  <section class="newsletter">
    <h2>Stay Informed</h2>
    <p>Join our newsletter to receive regular updates on AI advancements and community insights.</p>
    <NewsletterSignup />
  </section>

  <div class="stylish-divider"></div>

  <section class="countdown">
    <div class="countdown-container">
      <Countdown {targetDate} />
      <p>The technological singularity is approaching rapidly. Will you be prepared?</p>
    </div>
  </section>

  <Spacer height="1rem"/>
</div>

<style>

.book-info {
    text-align: center;
    margin-bottom: 3rem;
    width: 100%;
  }

  .main-content {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
    box-sizing: border-box;
  }

  header, section {
    margin-bottom: 3rem;
    width: 100%;
  }

  .title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: var(--color-text-primary);
  }

  .subtitle {
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    color: var(--color-text-secondary);
  }

  h2 {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    font-weight: bold;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  p, li {
    font-size: clamp(1rem, 2vw, 1.2rem);
    line-height: 1.6;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
  }

  .content-grid {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }

  .ul-centered-left {
    display: inline-block;
    text-align: left;
    max-width: 600px;
    margin: 0 auto;
  }

  .ul-centered-left p {
    margin-bottom: 1rem;
  }

  .ul-centered-left ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
  }

  .text-content {
    width: 100%;
    text-align: left;
  }

  .visual-content {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }

  blockquote {
    background-color: var(--color-bg-secondary);
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    width: 100%;
  }

  blockquote p {
    font-style: italic;
  }

  blockquote footer {
    font-weight: bold;
    margin-top: 0.5rem;
  }

  .countdown-container {
    background-color: var(--color-bg-secondary);
    padding: 1.5rem;
    border-radius: 8px;
    width: 100%;
  }

  .stylish-divider {
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
    margin: 2rem auto;
    width: 100%;
    max-width: 80%;
  }

  .book-sample-wrapper {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }

  @media (max-width: 640px) {
    .book-sample-wrapper {
      width: 95%; /* Slightly smaller on very small screens */
    }
  }

  @media (min-width: 768px) {
    .main-content {
      padding: 2rem;
    }
  }

  @media (min-width: 1024px) {
    .main-content {
      padding: 3rem;
    }
  }

  /* Dark mode styles */
  :global(.dark) .title,
  :global(.dark) h2,
  :global(.dark) p,
  :global(.dark) li {
    color: #e5e7eb;
  }

  :global(.dark) .subtitle {
    color: #9ca3af;
  }

  :global(.dark) blockquote,
  :global(.dark) .countdown-container {
    background-color: #2a2a2a;
  }

  :global(.dark) .stylish-divider {
    background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
  }

  :global(.dark) .placeholder-image {
    background-color: #2a2a2a;
    color: #9ca3af;
  }
</style>