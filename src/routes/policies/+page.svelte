<script>
  import { onMount } from 'svelte';
  // Every offer claim on this page is derived, never typed. See src/lib/offer.js
  // for why: the sales pages and this page used to describe two different
  // transactions, and the fix is one object rather than better proofreading.
  import { offer, cadence, refundClause } from '$lib/offer';

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

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:title" content="Our Policies" />
  <meta property="og:description" content="Privacy Policy and Disclaimers for Surviving the Singularity website." />
  <meta property="og:url" content="https://survivingthesingularity.com/policies" />
  <meta property="og:image" content="https://survivingthesingularity.com/images/og/home.png" />
  <meta property="og:image:secure_url" content="https://survivingthesingularity.com/images/og/home.png" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="2400" />
  <meta property="og:image:height" content="1260" />
  <meta property="og:image:alt" content="Surviving the Singularity: a practical field guide for staying human in the age of AI." />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Our Policies" />
  <meta name="twitter:description" content="Privacy Policy and Disclaimers for Surviving the Singularity website." />
  <meta name="twitter:image" content="https://survivingthesingularity.com/images/og/home.png" />
</svelte:head>

<div class="policies-page">
  <div class="policies-inner">
    <header class="p-header">
      <h1>Our Policies</h1>
      <p class="p-sub">Last updated: 29 July 2026.</p>
    </header>

    <section id="what-you-buy" class="p-section">
      <h2>What the {offer.price} preorder is</h2>
      <p class="p-offer-sentence">{offer.sentence}</p>

      <p><strong>Included:</strong></p>
      <ul class="p-offer-list">
        {#each offer.included as item}
          <li><strong>{item.title}</strong> {item.detail}</li>
        {/each}
      </ul>

      <p><strong>Not included:</strong></p>
      <ul class="p-offer-list">
        {#each offer.excluded as item}
          <li><strong>{item.title}</strong> {item.detail}</li>
        {/each}
      </ul>

      <p>
        <strong>What "you keep getting it" means, exactly:</strong> {offer.foreverScope}
      </p>

      <p>
        <strong>When the preorder window closes:</strong> {offer.windowClose}
      </p>

      <p>
        <strong>How often things change:</strong> {cadence.research} {cadence.site}
        {cadence.newsletter} {cadence.book} {cadence.print}
      </p>
    </section>

    <section id="privacy-policy" class="p-section">
      <h2>Privacy &amp; Contact</h2>
      <p>
        <strong>Website Usage:</strong> This site itself does not set first-party tracking cookies and does not run third-party analytics or advertising tags as of the last-updated date above. The site may set a small number of strictly-functional values in browser localStorage (for example, to remember whether you have dismissed the disclaimer banner). Outbound links to third-party services such as Substack, Ko-fi, YouTube, and Spotify will be subject to those services' own privacy practices once you click through. You should review their policies separately.
      </p>

      <!-- DRAFTED 2026-07-29. CalOPPA requires a site collecting personal
           information from California residents to disclose HOW it responds to
           Do Not Track signals. It does not require honouring them, so the
           compliant move is an accurate statement, and the statement below is
           accurate as measured: grep found zero references to DNT, Sec-GPC,
           navigator.doNotTrack or globalPrivacyControl anywhere in
           hooks.server.js or the rest of src, so nothing reads those headers.

           ONE THING TO CONFIRM BEFORE THIS GOES LIVE: static/_headers allows
           static.cloudflareinsights.com in script-src and cloudflareinsights.com
           in connect-src. Cloudflare Web Analytics is injected at the edge, not
           from this repo, so whether it is actually enabled cannot be determined
           from the source. If it IS enabled, the "no third-party analytics"
           sentence in the paragraph above needs qualifying. Check the Cloudflare
           dashboard. -->
      <p>
        <strong>Do Not Track and Global Privacy Control:</strong> Some browsers
        can send a Do Not Track (DNT) header or a Global Privacy Control signal.
        This site does not currently detect or respond to either one. That is
        stated plainly rather than dressed up, because the honest position is
        that there is very little here for such a signal to switch off: the site
        runs no advertising tags and no cross-site tracking, so there is no
        behavioural profile being built to opt out of. If that ever changes, this
        section changes with it.
      </p>

      <p>
        <strong>Children:</strong> This site is not directed to children under 13. Personal information from children under 13 is not knowingly collected. If you believe a child has provided personal information, you may contact
        <!-- Was info@thecoffeejesus.com, a leftover from before the contact
             address was migrated on 2026-07-29. Every other address on this page
             already derives from the offer module; this one had been missed, so a
             child-safety report would have gone to a stale inbox. -->
        <a href="mailto:{offer.refund.contact}">{offer.refund.contact}</a>;
        review on a best-available-basis with no guaranteed action is contemplated.
      </p>

      <p>
        <strong>Book Preorders &amp; Email Collection:</strong> Email addresses and payment information have been collected from people who preordered the book or requested advance copies. This information is used only for book fulfillment and communication about the book's progress.
      </p>

      <p>
        <strong>Data Usage:</strong> Email addresses collected for preorder purposes are used in connection with book fulfillment and related communications. Payment information was processed through third-party payment processors for preorders. Personal information is not sold to third parties for marketing.
      </p>

      <p>
        <strong>Book Status:</strong> The book is in active development and readable now, in the state it is currently in. The finished edition is targeted for September 2026. That is a target and not a guarantee, and it is the one date on this page that may move. Your access does not depend on it: the {offer.price} purchase delivers immediately and nothing about it waits for a release date.
      </p>

      <p>
        <strong>Preorder Refund Eligibility:</strong> {refundClause()}
      </p>

      <p>
        <strong>Contact:</strong> Preorder questions and refund requests may be sent to
        <a href="mailto:{offer.refund.contact}">{offer.refund.contact}</a>.
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
    min-height: 100dvh;
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

  /* The offer sentence renders at the top of the legal page at a size that says
     it matters, because the reason this page exists is that the sales layer and
     the legal layer once described two different transactions. */
  .p-offer-sentence {
    color: #fafafa;
    font-size: 1.05rem;
    line-height: 1.7;
    border-left: 2px solid #f59e0b;
    padding-left: 1rem;
    margin: 0 0 1.5rem 0;
  }
  .p-offer-list {
    color: #e9eef5;
    line-height: 1.75;
    font-size: 0.94rem;
    margin: 0 0 1.25rem 0;
    padding-left: 1.15rem;
  }
  .p-offer-list li {
    margin-bottom: 0.5rem;
  }
  .p-offer-list strong {
    color: #fafafa;
    font-weight: 700;
  }
</style>
