<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';

  const post = {
    title: 'DARPA Seeks Plans for Large Bio-Mechanical Space Structures',
    date: '2024-03-04',
    author: 'Christopher Tavolazzi',
    image: 'https://futurism.com/_next/image?url=https%3A%2F%2Fwordpress-assets.futurism.com%2F2025%2F02%2Fdarpa-requests-plans-large-bio-mechanical-space-structures.jpg&w=2048&q=75',
    readingTime: '5 min read'
  };

  let isImageLoaded = false;
  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

<div class="blog-post" in:fade={{ duration: 300, delay: 200 }}>
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{post.readingTime}</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
      </div>
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src={post.image}
        alt={post.title}
        class="w-full h-auto transition-opacity duration-300"
        class:opacity-0={!isImageLoaded}
        class:opacity-100={isImageLoaded}
        on:load={() => isImageLoaded = true}
      />
    </div>

    <div class="content">
      <p class="lead">
        DARPA has issued a request for information on building massive biological structures in space,
        exploring a sci-fi future where space infrastructure might be grown rather than assembled.
      </p>

      <h2>The Future of Space Construction</h2>
      <p>
        In a move that seems straight out of science fiction, DARPA (Defense Advanced Research Projects Agency)
        is exploring the possibility of growing large-scale structures in space using biological and
        bio-mechanical processes. This groundbreaking initiative could revolutionize how we build and
        maintain space infrastructure.
      </p>

      <h2>Key Points of the Initiative</h2>
      <ul>
        <li>Bio-mechanical hybrid structures that can self-repair and adapt</li>
        <li>Reduced launch costs by growing structures in space</li>
        <li>Potential applications in space stations, satellites, and deep space missions</li>
        <li>Integration of living materials with mechanical components</li>
      </ul>

      <h2>Implications for Space Exploration</h2>
      <p>
        This innovative approach to space construction could solve many of the current challenges in space
        exploration and colonization. By utilizing biological processes, we might be able to create
        structures that are not only self-maintaining but also capable of adapting to changing conditions
        in space.
      </p>

      <blockquote>
        "The integration of biological processes with space construction could be the key to sustainable
        long-term presence in space." - DARPA spokesperson
      </blockquote>

      <h2>Technical Challenges</h2>
      <p>
        While the concept is promising, there are significant technical challenges to overcome:
      </p>
      <ul>
        <li>Maintaining biological processes in the harsh space environment</li>
        <li>Ensuring structural integrity and stability</li>
        <li>Controlling growth and development in zero gravity</li>
        <li>Integration with existing space technologies</li>
      </ul>

      <h2>Looking Ahead</h2>
      <p>
        As we continue to push the boundaries of space exploration, innovations like bio-mechanical
        structures could play a crucial role in establishing a permanent human presence beyond Earth.
        The success of this initiative could mark the beginning of a new era in space construction
        and exploration.
      </p>
    </div>
  </article>

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
    max-height: 500px;
    overflow: hidden;
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
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

  blockquote {
    border-left: 4px solid var(--color-primary);
    padding-left: 1rem;
    margin: 2rem 0;
    font-style: italic;
    color: var(--color-text-secondary);
  }

  .newsletter-section {
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