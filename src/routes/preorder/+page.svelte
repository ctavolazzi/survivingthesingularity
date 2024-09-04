<script>
  import PreorderButton from '$lib/components/PreorderButton.svelte';
  import CountdownTimer from '$lib/components/CountdownTimer.svelte';
  import BookCoverModal from '$lib/components/BookCoverModal.svelte';
  import { onMount } from 'svelte';
  import coverImage from '$lib/images/Surviving-the-Singularity-Cover.png';
  import welcomeImage from '$lib/images/sts-welcome.png';

  let pageTitle = "Preorder 'Surviving the Singularity'";
  let isModalOpen = false;
  const offerEndDate = new Date('2024-11-08T23:59:59');

  onMount(() => {
      document.title = pageTitle;
  });

  function openModal() {
      isModalOpen = true;
  }

  function closeModal() {
      isModalOpen = false;
  }
</script>

<svelte:head>
  <title>{pageTitle}</title>
  <meta name="description" content="Preorder 'Surviving the Singularity' and prepare for the AI revolution. Secure your future in a world of rapid technological change.">
</svelte:head>

<div class="preorder-page">
  <header class="hero">
    <h1>{pageTitle}</h1>
    <p class="subtitle">Your Essential Guide to Thriving in the AI Revolution</p>
    <div class="cover-image-container">
        <img src={coverImage} alt="Surviving the Singularity Book Cover" class="book-cover" on:click={openModal} />
    </div>
      <div class="hero-cta">
          <div class="preorder-button-wrapper">
              <PreorderButton />
          </div>
          <button class="learn-more" on:click={openModal}>Learn More</button>
      </div>
      <CountdownTimer countdownText="Limited Time Offer Ends In:" endDate={offerEndDate} />
  </header>

  <section class="book-preview">
      <div class="book-details">
          <h2>Unveiling the Future: What's Inside the Book?</h2>
          <p class="order-now-text">In 'Surviving the Singularity', you'll discover:</p>
          <ul>
              <li>The true timeline of AI advancement and its impact on society</li>
              <li>Strategies to future-proof your career in an AI-driven world</li>
              <li>Ethical considerations and how to shape a positive AI future</li>
              <li>Personal development techniques to thrive alongside AI</li>
          </ul>
          <div class="preorder-button-wrapper">
              <PreorderButton />
          </div>
      </div>
  </section>

  <section class="urgency">
      <h2 class="text-center font-bold">Why Act Now?</h2>
      <div class="urgency-points">
          <div class="urgency-point">
              <h3>Beat the AI Curve</h3>
              <p>Stay ahead of the rapid changes in technology and society. Don't get left behind in the AI revolution.</p>
          </div>
          <div class="urgency-point">
              <h3>Limited Time Bonuses</h3>
              <p>Preorder now to receive exclusive content and join a community of forward-thinkers preparing for the future.</p>
          </div>
          <div class="urgency-point">
              <h3>Be Part of the Solution</h3>
              <p>Your preorder supports research and initiatives aimed at ensuring a positive AI future for humanity.</p>
          </div>
      </div>
      <div class="preorder-button-wrapper">
          <PreorderButton />
      </div>
  </section>

  <section class="author-bio">
      <h2 class="text-center">Meet the Author: Your Guide to the AI Revolution</h2>
      <div class="author-content">
          <img src={welcomeImage} alt="Author Name" class="author-image" />
          <div class="author-text">
              <p>With over 20 years of experience in AI and technology, Christopher Tavolazzi brings unparalleled insights into the future of humanity and artificial intelligence. As a renowned futurist and AI ethicist, he has advised Fortune 500 companies and governments on preparing for the technological Singularity.</p>
              <blockquote>"My goal is to empower every reader with the knowledge and tools to not just survive, but thrive in the coming age of superintelligent AI." - Christopher Tavolazzi</blockquote>
          </div>
      </div>
  </section>

  <section class="expert-endorsements">
      <h2 class="text-center">What the Experts Are Saying</h2>
      <div class="endorsements">
          <div class="endorsement">
              <p>"A must-read for anyone concerned about our technological future. Christopher [Tavolazzi] provides a roadmap for humanity in the age of AI."</p>
              <cite>- Dr. Jane Smith, AI Ethics Professor, MIT</cite>
          </div>
          <div class="endorsement">
              <p>"'Surviving the Singularity' is not just a book; it's a survival guide for the 21st century and beyond."</p>
              <cite>- John Doe, CEO of FutureTech Inc.</cite>
          </div>
      </div>
      <div class="preorder-button-wrapper">
          <PreorderButton />
      </div>
  </section>

  <section class="bonus-content">
      <h2 class="text-center">Exclusive Preorder Bonuses</h2>
      <p class="text-center order-now-text">Order now and receive these limited-time bonuses:</p>
      <div class="bonuses">
          <div class="bonus-item">
              <h3>Digital Workbook</h3>
              <p>"Personal AI Readiness Assessment"</p>
          </div>
          <div class="bonus-item">
              <h3>Exclusive Webinar</h3>
              <p>"Q&A with the Author: Your AI Future"</p>
          </div>
          <div class="bonus-item">
              <h3>Early Access</h3>
              <p>"Singularity Survival Community" online forum</p>
          </div>
          <div class="bonus-item">
              <h3>Monthly Newsletter</h3>
              <p>"AI Breakthroughs and Their Implications"</p>
          </div>
      </div>
      <p class="urgency-text order-now-text">These bonuses are only available for a limited time. Don't miss out!</p>
      <div class="preorder-button-wrapper">
          <PreorderButton />
      </div>
  </section>

  <section class="faq">
      <h2 class="text-center">Frequently Asked Questions</h2>
      <div class="faq-items">
          <div class="faq-item">
              <h3>When will the book be released?</h3>
              <p>The book is scheduled for release on [Release Date]. Preorder customers will receive their copies before the official release date.</p>
          </div>
          <div class="faq-item">
              <h3>Is this book for technical or non-technical readers?</h3>
              <p>'Surviving the Singularity' is written for a general audience. While it covers complex topics, it's accessible to anyone interested in the future of AI and its impact on society.</p>
          </div>
          <div class="faq-item">
              <h3>How will I receive the preorder bonuses?</h3>
              <p>Upon completing your preorder, you'll receive an email with instructions on how to access your exclusive bonuses.</p>
          </div>
          <div class="faq-item">
              <h3>Is there a money-back guarantee?</h3>
              <p>Yes, we offer a 30-day money-back guarantee. If you're not satisfied with the book, you can request a full refund within 30 days of the release date.</p>
          </div>
      </div>
  </section>

  <section class="final-cta">
      <h2 class="text-center">Prepare for Tomorrow, Today</h2>
      <p class="text-center final-cta-text">The singularity is approaching faster than we think. Will you be ready? Secure your copy of 'Surviving the Singularity' now and take the first step towards a future where you not only survive but thrive alongside AI.</p>
      <p class="text-center final-cta-text order-now-text">Preorder now and receive these limited-time bonuses:</p>
      <div class="bonuses">
          <div class="bonus-item">
              <h3>Digital Workbook</h3>
              <p>"Personal AI Readiness Assessment"</p>
          </div>
          <div class="bonus-item">
              <h3>Exclusive Webinar</h3>
              <p>"Q&A with the Author: Your AI Future"</p>
          </div>
          <div class="bonus-item">
              <h3>Early Access</h3>
              <p>"Singularity Survival Community" online forum</p>
          </div>
          <div class="bonus-item">
              <h3>Monthly Newsletter</h3>
              <p>"AI Breakthroughs and Their Implications"</p>
          </div>
      </div>
      <p class="urgency-text order-now-text">These bonuses are only available for a limited time. Don't miss out!</p>
      <CountdownTimer countdownText="Preorder Offer Ends In:" endDate={offerEndDate} />
      <div class="preorder-button-wrapper">
          <PreorderButton />
      </div>
    </section>
    <BookCoverModal isOpen={isModalOpen} on:close={closeModal} />
