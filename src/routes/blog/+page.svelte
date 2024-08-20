<!-- src/routes/blog/+page.svelte -->
<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import { onMount } from 'svelte';
  import { posts } from '$lib/data/blog-posts/blogPosts.js';  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });
</script>

<Spacer height="1.25rem"/>

<div class="main-content" style="padding-top: {navbarHeight}px">
  <div class="content-container">
    <h1 class="title">Blog Posts</h1>

    <div class="post-grid">
      {#each posts as post}
        <a href="/blog/{post.slug}" class="post-card-link">
          <div class="post-card">
            <img src={post.image} alt={post.title} class="post-image" />
            <div class="post-content">
              <h2 class="post-title">{post.title}</h2>
              <p class="post-date">{post.date}</p>
              <p class="post-author">By {post.author}</p>
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
    transition: padding-top 0.3s ease-in-out;
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  .title {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    color: var(--color-text-primary);
    text-align: center;
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
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .post-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  .post-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .post-content {
    padding: 1.5rem;
  }

  .post-title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--color-text-primary);
  }

  .post-date, .post-author {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    margin-bottom: 0.5rem;
  }

  .post-excerpt {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .read-more {
    display: inline-block;
    font-weight: 600;
    color: var(--color-text-primary);
  }

  @media (max-width: 768px) {
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