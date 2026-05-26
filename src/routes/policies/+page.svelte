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
    <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Last Updated: May 25, 2026</p>

    <div class="prose prose-lg dark:prose-invert max-w-none">
            <p class="mb-4"><strong>Website Usage:</strong> This site itself does not set first-party tracking cookies and does not run third-party analytics or advertising tags as of the last-updated date above. The site may set a small number of strictly-functional values in browser localStorage (for example, to remember whether you have dismissed the disclaimer banner). Outbound links to third-party services such as Substack, Ko-fi, YouTube, and Spotify will be subject to those services' own privacy practices once you click through. You should review their policies separately.</p>

            <p class="mb-4"><strong>Children:</strong> This site is not directed to children under 13. Personal information from children under 13 is not knowingly collected. If you believe a child has provided personal information, you may contact <a href="mailto:info@survivingthesingularity.com" class="text-blue-600 dark:text-blue-400 hover:underline">info@survivingthesingularity.com</a>; review on a best-available-basis with no guaranteed action is contemplated.</p>

      <p class="mb-4"><strong>Book Preorders &amp; Email Collection:</strong> Email addresses and payment information have been collected from people who preordered the book or requested advance copies. This information is used only for book fulfillment and communication about the book's progress.</p>

      <p class="mb-4"><strong>Data Usage:</strong> Email addresses collected for preorder purposes are used in connection with book fulfillment and related communications. Payment information was processed through third-party payment processors for preorders. Personal information is not sold to third parties for marketing.</p>

      <p class="mb-4"><strong>Book Status:</strong> The book is in active development. As of May 2026, no firm shipping date has been set. Periodic progress updates may be sent by email. No specific delivery date is guaranteed.</p>

      <p class="mb-4"><strong>Preorder Refund Eligibility:</strong> Preorder customers may request a full refund at any time prior to shipment, for any reason or no reason, by emailing <a href="mailto:info@survivingthesingularity.com" class="text-blue-600 dark:text-blue-400 hover:underline">info@survivingthesingularity.com</a> from the email address used to place the order with the subject line "Refund request". Refunds, where eligible, are processed to the original payment method in accordance with applicable law and the policies of the relevant payment processor. No specific timeline for refund processing is guaranteed beyond what applicable law requires. The U.S. FTC Mail, Internet, or Telephone Order Merchandise Rule and any other applicable consumer-protection laws govern over anything stated on this page.</p>

      <p class="mb-4"><strong>Contact:</strong> Preorder questions and refund requests may be sent to <a href="mailto:info@survivingthesingularity.com" class="text-blue-600 dark:text-blue-400 hover:underline">info@survivingthesingularity.com</a>. No specific response time is promised; reasonable effort, when made, is informational and creates no obligation.</p>
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