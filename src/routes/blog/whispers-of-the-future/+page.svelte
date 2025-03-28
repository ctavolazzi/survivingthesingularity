<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import { post } from '$lib/data/blog-posts/whispers-of-the-future/index.js';
  import { marked } from 'marked';
  import { browser } from '$app/environment';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import SocialShare from '$lib/components/SocialShare.svelte';

  const defaultAvatar = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="%23718096" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';

  let htmlContent = marked(post.content);
  let readingTime = '5 min read';
  let scrollProgress = 0;
  let isImageLoaded = false;
  let mounted = false;
  let audio;

  // Audio information (would normally come from post object)
  const audioInfo = {
    src: '/audio/whispers-of-future-reduced.mp3',
    title: 'Listen to the AI Audio Version: Whispers of the Future'
  };

  function handleBackToBlog() {
    window.history.back();
  }

  // Function to safely get avatar URL with fallback
  function getAvatarSrc(post) {
    // During SSR, always return null to prevent any attempts to load images
    if (typeof window === 'undefined' || !browser) {
      return null;
    }

    // Special handling to avoid loading /images/default-avatar.jpg
    if (!post?.authorAvatar || post.authorAvatar === '/images/default-avatar.jpg') {
      return defaultAvatar; // Use our inline SVG data URL
    }

    // Only use actual author avatar if it exists and isn't the default path
    return post.authorAvatar;
  }

  onMount(() => {
    mounted = true;
    // Don't run on the server
    if (typeof window === 'undefined') return;

    const updateScrollProgress = () => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight - windowHeight;
      scrollProgress = (window.scrollY / documentHeight) * 100;
    };

    window.addEventListener('scroll', updateScrollProgress);

    return () => {
      window.removeEventListener('scroll', updateScrollProgress);
    };
  });
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content={post.excerpt || "Exploring the future of AI and technology"} />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content={post.excerpt || "Exploring the future of AI and technology"} />
  <meta property="og:image" content={`https://survivingthesingularity.com/images/blog/whispers-ai-featured.png`} />
  <meta property="og:url" content={`https://survivingthesingularity.com/blog/whispers-of-the-future`} />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={post.title} />
  <meta name="twitter:description" content={post.excerpt || "Exploring the future of AI and technology"} />
  <meta name="twitter:image" content={`https://survivingthesingularity.com/images/blog/whispers-ai-featured.png`} />
</svelte:head>

<div class="progress-bar" style="width: {scrollProgress}%"></div>

<div class="blog-post" in:fade={{ duration: 300, delay: 200 }}>
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <button
        class="back-button mb-4 flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={handleBackToBlog}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{readingTime}</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
      </div>

      <!-- Add SocialShare component -->
      <SocialShare
        title={post.title}
        description={post.excerpt || "Exploring the future of AI and technology"}
        image={post.imageUrl}
      />

      <!-- Audio Player -->
      <div class="audio-player-container mb-6">
        <div class="flex items-center">
          <div class="audio-player-icon mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-headphones">
              <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
              <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
            </svg>
          </div>
          <div class="audio-player-text">
            <p class="text-sm font-medium">{audioInfo.title}</p>
          </div>
        </div>
        <audio
          bind:this={audio}
          src={audioInfo.src}
          controls
          preload="metadata"
          class="w-full mt-2"
        >
          Your browser does not support the audio element.
        </audio>
      </div>
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src="/images/blog/whispers-ai-featured.png"
        alt={post.title}
        class="w-full h-auto transition-opacity duration-300"
        class:opacity-0={!isImageLoaded}
        class:opacity-100={isImageLoaded}
        on:load={() => isImageLoaded = true}
      />
    </div>

    <div class="content">
      {@html htmlContent}
    </div>

    <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-center mb-8">
        <button
          class="back-button flex items-center text-blue-600 dark:text-blue-400 hover:underline"
          on:click={handleBackToBlog}
        >
          <span class="inline-block mr-1">←</span> Back to Blog
        </button>

        <!-- Add SocialShare component at the bottom too -->
        <div class="bottom-share">
          <SocialShare
            title={post.title}
            description={post.excerpt || "Exploring the future of AI and technology"}
            image={post.imageUrl}
          />
        </div>
      </div>

      <NewsletterSignup />
      <Spacer height="2rem" />
      <DiscordButton />
    </div>
  </article>
</div>

<style>
  .blog-post {
    min-height: 100vh;
  }

  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background-color: #3b82f6;
    z-index: 100;
    transition: width 0.1s ease-out;
  }

  .featured-image-container {
    max-height: 500px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background-color: rgba(15, 23, 42, 0.05);
    border-radius: 0.5rem;
    margin-bottom: 2rem;
  }

  .featured-image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    border-radius: 0.5rem;
  }

  .content :global(img) {
    max-width: 100%;
    height: auto;
    border-radius: 0.375rem;
    margin: 1.5rem 0;
  }

  .content :global(blockquote) {
    border-left: 4px solid #3b82f6;
    padding-left: 1rem;
    font-style: italic;
    color: #4b5563;
  }

  .content :global(pre) {
    background-color: #1e293b;
    padding: 1rem;
    border-radius: 0.375rem;
    overflow-x: auto;
  }

  .content :global(code) {
    font-family: monospace;
  }

  .content :global(a) {
    color: #3b82f6;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .content :global(a:hover) {
    color: #2563eb;
    text-decoration: underline;
  }

  .bottom-share :global(.share-container) {
    margin: 0;
  }

  @media (max-width: 640px) {
    .bottom-share {
      display: none; /* Hide bottom share on mobile to save space */
    }
  }

  /* Audio player styling */
  .audio-player-container {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: rgba(241, 245, 249, 0.5);
    margin-bottom: 1rem;
    border: 1px solid rgba(203, 213, 225, 0.5);
  }

  :global(.dark) .audio-player-container {
    background-color: rgba(30, 41, 59, 0.5);
    border-color: rgba(51, 65, 85, 0.5);
  }

  .audio-player-icon {
    color: var(--color-primary, #3b82f6);
  }

  .audio-player-text {
    color: var(--color-text-primary);
  }

  audio {
    width: 100%;
    height: 36px;
  }

  audio::-webkit-media-controls-panel {
    background-color: rgba(241, 245, 249, 0.8);
  }

  :global(.dark) audio::-webkit-media-controls-panel {
    background-color: rgba(30, 41, 59, 0.8);
  }
</style>