<script>
  import { novelPrefs, FONT_SIZES } from '$lib/novel/novelReader.js';

  function step(delta) {
    novelPrefs.update((p) => {
      const i = FONT_SIZES.indexOf(p.size);
      const next = FONT_SIZES[Math.min(FONT_SIZES.length - 1, Math.max(0, (i < 0 ? 2 : i) + delta))];
      return { ...p, size: next };
    });
  }
  function toggleTheme() {
    novelPrefs.update((p) => ({ ...p, theme: p.theme === 'paper' ? 'night' : 'paper' }));
  }
  $: smallest = $novelPrefs.size === FONT_SIZES[0];
  $: largest = $novelPrefs.size === FONT_SIZES[FONT_SIZES.length - 1];
</script>

<div class="controls" role="group" aria-label="Reading settings">
  <button type="button" on:click={() => step(-1)} disabled={smallest} aria-label="Smaller text">A<span class="minus">−</span></button>
  <button type="button" on:click={() => step(1)} disabled={largest} aria-label="Larger text">A<span class="plus">+</span></button>
  <button type="button" on:click={toggleTheme} aria-label={$novelPrefs.theme === 'paper' ? 'Switch to dark page' : 'Switch to light page'}>
    {#if $novelPrefs.theme === 'paper'}
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
    {:else}
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4.5" stroke="currentColor" stroke-width="2"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    {/if}
  </button>
</div>

<style>
  .controls { display: flex; gap: 6px; }
  button {
    min-width: 44px;
    min-height: 40px;
    padding: 0 10px;
    border-radius: 8px;
    border: 1px solid var(--rule);
    background: var(--card);
    color: var(--ink);
    font: 600 15px/1 Inter, system-ui, sans-serif;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  button:disabled { opacity: 0.4; cursor: default; }
  .minus, .plus { font-size: 12px; margin-left: 1px; }
</style>
