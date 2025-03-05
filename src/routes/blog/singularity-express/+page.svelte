<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import { post } from '$lib/data/blog-posts/singularity-express/index.js';
  import { marked } from 'marked';
  import { browser } from '$app/environment';

  const defaultAvatar = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="%23718096" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';

  let htmlContent = marked(post.content);
  let readingTime = '5 min read'; // This could be calculated dynamically
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
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{readingTime}</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
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
      <p class="lead">
        The Singularity Express has pulled into the station, and it's bringing with it a new era of AI
        that can think and reason. Get ready for Level 2 AI capabilities that will transform how we
        interact with artificial intelligence.
      </p>

      <h2>Welcome to Level 2</h2>
      <p>
        We're witnessing a pivotal moment in AI development. The transition to Level 2 AI represents
        a significant leap forward in machine intelligence, where AI systems can now demonstrate
        genuine reasoning capabilities and understanding rather than just pattern matching.
      </p>

      <h2>What Makes Level 2 Different?</h2>
      <ul>
        <li>True reasoning capabilities beyond pattern recognition</li>
        <li>Improved context understanding and retention</li>
        <li>More sophisticated problem-solving abilities</li>
        <li>Better handling of abstract concepts</li>
        <li>Enhanced natural language understanding</li>
      </ul>

      <h2>Real-World Implications</h2>
      <p>
        The arrival of Level 2 AI capabilities brings with it profound implications for various sectors:
      </p>
      <ul>
        <li>More sophisticated automated decision-making systems</li>
        <li>Enhanced natural language processing and generation</li>
        <li>Improved problem-solving in complex domains</li>
        <li>More nuanced human-AI interactions</li>
      </ul>

      <blockquote>
        "We're not just seeing incremental improvements anymore. This is a fundamental shift in how
        AI systems process and understand information." - AI Research Lead
      </blockquote>

      <h2>Preparing for the Future</h2>
      <p>
        As we enter this new phase of AI development, it's crucial to understand both the opportunities
        and challenges that lie ahead. Level 2 AI capabilities will require:
      </p>
      <ul>
        <li>New frameworks for AI safety and ethics</li>
        <li>Updated regulatory approaches</li>
        <li>Enhanced security measures</li>
        <li>Revised educational and training programs</li>
      </ul>

      <h2>The Road Ahead</h2>
      <p>
        The Singularity Express is just beginning its journey. As we move forward with Level 2 AI,
        we're entering uncharted territory that promises to reshape our relationship with technology
        and our understanding of intelligence itself. Stay tuned as we continue to explore this
        exciting new frontier.
      </p>
    </div>
  </article>

  <Spacer height="2rem" />

  <div class="newsletter-section">
    <NewsletterSignup />
  </div>
</div>

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

  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--color-primary, #3b82f6);
    z-index: 100;
    transition: width 0.1s;
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