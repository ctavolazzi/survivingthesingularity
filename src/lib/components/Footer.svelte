<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="/" class="footer-logo-link">
          <img src="/android-chrome-192x192.png" class="footer-logo" alt="Logo" loading="lazy">
          <span class="footer-brand-name">Surviving the Singularity</span>
        </a>
        <p class="footer-tagline">Understanding what's coming. Preparing for what's next.</p>
      </div>

      <div class="footer-links-group">
        <div class="footer-col">
          <h4 class="footer-col-title">Navigate</h4>
          <a href="/" class="footer-link">Home</a>
          <a href="/about" class="footer-link">About</a>
          <a href="/blog" class="footer-link">Blog</a>
          <a href="/start-here" class="footer-link">Start Here</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-col-title">Resources</h4>
          <a href="/sample" class="footer-link">Book Sample</a>
          <a href="/policies" class="footer-link">Policies</a>
          <a href="/policies#disclaimers" class="footer-link">Disclaimers</a>
        </div>
      </div>
    </div>

    <div class="footer-divider"></div>

    <div class="footer-bottom">
      <p class="footer-disclaimer">
        The content on this site represents educated guesses and personal opinions. Nothing is certain about the future.
        This is commentary only — not financial, legal, or professional advice.
      </p>
      <p class="footer-copyright">
        &copy; {new Date().getFullYear()} Surviving the Singularity. Built with curiosity.
      </p>
    </div>
  </div>
</footer>

<style>
  .site-footer {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0) 0%, #020617 100%);
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
    max-width: 300px;
  }

  .footer-logo-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    margin-bottom: 0.75rem;
  }

  .footer-logo {
    width: 28px;
    height: 28px;
    border-radius: 6px;
  }

  .footer-brand-name {
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
  }

  .footer-tagline {
    font-size: 0.85rem;
    color: #64748b;
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
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    margin: 0 0 0.25rem 0;
  }

  .footer-link {
    font-size: 0.85rem;
    color: #94a3b8;
    text-decoration: none;
    transition: color 0.2s;
    padding: 0.15rem 0;
  }

  .footer-link:hover {
    color: #e2e8f0;
  }

  .footer-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.1), transparent);
    margin: 2.5rem 0;
  }

  .footer-bottom {
    text-align: center;
  }

  .footer-disclaimer {
    font-size: 0.75rem;
    color: #475569;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto 1rem;
  }

  .footer-copyright {
    font-size: 0.7rem;
    color: #334155;
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
