<script>
  import { onMount } from 'svelte';
  import NewsletterSignup from './NewsletterSignup.svelte';
  import DiscordButton from './DiscordButton.svelte';
  import SocialShare from './SocialShare.svelte';
  import Spacer from './Spacer.svelte';
  import RecommendedContent from './RecommendedContent.svelte';
  import MysteryBoxAd from '$lib/components/ads/MysteryBoxAd.svelte';

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

  let audio;
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content={post.description} />
</svelte:head>

<div class="blog-post">
  <article class="prose prose-lg dark:prose-invert mx-auto px-3 sm:px-4 py-6 max-w-3xl">
    <header class="mb-6">
      <h1 class="text-3xl sm:text-4xl font-bold mb-3">{post.title}</h1>
      <div class="flex flex-wrap items-center text-sm text-gray-600 dark:text-gray-400 mb-3">
        <span class="mr-3">{post.date}</span>
        <span class="mr-3">·</span>
        <span class="mr-3">{post.readingTime}</span>
        <span class="mr-3">·</span>
        <span class="mr-3">By {post.author}</span>
        <button
          class="inline-flex items-center text-primary dark:text-primary-dark text-sm hover:text-primary-dark dark:hover:text-primary-hover-dark transition-colors ml-auto"
          on:click={() => {
            if (navigator.share) {
              navigator.share({
                title: post.title,
                text: post.description,
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
      <div class="featured-image-container mb-6 rounded-lg overflow-hidden">
        <img
          src={post.image}
          alt={post.title}
          class="w-full h-auto"
          loading="lazy"
          decoding="async"
        />
      </div>
    {/if}

    <!-- Post content -->
    <slot></slot>

    <!-- Author bio or other info -->
    <div class="author-bio mt-6 p-3 bg-gray-50 dark:bg-gray-800 rounded border-l-4 border-primary dark:border-primary-dark text-sm">
      <p class="italic">
        <em>{post.author} is the founder of AIECO, specializing in AI/ML and R&D. He is also the author of "Surviving the Singularity," a blog and book dedicated to navigating the future of artificial intelligence.</em>
      </p>
    </div>
  </article>

  <Spacer height="2rem" />

  <div class="recommended-content-section">
    <RecommendedContent
      title="Explore More AI Content"
      description="Check out these videos about AI and the future of technology"
      videos={recommendedVideos}
    />
  </div>

  <Spacer height="2rem" />

  <div class="blog-closing max-w-3xl mx-auto px-3 sm:px-4 py-4">
    <DiscordButton />
    <NewsletterSignup />

    <div class="mystery-box-wrapper">
      <a href="https://treasuretavernhq.myshopify.com/products/%F0%9F%91%89-mood-booster-mystery-box-classic-monthly-surprises-indie-finds" class="mystery-box-link" aria-label="Subscribe to Mood Booster Mystery Box">
        <MysteryBoxAd
          title="Mood Booster Mystery Box"
          subtitle="Monthly Surprises"
          description="Discover curated indie treasures delivered monthly to your door. Each box contains 5-7 handpicked items designed to boost your mood and bring joy to your everyday life."
          price="24.99"
          frequency="month"
          ctaText="Subscribe Now"
          ctaUrl="https://treasuretavernhq.myshopify.com/products/%F0%9F%91%89-mood-booster-mystery-box-classic-monthly-surprises-indie-finds"
          badgeText="Most Popular"
          itemCount="5-7 items"
        />
      </a>
    </div>
  </div>
</div>

<style>
  .share-top-container {
    margin: 1.5rem 0;
  }

  .blog-closing {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--color-border, #e2e8f0);
  }

  .mystery-box-wrapper {
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
</style>