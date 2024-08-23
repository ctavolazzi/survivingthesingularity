<script>
  import { posts } from '$lib/data/blog-posts/blogPosts.js';
</script>

<div class="main-content">
  <div class="content-container">
    <h1 class="title">Blog Posts</h1>

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
    font-size: 3rem;
    margin-bottom: 2rem;
    color: var(--color-text-primary);
    text-align: center;
    font-weight: 700;
    letter-spacing: -0.5px;
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
</style>