<script>
    import Spacer from '$lib/components/Spacer.svelte';
    import { post } from '$lib/data/blog-posts/claude-projects-weekend-project/index.js';
    import { marked } from 'marked';
    import RecommendedContent from '$lib/components/RecommendedContent.svelte';
    import SocialShare from '$lib/components/SocialShare.svelte';

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
      <button
        class="back-button mb-4 flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={() => window.history.back()}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">8 min read</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
      </div>

      <SocialShare
        title={post.title}
        description="Ready to supercharge your AI workflow? Join us for a weekend challenge exploring Claude Projects, a powerful new feature that's transforming how we interact with AI."
        image={post.imageUrl}
      />
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

  <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700 max-w-4xl mx-auto px-4">
    <div class="flex justify-between items-center mb-8">
      <button
        class="back-button flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={() => window.history.back()}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>

      <div class="bottom-share">
        <SocialShare
          title={post.title}
          description="Ready to supercharge your AI workflow? Join us for a weekend challenge exploring Claude Projects, a powerful new feature that's transforming how we interact with AI."
          image={post.imageUrl}
        />
      </div>
    </div>

    <div class="recommended-content-section mb-8">
      <RecommendedContent
        title="View more content like this"
        description="Here are some more videos that dive deeper into AI and gaming"
        videos={recommendedVideos}
      />
    </div>

    <Spacer height="2rem" />
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
    border-radius: 0.5rem;
    background-color: rgba(15, 23, 42, 0.05);
    margin-bottom: 2rem;
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
    max-height: 80vh;
    border-radius: 0.5rem;
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

  .newsletter-container {
    max-width: 4xl;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Dark mode adjustments */
  :global(.dark) .blog-post {
    background-color: var(--color-bg-primary-dark);
    color: var(--color-text-primary-dark);
  }

  .bottom-share :global(.share-container) {
    margin: 0;
  }

  @media (max-width: 640px) {
    .bottom-share {
      display: none; /* Hide bottom share on mobile to save space */
    }
  }

  .back-button {
    display: inline-flex;
    align-items: center;
    transition: all 0.2s ease;
  }

  .back-button:hover {
    transform: translateX(-2px);
  }
</style>
