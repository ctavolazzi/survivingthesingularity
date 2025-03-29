<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import { browser } from '$app/environment';
  import NewsletterSignup from './NewsletterSignup.svelte';
  import DiscordButton from './DiscordButton.svelte';
  import SocialShare from './SocialShare.svelte';
  import Spacer from './Spacer.svelte';
  import RecommendedContent from './RecommendedContent.svelte';
  import MysteryBoxAd from '$lib/components/ads/MysteryBoxAd.svelte';
  import TreasureTavernAd from '$lib/components/ads/TreasureTavernAd.svelte';

  export let post = {
    title: '',
    date: '',
    author: '',
    image: '',
    readingTime: '',
    description: '',
    audioSrc: '',
    audioTitle: ''
  };

  // Options to customize the template
  export let options = {
    showBackButton: true,
    showProgressBar: false,
    showAds: true,
    showAuthorBio: true,
    showShareBottom: true,
    showMysteryBox: false,
    showTreasureTavern: true,
    fadeInContent: true,
    borderOnFeaturedImage: false,
    showFaq: false
  };

  // Default recommended videos - can be overridden by the page using this template
  export let recommendedVideos = [
    {
      id: "PNqwvJCz_2w",
      title: "Game Over? Voice Actors vs AI"
    },
    {
      id: "GYBT66bPfu8",
      title: "Is the Gaming Industry Doomed?: Google's AI Generates Playable DOOM in Real-Time"
    },
    {
      id: "YLo7EH2zsW0",
      title: "AI Plays Minecraft: Voyager - An Open-Ended Embodied Agent with Large Language Models"
    }
  ];

  // FAQ data - can be provided by the page using this template
  export let faqItems = [];
  let expandedFaqs = [];

  // Toggle FAQ item open/closed
  function toggleFaq(index) {
    expandedFaqs[index] = !expandedFaqs[index];
    expandedFaqs = [...expandedFaqs]; // Trigger reactivity
  }

  // Reading progress (optional)
  let readingProgress = 0;
  let audio;
  let mounted = false;

  function handleBackToBlog() {
    window.history.back();
  }

  onMount(() => {
    mounted = true;

    // Initialize expandedFaqs with the first item open if there are any FAQs
    if (faqItems.length > 0) {
      expandedFaqs = Array(faqItems.length).fill(false);
      expandedFaqs[0] = true; // First one open by default
    }

    if (options.showProgressBar && browser) {
      const updateReadingProgress = () => {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight - windowHeight;
        readingProgress = (window.scrollY / documentHeight) * 100;
      };

      window.addEventListener('scroll', updateReadingProgress);
      return () => window.removeEventListener('scroll', updateReadingProgress);
    }
  });
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content={post.description} />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content={post.description} />
  <meta property="og:image" content={post.image} />
  <meta property="og:url" content={`https://survivingthesingularity.com/blog/${post.slug || ''}`} />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={post.title} />
  <meta name="twitter:description" content={post.description} />
  <meta name="twitter:image" content={post.image} />
</svelte:head>

