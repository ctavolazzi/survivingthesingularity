<script>
  import { onMount } from 'svelte';

  // Preset option sets - clickable chips, no sliders
  const incomeOptions = [
    { label: '$2K/mo', value: 2000 },
    { label: '$3.5K/mo', value: 3500 },
    { label: '$5K/mo', value: 5000 },
    { label: '$8K/mo', value: 8000 },
    { label: '$12K/mo', value: 12000 },
  ];

  const savingsRateOptions = [
    { label: '5%', pct: 0.05 },
    { label: '10%', pct: 0.10 },
    { label: '20%', pct: 0.20 },
    { label: '30%', pct: 0.30 },
    { label: '40%', pct: 0.40 },
  ];

  const currentSavingsOptions = [
    { label: '$0', value: 0 },
    { label: '$5K', value: 5000 },
    { label: '$15K', value: 15000 },
    { label: '$30K', value: 30000 },
    { label: '$60K', value: 60000 },
  ];

  let selectedIncome = 1;      // index into incomeOptions
  let selectedSavingsRate = 2; // index into savingsRateOptions
  let selectedCurrentSavings = 1; // index into currentSavingsOptions

  let animated = false;
  onMount(() => { setTimeout(() => { animated = true; }, 200); });

  $: monthlyIncome = incomeOptions[selectedIncome].value;
  $: savingsRate = savingsRateOptions[selectedSavingsRate].pct;
  $: currentSavings = currentSavingsOptions[selectedCurrentSavings].value;
  $: monthlySavings = Math.round(monthlyIncome * savingsRate);

  // Illustrative target - clearly labelled
  const targetAmount = 100000;

  $: monthsToTarget = monthlySavings > 0
    ? Math.ceil((targetAmount - currentSavings) / monthlySavings)
    : Infinity;
  $: yearsToTarget = monthsToTarget / 12;

  // Progress ring
  $: progressPercent = Math.min(100, Math.round((currentSavings / targetAmount) * 100));
  $: circumference = 2 * Math.PI * 54;
  $: dashoffset = circumference - (progressPercent / 100) * circumference;

  // Milestones
  const milestones = [
    { label: 'Land deposit', amount: 10000, icon: '01' },
    { label: 'Building kit', amount: 40000, icon: '02' },
    { label: 'Utilities in', amount: 70000, icon: '03' },
    { label: 'Full target', amount: 100000, icon: '04' },
  ];

  $: milestonesWithState = milestones.map(m => ({
    ...m,
    reached: currentSavings >= m.amount,
    pct: Math.round((m.amount / targetAmount) * 100),
  }));

  function formatMoney(n) {
    if (n >= 1000) return '$' + (n / 1000).toFixed(n % 1000 === 0 ? 0 : 1) + 'K';
    return '$' + n;
  }

  function formatYears(y) {
    if (!isFinite(y)) return 'n/a';
    if (y < 1) return Math.round(y * 12) + ' mos';
    return y.toFixed(1) + ' yrs';
  }
</script>

