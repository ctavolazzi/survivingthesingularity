<script>
  import { onMount } from 'svelte';
  export let data;
  const { posts } = data;
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import FeaturedPosts from '$lib/components/FeaturedPosts.svelte';
  import NewsTicker from '$lib/components/NewsTicker.svelte';
  import TreasureTavernAd from '$lib/components/ads/TreasureTavernAd.svelte';
  import { loadBlogPosts } from '$lib/data/blog-posts/blogPosts.js';

  // Create news ticker items array
  let newsTickerItems = [];

  // Function to determine category tag based on post content
  function getCategoryTag(post) {
    // Define tag based on post slug or title to create variety
    let tag = 'Blog';

    // Assign specific tags based on content type
    if (post.route && post.route.includes('singularity-express')) {
      return 'Opinion';
    } else if (post.route && post.route.includes('farm-bot-deep-dive')) {
      return 'Tech';
    } else if (post.route && post.route.includes('darpa-biomechanical-space-structures')) {
      return 'News';
    } else if (post.route && post.route.includes('claude-projects-weekend-project')) {
      return 'AI Update';
    } else if (post.route && post.route.includes('robot-farm-bot')) {
      return 'Review';
    } else if (post.route && post.route.includes('synthetic-biological-intelligence')) {
      return 'Science';
    } else if (post.title && post.title.toLowerCase().includes('regulatory')) {
      return 'Policy';
    } else if (post.title && post.title.toLowerCase().includes('breakthrough')) {
      return 'Breaking';
    } else if (post.title && post.title.toLowerCase().includes('future')) {
      return 'Future';
    } else if (post.title && post.title.toLowerCase().includes('review')) {
      return 'Review';
    } else if (post.title && post.title.toLowerCase().includes('guide')) {
      return 'Guide';
    }

    return 'AI Insights';
  }

  // Function to get category color based on tag
  function getCategoryColor(tag) {
    switch(tag) {
      case 'Opinion':
        return '#FF7043'; // Orange
      case 'Tech':
        return '#26A69A'; // Teal
      case 'News':
        return '#42A5F5'; // Blue
      case 'AI Update':
        return '#7E57C2'; // Purple
      case 'Review':
        return '#66BB6A'; // Green
      case 'Science':
        return '#EC407A'; // Pink
      case 'Policy':
        return '#78909C'; // Blue Grey
      case 'Breaking':
        return '#EF5350'; // Red
      case 'Future':
        return '#5C6BC0'; // Indigo
      case 'Guide':
        return '#FFA726'; // Amber
      default:
        return '#3b82f6'; // Default blue (var(--color-primary))
    }
  }

  // Load blog posts and format for news ticker
  onMount(async () => {
    const blogPosts = await loadBlogPosts();

    // Format blog posts for the news ticker with varied, appropriate tags
    newsTickerItems = blogPosts.map(post => {
      return {
        date: new Date(post.date).toISOString().split('T')[0],
        text: post.title,
        tag: getCategoryTag(post),
        link: `/blog/${post.slug}`
      };
    });
  });
</script>

