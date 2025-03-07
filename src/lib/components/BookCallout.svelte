<script>
  import bookCoverImage from '$lib/images/Surviving-the-Singularity-Cover.png';

  // Props
  export let title = "Navigate the Path to Singularity";
  export let description = "Get the insights and strategies you need to prepare for the technological changes that will reshape our world.";
  export let buttonText = "Explore the Book";
  export let buttonLink = "/sample"; // Default to sample page
  export let imageSrc = bookCoverImage; // Use the imported image
  export let shareLink = "https://survivingthesingularity.com"; // Default share link
  export let showShareButton = true; // Whether to show the share button
</script>

<div class="book-callout p-5 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 shadow-2xl rounded-lg max-w-3xl mx-auto my-2 border border-gray-700/50 backdrop-blur-sm">
  <div class="flex flex-col md:flex-row gap-6">
    <!-- Book cover image with enhanced glow effect -->
    <div class="flex-shrink-0 relative">
      <div class="absolute inset-0 bg-blue-500/30 opacity-30 blur-2xl rounded-full"></div>
      <img src={imageSrc} alt="Book cover" class="w-40 md:w-48 h-auto rounded-md shadow-[0_10px_25px_rgba(59,130,246,0.3)] mx-auto md:mx-0 relative z-10" />
    </div>

    <!-- Content with improved typography and spacing -->
    <div class="flex flex-col justify-center">
      <h2 class="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-100 mb-3 tracking-wide">
        {title}
      </h2>
      <p class="text-gray-300 mb-5 text-base md:text-lg leading-relaxed">
        {description}
      </p>

      <!-- Enhanced features list with animated entry -->
      <div class="grid grid-cols-1 gap-3 mb-6">
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

      <!-- Button group with two buttons side-by-side -->
      <div class="flex flex-row gap-3 flex-wrap">
        <a href={buttonLink} class="button-link inline-flex items-center px-6 py-3 text-base font-medium text-center text-white bg-blue-600 rounded-lg relative overflow-hidden">
          <span class="relative z-10">{buttonText}</span>
          <svg class="w-5 h-5 ml-2 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
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
            class="share-button inline-flex items-center px-6 py-3 text-base font-medium text-center text-blue-400 bg-blue-900/30 border border-blue-800/50 rounded-lg relative overflow-hidden hover:bg-blue-800/40 transition-colors"
          >
            <span class="relative z-10">Share the Book</span>
            <svg class="w-5 h-5 ml-2 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
            </svg>
          </button>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .book-callout {
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 30px rgba(59, 130, 246, 0.15) inset;
  }

  /* Fix for cursor flickering */
  .button-link, .share-button {
    position: relative;
    z-index: 5;
    cursor: pointer;
    white-space: nowrap;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .button-link:hover, .share-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }

  .share-button {
    backdrop-filter: blur(5px);
  }

  /* Mobile optimization */
  @media (max-width: 768px) {
    .book-callout {
      padding: 1.5rem;
      margin: 1rem 0;
    }
  }

  /* Ensure buttons stay side by side on very small screens */
  @media (max-width: 380px) {
    .button-link, .share-button {
      padding: 0.75rem 1rem;
      font-size: 0.875rem;
    }

    .button-link svg, .share-button svg {
      width: 1rem;
      height: 1rem;
    }
  }
</style>