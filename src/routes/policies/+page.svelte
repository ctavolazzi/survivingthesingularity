<script>
  import { onMount } from 'svelte';

  onMount(() => {
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

<div class="policies-page">
  <div class="policies-inner">
    <header class="p-header">
      <h1>Our Policies</h1>
      <p class="p-sub">Last updated: 25 May 2026.</p>
    </header>

    <section id="privacy-policy" class="p-section">
      <h2>Privacy &amp; Contact</h2>
      <p>
        <strong>Website Usage:</strong> This site itself does not set first-party tracking cookies and does not run third-party analytics or advertising tags as of the last-updated date above. The site may set a small number of strictly-functional values in browser localStorage (for example, to remember whether you have dismissed the disclaimer banner). Outbound links to third-party services such as Substack, Ko-fi, YouTube, and Spotify will be subject to those services' own privacy practices once you click through. You should review their policies separately.
      </p>

      <p>
        <strong>Children:</strong> This site is not directed to children under 13. Personal information from children under 13 is not knowingly collected. If you believe a child has provided personal information, you may contact
        <a href="mailto:info@thecoffeejesus.com">info@thecoffeejesus.com</a>;
        review on a best-available-basis with no guaranteed action is contemplated.
      </p>

      <p>
        <strong>Book Preorders &amp; Email Collection:</strong> Email addresses and payment information have been collected from people who preordered the book or requested advance copies. This information is used only for book fulfillment and communication about the book's progress.
      </p>

      <p>
        <strong>Data Usage:</strong> Email addresses collected for preorder purposes are used in connection with book fulfillment and related communications. Payment information was processed through third-party payment processors for preorders. Personal information is not sold to third parties for marketing.
      </p>

      <p>
        <strong>Book Status:</strong> The book is in active development. As of May 2026, no firm shipping date has been set. Periodic progress updates may be sent by email. No specific delivery date is guaranteed.
      </p>

      <p>
        <strong>Preorder Refund Eligibility:</strong> Preorder customers may request a full refund at any time prior to shipment, for any reason or no reason, by emailing
        <a href="mailto:info@thecoffeejesus.com">info@thecoffeejesus.com</a>
        from the email address used to place the order with the subject line "Refund request". Refunds, where eligible, are processed to the original payment method in accordance with applicable law and the policies of the relevant payment processor. No specific timeline for refund processing is guaranteed beyond what applicable law requires. The U.S. FTC Mail, Internet, or Telephone Order Merchandise Rule and any other applicable consumer-protection laws govern over anything stated on this page.
      </p>

      <p>
        <strong>Contact:</strong> Preorder questions and refund requests may be sent to
        <a href="mailto:info@thecoffeejesus.com">info@thecoffeejesus.com</a>.
        No specific response time is promised; reasonable effort, when made, is informational and creates no obligation.
      </p>
    </section>

    <section id="disclaimers" class="p-section">
      <h2>Disclaimers</h2>
      <p>
        <strong>This content represents personal opinions and speculation.</strong>
        Nothing on this site should be considered certain or guaranteed. All discussions about future events are speculation, not certainty.
      </p>
      <p>
        <strong>Not professional advice.</strong>
        This information is for educational purposes only and should not be taken as financial, legal, investment, medical, or other professional advice.
      </p>
      <p>
        <strong>Do your own research.</strong>
        We encourage visitors to conduct their own research, exercise critical thinking, and consult qualified professionals before making decisions based on information found here.
      </p>
      <p>
        <strong>No liability.</strong>
        We are not liable for any losses, damages, or negative outcomes that may result from using or relying upon information on this website.
      </p>
      <p>
        See also the <a href="/disclaimer">full disclaimer</a> and the <a href="/terms">terms of use</a>.
      </p>
    </section>
  </div>
</div>

<style>
  .policies-page {
    padding: 4rem 1.5rem 6rem;
    background: #020617;
    color: #e2e8f0;
    min-height: 100vh;
  }
  .policies-inner {
    max-width: 760px;
    margin: 0 auto;
  }
  .p-header {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  }
  .p-header h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 900;
    color: #fafafa;
    margin: 0 0 1rem 0;
    letter-spacing: -0.03em;
  }
  .p-sub {
    color: #dde4ef;
    margin: 0;
  }
  .p-section {
    margin-bottom: 2.25rem;
  }
  .p-section h2 {
    font-size: 1.2rem;
    font-weight: 700;
    color: #fafafa;
    margin: 0 0 0.85rem 0;
    letter-spacing: -0.02em;
  }
  .p-section p {
    color: #e9eef5;
    line-height: 1.75;
    margin: 0 0 0.9rem 0;
    font-size: 0.94rem;
  }
  .p-section strong {
    color: #fafafa;
    font-weight: 700;
  }
  .p-section a {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .p-section a:hover {
    color: #fbbf24;
  }
</style>
