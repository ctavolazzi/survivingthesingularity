<script>
  import { sections } from '$lib/data/blueprint.js';
</script>

<svelte:head>
  <title>Optional Content Review: Surviving the Singularity</title>
  <meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div class="opt-page">

  <header class="opt-header">
    <p class="opt-eyebrow">Internal Review Only</p>
    <h1 class="opt-title">Retired Content</h1>
    <p class="opt-sub">Pages removed from the public site. Review what was here, decide what to keep or merge into the book. Everything is git-recoverable on branch <code>homepage-redux-jun2026</code>.</p>
  </header>

  <!-- ── OLD BLUEPRINT CHAPTERS ── -->
  <section class="opt-section">
    <div class="opt-section-head">
      <span class="opt-tag">Was: /blueprint</span>
      <h2 class="opt-section-title">The YouTube Shouse Blueprint</h2>
      <p class="opt-section-desc">8 chapters of tactical material-independence content. Steel construction, FarmBot, local AI, YouTube monetization, land acquisition. Data-heavy with cost tables and specs.</p>
    </div>

    <div class="opt-grid">
      {#each sections as s}
        <div class="opt-card">
          <span class="opt-card-num">{s.number}</span>
          <div class="opt-card-body">
            <div class="opt-card-title">{s.title}</div>
            <div class="opt-card-sub">{s.subtitle}</div>
            <div class="opt-card-blocks">
              {s.content?.length ?? 0} content blocks
              ({s.content?.filter(b => b.type === 'table').length ?? 0} tables,
              {s.content?.filter(b => b.type === 'prose').length ?? 0} prose)
            </div>
          </div>
        </div>
      {/each}
    </div>

    <p class="opt-note">Full content still available in <code>src/lib/data/blueprint.js</code>. The renderer at <code>src/routes/blueprint/[section]</code> is deleted but data is intact.</p>
  </section>

  <!-- ── AGI PAGE ── -->
  <section class="opt-section">
    <div class="opt-section-head">
      <span class="opt-tag">Was: /agi</span>
      <h2 class="opt-section-title">What is AGI?</h2>
      <p class="opt-section-desc">1,734-line explainer page. Covered: AI spectrum (ANI to AGI to ASI), expert timeline forecasts (Altman 2025-27, Hinton 5-20yr), 6 things AGI could do for humanity, 4 prep actions, technology watch list, interactive scenario builder. Linked heavily to /why and /checklist.</p>
    </div>
    <div class="opt-items">
      <div class="opt-item">
        <span class="opt-item-label">Key content</span>
        <span class="opt-item-val">AI level cards (ANI / AGI / ASI), expert forecasts table, "What AGI could do" grid (6 domains), "Why prepare now" section, tech watch list</span>
      </div>
      <div class="opt-item">
        <span class="opt-item-label">Possible merge target</span>
        <span class="opt-item-val">Part I of the book page (What is the Singularity) could absorb the AI-level cards and expert timeline data</span>
      </div>
    </div>
  </section>

  <!-- ── WHY PAGE ── -->
  <section class="opt-section">
    <div class="opt-section-head">
      <span class="opt-tag">Was: /why</span>
      <h2 class="opt-section-title">Why Now</h2>
      <p class="opt-section-desc">1,479-line evidence-and-timeline page. Covered: public milestones (2023-2026), paraphrased researcher positions, benchmark notes, the "one way to think about it" framing, Discord community section, final CTA. Sourced and epistemic-humility framing throughout.</p>
    </div>
    <div class="opt-items">
      <div class="opt-item">
        <span class="opt-item-label">Key content</span>
        <span class="opt-item-val">6 milestone dates with plain-language explanations, 5+ researcher positions paraphrased, benchmark figures (SWE-bench, ARC, MMLU)</span>
      </div>
      <div class="opt-item">
        <span class="opt-item-label">Possible merge target</span>
        <span class="opt-item-val">The Mathematical Map in Part I of the rebuilt book page; or a standalone "Evidence" appendix if /evidence stays retired</span>
      </div>
    </div>
  </section>

  <!-- ── EVIDENCE PAGE ── -->
  <section class="opt-section">
    <div class="opt-section-head">
      <span class="opt-tag">Was: /evidence</span>
      <h2 class="opt-section-title">The Evidence</h2>
      <p class="opt-section-desc">728-line curated evidence hub. Organized by category (Physical Automation, Knowledge Work, Creative, Healthcare, etc.) with tagged, searchable evidence items linking to primary sources. Timeline bar at top. Designed for skeptics and researchers.</p>
    </div>
    <div class="opt-items">
      <div class="opt-item">
        <span class="opt-item-label">Key content</span>
        <span class="opt-item-val">Categorized evidence items with external links to footage, papers, and deployment data. Copy-to-clipboard export. Structured data still in its data file.</span>
      </div>
      <div class="opt-item">
        <span class="opt-item-label">Possible merge target</span>
        <span class="opt-item-val">Could become an appendix or "Sources" section in the book. Or restore as a linked resource from the book page if it earns its place.</span>
      </div>
    </div>
  </section>

  <!-- ── SHOUSE PAGE ── -->
  <section class="opt-section">
    <div class="opt-section-head">
      <span class="opt-tag">Was: /shouse</span>
      <h2 class="opt-section-title">Shouse Builder (3D Game)</h2>
      <p class="opt-section-desc">A 3D isometric strategy game: build a $25K shouse (container shell, solar, local-AI rack, FarmBot bed) before a deadline. Powered by <code>ShouseGame.svelte</code> in <code>src/lib/components/game/</code>.</p>
    </div>
    <div class="opt-items">
      <div class="opt-item">
        <span class="opt-item-label">Component status</span>
        <span class="opt-item-val">The ShouseGame component still exists. Only the route is retired. Can be restored or linked from the book's Part III (Shouse Grid section).</span>
      </div>
    </div>
  </section>

  <!-- ── TIMELINE / SITEMAP ── -->
  <section class="opt-section">
    <div class="opt-section-head">
      <span class="opt-tag">Was: /timeline + /sitemap</span>
      <h2 class="opt-section-title">Timeline + Human Sitemap</h2>
      <p class="opt-section-desc">/timeline was 1 line (stub). /sitemap was a human-readable site index. Both retired. <code>sitemap.xml</code> (machine-readable) still exists at the root.</p>
    </div>
  </section>

</div>

<style>
  .opt-page {
    max-width: 860px;
    margin: 0 auto;
    padding: clamp(2rem, 5vw, 4rem) clamp(1rem, 4vw, 2rem);
    color: #e2e8f0;
    font-family: 'Outfit', system-ui, sans-serif;
  }

  .opt-header {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(245, 158, 11, 0.25);
  }

  .opt-eyebrow {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #f59e0b;
    margin: 0 0 0.6rem;
    font-family: 'JetBrains Mono', monospace;
  }

  .opt-title {
    font-size: clamp(1.8rem, 5vw, 2.8rem);
    font-weight: 900;
    color: #f1f5f9;
    margin: 0 0 0.75rem;
    letter-spacing: -0.03em;
  }

  .opt-sub {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
  }

  code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    background: rgba(255, 255, 255, 0.06);
    padding: 0.15em 0.4em;
    border-radius: 3px;
    color: #f59e0b;
  }

  .opt-section {
    margin-bottom: 3rem;
    padding-bottom: 2.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }

  .opt-section:last-child { border-bottom: none; }

  .opt-section-head { margin-bottom: 1.5rem; }

  .opt-tag {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #64748b;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.25rem 0.6rem;
    margin-bottom: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
  }

  .opt-section-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
  }

  .opt-section-desc {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
    max-width: 680px;
  }

  .opt-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  @media (max-width: 560px) {
    .opt-grid { grid-template-columns: 1fr; }
  }

  .opt-card {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-left: 2px solid rgba(245, 158, 11, 0.3);
  }

  .opt-card-num {
    font-size: 0.7rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
    margin-top: 0.1rem;
  }

  .opt-card-body { flex: 1; min-width: 0; }

  .opt-card-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.2rem;
  }

  .opt-card-sub {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0 0 0.3rem;
    line-height: 1.4;
  }

  .opt-card-blocks {
    font-size: 0.72rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
  }

  .opt-note {
    font-size: 0.8rem;
    color: #475569;
    line-height: 1.5;
    margin: 0;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.02);
    border-left: 2px solid rgba(255, 255, 255, 0.06);
  }

  .opt-items {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .opt-item {
    display: grid;
    grid-template-columns: 160px 1fr;
    gap: 1rem;
    padding: 0.75rem;
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 0.85rem;
    line-height: 1.5;
  }

  @media (max-width: 560px) {
    .opt-item { grid-template-columns: 1fr; }
  }

  .opt-item-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    padding-top: 0.1rem;
  }

  .opt-item-val { color: #94a3b8; }
</style>
