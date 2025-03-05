<script>
    export let post;
    import { goto } from '$app/navigation';

    function handleReadBlog() {
        goto(`/blog/${post.slug}`);
    }
</script>

  <div class="blog-post-container">
    <h2 class="blog-post-title">{post.title}</h2>
    <div class="blog-post-image-container">
      <img src={post.imageUrl} alt={post.title} class="blog-post-image" loading="lazy" decoding="async"/>
    </div>
    <p class="blog-post-description">{post.excerpt}</p>
    <button class="big-button" on:click={handleReadBlog}>Read the Blog</button>
  </div>

  <style>
    .blog-post-container {
      text-align: center;
      margin: 2rem 0;
    }

    .blog-post-title {
      font-size: 1.5rem;
      font-weight: bold;
      color: var(--color-text-primary);
    }

    .blog-post-image-container {
      display: flex;
      justify-content: center;
      margin: 1rem 0;
    }

    .blog-post-image {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .blog-post-description {
      font-size: 1rem;
      font-weight: bold;
      color: var(--color-text-secondary);
      margin: 0.5rem 0 1rem;
    }

    .big-button {
      flex: 1;
      font-weight: 600;
      font-size: 1.1rem;
      background-color: #ffffff;
      border: 1px solid #2c3e50;
      border-radius: 6px;
      color: #2c3e50;
      padding: 0.75rem 1rem;
      cursor: pointer;
      transition: background-color 0.2s ease;
      text-align: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  </style>