<script>
  import { onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';

  // Props with default values
  export let title = "Featured Articles";
  export let subtitle = "Our most impactful insights for the AI age";
  export let maxPosts = 3;
  export let showImages = true;

  // State
  let posts = [];
  let loading = true;
  let error = null;

  // Fetch featured posts on component mount
  onMount(async () => {
    try {
      const response = await fetch('/api/featured-posts?limit=' + maxPosts);

      if (!response.ok) {
        throw new Error(`Error fetching featured posts: ${response.statusText}`);
      }

      const data = await response.json();
      posts = data.posts;
      loading = false;
    } catch (err) {
      console.error('Failed to fetch featured posts:', err);
      error = err.message;
      loading = false;
    }
  });
</script>

<section class="featured-posts-section">
  <div class="featured-header">
    <h2 class="featured-title">{title}</h2>
    {#if subtitle}
      <p class="featured-subtitle">{subtitle}</p>
    {/if}
    <div class="stylish-divider"></div>
  </div>

  {#if loading}
    <div class="loading-container" in:fade>
      <div class="loading-spinner"></div>
      <p>Loading featured posts...</p>
    </div>
  {:else if error}
    <div class="error-container" in:fade>
      <p class="error-message">Unable to load featured posts: {error}</p>
    </div>
  {:else if posts.length === 0}
    <div class="empty-container" in:fade>
      <p>No featured posts available at this time.</p>
    </div>
  {:else}
    <div class="featured-grid" in:fade={{ duration: 400 }}>
      {#each posts as post, i}
        <a
          href={post.route}
          class="featured-card"
          in:slide={{ delay: i * 100, duration: 300 }}
        >
          {#if showImages && post.image}
            <div class="featured-image-container">
              <img src={post.image} alt={post.title} class="featured-image" loading="lazy" />
              <div class="featured-badge">Featured</div>
            </div>
          {/if}
          <div class="featured-content">
            <div class="featured-meta">
              <time datetime={post.date} class="featured-date">{post.date}</time>
              <span class="featured-author">By {post.author}</span>
            </div>
            <h3 class="featured-post-title">{post.title}</h3>
            <p class="featured-excerpt">{post.excerpt}</p>
            <span class="read-more">Read article <span class="arrow">→</span></span>
          </div>
        </a>
      {/each}
    </div>
  {/if}
</section>

<style>
  .featured-posts-section {
    margin: 3rem 0;
    width: 100%;
  }

  .featured-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .featured-title {
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: white;
    line-height: 1.2;
  }

  .featured-subtitle {
    font-size: clamp(1rem, 2vw, 1.125rem);
    color: #e2e8f0;
    margin-bottom: 1rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .stylish-divider {
    height: 4px;
    width: 80px;
    margin: 1.5rem auto;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 2px;
  }

  .featured-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 350px), 1fr));
    gap: 2rem;
    width: 100%;
  }

  .featured-card {
    display: flex;
    flex-direction: column;
    background-color: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
    text-decoration: none;
  }

  .featured-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 10px rgba(59, 130, 246, 0.2);
  }

  .featured-card:focus {
    outline: 3px solid #3b82f6;
    outline-offset: 5px;
  }

  .featured-image-container {
    position: relative;
    height: 180px;
    overflow: hidden;
  }

  .featured-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }

  .featured-card:hover .featured-image {
    transform: scale(1.05);
  }

  .featured-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .featured-content {
    padding: 1.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .featured-meta {
    display: flex;
    font-size: 0.875rem;
    color: #94a3b8;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .featured-post-title {
    font-size: clamp(1.25rem, 3vw, 1.5rem);
    font-weight: 700;
    margin-bottom: 0.75rem;
    color: white;
    line-height: 1.3;
  }

  .featured-excerpt {
    font-size: 0.95rem;
    color: #cbd5e1;
    margin-bottom: 1.5rem;
    flex: 1;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .read-more {
    font-size: 0.95rem;
    font-weight: 600;
    color: #60a5fa;
    display: flex;
    align-items: center;
    margin-top: auto;
  }

  .arrow {
    transition: transform 0.2s ease;
    margin-left: 0.25rem;
  }

  .featured-card:hover .arrow {
    transform: translateX(6px);
  }

  .loading-container, .error-container, .empty-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    width: 100%;
    text-align: center;
    padding: 2rem;
    background-color: rgba(30, 41, 59, 0.5);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .loading-spinner {
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-left-color: #3b82f6;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  @keyframes spin {
    100% {
      transform: rotate(360deg);
    }
  }

  .error-message {
    color: #f87171;
    font-weight: 500;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .featured-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .featured-posts-section {
      margin: 2rem 0;
    }

    .featured-title {
      font-size: 1.75rem;
    }

    .featured-content {
      padding: 1.25rem;
    }
  }

  @media (max-width: 480px) {
    .featured-image-container {
      height: 160px;
    }

    .featured-post-title {
      font-size: 1.15rem;
    }

    .featured-excerpt {
      font-size: 0.9rem;
      margin-bottom: 1rem;
      -webkit-line-clamp: 2;
    }

    .featured-badge {
      font-size: 0.7rem;
      padding: 0.2rem 0.6rem;
    }
  }

  /* Safari fix for grid gaps */
  @supports (-webkit-touch-callout: none) {
    .featured-grid {
      display: flex;
      flex-wrap: wrap;
    }

    .featured-grid > a {
      flex: 1 1 300px;
      margin: 1rem;
    }
  }

  /* Add browser compatibility fixes at the bottom of the style block */

  /* Fix for Firefox */
  @supports (-moz-appearance: none) {
    .featured-card {
      backface-visibility: hidden;
    }

    .featured-badge {
      transform: translateZ(0);
    }
  }

  /* Fix for older Edge versions */
  @supports (-ms-ime-align: auto) {
    .featured-grid {
      display: flex;
      flex-wrap: wrap;
    }

    .featured-grid > a {
      flex: 1 1 300px;
      margin: 1rem;
      max-width: calc(50% - 2rem);
    }
  }

  /* Fix for IE11 */
  @media all and (-ms-high-contrast: none), (-ms-high-contrast: active) {
    .featured-grid {
      display: flex;
      flex-wrap: wrap;
    }

    .featured-grid > a {
      flex: 0 0 calc(33.33% - 2rem);
      margin: 1rem;
      max-width: calc(33.33% - 2rem);
    }

    @media (max-width: 768px) {
      .featured-grid > a {
        flex: 0 0 calc(100% - 2rem);
        max-width: 100%;
      }
    }
  }
</style>