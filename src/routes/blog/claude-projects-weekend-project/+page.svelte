<script>
    import Spacer from '$lib/components/Spacer.svelte';
    import { post } from '$lib/data/blog-posts/claude-projects-weekend-project/index.js';
    import { marked } from 'marked';
    import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
    import SkoolGroup from '$lib/components/SkoolGroup.svelte';
    import RecommendedContent from '$lib/components/RecommendedContent.svelte';

    const renderer = new marked.Renderer();
    renderer.link = (href, title, text) => {
      console.log('Link renderer:', { href, title, text });
      
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

    function handleBackToBlog() {
      window.history.back();
    }

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
    <title>{post.title} | Your Blog Name</title>
    <meta name="description" content={post.excerpt} />
    <meta property="og:title" content={post.title} />
    <meta property="og:description" content={post.excerpt} />
    <meta property="og:image" content={post.imageUrl} />
    <meta property="og:type" content="article" />
    <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="main-content">
  <div class="content-container">
    <h1 class="text-4xl font-bold mb-4 text-[var(--color-text-primary)]">{post.title}</h1>
    <p class="text-[var(--color-text-secondary)] italic mb-6">{post.date} - {post.author}</p>
    
    <div class="button-container">
      <button class="big-button" on:click={handleBackToBlog}>← Back to Blog List</button>
    </div>

    <img src={post.imageUrl} alt="Blog post header" class="w-full max-w-2xl h-auto mb-6 rounded mx-auto" />

    <div class="blog-content">
      {@html htmlContent}
    </div>

    <Spacer height="2rem"/>
    <RecommendedContent 
      title="View more content like this"
      description="Here are some more videos that dive deeper into AI and gaming"
      videos={recommendedVideos}
    />

    <Spacer height="2rem"/>
    <div class="button-container">
      <button class="big-button" on:click={handleBackToBlog}>← Back to Blog List</button>
    </div>

    <Spacer height="1rem"/>

    <NewsletterSignup />
    <Spacer height="1rem"/>
    <SkoolGroup />
  </div>

  <Spacer height="2rem"/>

  <div class="button-container">
    <button class="big-button" on:click={handleBackToBlog}>← Back to Blog List</button>
  </div>

  <Spacer height="1rem"/>

  <NewsletterSignup />
  <Spacer height="1rem"/>
  <SkoolGroup />
</div>

<style>
  .main-content {
    padding-top: 50px; /* Adjust this value if needed */
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  .button-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 1rem 0;
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
    transition: all 0.3s ease;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    max-width: 300px;
  }

  .big-button:hover {
    background-color: #f8f9fa;
    border-color: #34495e;
    color: #34495e;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }

  :global(.dark) .big-button {
    background-color: #2c3e50;
    color: #ffffff;
    border-color: #34495e;
  }

  :global(.dark) .big-button:hover {
    background-color: #34495e;
    border-color: #4a6785;
    color: #ffffff;
  }

  .blog-content :global(h1) {
    font-size: 2.25rem;
    font-weight: bold;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  .blog-content :global(h2) {
    font-size: 1.875rem;
    font-weight: bold;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  .blog-content :global(h3) {
    font-size: 1.5rem;
    font-weight: bold;
    margin-top: 1rem; /* Fixed: added 'rem' */
  }

  .blog-content :global(p) {
    margin-bottom: 1rem;
    line-height: 1.625;
    color: var(--color-text-secondary);
  }

  .blog-content :global(ul), .blog-content :global(ol) {
    padding-left: 1.5em;
    margin-left: 0;
  }

  .blog-content :global(li) {
    margin-bottom: 0.5em;
  }

  .blog-content :global(ul) {
    list-style-type: disc;
  }

  .blog-content :global(ol) {
    list-style-type: none;
    counter-reset: custom-counter;
  }

  .blog-content :global(ol > li) {
    display: flex;
    align-items: flex-start;
  }

  .blog-content :global(ol > li::before) {
    content: counter(custom-counter) ") ";
    counter-increment: custom-counter;
    flex: 0 0 1.5em;
    margin-right: 0.5em;
    text-align: right;
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
    margin: 1rem auto;
    display: block;
    border-radius: 8px;
  }

  @media (max-width: 768px) {
    .big-button {
      max-width: none;
      width: 100%;
    }
  }
</style>
