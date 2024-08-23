<script>
    import BlogPost from './BlogPost.svelte';
    export let post;
  </script>
  
  <!-- <hr class="section-divider"> -->
  
  <div class="latest-news-container">
    <h2 class="heading-text">Latest News</h2>
    <div class="news-card">
      <BlogPost {post} />
    </div>
  </div>
  
  <!-- <hr class="section-divider"> -->
  
  <style>
    .latest-news-container {
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1rem;
    }
  
    .heading-text {
      font-size: 2rem;
      font-weight: 600;
      text-align: center;
      margin-bottom: 1.5rem;
      color: var(--color-text-primary);
    }
  
    .news-card {
      background-color: #ffffff;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      padding: 2rem;
      margin-top: 1rem;
      border: 1px solid #e5e7eb;
    }
  
    /* .section-divider {
      border: 0;
      height: 1px;
      background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
      margin: 2rem auto;
      max-width: 80%;
    } */
  
    :global(.dark) .heading-text {
      color: #e5e7eb;
    }
  
    :global(.dark) .news-card {
      background-color: #2c3e50;
      border-color: #4a6785;
    }
  
    /* :global(.dark) .section-divider {
      background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
    } */
  </style>