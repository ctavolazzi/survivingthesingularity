<script>
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import RecommendedContent from '$lib/components/RecommendedContent.svelte';
  import SocialShare from '$lib/components/SocialShare.svelte';

  const post = {
    title: 'Farm Bot Deep Dive - Exploring AI-Powered Precision Agriculture',
    date: '2024-08-24',
    author: 'Christopher Tavolazzi',
    image: 'https://www.open-electronics.org/wp-content/uploads/2013/10/FarmBot-Genesis-Homepage-Image.jpg',
    readingTime: '8 min read',
    description: "Dive deep into the world of FarmBot, a revolutionary CNC automated, AI-powered system that's transforming backyard gardening and small-scale agriculture with precision and efficiency."
  };

  // Recommended videos related to agriculture, robots, and sustainability
  const recommendedVideos = [
    {
      id: "GYBT66bPfu8",
      title: "Is the Gaming Industry Doomed?: Google's AI Generates Playable DOOM in Real-Time"
    },
    {
      id: "U1tQbD25dGY",
      title: "Futurist: How AI and Robotics Will Reshape Our Economy"
    },
    {
      id: "YLo7EH2zsW0",
      title: "AI Plays Minecraft: Voyager - An Open-Ended Embodied Agent with Large Language Models"
    }
  ];
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content={post.description} />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content={post.description} />
  <meta property="og:image" content={post.image} />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="blog-post">
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <button
        class="back-button mb-4 flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={() => window.history.back()}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{post.readingTime}</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
      </div>

      <!-- Add SocialShare component -->
      <SocialShare
        title={post.title}
        description={post.description}
        image={post.image}
      />
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src={post.image}
        alt={post.title}
        class="w-full h-auto"
        loading="lazy"
        decoding="async"
      />
    </div>

    <div class="content">
      <p class="lead">
        Dive deep into the world of FarmBot, a revolutionary CNC automated, AI-powered system that's
        transforming backyard gardening and small-scale agriculture with precision and efficiency.
      </p>

      <h2>The Technology Behind FarmBot</h2>
      <p>
        FarmBot combines precision CNC machinery with sophisticated AI algorithms to create a
        comprehensive automated farming solution. At its core, it's a robotic system that can
        handle virtually every aspect of plant care with remarkable precision.
      </p>

      <h2>Core Components</h2>
      <ul>
        <li>CNC-guided positioning system for precise tool movement</li>
        <li>Interchangeable tool heads for different tasks</li>
        <li>AI-powered plant recognition and monitoring</li>
        <li>Automated watering and nutrient delivery systems</li>
        <li>Environmental sensors and weather monitoring</li>
      </ul>

      <h2>AI and Machine Learning Integration</h2>
      <p>
        The FarmBot system leverages advanced AI capabilities in several key areas:
      </p>
      <ul>
        <li>Computer vision for plant identification and health monitoring</li>
        <li>Machine learning for optimal growing conditions</li>
        <li>Predictive analytics for harvest timing</li>
        <li>Automated pest and disease detection</li>
      </ul>

      <blockquote>
        "FarmBot represents the perfect fusion of traditional farming knowledge with cutting-edge
        technology, making precision agriculture accessible to everyone." - Agricultural Innovation Review
      </blockquote>

      <h2>Precision Agriculture Features</h2>
      <p>
        The system's precision capabilities include:
      </p>
      <ul>
        <li>Sub-millimeter positioning accuracy</li>
        <li>Individual plant care customization</li>
        <li>Optimized resource utilization</li>
        <li>Real-time growth tracking and analysis</li>
        <li>Automated crop rotation planning</li>
      </ul>

      <h2>Data-Driven Farming</h2>
      <p>
        FarmBot's approach to agriculture is fundamentally data-driven, collecting and analyzing
        information about:
      </p>
      <ul>
        <li>Soil conditions and nutrient levels</li>
        <li>Plant growth rates and health metrics</li>
        <li>Water usage and efficiency</li>
        <li>Environmental conditions and their impact</li>
      </ul>

      <h2>Future Developments</h2>
      <p>
        As FarmBot technology continues to evolve, we can expect to see even more advanced features
        and capabilities, including enhanced AI decision-making, improved efficiency, and greater
        integration with other smart home and agricultural systems. This is truly just the beginning
        of the precision agriculture revolution.
      </p>
    </div>
  </article>

  <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700 max-w-4xl mx-auto px-4">
    <div class="flex justify-between items-center mb-8">
      <button
        class="back-button flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={() => window.history.back()}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>

      <!-- Add SocialShare component at the bottom too -->
      <div class="bottom-share">
        <SocialShare
          title={post.title}
          description={post.description}
          image={post.image}
        />
      </div>
    </div>

    <div class="recommended-content-section mb-8">
      <RecommendedContent
        title="Explore More Technology Content"
        description="Check out these videos about AI, robotics, and future technologies"
        videos={recommendedVideos}
      />
    </div>

    <NewsletterSignup />
    <Spacer height="2rem" />
    <DiscordButton />
  </div>
</div>

<style>
  .blog-post {
    min-height: 100vh;
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
  }

  .featured-image-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 0.5rem;
    background-color: rgba(15, 23, 42, 0.05);
    margin-bottom: 2rem;
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
    max-height: 80vh;
    border-radius: 0.5rem;
  }

  .content {
    font-size: 1.125rem;
    line-height: 1.75;
  }

  .content h2 {
    color: #ff7708;
    font-weight: bold;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
  }

  .lead {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-bottom: 2rem;
  }

  blockquote {
    border-left: 4px solid var(--color-primary);
    padding-left: 1rem;
    margin: 2rem 0;
    font-style: italic;
    color: var(--color-text-secondary);
  }

  .newsletter-section {
    max-width: 4xl;
    margin: 0 auto;
    padding: 0 1rem;
  }

  /* Dark mode adjustments */
  :global(.dark) .blog-post {
    background-color: var(--color-bg-primary-dark);
    color: var(--color-text-primary-dark);
  }

  .bottom-share :global(.share-container) {
    margin: 0;
  }

  @media (max-width: 640px) {
    .bottom-share {
      display: none; /* Hide bottom share on mobile to save space */
    }
  }

  .back-button {
    display: inline-flex;
    align-items: center;
    transition: all 0.2s ease;
  }

  .back-button:hover {
    transform: translateX(-2px);
  }
</style>