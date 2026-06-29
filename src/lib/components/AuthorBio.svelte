<script>
  // Author bio block for /book landing page. Cross-links to home base
  // (thecoffeejesus.com) + Substack + GitHub. Uses theme tokens from theme.css.
  export let headshot = '/author-headshot.png';
  export let name = 'Christopher Tavolazzi';
  export let alias = 'The Coffee Jesus';
</script>

<section class="author-bio">
  <div class="eyebrow">About the Author</div>
  <div class="bio-grid">
    <div class="bio-photo">
      <img src={headshot} alt="Portrait of {name}" loading="lazy" width="160" height="160" />
      <div class="photo-glow" aria-hidden="true"></div>
    </div>
    <div class="bio-text">
      <h3>{name}</h3>
      <p class="alias">a.k.a. <span class="mono">{alias}</span></p>
      <p class="bio-roles">Developer, futurist, musician ☕</p>
      <p class="bio-founder">Founder of <a href="https://johnnyautoseed.com" target="_blank" rel="noopener noreferrer">Johnny Autoseed</a>.</p>
      <p>
        Reskilling people to pilot robots and do real, meaningful work. An autonomous seed-to-table pipeline bridging kitchens and community gardens with AI-driven robotics.
      </p>
      <p>
        I write to make sense of the shift in real time. The book updates as the world does.
      </p>
      <div class="bio-links">
        <a href="https://thecoffeejesus.com" target="_blank" rel="noopener noreferrer">🌐 Home base</a>
        <a href="https://thecoffeejesus.substack.com" target="_blank" rel="noopener noreferrer">✍️ Substack</a>
        <a href="https://github.com/ctavolazzi" target="_blank" rel="noopener noreferrer">⌨️ GitHub</a>
        <a href="https://www.youtube.com/@thecoffeejesus" target="_blank" rel="noopener noreferrer">▶️ YouTube</a>
      </div>
    </div>
  </div>
</section>

<style>
  .author-bio {
    background: var(--color-surface, rgba(30,41,59,0.5));
    border: 1px solid var(--color-border, rgba(148,163,184,0.1));
    border-radius: var(--radius-lg, 16px);
    padding: 2.5rem;
    margin-bottom: 2rem;
  }

  .eyebrow {
    display: inline-block;
    font-family: var(--font-mono, var(--font-primary));
    font-size: 0.85rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--color-primary, #f59e0b);
    margin-bottom: 1.25rem;
  }

  .bio-grid {
    display: grid;
    grid-template-columns: 160px 1fr;
    gap: 1.75rem;
    align-items: start;
  }

  .bio-photo {
    position: relative;
    width: 160px;
    height: 160px;
  }

  .bio-photo img {
    width: 160px;
    height: 160px;
    object-fit: cover;
    border-radius: var(--radius-md, 12px);
    border: 1px solid var(--color-border, rgba(148,163,184,0.15));
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.6);
    position: relative;
    z-index: 1;
    display: block;
  }

  .photo-glow {
    position: absolute;
    inset: -10%;
    background: radial-gradient(circle, var(--color-primary, #f59e0b) 0%, transparent 65%);
    filter: blur(28px);
    opacity: 0.28;
    z-index: 0;
    pointer-events: none;
  }

  .bio-text h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-text-primary, #f1f5f9);
    margin: 0 0 0.25rem;
    font-family: var(--font-primary, 'Inter', sans-serif);
  }

  .alias {
    font-size: 0.9rem;
    margin: 0 0 1rem;
    color: var(--color-text-muted, #dde4ef);
  }

  .alias .mono {
    font-family: var(--font-mono, var(--font-primary));
    color: var(--color-primary, #f59e0b);
  }

  .bio-text p {
    color: var(--color-text-secondary, #dde4ef);
    line-height: 1.7;
    margin: 0 0 1rem;
  }

  .bio-roles {
    font-size: 0.82rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin: 0 0 0.35rem;
    color: var(--color-text-muted, #94a3b8);
  }

  .bio-text a {
    color: var(--color-primary, #f59e0b);
    text-decoration: none;
    border-bottom: 1px dashed currentColor;
  }
  .bio-text a:hover { color: var(--color-primary-light, #fbbf24); }

  .bio-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1.25rem;
    margin-top: 1.25rem;
  }

  .bio-links a {
    font-size: 0.9rem;
    border-bottom: none;
    color: var(--color-text-primary, #f1f5f9);
    transition: color 150ms ease;
  }
  .bio-links a:hover {
    color: var(--color-primary, #f59e0b);
  }

  @media (max-width: 640px) {
    .author-bio { padding: 1.5rem; }
    .bio-grid {
      grid-template-columns: 1fr;
      justify-items: center;
      text-align: center;
    }
    .bio-links { justify-content: center; }
  }
</style>
