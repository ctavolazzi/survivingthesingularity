<script>
  // Wire this to your Stripe payment link when ready
  const STRIPE_LINK = '#';
</script>

<svelte:head>
  <title>Early Access — Surviving the Singularity</title>
  <meta name="description" content="$5 gets you instant access to the full blueprint, checklist, live research feed, book draft, and everything I ship next. Limited time pricing." />
</svelte:head>

<!-- ── HERO ── -->
<section class="ea-hero">
  <div class="ea-hero-inner">

    <!-- Book cover -->
    <div class="ea-cover-col">
      <div class="ea-cover-wrap">
        <div class="ea-cover-glow" aria-hidden="true"></div>
        <img
          src="/images/surviving_the_singularity_cover_1200.png"
          alt="Surviving the Singularity book cover"
          class="ea-cover-img"
          width="600"
          height="800"
        />
        <div class="ea-cover-badge">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
            <circle cx="6" cy="6" r="6" fill="#f59e0b" opacity="0.2"/>
            <circle cx="6" cy="6" r="3" fill="#f59e0b"/>
          </svg>
          Book draft in progress
        </div>
      </div>
    </div>

    <!-- Offer card -->
    <div class="ea-offer-col">
      <div class="ea-urgency-badge">
        <span class="ea-urgency-dot" aria-hidden="true"></span>
        Limited time offer
      </div>

      <h1 class="ea-heading">
        Everything I'm<br>building.<br><span class="ea-amber">Five dollars.</span>
      </h1>
      <p class="ea-sub">
        One payment. Instant access to the full blueprint, every chapter, the live research feed, and everything I ship next. This price goes up.
      </p>

      <div class="ea-price-card">
        <div class="ea-price-row">
          <div class="ea-price-amount"><sup>$</sup>5</div>
          <div class="ea-price-meta-col">
            <span class="ea-price-type">one-time payment</span>
            <span class="ea-price-note">instant access &middot; keeps growing</span>
          </div>
        </div>

        <a href={STRIPE_LINK} class="ea-buy-btn">
          Get Early Access Now
          <span class="ea-buy-icon" aria-hidden="true">
            <svg width="13" height="13" viewBox="0 0 12 12" fill="none"><path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </span>
        </a>

        <ul class="ea-quick-list">
          <li>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
            12-step readiness checklist
          </li>
          <li>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
            Full blueprint &mdash; all 8 chapters
          </li>
          <li>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
            Live research signal feed
          </li>
          <li>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
            Book draft + everything I ship next
          </li>
        </ul>

        <p class="ea-secure-note">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          Secure checkout via Stripe. <a href="/policies">Privacy policy</a>.
        </p>
      </div>
    </div>

  </div>
</section>

<!-- ── CONTENT PREVIEW (chapter images) ── -->
<section class="ea-preview">
  <div class="ea-preview-inner">
    <p class="ea-label">A look inside</p>
    <h2 class="ea-preview-heading">The book the blueprint is based on.</h2>
    <p class="ea-preview-sub">Written in public, updated as the field moves. You're reading it as it's being built.</p>

    <div class="ea-image-grid">
      <div class="ea-img-cell ea-img-large">
        <img src="/book-images/ch02-factory-robots.jpg" alt="Factory automation robots — Chapter 2" loading="lazy" />
        <div class="ea-img-cap">Physical Automation</div>
      </div>
      <div class="ea-img-cell">
        <img src="/book-images/ch11-spot.jpg" alt="Boston Dynamics Spot — Chapter 11" loading="lazy" />
        <div class="ea-img-cap">Field Robotics</div>
      </div>
      <div class="ea-img-cell">
        <img src="/book-images/ch12-farmbot.jpg" alt="FarmBot garden automation — Chapter 12" loading="lazy" />
        <div class="ea-img-cap">Food Autonomy</div>
      </div>
      <div class="ea-img-cell ea-img-wide">
        <img src="/book-images/ch01-atlas.jpg" alt="Boston Dynamics Atlas — Chapter 1" loading="lazy" />
        <div class="ea-img-cap">The New Era</div>
      </div>
    </div>
  </div>
