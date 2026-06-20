<script>
  import { createEventDispatcher } from 'svelte';
  import { shouseGame } from '$lib/stores/shouseGame.js';
  import { STAGES } from '$lib/game/shouse/engine/stages.js';
  import { computeScore, computeGrade, GRADE_LABELS } from '$lib/game/shouse/engine/scoring.js';
  import { ACHIEVEMENT_DEFS } from '$lib/game/shouse/engine/achievements.js';

  export let game;

  const dispatch = createEventDispatcher();

  $: s = $shouseGame;
  $: score = s ? computeScore({ ...s, haulUses: s.haulUses, generatorUses: s.generatorUses }) : 0;
  $: grade = computeGrade(score);
  $: builtStages = s ? STAGES.slice(0, s.stage) : [];
  $: unlockedAchievements = s
    ? ACHIEVEMENT_DEFS.filter((d) => s.achievements.includes(d.id))
    : [];
  $: isBest = s && score >= s.best.bestScore && s.won;
</script>

{#if s && (s.won || s.lost)}
  <div class="end-backdrop">
    <div class="end-card" role="dialog" aria-label="Game over">
      {#if s.won}
        <div class="end-eyebrow">Shouse complete, day {s.day} of {s.maxDay}</div>
        <div class="grade grade-{grade.toLowerCase()}">{grade}</div>
        <h2 class="end-title">
          {GRADE_LABELS[grade]}
          {#if isBest}<span class="best-tag">New personal best</span>{/if}
        </h2>
      {:else}
        <div class="end-eyebrow">
          {s.loseReason === 'deadline' ? "Time's up" : 'Systems failure'}
        </div>
        <h2 class="end-title">
          {s.loseReason === 'deadline'
            ? `Day ${s.maxDay} arrived with the shouse at stage ${s.stage}/6.`
            : `Resources flatlined too long. Safeties tripped on day ${s.day}.`}
        </h2>
      {/if}

      <div class="stats-grid">
        {#if s.won}<div class="stat"><span class="stat-value">{score}</span><span class="stat-label">Score</span></div>{/if}
        <div class="stat"><span class="stat-value">${s.cash.toLocaleString()}</span><span class="stat-label">Cash left</span></div>
        <div class="stat"><span class="stat-value">{s.stage}/6</span><span class="stat-label">Stages built</span></div>
        <div class="stat"><span class="stat-value">{s.eventsTriggered}</span><span class="stat-label">Events survived</span></div>
        {#if s.harvests > 0}
          <div class="stat"><span class="stat-value">{s.harvests}</span><span class="stat-label">Harvests</span></div>
        {/if}
        <div class="stat"><span class="stat-value">{s.upgrades.length}</span><span class="stat-label">Upgrades</span></div>
      </div>

      {#if unlockedAchievements.length > 0}
        <div class="achievements">
          {#each unlockedAchievements as a (a.id)}
            <span class="achievement" title={a.desc}>🏆 {a.name}</span>
          {/each}
        </div>
      {/if}

      {#if builtStages.length > 0}
        <div class="built-list">
          <h3 class="built-title">What you built, and the real-world chapters behind it</h3>
          {#each builtStages as st (st.id)}
            <a class="built-row" href="/blueprint/{st.blueprintSlug}" target="_blank" rel="noopener">
              <span class="built-name">{st.shortName}</span>
              <span class="built-lesson">{st.lesson}</span>
              <span class="built-link">{st.blueprintTitle} →</span>
            </a>
          {/each}
        </div>
      {/if}

      <div class="end-actions">
        <button class="end-btn primary" on:click={() => dispatch('replay')}>Play Again</button>
        <button class="end-btn" on:click={() => dispatch('menu')}>Change Difficulty</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .end-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(2, 6, 23, 0.82);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 30;
    backdrop-filter: blur(4px);
    overflow-y: auto;
    padding: 1rem;
  }
  .end-card {
    background: #0f172a;
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: 16px;
    padding: 1.8rem;
    max-width: 560px;
    width: 100%;
    max-height: 100%;
    overflow-y: auto;
    text-align: center;
  }
  .end-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #94a3b8;
  }
  .grade {
    font-family: var(--font-mono);
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0.3rem 0;
  }
  .grade-s { color: #fbbf24; text-shadow: 0 0 30px rgba(245, 158, 11, 0.5); }
  .grade-a { color: #f59e0b; }
  .grade-b { color: #3b82f6; }
  .grade-c { color: #94a3b8; }
  .grade-d { color: #64748b; }
  .end-title {
    font-size: 1.15rem;
    color: #f1f5f9;
    margin: 0 0 1.2rem;
    line-height: 1.4;
  }
  .best-tag {
    display: inline-block;
    margin-left: 0.5rem;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: 6px;
    padding: 0.15rem 0.5rem;
    vertical-align: middle;
  }
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
    gap: 0.7rem;
    margin-bottom: 1.2rem;
  }
  .stat {
    background: rgba(30, 41, 59, 0.5);
    border-radius: 10px;
    padding: 0.6rem 0.4rem;
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }
  .stat-value {
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 1.05rem;
    color: #f1f5f9;
  }
  .stat-label {
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
  }
  .achievements {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    justify-content: center;
    margin-bottom: 1.2rem;
  }
  .achievement {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: #fbbf24;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 6px;
    padding: 0.25rem 0.55rem;
  }
  .built-list {
    text-align: left;
    margin-bottom: 1.3rem;
  }
  .built-title {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94a3b8;
    margin: 0 0 0.5rem;
  }
  .built-row {
    display: grid;
    grid-template-columns: 84px 1fr auto;
    gap: 0.6rem;
    align-items: center;
    padding: 0.45rem 0.55rem;
    border-radius: 8px;
    text-decoration: none;
    transition: background 0.15s;
  }
  .built-row:hover {
    background: rgba(30, 41, 59, 0.6);
  }
  .built-name {
    font-family: var(--font-mono);
    font-size: 0.74rem;
    font-weight: 700;
    color: #f59e0b;
  }
  .built-lesson {
    font-size: 0.72rem;
    color: #94a3b8;
    line-height: 1.35;
  }
  .built-link {
    font-size: 0.7rem;
    color: #60a5fa;
    white-space: nowrap;
  }
  .end-actions {
    display: flex;
    gap: 0.7rem;
    justify-content: center;
  }
  .end-btn {
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 0.85rem;
    border-radius: 8px;
    padding: 0.7rem 1.3rem;
    cursor: pointer;
    min-height: 44px;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.3);
    color: #f1f5f9;
    transition: border-color 0.15s, background 0.15s;
  }
  .end-btn:hover {
    border-color: #f59e0b;
  }
  .end-btn.primary {
    background: #f59e0b;
    border-color: #f59e0b;
    color: #020617;
  }
  .end-btn.primary:hover {
    background: #fbbf24;
  }
</style>