</div>


<style>
  .preorder-page {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem 1rem;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: var(--text-primary);
      background-color: var(--bg-primary);
  }

  .hero {
      text-align: center;
      margin-bottom: 4rem;
  }

  h1 {
      font-size: 3rem;
      margin-bottom: 1rem;
      color: var(--text-accent);
      font-weight: bold;
  }

  .subtitle {
      font-size: 1.5rem;
      margin-bottom: 2rem;
      color: var(--text-secondary);
  }

  .hero-cta {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-bottom: 2rem;
  }

  .learn-more {
      padding: 0.5rem 1rem;
      background-color: var(--bg-secondary);
      color: var(--text-primary);
      border: 2px solid var(--text-accent);
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.3s ease;
  }

  .learn-more:hover {
      background-color: var(--text-accent);
      color: var(--bg-primary);
  }

  section {
      margin-bottom: 4rem;
  }

  h2 {
      font-size: 2rem;
      margin-bottom: 1.5rem;
      color: var(--text-accent);
  }

  .book-preview {
      display: flex;
      align-items: center;
      gap: 2rem;
  }

  .book-cover {
      max-width: 300px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      border-radius: 4px;
      cursor: pointer;
      transition: transform 0.2s ease-in-out;
  }

  .book-cover:hover {
      transform: scale(1.05);
  }

  .book-details ul {
      list-style-type: none;
      padding: 0;
  }

  .book-details li {
      margin-bottom: 0.5rem;
      padding-left: 1.5rem;
      position: relative;
  }

  .book-details li::before {
      content: "✓";
      position: absolute;
      left: 0;
      color: var(--text-accent);
  }

  .urgency-points {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1rem;
  }

  .urgency-point {
      background-color: var(--bg-secondary);
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .urgency-point h3 {
      color: var(--text-accent);
      margin-bottom: 0.25rem;
  }

  .author-image {
      max-width: 100%; /* This allows the image to use its original dimensions */
      height: auto; /* Maintains aspect ratio */
      border-radius: 20px; /* Adds rounded corners */
      border: 4px solid white; /* Adds a white border */
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Optional: adds a subtle shadow */
  }

  .author-content {
      display: flex;
      gap: 2rem;
      align-items: center;
  }

  blockquote {
      font-style: italic;
      border-left: 4px solid var(--text-accent);
      padding-left: 1rem;
      margin-top: 1rem;
  }

  .endorsements {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2rem;
  }

  .endorsement {
      background-color: var(--bg-secondary);
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .endorsement cite {
      display: block;
      margin-top: 1rem;
      font-weight: bold;
  }

  .bonuses {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2rem;
  }

  .bonus-item {
      background-color: var(--bg-secondary);
      padding: 1rem;
      border-radius: 8px;
      text-align: center;
  }

  .bonus-item h3 {
      color: var(--text-accent);
      margin-bottom: 0.5rem;
  }

  .urgency-text {
      font-weight: bold;
      color: var(--text-accent);
      margin-bottom: 1rem;
  }

  .faq-items {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2rem;
  }

  .faq-item {
      background-color: var(--bg-secondary);
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .faq-item h3 {
      color: var(--text-accent);
      margin-bottom: 0.5rem;
  }

  .final-cta {
        text-align: center;
        background-color: var(--bg-secondary);
        padding: 3rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

  .final-cta-text {
      font-size: 1.2rem;
      line-height: 1.6;
      max-width: 800px;
      margin: 1.5rem auto 2rem;
      color: var(--text-secondary);
  }

  .order-now-text {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--text-accent);
        margin: 1rem auto; /* Increased vertical margin */
        padding: 1rem; /* Increased padding */
        text-align: center;
        max-width: 80%; /* Limit width to create horizontal space */
        display: block; /* Ensure it's a block-level element */
    }

  .bonuses {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      justify-content: center;
      font-size: 1.2rem;
      border: 2px solid var(--text-accent);
      border-radius: 8px;
      padding: 1rem;
      margin: 0 auto;
      max-width: 800px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 0 10px var(--text-accent);
      animation: neon-glow 1.5s ease-in-out infinite alternate;
  }

  .bonuses::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(
          circle,
          rgba(var(--text-accent-rgb), 0.1) 0%,
          rgba(var(--text-accent-rgb), 0) 70%
      );
      animation: rotate 6s linear infinite;
  }

  @keyframes neon-glow {
      from {
          box-shadow: 0 0 10px var(--text-accent),
                      0 0 20px var(--text-accent),
                      0 0 30px var(--text-accent);
      }
      to {
          box-shadow: 0 0 20px var(--text-accent),
                      0 0 30px var(--text-accent),
                      0 0 40px var(--text-accent);
      }
  }

  @keyframes rotate {
      0% {
          transform: rotate(0deg);
      }
      100% {
          transform: rotate(360deg);
      }
  }

  .bonus-item {
      flex: 1 1 200px;
      text-align: center;
      padding: 1rem;
      border: 2px solid var(--text-accent);
      border-radius: 8px;
      margin: 0.5rem;
  }

  @media (max-width: 768px) {
      .book-preview, .author-content {
          flex-direction: column;
          text-align: center;
      }

      .book-cover, .author-image {
          margin-bottom: 1rem;
      }

      .hero-cta {
          flex-direction: column;
      }

      h1 {
          font-size: 2.5rem;
      }

      .subtitle {
          font-size: 1.2rem;
      }
  }

  /* Add this new style for the PreorderButton wrapper */
  .preorder-button-wrapper {
      display: flex;
      justify-content: center;
      margin: 2rem 0;
  }

  .cover-image-container {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }

  .book-cover {
    max-width: 300px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
  }
</style>