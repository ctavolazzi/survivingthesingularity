<svelte:head>
  <title>Accessibility Statement - Surviving the Singularity</title>
  <meta name="description" content="Accessibility statement for survivingthesingularity.com" />
</svelte:head>

<div class="a11y-page">
  <div class="a-inner">
    <header class="a-header">
      <h1>Accessibility Statement</h1>
      <p class="a-sub">Last updated: 26 May 2026.</p>
    </header>

    <section class="a-section">
      <h2>Informational notes only</h2>
      <p>
        This page is provided for informational purposes only and does not
        create any obligation, warranty, or guarantee of any kind. It is not
        a legal accessibility certification. The site is provided "as is" and
        "as available"; see the <a href="/terms">Terms of Use</a> and
        <a href="/disclaimer">Disclaimer</a>, which control over anything on
        this page.
      </p>
      <p>
        The site has been built with general reference to
        <strong>Web Content Accessibility Guidelines (WCAG) 2.1</strong>,
        without any representation that all guidelines are met.
      </p>
    </section>

    <section class="a-section">
      <h2>General notes on current state</h2>
      <ul>
        <li>Semantic HTML structure is used in many sections, including headings, landmarks, and lists</li>
        <li>Many links and buttons are keyboard-navigable with visible focus indicators</li>
        <li><code>aria-hidden</code> is used on many decorative SVG icons</li>
        <li>Alt text is provided on most content images</li>
        <li><code>rel="noopener noreferrer"</code> is used on outbound links opening in new tabs</li>
        <li>No representation is made that any of the above is complete, correct, or sufficient for any individual user's needs</li>
      </ul>
    </section>

    <section class="a-section">
      <h2>Known gaps</h2>
      <p>
        Areas where this site may not meet WCAG 2.1 AA in full include, without limitation:
      </p>
      <ul>
        <li>Secondary text in some places uses muted colors that may not meet the 4.5:1 contrast minimum</li>
        <li>The site uses a dark-only theme; no light-mode option is currently provided</li>
        <li>Some interactive widgets (calculator, countdown, dashboard) may not be optimally screen-reader friendly. They are informational only; underlying disclosures are available in plain text on the <a href="/disclaimer">disclaimer page</a></li>
        <li>Animated elements (sweeping highlights, pulsing dots) may not honor <code>prefers-reduced-motion</code> in every case</li>
        <li>Other gaps may exist that have not been documented here</li>
      </ul>
    </section>

    <section class="a-section">
      <h2>Feedback</h2>
      <p>
        Feedback may be sent to
        <a href="mailto:info@survivingthesingularity.com">info@survivingthesingularity.com</a>.
        No response, acknowledgement, or remediation timeline is promised or
        implied. Submission of feedback does not create any legal obligation,
        contract, or expectation of action.
      </p>
    </section>

    <section class="a-section">
      <h2>Third-party content</h2>
      <p>
        Where this site embeds or links to third-party services, accessibility
        of those services is the responsibility of those providers. No liability
        is accepted for third-party accessibility.
      </p>
    </section>
  </div>
</div>

<style>
  .a11y-page {
    padding: 4rem 1.5rem 6rem;
    background: #020617;
    color: #e2e8f0;
    min-height: 100vh;
  }
  .a-inner {
    max-width: 760px;
    margin: 0 auto;
  }
  .a-header {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  }
  .a-header h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 900;
    color: #fafafa;
    margin: 0 0 1rem 0;
    letter-spacing: -0.03em;
  }
  .a-sub {
    color: #94a3b8;
    margin: 0;
  }
  .a-section { margin-bottom: 2.25rem; }
  .a-section h2 {
    font-size: 1.2rem;
    font-weight: 700;
    color: #fafafa;
    margin: 0 0 0.85rem 0;
  }
  .a-section p {
    color: #cbd5e1;
    line-height: 1.75;
    margin: 0 0 0.9rem 0;
    font-size: 0.94rem;
  }
  .a-section ul { margin: 0 0 1rem 0; padding-left: 1.2rem; }
  .a-section li {
    color: #cbd5e1;
    line-height: 1.7;
    margin-bottom: 0.35rem;
    font-size: 0.94rem;
  }
  .a-section a {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .a-section a:hover { color: #fbbf24; }
  .a-section code {
    background: rgba(148, 163, 184, 0.1);
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 0.86em;
    color: #f1f5f9;
  }
  .a-section strong { color: #fafafa; }
</style>
