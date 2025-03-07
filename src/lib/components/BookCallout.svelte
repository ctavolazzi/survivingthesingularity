<script>
  import bookCoverImage from '$lib/images/Surviving-the-Singularity-Cover.png';

  // Props
  export let title = "Navigate the Path to Singularity";
  export let description = "Get the insights and strategies you need to prepare for the technological changes that will reshape our world.";
  export let buttonText = "Explore the Book";
  export let buttonLink = "/sample"; // Default to sample page
  export let imageSrc = bookCoverImage; // Use the imported image
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

      <!-- Simplified action button - ULTRA FAST VERSION -->
      <div class="flex">
        <a href={buttonLink} class="button-link inline-flex items-center px-6 py-3 text-base font-medium text-center text-white bg-blue-600 rounded-lg relative overflow-hidden">
          <span class="relative z-10">{buttonText}</span>
          <svg class="w-5 h-5 ml-2 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
        </a>
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
  .button-link {
    position: relative;
    z-index: 5;
    cursor: pointer;
  }

  /* Mobile optimization */
  @media (max-width: 768px) {
    .book-callout {
      padding: 1.5rem;
      margin: 1rem 0;
    }
  }
</style>