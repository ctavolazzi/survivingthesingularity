<script>
  import { browser } from '$app/environment';
  import { fly } from 'svelte/transition';
  import { createEventDispatcher, onMount } from 'svelte';

  export let open = false;

  const dispatch = createEventDispatcher();

  const STORAGE_KEY = 'sts-reading-prefs';

  let fontSize = 'medium';
  let contentWidth = 'normal';
  let lineHeight = 'normal';

  const fontSizes = [
    { value: 'small', label: 'S', px: '0.95rem' },
    { value: 'medium', label: 'M', px: '1.05rem' },
    { value: 'large', label: 'L', px: '1.2rem' },
    { value: 'xlarge', label: 'XL', px: '1.35rem' },
  ];

  const contentWidths = [
    { value: 'narrow', label: 'Narrow', px: '620px' },
    { value: 'normal', label: 'Normal', px: '780px' },
    { value: 'wide', label: 'Wide', px: '960px' },
  ];

  const lineHeights = [
    { value: 'compact', label: 'Compact', val: '1.6' },
    { value: 'normal', label: 'Normal', val: '1.85' },
    { value: 'relaxed', label: 'Relaxed', val: '2.1' },
  ];

  function load() {
    if (!browser) return;
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const prefs = JSON.parse(stored);
        fontSize = prefs.fontSize || 'medium';
        contentWidth = prefs.contentWidth || 'normal';
        lineHeight = prefs.lineHeight || 'normal';
      }
    } catch {}
  }

  function save() {
    if (!browser) return;
    const prefs = { fontSize, contentWidth, lineHeight };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
    dispatch('change', prefs);
  }

  function setFontSize(val) { fontSize = val; save(); }
  function setContentWidth(val) { contentWidth = val; save(); }
  function setLineHeight(val) { lineHeight = val; save(); }

  function resetDefaults() {
    fontSize = 'medium';
    contentWidth = 'normal';
    lineHeight = 'normal';
    save();
  }

  onMount(load);

  $: currentFontPx = fontSizes.find(f => f.value === fontSize)?.px || '1.05rem';
  $: currentWidthPx = contentWidths.find(w => w.value === contentWidth)?.px || '780px';
  $: currentLineHeight = lineHeights.find(l => l.value === lineHeight)?.val || '1.85';

  // Dispatch the CSS variables whenever they change
  $: if (browser && (currentFontPx || currentWidthPx || currentLineHeight)) {
    dispatch('change', {
      '--reading-font-size': currentFontPx,
      '--reading-max-width': currentWidthPx,
      '--reading-line-height': currentLineHeight
    });
  }
</script>

{#if open}
  <div class="prefs-panel" transition:fly={{ y: -10, duration: 200 }}>
    <div class="prefs-header">
      <span class="prefs-title">Reading Preferences</span>
      <button class="prefs-close" on:click={() => dispatch('close')}>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M1 1L13 13M13 1L1 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      </button>
    </div>

    <div class="prefs-group">
      <span class="prefs-label">Font Size</span>
      <div class="prefs-options">
        {#each fontSizes as fs}
          <button
            class="prefs-opt"
            class:prefs-opt-active={fontSize === fs.value}
            on:click={() => setFontSize(fs.value)}
            style="font-size: {fs.value === 'small' ? '0.75rem' : fs.value === 'medium' ? '0.85rem' : fs.value === 'large' ? '1rem' : '1.15rem'}"
          >
            {fs.label}
          </button>
        {/each}
      </div>
    </div>

    <div class="prefs-group">
      <span class="prefs-label">Content Width</span>
      <div class="prefs-options">
        {#each contentWidths as cw}
          <button
            class="prefs-opt prefs-opt-text"
            class:prefs-opt-active={contentWidth === cw.value}
            on:click={() => setContentWidth(cw.value)}
          >
            {cw.label}
          </button>
        {/each}
      </div>
    </div>

    <div class="prefs-group">
      <span class="prefs-label">Line Height</span>
      <div class="prefs-options">
        {#each lineHeights as lh}
          <button
            class="prefs-opt prefs-opt-text"
            class:prefs-opt-active={lineHeight === lh.value}
            on:click={() => setLineHeight(lh.value)}
          >
            {lh.label}
          </button>
        {/each}
      </div>
    </div>

    <button class="prefs-reset" on:click={resetDefaults}>Reset to defaults</button>
  </div>
{/if}

<style>
  .prefs-panel {
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    width: 280px;
    background: #0f172a;
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 14px;
    padding: 1rem;
    z-index: 100;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
  }

  .prefs-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .prefs-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #e2e8f0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .prefs-close {
    background: none;
    border: none;
    color: #475569;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: color 0.2s;
  }

  .prefs-close:hover { color: #94a3b8; }

  .prefs-group {
    margin-bottom: 0.85rem;
  }

  .prefs-label {
    display: block;
    font-size: 0.7rem;
    color: #64748b;
    margin-bottom: 0.4rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .prefs-options {
    display: flex;
    gap: 0.35rem;
  }

  .prefs-opt {
    flex: 1;
    padding: 0.45rem 0.5rem;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 8px;
    color: #94a3b8;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s;
    font-family: inherit;
    text-align: center;
  }

  .prefs-opt:hover {
    border-color: rgba(245, 158, 11, 0.2);
    color: #e2e8f0;
  }

  .prefs-opt-active {
    background: rgba(245, 158, 11, 0.12);
    border-color: rgba(245, 158, 11, 0.3);
    color: #f59e0b;
  }

  .prefs-opt-text {
    font-size: 0.72rem;
    font-weight: 600;
  }

  .prefs-reset {
    width: 100%;
    padding: 0.5rem;
    background: none;
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 8px;
    color: #475569;
    font-size: 0.72rem;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s;
    margin-top: 0.25rem;
  }

  .prefs-reset:hover {
    color: #94a3b8;
    border-color: rgba(148, 163, 184, 0.12);
  }
</style>
