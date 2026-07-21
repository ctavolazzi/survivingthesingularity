<!--
  LocalGridSizer.svelte

  Explorable for Chapter 17 (Tools of the Trade). The chapter argues that
  routing solar power through an inverter costs "up to 30%" of captured
  energy to DC-to-AC-to-DC conversion loss, and that a DC-native microgrid
  eliminates that loss entirely. This widget lets the reader size their own
  panel array, sun-hours, and battery bank, then feel that 30% as a real
  number and a real list of loads that do or don't run.

  Self-contained: no props, no external data. First `awesome-explorables`
  style widget on the site. See registry.js for how new ones get added.
-->
<script>
  // Source: Chapter 17, "This is a thermodynamic disaster. You are losing
  // up to 30% of your captured solar energy simply converting it back and
  // forth through silicon components..." Kept as a named, sourced constant
  // rather than a magic number so the claim stays traceable to the text.
  const INVERTER_LOSS_FRACTION = 0.30;

  let panelWatts = 400;
  let sunHours = 4.5;
  let batteryKwh = 5;
  let mode = 'dc'; // 'dc' | 'inverter'

  // Illustrative daily loads, not a spec sheet. Watt-hours per day, ordered
  // by survival priority (comms and food storage before comfort/compute).
  const LOADS = [
    { id: 'comms', label: 'LoRa mesh + comms', wh: 40 },
    { id: 'fridge', label: '12V compressor fridge', wh: 600 },
    { id: 'pump', label: 'Well pump', wh: 250 },
    { id: 'lighting', label: 'LED lighting', wh: 120 },
    { id: 'compute', label: 'Local compute (mesh node, small server)', wh: 300 }
  ];

  $: dailyGenerationWh = panelWatts * sunHours;
  $: lossFraction = mode === 'inverter' ? INVERTER_LOSS_FRACTION : 0;
  $: usableWh = dailyGenerationWh * (1 - lossFraction);
  $: lostWh = dailyGenerationWh - usableWh;
  $: batteryWh = batteryKwh * 1000;
  $: usableCappedWh = Math.min(usableWh, batteryWh);

  // Greedily fill the load list against the usable budget, in priority
  // order. A load is OK if it fits fully, LIMITED if it's the load that
  // exhausts the remaining budget (fits partially), and unmet otherwise.
  $: loadStatus = (() => {
    let remaining = usableCappedWh;
    return LOADS.map((load) => {
      if (remaining <= 0) return { ...load, status: 'no' };
      if (load.wh <= remaining) {
        remaining -= load.wh;
        return { ...load, status: 'ok' };
      }
      remaining = 0;
      return { ...load, status: 'limited' };
    });
  })();

  $: genBarPct = 100;
  $: usableBarPct = dailyGenerationWh > 0 ? Math.round((usableWh / dailyGenerationWh) * 100) : 0;

  function fmtWh(wh) {
    return `${Math.round(wh).toLocaleString()} Wh`;
  }
</script>

