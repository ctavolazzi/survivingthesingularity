<script>
  import { createEventDispatcher } from 'svelte';
  import { shouseGame } from '$lib/stores/shouseGame.js';
  import { SHAKEDOWN_DAYS } from '$lib/game/shouse/engine/createGame.js';

  export let game;

  const dispatch = createEventDispatcher();

  $: s = $shouseGame;

  function cdSeconds(frames) {
    return Math.ceil(frames / 60);
  }
</script>

{#if s}
  <!-- Top strip: clock, forecast, events, cash -->
  <div class="hud hud-top">
    <div class="hud-block">
      <span class="hud-label">Day</span>
      <span class="hud-value">{s.day}<span class="hud-dim">/{s.maxDay}</span></span>
      {#if s.stage >= 6 && !s.won}
        <span class="badge badge-amber">Shakedown {s.shakedownDays}/{SHAKEDOWN_DAYS}</span>
      {/if}
      {#if s.paused && !s.won && !s.lost && !s.pendingUpgrade}
        <span class="badge badge-blue">Paused</span>
      {/if}
    </div>

    <div class="hud-block forecast">
      {#each s.forecast as f (f.day)}
        <span class="forecast-chip" title={f.label}>
          <span class="forecast-day">D{f.day}</span>
          {f.label}
        </span>
      {/each}
      {#each s.activeEvents as ev (ev.id)}
        <span class="badge badge-red">{ev.name} ({ev.endsOnDay - s.day}d)</span>
      {/each}
    </div>

    <div class="hud-block">
      <span class="hud-label">Cash</span>
      <span class="hud-value cash">${s.cash.toLocaleString()}</span>
    </div>
  </div>

  <!-- Bottom strip: meters + actions -->
  <div class="hud hud-bottom">
    <div class="meters">
      <div class="meter">
        <span class="meter-label">Water</span>
        <div class="meter-track" class:inactive={s.stage < 3}>
          <div
            class="meter-fill"
            class:danger={s.water < 20}
            style="width: {Math.min(100, (s.water / s.waterCap) * 100)}%"
          ></div>
        </div>
        <span class="meter-num">{s.stage >= 3 ? s.water : '--'}</span>
      </div>
      <div class="meter">
        <span class="meter-label">Power</span>
        <div class="meter-track" class:inactive={s.stage < 3}>
          <div
            class="meter-fill power"
            class:danger={s.power < 20}
            style="width: {Math.min(100, (s.power / s.powerCap) * 100)}%"
          ></div>
        </div>
        <span class="meter-num">{s.stage >= 3 ? s.power : '--'}</span>
      </div>
      {#if s.stressFrames > 0}
        <div class="stress-warn">SYSTEM STRESS: refill now or safeties trip</div>
      {/if}
    </div>

    <div class="actions">
      <button
        class="btn"
        disabled={s.haulCd > 0 || s.won || s.lost}
        on:click={() => game.haulWater()}
        title="+30 water"
      >
        {s.haulCd > 0 ? `Haul ${cdSeconds(s.haulCd)}s` : 'Haul Water'}
      </button>
      <button
        class="btn"
        disabled={s.generatorCd > 0 || s.cash < 40 || s.won || s.lost}
        on:click={() => game.runGenerator()}
        title="+35 power, $40 fuel"
      >
        {s.generatorCd > 0 ? `Gen ${cdSeconds(s.generatorCd)}s` : 'Generator $40'}
      </button>

      <div class="divider"></div>

      <button class="btn btn-icon" on:click={() => game.togglePause()} title="Pause (Space)">
        {s.paused ? '▶' : '⏸'}
      </button>
      {#each [1, 2, 3] as sp}
        <button
          class="btn btn-icon"
          class:active={s.speed === sp}
          on:click={() => game.setSpeed(sp)}
          title="{sp}x speed"
        >
          {sp}x
        </button>
      {/each}

      <div class="divider"></div>

      <button class="btn btn-icon" on:click={() => dispatch('rotate', -1)} title="Rotate left (Q)">⟲</button>
      <button class="btn btn-icon" on:click={() => dispatch('rotate', 1)} title="Rotate right (E)">⟳</button>
      <button class="btn btn-icon" on:click={() => dispatch('cutaway')} title="Cutaway view (C)">⌂</button>
    </div>
  </div>
{/if}

<style>
  .hud {
    position: absolute;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.9rem;
    pointer-events: none;
    z-index: 5;
  }
  .hud > * {
    pointer-events: auto;
  }
  .hud-top {
    top: 0;
    justify-content: space-between;
    flex-wrap: wrap;
  }
  .hud-bottom {
    bottom: 0;
    justify-content: space-between;
    flex-wrap: wrap;
  }
  .hud-block {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 8px;
    padding: 0.35rem 0.7rem;
    backdrop-filter: blur(4px);
  }
  .hud-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94a3b8;
  }
  .hud-value {
    font-family: var(--font-mono);
    font-weight: 700;
    color: #f1f5f9;
    font-size: 1.05rem;
  }
  .hud-dim {
    color: #64748b;
    font-size: 0.85rem;
  }
  .cash {
    color: #f59e0b;
  }
  .forecast {
    gap: 0.4rem;
  }
  .forecast-chip {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: #cbd5e1;
    background: rgba(30, 41, 59, 0.8);
    border-radius: 6px;
    padding: 0.15rem 0.45rem;
    white-space: nowrap;
  }
  .forecast-day {
    color: #64748b;
    margin-right: 0.25rem;
  }
  .badge {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 700;
    border-radius: 6px;
    padding: 0.15rem 0.5rem;
    white-space: nowrap;
  }
  .badge-amber {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.4);
  }
  .badge-blue {
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.4);
  }
  .badge-red {
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
  }
  .meters {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 8px;
    padding: 0.5rem 0.7rem;
    backdrop-filter: blur(4px);
    min-width: 220px;
  }
  .meter {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .meter-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94a3b8;
    width: 50px;
    white-space: nowrap;
  }
  .meter-track {
    flex: 1;
    height: 8px;
    background: rgba(30, 41, 59, 0.9);
    border-radius: 4px;
    overflow: hidden;
  }
  .meter-track.inactive {
    opacity: 0.35;
  }
  .meter-fill {
    height: 100%;
    background: #3b82f6;
    border-radius: 4px;
    transition: width 0.3s ease;
  }
  .meter-fill.power {
    background: #f59e0b;
  }
  .meter-fill.danger {
    background: #ef4444;
  }
  .meter-num {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: #f1f5f9;
    width: 28px;
    text-align: right;
  }
  .stress-warn {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 700;
    color: #f87171;
    animation: blink 0.8s infinite alternate;
  }
  @keyframes blink {
    from { opacity: 1; }
    to { opacity: 0.45; }
  }
  .actions {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    flex-wrap: wrap;
  }
  .btn {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(245, 158, 11, 0.35);
    color: #f1f5f9;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    min-height: 44px;
    backdrop-filter: blur(4px);
    transition: border-color 0.15s, background 0.15s;
  }
  .btn:hover:not(:disabled) {
    border-color: #f59e0b;
    background: rgba(245, 158, 11, 0.12);
  }
  .btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
  .btn-icon {
    min-width: 44px;
    padding: 0.5rem 0.5rem;
  }
  .btn.active {
    background: rgba(245, 158, 11, 0.2);
    border-color: #f59e0b;
    color: #fbbf24;
  }
  .divider {
    width: 1px;
    height: 28px;
    background: rgba(148, 163, 184, 0.2);
  }
  @media (max-width: 640px) {
    .hud {
      padding: 0.4rem 0.5rem;
      gap: 0.4rem;
    }
    .meters {
      min-width: 170px;
    }
    .forecast {
      display: none;
    }
  }
</style>