</section>

<!-- ── WHAT YOU GET ── -->
<section class="ea-includes">
  <div class="ea-includes-inner">
    <p class="ea-label">What's included</p>
    <h2 class="ea-includes-heading">The full kit, right now.</h2>

    <div class="ea-items">

      <div class="ea-item">
        <div class="ea-item-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
          </svg>
        </div>
        <div class="ea-item-body">
          <div class="ea-item-name">Readiness Checklist</div>
          <div class="ea-item-desc">12 concrete steps. Cost estimate per step. Ordered by impact. Starts where you are right now.</div>
          <span class="ea-tag ea-tag-live">Live now</span>
        </div>
      </div>

      <div class="ea-item">
        <div class="ea-item-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/>
          </svg>
        </div>
        <div class="ea-item-body">
          <div class="ea-item-name">Full Blueprint, All 8 Chapters</div>
          <div class="ea-item-desc">Local AI, physical automation, food security, energy, digital leverage. Deep and specific, not motivational.</div>
          <span class="ea-tag ea-tag-live">Live now</span>
        </div>
      </div>

      <div class="ea-item">
        <div class="ea-item-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </div>
        <div class="ea-item-body">
          <div class="ea-item-name">Research Signal Feed</div>
          <div class="ea-item-desc">Curated arXiv papers, robotics breakthroughs, AI policy signals. Updated automatically as the field moves.</div>
          <span class="ea-tag ea-tag-live">Live now</span>
        </div>
      </div>

      <div class="ea-item">
        <div class="ea-item-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/>
          </svg>
        </div>
        <div class="ea-item-body">
          <div class="ea-item-name">Book Draft</div>
          <div class="ea-item-desc">Read <em>Surviving the Singularity</em> as it's being written. See the thinking before it's polished.</div>
          <span class="ea-tag ea-tag-draft">In progress</span>
        </div>
      </div>

      <div class="ea-item">
        <div class="ea-item-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
        </div>
        <div class="ea-item-body">
          <div class="ea-item-name">Everything I Ship Next</div>
          <div class="ea-item-desc">New tools, frameworks, and resources as they come out. Early access price never goes up for you.</div>
          <span class="ea-tag ea-tag-soon">Ongoing</span>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ── AUTHOR ── -->
<section class="ea-author">
  <div class="ea-author-inner">
    <div class="ea-author-photo-wrap">
      <img src="/author-headshot.png" alt="Author photo" class="ea-author-photo" width="120" height="120" loading="lazy" />
    </div>
    <div class="ea-author-copy">
      <p class="ea-label">Who's building this</p>
      <p class="ea-author-text">
        I'm writing this book and building these tools in public, because I think the window to prepare is shorter than most people expect. The $5 gets you everything I've made so far and everything I make next. No gatekeeping, no upsells.
      </p>
    </div>
  </div>
</section>

<!-- ── BOTTOM CTA ── -->
<section class="ea-bottom">
  <div class="ea-bottom-inner">
    <p class="ea-urgency-inline">
      <span class="ea-urgency-dot" aria-hidden="true"></span>
      Limited time offer
    </p>
    <h2 class="ea-bottom-heading">Five dollars.<br>Don't wait.</h2>
    <p class="ea-bottom-sub">This is the lowest the price will ever be. Everything I'm building, open to you now.</p>
    <a href={STRIPE_LINK} class="ea-bottom-btn">
      Get Early Access - $5
      <svg width="16" height="16" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
    <p class="ea-bottom-fine">Secure checkout via Stripe. Instant access. <a href="/policies">Privacy</a>.</p>
  </div>
</section>

