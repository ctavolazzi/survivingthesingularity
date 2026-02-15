<script>
  import { onMount, onDestroy } from 'svelte';

  let mounted = false;

  // Simulated "live" data points — these animate/tick on mount
  let metrics = [
    { label: 'Dollar Purchasing Power', value: 0.798, display: '$0.80', unit: 'per 2020 dollar', trend: 'down', color: '#ef4444', sparkline: [1.0, 0.97, 0.93, 0.88, 0.85, 0.82, 0.80] },
    { label: 'Median Home Price', value: 500000, display: '$500K', unit: 'United States', trend: 'up', color: '#ef4444', sparkline: [290, 320, 350, 400, 430, 475, 500] },
    { label: 'Shouse Build Cost', value: 100000, display: '$100K', unit: 'all-in estimate', trend: 'stable', color: '#10b981', sparkline: [95, 97, 98, 100, 100, 100, 100] },
    { label: 'Monthly Overhead Savings', value: 1450, display: '$1,450', unit: 'vs traditional mortgage', trend: 'up', color: '#10b981', sparkline: [800, 950, 1050, 1200, 1300, 1400, 1450] },
    { label: 'YouTube Channels Created', value: 114000000, display: '114M+', unit: 'global creator economy', trend: 'up', color: '#3b82f6', sparkline: [51, 65, 78, 89, 95, 105, 114] },
    { label: 'Llama 4 VRAM Req.', value: 48, display: '48 GB', unit: 'consumer hardware', trend: 'down', color: '#10b981', sparkline: [128, 96, 80, 64, 56, 52, 48] },
  ];

  let tickInterval;

  onMount(() => {
    mounted = true;
    // Subtle tick animation — randomly update sparkline tails
    tickInterval = setInterval(() => {
      metrics = metrics.map(m => {
        const last = m.sparkline[m.sparkline.length - 1];
        const jitter = last * (0.98 + Math.random() * 0.04);
        return {
          ...m,
          sparkline: [...m.sparkline.slice(1), jitter]
        };
      });
    }, 2000);
  });

  onDestroy(() => {
    if (tickInterval) clearInterval(tickInterval);
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
    <div class="dash-dot-pulse"></div>
    <span class="dash-live">Live economic indicators</span>
  </div>
</div>

<style>
  .dashboard {
    margin-top: 2rem;
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
