<script>
  const SUBSTACK_URL = 'https://thecoffeejesus.substack.com';
  const CONTACT_EMAIL = 'info@thecoffeejesus.com';
</script>

<section class="book-banner" aria-label="Book status announcement">
  <div class="inner">

    <!-- Cover -->
    <div class="cover-wrap">
      <div class="cover-glow" aria-hidden="true"></div>
      <img
        src="/images/surviving_the_singularity_cover_1200.png"
        alt="Surviving the Singularity — book cover"
        class="cover-img"
        width="300"
        height="450"
        loading="eager"
      />
      <div class="badge" aria-label="Status: In Editing">IN EDITING</div>
    </div>

    <!-- Content -->
    <div class="content">
      <p class="eyebrow">The Book</p>
      <h2 class="title">Surviving the Singularity</h2>
      <p class="status-line">
        <span class="status-dot" aria-hidden="true"></span>
        Currently in editing — releasing when it's ready
      </p>

      <p class="body">
        The book is being carefully edited and refined. No arbitrary release date —
        it ships when it's genuinely ready. Subscribe free to get notified the moment it launches.
      </p>

      <!-- Substack CTA -->
      <a
        href={SUBSTACK_URL}
        target="_blank"
        rel="noopener noreferrer"
        class="btn-subscribe"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M4 4h16v4H4z"/><path d="M4 12h16"/><path d="M4 20h16"/>
        </svg>
        Subscribe Free on Substack
      </a>
      <p class="sub-meta">Free subscription · unsubscribe anytime</p>

      <!-- Preorder notice -->
      <div class="preorder-notice" role="note">
        <svg class="notice-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <p>
          <strong>Pre-ordered the book?</strong>
          You'll be emailed at the address you submitted when you placed your order.
          If you don't receive a notification, please reach out:
          <a href="mailto:{CONTACT_EMAIL}" class="email-link">{CONTACT_EMAIL}</a>
        </p>
      </div>
    </div>

  </div>
</section>

<style>
  .book-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 1.25rem;
    padding: 3rem 2rem;
    margin: 3rem auto;
    max-width: 900px;
    box-shadow:
      0 0 0 1px rgba(245, 158, 11, 0.08),
      0 24px 64px rgba(0, 0, 0, 0.5);
  }

  .inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2.5rem;
  }

  @media (min-width: 680px) {
    .inner {
      flex-direction: row;
      align-items: flex-start;
    }
  }

  /* Cover */
  .cover-wrap {
    position: relative;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
  }

  .cover-glow {
    position: absolute;
    inset: -20px;
    background: radial-gradient(ellipse at center, rgba(245, 158, 11, 0.25) 0%, transparent 70%);
    border-radius: 50%;
    filter: blur(20px);
    pointer-events: none;
  }

  .cover-img {
    width: 200px;
    height: auto;
    border-radius: 0.5rem;
    box-shadow:
      0 4px 6px rgba(0,0,0,0.3),
      0 20px 40px rgba(0,0,0,0.5),
      4px 4px 0 rgba(245, 158, 11, 0.15);
    position: relative;
    z-index: 1;
    display: block;
  }

  @media (min-width: 680px) {
    .cover-img {
      width: 220px;
    }
  }

  .badge {
    position: absolute;
    top: -10px;
    right: -10px;
    z-index: 2;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
  }

  /* Content */
  .content {
    flex: 1;
    min-width: 0;
  }

  .eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0 0 0.5rem;
  }

  .title {
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 0.75rem;
    line-height: 1.15;
  }

  .status-line {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;
    margin: 0 0 1.25rem;
    font-family: 'JetBrains Mono', monospace;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #f59e0b;
    box-shadow: 0 0 8px #f59e0b;
    animation: pulse 2s ease-in-out infinite;
    flex-shrink: 0;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
  }

  .body {
    font-size: 1rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin: 0 0 1.75rem;
  }

  /* Subscribe button */
  .btn-subscribe {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.9rem 1.75rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-weight: 800;
    font-size: 0.95rem;
    border-radius: 10px;
    text-decoration: none;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    white-space: nowrap;
    margin-bottom: 0.5rem;
  }

  .btn-subscribe:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(245, 158, 11, 0.35);
  }

  .sub-meta {
    font-size: 0.72rem;
    color: #64748b;
    margin: 0 0 1.75rem;
  }

  /* Preorder notice */
  .preorder-notice {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    background: rgba(245, 158, 11, 0.07);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 0.75rem;
    padding: 1rem 1.1rem;
  }

  .notice-icon {
    color: #f59e0b;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .preorder-notice p {
    font-size: 0.875rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.6;
  }

  .preorder-notice strong {
    color: #e2e8f0;
  }

  .email-link {
    color: #f59e0b;
    text-decoration: none;
    font-weight: 600;
  }

  .email-link:hover {
    text-decoration: underline;
  }
</style>
