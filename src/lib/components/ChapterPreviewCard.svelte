<script>
  // Rich card for a single chapter, used on the /book landing page grid.
  // Section shape comes from sectionsWithMeta in $lib/bookContent.js.
  export let section;
  export let index = 0;

  // Parse "Chapter N: Long Title" → { num, title } so we can style the number
  // separately and surface a shorter title in the card body.
  $: parsed = (() => {
    const m = /^Chapter\s+(\d+)\s*[:.\-]\s*(.+)$/i.exec(section.title);
    if (m) return { num: parseInt(m[1], 10), title: m[2] };
    return { num: null, title: section.title };
  })();

  $: chapterLabel = parsed.num != null
    ? `Ch. ${String(parsed.num).padStart(2, '0')}`
    : section.id.replace(/-/g, ' ');
</script>

<a class="chapter-card" href="/book/{section.id}" data-index={index}>
  <div class="card-meta">
    <span class="ch-num">{chapterLabel}</span>
    {#if section.readMinutes}
      <span class="read-time">{section.readMinutes} min read</span>
    {/if}
  </div>
  <h3 class="card-title">{parsed.title}</h3>
  {#if section.teaser}
    <p class="card-teaser">{section.teaser}</p>
  {/if}
  <div class="card-cta">Read chapter <span aria-hidden="true">→</span></div>
</a>

<style>
  .chapter-card {
    display: flex;
    flex-direction: column;
    background: var(--color-bg-secondary, #0f172a);
    border: 1px solid var(--color-border, rgba(148,163,184,0.1));
    border-radius: var(--radius-md, 12px);
    padding: 1.25rem 1.25rem 1.5rem;
    text-decoration: none;
    color: inherit;
    transition: transform 200ms ease, border-color 200ms ease, box-shadow 200ms ease;
    position: relative;
    overflow: hidden;
    height: 100%;
  }

  .chapter-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    pointer-events: none;
    box-shadow: 0 0 0 0 rgba(245, 158, 11, 0);
    transition: box-shadow 200ms ease;
  }

  .chapter-card:hover {
    border-color: var(--color-primary, #f59e0b);
    transform: translateY(-3px);
  }
  .chapter-card:hover::before {
    box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.35), 0 12px 30px -10px rgba(245, 158, 11, 0.18);
  }

  .card-meta {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.65rem;
  }

  .ch-num {
    font-family: var(--font-mono, var(--font-primary));
    font-size: 0.86rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-primary, #f59e0b);
    font-weight: 600;
  }

  .read-time {
    font-family: var(--font-mono, var(--font-primary));
    font-size: 0.82rem;
    color: var(--color-text-muted, #dde4ef);
  }

  .card-title {
    font-family: var(--font-primary, 'Inter', sans-serif);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--color-text-primary, #f1f5f9);
    line-height: 1.3;
    margin: 0 0 0.5rem;
  }

  .card-teaser {
    font-size: 0.88rem;
    color: var(--color-text-secondary, #dde4ef);
    line-height: 1.55;
    margin: 0 0 1rem;
    /* Clamp teaser to 4 lines for consistent card heights */
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
    flex: 1;
  }

  .card-cta {
    font-family: var(--font-mono, var(--font-primary));
    font-size: 0.8rem;
    color: var(--color-primary, #f59e0b);
    margin-top: auto;
    letter-spacing: 0.05em;
  }

  .chapter-card:hover .card-cta {
    color: var(--color-primary-light, #fbbf24);
  }

  @media (prefers-reduced-motion: reduce) {
    .chapter-card:hover { transform: none; }
  }
</style>
