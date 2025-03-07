<script>
  import { onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';

  // Props with default values
  export let title = "Latest News";
  export let subtitle = "Stay updated with our newest content";
  export let showImage = true;

  // State for the latest post
  let latestPost = null;
  let loading = true;
  let error = null;

  // Fetch latest post on component mount
  onMount(async () => {
    try {
      const response = await fetch('/api/latest-post');

      if (!response.ok) {
        throw new Error(`Error fetching latest post: ${response.statusText}`);
      }

      const data = await response.json();
      latestPost = data.post;
      loading = false;
    } catch (err) {
      console.error('Failed to fetch latest post:', err);
      error = err.message;
      loading = false;
    }
  });
</script>

<section class="latest-news-section">
  <div class="latest-header">
    <h2 class="latest-title">{title}</h2>
    {#if subtitle}
      <p class="latest-subtitle">{subtitle}</p>
    {/if}
    <div class="stylish-divider"></div>
  </div>

  {#if loading}
    <div class="loading-container" in:fade>
      <div class="loading-spinner"></div>
      <p>Loading latest post...</p>
    </div>
  {:else if error}
    <div class="error-container" in:fade>
      <p class="error-message">Unable to load latest post: {error}</p>
    </div>
  {:else if !latestPost}
    <div class="empty-container" in:fade>
      <p>No latest post available at this time.</p>
    </div>
  {:else}
    <div class="latest-post-container" in:fade={{ duration: 400 }}>
      <a href={latestPost.route} class="latest-post-card" in:slide={{ duration: 300 }}>
        <div class="latest-content-wrapper">
          <div class="latest-content">
            <div class="new-tag">NEW</div>
            <div class="latest-meta">
              <time datetime={latestPost.date} class="latest-date">{latestPost.date}</time>
              <span class="latest-author">By {latestPost.author}</span>
            </div>
            <h3 class="latest-post-title">{latestPost.title}</h3>
            <p class="latest-excerpt">{latestPost.excerpt}</p>
            <span class="read-more">Read article <span class="arrow">→</span></span>
          </div>

          {#if showImage && latestPost.image}
            <div class="latest-image-container">
              <img src={latestPost.image} alt={latestPost.title} class="latest-image" loading="lazy" />
            </div>
          {/if}
        </div>
      </a>
    </div>
  {/if}
</section>

<style>
  .latest-news-section {
    margin: 1rem 0;
    width: 100%;
  }

  .latest-header {
    text-align: center;
    margin-bottom: 1rem;
  }

  .latest-title {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: white;
    line-height: 1.2;
  }

  .latest-subtitle {
    font-size: clamp(0.95rem, 2vw, 1.1rem);
    color: #e2e8f0;
    margin-bottom: 0.75rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .stylish-divider {
    height: 4px;
    width: 80px;
    margin: 1rem auto;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 2px;
  }

  .latest-post-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
  }

  .latest-post-card {
    display: block;
    background-color: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-decoration: none;
  }

  .latest-post-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 15px rgba(59, 130, 246, 0.3);
  }

  .latest-post-card:focus {
    outline: 3px solid #3b82f6;
    outline-offset: 5px;
  }

  .latest-content-wrapper {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    min-height: 220px;
  }

  .latest-content {
    padding: 1.25rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  .new-tag {
    display: inline-block;
    background: linear-gradient(135deg, #ef4444, #f97316);
    color: white;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.25rem 0.8rem;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    letter-spacing: 0.05em;
  }

  .latest-meta {
    display: flex;
    font-size: 0.95rem;
    color: #94a3b8;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .latest-post-title {
    font-size: clamp(1.5rem, 4vw, 2rem);
    font-weight: 700;
    margin-bottom: 0.75rem;
    color: white;
    line-height: 1.2;
  }

  .latest-excerpt {
    font-size: 1rem;
    color: #cbd5e1;
    margin-bottom: 1.5rem;
    flex: 1;
    line-height: 1.6;
    max-width: 650px;
  }

  .latest-image-container {
    flex: 0 0 40%;
    position: relative;
    overflow: hidden;
  }

  .latest-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
  }

  .latest-post-card:hover .latest-image {
    transform: scale(1.05);
  }

  .read-more {
    font-size: 1.05rem;
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

  .latest-post-card:hover .arrow {
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
  @media (max-width: 900px) {
    .latest-content-wrapper {
      flex-direction: column-reverse;
    }

    .latest-image-container {
      height: 220px;
      flex-basis: auto;
    }

    .latest-content {
      padding: 1.25rem;
    }

    .latest-post-title {
      font-size: 1.35rem;
    }
  }

  @media (max-width: 480px) {
    .latest-image-container {
      height: 200px;
    }

    .latest-content {
      padding: 1.25rem;
    }

    .latest-post-title {
      font-size: 1.25rem;
    }

    .latest-excerpt {
      font-size: 0.95rem;
      margin-bottom: 1.5rem;
    }

    .new-tag {
      font-size: 0.7rem;
      padding: 0.2rem 0.6rem;
    }
  }
</style>