<div class="cd" class:animated>

  <div class="cd-warning">
    <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><circle cx="6.5" cy="6.5" r="5.5" stroke="#fbbf24" stroke-width="1.1"/><path d="M6.5 3.5v3M6.5 8.5v.5" stroke="#fbbf24" stroke-width="1.4" stroke-linecap="round"/></svg>
    <span>Toy model only. Not a forecast. Not financial advice. Illustrative arithmetic; ignores inflation, taxes, market conditions, life circumstances. Consult professionals before acting on anything.</span>
  </div>

  <!-- Top: ring + quick read -->
  <div class="cd-top">
    <div class="ring-wrap">
      <svg viewBox="0 0 120 120" class="ring-svg">
        <defs>
          <linearGradient id="cd-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#f59e0b"/>
            <stop offset="100%" style="stop-color:#10b981"/>
          </linearGradient>
        </defs>
        <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="7"/>
        <circle cx="60" cy="60" r="54" fill="none" stroke="url(#cd-grad)" stroke-width="7"
          stroke-linecap="round"
          stroke-dasharray={circumference}
          stroke-dashoffset={animated ? dashoffset : circumference}
          transform="rotate(-90 60 60)"
          style="transition: stroke-dashoffset 1.2s ease"
        />
      </svg>
      <div class="ring-center">
        <span class="ring-pct">{progressPercent}%</span>
        <span class="ring-label">of target</span>
      </div>
    </div>

    <div class="cd-readout">
      <div class="readout-row">
        <span class="readout-label">Saving / mo (approx.)</span>
        <span class="readout-val">{formatMoney(monthlySavings)}</span>
      </div>
      <div class="readout-row">
        <span class="readout-label">Illustrative time to $100K target</span>
        <span class="readout-val readout-highlight">{formatYears(yearsToTarget)}</span>
      </div>
      <p class="readout-note">$100K is one rough illustrative target. Your real number could be higher or lower by a large margin depending on land, location, scope, and many other factors.</p>
    </div>
  </div>

  <!-- Inputs: chips -->
  <div class="cd-inputs">
    <div class="chip-group">
      <span class="chip-label">Monthly income</span>
      <div class="chips">
        {#each incomeOptions as opt, i}
          <button
            class="chip"
            class:chip-active={selectedIncome === i}
            on:click={() => selectedIncome = i}
          >{opt.label}</button>
        {/each}
      </div>
    </div>

    <div class="chip-group">
      <span class="chip-label">Savings rate</span>
      <div class="chips">
        {#each savingsRateOptions as opt, i}
          <button
            class="chip"
            class:chip-active={selectedSavingsRate === i}
            on:click={() => selectedSavingsRate = i}
          >{opt.label}</button>
        {/each}
      </div>
    </div>

    <div class="chip-group">
      <span class="chip-label">Already saved</span>
      <div class="chips">
        {#each currentSavingsOptions as opt, i}
          <button
            class="chip"
            class:chip-active={selectedCurrentSavings === i}
            on:click={() => selectedCurrentSavings = i}
          >{opt.label}</button>
        {/each}
      </div>
    </div>
  </div>

  <!-- Milestone track -->
  <div class="milestones">
    <div class="ms-track">
      <div class="ms-fill" style="width: {progressPercent}%"></div>
      {#each milestonesWithState as m}
        <div class="ms-dot" class:ms-reached={m.reached} style="left: {m.pct}%">
          <span class="ms-icon">{m.icon}</span>
        </div>
      {/each}
    </div>
    <div class="ms-labels">
      {#each milestonesWithState as m}
        <div class="ms-label" class:ms-label-reached={m.reached} style="left: {m.pct}%">
          <span class="ms-name">{m.label}</span>
          <span class="ms-amt">{formatMoney(m.amount)}</span>
        </div>
      {/each}
    </div>
  </div>

  <!-- Deep dive CTA -->
  <div class="cd-deepdive">
    <div class="deepdive-text">
      <p class="deepdive-title">Want the full breakdown?</p>
      <p class="deepdive-sub">Anticipated tech products, real cost ranges, emerging robotics (Unitree, Figure AI, FarmBot, Asimov), and a more comprehensive scenario tool.</p>
    </div>
    <a href="/agi#scenario" class="deepdive-btn">
      Explore the deep dive
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7H11.5M11.5 7L8 3.5M11.5 7L8 10.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>

</div>

<style>
  .cd {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.07);
    border-radius: 20px;
    padding: 1.75rem;
    margin-top: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.75rem;
  }

  /* Warning */
  .cd-warning {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.7rem 0.9rem;
    background: rgba(120, 53, 15, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 8px;
  }
  .cd-warning svg { flex-shrink: 0; margin-top: 0.1rem; }
  .cd-warning span {
    font-size: 0.8rem;
    color: #fcd34d;
    line-height: 1.55;
    font-family: var(--font-primary);
    font-weight: 500;
    letter-spacing: 0.02em;
  }

  /* Top: ring + readout */
  .cd-top {
    display: flex;
    align-items: center;
    gap: 2rem;
  }

  .ring-wrap {
    position: relative;
    width: 110px;
    height: 110px;
    flex-shrink: 0;
  }

  .ring-svg { width: 100%; height: 100%; }

  .ring-center {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.1rem;
  }

  .ring-pct {
    font-size: 1.3rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: var(--font-primary);
    line-height: 1;
  }

  .ring-label {
    font-size: 0.82rem;
    color: #dde4ef;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .cd-readout {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .readout-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.06);
  }

  .readout-label {
    font-size: 0.82rem;
    color: #dde4ef;
    font-weight: 500;
  }

  .readout-val {
    font-size: 0.9rem;
    font-weight: 700;
    color: #e2e8f0;
    font-family: var(--font-primary);
    white-space: nowrap;
  }

  .readout-highlight { color: #f59e0b; font-size: 1.1rem; }

  .readout-note {
    font-size: 0.86rem;
    color: #dde4ef;
    line-height: 1.5;
    margin: 0;
    font-style: italic;
  }

  /* Chip inputs */
  .cd-inputs {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .chip-group {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
  }

  .chip-label {
    font-size: 0.86rem;
    font-weight: 700;
    color: #dde4ef;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: var(--font-primary);
  }

  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .chip {
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: var(--font-primary);
    border: 1px solid rgba(148, 163, 184, 0.1);
    background: rgba(30, 41, 59, 0.5);
    color: #dde4ef;
    cursor: pointer;
    transition: all 0.15s ease;
    line-height: 1;
  }

  .chip:hover {
    border-color: rgba(245, 158, 11, 0.3);
    color: #dde4ef;
  }

  .chip-active {
    background: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.4);
    color: #f59e0b;
  }

  /* Milestones */
  .milestones {
    padding: 0 0.25rem;
  }

  .ms-track {
    position: relative;
    height: 4px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 2px;
    margin-bottom: 1.75rem;
  }

  .ms-fill {
    position: absolute;
    left: 0; top: 0;
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #10b981);
    border-radius: 2px;
    transition: width 0.8s ease;
  }

  .ms-dot {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #0f172a;
    border: 2px solid rgba(148, 163, 184, 0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: border-color 0.3s, background 0.3s;
  }

  .ms-reached {
    background: rgba(16, 185, 129, 0.12);
    border-color: #10b981;
  }

  .ms-icon {
    font-size: 0.82rem;
    font-weight: 800;
    color: #dde4ef;
    font-family: var(--font-primary);
  }

  .ms-reached .ms-icon { color: #10b981; }

  .ms-labels {
    position: relative;
    height: 2.25rem;
  }

  .ms-label {
    position: absolute;
    transform: translateX(-50%);
    text-align: center;
    white-space: nowrap;
  }

  .ms-name {
    display: block;
    font-size: 0.82rem;
    color: #dde4ef;
    font-weight: 600;
  }

  .ms-amt {
    display: block;
    font-size: 0.82rem;
    color: #1e293b;
    font-family: var(--font-primary);
  }

  .ms-label-reached .ms-name { color: #10b981; }
  .ms-label-reached .ms-amt { color: #059669; }

  /* Deep dive */
  .cd-deepdive {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    padding: 1rem 1.25rem;
    background: rgba(245, 158, 11, 0.04);
    border: 1px solid rgba(245, 158, 11, 0.1);
    border-radius: 10px;
  }

  .deepdive-text {
    flex: 1;
    min-width: 0;
  }

  .deepdive-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #d4d4d8;
    margin: 0 0 0.2rem 0;
  }

  .deepdive-sub {
    font-size: 0.85rem;
    color: #dde4ef;
    line-height: 1.5;
    margin: 0;
  }

  .deepdive-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 1.1rem;
    border-radius: 7px;
    font-size: 0.8rem;
    font-weight: 700;
    text-decoration: none;
    background: rgba(245, 158, 11, 0.08);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.25);
    white-space: nowrap;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .deepdive-btn:hover {
    background: rgba(245, 158, 11, 0.14);
    border-color: rgba(245, 158, 11, 0.45);
  }

  @media (max-width: 640px) {
    .cd { padding: 1.25rem; gap: 1.25rem; }
    .cd-top { flex-direction: column; align-items: flex-start; gap: 1rem; }
    .cd-deepdive { flex-direction: column; align-items: flex-start; }
    .deepdive-btn { width: 100%; justify-content: center; }
    .ms-labels { display: none; }
  }
</style>
