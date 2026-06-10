<script>
  import { onDestroy } from 'svelte';
  import { createShouseGame } from '$lib/game/shouse/engine/createGame.js';
  import { DIFFICULTIES } from '$lib/game/shouse/engine/constants.js';
  import { TOTAL_BUILD_COST } from '$lib/game/shouse/engine/stages.js';
  import { shouseGame } from '$lib/stores/shouseGame.js';
  import GameCanvas from './GameCanvas.svelte';
  import GameHUD from './GameHUD.svelte';
  import BuildMenu from './BuildMenu.svelte';
  import EventToast from './EventToast.svelte';
  import EndScreen from './EndScreen.svelte';

  let phase = 'start'; // start | playing
  let game = null;
  let canvasComp;
  let difficulty = 'builder';
  let unsubscribe = null;
  let toasts = [];
  let toastId = 0;
  let best = null;

  // best score for the start screen (localStorage, client only)
  import { browser } from '$app/environment';
  if (browser) {
    try {
      best = JSON.parse(localStorage.getItem('sts-shouse-builder') || 'null');
    } catch {
      best = null;
    }
  }

  function pushToast(kind, title, msg, link = null, duration = 4500) {
    const t = { id: ++toastId, kind, title, msg, link };
    toasts = [...toasts, t];
    setTimeout(() => {
      toasts = toasts.filter((x) => x.id !== t.id);
    }, duration);
  }

  function start(diff) {
    difficulty = diff;
    game = createShouseGame({ difficulty: diff });
    unsubscribe = game.subscribe((evt) => {
      if (evt.type === 'event') {
        pushToast('event', evt.event.name, evt.event.msg);
      } else if (evt.type === 'achievement') {
        pushToast('achievement', `Achievement: ${evt.achievement.name}`, evt.achievement.desc);
      } else if (evt.type === 'buildStart') {
        pushToast('stage', `Crew on site: ${evt.stage.name}`, `${evt.stage.buildDays} days to complete.`);
      } else if (evt.type === 'stage') {
        pushToast(
          'stage',
          `${evt.stage.name} complete`,
          evt.stage.lesson,
          { href: `/blueprint/${evt.stage.blueprintSlug}`, label: `Read: ${evt.stage.blueprintTitle}` },
          7000
        );
      } else if (evt.type === 'harvest') {
        pushToast('stage', `Harvest: ${evt.plant.name}`, `+$${evt.plant.salePrice} produce sold.`, null, 2500);
      }
    });
    phase = 'playing';
  }

  function teardown() {
    unsubscribe?.();
    unsubscribe = null;
    game = null;
    toasts = [];
    shouseGame.reset();
    if (browser) {
      try {
        best = JSON.parse(localStorage.getItem('sts-shouse-builder') || 'null');
      } catch {
        /* ignore */
      }
    }
  }

  function replay() {
    const d = difficulty;
    teardown();
    start(d);
  }

  function backToMenu() {
    teardown();
    phase = 'start';
  }

  onDestroy(teardown);
</script>