<style>
  /* ── TOKENS ── */
  :root {
    --amber: #f59e0b;
    --amber-dim: rgba(245,158,11,0.12);
    --amber-glow: rgba(245,158,11,0.18);
    --surface: #0f172a;
    --surface-2: #1e293b;
    --border: rgba(255,255,255,0.05);
    --border-mid: rgba(255,255,255,0.09);
    --text-1: #f8fafc;
    --text-2: #cbd5e1;
    --text-3: #64748b;
    --green: #10b981;
    --r-card: 20px;
    --r-pill: 999px;
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  /* ── HERO ── */
  .ea-hero {
    padding-top: clamp(80px, 12vw, 120px);
    padding-bottom: clamp(48px, 7vw, 80px);
    background: linear-gradient(180deg, rgba(245,158,11,0.04) 0%, transparent 60%);
  }
  .ea-hero-inner {
    max-width: 1080px; margin: 0 auto;
    padding: 0 clamp(20px, 5vw, 48px);
    display: grid;
    grid-template-columns: 1fr 1.1fr;
    gap: clamp(32px, 5vw, 64px);
    align-items: center;
  }
  @media (max-width: 768px) {
    .ea-hero-inner { grid-template-columns: 1fr; }
  }

  /* Book cover */
  .ea-cover-col { display: flex; justify-content: center; }
  .ea-cover-wrap { position: relative; display: inline-block; }
  .ea-cover-glow {
    position: absolute; inset: -20px;
    background: radial-gradient(ellipse at center, rgba(245,158,11,0.25) 0%, transparent 70%);
    filter: blur(20px); z-index: 0; pointer-events: none;
  }
  .ea-cover-img {
    position: relative; z-index: 1;
    width: min(340px, 100%); height: auto;
    border-radius: 8px;
    box-shadow: 0 32px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(245,158,11,0.15);
    transform: perspective(1200px) rotateY(4deg);
  }
  .ea-cover-badge {
    position: absolute; bottom: -14px; left: 50%; transform: translateX(-50%);
    z-index: 2;
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(15,23,42,0.9); border: 1px solid var(--border-mid);
    border-radius: var(--r-pill); padding: 6px 14px;
    font-size: 0.78rem; color: var(--text-2); white-space: nowrap;
    backdrop-filter: blur(12px);
  }

  /* Urgency badge */
  .ea-urgency-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 14px;
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: var(--r-pill);
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--amber); margin-bottom: 20px;
  }
  .ea-urgency-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--amber); box-shadow: 0 0 8px var(--amber);
    flex-shrink: 0;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
  }
  @media (prefers-reduced-motion: reduce) { .ea-urgency-dot { animation: none; } }

  .ea-heading {
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 900; line-height: 1.0;
    letter-spacing: -0.025em; color: var(--text-1);
    margin-bottom: 16px;
  }
  .ea-amber { color: var(--amber); }

  .ea-sub {
    font-size: clamp(0.95rem, 2vw, 1.05rem);
    color: var(--text-2); line-height: 1.65;
    margin-bottom: 28px; max-width: 480px;
  }

  /* Price card */
  .ea-price-card {
    background: var(--surface);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: var(--r-card);
    padding: 24px 24px 20px;
    box-shadow: 0 0 0 1px rgba(245,158,11,0.06), 0 24px 64px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
  }
  .ea-price-row {
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 20px;
  }
  .ea-price-amount {
    font-size: 3.6rem; font-weight: 900; color: var(--text-1);
    line-height: 1; letter-spacing: -0.04em; flex-shrink: 0;
  }
  .ea-price-amount sup {
    font-size: 0.38em; vertical-align: super;
    font-weight: 700; color: var(--amber);
  }
  .ea-price-meta-col {
    display: flex; flex-direction: column; gap: 4px;
  }
  .ea-price-type {
    font-size: 0.85rem; font-weight: 700; color: var(--text-1); line-height: 1.2;
  }
  .ea-price-note {
    font-size: 0.75rem; color: var(--text-3);
    font-family: 'JetBrains Mono', monospace;
  }
  .ea-buy-btn {
    display: flex; align-items: center; justify-content: center; gap: 10px;
    width: 100%; padding: 15px 24px;
    background: var(--amber); color: #0a0a0a;
    font-size: 1rem; font-weight: 800;
    border: none; border-radius: var(--r-pill); cursor: pointer;
    text-decoration: none; white-space: nowrap;
    box-shadow: 0 4px 20px rgba(245,158,11,0.35);
    transition: filter 0.2s ease, transform 0.2s var(--ease-spring), box-shadow 0.2s ease;
    margin-bottom: 16px;
  }
  .ea-buy-btn:hover {
    filter: brightness(1.08); transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(245,158,11,0.45);
  }
  .ea-buy-btn:active { transform: scale(0.98); }
  .ea-buy-icon {
    width: 26px; height: 26px; background: rgba(0,0,0,0.15);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }

  .ea-quick-list {
    list-style: none; display: flex; flex-direction: column; gap: 8px;
    margin-bottom: 16px;
  }
  .ea-quick-list li {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.85rem; color: var(--text-2);
  }
  .ea-secure-note {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.75rem; color: var(--text-3); padding-top: 12px;
    border-top: 1px solid var(--border);
  }
  .ea-secure-note a { color: var(--text-2); text-decoration: underline; text-underline-offset: 2px; }

  /* ── CONTENT PREVIEW ── */
  .ea-preview {
    border-top: 1px solid var(--border);
    padding: clamp(48px, 7vw, 80px) 0;
  }
  .ea-preview-inner {
    max-width: 1080px; margin: 0 auto;
    padding: 0 clamp(20px, 5vw, 48px);
  }
  .ea-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: var(--amber); margin-bottom: 10px;
  }
  .ea-preview-heading {
    font-size: clamp(1.5rem, 3.5vw, 2.2rem); font-weight: 800;
    color: var(--text-1); letter-spacing: -0.02em; line-height: 1.15;
    margin-bottom: 10px;
  }
  .ea-preview-sub {
    font-size: 1rem; color: var(--text-3); margin-bottom: 32px; max-width: 520px;
  }

  .ea-image-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 8px;
  }
  .ea-img-cell {
    position: relative; overflow: hidden;
    border-radius: 12px;
    background: var(--surface);
    aspect-ratio: 4/3;
  }
  .ea-img-large {
    grid-row: 1 / 3;
    aspect-ratio: unset;
  }
  .ea-img-wide {
    grid-column: 2 / 4;
    aspect-ratio: 16/7;
  }
  .ea-img-cell img {
    width: 100%; height: 100%; object-fit: cover;
    transition: transform 0.5s var(--ease-out);
    display: block;
  }
  .ea-img-cell:hover img { transform: scale(1.04); }
  .ea-img-cap {
    position: absolute; bottom: 10px; left: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: rgba(255,255,255,0.7);
    background: rgba(2,6,23,0.65);
    padding: 3px 8px; border-radius: 4px;
    backdrop-filter: blur(6px);
  }
  @media (max-width: 640px) {
    .ea-image-grid {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto auto;
    }
    .ea-img-large { grid-row: auto; aspect-ratio: 4/3; }
    .ea-img-wide { grid-column: 1 / 3; }
  }

  /* ── INCLUDES ── */
  .ea-includes {
    border-top: 1px solid var(--border);
    padding: clamp(48px, 7vw, 80px) 0;
  }
  .ea-includes-inner {
    max-width: 1080px; margin: 0 auto;
    padding: 0 clamp(20px, 5vw, 48px);
  }
  .ea-includes-heading {
    font-size: clamp(1.5rem, 3.5vw, 2.2rem); font-weight: 800;
    color: var(--text-1); letter-spacing: -0.02em;
    margin-bottom: clamp(28px, 4vw, 44px);
  }

  .ea-items {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  @media (max-width: 640px) {
    .ea-items { grid-template-columns: 1fr; }
  }
  .ea-item {
    display: flex; gap: 16px; align-items: flex-start;
    background: var(--surface);
    border: 1px solid var(--border-mid);
    border-radius: var(--r-card);
    padding: 20px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .ea-item:hover {
    border-color: rgba(245,158,11,0.2);
    box-shadow: 0 8px 28px rgba(0,0,0,0.25);
  }
  .ea-item-icon {
    width: 40px; height: 40px; flex-shrink: 0;
    background: var(--amber-dim);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    color: var(--amber);
  }
  .ea-item-body { flex: 1; min-width: 0; }
  .ea-item-name {
    font-size: 0.95rem; font-weight: 700; color: var(--text-1);
    margin-bottom: 4px; line-height: 1.3;
  }
  .ea-item-desc {
    font-size: 0.85rem; color: var(--text-3); line-height: 1.5; margin-bottom: 8px;
  }
  .ea-tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace; font-size: 0.64rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    padding: 2px 8px; border-radius: 4px;
  }
  .ea-tag-live { background: rgba(16,185,129,0.12); color: var(--green); }
  .ea-tag-draft { background: var(--amber-dim); color: var(--amber); }
  .ea-tag-soon { background: rgba(148,163,184,0.08); color: var(--text-3); }

  /* ── AUTHOR ── */
  .ea-author {
    border-top: 1px solid var(--border);
    padding: clamp(40px, 6vw, 64px) 0;
    background: linear-gradient(180deg, transparent 0%, rgba(245,158,11,0.03) 100%);
  }
  .ea-author-inner {
    max-width: 1080px; margin: 0 auto;
    padding: 0 clamp(20px, 5vw, 48px);
    display: flex; gap: 28px; align-items: center;
  }
  @media (max-width: 640px) {
    .ea-author-inner { flex-direction: column; align-items: flex-start; }
  }
  .ea-author-photo-wrap { flex-shrink: 0; }
  .ea-author-photo {
    width: 88px; height: 88px; border-radius: 50%; object-fit: cover;
    border: 2px solid rgba(245,158,11,0.3);
    box-shadow: 0 0 0 4px rgba(245,158,11,0.08);
  }
  .ea-author-text {
    font-size: clamp(0.95rem, 2vw, 1.05rem); color: var(--text-2);
    line-height: 1.7; max-width: 600px; margin-top: 8px;
  }

  /* ── BOTTOM CTA ── */
  .ea-bottom {
    border-top: 1px solid var(--border);
    padding: clamp(64px, 10vw, 100px) 0;
    text-align: center;
  }
  .ea-bottom-inner {
    max-width: 600px; margin: 0 auto;
    padding: 0 clamp(20px, 5vw, 48px);
  }
  .ea-urgency-inline {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--amber); margin-bottom: 20px;
  }
  .ea-bottom-heading {
    font-size: clamp(2.4rem, 7vw, 4rem);
    font-weight: 900; line-height: 1.0; letter-spacing: -0.025em;
    color: var(--text-1); margin-bottom: 16px;
  }
  .ea-bottom-sub {
    font-size: 1.05rem; color: var(--text-3); margin-bottom: 36px; line-height: 1.6;
  }
  .ea-bottom-btn {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 17px 36px;
    background: var(--amber); color: #0a0a0a;
    font-size: 1.05rem; font-weight: 800;
    border-radius: var(--r-pill); text-decoration: none;
    box-shadow: 0 4px 20px rgba(245,158,11,0.4);
    transition: filter 0.2s ease, transform 0.2s var(--ease-spring);
    margin-bottom: 16px;
  }
  .ea-bottom-btn:hover { filter: brightness(1.08); transform: translateY(-2px); }
  .ea-bottom-btn:active { transform: scale(0.98); }
  .ea-bottom-fine {
    font-size: 0.8rem; color: var(--text-3);
  }
  .ea-bottom-fine a { color: var(--text-2); text-decoration: underline; text-underline-offset: 2px; }
</style>
