<script>
  import { fade, fly } from 'svelte/transition';
  import FAQ from '$lib/components/FAQ.svelte';
  import Countdown from '$lib/components/Countdown.svelte';
  import AIThreatMeter from '$lib/components/AIThreatMeter.svelte';
  import StSFreeGuideImage from '$lib/images/StSFreeGuide.png';

  const targetDate = new Date("2027-01-01T00:00:00").getTime(); // Adjust as needed
</script>

<div class="about-container">
  <header>
    <h1 class="title" in:fly="{{ y: -20, duration: 500 }}">About Surviving the Singularity</h1>
    <p class="subtitle" in:fly="{{ y: 20, duration: 500, delay: 200 }}">Navigate the AI Revolution with Confidence</p>
  </header>

  <section class="intro" in:fade="{{ duration: 500, delay: 400 }}">
    <p>The AI revolution isn't coming—it's already here. At Surviving the Singularity, we're not just observing this transformation; we're equipping you to thrive in it.</p>
  </section>

  <section class="why-join" in:fade="{{ duration: 500, delay: 600 }}">
    <h2>Why Join Our AI Mastery Community?</h2>
    <ol>
      <li><strong>Curated, Actionable Insights:</strong> Cut through the noise with our expertly curated content on the latest AI advancements and their real-world applications.</li>
      <li><strong>Practical Implementation Strategies:</strong> Learn how to leverage AI tools and techniques to enhance your career, business, and personal growth.</li>
      <li><strong>Exclusive AI Innovators Network:</strong> Connect with forward-thinking professionals, industry experts, and AI enthusiasts who are shaping the future.</li>
      <li><strong>Weekly Mastery Sessions:</strong> Dive deep into AI concepts, tools, and strategies with our live interactive sessions led by industry experts.</li>
      <li><strong>Personalized Learning Paths:</strong> Whether you're an AI novice or a seasoned pro, our community offers tailored content to accelerate your growth.</li>
      <li><strong>Ethical AI Framework:</strong> Understand the societal impacts of AI and learn how to implement AI responsibly and ethically.</li>
    </ol>
  </section>

  <section class="approach" in:fade="{{ duration: 500, delay: 800 }}">
    <h2>Our Approach: Informed Optimism</h2>
    <p>We believe in embracing AI's potential while maintaining a critical perspective. Our community fosters:</p>
    <ul>
      <li><strong>Curiosity:</strong> We encourage continuous learning and exploration of AI's possibilities.</li>
      <li><strong>Critical Thinking:</strong> We analyze AI developments with a balanced, informed approach.</li>
      <li><strong>Creativity:</strong> We inspire innovative applications of AI across various industries.</li>
      <li><strong>Community:</strong> We support each other in navigating the challenges and opportunities of the AI age.</li>
    </ul>
  </section>

  <section class="survival-kit" in:fade="{{ duration: 500, delay: 1000 }}">
    <h2>Your Singularity Survival Kit</h2>
    <p>Get started with our free guide to navigating the AI revolution</p>
    <div class="kit-items">
      <div class="kit-item">
        <img src={StSFreeGuideImage} alt="Surviving the Singularity Free Guide" />
        <div class="kit-info">
          <h3>Surviving the Singularity: Free Guide</h3>
          <p>Your first step in preparing for the AI-driven future. Download now and start your journey!</p>
          <a href="/download" class="cta-button">Download Free Guide</a>
        </div>
      </div>
    </div>
  </section>

  <AIThreatMeter />

  <section class="join-skool" in:fade="{{ duration: 500, delay: 1200 }}">
    <h2>Join the AI Mastery Guild on Skool</h2>
    <p>Secure your spot in our exclusive community and gain access to:</p>
    <ul>
      <li><strong>Cutting-Edge AI Tools:</strong> Stay ahead with early access to emerging AI technologies.</li>
      <li><strong>Implementation Playbooks:</strong> Step-by-step guides to apply AI in your work and life.</li>
      <li><strong>Expert-Led Workshops:</strong> Learn from AI pioneers and industry leaders.</li>
      <li><strong>Peer Networking:</strong> Collaborate with like-minded individuals on AI projects and ideas.</li>
      <li><strong>Resource Library:</strong> Access our comprehensive collection of AI research, case studies, and tutorials.</li>
    </ul>
  </section>

  <section class="cta" in:fade="{{ duration: 500, delay: 1400 }}">
    <h2>Your AI Future Starts Here</h2>
    <p>Don't just survive the AI revolution—lead it. Join Surviving the Singularity and transform uncertainty into opportunity.</p>
    <a href="/join-skool" class="cta-button">Secure Your Lifetime Membership Now</a>
    <p class="urgency">Limited spots available at current pricing. Invest in your future today!</p>
  </section>

  <FAQ />

  <section class="countdown" in:fade="{{ duration: 500, delay: 1600 }}">
    <h2>Time Left Until the Singularity</h2>
    <Countdown targetDate={targetDate} />
    <p>Don't let AI catch you unprepared.</p>
  </section>
</div>

<style>
  .about-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    font-family: Arial, sans-serif;
  }

  .title {
    font-size: 2.5rem;
    color: var(--color-text-primary);
  }

  .subtitle {
    font-size: 1.2rem;
    color: var(--color-text-secondary);
  }

  section {
    margin-bottom: 3rem;
  }

  h2 {
    font-size: 1.8rem;
    color: var(--color-text-primary);
    margin-bottom: 1rem;
  }

  .intro, .why-join, .approach, .join-skool {
    margin-bottom: 2rem;
  }

  ol, ul {
    padding-left: 1.5rem;
  }

  li {
    margin-bottom: 0.5rem;
  }

  .survival-kit {
    background-color: var(--color-bg-secondary);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 2rem;
  }

  .kit-items {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .kit-item {
    display: flex;
    align-items: center;
    background-color: var(--color-bg-primary);
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .kit-item img {
    width: 150px; /* Adjust as needed */
    height: auto;
    object-fit: cover;
    margin-right: 1rem;
  }

  .kit-info {
    flex-grow: 1;
  }

  .urgency {
    color: var(--color-danger);
    font-weight: bold;
    margin-top: 1rem;
  }

  .cta-button {
    display: inline-block;
    background-color: var(--color-primary);
    color: var(--color-text-on-primary);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: bold;
    transition: background-color 0.3s ease;
    margin-top: 1rem;
    border: none;
    cursor: pointer;
  }

  .cta-button:hover {
    background-color: var(--color-primary-dark);
  }

  /* Dark mode adjustments */
  :global(.dark) {
    --color-text-primary: #ffffff;
    --color-text-secondary: #cccccc;
    --color-bg-primary: #1a1a1a;
    --color-bg-secondary: #2c2c2c;
    --color-border: #444444;
    --color-primary: #4a90e2;
    --color-primary-dark: #3a7bc8;
    --color-text-on-primary: #ffffff;
    --color-danger: #ff6b6b;
  }

  /* Light mode colors */
  :global(:not(.dark)) {
    --color-text-primary: #333333;
    --color-text-secondary: #666666;
    --color-bg-primary: #ffffff;
    --color-bg-secondary: #f0f0f0;
    --color-border: #e0e0e0;
    --color-primary: #3a7bc8;
    --color-primary-dark: #2c5d99;
    --color-text-on-primary: #ffffff;
    --color-danger: #d32f2f;
  }
</style>