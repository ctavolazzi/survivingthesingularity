<script>
  import { fade } from 'svelte/transition';
  import FAQ from '$lib/components/FAQ.svelte';
  import Countdown from '$lib/components/Countdown.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import BookSample from '$lib/components/BookSample.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import FloatingPopupProgressBar from '$lib/components/FloatingPopupProgressBar.svelte';
  import CommunityIntakePopupForm from '$lib/components/CommunityIntakePopupForm.svelte';
  import FloatingQuotePopup from '$lib/components/FloatingQuotePopup.svelte';
  import { goto } from '$app/navigation';

  const targetDate = new Date("2027-11-20T23:59:59").getTime();

  const handleGetFreeSample = () => {
    goto("/sample");
    console.log("Get a free sample");
  };
</script>

<div class="main-content text-center">
  <header>
    <h1 class="title">Surviving the Singularity</h1>
    <p class="subtitle">Navigate and Thrive in the AI Revolution</p>
    <p class="tagline">A comprehensive program to prepare you for the AI-driven future</p>
  </header>

  <section class="intro">
    <p class="large-text">The future is approaching faster than you think. Are you prepared?</p>
    <p>Our comprehensive program equips you with the knowledge, skills, and community to not just survive, but thrive in the coming age of artificial intelligence.</p>
  </section>

  <div class="stylish-divider"></div>

  <section class="program-overview">
    <h2 class="text-center">What You'll Gain</h2>
    <div class="content-grid">
      <div class="ul-centered-left">
        <ul>
          <li>Deep understanding of AI and its societal impacts</li>
          <li>Practical skills for adapting to an AI-driven world</li>
          <li>Strategies for future-proofing your career</li>
          <li>Network of like-minded individuals and experts</li>
          <li>Confidence in navigating rapid technological changes</li>
        </ul>
      </div>
    </div>
  </section>

  <div class="stylish-divider"></div>

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

  <section class="program-structure">
    <h2 class="text-center">Program Structure</h2>
    <div class="content-grid">
      <div class="ul-centered-left">
        <p class="text-center">Our self-paced program typically takes 12 weeks to complete:</p>
        <ul class="feature-list">
          <li><span class="icon">📚</span> Weekly modules with video lessons and readings</li>
          <li><span class="icon">🧠</span> Interactive exercises and quizzes</li>
          <li><span class="icon">💬</span> Monthly live Q&A sessions with experts</li>
          <li><span class="icon">🌐</span> Ongoing access to our online community</li>
        </ul>
        <p class="text-center">Access all materials for a full year after enrollment.</p>
      </div>
    </div>
  </section>

  <div class="stylish-divider"></div>

  <section class="future-learning">
    <h2 class="text-center">Experience the Future of Learning</h2>
    <div class="content-grid">
      <div class="ul-centered-left">
        <p>Our innovative QR code system is just the beginning of your journey:</p>
        <ul>
          <li>Access exclusive online content updated in real-time</li>
          <li>Dive deep into AI topics with curated resources</li>
          <li>Participate in our vibrant online learning community</li>
          <li>Engage in practical exercises to prepare for the AI-driven future</li>
          <li>Track your progress and unlock achievements as you adapt to the rapidly evolving tech landscape</li>
        </ul>
      </div>
    </div>
  </section>

  <div class="stylish-divider"></div>

  <section class="who-is-this-for">
    <h2 class="text-center">Who Is This For?</h2>
    <div class="content-grid">
      <div class="ul-centered-left">
        <p class="font-bold">This program is ideal for:</p>
        <ul>
          <li>Professionals looking to future-proof their careers</li>
          <li>Entrepreneurs seeking AI-driven opportunities</li>
          <li>Students preparing for an AI-dominated job market</li>
          <li>Anyone curious about the impact of AI on society</li>
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

  <section class="future-scenarios">
    <h2 class="font-bold text-center">Preparing for the Near Future</h2>
    <div class="content-grid">
      <div class="ul-centered-left">
        <p>The technological singularity is closer than you think. Our program helps you prepare for scenarios like:</p>
        <ul>
          <li>Robots handling household chores by 2025</li>
          <li>AI doctors leveraging all medical knowledge for diagnoses by 2026</li>
          <li>Autonomous vehicles becoming the norm on our roads</li>
          <li>AI-driven personal assistants managing your daily life</li>
          <li>Rapid job market shifts due to AI and automation</li>
        </ul>
        <p class="emphasis-text font-bold">Don't just witness the future—be ready to thrive in it.</p>
      </div>
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

  <!-- <section class="enrollment">
    <h2 class="text-center">Join Surviving the Singularity</h2>
    <div class="pricing-grid">
      <div class="pricing-option">
        <h3>Basic Access</h3>
        <p class="price">$299</p>
        <ul>
          <li>Full course access</li>
          <li>Community forum</li>
          <li>3 months support</li>
        </ul>
        <button class="enroll-button" on:click={() => goto("/enroll/basic")}>Enroll Now</button>
      </div>
      <div class="pricing-option featured">
        <h3>Premium Access</h3>
        <p class="price">$499</p>
        <ul>
          <li>Everything in Basic</li>
          <li>1-on-1 coaching session</li>
          <li>Lifetime support</li>
          <li>Exclusive webinars</li>
        </ul>
        <button class="enroll-button" on:click={() => goto("/enroll/premium")}>Enroll Now</button>
      </div>
    </div>
    <p class="money-back">30-day money-back guarantee</p>
  </section> -->

  <div class="stylish-divider"></div>

  <!-- <section class="countdown">
    <div class="countdown-container">
      <Countdown {targetDate} />
      <p class="text-center">The technological singularity is approaching rapidly.</p>
      <p class="text-center large-text">Will you be prepared?</p>
      <div class="text-center">
        <p><em>This timer is our estimate of when human-level robots with general intelligence will begin to be mass-produced and available to the public.</em></p>
        <p>
          If that makes you feel anxious, or excited, or both, we'd love to have you join us on this journey.
        </p>
        <p>
          <button class="big-button" on:click={handleGetFreeSample}>Get a free sample</button>
        </p>
      </div>
    </div>
  </section> -->
  <CommunityIntakePopupForm />

  <Spacer height="50px" />

  <section class="support-info">
    <h2 class="text-center">We're Here to Help</h2>
    <p>Have questions? Our support team is available 24/7.</p>
    <p>Email: info@survivingthesingularity.com</p>
  </section>

  <Spacer height="1rem"/>
