<script>
  import bookCoverImage from '$lib/images/Surviving-the-Singularity-Cover.png';
  import bookCoverImageWebP from '$lib/images/Surviving-the-Singularity-Cover.webp';
  import SafeResponsiveImage from './SafeResponsiveImage.svelte';

  // Props
  export let title = "Navigate the Path to Singularity";
  export let imageSrc = bookCoverImage; // Use the imported image
  export let imageWebPSrc = bookCoverImageWebP; // WebP version
  export let subtitle = "Want to know more?";
  export let description = "Get the insights and strategies you need to prepare for the technological changes that will reshape our world.";
  export let buttonText = "Explore the Book";
  export let buttonLink = "/sample"; // Default to sample page
  export let shareLink = "https://survivingthesingularity.com"; // Default share link
  export let showShareButton = true; // Whether to show the share button
</script>

<div class="book-callout p-5 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 shadow-2xl rounded-lg max-w-3xl mx-auto my-2 border border-gray-700/50 backdrop-blur-sm">
  <div class="flex flex-col gap-6">
    <!-- Title at the top -->
    <div class="text-center">
      <h2 class="book-callout-title text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-100 mb-3 tracking-wide">
        {title}
      </h2>
    </div>

    <!-- Book cover image right below the title -->
    <div class="flex justify-center">
      <div class="flex-shrink-0 relative">
        <div class="absolute inset-0 bg-blue-500/30 opacity-30 blur-2xl rounded-full"></div>
        <div class="book-glow-effect"></div>
        <SafeResponsiveImage
          src={imageSrc}
          srcWebp={imageWebPSrc}
          srcset=""
          srcsetWebp=""
          alt="Book cover"
          class="w-40 md:w-48 h-auto rounded-md shadow-[0_10px_25px_rgba(59,130,246,0.3)] mx-auto relative z-10 transform hover:scale-105 transition-transform duration-300"
        />
      </div>
    </div>

    <!-- Content below the image -->
    <div class="flex flex-col text-center">
      <h3 class="book-callout-subtitle text-xl md:text-2xl font-semibold text-blue-300 mb-2">
        {subtitle}
      </h3>
      <p class="text-gray-300 mb-5 text-base md:text-lg leading-relaxed max-w-2xl mx-auto text-left">
        {description}
      </p>

      <!-- Bullet points - restore original styling -->
      <div class="grid grid-cols-1 gap-3 mb-6 max-w-2xl mx-auto text-left">
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          <span class="text-gray-300">Learn to navigate rapid technological changes</span>
        </div>
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          <span class="text-gray-300">Understand AI's impact on your career & future</span>
        </div>
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          <span class="text-gray-300">Actionable strategies to thrive in the new era</span>
        </div>
      </div>
    </div>

    <!-- Button group side by side -->
    <div class="flex flex-row justify-center gap-3">
      <a href={buttonLink} class="button-link inline-flex items-center justify-center px-4 py-3 text-sm md:text-base font-medium text-center text-white bg-blue-600 rounded-lg relative overflow-hidden">
        <span class="btn-text relative z-10">{buttonText}</span>
        <svg class="w-4 h-4 ml-2 md:w-5 md:h-5 md:ml-2 flex-shrink-0 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
      </a>

      {#if showShareButton}
        <button
          on:click={() => {
            if (navigator.share) {
              navigator.share({
                title: 'Surviving the Singularity',
                text: 'Check out this book about navigating the AI revolution',
                url: shareLink,
              }).catch(err => console.error('Error sharing:', err));
            } else {
              // Fallback - copy to clipboard
              navigator.clipboard.writeText(shareLink);
              alert('Link copied to clipboard!');
            }
          }}
          class="share-button inline-flex items-center justify-center px-4 py-3 text-sm md:text-base font-medium text-center text-blue-400 bg-blue-900/30 border border-blue-800/50 rounded-lg relative overflow-hidden"
        >
          <span class="btn-text relative z-10">Share the Book</span>
          <svg class="w-4 h-4 ml-2 md:w-5 md:h-5 md:ml-2 flex-shrink-0 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
          </svg>
        </button>
      {/if}
    </div>
  </div>
</div>

<style>
  .book-callout {
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 30px rgba(59, 130, 246, 0.15) inset;
    background-image: radial-gradient(circle at top right, rgba(59, 130, 246, 0.1), transparent 70%),
                      radial-gradient(circle at bottom left, rgba(99, 102, 241, 0.1), transparent 70%);
  }

  /* Book glow effect */
  .book-glow-effect {
    position: absolute;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at center, rgba(59, 130, 246, 0.3), transparent 60%);
    filter: blur(20px);
    opacity: 0.6;
    z-index: 5;
    animation: pulse 3s infinite alternate;
  }

  @keyframes pulse {
    0% { opacity: 0.4; transform: scale(0.95); }
    100% { opacity: 0.7; transform: scale(1.05); }
  }

  /* Add responsive title style */
  .book-callout-title {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    line-height: 1.2;
    hyphens: auto; /* Allow hyphenation */
    background-image: linear-gradient(135deg, #fff, #60a5fa);
    -webkit-background-clip: text;
    background-clip: text;
    text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
    margin-bottom: 0.5rem;
  }

  /* Add responsive subtitle style */
  .book-callout-subtitle {
    line-height: 1.2;
    font-size: clamp(1.2rem, 3vw, 1.75rem);
    margin-bottom: 1rem;
    color: #60a5fa;
    text-shadow: 0 0 10px rgba(96, 165, 250, 0.4);
  }

  /* Fix for cursor flickering */
  .button-link, .share-button {
    position: relative;
    z-index: 5;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: clamp(0.75rem, 2vw, 1rem);
    letter-spacing: 0.5px;
    min-width: 140px;
    max-width: 250px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .btn-text {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .button-link::before, .share-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
    z-index: 1;
  }

  .button-link:hover, .share-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
  }

  .button-link {
    background: linear-gradient(to right, #2563eb, #3b82f6);
  }

  .share-button {
    backdrop-filter: blur(5px);
    border: 1px solid rgba(96, 165, 250, 0.3);
  }

  /* Mobile optimization */
  @media (max-width: 768px) {
    .book-callout {
      padding: 1.5rem;
      margin: 1rem 0;
    }

    .book-callout-title {
      font-size: clamp(1.35rem, 4vw, 2rem);
    }

    .book-callout-subtitle {
      font-size: clamp(1.1rem, 3.5vw, 1.5rem);
    }
  }

  /* Ensure buttons stay side by side on very small screens */
  @media (max-width: 380px) {
    .button-link, .share-button {
      padding: 0.5rem 0.75rem;
      min-width: 110px;
      max-width: 160px;
    }

    .button-link svg, .share-button svg {
      width: 0.85rem;
      height: 0.85rem;
      margin-left: 0.25rem;
    }

    /* Create more compact text for ultra small screens */
    @media (max-width: 320px) {
      .button-link, .share-button {
        padding: 0.5rem;
        min-width: 100px;
      }

      .button-link .btn-text {
        max-width: 70px;
      }

      .share-button .btn-text {
        max-width: 70px;
      }
    }

    .book-callout-title {
      font-size: clamp(1.2rem, 3.5vw, 1.5rem);
    }

    .book-callout-subtitle {
      font-size: clamp(1rem, 3vw, 1.2rem);
    }
  }
</style>