<script>
  function handleBackBook() {
    window.location.href = 'https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook';
  }
</script>

<!-- Footer Component -->
<footer class="bg-gray-900 text-white py-6 mt-8">
  <div class="container mx-auto px-4">
    <div class="flex flex-col md:flex-row justify-center items-start text-left space-y-4 md:space-y-0 md:space-x-8">
      <div class="w-full md:w-auto text-center md:text-left">
        <h5 class="font-bold text-lg mb-2">Quick Links</h5>
        <ul class="list-none">
          <li class="mb-1"><a href="/" class="text-gray-400 hover:text-gray-200">Home</a></li>
          <li class="mb-1"><a href="/about" class="text-gray-400 hover:text-gray-200">About Us</a></li>
          <li class="mb-1"><a href="/contact" class="text-gray-400 hover:text-gray-200">Contact</a></li>
          <li class="mb-1">
            <a href="/discord" class="text-cyan-400 hover:text-cyan-300 transition-colors">
              Join Our Discord
              <span class="inline-block ml-1 animate-pulse">•</span>
            </a>
          </li>
        </ul>
      </div>
      <div class="w-full md:w-auto text-center md:text-left">
        <h5 class="font-bold text-lg mb-2">Policies</h5>
        <ul class="list-none">
          <li class="mb-1"><a href="/policies" class="text-gray-400 hover:text-gray-200">All Policies</a></li>
          <li class="mb-1"><a href="/policies#disclaimers" class="text-gray-400 hover:text-gray-200">Disclaimers</a></li>
        </ul>
      </div>
    </div>
    <!-- <div class="text-center mt-4">
      <button class="buy-button w-full md:w-auto px-6 py-2" on:click={handleBackBook}>Back the Book on Kickstarter</button>
    </div> -->

    <div class="disclaimer-section mt-6 pt-4 border-t border-gray-800 text-center">
      <p class="text-gray-500 text-sm">
        <strong>Disclaimer:</strong> The content on this site represents educated guesses and personal opinions. Nothing is certain about the future.
        Always do your own research and consult appropriate professionals before making decisions.
        This is commentary and opinion only and should not be taken as financial, legal, or professional advice.
      </p>
      <p class="text-gray-500 text-xs mt-2">
        <a href="/policies#disclaimers" class="text-gray-400 hover:text-gray-200">Read our full disclaimers</a>
      </p>
    </div>
  </div>
</footer>

<style>
  /* Removed unused buy-button selectors */

  footer ul {
    padding: 0;
  }

  footer ul li {
    list-style: none;
  }

  .disclaimer-section {
    max-width: 800px;
    margin: 0 auto;
  }
</style>