{#if options.showProgressBar}
  <!-- Reading Progress Bar -->
  <div class="fixed top-0 left-0 w-full h-1 bg-gray-200 dark:bg-gray-700 z-50">
    <div
      class="h-full bg-primary dark:bg-primary-dark transition-all duration-300"
      style="width: {readingProgress}%">
    </div>
  </div>
{/if}

<div class="blog-post" in:fade|local={{ duration: 300, delay: 200 }}>
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      {#if options.showBackButton}
        <button
          class="back-button mb-4 flex items-center text-blue-600 dark:text-blue-400 hover:underline"
          on:click={handleBackToBlog}
        >
          <span class="inline-block mr-1">←</span> Back to Blog
        </button>
      {/if}

      <h1 class="blog-post-title text-3xl md:text-4xl lg:text-5xl font-bold mb-4">{post.title}</h1>
      <div class="flex flex-wrap items-center text-sm md:text-base text-gray-600 dark:text-gray-400 gap-2 mb-4">
        <span>{post.date}</span>
        <span class="hidden md:inline">·</span>
        <span>{post.readingTime}</span>
        <span class="hidden md:inline">·</span>
        <span>By {post.author}</span>
      </div>

      <!-- Social Share at the top -->
      <div class="share-top-container">
        <SocialShare
          title={post.title}
          description={post.description}
          image={post.image}
        />
      </div>

      {#if post.audioSrc && post.audioTitle}
        <div class="audio-player-container mb-6">
          <div class="flex items-center">
            <div class="audio-player-icon mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-headphones">
                <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
                <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
              </svg>
            </div>
            <div class="audio-player-text">
              <p class="text-sm font-medium">{post.audioTitle}</p>
            </div>
          </div>
          <audio
            bind:this={audio}
            src={post.audioSrc}
            controls
            preload="metadata"
            class="w-full mt-2"
          >
            Your browser does not support the audio element.
          </audio>
        </div>
      {/if}
    </header>

    {#if post.image}
      <div class="featured-image-container mb-8 rounded-lg overflow-hidden" class:shadow-xl={options.borderOnFeaturedImage}>
        <!-- Check if custom image is provided through a slot -->
        <slot name="featured-image">
          <!-- Default image implementation -->
          <img
            src={post.image}
            alt={post.title}
            class="w-full h-auto transform hover:scale-105 transition-transform duration-500"
            loading="lazy"
            decoding="async"
          />
        </slot>
      </div>
    {/if}

    <!-- FAQ Section -->
    {#if options.showFaq && faqItems.length > 0}
      <div class="faq-section mb-8">
        <h2 class="text-2xl font-bold mb-6">Frequently Asked Questions</h2>

        <div class="space-y-3">
          {#each faqItems as faq, index}
            <div class="faq-item">
              <button
                class="faq-button"
                class:expanded={expandedFaqs[index]}
                on:click={() => toggleFaq(index)}
                aria-expanded={expandedFaqs[index]}
              >
                <span class="question">{faq.question}</span>
                <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>
              {#if expandedFaqs[index]}
                <div class="faq-content" transition:fade={{ duration: 150 }}>
                  <p>{faq.answer}</p>
                </div>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Post content -->
    <div class="content">
      <p class="lead">
        {post.description || ""}
      </p>

      <slot></slot>
    </div>

    <!-- Author bio or other info -->
    {#if options.showAuthorBio}
      <div class="author-bio mt-6 p-3 bg-gray-50 dark:bg-gray-800 rounded border-l-4 border-primary dark:border-primary-dark text-sm">
        <p class="italic">
          <em>{post.author} is the founder of AIECO, specializing in AI/ML and R&D. He is also the author of "Surviving the Singularity," a blog and book dedicated to navigating the future of artificial intelligence.</em>
        </p>
      </div>
    {/if}
  </article>

  <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700 max-w-4xl mx-auto px-4">
    {#if options.showShareBottom}
      <div class="flex justify-between items-center mb-8">
        {#if options.showBackButton}
          <button
            class="back-button flex items-center text-blue-600 dark:text-blue-400 hover:underline"
            on:click={handleBackToBlog}
          >
            <span class="inline-block mr-1">←</span> Back to Blog
          </button>
        {/if}

        <!-- Bottom share section -->
        <div class="bottom-share">
          <SocialShare
            title={post.title}
            description={post.description}
            image={post.image}
          />
        </div>
      </div>
    {/if}

    <!-- Recommended content section -->
    <div class="recommended-content-section mb-8">
      <RecommendedContent
        title="Explore More AI Content"
        description="Check out these videos about AI and the future of technology"
        videos={recommendedVideos}
      />
    </div>

    <!-- Newsletter and Discord -->
    <NewsletterSignup />
    <Spacer height="2rem" />
    <DiscordButton />

    <!-- Ads section -->
    {#if options.showAds}
      <div class="ads-wrapper mt-8">
        {#if options.showMysteryBox}
          <a href="https://treasuretavernhq.com/products/%F0%9F%91%89-mood-booster-mystery-box-classic-monthly-surprises-indie-finds" class="mystery-box-link" aria-label="Subscribe to Mood Booster Mystery Box">
            <MysteryBoxAd
              title="Mood Booster Mystery Box"
              subtitle="Monthly Surprises"
              description="Discover curated indie treasures delivered monthly to your door. Each box contains 5-7 handpicked items designed to boost your mood and bring joy to your everyday life."
              price="24.99"
              frequency="month"
              ctaText="Subscribe Now"
              ctaUrl="https://treasuretavernhq.com/products/%F0%9F%91%89-mood-booster-mystery-box-classic-monthly-surprises-indie-finds"
              badgeText="Most Popular"
              itemCount="5-7 items"
            />
          </a>
        {/if}

        {#if options.showTreasureTavern}
          <div class="mt-8">
            <TreasureTavernAd
              title="Discover Treasure Tavern"
              subtitle="Curated Joy, Delivered Monthly"
              description="Join thousands discovering unique, handpicked treasures every month. From self-care items to quirky finds, each box is designed to brighten your day."
              bulletPoints={[
                "5-7 Handpicked items monthly",
                "Supports small & indie businesses",
                "Flexible subscription options",
                "Free shipping in the United States"
              ]}
              ctaText="Shop Now"
              ctaUrl="https://treasuretavernhq.com/"
              badgeText="Community Favorite"
            />
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .blog-post {
    min-height: 100vh;
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
  }

  .blog-post-title {
    white-space: normal;
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: none;
    -webkit-hyphens: none;
    -ms-hyphens: none;
    font-size: clamp(1.75rem, 4vw, 2.5rem);
  }

  @media (max-width: 480px) {
    .blog-post-title {
      font-size: clamp(1.5rem, 3.5vw, 1.75rem);
    }
  }

  @media (max-width: 350px) {
    .blog-post-title {
      font-size: clamp(1.35rem, 3vw, 1.5rem);
    }
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
    max-height: 80vh; /* Limit height on large screens */
    border-radius: 0.5rem;
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

  .share-top-container {
    margin: 1.5rem 0;
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

  /* Audio player styling */
  .audio-player-container {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: var(--color-bg-secondary, #f3f4f6);
    margin-bottom: 1rem;
  }

  :global(.dark) .audio-player-container {
    background-color: var(--color-bg-secondary-dark, #374151);
  }

  .audio-player-icon {
    color: var(--color-primary, #f97316);
  }

  .ads-wrapper {
    margin-top: 2.5rem;
  }

  .mystery-box-link {
    display: block;
    text-decoration: none;
    color: inherit;
  }

  /* Ensure the link doesn't show the default purple outline when clicked */
  .mystery-box-link:focus {
    outline: none;
  }

  /* Add a subtle hover effect to indicate the whole component is clickable */
  .mystery-box-link:hover {
    transform: translateY(-2px);
    transition: transform 0.3s ease;
  }

  /* Global styles for content */
  :global(.content h2) {
    color: #ff7708;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-weight: bold;
    font-size: 1.875rem;
  }

  :global(.content h3) {
    color: #ff7708;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-weight: bold;
    font-size: 1.5rem;
  }

  :global(.content p) {
    margin-bottom: 1rem;
    line-height: 1.625;
    color: var(--color-text-secondary);
  }

  :global(.content ul), :global(.content ol) {
    padding-left: 1.5em;
    margin-left: 0;
    margin-bottom: 1.5rem;
  }

  :global(.content li) {
    margin-bottom: 0.5em;
    color: var(--color-text-secondary);
  }

  :global(.content ul) {
    list-style-type: disc;
  }

  :global(.content ol) {
    list-style-type: decimal;
  }

  :global(.content a) {
    color: #3b82f6;
    text-decoration: underline;
  }

  :global(.content a:hover) {
    color: #2563eb;
  }

  :global(.content blockquote) {
    border-left: 4px solid var(--color-primary);
    padding-left: 1rem;
    margin: 2rem 0;
    font-style: italic;
    color: var(--color-text-secondary);
  }

  /* FAQ section styling */
  .faq-section {
    margin-bottom: 3rem;
  }

  .faq-item {
    border-bottom: 1px solid rgba(203, 213, 225, 0.3);
    margin-bottom: 0.5rem;
  }

  .faq-item:last-child {
    border-bottom: none;
  }

  .faq-button {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1rem 0;
    text-align: left;
    font-weight: 600;
    font-size: 1.05rem;
    color: var(--color-text-primary);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .faq-button:hover {
    color: var(--color-primary, #3b82f6);
  }

  .question {
    flex: 1;
    padding-right: 1rem;
    line-height: 1.4;
  }

  .chevron {
    margin-top: 0.25rem;
    min-width: 20px;
    transition: transform 0.2s ease;
    color: var(--color-primary, #3b82f6);
  }

  .faq-button.expanded .chevron {
    transform: rotate(180deg);
  }

  .faq-content {
    padding: 0 0 1.25rem;
    line-height: 1.6;
    color: var(--color-text-secondary, #4b5563);
  }

  @media (max-width: 640px) {
    .faq-button {
      font-size: 1rem;
      padding: 0.75rem 0;
    }

    .faq-content {
      padding: 0 0 1rem;
      font-size: 0.95rem;
    }
  }
</style>