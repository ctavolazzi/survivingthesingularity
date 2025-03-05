<script>
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import bookCoverImage from '$lib/images/Surviving-the-Singularity-Cover.png';

  // Props
  export let title = "Navigate the Path to Singularity";
  export let description = "Get the insights and strategies you need to prepare for the technological changes that will reshape our world.";
  export let buttonText = "Explore the Book";
  export let buttonLink = "/sample"; // Default to sample page
  export let imageSrc = bookCoverImage; // Use the imported image

  let visible = false;
  let bookCalloutElement;

  onMount(() => {
    // Check if element is in viewport using the bound reference
    if (bookCalloutElement) {
      const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
          visible = true;
          observer.disconnect();
        }
      }, { threshold: 0.2 });

      observer.observe(bookCalloutElement);
    }
  });
</script>

<div bind:this={bookCalloutElement} class="book-callout p-5 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 shadow-2xl rounded-lg max-w-3xl mx-auto my-2 border border-gray-700/50 backdrop-blur-sm">
  {#if visible}
    <div class="flex flex-col md:flex-row gap-6" in:fade={{ duration: 800 }}>
      <!-- Book cover image with enhanced glow effect -->
      <div class="flex-shrink-0 relative" in:fly={{ y: 20, duration: 800, delay: 200 }}>
        <div class="absolute inset-0 bg-blue-500/30 opacity-30 blur-2xl rounded-full"></div>
        <img src={imageSrc} alt="Book cover" class="w-40 md:w-48 h-auto rounded-md shadow-[0_10px_25px_rgba(59,130,246,0.3)] mx-auto md:mx-0 relative z-10 transform transition-all duration-500 hover:scale-105 hover:shadow-[0_15px_30px_rgba(59,130,246,0.4)]" />
      </div>

      <!-- Content with improved typography and spacing -->
      <div class="flex flex-col justify-center">
        <h2 class="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-100 mb-3 tracking-wide" in:fly={{ y: 20, duration: 800, delay: 300 }}>
          {title}
        </h2>
        <p class="text-gray-300 mb-5 text-base md:text-lg leading-relaxed" in:fly={{ y: 20, duration: 800, delay: 400 }}>
          {description}
        </p>

        <!-- Enhanced features list with animated entry -->
        <div class="grid grid-cols-1 gap-3 mb-6" in:fly={{ y: 20, duration: 800, delay: 500 }}>
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

        <!-- Simplified action button -->
        <div class="flex" in:fly={{ y: 20, duration: 800, delay: 600 }}>
          <a href={buttonLink} class="button-link inline-flex items-center px-6 py-3 text-base font-medium text-center text-white bg-gradient-to-r from-blue-600 via-blue-500 to-blue-600 rounded-lg hover:from-blue-500 hover:via-blue-400 hover:to-blue-500 focus:ring-4 focus:outline-none focus:ring-blue-300 shadow-lg shadow-blue-500/30 transition-all duration-300 hover:shadow-blue-500/50 hover:translate-y-[-2px] relative overflow-hidden group">
            <span class="relative z-10">{buttonText}</span>
            <svg class="w-5 h-5 ml-2 relative z-10 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
            <span class="button-overlay absolute top-0 left-0 w-full h-full bg-gradient-to-r from-blue-400 to-blue-300 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></span>
          </a>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .book-callout {
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 30px rgba(59, 130, 246, 0.15) inset;
  }

  .book-callout::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, rgba(17, 24, 39, 0) 70%);
    z-index: 0;
    animation: pulse 8s ease-in-out infinite alternate;
  }

  .book-callout::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, transparent 50%, rgba(20, 184, 166, 0.1) 100%);
    z-index: 0;
    opacity: 0.5;
  }

  @keyframes pulse {
    0% {
      opacity: 0.3;
      transform: translate(-50%, -50%) scale(1);
    }
    100% {
      opacity: 0.5;
      transform: translate(-50%, -50%) scale(1.2);
    }
  }

  /* Fix for cursor flickering */
  .button-link {
    position: relative;
    z-index: 5;
    cursor: pointer;
    transform: translateZ(0); /* Force hardware acceleration */
    backface-visibility: hidden; /* Prevent flickering in some browsers */
    -webkit-font-smoothing: subpixel-antialiased;
  }

  .button-overlay {
    pointer-events: none; /* Ensures hover events pass through to the button */
  }

  /* Mobile optimization */
  @media (max-width: 768px) {
    .book-callout {
      padding: 1.5rem;
      margin: 1rem 0;
    }
  }
</style>