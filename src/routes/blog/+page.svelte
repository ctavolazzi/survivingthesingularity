<!-- src/routes/blog/+page.svelte -->
<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import { onMount } from 'svelte';

  const posts = [
    {
      id: "singularity-express",
      title: "The Singularity Express Arrives at the Station",
      date: "2024-08-08",
      excerpt: "Choo Choo, Motherfuckers. The Singularity Express just pulled into the station, and it's one hell of a ride."
    },
    // Add more posts here as needed
  ];

  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });
</script>

<Spacer height="1.25rem"/>

<div class="main-content" style="padding-top: {navbarHeight}px">
  <div class="content-container">
    <h1 class="title">Blog Posts</h1>

    <ul class="post-list">
      {#each posts as post}
        <li class="post-item">
          <h2 class="post-title">
            <a href="/blog/{post.id}" class="post-link">{post.title}</a>
          </h2>
          <p class="post-date">{post.date}</p>
          <p class="post-excerpt">{post.excerpt}</p>
          <a href="/blog/{post.id}" class="read-more">Read more →</a>
        </li>
      {/each}
    </ul>
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

  .post-list {
    list-style-type: none;
    padding: 0;
  }

  .post-item {
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 2rem;
    margin-bottom: 2rem;
  }

  .post-title {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }

  .post-link {
    color: var(--color-text-primary);
    text-decoration: none;
    transition: color 0.3s ease;
  }

  .post-link:hover {
    color: var(--color-text-secondary);
  }

  .post-date {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    margin-bottom: 1rem;
  }

  .post-excerpt {
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .read-more {
    display: inline-block;
    font-weight: 600;
    color: var(--color-text-primary);
    text-decoration: none;
    transition: color 0.3s ease;
  }

  .read-more:hover {
    color: var(--color-text-secondary);
  }

  @media (max-width: 768px) {
    .title {
      font-size: 2rem;
    }

    .post-title {
      font-size: 1.5rem;
    }

    .post-excerpt {
      font-size: 1rem;
    }
  }

  :global(.dark) .post-link {
    color: #e5e7eb;
  }

  :global(.dark) .post-link:hover {
    color: #d1d5db;
  }

  :global(.dark) .post-date {
    color: #9ca3af;
  }

  :global(.dark) .post-excerpt {
    color: #d1d5db;
  }

  :global(.dark) .read-more {
    color: #e5e7eb;
  }

  :global(.dark) .read-more:hover {
    color: #d1d5db;
  }
</style>