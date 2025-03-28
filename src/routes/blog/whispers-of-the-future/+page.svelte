<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import { post } from '$lib/data/blog-posts/whispers-of-the-future/index.js';
  import { marked } from 'marked';
  import { browser } from '$app/environment';
  import DiscordButton from '$lib/components/DiscordButton.svelte';

  const defaultAvatar = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="%23718096" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';

  let htmlContent = marked(post.content);
  let readingTime = '4 min read'; // Estimated reading time
  let scrollProgress = 0;
  let isProcessingClick = false;
  let lastClickTime = 0;
  let isImageLoaded = false;
  let mounted = false;

  function handleBackToBlog() {
    window.history.back();
  }

  // Debounce helper for share button clicks
  function debounceClick(callback) {
    return (event) => {
      // Don't process during SSR
      if (!browser || typeof window === 'undefined') return;

      const now = Date.now();
      if (now - lastClickTime < 500 || isProcessingClick) {
        event.preventDefault();
        event.stopPropagation();
        return;
      }

      isProcessingClick = true;
      lastClickTime = now;

      try {
        callback();
      } catch (error) {
        console.error('Share error:', error);
      } finally {
        setTimeout(() => {
          isProcessingClick = false;
        }, 200);
      }
    };
  }

  // Share functions
  const shareOnTwitter = debounceClick(() => {
    if (typeof window !== 'undefined') {
      const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(window.location.href)}`;
      window.open(url, '_blank');
    }
  });

  const shareOnLinkedIn = debounceClick(() => {
    if (typeof window !== 'undefined') {
      const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`;
      window.open(url, '_blank');
    }
  });

  const copyLink = debounceClick(() => {
    if (typeof window !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href)
        .then(() => {
          // Could show a toast or notification here
          alert('Link copied to clipboard');
        })
        .catch(err => {
          console.error('Could not copy link: ', err);
        });
    }
  });

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
      <div class="share-buttons flex space-x-2">
        <button
          class="share-button twitter p-2 rounded-full bg-blue-500 hover:bg-blue-600 text-white"
          title="Share on Twitter"
          on:click={shareOnTwitter}
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M22 4.01c-1 .49-1.98.689-3 .99-1.121-1.265-2.783-1.335-4.38-.737S11.977 6.323 12 8v1c-3.245.083-6.135-1.395-8-4 0 0-4.182 7.433 4 11-1.872 1.247-3.739 2.088-6 2 3.308 1.803 6.913 2.423 10.034 1.517 3.58-1.04 6.522-3.723 7.651-7.742a13.84 13.84 0 0 0 .497-3.753C20.18 7.773 21.692 5.25 22 4.009z"></path></svg>
        </button>
        <button
          class="share-button linkedin p-2 rounded-full bg-blue-700 hover:bg-blue-800 text-white"
          title="Share on LinkedIn"
          on:click={shareOnLinkedIn}
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
        </button>
        <button
          class="share-button copy p-2 rounded-full bg-gray-500 hover:bg-gray-600 text-white"
          title="Copy Link"
          on:click={copyLink}
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        </button>
      </div>
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src={post.imageUrl}
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
        <div class="share-buttons flex space-x-2">
          <button
            class="share-button twitter p-2 rounded-full bg-blue-500 hover:bg-blue-600 text-white"
            title="Share on Twitter"
            on:click={shareOnTwitter}
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M22 4.01c-1 .49-1.98.689-3 .99-1.121-1.265-2.783-1.335-4.38-.737S11.977 6.323 12 8v1c-3.245.083-6.135-1.395-8-4 0 0-4.182 7.433 4 11-1.872 1.247-3.739 2.088-6 2 3.308 1.803 6.913 2.423 10.034 1.517 3.58-1.04 6.522-3.723 7.651-7.742a13.84 13.84 0 0 0 .497-3.753C20.18 7.773 21.692 5.25 22 4.009z"></path></svg>
          </button>
          <button
            class="share-button linkedin p-2 rounded-full bg-blue-700 hover:bg-blue-800 text-white"
            title="Share on LinkedIn"
            on:click={shareOnLinkedIn}
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
          </button>
          <button
            class="share-button copy p-2 rounded-full bg-gray-500 hover:bg-gray-600 text-white"
            title="Copy Link"
            on:click={copyLink}
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
          </button>
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
    background-color: rgba(15, 23, 42, 0.1);
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
    object-position: center;
  }

  .share-buttons {
    display: flex;
    gap: 0.5rem;
  }

  .share-button {
    transition: all 0.2s ease;
  }

  .share-button:hover {
    transform: translateY(-2px);
  }

  .back-button {
    display: inline-flex;
    align-items: center;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
  }

  .back-button:hover {
    transform: translateX(-2px);
  }

  /* Dark mode styles for content */
  :global(.dark) .content {
    color: #e2e8f0;
  }

  :global(.dark) .content h1,
  :global(.dark) .content h2,
  :global(.dark) .content h3,
  :global(.dark) .content h4,
  :global(.dark) .content h5,
  :global(.dark) .content h6 {
    color: #f8fafc;
  }

  :global(.dark) .content a {
    color: #93c5fd;
  }

  :global(.dark) .content blockquote {
    border-left-color: #475569;
    color: #cbd5e1;
  }

  :global(.dark) .content code {
    background-color: #1e293b;
    color: #f1f5f9;
  }

  :global(.dark) .content pre {
    background-color: #0f172a;
  }

  /* Styling for content display */
  .content :global(h1) {
    font-size: 2rem;
    font-weight: 700;
    margin: 2rem 0 1rem;
  }

  .content :global(h2) {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 1.5rem 0 1rem;
    color: #1a202c;
  }

  .content :global(h3) {
    font-size: 1.25rem;
    font-weight: 700;
    margin: 1.25rem 0 0.75rem;
    color: #1a202c;
  }

  .content :global(p) {
    margin-bottom: 1.25rem;
    line-height: 1.7;
  }

  .content :global(ul) {
    list-style-type: disc;
    margin: 1rem 0;
    padding-left: 1.5rem;
  }

  .content :global(ol) {
    list-style-type: decimal;
    margin: 1rem 0;
    padding-left: 1.5rem;
  }

  .content :global(li) {
    margin-bottom: 0.5rem;
  }

  .content :global(blockquote) {
    padding: 1rem;
    border-left: 4px solid #e2e8f0;
    background-color: #f8fafc;
    margin: 1.5rem 0;
    font-style: italic;
  }

  .content :global(code) {
    background-color: #f1f5f9;
    padding: 0.2rem 0.4rem;
    border-radius: 0.25rem;
    font-family: monospace;
  }

  .content :global(pre) {
    background-color: #f1f5f9;
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin: 1.5rem 0;
  }

  .content :global(pre code) {
    background-color: transparent;
    padding: 0;
  }

  .content :global(a) {
    color: #3b82f6;
    text-decoration: none;
  }

  .content :global(a:hover) {
    text-decoration: underline;
  }

  .content :global(hr) {
    margin: 2rem 0;
    border: 0;
    border-top: 1px solid #e2e8f0;
  }

  .content :global(img) {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1.5rem auto;
    border-radius: 0.5rem;
  }

  .content :global(table) {
    width: 100%;
    margin: 1.5rem 0;
    border-collapse: collapse;
  }

  .content :global(th),
  .content :global(td) {
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .content :global(th) {
    background-color: #f8fafc;
    font-weight: 600;
  }
</style>