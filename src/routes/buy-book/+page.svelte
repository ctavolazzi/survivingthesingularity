<script>
  import { onMount } from 'svelte';
  import BuyBookButton from '../../components/BuyBookButton.svelte';

  let daysLeft = 10;
  let countdown;

  function startCountdown() {
    countdown = setInterval(() => {
      daysLeft--;
      if (daysLeft === 0) {
        clearInterval(countdown);
      }
    }, 86400000);
  }

  onMount(() => {
    startCountdown();
  });
</script>

<div class="container mx-auto px-4 py-8 text-black bg-white">
  <header class="border-b border-gray-300 mb-8 text-center">
    <h1 class="text-4xl font-bold mb-4">Unlock the Secrets to Surviving the Singularity</h1>
  </header>

  <section class="border-b border-gray-300 mb-8 text-center">
    <h2 class="text-2xl font-bold mb-4">Prepare for the Future with "Surviving the Singularity"</h2>
    <p class="mb-4">
      In this groundbreaking book, renowned futurist [Author Name] reveals the
      key strategies and insights you need to navigate the coming technological
      singularity. Discover how to future-proof your career, stay ahead of the
      curve, and thrive in a world dominated by artificial intelligence.
    </p>
    <blockquote class="bg-gray-100 p-4 rounded-lg mx-auto max-w-xl">
      <p>
        "This book is a must-read for anyone concerned about the impact of AI on
        our society." - [Influential Figure Name]
      </p>
    </blockquote>
  </section>

  <section class="border-b border-gray-300 mb-8 text-center">
    <h2 class="text-2xl font-bold mb-4">Table of Contents</h2>
    <div class="bg-gray-100 p-4 rounded-lg mx-auto max-w-xl">
      <p class="mb-4">You need to purchase the book to unlock the content.</p>
      <div class="animate-pulse">
        <div class="h-4 bg-gray-200 rounded mb-2"></div>
        <div class="h-4 bg-gray-200 rounded mb-2"></div>
        <div class="h-4 bg-gray-200 rounded mb-2"></div>
      </div>
    </div>
  </section>

  <section class="border-b border-gray-300 mb-8 text-center">
    <h2 class="text-2xl font-bold mb-4">Get Your Copy Today</h2>
    <p class="mb-4">For a limited time, get the exclusive companion guide for free!</p>
    <div class="bg-yellow-100 p-4 rounded-lg mb-4 max-w-md mx-auto">
      <p>Offer ends in {daysLeft} days</p>
    </div>
    <BuyBookButton className="bg-black text-white py-4 px-8 text-2xl font-bold rounded-lg shadow-lg transition duration-300 transform hover:bg-gray-800 hover:scale-105" />
    <p class="mt-4">60-Day Money-Back Guarantee - No Questions Asked!</p>
  </section>

  <section class="border-b border-gray-300 mb-8 text-center">
    <h2 class="text-2xl font-bold mb-4">What Others Are Saying</h2>
    <div class="bg-gray-100 p-4 rounded-lg mx-auto max-w-xl">
      <blockquote>
        <p>
          "This book has completely changed my perspective on the future of
          technology. A must-read for anyone interested in AI and its
          implications." - [Reviewer Name]
        </p>
      </blockquote>
    </div>
  </section>

  <section class="border-b border-gray-300 text-center">
    <h2 class="text-2xl font-bold mb-4">Complete Your Journey</h2>
    <p class="mb-4">
      Enhance your learning experience with these complementary products:
    </p>
    <ul class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <li class="bg-white rounded-lg shadow-md p-4">
        <h3 class="text-xl font-bold mb-2">Audiobook Version</h3>
        <p class="mb-4">Listen on the go with the "Surviving the Singularity" audiobook.</p>
        <button class="bg-black text-white py-4 px-8 text-2xl font-bold rounded-lg shadow-lg transition duration-300 transform hover:bg-gray-800 hover:scale-105">Add to Cart - $14.99</button>
      </li>
      <!-- Add more upsell products as needed -->
    </ul>
  </section>
</div>

<style>

</style>
