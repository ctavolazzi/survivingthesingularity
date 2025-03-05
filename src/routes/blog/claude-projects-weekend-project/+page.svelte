<script>
    import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
    import Spacer from '$lib/components/Spacer.svelte';
    import { post } from '$lib/data/blog-posts/claude-projects-weekend-project/index.js';
    import { marked } from 'marked';
    import RecommendedContent from '$lib/components/RecommendedContent.svelte';

    const renderer = new marked.Renderer();
    renderer.link = (href, title, text) => {
      if (typeof href === 'object' && href.href) {
        href = href.href;
      }

      if (typeof href === 'string' && (href.includes('youtube.com') || href.includes('youtu.be'))) {
        const videoId = href.includes('youtube.com') ? href.split('v=')[1] : href.split('/').pop();
        return `<YouTubeVidBox videoId="${videoId}" title="${text}" />`;
      }
      return `<a href="${href}" title="${title || ''}" target="_blank" rel="noopener noreferrer">${text}</a>`;
    };

    let htmlContent = marked(post.content, { renderer });

    const recommendedVideos = [
      {
        id: "GYBT66bPfu8",
        title: "Is the Gaming Industry Doomed?: Google's AI Generates Playable DOOM in Real-Time Frame-by-Frame"
      },
      {
        id: "PNqwvJCz_2w",
        title: "Game Over? Voice Actors vs AI"
      },
      {
        id: "YLo7EH2zsW0",
        title: "AI Plays Minecraft: Voyager - An Open-Ended Embodied Agent with Large Language Models"
      }
    ];
</script>

<svelte:head>
    <title>{post.title} | Surviving the Singularity</title>
    <meta name="description" content="Ready to supercharge your AI workflow? Join us for a weekend challenge exploring Claude Projects, a powerful new feature that's transforming how we interact with AI." />
    <meta property="og:title" content={post.title} />
    <meta property="og:description" content="Ready to supercharge your AI workflow? Join us for a weekend challenge exploring Claude Projects, a powerful new feature that's transforming how we interact with AI." />
    <meta property="og:image" content={post.imageUrl} />
    <meta property="og:type" content="article" />
    <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="blog-post">
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">8 min read</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
      </div>
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src={post.imageUrl}
        alt={post.title}
        class="w-full h-auto"
        loading="lazy"
        decoding="async"
      />
    </div>

    <div class="content">
      <p class="lead">
        Ready to supercharge your AI workflow? Join us for a weekend challenge exploring Claude Projects, a powerful new feature that's transforming how we interact with AI.
      </p>

      <div class="blog-content">
        {@html htmlContent}
      </div>
    </div>
  </article>

  <Spacer height="2rem" />

  <div class="recommended-content-section">
    <RecommendedContent
      title="View more content like this"
      description="Here are some more videos that dive deeper into AI and gaming"
      videos={recommendedVideos}
    />
  </div>

  <Spacer height="2rem" />

  <div class="newsletter-section">
    <NewsletterSignup />
  </div>
</div>

<style>
  .blog-post {
    min-height: 100vh;
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
  }

  .featured-image-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: contain;
    max-height: 80vh; /* Limit height on large screens */
  }

  .content {
    font-size: 1.125rem;
    line-height: 1.75;
  }

  .lead {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-bottom: 2rem;
  }

  .blog-content :global(h1), .blog-content :global(h2), .blog-content :global(h3) {
    color: #ff7708;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-weight: bold;
  }

  .blog-content :global(h1) {
    font-size: 2.25rem;
  }

  .blog-content :global(h2) {
    font-size: 1.875rem;
  }

  .blog-content :global(h3) {
    font-size: 1.5rem;
  }

  .blog-content :global(p) {
    margin-bottom: 1rem;
    line-height: 1.625;
    color: var(--color-text-secondary);
  }

  .blog-content :global(ul), .blog-content :global(ol) {
    padding-left: 1.5em;
    margin-left: 0;
    margin-bottom: 1.5rem;
  }

  .blog-content :global(li) {
    margin-bottom: 0.5em;
    color: var(--color-text-secondary);
  }

  .blog-content :global(ul) {
    list-style-type: disc;
  }

  .blog-content :global(ol) {
    list-style-type: decimal;
  }

  .blog-content :global(a) {
    color: #3b82f6;
    text-decoration: underline;
  }

  .blog-content :global(a:hover) {
    color: #2563eb;
  }

  .blog-content :global(img) {
    max-width: 100%;
    height: auto;
    margin: 1.5rem auto;
    display: block;
    border-radius: 8px;
  }

  .blog-content :global(blockquote) {
    border-left: 4px solid var(--color-primary);
    padding-left: 1rem;
    margin: 2rem 0;
    font-style: italic;
    color: var(--color-text-secondary);
  }

  .newsletter-section, .recommended-content-section {
    max-width: 4xl;
    margin: 0 auto;
    padding: 0 1rem;
  }

  /* Dark mode adjustments */
  :global(.dark) .blog-post {
    background-color: var(--color-bg-primary-dark);
    color: var(--color-text-primary-dark);
  }
</style>
