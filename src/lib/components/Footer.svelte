<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="footer-logo-row">
          <span class="footer-mark">STS</span>
          <span class="footer-brand-name">Surviving the Singularity</span>
        </div>
        <p class="footer-tagline">Material independence through digital leverage, local intelligence, and minimalist infrastructure.</p>
      </div>

      <div class="footer-links-group">
        <div class="footer-col">
          <h4 class="footer-col-title">Navigate</h4>
          <a href="/" class="footer-link">Home</a>
          <a href="/blueprint" class="footer-link">The Blueprint</a>
          <a href="/book" class="footer-link">Book</a>
          <a href="/blog" class="footer-link">Blog</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-col-title">Resources</h4>
          <a href="/about" class="footer-link">About</a>
          <a href="/policies" class="footer-link">Privacy</a>
          <a href="/terms" class="footer-link">Terms</a>
          <a href="/disclaimer" class="footer-link">Disclaimer</a>
          <a href="/accessibility" class="footer-link">Accessibility</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-col-title">Subscribe</h4>
          <a href="https://thecoffeejesus.substack.com" target="_blank" rel="noopener noreferrer" class="footer-link footer-link-accent">
            Substack
          </a>
          <a href="https://ko-fi.com/thecoffeejesus" target="_blank" rel="noopener noreferrer" class="footer-link">
            Buy me a coffee
          </a>
        </div>
      </div>
    </div>

    <div class="footer-divider"></div>

    <div class="footer-bottom">
      <div class="footer-disclaimer-box">
        <p class="footer-disclaimer-title">
          ⚠ Informational &amp; educational use only
        </p>
        <p class="footer-disclaimer">
          <strong>This site is for informational and educational purposes only. It is not professional advice and should not be used in place of professional advice. Please consult all relevant professionals before making any decisions.</strong>
          You assume all risk for any action you take or fail to take based on anything you read here. See our <a href="/terms" class="footer-disclaimer-link">terms</a> and <a href="/policies" class="footer-disclaimer-link">privacy policy</a> for details.
          <a href="/disclaimer" class="footer-disclaimer-link">Full disclaimer →</a>
        </p>
      </div>

      <p class="footer-consent">
        <strong>By accessing or using this site, you acknowledge that you have read, understood, and agree to be bound by the</strong>
        <a href="/terms" class="footer-disclaimer-link">Terms of Use</a>,
        <a href="/disclaimer" class="footer-disclaimer-link">Disclaimer</a>, and
        <a href="/policies" class="footer-disclaimer-link">Privacy &amp; Policies</a>.
        If you do not agree, do not use this site.
      </p>

      <p class="footer-copyright">
        &copy; {new Date().getFullYear()} Surviving the Singularity. All rights reserved where applicable.
      </p>
    </div>
  </div>
</footer>

<style>
  .site-footer {
    background: linear-gradient(180deg, transparent 0%, rgba(15, 23, 42, 0.8) 30%, #020617 100%);
    padding: 4rem 1.5rem 2rem;
    margin-top: 4rem;
  }

  .footer-inner {
    max-width: 1000px;
    margin: 0 auto;
  }

  .footer-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 3rem;
    flex-wrap: wrap;
  }

  .footer-brand {
    max-width: 360px;
  }

  .footer-logo-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .footer-mark {
    font-size: 0.8rem;
    font-weight: 800;
    color: #f59e0b;
    letter-spacing: 0.08em;
    font-family: var(--font-primary);
  }

  .footer-brand-name {
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
  }

  .footer-tagline {
    font-size: 0.85rem;
    color: #dde4ef;
    line-height: 1.6;
    margin: 0;
  }

  .footer-links-group {
    display: flex;
    gap: 3rem;
  }

  .footer-col {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .footer-col-title {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #dde4ef;
    margin: 0 0 0.25rem 0;
  }

  .footer-link {
    font-size: 0.85rem;
    color: #dde4ef;
    text-decoration: none;
    transition: color 0.2s;
    padding: 0.15rem 0;
  }

  .footer-link:hover {
    color: #f59e0b;
  }

  .footer-link-accent {
    color: #f59e0b;
    font-weight: 600;
  }

  .footer-link-accent:hover {
    color: #fbbf24;
  }

  .footer-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.15), transparent);
    margin: 2.5rem 0;
  }

  .footer-bottom {
    text-align: center;
  }

  .footer-disclaimer-box {
    max-width: 720px;
    margin: 0 auto 1.25rem;
    padding: 1rem 1.25rem;
    background: rgba(120, 53, 15, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 10px;
    text-align: left;
  }

  .footer-disclaimer-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #fcd34d;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 0.5rem 0;
    font-family: var(--font-primary);
  }

  .footer-disclaimer {
    font-size: 0.86rem;
    color: #e9eef5;
    line-height: 1.65;
    margin: 0;
  }

  .footer-disclaimer-link {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 2px;
    font-weight: 600;
    white-space: nowrap;
  }

  .footer-disclaimer-link:hover {
    color: #fbbf24;
  }

  .footer-consent {
    max-width: 720px;
    margin: 0 auto 1rem;
    padding: 0.85rem 1.1rem;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 8px;
    font-size: 0.82rem;
    color: #dde4ef;
    line-height: 1.6;
    text-align: left;
  }
  .footer-consent strong {
    color: #e2e8f0;
    font-weight: 600;
  }

  .footer-copyright {
    font-size: 0.8rem;
    color: #dde4ef;
    margin: 0;
  }

  @media (max-width: 640px) {
    .footer-top {
      flex-direction: column;
      gap: 2rem;
    }

    .footer-brand {
      max-width: 100%;
    }

    .footer-links-group {
      width: 100%;
      gap: 2rem;
    }
  }
</style>
