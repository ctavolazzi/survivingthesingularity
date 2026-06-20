<script>
  import { shouseGame } from '$lib/stores/shouseGame.js';
  import { STAGES } from '$lib/game/shouse/engine/stages.js';
  import { CROP_PRESETS } from '$lib/game/shouse/data/plants.js';

  export let game;

  $: s = $shouseGame;
  $: nextStage = s ? STAGES[s.stage] : null;
  $: buildCheck = s && nextStage && !s.building ? game.canBuild() : null;
  $: cost = s && nextStage ? game.nextStageCost() : 0;
  $: buildingStage = s && s.building ? STAGES[s.building.index] : null;

  let collapsed = false;
</script>

{#if s && !s.won && !s.lost}
  <!-- Upgrade picker modal: pauses the sim until a choice is made -->
  {#if s.pendingUpgrade}
    <div class="modal-backdrop">
      <div class="modal" role="dialog" aria-label="Choose an upgrade">
        <h3 class="modal-title">{s.pendingUpgrade.label}: pick one</h3>
        <div class="upgrade-options">
          {#each s.pendingUpgrade.options as opt (opt.id)}
            <button class="upgrade-card" on:click={() => game.selectUpgrade(opt.id)}>
              <span class="upgrade-name" style="color: {opt.color}">{opt.name}</span>
              <span class="upgrade-desc">{opt.desc}</span>
            </button>
          {/each}
        </div>
      </div>
    </div>
  {/if}

  <div class="build-panel" class:collapsed>
    <button class="panel-toggle" on:click={() => (collapsed = !collapsed)}>
      {collapsed ? '▴ Build' : '▾'}
    </button>

    {#if !collapsed}
      {#if buildingStage}
        <div class="panel-head">
          <span class="stage-num">Stage {s.building.index + 1}/6</span>
          <h3 class="stage-name">{buildingStage.name}</h3>
        </div>
        <div class="construction">
          <span class="construction-label">Under construction</span>
          <div class="progress-track">
            <div
              class="progress-fill"
              style="width: {((s.building.totalDays - s.building.daysLeft) / s.building.totalDays) * 100}%"
            ></div>
          </div>
          <span class="construction-days">{s.building.daysLeft}d left</span>
        </div>
      {:else if nextStage}
        <div class="panel-head">
          <span class="stage-num">Stage {s.stage + 1}/6</span>
          <h3 class="stage-name">{nextStage.name}</h3>
        </div>
        <p class="stage-desc">{nextStage.desc}</p>

        <div class="stage-stats">
          <span class="stat">
            <span class="stat-label">Cost</span>
            <span class="stat-value" class:discounted={s.discountNext > 0}>
              ${cost.toLocaleString()}
              {#if s.discountNext > 0}<span class="discount-tag">-15%</span>{/if}
            </span>
          </span>
          <span class="stat">
            <span class="stat-label">Build</span>
            <span class="stat-value">{nextStage.buildDays}d</span>
          </span>
          {#if nextStage.waterDrain || nextStage.powerDrain}
            <span class="stat">
              <span class="stat-label">Drain</span>
              <span class="stat-value drain">
                {nextStage.waterDrain ? `${nextStage.waterDrain}w` : ''}
                {nextStage.powerDrain ? `${nextStage.powerDrain}p` : ''}/d
              </span>
            </span>
          {/if}
          {#if nextStage.incomePerDay}
            <span class="stat">
              <span class="stat-label">{nextStage.incomeLabel}</span>
              <span class="stat-value income">+${nextStage.incomePerDay}/d</span>
            </span>
          {/if}
          {#if nextStage.powerRegen}
            <span class="stat">
              <span class="stat-label">Solar</span>
              <span class="stat-value income">+{nextStage.powerRegen} pwr/d</span>
            </span>
          {/if}
        </div>

        {#if nextStage.id === 'solar_farmbot'}
          <div class="crop-select">
            <span class="stat-label">FarmBot bed</span>
            <div class="crop-options">
              {#each CROP_PRESETS as crop (crop.id)}
                <button
                  class="crop-chip"
                  class:active={s.cropPreset === crop.id}
                  on:click={() => game.setCrop(crop.id)}
                  title={crop.desc}
                >
                  {crop.name}
                </button>
              {/each}
            </div>
          </div>
        {/if}

        <button
          class="build-btn"
          disabled={!buildCheck?.ok}
          on:click={() => game.buildNextStage()}
        >
          {buildCheck?.ok ? `Build: $${cost.toLocaleString()}` : buildCheck?.reason || '...'}
        </button>

        <a class="blueprint-link" href="/blueprint/{nextStage.blueprintSlug}" target="_blank" rel="noopener">
          Read: {nextStage.blueprintTitle} →
        </a>
      {:else}
        <div class="panel-head">
          <h3 class="stage-name">Shouse complete</h3>
        </div>
        <p class="stage-desc">All systems running. Survive the shakedown.</p>
      {/if}
    {/if}
  </div>
{/if}

<style>
  .build-panel {
    position: absolute;
    left: 0.9rem;
    top: 4.2rem;
    width: 260px;
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    padding: 0.9rem;
    backdrop-filter: blur(6px);
    z-index: 6;
  }
  .build-panel.collapsed {
    width: auto;
    padding: 0.3rem;
  }
  .panel-toggle {
    position: absolute;
    top: 0.4rem;
    right: 0.4rem;
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 0.8rem;
    padding: 0.2rem 0.4rem;
  }
  .collapsed .panel-toggle {
    position: static;
    color: #fbbf24;
    font-family: var(--font-mono);
    font-weight: 700;
  }
  .panel-head {
    margin-bottom: 0.4rem;
  }
  .stage-num {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: #f59e0b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }
  .stage-name {
    margin: 0.1rem 0 0;
    font-size: 1rem;
    color: #f1f5f9;
    font-weight: 700;
  }
  .stage-desc {
    font-size: 0.78rem;
    color: #94a3b8;
    line-height: 1.45;
    margin: 0 0 0.6rem;
  }
  .stage-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1rem;
    margin-bottom: 0.7rem;
  }
  .stat {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
  }
  .stat-label {
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
  }
  .stat-value {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    font-weight: 700;
    color: #f1f5f9;
  }
  .stat-value.income {
    color: #10b981;
  }
  .stat-value.drain {
    color: #f87171;
  }
  .stat-value.discounted {
    color: #10b981;
  }
  .discount-tag {
    font-size: 0.65rem;
    color: #10b981;
    margin-left: 0.25rem;
  }
  .crop-select {
    margin-bottom: 0.7rem;
  }
  .crop-options {
    display: flex;
    gap: 0.35rem;
    margin-top: 0.3rem;
    flex-wrap: wrap;
  }
  .crop-chip {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.25);
    color: #cbd5e1;
    border-radius: 6px;
    padding: 0.3rem 0.5rem;
    cursor: pointer;
  }
  .crop-chip.active {
    border-color: #10b981;
    color: #34d399;
    background: rgba(16, 185, 129, 0.12);
  }
  .build-btn {
    width: 100%;
    background: #f59e0b;
    color: #020617;
    border: none;
    border-radius: 8px;
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 0.85rem;
    padding: 0.65rem;
    cursor: pointer;
    min-height: 44px;
    transition: background 0.15s;
  }
  .build-btn:hover:not(:disabled) {
    background: #fbbf24;
  }
  .build-btn:disabled {
    background: rgba(148, 163, 184, 0.2);
    color: #94a3b8;
    cursor: not-allowed;
    font-size: 0.74rem;
  }
  .blueprint-link {
    display: block;
    margin-top: 0.55rem;
    font-size: 0.72rem;
    color: #60a5fa;
    text-decoration: none;
  }
  .blueprint-link:hover {
    text-decoration: underline;
  }
  .construction {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .construction-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #fbbf24;
  }
  .progress-track {
    flex: 1;
    height: 8px;
    background: rgba(30, 41, 59, 0.9);
    border-radius: 4px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: #f59e0b;
    border-radius: 4px;
    transition: width 0.4s ease;
  }
  .construction-days {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: #f1f5f9;
  }
  .modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(2, 6, 23, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 20;
    backdrop-filter: blur(3px);
  }
  .modal {
    background: #0f172a;
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: 14px;
    padding: 1.4rem;
    max-width: 480px;
    width: calc(100% - 2rem);
  }
  .modal-title {
    margin: 0 0 1rem;
    font-size: 1.05rem;
    color: #f1f5f9;
  }
  .upgrade-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.7rem;
  }
  .upgrade-card {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 10px;
    padding: 0.9rem;
    cursor: pointer;
    text-align: left;
    transition: border-color 0.15s, transform 0.15s;
  }
  .upgrade-card:hover {
    border-color: #f59e0b;
    transform: translateY(-2px);
  }
  .upgrade-name {
    font-weight: 700;
    font-size: 0.92rem;
  }
  .upgrade-desc {
    font-size: 0.76rem;
    color: #94a3b8;
    line-height: 1.4;
  }
  @media (max-width: 640px) {
    .build-panel {
      left: 0.5rem;
      top: 3.6rem;
      width: 220px;
    }
    .upgrade-options {
      grid-template-columns: 1fr;
    }
  }
</style>
