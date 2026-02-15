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
          <a href="/policies" class="footer-link">Policies</a>
        </div>
      </div>
    </div>

    <div class="footer-divider"></div>

    <div class="footer-bottom">
      <p class="footer-disclaimer">
        This is commentary only — not financial, legal, or professional advice. Build at your own risk. Think for yourself.
      </p>
      <p class="footer-copyright">
        &copy; {new Date().getFullYear()} Surviving the Singularity. Built with your own two hands.
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
    font-family: 'JetBrains Mono', monospace;
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
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
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
    color: #f59e0b;
  }

  .footer-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.15), transparent);
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
