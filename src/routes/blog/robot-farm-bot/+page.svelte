<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import RecommendedContent from '$lib/components/RecommendedContent.svelte';

  const post = {
    title: 'Robot Farm Bot - The Future of Residential Agriculture',
    date: '2024-08-15',
    author: 'Christopher Tavolazzi',
    image: 'https://farm.bot/cdn/shop/files/FarmBot_Genesis_v1-3_c10ecd67-00ed-4ae1-a32e-111f11312655_2049x1365.jpg?v=1697756943',
    readingTime: '7 min read'
  };

  // Recommended videos related to agriculture, robotics, and sustainability
  const recommendedVideos = [
    {
      id: "YLo7EH2zsW0",
      title: "AI Plays Minecraft: Voyager - An Open-Ended Embodied Agent with Large Language Models"
    },
    {
      id: "U1tQbD25dGY",
      title: "Futurist: How AI and Robotics Will Reshape Our Economy"
    },
    {
      id: "GYBT66bPfu8",
      title: "Is the Gaming Industry Doomed?: Google's AI Generates Playable DOOM in Real-Time"
    }
  ];

  let isImageLoaded = false;
  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

<div class="blog-post" in:fade={{ duration: 300, delay: 200 }}>
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{post.readingTime}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">By {post.author}</span>
        <button
          class="inline-flex items-center text-primary dark:text-primary-dark text-sm hover:text-primary-dark dark:hover:text-primary-hover-dark transition-colors ml-auto"
          on:click={() => {
            if (navigator.share) {
              navigator.share({
                title: post.title,
                text: "Imagine a world where your backyard vegetable garden is tended by an AI-powered robot, ensuring a bountiful harvest with minimal effort.",
                url: window.location.href,
              }).catch(err => console.error('Error sharing:', err));
            } else {
              navigator.clipboard.writeText(window.location.href)
                .then(() => alert('Link copied to clipboard!'))
                .catch(err => console.error('Failed to copy:', err));
            }
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1">
            <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
            <polyline points="16 6 12 2 8 6"></polyline>
            <line x1="12" y1="2" x2="12" y2="15"></line>
          </svg>
          Share
        </button>
      </div>
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src={post.image}
        alt={post.title}
        class="w-full h-auto transition-opacity duration-300"
        class:opacity-0={!isImageLoaded}
        class:opacity-100={isImageLoaded}
        on:load={() => isImageLoaded = true}
      />
    </div>

    <div class="content">
      <p class="lead">
        Imagine a world where your backyard vegetable garden is tended by an AI-powered robot,
        ensuring a bountiful harvest with minimal effort. Welcome to the era of the Robot Farm Bot.
      </p>

      <h2>Revolutionizing Home Gardening</h2>
      <p>
        The Robot Farm Bot represents a groundbreaking advancement in residential agriculture,
        combining precision farming techniques with artificial intelligence to create an
        automated gardening system that anyone can use. This innovative technology is transforming
        how we think about growing food at home.
      </p>

      <h2>Key Features</h2>
      <ul>
        <li>Automated planting, watering, and weeding</li>
        <li>AI-powered plant monitoring and care</li>
        <li>Precision nutrient delivery systems</li>
        <li>Mobile app control and monitoring</li>
        <li>Weather-adaptive scheduling</li>
      </ul>

      <h2>How It Works</h2>
      <p>
        The Robot Farm Bot operates on a precision CNC system, moving along X, Y, and Z axes to
        access every part of your garden. Using an array of sensors and tools, it can:
      </p>
      <ul>
        <li>Plant seeds at optimal depth and spacing</li>
        <li>Monitor soil moisture and nutrient levels</li>
        <li>Identify and remove weeds</li>
        <li>Water plants with precision</li>
        <li>Track plant growth and health</li>
      </ul>

      <blockquote>
        "The Robot Farm Bot is not just a gardening tool; it's a complete agricultural
        solution that brings commercial farming technology to your backyard."
        - Agricultural Technology Review
      </blockquote>

      <h2>Benefits for Home Gardeners</h2>
      <p>
        This revolutionary system offers numerous advantages for home gardeners:
      </p>
      <ul>
        <li>Reduced time and effort in garden maintenance</li>
        <li>Increased crop yields through precision care</li>
        <li>Year-round growing capabilities</li>
        <li>Data-driven plant care decisions</li>
        <li>Sustainable water and resource usage</li>
      </ul>

      <h2>The Future of Home Growing</h2>
      <p>
        As we move towards a more sustainable future, technologies like the Robot Farm Bot
        will play a crucial role in enabling people to grow their own food efficiently and
        sustainably. This is just the beginning of a new era in residential agriculture,
        where technology and nature work together to create abundant home gardens.
      </p>
    </div>
  </article>

  <Spacer height="2rem" />

  <div class="recommended-content-section">
    <RecommendedContent
      title="Explore More Technology Content"
      description="Check out these videos about AI, robotics, and future technologies"
      videos={recommendedVideos}
    />
  </div>

  <Spacer height="2rem" />

  <div class="newsletter-section">
    <NewsletterSignup />
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
    max-height: 500px;
    overflow: hidden;
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
  }

  .content {
    font-size: 1.125rem;
    line-height: 1.75;
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
</style>