</div>

<!-- <FloatingPopupProgressBar /> -->
<!-- <FloatingQuotePopup minDelay={20000} /> -->

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
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
  }

  .ul-centered-left p {
    margin-bottom: 1rem;
  }

  .ul-centered-left ul {
    list-style-type: disc;
    padding-left: 2.5rem;
    margin-bottom: 1rem;
    text-align: left;
  }

  .emphasis-text {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--color-text-secondary);
    margin-top: 1rem;
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

  .large-text {
    font-size: 1.5rem; /* Equivalent to text-2xl in Tailwind */
    line-height: 2rem;
  }

  @keyframes pulse-glow {
    0% {
      box-shadow: 0 0 5px #FF8C00, 0 0 10px #FF8C00, 0 0 15px #FF8C00;
    }
    50% {
      box-shadow: 0 0 10px #FFA500, 0 0 20px #FFA500, 0 0 30px #FFA500;
    }
    100% {
      box-shadow: 0 0 5px #FF8C00, 0 0 10px #FF8C00, 0 0 15px #FF8C00;
    }
  }

  .big-button {
    font-size: 1.5rem;
    padding: 1rem 2rem;
    background-color: #FF8C00; /* Dark Orange */
    color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    position: relative;
    overflow: hidden;
    animation: pulse-glow 2s infinite;
  }

  .big-button::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,215,0,0.3) 0%, rgba(255,165,0,0.1) 50%, rgba(255,140,0,0) 70%);
    transform: scale(0);
    transition: transform 0.6s ease-out;
  }

  .big-button:hover {
    background-color: #FFA500; /* Brighter Orange */
    transform: scale(1.05);
    animation: pulse-glow 1s infinite;
  }

  .big-button:hover::before {
    transform: scale(1);
  }

  .big-button:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(255, 140, 0, 0.5), 0 0 25px rgba(255, 165, 0, 0.7);
  }

  /* Dark mode styles */
  :global(.dark) .big-button {
    background-color: #FFA500; /* Brighter Orange for dark mode */
    color: #1a1a1a; /* Dark text for contrast */
  }

  :global(.dark) .big-button:hover {
    background-color: #FFD700; /* Gold */
  }

  :global(.dark) .big-button {
    animation: pulse-glow-dark 2s infinite;
  }

  :global(.dark) .big-button:hover {
    animation: pulse-glow-dark 1s infinite;
  }

  @keyframes pulse-glow-dark {
    0% {
      box-shadow: 0 0 5px #FFA500, 0 0 10px #FFA500, 0 0 15px #FFA500;
    }
    50% {
      box-shadow: 0 0 10px #FFD700, 0 0 20px #FFD700, 0 0 30px #FFD700;
    }
    100% {
      box-shadow: 0 0 5px #FFA500, 0 0 10px #FFA500, 0 0 15px #FFA500;
    }
  }

  .tagline {
    font-size: 1.2rem;
    color: var(--color-text-secondary);
    margin-bottom: 1rem;
  }

  .pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

  .pricing-option {
    background-color: var(--color-bg-secondary);
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
  }

  .pricing-option.featured {
    border: 2px solid var(--color-accent);
  }

  .price {
    font-size: 2rem;
    font-weight: bold;
    margin: 1rem 0;
  }

  .enroll-button {
    background-color: var(--color-accent);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .enroll-button:hover {
    background-color: var(--color-accent-hover);
  }

  .money-back {
    margin-top: 1rem;
    font-style: italic;
  }

  /* Dark mode styles */
  :global(.dark) .pricing-option {
    background-color: #2a2a2a;
  }

  :global(.dark) .enroll-button {
    background-color: #FFA500;
    color: #1a1a1a;
  }

  :global(.dark) .enroll-button:hover {
    background-color: #FFD700;
  }

  .feature-list {
    list-style-type: none;
    padding: 0;
    margin: 1rem 0;
  }

  .feature-list li {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    font-size: 1.1rem;
  }

  .icon {
    margin-right: 1rem;
    font-size: 1.5rem;
  }
</style>