<div class="main-content">
  <!-- Enhanced Hero Section -->
  <div class="hero-section">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <div class="hero-badge">Surviving the Singularity</div>
      <h1 class="hero-title">Insights for the AI Age</h1>
      <div class="hero-tagline">
        <p class="hero-description">Expert insights to help you navigate the rapidly evolving world of artificial intelligence and technology.</p>
        <div class="hero-cta">
          <span class="rocket">🚀</span>
          <span class="cta-text">Prepare for the future. Gain valuable insights. Stay ahead of the curve.</span>
        </div>
      </div>
    </div>
    <div class="hero-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
      <div class="grid-pattern"></div>
    </div>
  </div>

  <div class="content-container">
    <!-- News Ticker -->
    <div class="news-ticker-wrapper">
      <NewsTicker
        title="AI & Tech Updates"
        scrollSpeed={2500}
        items={newsTickerItems}
        backgroundColor="rgba(15, 23, 42, 0.7)"
        textColor="white"
        accentColor="#3b82f6"
      />
    </div>

    <!-- Featured Posts -->
    <div class="featured-posts-wrapper">
      <FeaturedPosts
        title="Featured Insights"
        subtitle="Must-read content to help you navigate the AI revolution"
        maxPosts={3}
        showImages={true}
      />
    </div>

    <h2 id="latest-posts" class="section-title">Latest Posts</h2>
    <div class="stylish-divider"></div>

    <div class="post-grid">
      {#each posts as post}
      {@const categoryTag = getCategoryTag(post)}
      {@const categoryColor = getCategoryColor(categoryTag)}
      <a href={post.route} class="post-card-link">
        <article class="post-card">
          <div class="post-image-container">
            <img src={post.image} alt={post.title} class="post-image" loading="lazy" />
            <div class="post-category" style="background-color: {categoryColor};">{categoryTag}</div>
          </div>
          <div class="post-content">
            <div class="post-meta">
              <time datetime={post.date} class="post-date">{post.date}</time>
              <span class="post-author">By {post.author}</span>
            </div>
            <h2 class="post-title">{post.title}</h2>
            <p class="post-excerpt">{post.excerpt}</p>
            <span class="read-more">Read article <span class="arrow">→</span></span>
          </div>
        </article>
      </a>
      {/each}
    </div>

    <div class="stylish-divider"></div>
    <NewsletterSignup />
    <DiscordButton />

    <!-- Add Treasure Tavern Ad -->
    <div class="treasure-tavern-container">
      <TreasureTavernAd
        title="Discover Unique Treasures"
        subtitle="The Treasure Tavern"
        description="Curated gems from the far corners of the Internet."
        bulletPoints={[
          "Unique finds you won't see elsewhere",
          "Support our work with every purchase",
          "Each item has a story to tell",
          "Fresh collections added monthly"
        ]}
        ctaText="Explore the Tavern"
        ctaUrl="https://treasuretavernhq.myshopify.com/"
        badgeText="Support Our Work"
      />
    </div>
  </div>
</div>

<style>
  .main-content {
    padding-top: 0; /* Removed padding to accommodate hero */
  }

  /* Hero Section Styles */
  .hero-section {
    position: relative;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 1.5rem;
    overflow: hidden;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    margin-bottom: 1rem;
  }

  .hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.15), transparent 50%);
    z-index: 1;
  }

  .hero-content {
    position: relative;
    max-width: 900px;
    width: 100%;
    text-align: center;
    z-index: 2;
  }

  .hero-decoration {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    overflow: hidden;
  }

  .circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
  }

  .circle-1 {
    width: 400px;
    height: 400px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    top: -120px;
    right: -100px;
  }

  .circle-2 {
    width: 300px;
    height: 300px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    bottom: -80px;
    left: -80px;
  }

  .circle-3 {
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1), transparent);
    top: 20%;
    left: 10%;
  }

  .grid-pattern {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    z-index: -1;
  }

  .hero-badge {
    display: inline-block;
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(59, 130, 246, 0.2);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .hero-title {
    font-size: clamp(3rem, 8vw, 4.5rem);
    margin-bottom: 1.5rem;
    color: white;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
    background: linear-gradient(120deg, #f0f9ff, #e0f2fe, #bae6fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  }

  .hero-tagline {
    max-width: 700px;
    margin: 0 auto;
  }

  .hero-tagline p {
    font-size: clamp(1.1rem, 2vw, 1.25rem);
    line-height: 1.6;
    margin-bottom: 1rem;
    color: #e2e8f0;
  }

  .hero-description {
    color: #cbd5e1 !important;
    font-size: clamp(1rem, 2vw, 1.15rem) !important;
    max-width: 90%;
    margin: 0 auto 2rem !important;
  }

  .hero-cta {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin: 2rem auto;
    padding: 1rem 1.5rem;
    background: rgba(30, 41, 59, 0.6);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    max-width: max-content;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }

  .rocket {
    font-size: 1.8rem;
    display: inline-block;
  }

  .cta-text {
    font-size: clamp(0.95rem, 2vw, 1.05rem);
    font-weight: 500;
    color: #f8fafc;
    font-style: italic;
  }

  /* Content styles */
  .content-container {
    max-width: 1200px;
    margin: 0.5rem auto 2rem;
    padding: 0 1.5rem;
    width: 100%;
  }

  .section-title {
    font-size: clamp(2rem, 4vw, 2.75rem);
    margin: 3rem 0 1.5rem;
    text-align: center;
    color: var(--color-text-primary);
    font-weight: 700;
    position: relative;
    padding-bottom: 1rem;
  }

  .section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
    border-radius: 2px;
  }

  .stylish-divider {
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
    margin: 2rem auto;
    max-width: 80%;
  }

  :global(.dark) .stylish-divider {
    background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
  }

  .post-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 350px), 1fr));
    gap: 2.5rem;
  }

  .post-card-link {
    text-decoration: none;
    color: inherit;
    display: block;
    height: 100%;
    transition: transform 0.2s ease-out;
  }

  .post-card-link:hover {
    transform: translateY(-3px);
  }

  .post-card-link:focus {
    outline: 3px solid var(--color-primary);
    outline-offset: 5px;
    border-radius: 12px;
  }

  .post-card {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: var(--color-background-secondary);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.2s ease;
  }

  .post-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  }

  .post-image-container {
    position: relative;
    aspect-ratio: 16 / 9;
    overflow: hidden;
  }

  .post-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .post-category {
    position: absolute;
    top: 1rem;
    left: 1rem;
    padding: 0.45rem 0.9rem;
    background-color: var(--color-primary);
    color: white;
    font-size: 0.9rem;
    font-weight: 700;
    border-radius: 30px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease;
  }

  .post-card:hover .post-category {
    transform: translateY(-3px);
  }

  .post-content {
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }

  .post-meta {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    font-size: 0.85rem;
    color: var(--color-text-secondary);
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
  }

  .post-date {
    font-weight: 500;
  }

  .post-author {
    font-style: italic;
  }

  .post-title {
    font-size: clamp(1.35rem, 3vw, 1.65rem);
    margin-bottom: 1rem;
    color: var(--color-text-primary);
    font-weight: 700;
    line-height: 1.3;
  }

  .post-excerpt {
    font-size: clamp(0.95rem, 2vw, 1rem);
    line-height: 1.6;
    margin-bottom: 1.5rem;
    color: var(--color-text-secondary);
    flex-grow: 1;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .read-more {
    display: inline-flex;
    align-items: center;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--color-primary);
    margin-top: auto;
  }

  .arrow {
    display: inline-block;
    margin-left: 0.35rem;
  }

  /* Component containers styling */
  .news-ticker-wrapper {
    margin: 0 0 2rem 0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }

  .featured-posts-wrapper {
    margin: 0 0 3.5rem;
  }

  /* Styling for the Treasure Tavern container */
  .treasure-tavern-container {
    width: 100%;
    max-width: 900px;
    margin: 3rem auto 2rem;
    padding: 0 1rem;
  }

  /* Improved mobile optimization */
  @media (max-width: 768px) {
    .hero-section {
      min-height: 400px;
      padding: 3rem 1rem;
      margin-bottom: 0.75rem;
    }

    .hero-cta {
      flex-direction: column;
      gap: 0.5rem;
      padding: 1rem;
    }

    .content-container {
      padding: 0 1rem;
      margin: 0.5rem auto 1.5rem;
    }

    .news-ticker-wrapper {
      margin-bottom: 1.5rem;
    }

    .featured-posts-wrapper {
      margin: 0 0 2.5rem;
    }

    .treasure-tavern-container {
      margin: 2.5rem auto 1.5rem;
    }
  }

  @media (max-width: 480px) {
    .hero-section {
      min-height: 350px;
      padding: 2rem 1rem;
      margin-bottom: 0.5rem;
    }

    .news-ticker-wrapper {
      margin-bottom: 1rem;
    }

    .featured-posts-wrapper {
      margin: 0 0 2rem;
    }

    .content-container {
      margin: 0.25rem auto 1.5rem;
    }

    .treasure-tavern-container {
      margin: 2rem auto 1rem;
    }
  }

  /* Additional CSS for very small screens */
  @media (max-width: 350px) {
    .hero-title {
      font-size: clamp(2.5rem, 7vw, 3rem);
    }

    .post-title, .section-title {
      font-size: clamp(1.25rem, 2.5vw, 1.5rem);
    }
  }
</style>