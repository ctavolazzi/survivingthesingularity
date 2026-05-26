<script>
  import { onMount } from 'svelte';

  let mounted = false;

  // Static reference figures. Not market data, not a forecast. Sparklines
  // illustrate the shape of the indicator across a stylized 2020-2026 window.
  let metrics = [
    { label: 'Dollar Purchasing Power', display: '~$0.80', unit: 'per 2020 dollar (illustrative)', trend: 'down', color: '#ef4444', sparkline: [1.0, 0.97, 0.93, 0.88, 0.85, 0.82, 0.80] },
    { label: 'Median Home Price', display: '~$500K', unit: 'United States (illustrative)', trend: 'up', color: '#ef4444', sparkline: [290, 320, 350, 400, 430, 475, 500] },
    { label: 'Shouse Build Cost', display: 'varies', unit: 'highly region-dependent', trend: 'stable', color: '#10b981', sparkline: [95, 97, 98, 100, 100, 100, 100] },
    { label: 'Monthly Overhead Delta', display: 'varies', unit: 'depends on your situation', trend: 'up', color: '#10b981', sparkline: [800, 950, 1050, 1200, 1300, 1400, 1450] },
    { label: 'Creator Channels', display: '100M+', unit: 'global, order of magnitude', trend: 'up', color: '#3b82f6', sparkline: [51, 65, 78, 89, 95, 105, 114] },
    { label: 'Local LLM VRAM Req.', display: 'tens of GB', unit: 'consumer hardware', trend: 'down', color: '#10b981', sparkline: [128, 96, 80, 64, 56, 52, 48] },
  ];

  onMount(() => {
    mounted = true;
  });

  function sparklinePath(data, width = 80, height = 24) {
    if (!data || data.length < 2) return '';
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;
    const stepX = width / (data.length - 1);
    return data.map((val, i) => {
      const x = i * stepX;
      const y = height - ((val - min) / range) * height;
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
  }
</script>

<div class="dashboard" class:mounted>
  <p class="dash-info-only">
    This site is for informational and educational purposes only. Not professional advice. Consult all relevant professionals before making any decisions. Offered AS-IS.
  </p>

  <div class="dash-grid">
    {#each metrics as metric, i}
      <div class="dash-card" style="animation-delay: {i * 80}ms">
        <div class="dash-card-top">
          <span class="dash-label">{metric.label}</span>
          <span class="dash-trend dash-trend-{metric.trend}">
            {#if metric.trend === 'up'}
              <svg width="10" height="10" viewBox="0 0 10 10"><path d="M1 8L5 2L9 8" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
            {:else if metric.trend === 'down'}
              <svg width="10" height="10" viewBox="0 0 10 10"><path d="M1 2L5 8L9 2" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
            {:else}
              <svg width="10" height="10" viewBox="0 0 10 10"><line x1="1" y1="5" x2="9" y2="5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            {/if}
          </span>
        </div>
        <div class="dash-value" style="color: {metric.color}">{metric.display}</div>
        <div class="dash-bottom">
          <span class="dash-unit">{metric.unit}</span>
          <svg class="dash-sparkline" viewBox="0 0 80 24" preserveAspectRatio="none">
            <path d={sparklinePath(metric.sparkline)} fill="none" stroke={metric.color} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
          </svg>
        </div>
      </div>
    {/each}
  </div>

  <div class="dash-footer">
    <span class="dash-live">Reference indicators only — verify all figures yourself.</span>
  </div>

  <p class="dash-disclaimer">
    Illustrative reference figures, not market data. Cost and savings figures vary widely by region, regulation, and individual circumstance. Numbers shown should not inform any decision. Not financial or economic advice. <a href="/disclaimer">Full disclaimer</a>.
  </p>
</div>

<style>
  .dashboard {
    margin-top: 2rem;
  }

  .dash-info-only {
    margin: 0 0 1.25rem 0;
    padding: 0.75rem 1rem;
    background: rgba(127, 29, 29, 0.18);
    border: 1px solid rgba(248, 113, 113, 0.3);
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #fecaca;
    line-height: 1.5;
    letter-spacing: 0.03em;
    font-weight: 600;
    text-align: center;
  }

  .dash-disclaimer {
    margin-top: 1rem;
    font-size: 0.7rem;
    color: #475569;
    line-height: 1.55;
    font-style: italic;
    max-width: 720px;
  }

  .dash-disclaimer a {
    color: #64748b;
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  .dash-disclaimer a:hover {
    color: #f59e0b;
  }

  .dash-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }

  .dash-card {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 14px;
    padding: 1.25rem;
    animation: dashFadeIn 0.5s ease forwards;
    opacity: 0;
    transition: all 0.2s ease;
  }

  .dash-card:hover {
    border-color: rgba(148, 163, 184, 0.12);
    background: rgba(30, 41, 59, 0.45);
    transform: translateY(-2px);
  }

  @keyframes dashFadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .dash-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .dash-label {
    font-size: 0.7rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .dash-trend {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 6px;
  }

  .dash-trend-up { color: #ef4444; background: rgba(239, 68, 68, 0.1); }
  .dash-trend-down { color: #10b981; background: rgba(16, 185, 129, 0.1); }
  .dash-trend-stable { color: #64748b; background: rgba(100, 116, 139, 0.1); }

  /* Override: for metrics where down is bad (purchasing power) */
  .dash-card:first-child .dash-trend-down { color: #ef4444; background: rgba(239, 68, 68, 0.1); }

  .dash-value {
    font-size: 1.5rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
  }

  .dash-bottom {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }

  .dash-unit {
    font-size: 0.62rem;
    color: #475569;
    font-weight: 500;
  }

  .dash-sparkline {
    width: 60px;
    height: 20px;
  }

  .dash-footer {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1rem;
    justify-content: center;
  }

  .dash-dot-pulse {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10b981;
    animation: pulse-dot 2s ease-in-out infinite;
  }

  @keyframes pulse-dot {
    0%, 100% { opacity: 0.4; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.3); }
  }

  .dash-live {
    font-size: 0.65rem;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
  }

  @media (max-width: 768px) {
    .dash-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 480px) {
    .dash-grid {
      grid-template-columns: 1fr;
    }

    .dash-card {
      padding: 1rem;
    }
  }
</style>
