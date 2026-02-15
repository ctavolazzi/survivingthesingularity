<script>
  import { fly } from 'svelte/transition';

  let monthlyPayment = 2000;
  let showResults = false;
  let animateNumbers = false;

  const SHOUSE_MONTHLY = 550; // ~$100K over 15 yrs at 6% or $66K cash = ~$550/mo opportunity cost
  const SHOUSE_BUILD_COST = 100000;

  function calculate() {
    showResults = true;
    animateNumbers = false;
    setTimeout(() => { animateNumbers = true; }, 50);
  }

  $: monthlySavings = monthlyPayment - SHOUSE_MONTHLY;
  $: yearlySavings = monthlySavings * 12;
  $: fiveYearSavings = yearlySavings * 5;
  $: tenYearSavings = yearlySavings * 10;
  $: thirtyYearSavings = yearlySavings * 30;
  $: thirtyYearTraditional = monthlyPayment * 12 * 30;
  $: thirtyYearShouse = SHOUSE_MONTHLY * 12 * 30 + SHOUSE_BUILD_COST;
  $: percentSaved = Math.round(((thirtyYearTraditional - thirtyYearShouse) / thirtyYearTraditional) * 100);
  $: yearsReclaimed = Math.round(thirtyYearSavings / (monthlyPayment * 12));

  function formatMoney(n) {
    if (n >= 1000000) return '$' + (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return '$' + Math.round(n / 1000) + 'K';
    return '$' + n.toLocaleString();
  }
</script>

<div class="calc-wrapper">
  <div class="calc-input-section">
    <label for="monthly" class="calc-question">What's your current monthly rent or mortgage?</label>
    <div class="input-row">
      <span class="input-prefix">$</span>
      <input
        id="monthly"
        type="range"
        min="500"
        max="5000"
        step="50"
        bind:value={monthlyPayment}
        class="calc-slider"
      />
      <span class="input-value">{monthlyPayment.toLocaleString()}<span class="input-per">/mo</span></span>
    </div>
    <div class="slider-labels">
      <span>$500</span>
      <span>$2,500</span>
      <span>$5,000</span>
    </div>
    <button class="calc-btn" on:click={calculate}>
      Calculate My Savings
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
  </div>

  {#if showResults}
    <div class="calc-results" in:fly={{ y: 20, duration: 400 }}>
      <div class="results-header">
        <h3 class="results-title">Your Exit Strategy Numbers</h3>
        <p class="results-subtitle">Based on ${monthlyPayment.toLocaleString()}/mo vs. the Shouse at ~${SHOUSE_MONTHLY}/mo</p>
      </div>

      <div class="results-grid">
        <div class="result-card result-highlight">
          <span class="result-label">30-Year Savings</span>
          <span class="result-value" class:animate={animateNumbers}>{formatMoney(thirtyYearSavings)}</span>
          <span class="result-detail">That's {percentSaved}% less spent on housing</span>
        </div>
        <div class="result-card">
          <span class="result-label">Monthly Freed Up</span>
          <span class="result-value" class:animate={animateNumbers}>{formatMoney(monthlySavings)}</span>
          <span class="result-detail">Redirected to building your engine</span>
        </div>
        <div class="result-card">
          <span class="result-label">5-Year Total Saved</span>
          <span class="result-value" class:animate={animateNumbers}>{formatMoney(fiveYearSavings)}</span>
          <span class="result-detail">Enough to fund a business</span>
        </div>
        <div class="result-card">
          <span class="result-label">Years Reclaimed</span>
          <span class="result-value" class:animate={animateNumbers}>~{yearsReclaimed}</span>
          <span class="result-detail">Of not working to pay a mortgage</span>
        </div>
      </div>

      <div class="comparison-bar">
        <div class="bar-row">
          <span class="bar-label">Traditional ({monthlyPayment.toLocaleString()}/mo x 30 yrs)</span>
          <div class="bar-track">
            <div class="bar-fill bar-old" style="width: 100%"></div>
          </div>
          <span class="bar-amount">{formatMoney(thirtyYearTraditional)}</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">Shouse Strategy</span>
          <div class="bar-track">
            <div class="bar-fill bar-new" style="width: {Math.round((thirtyYearShouse / thirtyYearTraditional) * 100)}%"></div>
          </div>
          <span class="bar-amount">{formatMoney(thirtyYearShouse)}</span>
        </div>
      </div>

      <p class="results-cta">
        That's <strong>{formatMoney(thirtyYearSavings)}</strong> you keep. Read the blueprint to see how.
      </p>
    </div>
  {/if}
</div>

<style>
  .calc-wrapper {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 20px;
    padding: 2.5rem;
    margin-top: 1rem;
  }

  .calc-question {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
    display: block;
    margin-bottom: 1.5rem;
  }

  .input-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
  }

  .input-prefix {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
  }

  .calc-slider {
    flex: 1;
    -webkit-appearance: none;
    appearance: none;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    outline: none;
    cursor: pointer;
  }

  .calc-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
    cursor: grab;
    transition: transform 0.15s;
  }

  .calc-slider::-webkit-slider-thumb:active {
    cursor: grabbing;
    transform: scale(1.15);
  }

  .calc-slider::-moz-range-thumb {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
    border: none;
    cursor: grab;
  }

  .input-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    min-width: 140px;
    text-align: right;
  }

  .input-per {
    font-size: 0.8rem;
    font-weight: 500;
    color: #64748b;
  }

  .slider-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: #475569;
    margin-bottom: 1.5rem;
    padding: 0 0.25rem;
  }

  .calc-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.85rem 2rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.95rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: inherit;
  }

  .calc-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(245, 158, 11, 0.4);
  }

  /* Results */
  .calc-results {
    margin-top: 2.5rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(148, 163, 184, 0.08);
  }

  .results-header {
    margin-bottom: 1.5rem;
  }

  .results-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.25rem 0;
  }

  .results-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
  }

  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .result-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 14px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .result-highlight {
    border-color: rgba(245, 158, 11, 0.2);
    background: rgba(245, 158, 11, 0.05);
  }

  .result-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
  }

  .result-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    transition: transform 0.3s ease;
  }

  .result-value.animate {
    animation: pop 0.4s ease;
  }

  @keyframes pop {
    0% { transform: scale(0.8); opacity: 0.5; }
    60% { transform: scale(1.05); }
    100% { transform: scale(1); opacity: 1; }
  }

  .result-detail {
    font-size: 0.78rem;
    color: #94a3b8;
    line-height: 1.3;
  }

  /* Comparison bars */
  .comparison-bar {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .bar-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .bar-label {
    font-size: 0.75rem;
    color: #94a3b8;
    min-width: 130px;
    white-space: nowrap;
  }

  .bar-track {
    flex: 1;
    height: 10px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 5px;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    border-radius: 5px;
    transition: width 0.8s ease;
  }

  .bar-old {
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.6), rgba(239, 68, 68, 0.3));
  }

  .bar-new {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.8), rgba(16, 185, 129, 0.4));
  }

  .bar-amount {
    font-size: 0.8rem;
    font-weight: 700;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    min-width: 60px;
    text-align: right;
  }

  .results-cta {
    font-size: 0.95rem;
    color: #94a3b8;
    text-align: center;
    margin: 0;
  }

  .results-cta strong {
    color: #10b981;
    font-weight: 700;
  }

  @media (max-width: 640px) {
    .calc-wrapper {
      padding: 1.5rem;
    }

    .input-value {
      font-size: 1.3rem;
      min-width: 100px;
    }

    .bar-label {
      min-width: 80px;
      font-size: 0.65rem;
    }

    .results-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