{#if phase === 'start'}
  <div class="start-screen">
    <div class="start-inner">
      <span class="start-eyebrow">A Surviving the Singularity strategy game</span>
      <h1 class="start-title">Shouse Builder</h1>
      <p class="start-sub">
        Raw land. <span class="mono amber">${(25000).toLocaleString()}</span>. One season.
        Build the ultimate shouse — container shell, 200A utilities, RV living quarters,
        a local-AI server rack, solar, and a FarmBot bed — before the deadline.
        Total bill: <span class="mono">${TOTAL_BUILD_COST.toLocaleString()}</span>.
        The gap is yours to close.
      </p>

      <div class="how-to">
        <div class="how-item"><span class="how-key">Build</span> stages in order — each takes days and dollars</div>
        <div class="how-item"><span class="how-key">Watch</span> water + power once utilities go live</div>
        <div class="how-item"><span class="how-key">Earn</span> rent savings, content income, produce sales</div>
        <div class="how-item"><span class="how-key">Survive</span> heat waves, outages, inspections, GPU spikes</div>
      </div>

      <div class="difficulty-row">
        {#each Object.entries(DIFFICULTIES) as [key, d] (key)}
          <button class="diff-card" class:selected={difficulty === key} on:click={() => (difficulty = key)}>
            <span class="diff-name">{d.label}</span>
            <span class="diff-desc">{d.desc}</span>
            <span class="diff-stats mono">{d.maxDay} days · ${d.startCash.toLocaleString()}</span>
          </button>
        {/each}
      </div>

      <button class="start-btn" on:click={() => start(difficulty)}>Break Ground</button>

      {#if best?.bestScore}
        <div class="best-line mono">
          Best: {best.bestScore} ({best.bestGrade}) · {best.gamesPlayed} builds attempted
        </div>
      {/if}

      <div class="start-footer">
        <span class="controls-hint mono">drag pan · scroll zoom · Q/E rotate · C cutaway · Space pause · 1/2/3 speed</span>
        <a href="/blueprint/the-shouse" class="footer-link">Based on Blueprint Ch. 02: The Shouse →</a>
      </div>
    </div>
  </div>
{:else if game}
  <div class="game-stage">
    <GameCanvas bind:this={canvasComp} {game} />
    <GameHUD
      {game}
      on:rotate={(e) => canvasComp?.rotate(e.detail)}
      on:cutaway={() => canvasComp?.toggleCutaway()}
    />
    <BuildMenu {game} />
    <EventToast {toasts} />
    <EndScreen {game} on:replay={replay} on:menu={backToMenu} />
  </div>
{/if}

<style>
  .start-screen {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-y: auto;
    background:
      radial-gradient(ellipse at 30% 20%, rgba(245, 158, 11, 0.07), transparent 50%),
      radial-gradient(ellipse at 70% 80%, rgba(59, 130, 246, 0.06), transparent 50%),
      #020617;
  }
  .start-inner {
    max-width: 640px;
    padding: 2rem 1.5rem;
    text-align: center;
  }
  .start-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #f59e0b;
  }
  .start-title {
    font-size: clamp(2.2rem, 6vw, 3.4rem);
    font-weight: 800;
    color: #f1f5f9;
    margin: 0.3rem 0 0.8rem;
    letter-spacing: -0.02em;
  }
  .start-sub {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0 0 1.4rem;
  }
  .mono {
    font-family: var(--font-mono);
  }
  .amber {
    color: #f59e0b;
    font-weight: 700;
  }
  .how-to {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    text-align: left;
  }
  .how-item {
    font-size: 0.78rem;
    color: #94a3b8;
    background: rgba(30, 41, 59, 0.4);
    border-radius: 8px;
    padding: 0.55rem 0.7rem;
    line-height: 1.4;
  }
  .how-key {
    font-family: var(--font-mono);
    font-weight: 700;
    color: #f59e0b;
    text-transform: uppercase;
    font-size: 0.68rem;
    margin-right: 0.3rem;
  }
  .difficulty-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.7rem;
    margin-bottom: 1.4rem;
  }
  .diff-card {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 12px;
    padding: 0.9rem 0.7rem;
    cursor: pointer;
    text-align: center;
    transition: border-color 0.15s, transform 0.15s;
  }
  .diff-card:hover {
    transform: translateY(-2px);
  }
  .diff-card.selected {
    border-color: #f59e0b;
    background: rgba(245, 158, 11, 0.08);
  }
  .diff-name {
    font-weight: 700;
    font-size: 0.95rem;
    color: #f1f5f9;
  }
  .diff-desc {
    font-size: 0.7rem;
    color: #94a3b8;
    line-height: 1.35;
  }
  .diff-stats {
    font-size: 0.68rem;
    color: #64748b;
  }
  .start-btn {
    background: #f59e0b;
    color: #020617;
    border: none;
    border-radius: 10px;
    font-family: var(--font-mono);
    font-weight: 800;
    font-size: 1rem;
    padding: 0.85rem 2.4rem;
    cursor: pointer;
    min-height: 48px;
    transition: background 0.15s, transform 0.15s;
  }
  .start-btn:hover {
    background: #fbbf24;
    transform: translateY(-1px);
  }
  .best-line {
    margin-top: 0.9rem;
    font-size: 0.74rem;
    color: #64748b;
  }
  .start-footer {
    margin-top: 1.6rem;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }
  .controls-hint {
    font-size: 0.66rem;
    color: #475569;
  }
  .footer-link {
    font-size: 0.76rem;
    color: #60a5fa;
    text-decoration: none;
  }
  .footer-link:hover {
    text-decoration: underline;
  }
  .game-stage {
    position: absolute;
    inset: 0;
  }
  @media (max-width: 640px) {
    .how-to,
    .difficulty-row {
      grid-template-columns: 1fr;
    }
  }
</style>
