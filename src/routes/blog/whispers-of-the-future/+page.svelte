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

  let htmlContent = marked(post.content);
  let readingTime = '5 min read';
  let scrollProgress = 0;
  let isImageLoaded = false;
  let mounted = false;

  function handleBackToBlog() {
    window.history.back();
  }

  onMount(() => {
    mounted = true;
    if (typeof window === 'undefined') return;

    // Debug: Log the image URL to console
    console.log('Image URL:', post.imageUrl);

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

<div class="progress-bar" style="width: {scrollProgress}%"></div>

<div class="blog-post" in:fade={{ duration: 300, delay: 200 }}>
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{readingTime}</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
      </div>

      <SocialShare
        title={post.title}
        description={post.excerpt}
        image={post.imageUrl}
      />
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src={post.imageUrl}
        alt={post.title}
        class="w-full h-auto transition-opacity duration-300"
        class:opacity-0={!isImageLoaded}
        class:opacity-100={isImageLoaded}
        on:load={() => {
          console.log('Image loaded successfully');
          isImageLoaded = true;
        }}
        on:error={(e) => {
          console.error('Image failed to load:', e);
          console.error('Image path:', post.imageUrl);
        }}
      />
    </div>

    <div class="content">
      {@html htmlContent}
    </div>
  </article>

  <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700 max-w-4xl mx-auto px-4">
    <div class="flex justify-between items-center mb-8">
      <button
        class="back-button flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={handleBackToBlog}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>

      <SocialShare
        title={post.title}
        description={post.excerpt}
        image={post.imageUrl}
      />
    </div>

    <NewsletterSignup />
    <Spacer height="2rem" />
    <DiscordButton />
  </div>
</div>

<style>
  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    z-index: 100;
    transition: width 0.1s;
  }

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
    transition: opacity 0.3s ease;
  }
</style>