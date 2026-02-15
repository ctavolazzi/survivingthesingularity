<script>
  import { fly, fade } from 'svelte/transition';

  const rows = [
    {
      layer: 'Labor',
      old: 'Sedentary office toil',
      new: 'Biology-matched physical utility',
      tool: 'Mobile Aloha / DIY Robotics',
      detail: 'Instead of sitting at a desk 8 hours a day destroying your body, build things with your hands. Open-source robotics (Mobile Aloha, $32K) let you automate the repetitive physical tasks while you focus on creative work.',
      icon: 'L',
      color: '#f59e0b'
    },
    {
      layer: 'Capital',
      old: 'Inflationary fiat currency',
      new: 'Hard assets & cash flow products',
      tool: 'Lemon Squeezy / Digital Solutions',
      detail: 'Your money loses 5%+ per year sitting in a bank. Hard assets (land, buildings, tools) hold value. Digital products ($20 FogSift offers) create recurring cash flow that compounds instead of eroding.',
      icon: 'C',
      color: '#3b82f6'
    },
    {
      layer: 'Safety Net',
      old: 'Bismarckian PAYGO system',
      new: 'Reciprocal survival blueprints',
      tool: 'Title 25 Owner-Built Housing',
      detail: 'Social Security was designed when life expectancy was 63. The new safety net is a paid-off structure on owned land, food production capacity, and a community of builders who share knowledge freely.',
      icon: 'S',
      color: '#10b981'
    },
    {
      layer: 'Intelligence',
      old: 'Walled-garden APIs',
      new: 'Local, private, uncensored AI',
      tool: 'RTX 5090 / Llama 4 Scout',
      detail: 'Cloud AI providers can change pricing, censor outputs, or shut down access anytime. A $2,000 GPU running Llama 4 Scout locally gives you uncensored, private AI that works offline — forever.',
      icon: 'I',
      color: '#8b5cf6'
    },
    {
      layer: 'Reality',
      old: 'Algorithmic consumption',
      new: 'Evidence-based production',
      tool: 'YouTube / n8n Manifesto',
      detail: 'Stop consuming content designed to keep you scrolling. Start producing content that teaches what you know. The One-Hour Rule: anything that took you more than an hour to learn is worth a video.',
      icon: 'R',
      color: '#f97316'
    },
  ];

  let expandedIndex = -1;
  let hoveredIndex = -1;

  function toggleRow(i) {
    expandedIndex = expandedIndex === i ? -1 : i;
  }
</script>

<div class="stack-interactive">
  <div class="stack-header-row">
    <span class="sh-layer">Layer</span>
    <span class="sh-col">Old System</span>
    <span class="sh-col">New System</span>
    <span class="sh-col sh-tool">Sovereign Tool</span>
  </div>

  {#each rows as row, i}
    <button
      class="stack-row"
      class:stack-row-expanded={expandedIndex === i}
      class:stack-row-hovered={hoveredIndex === i}
      on:click={() => toggleRow(i)}
      on:mouseenter={() => hoveredIndex = i}
      on:mouseleave={() => hoveredIndex = -1}
      style="animation-delay: {i * 60}ms"
    >
      <div class="stack-row-main">
        <div class="stack-layer">
          <span class="layer-icon" style="background: {row.color}15; color: {row.color}; border-color: {row.color}30">{row.icon}</span>
          <span class="layer-name" style="color: {row.color}">{row.layer}</span>
        </div>
        <span class="stack-old">{row.old}</span>
        <span class="stack-new">{row.new}</span>
        <span class="stack-tool">{row.tool}</span>
        <svg class="stack-chevron" class:stack-chevron-open={expandedIndex === i} width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>

      {#if expandedIndex === i}
        <div class="stack-detail" transition:fly={{ y: -8, duration: 200 }}>
          <div class="detail-bar" style="background: {row.color}"></div>
          <p class="detail-text">{row.detail}</p>
        </div>
      {/if}
    </button>
  {/each}
</div>

<style>
  .stack-interactive {
    margin-top: 2rem;
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 16px;
    overflow: hidden;
  }

  .stack-header-row {
    display: grid;
    grid-template-columns: 180px 1fr 1fr 1fr 24px;
    gap: 1rem;
    padding: 0.85rem 1.25rem;
    background: rgba(30, 41, 59, 0.6);
    border-bottom: 1px solid rgba(148, 163, 184, 0.06);
  }

  .sh-layer, .sh-col {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
  }

  .stack-row {
    display: block;
    width: 100%;
    background: none;
    border: none;
    border-bottom: 1px solid rgba(148, 163, 184, 0.04);
    cursor: pointer;
    text-align: left;
    font-family: inherit;
    transition: all 0.2s ease;
    animation: rowFade 0.4s ease forwards;
    opacity: 0;
    padding: 0;
  }

  @keyframes rowFade {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .stack-row:hover, .stack-row-hovered {
    background: rgba(245, 158, 11, 0.02);
  }

  .stack-row-expanded {
    background: rgba(30, 41, 59, 0.3);
  }

  .stack-row-main {
    display: grid;
    grid-template-columns: 180px 1fr 1fr 1fr 24px;
    gap: 1rem;
    padding: 1rem 1.25rem;
    align-items: center;
  }

  .stack-layer {
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .layer-icon {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 7px;
    font-size: 0.7rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    border: 1px solid;
    flex-shrink: 0;
  }

  .layer-name {
    font-size: 0.85rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
  }

  .stack-old {
    font-size: 0.85rem;
    color: #64748b;
  }

  .stack-new {
    font-size: 0.85rem;
    color: #e2e8f0;
    font-weight: 500;
  }

  .stack-tool {
    font-size: 0.8rem;
    color: #fbbf24;
    font-family: 'JetBrains Mono', monospace;
  }

  .stack-chevron {
    color: #334155;
    transition: transform 0.2s ease;
    flex-shrink: 0;
  }

  .stack-chevron-open {
    transform: rotate(180deg);
    color: #f59e0b;
  }

  .stack-detail {
    display: flex;
    gap: 1rem;
    padding: 0 1.25rem 1.25rem 1.25rem;
    margin-left: 180px;
  }

  .detail-bar {
    width: 3px;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .detail-text {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.65;
    margin: 0;
  }

  @media (max-width: 768px) {
    .stack-header-row {
      display: none;
    }

    .stack-row-main {
      grid-template-columns: 1fr;
      gap: 0.4rem;
    }

    .stack-old, .stack-tool {
      display: none;
    }

    .sh-tool {
      display: none;
    }

    .stack-detail {
      margin-left: 0;
    }

    .stack-chevron {
      position: absolute;
      right: 1rem;
      top: 50%;
      transform: translateY(-50%);
    }

    .stack-chevron-open {
      transform: translateY(-50%) rotate(180deg);
    }

    .stack-row-main {
      position: relative;
      padding-right: 2.5rem;
    }
  }
</style>
