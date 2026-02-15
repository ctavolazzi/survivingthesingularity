<script>
  import { onMount } from 'svelte';

  let monthlyIncome = 4000;
  let monthlySavings = 500;
  let currentSavings = 5000;
  let targetAmount = 100000; // Shouse + land target

  let animated = false;

  onMount(() => {
    setTimeout(() => { animated = true; }, 200);
  });

  $: monthlyRate = monthlySavings;
  $: monthsToTarget = monthlyRate > 0 ? Math.ceil((targetAmount - currentSavings) / monthlyRate) : Infinity;
  $: yearsToTarget = monthsToTarget / 12;
  $: targetDate = new Date(Date.now() + monthsToTarget * 30.44 * 24 * 60 * 60 * 1000);

  // Shouse-optimized: If you cut housing to $550/mo (shouse equivalent), how much faster?
  $: currentHousingEstimate = Math.round(monthlyIncome * 0.33);
  $: shouseHousing = 550;
  $: extraSavings = Math.max(0, currentHousingEstimate - shouseHousing);
  $: optimizedMonthly = monthlySavings + extraSavings;
  $: optimizedMonths = optimizedMonthly > 0 ? Math.ceil((targetAmount - currentSavings) / optimizedMonthly) : Infinity;
  $: monthsSaved = monthsToTarget - optimizedMonths;
  $: yearsSaved = (monthsSaved / 12).toFixed(1);

  // Progress ring
  $: progressPercent = Math.min(100, Math.round((currentSavings / targetAmount) * 100));
  $: circumference = 2 * Math.PI * 54;
  $: dashoffset = circumference - (progressPercent / 100) * circumference;

  // Milestones
  $: milestones = [
    { label: 'Land down payment', amount: 15000, icon: 'M' },
    { label: 'Steel building kit', amount: 45000, icon: 'S' },
    { label: 'Shouse + utilities', amount: 75000, icon: 'U' },
    { label: 'Full independence', amount: 100000, icon: 'F' },
  ].map(m => ({
    ...m,
    reached: currentSavings >= m.amount,
    pct: Math.round((m.amount / targetAmount) * 100)
  }));

  function formatDate(d) {
    return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  }

  function formatMoney(n) {
    return '$' + n.toLocaleString();
  }
</script>