<div class="grid-sizer">
  <div class="grid-sizer-header">
    <span class="eyebrow">Explorable &middot; Chapter 17</span>
    <h3>Build Your Own Grid</h3>
    <p class="dek">Size a microgrid. Watch what the inverter actually costs you.</p>
  </div>

  <div class="controls">
    <label class="control">
      <span class="control-label">
        Panel array
        <span class="control-value">{panelWatts} W</span>
      </span>
      <input
        type="range"
        min="100"
        max="3000"
        step="50"
        bind:value={panelWatts}
        aria-label="Panel array wattage"
      />
    </label>

    <label class="control">
      <span class="control-label">
        Peak sun hours / day
        <span class="control-value">{sunHours.toFixed(1)} h</span>
      </span>
      <input
        type="range"
        min="1"
        max="8"
        step="0.5"
        bind:value={sunHours}
        aria-label="Peak sun hours per day"
      />
    </label>

    <label class="control">
      <span class="control-label">
        Battery bank
        <span class="control-value">{batteryKwh} kWh</span>
      </span>
      <input
        type="range"
        min="1"
        max="20"
        step="1"
        bind:value={batteryKwh}
        aria-label="Battery bank capacity in kilowatt-hours"
      />
    </label>

    <div class="mode-toggle" role="radiogroup" aria-label="Delivery mode">
      <button
        type="button"
        role="radio"
        aria-checked={mode === 'dc'}
        class:active={mode === 'dc'}
        on:click={() => (mode = 'dc')}
      >
        DC-native
      </button>
      <button
        type="button"
        role="radio"
        aria-checked={mode === 'inverter'}
        class:active={mode === 'inverter'}
        on:click={() => (mode = 'inverter')}
      >
        Inverter (AC)
      </button>
    </div>
  </div>

  <div class="results" aria-live="polite">
    <div class="bars">
      <div class="bar-row">
        <span class="bar-label">Captured</span>
        <div class="bar-track">
          <div class="bar-fill bar-captured" style="width: {genBarPct}%"></div>
        </div>
        <span class="bar-value">{fmtWh(dailyGenerationWh)}</span>
      </div>
      <div class="bar-row">
        <span class="bar-label">Usable</span>
        <div class="bar-track">
          <div class="bar-fill bar-usable" class:is-inverter={mode === 'inverter'} style="width: {usableBarPct}%"></div>
        </div>
        <span class="bar-value">{fmtWh(usableWh)}</span>
      </div>
    </div>

    {#if mode === 'inverter'}
      <p class="loss-note">
        The inverter round trip costs you <strong>{fmtWh(lostWh)}</strong> today:
        {Math.round(lossFraction * 100)}% of everything the panels caught, gone to heat
        before it reaches a single device.
      </p>
    {:else}
      <p class="loss-note loss-note-good">
        Zero conversion loss. Every watt-hour the panels catch reaches the fuse block.
      </p>
    {/if}

    <div class="loads">
      <span class="loads-heading">Loads you can run today</span>
      <ul>
        {#each loadStatus as load}
          <li class="load-row load-{load.status}">
            <span class="load-label">{load.label}</span>
            <span class="load-wh">{load.wh} Wh/day</span>
            <span class="load-status">
              {#if load.status === 'ok'}OK{:else if load.status === 'limited'}LIMITED{:else}OFF{/if}
            </span>
          </li>
        {/each}
      </ul>
    </div>
  </div>
</div>

<style>
  .grid-sizer {
    background: var(--color-surface);
    border: var(--border-hard);
    box-shadow: var(--shadow-hard);
    padding: var(--space-lg);
    margin: var(--space-xl) 0;
    font-family: var(--font-primary);
    color: var(--color-text-primary);
  }

  /* Mobile-first: most readers hit this on a phone. Keep every element
     inside the card's own width no matter how the surrounding prose
     column behaves, and never let padding push content past the viewport. */
  .grid-sizer,
  .grid-sizer * {
    box-sizing: border-box;
  }

  @media (max-width: 480px) {
    .grid-sizer {
      padding: var(--space-md);
      margin: var(--space-lg) 0;
    }
  }

  .grid-sizer-header {
    margin-bottom: var(--space-lg);
  }

  .eyebrow {
    display: block;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--color-primary);
    margin-bottom: var(--space-xs);
  }

  .grid-sizer-header h3 {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 var(--space-xs) 0;
    color: var(--color-text-primary);
  }

  .dek {
    margin: 0;
    color: var(--color-text-secondary);
    font-size: 0.95rem;
  }

  .controls {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
    padding-bottom: var(--space-lg);
    border-bottom: var(--border-hard);
  }

  @media (min-width: 640px) {
    .controls {
      grid-template-columns: 1fr 1fr;
    }
  }

  .control {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
  }

  .control-label {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
  }

  .control-value {
    font-family: var(--font-mono);
    color: var(--color-primary-light);
    font-weight: 600;
  }

  input[type='range'] {
    /* Native range inputs have a tiny visual/tap target by default; pad the
       box so the touchable area on a phone is closer to the ~44px minimum
       even though the visible track stays thin. */
    width: 100%;
    padding: var(--space-sm) 0;
    accent-color: var(--color-primary);
    background: transparent;
  }

  .mode-toggle {
    display: flex;
    gap: 0;
    border: var(--border-hard);
    align-self: stretch;
    width: 100%;
  }

  @media (min-width: 640px) {
    .mode-toggle {
      align-self: start;
      width: auto;
    }
  }

  .mode-toggle button {
    flex: 1;
    min-height: 44px;
    font-family: var(--font-mono);
    font-size: 0.8rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    padding: var(--space-sm) var(--space-md);
    background: transparent;
    color: var(--color-text-secondary);
    border: none;
    cursor: pointer;
  }

  .mode-toggle button + button {
    border-left: var(--border-hard);
  }

  .mode-toggle button.active {
    background: var(--color-primary);
    color: var(--color-bg-primary);
    font-weight: 700;
  }

  .mode-toggle button:focus-visible,
  input[type='range']:focus-visible {
    outline: 2px solid var(--color-secondary-light);
    outline-offset: 2px;
  }

  .bars {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
  }

  .bar-row {
    display: grid;
    grid-template-columns: 5.5rem 1fr auto;
    align-items: center;
    gap: var(--space-sm);
  }

  @media (max-width: 420px) {
    /* Below ~420px, three columns crush the value column into wrapping.
       Stack label+value above the track instead. */
    .bar-row {
      grid-template-columns: 1fr auto;
      grid-template-areas: 'label value' 'track track';
      row-gap: var(--space-xs);
    }
    .bar-label {
      grid-area: label;
    }
    .bar-value {
      grid-area: value;
    }
    .bar-track {
      grid-area: track;
    }
  }

  .bar-label {
    font-size: 0.8rem;
    color: var(--color-text-secondary);
  }

  .bar-track {
    height: 0.85rem;
    background: var(--color-bg-tertiary);
    border: 1px solid rgba(241, 245, 249, 0.1);
    position: relative;
  }

  .bar-fill {
    height: 100%;
  }

  .bar-captured {
    background: var(--color-secondary);
  }

  .bar-usable {
    background: var(--color-success);
  }

  .bar-usable.is-inverter {
    background: var(--color-warning);
  }

  .bar-value {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--color-text-primary);
    white-space: nowrap;
    text-align: right;
  }

  .loss-note {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    margin: var(--space-md) 0;
    padding: var(--space-sm) var(--space-md);
    border-left: 3px solid var(--color-warning);
    background: rgba(245, 158, 11, 0.08);
  }

  .loss-note-good {
    border-left-color: var(--color-success);
    background: rgba(16, 185, 129, 0.08);
  }

  .loads {
    margin-top: var(--space-lg);
  }

  .loads-heading {
    display: block;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin-bottom: var(--space-sm);
  }

  .loads ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 1px;
    background: rgba(241, 245, 249, 0.08);
  }

  .load-row {
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: var(--space-md);
    align-items: center;
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-secondary);
    font-size: 0.85rem;
  }

  @media (max-width: 420px) {
    /* Three columns of text ("12V compressor fridge" + "600 Wh/day" +
       "LIMITED") don't fit a 320-375px phone without wrapping mid-word.
       Give the label its own row, keep wh/status on one line below it. */
    .load-row {
      grid-template-columns: 1fr auto;
      grid-template-areas: 'label label' 'wh status';
      row-gap: 0.2rem;
      gap: var(--space-sm);
    }
    .load-label {
      grid-area: label;
    }
    .load-wh {
      grid-area: wh;
    }
    .load-status {
      grid-area: status;
    }
  }

  .load-label {
    color: var(--color-text-primary);
  }

  .load-wh {
    font-family: var(--font-mono);
    color: var(--color-text-muted);
    white-space: nowrap;
  }

  .load-status {
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    min-width: 4.5rem;
    text-align: right;
  }

  .load-ok .load-status {
    color: var(--color-success);
  }

  .load-limited .load-status {
    color: var(--color-warning);
  }

  .load-no .load-status {
    color: var(--color-text-muted);
  }

  @media (prefers-reduced-motion: no-preference) {
    .bar-fill {
      transition: width 0.25s ease-out;
    }
  }
</style>
