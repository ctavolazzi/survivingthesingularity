<script>
  import { onMount } from 'svelte';

  onMount(() => {
    // Handle anchor links in URL
    if (window.location.hash) {
      const element = document.querySelector(window.location.hash);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
</script>

<svelte:head>
  <title>Our Policies - Surviving the Singularity</title>
  <meta name="description" content="Privacy Policy and Disclaimers for Surviving the Singularity website." />
</svelte:head>

<div class="container mx-auto px-4 py-8 max-w-4xl">
  <h1 class="text-4xl font-bold mb-8 text-center text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-600">Our Policies</h1>

  <!-- Privacy & Contact -->
  <section id="privacy-policy" class="mb-12">
    <h2 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-200">Privacy & Contact</h2>
    <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Last Updated: July 2, 2025</p>

    <div class="prose prose-lg dark:prose-invert max-w-none">
            <p class="mb-4"><strong>Website Usage:</strong> This website does not collect personal data through cookies or tracking. You can browse and read content without providing any personal information.</p>

      <p class="mb-4"><strong>Book Preorders & Email Collection:</strong> We have collected email addresses and payment information from people who preordered the book or requested advance copies. This information is used solely for book fulfillment and communication about the book's progress.</p>

      <p class="mb-4"><strong>Data Usage:</strong> Email addresses are used only to send book updates and delivery notifications. Payment information was processed through secure payment processors for preorders. We do not sell, share, or use this information for any other purpose.</p>

      <p class="mb-4"><strong>Contact Us:</strong> If you have questions about your preorder, need a refund, or want to update your information, email <a href="mailto:info@survivingthesingularity.com" class="text-blue-600 dark:text-blue-400 hover:underline">info@survivingthesingularity.com</a>.</p>

      <p class="mb-6"><strong>Book Status:</strong> The book is still in development. Advance copies and final versions will be distributed to preorder customers when complete.</p>
    </div>
  </section>

  <!-- Disclaimers -->
  <section id="disclaimers" class="mb-12">
    <h2 class="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-200">Disclaimers</h2>

    <div class="prose prose-lg dark:prose-invert max-w-none">
      <p class="mb-4"><strong>This content represents personal opinions and speculation.</strong> Nothing on this site should be considered certain or guaranteed. All discussions about future events are speculation, not certainty.</p>

      <p class="mb-4"><strong>Not professional advice.</strong> This information is for educational purposes only and should not be taken as financial, legal, investment, medical, or other professional advice.</p>

      <p class="mb-4"><strong>Do your own research.</strong> We encourage visitors to conduct their own research, exercise critical thinking, and consult qualified professionals before making decisions based on information found here.</p>

      <p class="mb-6"><strong>No liability.</strong> We are not liable for any losses, damages, or negative outcomes that may result from using or relying upon information on this website.</p>
    </div>
  </section>
</div>

<style>
  .prose p {
    margin-bottom: 1rem;
  }
</style>