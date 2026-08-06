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
      <p class="p-sub">Last updated: 1 August 2026.</p>
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
      <!-- RE-UPDATED 2026-08-04 when accounts were removed. This paragraph
           briefly disclosed a sign-in session cookie while /signup existed
           (2026-08-01 to 2026-08-04); accounts are gone, so the no-first-party-
           cookies statement is true again. The privacy policy is the one
           document on the site where being out of date is itself the harm:
           re-check, do not trust, if auth ever returns. -->
      <p>
        <strong>Website Usage:</strong> This site does not run third-party analytics or advertising tags, and sets no tracking, advertising, or sign-in cookies, as of the last-updated date above. There are no user accounts (see <a href="#accounts">Accounts</a>). The site may store a small number of strictly-functional values in browser localStorage, for example whether you have dismissed the disclaimer banner. Outbound links to third-party services such as Substack, Ko-fi, YouTube, and Spotify will be subject to those services' own privacy practices once you click through. You should review their policies separately.
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

      <!-- Accounts were removed 2026-08-04 by CT's ruling: the identity model
           is the purchase email, nothing else. Every claim in this block is
           checkable against code:
             what is stored on purchase -> src/lib/server/transactions.js
                                           (recordCheckoutCompleted)
             what purchase email sends  -> src/lib/server/email.js
             consent at checkout        -> src/routes/api/stripe-checkout/+server.js -->
      <section id="accounts">
        <p>
          <strong>No accounts:</strong> This site has no user accounts, no
          profiles, no passwords, and no sign-in. There is nothing to register
          for and no login cookie to set. Everything readable on the site is
          readable by anyone with the link, and paid content is delivered by
          email instead of behind a login.
        </p>

        <p>
          <strong>What buying the book stores:</strong> When you preorder, the
          record kept is the one the payment created: the email address and name
          you gave at checkout, what you bought, what you paid, and the payment
          reference. That record is the whole of your identity here. It exists
          so your purchase can be delivered, looked up if something goes wrong,
          and honored when future editions ship.
        </p>

        <p id="purchase-emails">
          <strong>What your purchase email is used for:</strong> Buying the book
          means we will email you: the receipt and download delivery for the
          edition you bought, and notice when a new edition of the book is
          released, including any upgrade discount your purchase entitles you
          to (up to and including free, depending on the terms current at that
          release). These messages are part of what you bought, not a
          newsletter. Each one carries an unsubscribe link, and unsubscribing
          from release notices never affects your access to what you already
          purchased.
        </p>

        <p>
          <strong>Marketing is a separate decision:</strong> Buying the book is
          not permission to send you marketing. If you want the newsletter you
          have to ask for it separately, and you can stop it at any time from
          the unsubscribe link in any message.
        </p>

        <p>
          <strong>Removing your data:</strong> Write to
          <a href="mailto:{offer.refund.contact}">{offer.refund.contact}</a> and
          say so. We will remove your email from the release-notice list and any
          newsletter list. Records we are required to keep for a completed
          purchase - the order itself, and what the payment processor holds -
          survive that removal, because those are financial records rather than
          contact preferences.
        </p>
      </section>

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
