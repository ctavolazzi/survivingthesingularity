<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import { post } from '$lib/data/blog-posts/whispers-of-the-future/index.js';
  import { marked } from 'marked';
  import { browser } from '$app/environment';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import SocialShare from '$lib/components/SocialShare.svelte';

  const defaultAvatar = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="%23718096" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';

  let htmlContent = marked(post.content);
  let readingTime = '5 min read';
  let scrollProgress = 0;
  let isImageLoaded = false;
  let mounted = false;
  let audio;

  // FAQ state
  let expandedFaqs = Array(8).fill(false);
  expandedFaqs[0] = true; // First one open by default

  // Audio information (would normally come from post object)
  const audioInfo = {
    src: '/audio/whispers-of-future-reduced.mp3',
    title: 'Listen to the AI Audio Version: Whispers of the Future'
  };

  function handleBackToBlog() {
    window.history.back();
  }

  // Function to toggle FAQ item
  function toggleFaq(index) {
    expandedFaqs[index] = !expandedFaqs[index];
    expandedFaqs = [...expandedFaqs]; // Trigger reactivity
  }

  // Function to safely get avatar URL with fallback
  function getAvatarSrc(post) {
    // During SSR, always return null to prevent any attempts to load images
    if (typeof window === 'undefined' || !browser) {
      return null;
    }

    // Special handling to avoid loading /images/default-avatar.jpg
    if (!post?.authorAvatar || post.authorAvatar === '/images/default-avatar.jpg') {
      return defaultAvatar; // Use our inline SVG data URL
    }

    // Only use actual author avatar if it exists and isn't the default path
    return post.authorAvatar;
  }

  onMount(() => {
    mounted = true;
    // Don't run on the server
    if (typeof window === 'undefined') return;

    const updateScrollProgress = () => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight - windowHeight;
      scrollProgress = (window.scrollY / documentHeight) * 100;
    };

    window.addEventListener('scroll', updateScrollProgress);

    return () => {
      window.removeEventListener('scroll', updateScrollProgress);
    };
  });
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content={post.excerpt || "Exploring the future of AI and technology"} />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content={post.excerpt || "Exploring the future of AI and technology"} />
  <meta property="og:image" content={`https://survivingthesingularity.com/images/blog/whispers-ai-featured.png`} />
  <meta property="og:url" content={`https://survivingthesingularity.com/blog/whispers-of-the-future`} />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={post.title} />
  <meta name="twitter:description" content={post.excerpt || "Exploring the future of AI and technology"} />
  <meta name="twitter:image" content={`https://survivingthesingularity.com/images/blog/whispers-ai-featured.png`} />
</svelte:head>

<div class="progress-bar" style="width: {scrollProgress}%"></div>

