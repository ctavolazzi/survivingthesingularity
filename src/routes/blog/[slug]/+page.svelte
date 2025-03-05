<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import { marked } from 'marked';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  // Get page params from URL
  export let data;
  const { post, nextPost, prevPost } = data;

  let htmlContent = marked(post?.content || '');
  let readingTime = '5 min read'; // This could be calculated dynamically based on content length
  let scrollProgress = 0;
  let isProcessingClick = false;
  let lastClickTime = 0;

  // Simple data URL for default avatar to avoid 404 errors
  const defaultAvatar = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="%23718096" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';

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

  // Calculate estimated reading time
  onMount(() => {
    // Don't run on the server
    if (typeof window === 'undefined') return;

    // Estimate reading time (average reading speed: 200 words per minute)
    if (post.rawContent) {
      const wordCount = post.rawContent.trim().split(/\s+/).length;
      const minutes = Math.ceil(wordCount / 200);
      readingTime = `${minutes} min read`;
    }

    // Setup scroll progress tracking
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

{#if !post}
  <div class="error-container">
    <h1>Post not found</h1>
    <p>Sorry, the blog post you're looking for doesn't exist.</p>
    <a href="/blog" class="back-link">Return to blog</a>
  </div>
{:else}
  <div class="progress-bar" style="width: {scrollProgress}%"></div>

  <article class="main-content">
    <header class="article-header">
      <div class="content-container narrow">
        <a href="/blog" class="back-link">
          <span class="back-arrow">←</span> All articles
        </a>
        <h1 class="article-title">{post.title}</h1>

        <div class="article-meta">
          <div class="meta-item author">
            {#if typeof window !== 'undefined' && browser}
              <img src={getAvatarSrc(post)} alt="{post.author}" class="author-avatar" />
            {:else}
              <div class="author-avatar-placeholder"></div>
            {/if}
            <span>{post.author}</span>
          </div>
          <time datetime={post.date} class="meta-item date">{post.date}</time>
          <div class="meta-item reading-time">{readingTime}</div>
        </div>
      </div>

      <div class="featured-image-container">
        <img src={post.image} alt="{post.title}" class="featured-image" />
        <div class="image-overlay"></div>
      </div>
    </header>

    <div class="content-container">
      <div class="article-content-wrapper">
        <div class="share-sidebar">
          <button class="share-button" aria-label="Share on Twitter" on:click={shareOnTwitter}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>
          </button>
          <button class="share-button" aria-label="Share on LinkedIn" on:click={shareOnLinkedIn}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
          </button>
          <button class="share-button" aria-label="Copy Link" on:click={copyLink}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
          </button>
        </div>

        <div class="blog-content">
          {#if data.Content}
            <svelte:component this={data.Content} />
          {:else}
            {@html htmlContent}
          {/if}
        </div>
      </div>

      <div class="article-footer">
        <div class="tags">
          {#if post.tags}
            {#each post.tags as tag}
              <span class="tag">{tag}</span>
            {/each}
          {/if}
        </div>

        <div class="article-navigation">
          {#if prevPost}
            <a href="/blog/{prevPost.slug}" class="nav-button">
              <span class="nav-arrow">←</span>
              <span class="nav-text">Previous article</span>
            </a>
          {:else}
            <a href="/blog" class="nav-button">
              <span class="nav-arrow">←</span>
              <span class="nav-text">All articles</span>
            </a>
          {/if}

          {#if nextPost}
            <a href="/blog/{nextPost.slug}" class="nav-button next">
              <span class="nav-text">Next article</span>
              <span class="nav-arrow">→</span>
            </a>
          {/if}
        </div>
      </div>
    </div>
  </article>
{/if}

<style>
  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--color-primary, #3b82f6);
    z-index: 100;
    transition: width 0.1s;
  }

  .error-container {
    max-width: 800px;
    margin: 5rem auto;
    padding: 2rem;
    text-align: center;
  }

  .main-content {
    padding-top: 0;
    position: relative;
  }

  .article-header {
    position: relative;
    padding-top: 2rem;
    margin-bottom: 2rem;
  }

  .content-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1.5rem;
    width: 100%;
    position: relative;
  }

  .content-container.narrow {
    max-width: 700px;
  }

  .back-link {
    display: inline-flex;
    align-items: center;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-bottom: 1.5rem;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .back-link:hover {
    color: var(--color-primary);
  }

  .back-arrow {
    margin-right: 0.5rem;
    font-size: 1.1rem;
  }

  .article-title {
    font-size: clamp(2.2rem, 5vw, 3.2rem);
    line-height: 1.2;
    font-weight: 800;
    margin-bottom: 1.5rem;
    color: var(--color-text-primary);
    letter-spacing: -0.5px;
  }

  .article-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
    margin-bottom: 2rem;
    font-size: 0.95rem;
    color: var(--color-text-secondary);
  }

  .meta-item {
    display: flex;
    align-items: center;
  }

  .author {
    font-weight: 500;
  }

  .author-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 0.75rem;
    object-fit: cover;
    background-color: #f0f0f0;
  }

  .date, .reading-time {
    position: relative;
    padding-left: 1rem;
  }

  .date::before, .reading-time::before {
    content: "•";
    position: absolute;
    left: 0;
    color: var(--color-text-secondary);
    opacity: 0.6;
  }

  .featured-image-container {
    width: 100%;
    height: 40vh;
    min-height: 300px;
    max-height: 500px;
    position: relative;
    margin: 2rem 0;
    overflow: hidden;
  }

  .featured-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.5s ease;
  }

  .image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.4));
  }

  .article-content-wrapper {
    display: grid;
    grid-template-columns: 50px 1fr;
    gap: 2rem;
    position: relative;
    margin-bottom: 4rem;
  }

  .share-sidebar {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    position: sticky;
    top: 100px;
    height: fit-content;
  }

  .share-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-background-secondary);
    border: none;
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }

  .share-button:hover {
    transform: translateY(-2px);
    background: var(--color-primary);
    color: white;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }

  /* Blog Content */
  .blog-content {
    font-size: clamp(1rem, 2vw, 1.125rem);
    line-height: 1.75;
  }

  .blog-content :global(h1) {
    font-size: clamp(1.8rem, 4vw, 2.25rem);
    font-weight: bold;
    margin-top: 2.5rem;
    margin-bottom: 1.25rem;
    color: var(--color-text-primary);
    line-height: 1.3;
  }

  .blog-content :global(h2) {
    font-size: clamp(1.5rem, 3vw, 1.875rem);
    font-weight: bold;
    margin-top: 2.25rem;
    margin-bottom: 1.25rem;
    color: var(--color-text-primary);
    line-height: 1.3;
  }

  .blog-content :global(h3) {
    font-size: clamp(1.25rem, 2.5vw, 1.5rem);
    font-weight: bold;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
    line-height: 1.3;
  }

  .blog-content :global(p) {
    margin-bottom: 1.5rem;
    color: var(--color-text-secondary);
  }

  .blog-content :global(ul),
  .blog-content :global(ol) {
    margin-bottom: 1.5rem;
    padding-left: 1.75rem;
    color: var(--color-text-secondary);
  }

  .blog-content :global(li) {
    margin-bottom: 0.75rem;
  }

  .blog-content :global(a) {
    color: var(--color-primary);
    text-decoration: underline;
    text-underline-offset: 3px;
    transition: color 0.2s ease;
  }

  .blog-content :global(a:hover) {
    color: var(--color-primary-dark, #2563eb);
  }

  .blog-content :global(blockquote) {
    border-left: 4px solid var(--color-primary);
    padding-left: 1.5rem;
    margin: 2rem 0;
    font-style: italic;
    color: var(--color-text-secondary);
  }

  .blog-content :global(pre) {
    background: var(--color-background-secondary);
    border-radius: 6px;
    padding: 1.25rem;
    overflow-x: auto;
    margin: 1.5rem 0;
  }

  .blog-content :global(code) {
    font-family: monospace;
    font-size: 0.9em;
  }

  .blog-content :global(img) {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 2rem 0;
  }

  /* Article Footer */
  .article-footer {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(0,0,0,0.1);
  }

  :global(.dark) .article-footer {
    border-top-color: rgba(255,255,255,0.1);
  }

  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 2rem;
  }

  .tag {
    padding: 0.35rem 0.75rem;
    background-color: var(--color-background-secondary);
    color: var(--color-text-secondary);
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .tag:hover {
    background-color: var(--color-primary);
    color: white;
  }

  .article-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 2rem;
  }

  .nav-button {
    display: flex;
    align-items: center;
    padding: 0.75rem 1.25rem;
    background-color: var(--color-background-secondary);
    color: var(--color-text-secondary);
    border-radius: 50px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .nav-button:hover {
    background-color: var(--color-primary);
    color: white;
    transform: translateY(-2px);
  }

  .nav-arrow {
    font-size: 1.1rem;
  }

  .nav-button.next .nav-arrow {
    margin-left: 0.5rem;
  }

  .nav-button:not(.next) .nav-arrow {
    margin-right: 0.5rem;
  }

  /* Mobile optimizations */
  @media (max-width: 768px) {
    .article-header {
      padding-top: 1rem;
    }

    .content-container {
      padding: 0 1.25rem;
    }

    .featured-image-container {
      height: 30vh;
      min-height: 200px;
      margin: 1.5rem 0;
    }

    .article-content-wrapper {
      grid-template-columns: 1fr;
      gap: 0;
    }

    .share-sidebar {
      flex-direction: row;
      position: static;
      margin-bottom: 2rem;
      justify-content: center;
    }

    .article-navigation {
      flex-direction: column;
      gap: 1rem;
    }

    .nav-button {
      justify-content: center;
    }
  }

  /* Tablet optimizations */
  @media (min-width: 769px) and (max-width: 1024px) {
    .article-content-wrapper {
      grid-template-columns: 40px 1fr;
      gap: 1.5rem;
    }
  }

  /* Dark mode specific styling */
  :global(.dark) .share-button {
    background-color: #2d3748;
    color: #e5e7eb;
  }

  :global(.dark) .share-button:hover {
    background-color: var(--color-primary);
    color: white;
  }

  :global(.dark) .tag {
    background-color: #2d3748;
    color: #e5e7eb;
  }

  :global(.dark) .nav-button {
    background-color: #2d3748;
    color: #e5e7eb;
  }

  .author-avatar-placeholder {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 0.75rem;
    background-color: #f0f0f0;
  }
</style>