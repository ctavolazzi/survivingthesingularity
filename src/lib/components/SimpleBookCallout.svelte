<script>
  import bookCoverImage from '$lib/images/Surviving-the-Singularity-Cover.png';

  // Props with sensible defaults
  export let title = "Navigate the Path to Singularity";
  export let description = "Get the insights and strategies you need to prepare for the technological changes that will reshape our world.";
  export let buttonText = "Explore the Book";
  export let buttonLink = "/book";
  export let imageSrc = bookCoverImage;

  // Simple share function
  function shareBook() {
    if (navigator && navigator.share) {
      navigator.share({
        title: 'Surviving the Singularity',
        text: 'Check out this book about navigating the technological singularity!',
        url: window.location.origin + buttonLink,
      }).catch(err => {
        console.error('Share failed:', err);
      });
    } else {
      // Fallback for browsers that don't support navigator.share
      const url = window.location.origin + buttonLink;
      navigator.clipboard.writeText(url)
        .then(() => {
          alert('Link copied to clipboard!');
        })
        .catch(err => {
          console.error('Could not copy text: ', err);
        });
    }
  }
</script>

<div class="book-callout bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 shadow-xl rounded-lg max-w-3xl mx-auto my-8 p-6 border border-gray-700/50">
  <div class="flex flex-col md:flex-row gap-6">
    <!-- Book cover image -->
    <div class="flex-shrink-0 relative">
      <div class="absolute inset-0 bg-blue-500/30 opacity-30 blur-2xl rounded-full"></div>
      <img src={imageSrc} alt="Book cover" class="w-40 md:w-48 h-auto rounded-md shadow-lg mx-auto md:mx-0 relative z-10"  loading="lazy" \/\>
    </div>

    <!-- Content -->
    <div class="flex flex-col justify-center">
      <h2 class="text-2xl md:text-3xl font-bold text-white mb-3">
        {title}
      </h2>
      <p class="text-gray-300 mb-5 text-base md:text-lg">
        {description}
      </p>

      <!-- Features list -->
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

      <!-- Action buttons -->
      <div class="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4">
        <!-- Main CTA Button -->
        <a href={buttonLink} class="inline-flex items-center justify-center px-6 py-3 text-base font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 transition-all duration-300">
          {buttonText}
          <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
        </a>

        <!-- Share button -->
        <button
          class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 focus:ring-4 focus:outline-none focus:ring-purple-300 transition-all duration-300"
          on:click={shareBook}
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
          </svg>
          Share
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  /* Add any additional styles here if needed */
  .book-callout {
    backdrop-filter: blur(8px);
  }
</style>