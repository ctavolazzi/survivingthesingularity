<script>
  function handleBackBook() {
    window.location.href = 'https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook';
  }
</script>

<!-- Footer Component -->
<footer class="bg-gray-800 text-white py-6 mt-8">
  <div class="container mx-auto px-4">
    <div class="flex flex-col md:flex-row justify-center items-start text-left space-y-4 md:space-y-0 md:space-x-8">
      <div class="w-full md:w-auto text-center md:text-left">
        <h5 class="font-bold text-lg mb-2">Quick Links</h5>
        <ul class="list-none">
          <li class="mb-1"><a href="/" class="text-gray-400 hover:text-gray-200">Home</a></li>
          <li class="mb-1"><a href="/about" class="text-gray-400 hover:text-gray-200">About Us</a></li>
          <li class="mb-1"><a href="/contact" class="text-gray-400 hover:text-gray-200">Contact</a></li>
        </ul>
      </div>
      <div class="w-full md:w-auto text-center md:text-left">
        <h5 class="font-bold text-lg mb-2">Legal</h5>
        <ul class="list-none">
          <li class="mb-1"><a href="/policies#privacy-policy" class="text-gray-400 hover:text-gray-200">Privacy Policy</a></li>
          <li class="mb-1"><a href="/policies#terms-of-service" class="text-gray-400 hover:text-gray-200">Terms of Service</a></li>
          <li class="mb-1"><a href="/policies#cookie-policy" class="text-gray-400 hover:text-gray-200">Cookie Policy</a></li>
        </ul>
      </div>
    </div>
    <div class="text-center mt-6">
      <p>&copy; 2024 AIECO. All rights reserved.</p>
      <p class="text-gray-400 text-sm">469 East 5th Street, Chico, CA, 95926</p>
    </div>
    <!-- <div class="text-center mt-4">
      <button class="buy-button w-full md:w-auto px-6 py-2" on:click={handleBackBook}>Back the Book on Kickstarter</button>
    </div> -->
  </div>
</footer>

<style>
	.buy-button {
      font-weight: bold;
	    font-size: 1.5rem;
      background-color: #f8f9fa;
      color: #000000;
      border: 2px solid #000000;
      border-radius: 4px;
      padding: 1rem 1rem;
      cursor: pointer;
      transition: background-color 0.3s ease;
      text-align: center;
    }

    .buy-button:hover {
      background-color: #e2e6ea;
    }

  footer ul {
    padding: 0;
  }

  footer ul li {
    list-style: none;
  }
</style>
