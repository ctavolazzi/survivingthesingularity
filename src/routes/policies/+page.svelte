<script>
  import { onMount } from 'svelte';
  // Every offer claim on this page is derived, never typed. See src/lib/offer.js
  // for why: the sales pages and this page used to describe two different
  // transactions, and the fix is one object rather than better proofreading.
  import { offer, cadence, refundClause } from '$lib/offer';
  import book from '$lib/data/book/book.json';

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
      <p class="p-sub">Last updated: 12 October 2026.</p>
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
        <strong>Website usage:</strong> The site uses Cloudflare for hosting and
        delivery, including performance measurements. Requests may include your
        IP address, browser information, requested URL, and timing information.
        The site does not use advertising tags or create user accounts. Browser
        localStorage keeps functional preferences such as disclaimer choices,
        checklist progress and notes, and whether you have unlocked the reader.
        These local values stay in that browser unless you use a feature that
        sends them, such as emailing your checklist.
      </p>
      <p>
        <strong>Videos and external services:</strong> YouTube preview images
        load from YouTube's image service when shown. Pressing play loads a
        YouTube player, which can process information under Google's privacy
        policy. Some articles also contain embedded media from external services.
        Following links to Substack, Ko-fi, YouTube, Spotify, Discord, or other
        services brings you under their terms and privacy practices. The site
        does not control those services' cookies or data handling.
      </p>
      <p>
        <strong>Do Not Track and Global Privacy Control:</strong> This site does
        not currently detect or respond to DNT or GPC signals. Personal
        information is not sold for third-party marketing.
      </p>
      <p>
        <strong>Children:</strong> This site is not directed to children under
        13 and does not knowingly collect their personal information. Contact
        <a href="mailto:{offer.refund.contact}">{offer.refund.contact}</a> if you
        believe a child has submitted personal information.
      </p>

      <section id="accounts">
        <h3>Access and purchases</h3>
        <p>
          <strong>No personal accounts:</strong> There are no profiles or
          individual sign-ins. The full online draft uses a shared book-access
          password; this is separate from an account password. The
          <a href="/sample">public sample and reading guide</a> need no password.
          {offer.access}
        </p>
        <p>
          <strong>Checkout records:</strong> When you start checkout, we send
          your email to Stripe and keep a checkout record, even if you do not
          finish paying. A completed purchase record includes the email and
          name supplied at checkout, the product, amount, currency, payment
          references, and fulfillment status. Stripe processes payment details;
          the site does not store your full card number. These records support
          delivery, purchase recovery, refunds, and the benefits of your order.
        </p>
        <p id="purchase-emails">
          <strong>Purchase email:</strong> We use your purchase address to send
          the receipt, downloads, access instructions, and substantial digital
          edition updates while the project is maintained. Digital updates for
          this preorder cohort are included; a future Print Edition is a
          separate discounted purchase. Release notices can be unsubscribed
          from without losing material you already purchased.
        </p>
        <p>
          <strong>Email signup and preferences:</strong> A signup stores your
          email, signup source, and the email preferences submitted with the
          form. A checklist unlock or purchase is not permission for the weekly
          newsletter. The newsletter requires a separate choice, and you can
          unsubscribe using the link in an email or contact us to change your
          preferences. Registering an address that is already on the list does
          not change its existing preferences.
        </p>
      </section>

      <p>
        <strong>Checklist notes:</strong> Your progress and notes are saved in
        your browser. Choosing to email the checklist sends your address,
        answers, checked steps, and notes to our server and email provider so
        they can be included in the message to you. Avoid putting sensitive
        personal information in these notes or in email.
      </p>
      <p>
        <strong>Community applications:</strong> The application form collects
        your name, email address, and written answer. These are stored for review;
        a confirmation is sent to you and the application is emailed to the
        operator. Submitting an application does not subscribe you to marketing
        or create a Discord account.
      </p>
      <p>
        <strong>Service providers:</strong> Supabase stores signup, application,
        transaction, and delivery records. Resend sends transactional and
        requested emails. Delivery records can include the recipient address,
        message type, provider reference, timestamps, and delivery status.
        Stripe processes payments and Cloudflare serves the site. These providers
        process information needed to provide their services under their own
        privacy and retention practices.
      </p>
      <p>
        <strong>Retention and removal:</strong> Contact
        <a href="mailto:{offer.refund.contact}">{offer.refund.contact}</a> to
        request access, correction, or deletion of information you submitted.
        Signup and application records are kept to manage those requests;
        transaction and delivery records support purchases and troubleshooting.
        Financial records that must be retained for legal or accounting purposes
        may remain after contact preferences are removed. Clear this site's
        browser storage to remove locally saved progress and notes; doing so
        does not delete a previously sent email or server record.
      </p>
      <p>
        <strong>Book status:</strong> The current manuscript is version
        {book.version}, updated {book.lastUpdated}. It remains in development.
        There is no confirmed final-edition or print release date. The
        {offer.price} purchase gives access to the current digital material
        after payment; it does not wait for a future publication date.
      </p>
      <p>
        <strong>Digital preorder refunds:</strong> {refundClause()}
      </p>
      <p>
        <strong>Help with a purchase:</strong> Contact
        <a href="mailto:{offer.refund.contact}">{offer.refund.contact}</a> from
        the address used at checkout for access recovery, delivery issues,
        preorder questions, or refunds. Include your payment reference if you
        have it; do not send card details. No specific response time is promised.
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
