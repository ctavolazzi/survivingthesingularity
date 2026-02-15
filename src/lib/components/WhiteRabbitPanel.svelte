<script>
  import { activeRabbits, getAllRabbits, exportJournals, clearFinishedRabbits, loadJournals, clearJournals } from '$lib/debug/white-rabbit.js';
  import { fly, fade } from 'svelte/transition';

  let open = false;
  let activeTab = 'live';
  let savedJournals = [];
  let expandedTrace = null;
  let filterLevel = 'all';

  function togglePanel() {
    open = !open;
    if (open && activeTab === 'history') {
      savedJournals = loadJournals();
    }
  }

  function handleExport() {
    const data = exportJournals();
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rabbit-traces-${new Date().toISOString().slice(0, 19)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function handleClearHistory() {
    clearJournals();
    savedJournals = [];
  }

  function handleClearFinished() {
    clearFinishedRabbits();
  }

  function switchTab(tab) {
    activeTab = tab;
    if (tab === 'history') {
      savedJournals = loadJournals();
    }
  }

  function formatTime(ms) {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(1)}s`;
  }

  function getLevelColor(level) {
    return {
      debug: '#64748b',
      info: '#3b82f6',
      warn: '#f59e0b',
      error: '#ef4444'
    }[level] || '#64748b';
  }

  $: liveTraces = getAllRabbits().map(r => r.report());

  function handleKeydown(e) {
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
      e.preventDefault();
      togglePanel();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<!-- The Rabbit Hole — floating trigger -->
<button class="rabbit-trigger" on:click={togglePanel} class:rabbit-trigger-active={open} title="White Rabbit Traces (Ctrl+Shift+D)">
  <span class="rabbit-icon">🐇</span>
  {#if $activeRabbits.some(r => r.errors > 0)}
    <span class="rabbit-badge error">{$activeRabbits.reduce((sum, r) => sum + r.errors, 0)}</span>
  {:else if $activeRabbits.length > 0}
    <span class="rabbit-badge">{$activeRabbits.length}</span>
  {/if}
</button>

{#if open}
  <div class="rabbit-panel" transition:fly={{ x: 300, duration: 200 }}>
    <div class="rabbit-header">
      <div class="rabbit-title">
        <span class="rabbit-title-icon">🐇</span>
        White Rabbit
      </div>
      <div class="rabbit-actions">
        <button class="rabbit-action" on:click={handleExport} title="Export journals">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
        </button>
        <button class="rabbit-action" on:click={handleClearFinished} title="Clear finished">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
        </button>
        <button class="rabbit-action" on:click={togglePanel} title="Close">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
    </div>

    <div class="rabbit-tabs">
      <button class="rabbit-tab" class:rabbit-tab-active={activeTab === 'live'} on:click={() => switchTab('live')}>
        Live ({$activeRabbits.length})
      </button>
      <button class="rabbit-tab" class:rabbit-tab-active={activeTab === 'history'} on:click={() => switchTab('history')}>
        Journals ({savedJournals.length})
      </button>
    </div>

    <div class="rabbit-filter">
      {#each ['all', 'error', 'warn', 'info', 'debug'] as level}
        <button
          class="filter-btn"
          class:filter-btn-active={filterLevel === level}
          style="--level-color: {getLevelColor(level)}"
          on:click={() => filterLevel = level}
        >
          {level}
        </button>
      {/each}
    </div>

    <div class="rabbit-body">
      {#if activeTab === 'live'}
        {#if $activeRabbits.length === 0}
          <div class="rabbit-empty">No rabbits out. Waiting at the hole...</div>
        {:else}
          {#each liveTraces as trace}
            <button class="trace-item" on:click={() => expandedTrace = expandedTrace === trace.id ? null : trace.id}>
              <div class="trace-header">
                <span class="trace-status" class:trace-home={trace.returned}></span>
                <span class="trace-name">{trace.name}</span>
                <span class="trace-duration">{formatTime(trace.duration)}</span>
                {#if trace.summary.errors > 0}
                  <span class="trace-badge error">{trace.summary.errors} err</span>
                {/if}
                {#if trace.summary.warnings > 0}
                  <span class="trace-badge warn">{trace.summary.warnings} warn</span>
                {/if}
              </div>
              <div class="trace-id">{trace.id}</div>

              {#if expandedTrace === trace.id}
                <div class="trace-entries" transition:fly={{ y: -5, duration: 150 }}>
                  {#each trace.journal.filter(e => filterLevel === 'all' || e.level === filterLevel) as entry}
                    <div class="entry" style="--entry-color: {getLevelColor(entry.level)}">
                      <span class="entry-time">+{entry.elapsed}ms</span>
                      <span class="entry-level">{entry.level}</span>
                      <span class="entry-msg">{entry.message}</span>
                      {#if entry.data}
                        <span class="entry-data">{JSON.stringify(entry.data)}</span>
                      {/if}
                    </div>
                  {/each}
                </div>
              {/if}
            </button>
          {/each}
        {/if}
      {:else}
        {#if savedJournals.length === 0}
          <div class="rabbit-empty">No saved journals.</div>
        {:else}
          <button class="clear-btn" on:click={handleClearHistory}>Clear all journals</button>
          {#each [...savedJournals].reverse() as trace}
            <button class="trace-item" on:click={() => expandedTrace = expandedTrace === trace.id ? null : trace.id}>
              <div class="trace-header">
                <span class="trace-status trace-home"></span>
                <span class="trace-name">{trace.name}</span>
                <span class="trace-duration">{formatTime(trace.duration)}</span>
              </div>
              <div class="trace-id">{trace.id} — {trace.startTime}</div>

              {#if expandedTrace === trace.id}
                <div class="trace-entries" transition:fly={{ y: -5, duration: 150 }}>
                  {#each trace.journal.filter(e => filterLevel === 'all' || e.level === filterLevel) as entry}
                    <div class="entry" style="--entry-color: {getLevelColor(entry.level)}">
                      <span class="entry-time">+{entry.elapsed}ms</span>
                      <span class="entry-level">{entry.level}</span>
                      <span class="entry-msg">{entry.message}</span>
                    </div>
                  {/each}
                </div>
              {/if}
            </button>
          {/each}
        {/if}
      {/if}
    </div>
  </div>
{/if}

<style>
  .rabbit-trigger {
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.15);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    transition: all 0.2s;
    backdrop-filter: blur(8px);
    padding: 0;
  }

  .rabbit-icon {
    font-size: 1.1rem;
    filter: grayscale(0.5);
    transition: filter 0.2s;
  }

  .rabbit-trigger:hover .rabbit-icon,
  .rabbit-trigger-active .rabbit-icon {
    filter: grayscale(0);
  }

  .rabbit-trigger:hover,
  .rabbit-trigger-active {
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.15);
  }

  .rabbit-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    min-width: 16px;
    height: 16px;
    border-radius: 8px;
    background: #3b82f6;
    color: white;
    font-size: 0.6rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 3px;
  }

  .rabbit-badge.error {
    background: #ef4444;
  }

  .rabbit-panel {
    position: fixed;
    bottom: 0;
    right: 0;
    width: 420px;
    max-height: 80vh;
    background: rgba(10, 15, 25, 0.97);
    border-left: 1px solid rgba(148, 163, 184, 0.1);
    border-top: 1px solid rgba(148, 163, 184, 0.1);
    border-top-left-radius: 12px;
    z-index: 9998;
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(16px);
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 0.75rem;
  }

  .rabbit-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
  }

  .rabbit-title {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-weight: 700;
    color: #e2e8f0;
    font-size: 0.8rem;
    letter-spacing: 0.02em;
  }

  .rabbit-title-icon {
    font-size: 0.9rem;
  }

  .rabbit-actions {
    display: flex;
    gap: 0.25rem;
  }

  .rabbit-action {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: none;
    color: #475569;
    cursor: pointer;
    border-radius: 6px;
    transition: all 0.15s;
  }

  .rabbit-action:hover {
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.05);
  }

  .rabbit-tabs {
    display: flex;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
  }

  .rabbit-tab {
    flex: 1;
    padding: 0.5rem;
    background: none;
    border: none;
    color: #475569;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.7rem;
    font-weight: 600;
    transition: all 0.15s;
  }

  .rabbit-tab:hover { color: #94a3b8; }

  .rabbit-tab-active {
    color: #3b82f6;
    border-bottom: 2px solid #3b82f6;
  }

  .rabbit-filter {
    display: flex;
    gap: 0.25rem;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.05);
  }

  .filter-btn {
    padding: 0.2rem 0.5rem;
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 4px;
    background: none;
    color: #475569;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.15s;
  }

  .filter-btn:hover {
    border-color: var(--level-color);
    color: var(--level-color);
  }

  .filter-btn-active {
    border-color: var(--level-color);
    color: var(--level-color);
    background: rgba(59, 130, 246, 0.05);
  }

  .rabbit-body {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem;
  }

  .rabbit-empty {
    text-align: center;
    color: #334155;
    padding: 2rem 1rem;
    font-style: italic;
  }

  .trace-item {
    display: block;
    width: 100%;
    text-align: left;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 8px;
    padding: 0.6rem 0.75rem;
    margin-bottom: 0.4rem;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s;
  }

  .trace-item:hover {
    border-color: rgba(59, 130, 246, 0.15);
    background: rgba(59, 130, 246, 0.03);
  }

  .trace-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .trace-status {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #22c55e;
    animation: hop 1.5s infinite;
    flex-shrink: 0;
  }

  @keyframes hop {
    0%, 100% { opacity: 0.5; transform: translateY(0); }
    50% { opacity: 1; transform: translateY(-2px); }
  }

  .trace-home {
    background: #475569;
    animation: none;
  }

  .trace-name {
    color: #e2e8f0;
    font-weight: 600;
    flex: 1;
    font-size: 0.72rem;
  }

  .trace-duration {
    color: #475569;
    font-size: 0.65rem;
  }

  .trace-badge {
    font-size: 0.55rem;
    padding: 0.1rem 0.35rem;
    border-radius: 3px;
    font-weight: 700;
    text-transform: uppercase;
  }

  .trace-badge.error {
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
  }

  .trace-badge.warn {
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
  }

  .trace-id {
    color: #334155;
    font-size: 0.6rem;
    margin-top: 0.2rem;
  }

  .trace-entries {
    margin-top: 0.5rem;
    border-top: 1px solid rgba(148, 163, 184, 0.06);
    padding-top: 0.4rem;
    max-height: 300px;
    overflow-y: auto;
  }

  .entry {
    display: flex;
    gap: 0.4rem;
    padding: 0.2rem 0;
    align-items: flex-start;
    border-left: 2px solid var(--entry-color);
    padding-left: 0.5rem;
    margin-bottom: 0.15rem;
  }

  .entry-time {
    color: #334155;
    font-size: 0.6rem;
    min-width: 55px;
    flex-shrink: 0;
  }

  .entry-level {
    font-size: 0.55rem;
    color: var(--entry-color);
    text-transform: uppercase;
    font-weight: 700;
    min-width: 35px;
    flex-shrink: 0;
  }

  .entry-msg {
    color: #94a3b8;
    font-size: 0.65rem;
    flex: 1;
  }

  .entry-data {
    color: #475569;
    font-size: 0.58rem;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .clear-btn {
    display: block;
    width: 100%;
    padding: 0.4rem;
    background: rgba(239, 68, 68, 0.05);
    border: 1px solid rgba(239, 68, 68, 0.1);
    border-radius: 6px;
    color: #ef4444;
    cursor: pointer;
    font-family: inherit;
    font-size: 0.65rem;
    margin-bottom: 0.5rem;
    transition: all 0.15s;
  }

  .clear-btn:hover {
    background: rgba(239, 68, 68, 0.1);
  }

  @media (max-width: 640px) {
    .rabbit-panel {
      width: 100%;
      border-left: none;
    }
  }
</style>
