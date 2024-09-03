<script>
  import { posts } from '$lib/data/blog-posts/blogPosts.js';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import SkoolGroup from '$lib/components/SkoolGroup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';

  function handleJoinSkool() {
    // Handle join action (you can implement this later)
  }
</script>

<div class="main-content">
  <div class="content-container">
    <h1 class="title">Insights for the AI Age</h1>

    <div class="blog-intro">
      <p><strong>Welcome to the Surviving the Singularity blog</strong>, curated by Christopher Tavolazzi, author and AI expert. Dive into infrequent but profound explorations of AI, technology, and our rapidly evolving world.</p>
      <p>🚀 <em>Prepare for the future. Gain insights. Stay ahead of the curve.</em></p>
    </div>

    
    
    <h2 id="latest-posts" class="section-title">Latest Posts</h2>
    <div class="stylish-divider"></div>
    <div class="post-grid">
      {#each posts as post}
      <a href="/blog/{post.slug}" class="post-card-link">
        <div class="post-card">
          <img src={post.image} alt={post.title} class="post-image" />
          <div class="post-content">
            <h2 class="post-title">{post.title}</h2>
            <p class="post-meta">
              <span class="post-date">{post.date}</span> • 
              <span class="post-author">By {post.author}</span>
            </p>
            <p class="post-excerpt">{post.excerpt}</p>
            <span class="read-more">Read more →</span>
          </div>
        </div>
      </a>
      {/each}
    </div>
    
    <div class="stylish-divider"></div>
    <NewsletterSignup />
    <div class="stylish-divider"></div>
    
    <div class="skool-group-container">
      <SkoolGroup onButtonClick={handleJoinSkool} />
    </div>
  </div>
</div>

<style>
  .main-content {
    padding-top: 2rem;
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  .title {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
    text-align: center;
    font-weight: 800;
    letter-spacing: -1px;
  }

  .blog-intro {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background-color: var(--color-background-secondary);
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .blog-intro p {
    margin-bottom: 1rem;
    line-height: 1.7;
    color: var(--color-text-secondary);
    font-size: 1.1rem;
  }

  .cta-button {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: var(--color-primary);
    color: white;
    text-decoration: none;
    border-radius: 30px;
    font-weight: 600;
    transition: background-color 0.3s ease;
  }

  .cta-button:hover {
    background-color: var(--color-primary-dark);
  }

  .section-title {
    font-size: 2.5rem;
    margin: 3rem 0 2rem;
    text-align: center;
    color: var(--color-text-primary);
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
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
  }

  .post-card-link {
    text-decoration: none;
    color: inherit;
    display: block;
  }

  .post-card {
    background-color: var(--color-background-secondary);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
  }

  .post-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }

  .post-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease;
  }

  .post-card:hover .post-image {
    transform: scale(1.05);
  }

  .post-content {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    height: calc(100% - 200px);
  }

  .post-title {
    font-size: 1.75rem;
    margin-bottom: 0.75rem;
    color: var(--color-text-primary);
    font-weight: 600;
    line-height: 1.2;
  }

  .post-meta {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    margin-bottom: 1rem;
  }

  .post-excerpt {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
    flex-grow: 1;
  }

  .read-more {
    display: inline-block;
    font-weight: 600;
    color: var(--color-text-primary);
    transition: color 0.3s ease;
  }

  .post-card:hover .read-more {
    color: var(--color-primary);
  }

  @media (max-width: 768px) {
    .title {
      font-size: 2.5rem;
    }
    .post-grid {
      grid-template-columns: 1fr;
    }
  }

  :global(.dark) .post-card {
    background-color: #2d3748;
  }

  :global(.dark) .post-title {
    color: #e5e7eb;
  }

  :global(.dark) .post-date,
  :global(.dark) .post-author,
  :global(.dark) .post-excerpt {
    color: #9ca3af;
  }

  :global(.dark) .read-more {
    color: #e5e7eb;
  }

  .skool-group-container {
    margin-top: 4rem;
    display: flex;
    justify-content: center;
  }
</style>