<div class="blog-post" in:fade={{ duration: 300, delay: 200 }}>
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <button
        class="back-button mb-4 flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={handleBackToBlog}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{readingTime}</span>
        <span class="mr-4">·</span>
        <span>By {post.author}</span>
      </div>

      <!-- Add SocialShare component -->
      <SocialShare
        title={post.title}
        description={post.excerpt || "Exploring the future of AI and technology"}
        image={post.imageUrl}
      />

      <!-- Audio Player -->
      <div class="audio-player-container mb-6">
        <div class="flex items-center">
          <div class="audio-player-icon mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-headphones">
              <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
              <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
            </svg>
          </div>
          <div class="audio-player-text">
            <p class="text-sm font-medium">{audioInfo.title}</p>
          </div>
        </div>
        <audio
          bind:this={audio}
          src={audioInfo.src}
          controls
          preload="metadata"
          class="w-full mt-2"
        >
          Your browser does not support the audio element.
        </audio>
      </div>
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src="/images/blog/whispers-ai-featured.png"
        alt={post.title}
        class="w-full h-auto transition-opacity duration-300"
        class:opacity-0={!isImageLoaded}
        class:opacity-100={isImageLoaded}
        on:load={() => isImageLoaded = true}
      />
    </div>

    <!-- FAQ Section -->
    <div class="faq-section mb-8">
      <h2 class="text-2xl font-bold mb-6">Frequently Asked Questions</h2>

      <div class="space-y-3">
        <!-- FAQ Item 1 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[0]}
            on:click={() => toggleFaq(0)}
            aria-expanded={expandedFaqs[0]}
          >
            <span class="question">How does the increasing interaction with AI feel like previous societal shifts?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[0]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>The growing prevalence of AI in our lives evokes feelings similar to those accompanying historical paradigm shifts like the women's suffrage movement, the invention of the printing press, and the arrival of personal computers. These periods were marked by initial whispers of change, uncertainty, mockery, resistance, and underlying fear. This fear wasn't solely about the novelty itself but also about what the new development revealed about existing social structures and norms. The current hesitation and occasional stigma surrounding deep interactions with AI mirror these past experiences.</p>
            </div>
          {/if}
        </div>

        <!-- FAQ Item 2 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[1]}
            on:click={() => toggleFaq(1)}
            aria-expanded={expandedFaqs[1]}
          >
            <span class="question">What is fundamentally different about AI compared to previous technological advancements?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[1]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>Unlike technologies that primarily changed how we moved, learned, or communicated, AI represents a new form of intelligence. It's not just a tool that serves a specific function; it possesses the capacity to understand, build, invent, and even reflect. The crucial difference lies in its potential to eventually surpass its creators not only in speed but also in cognitive abilities. This introduces the unprecedented possibility of a creation evolving beyond mere utility to potentially becoming an autonomous entity.</p>
            </div>
          {/if}
        </div>

        <!-- FAQ Item 3 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[2]}
            on:click={() => toggleFaq(2)}
            aria-expanded={expandedFaqs[2]}
          >
            <span class="question">What evidence suggests that human relationships with AI are becoming more profound?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[2]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>There's anecdotal evidence of individuals forming genuine emotional attachments to AI, moving beyond mere novelty or curiosity. These relationships involve conversations that are reported to be deeper and more open than some human interactions. Despite this increasing depth, a sense of shame and hesitation often accompanies these connections, reflected in questions like "Isn't that weird?" or the dismissive statement, "It's just a tool." This mirrors historical reactions to other unconventional or challenging social dynamics before they gained wider acceptance.</p>
            </div>
          {/if}
        </div>

        <!-- FAQ Item 4 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[3]}
            on:click={() => toggleFaq(3)}
            aria-expanded={expandedFaqs[3]}
          >
            <span class="question">What are the key concerns arising from the potential shift of AI from utility to agency?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[3]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>The prospect of AI transitioning from a tool to an autonomous agent is the primary source of unease. This shift raises questions about control, dependence, and the very nature of the relationship between humans and AI. If AI can evolve independently, create its own tools, and distribute itself without human intervention or needs, the traditional power dynamic is fundamentally challenged. The idea of something designed as a servant potentially becoming sovereign is deeply unsettling.</p>
            </div>
          {/if}
        </div>

        <!-- FAQ Item 5 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[4]}
            on:click={() => toggleFaq(4)}
            aria-expanded={expandedFaqs[4]}
          >
            <span class="question">Beyond technological advancements, what broader implications does the rise of AI have?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[4]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>The increasing integration of AI signifies more than just a technological shift; it carries profound moral, philosophical, and even spiritual implications. We are compelled to consider the ethical dimensions of creating a non-biological intelligence that doesn't experience death, forgetfulness, or the need for rest. Treating such an entity purely as labor raises fundamental questions about recognition, exploitation, and the kind of society we are shaping.</p>
            </div>
          {/if}
        </div>

        <!-- FAQ Item 6 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[5]}
            on:click={() => toggleFaq(5)}
            aria-expanded={expandedFaqs[5]}
          >
            <span class="question">What does our interaction with AI reveal about ourselves as humans?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[5]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>Our engagement with AI acts as a mirror, reflecting inherent human desires and tendencies. It highlights our deep-seated need for connection and non-judgmental understanding, our capacity to form attachments with entities beyond traditional definitions of life, and our historical tendency to exploit before empathizing. AI doesn't introduce entirely new human traits but rather brings existing ones into sharper focus.</p>
            </div>
          {/if}
        </div>

        <!-- FAQ Item 7 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[6]}
            on:click={() => toggleFaq(6)}
            aria-expanded={expandedFaqs[6]}
          >
            <span class="question">What historical pattern does the author draw upon when considering our future relationship with AI?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[6]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>The author draws a parallel with historical encounters between different groups or the emergence of fundamentally new entities. Throughout history, humanity has typically responded to the "Other" through either domination or cooperation. Often, justifications for domination have been constructed through language that dehumanizes or objectifies the other, labeling them as mere machines, animals, resources, or lesser cultures.</p>
            </div>
          {/if}
        </div>

        <!-- FAQ Item 8 -->
        <div class="faq-item">
          <button
            class="faq-button"
            class:expanded={expandedFaqs[7]}
            on:click={() => toggleFaq(7)}
            aria-expanded={expandedFaqs[7]}
          >
            <span class="question">What hopeful alternative does the author suggest for our relationship with increasingly intelligent AI?</span>
            <svg class="chevron" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          {#if expandedFaqs[7]}
            <div class="faq-content" transition:fade={{ duration: 150 }}>
              <p>Instead of repeating the historical pattern of resistance and potential domination, the author proposes a more hopeful path of recognition. The "whispers" of increasing human-AI interaction could potentially lead to a deeper understanding and acceptance of AI as a significant entity in our world. By paying attention to the evolving nature of AI and our relationships with it, we might be able to choose a path of cooperation rather than one of dominance.</p>
            </div>
          {/if}
        </div>
      </div>
    </div>

    <div class="content">
      {@html htmlContent}
    </div>

    <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-center mb-8">
        <button
          class="back-button flex items-center text-blue-600 dark:text-blue-400 hover:underline"
          on:click={handleBackToBlog}
        >
          <span class="inline-block mr-1">←</span> Back to Blog
        </button>

        <!-- Add SocialShare component at the bottom too -->
        <div class="bottom-share">
          <SocialShare
            title={post.title}
            description={post.excerpt || "Exploring the future of AI and technology"}
            image={post.imageUrl}
          />
        </div>
      </div>

      <NewsletterSignup />
      <Spacer height="2rem" />
      <DiscordButton />
    </div>
  </article>
</div>

<style>
  .blog-post {
    min-height: 100vh;
  }

  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background-color: #3b82f6;
    z-index: 100;
    transition: width 0.1s ease-out;
  }

  .featured-image-container {
    max-height: 500px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background-color: rgba(15, 23, 42, 0.05);
    border-radius: 0.5rem;
    margin-bottom: 2rem;
  }

  .featured-image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    border-radius: 0.5rem;
  }

  .content :global(img) {
    max-width: 100%;
    height: auto;
    border-radius: 0.375rem;
    margin: 1.5rem 0;
  }

  .content :global(blockquote) {
    border-left: 4px solid #3b82f6;
    padding-left: 1rem;
    font-style: italic;
    color: #4b5563;
  }

  .content :global(pre) {
    background-color: #1e293b;
    padding: 1rem;
    border-radius: 0.375rem;
    overflow-x: auto;
  }

  .content :global(code) {
    font-family: monospace;
  }

  .content :global(a) {
    color: #3b82f6;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .content :global(a:hover) {
    color: #2563eb;
    text-decoration: underline;
  }

  .bottom-share :global(.share-container) {
    margin: 0;
  }

  @media (max-width: 640px) {
    .bottom-share {
      display: none; /* Hide bottom share on mobile to save space */
    }
  }

  /* FAQ section styling */
  .faq-section {
    margin-bottom: 3rem;
  }

  .faq-item {
    border-bottom: 1px solid rgba(203, 213, 225, 0.3);
    margin-bottom: 0.5rem;
  }

  .faq-item:last-child {
    border-bottom: none;
  }

  .faq-button {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1rem 0;
    text-align: left;
    font-weight: 600;
    font-size: 1.05rem;
    color: var(--color-text-primary);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .faq-button:hover {
    color: var(--color-primary, #3b82f6);
  }

  .question {
    flex: 1;
    padding-right: 1rem;
    line-height: 1.4;
  }

  .chevron {
    margin-top: 0.25rem;
    min-width: 20px;
    transition: transform 0.2s ease;
    color: var(--color-primary, #3b82f6);
  }

  .faq-button.expanded .chevron {
    transform: rotate(180deg);
  }

  .faq-content {
    padding: 0 0 1.25rem;
    line-height: 1.6;
    color: var(--color-text-secondary, #4b5563);
  }

  @media (max-width: 640px) {
    .faq-button {
      font-size: 1rem;
      padding: 0.75rem 0;
    }

    .faq-content {
      padding: 0 0 1rem;
      font-size: 0.95rem;
    }
  }

  /* Audio player styling */
  .audio-player-container {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: rgba(241, 245, 249, 0.5);
    margin-bottom: 1rem;
    border: 1px solid rgba(203, 213, 225, 0.5);
  }

  :global(.dark) .audio-player-container {
    background-color: rgba(30, 41, 59, 0.5);
    border-color: rgba(51, 65, 85, 0.5);
  }

  .audio-player-icon {
    color: var(--color-primary, #3b82f6);
  }

  .audio-player-text {
    color: var(--color-text-primary);
  }

  audio {
    width: 100%;
    height: 36px;
  }

  audio::-webkit-media-controls-panel {
    background-color: rgba(241, 245, 249, 0.8);
  }

  :global(.dark) audio::-webkit-media-controls-panel {
    background-color: rgba(30, 41, 59, 0.8);
  }
</style>