<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  export let data;
  const { posts } = data;

  let visible = false;
  onMount(() => { visible = true; });

  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  function estimateReadTime(excerpt) {
    // Rough estimate: excerpt length as proxy
    const words = excerpt ? excerpt.split(/\s+/).length : 0;
    return Math.max(3, Math.round(words / 30) + 3);
  }

  function getCategoryTag(post) {
    if (post.route?.includes('singularity-express')) return 'Opinion';
    if (post.route?.includes('farm-bot-deep-dive')) return 'Deep Dive';
    if (post.route?.includes('darpa')) return 'Research';
    if (post.route?.includes('claude-projects')) return 'AI Build';
    if (post.route?.includes('robot-farm-bot')) return 'Robotics';
    if (post.route?.includes('synthetic-biological')) return 'Biotech';
    if (post.route?.includes('neural-interfaces')) return 'Neurotech';
    if (post.route?.includes('whispers')) return 'Essay';
    return 'Insight';
  }
</script>

<svelte:head>
  <title>Blog — Surviving the Singularity</title>
  <meta name="description" content="Deep dives into AI, robotics, synthetic biology, and the technologies reshaping material independence." />
</svelte:head>

{#if visible}
  <div class="blog-page" in:fade={{ duration: 400 }}>
    <header class="blog-header">
      <p class="blog-label">The Blog</p>
      <h1 class="blog-title">Dispatches from the Build</h1>
      <p class="blog-subtitle">
        Deep dives into AI breakthroughs, robotics, synthetic biology, and the technologies reshaping the path to material independence.
      </p>
    </header>

    <!-- Featured post (first one) -->
    {#if posts.length > 0}
      {@const featured = posts[0]}
      <a href={featured.route} class="featured-card">
        <div class="featured-image-wrap">
          <img src={featured.image} alt={featured.title} class="featured-image" loading="lazy" />
          <div class="featured-overlay"></div>
          <span class="featured-badge">Latest</span>
        </div>
        <div class="featured-content">
          <div class="featured-meta">
            <span class="post-tag">{getCategoryTag(featured)}</span>
            <time>{formatDate(featured.date)}</time>
            <span>{estimateReadTime(featured.excerpt)} min read</span>
          </div>
          <h2 class="featured-title">{featured.title}</h2>
          <p class="featured-excerpt">{featured.excerpt}</p>
          <span class="read-link">Read article <span class="arrow">&rarr;</span></span>
        </div>
      </a>
    {/if}

    <!-- Post grid -->
    {#if posts.length > 1}
      <div class="posts-grid">
        {#each posts.slice(1) as post, i}
          <a href={post.route} class="post-card" style="animation-delay: {(i + 1) * 60}ms">
            <div class="post-image-wrap">
              <img src={post.image} alt={post.title} class="post-image" loading="lazy" />
            </div>
            <div class="post-content">
              <div class="post-meta">
                <span class="post-tag">{getCategoryTag(post)}</span>
                <time>{formatDate(post.date)}</time>
              </div>
              <h3 class="post-title">{post.title}</h3>
              <p class="post-excerpt">{post.excerpt}</p>
              <div class="post-footer">
                <span class="post-read-time">{estimateReadTime(post.excerpt)} min read</span>
                <span class="read-link">Read <span class="arrow">&rarr;</span></span>
              </div>
            </div>
          </a>
        {/each}
      </div>
    {/if}
  </div>
{/if}

<style>
  .blog-page {
    max-width: 1000px;
    margin: 0 auto;
    padding: 3rem 1.5rem 5rem;
  }

  .blog-header {
    margin-bottom: 3rem;
  }

  .blog-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #f59e0b;
    margin: 0 0 0.75rem 0;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
  }

  .blog-title {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 900;
    color: #f1f5f9;
    margin: 0 0 0.75rem 0;
    letter-spacing: -0.03em;
  }

  .blog-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0;
    max-width: 640px;
  }

  /* Featured card */
  .featured-card {
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 20px;
    overflow: hidden;
    text-decoration: none;
    transition: all 0.3s ease;
    margin-bottom: 3rem;
  }

  .featured-card:hover {
    border-color: rgba(245, 158, 11, 0.2);
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }

  .featured-image-wrap {
    position: relative;
    overflow: hidden;
    min-height: 300px;
  }

  .featured-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
  }

  .featured-card:hover .featured-image {
    transform: scale(1.05);
  }

  .featured-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(2, 6, 23, 0.3), transparent);
  }

  .featured-badge {
    position: absolute;
    top: 1rem;
    left: 1rem;
    padding: 0.3rem 0.7rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-size: 0.7rem;
    font-weight: 700;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .featured-content {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .featured-meta {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    font-size: 0.78rem;
    color: #64748b;
    margin-bottom: 1rem;
  }

  .post-tag {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
  }

  .featured-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.75rem 0;
    line-height: 1.3;
    letter-spacing: -0.02em;
  }

  .featured-excerpt {
    font-size: 0.92rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0 0 1.25rem 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .read-link {
    font-size: 0.88rem;
    font-weight: 600;
    color: #f59e0b;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
  }

  .arrow {
    transition: transform 0.2s;
  }

  .featured-card:hover .arrow,
  .post-card:hover .arrow {
    transform: translateX(3px);
  }

  /* Posts grid */
  .posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
    gap: 1.5rem;
  }

  .post-card {
    display: flex;
    flex-direction: column;
    background: rgba(30, 41, 59, 0.25);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 16px;
    overflow: hidden;
    text-decoration: none;
    transition: all 0.3s ease;
    animation: fadeUp 0.5s ease forwards;
    opacity: 0;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .post-card:hover {
    border-color: rgba(245, 158, 11, 0.2);
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
  }

  .post-image-wrap {
    overflow: hidden;
    aspect-ratio: 16 / 9;
    background: rgba(15, 23, 42, 0.5);
  }

  .post-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
  }

  .post-card:hover .post-image {
    transform: scale(1.05);
  }

  .post-content {
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  .post-meta {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    font-size: 0.75rem;
    color: #475569;
    margin-bottom: 0.75rem;
  }

  .post-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
    letter-spacing: -0.01em;
  }

  .post-excerpt {
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.5;
    margin: 0 0 1rem 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    flex: 1;
  }

  .post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .post-read-time {
    font-size: 0.72rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
  }

  @media (max-width: 768px) {
    .featured-card {
      grid-template-columns: 1fr;
    }

    .featured-image-wrap {
      min-height: 200px;
    }

    .blog-page {
      padding: 2rem 1rem 4rem;
    }
  }

  @media (max-width: 480px) {
    .posts-grid {
      gap: 1rem;
    }
  }
</style>