<div class="countdown" class:animated>
  <div class="countdown-top">
    <!-- Progress ring -->
    <div class="ring-wrap">
      <svg viewBox="0 0 120 120" class="ring-svg">
        <defs>
          <linearGradient id="ring-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#f59e0b"/>
            <stop offset="100%" style="stop-color:#10b981"/>
          </linearGradient>
        </defs>
        <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="6"/>
        <circle cx="60" cy="60" r="54" fill="none" stroke="url(#ring-grad)" stroke-width="6"
          stroke-linecap="round"
          stroke-dasharray={circumference}
          stroke-dashoffset={animated ? dashoffset : circumference}
          transform="rotate(-90 60 60)"
          style="transition: stroke-dashoffset 1.5s ease"
        />
      </svg>
      <div class="ring-center">
        <span class="ring-pct">{progressPercent}%</span>
        <span class="ring-label">saved</span>
      </div>
    </div>

    <!-- Target info -->
    <div class="target-info">
      <div class="target-date-label">Estimated independence date</div>
      <div class="target-date">
        {#if monthsToTarget === Infinity}
          <span class="target-never">Increase savings to calculate</span>
        {:else}
          {formatDate(targetDate)}
        {/if}
      </div>
      {#if monthsSaved > 0}
        <div class="shouse-boost">
          With shouse strategy: <strong>{yearsSaved} years sooner</strong>
        </div>
      {/if}
    </div>
  </div>

  <!-- Inputs -->
  <div class="countdown-inputs">
    <div class="input-group">
      <label class="input-label">Monthly income</label>
      <div class="input-wrap">
        <span class="input-prefix">$</span>
        <input type="range" min="1000" max="15000" step="250" bind:value={monthlyIncome} class="range-input" />
        <span class="input-value">{formatMoney(monthlyIncome)}</span>
      </div>
    </div>
    <div class="input-group">
      <label class="input-label">Monthly savings ability</label>
      <div class="input-wrap">
        <span class="input-prefix">$</span>
        <input type="range" min="0" max="5000" step="50" bind:value={monthlySavings} class="range-input" />
        <span class="input-value">{formatMoney(monthlySavings)}</span>
      </div>
    </div>
    <div class="input-group">
      <label class="input-label">Current savings</label>
      <div class="input-wrap">
        <span class="input-prefix">$</span>
        <input type="range" min="0" max="80000" step="1000" bind:value={currentSavings} class="range-input" />
        <span class="input-value">{formatMoney(currentSavings)}</span>
      </div>
    </div>
  </div>

  <!-- Milestones -->
  <div class="milestones">
    <div class="milestone-track">
      <div class="milestone-fill" style="width: {progressPercent}%"></div>
      {#each milestones as m}
        <div class="milestone-dot" class:milestone-reached={m.reached} style="left: {m.pct}%">
          <span class="milestone-icon">{m.icon}</span>
        </div>
      {/each}
    </div>
    <div class="milestone-labels">
      {#each milestones as m}
        <div class="milestone-label" class:milestone-label-reached={m.reached} style="left: {m.pct}%">
          <span class="milestone-name">{m.label}</span>
          <span class="milestone-amount">{formatMoney(m.amount)}</span>
        </div>
      {/each}
    </div>
  </div>

  <!-- Comparison -->
  <div class="comparison">
    <div class="compare-row">
      <span class="compare-label">Current path</span>
      <div class="compare-bar-bg">
        <div class="compare-bar compare-bar-old" style="width: {Math.min(100, (monthsToTarget / 360) * 100)}%"></div>
      </div>
      <span class="compare-time">{monthsToTarget === Infinity ? '--' : (yearsToTarget).toFixed(1) + ' yrs'}</span>
    </div>
    <div class="compare-row">
      <span class="compare-label">With shouse</span>
      <div class="compare-bar-bg">
        <div class="compare-bar compare-bar-new" style="width: {Math.min(100, (optimizedMonths / 360) * 100)}%"></div>
      </div>
      <span class="compare-time">{optimizedMonths === Infinity ? '--' : (optimizedMonths / 12).toFixed(1) + ' yrs'}</span>
    </div>
  </div>
</div>

<style>
  .countdown {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
  }

  .countdown-top {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .ring-wrap {
    position: relative;
    width: 120px;
    height: 120px;
    flex-shrink: 0;
  }

  .ring-svg {
    width: 100%;
    height: 100%;
  }

  .ring-center {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .ring-pct {
    font-size: 1.4rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
  }

  .ring-label {
    font-size: 0.65rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  .target-info {
    flex: 1;
  }

  .target-date-label {
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-bottom: 0.35rem;
  }

  .target-date {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f1f5f9;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
  }

  .target-never {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
  }

  .shouse-boost {
    margin-top: 0.5rem;
    font-size: 0.82rem;
    color: #10b981;
  }

  .shouse-boost strong {
    color: #34d399;
    font-weight: 700;
  }

  /* Inputs */
  .countdown-inputs {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .input-label {
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .input-wrap {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .input-prefix {
    font-size: 0.8rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
    width: 14px;
  }

  .range-input {
    flex: 1;
    -webkit-appearance: none;
    appearance: none;
    height: 4px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 2px;
    outline: none;
  }

  .range-input::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #f59e0b;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
    transition: transform 0.15s;
  }

  .range-input::-webkit-slider-thumb:hover {
    transform: scale(1.2);
  }

  .input-value {
    font-size: 0.85rem;
    font-weight: 700;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    min-width: 70px;
    text-align: right;
  }

  /* Milestones */
  .milestones {
    margin-bottom: 2rem;
    padding: 0 0.5rem;
  }

  .milestone-track {
    position: relative;
    height: 4px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 2px;
    margin-bottom: 2rem;
  }

  .milestone-fill {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #10b981);
    border-radius: 2px;
    transition: width 1s ease;
  }

  .milestone-dot {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #1e293b;
    border: 2px solid rgba(148, 163, 184, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
  }

  .milestone-reached {
    background: rgba(16, 185, 129, 0.15);
    border-color: #10b981;
  }

  .milestone-icon {
    font-size: 0.55rem;
    font-weight: 800;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
  }

  .milestone-reached .milestone-icon {
    color: #10b981;
  }

  .milestone-labels {
    position: relative;
    height: 2.5rem;
  }

  .milestone-label {
    position: absolute;
    transform: translateX(-50%);
    text-align: center;
    white-space: nowrap;
  }

  .milestone-name {
    display: block;
    font-size: 0.6rem;
    color: #475569;
    font-weight: 600;
  }

  .milestone-amount {
    display: block;
    font-size: 0.6rem;
    color: #334155;
    font-family: 'JetBrains Mono', monospace;
  }

  .milestone-label-reached .milestone-name {
    color: #10b981;
  }

  /* Comparison */
  .comparison {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .compare-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .compare-label {
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 600;
    min-width: 85px;
    white-space: nowrap;
  }

  .compare-bar-bg {
    flex: 1;
    height: 8px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 4px;
    overflow: hidden;
  }

  .compare-bar {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
  }

  .compare-bar-old {
    background: linear-gradient(90deg, #ef4444, #dc2626);
  }

  .compare-bar-new {
    background: linear-gradient(90deg, #10b981, #059669);
  }

  .compare-time {
    font-size: 0.78rem;
    font-weight: 700;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    min-width: 55px;
    text-align: right;
  }

  @media (max-width: 640px) {
    .countdown-top {
      flex-direction: column;
      text-align: center;
    }

    .milestone-labels {
      display: none;
    }

    .countdown {
      padding: 1.5rem;
    }
  }
</style>
