<script>
  import { onMount, onDestroy, tick } from 'svelte';
  import { sceneCatalog } from '$lib/bookScenes/catalog.js';
  export let sceneId;
  export let src;
  export let alt;
  $: info = sceneCatalog[sceneId];
  let mounted = false;
  let active = false;
  let loading = false;
  let failed = false;
  let selected = 'all';
  let angle = 0;
  let mode = 'illustration';
  let host;
  let controller;
  let pins = [];
  let disposed = false;
  let attempt = 0;
  $: description = info.options.find(option => option.id === selected)?.text ?? info.options[0].text;
  onMount(() => { mounted = true; });
  onDestroy(() => { disposed = true; attempt += 1; controller?.dispose(); });

  function stop() {
    attempt += 1;
    controller?.dispose(); controller = null;
    active = false; loading = false;
  }
  async function start() {
    failed = false; loading = true;
    const token = ++attempt;
    try {
      const { mountScene } = await import('$lib/bookScenes/runtime.js');
      if (disposed || token !== attempt) return;
      active = true;
      await tick();
      if (disposed || token !== attempt) return;
      controller = mountScene(host, sceneId, () => { stop(); failed = true; }, value => { pins = value; });
      controller.focus(selected); controller.view(angle, mode);
    } catch {
      stop(); failed = true;
    } finally { if (token === attempt) loading = false; }
  }
  function choose(value) { selected = value; controller?.focus(value); }
  function rotate(delta) { angle += delta; controller?.view(angle, mode); }
  function changeView(value) { mode = value; controller?.view(angle, mode); }
  function reset() { angle = 0; mode = 'illustration'; selected = 'all'; controller?.focus(selected); controller?.view(angle, mode); }
</script>

<div class="scene-presentation" data-scene-state={active ? 'webgl' : failed ? 'fallback' : 'still'}>
  <img class:concealed={active} class="scene-still" {src} {alt} width="960" height="800" loading="lazy" decoding="async" />
  {#if active}
    <div class="scene-live" role="img" aria-label={alt}>
      <div class="model-area"><div class="scene-canvas" bind:this={host}></div></div>
      <svg class="scene-annotations" viewBox="0 0 960 800" aria-hidden="true">
        <text x="40" y="54" fill="#f1f5f9" font-size="39" font-weight="700">{info.title}</text>
        <path d="M40 83H920 M40 610H920" stroke="#475569" stroke-width="1.5" fill="none" />
        {#each pins as pin}
          <circle cx={pin.x} cy={pin.y + 100} r="19" fill="#020617" stroke="#f59e0b" stroke-width="3" />
          <text x={pin.x} y={pin.y + 108} text-anchor="middle" font-size="25" font-weight="700" fill="#f1f5f9">{pin.number}</text>
        {/each}
        {#each info.labels as label, i}
          <text x={i % 2 ? 505 : 40} y={i < 2 ? 646 : 719} fill="#f59e0b" font-size="25" font-weight="700">{`${i + 1}  ${label[0]}`}</text>
          <text x={i % 2 ? 505 : 40} y={i < 2 ? 676 : 749} fill="#f1f5f9" font-size="26">{label[1]}</text>
        {/each}
        <text x="40" y="788" fill="#94a3b8" font-size="24">{info.note}</text>
      </svg>
    </div>
  {/if}
</div>

{#if mounted}
  <div class="scene-controls">
    <div class="main-controls">
      {#if active}
        <button type="button" class="primary" on:click={stop}>Use still illustration</button>
      {:else}
        <button type="button" class="primary" on:click={start} disabled={loading}>{loading ? 'Opening 3D view…' : 'Explore in 3D'}</button>
      {/if}
      <span class="control-hint">{active ? 'Use the buttons to explore. Nothing moves on its own.' : 'The complete illustration is available above.'}</span>
    </div>
    {#if failed}<p class="fallback-notice" role="status">The 3D view isn’t available here. The illustration and text below show the same connections.</p>{/if}
    {#if active}
      <div class="control-row" role="group" aria-label="Explore connections">
        {#each info.options as option}<button type="button" aria-pressed={selected === option.id} on:click={() => choose(option.id)}>{option.label}</button>{/each}
      </div>
      <div class="control-row" role="group" aria-label="Camera view">
        <button type="button" on:click={() => rotate(-Math.PI / 8)} aria-label="Rotate view left">Rotate left</button>
        <button type="button" on:click={() => rotate(Math.PI / 8)} aria-label="Rotate view right">Rotate right</button>
        <button type="button" aria-pressed={mode === 'top'} on:click={() => changeView(mode === 'top' ? 'illustration' : 'top')}>View from above</button>
        <button type="button" on:click={reset}>Reset view</button>
      </div>
      <p class="scene-explanation" role="status" aria-live="polite" aria-atomic="true">{description}</p>
    {/if}
  </div>
{/if}

<style>
  .scene-presentation { position: relative; width: 100%; aspect-ratio: 960 / 800; background: #020617; }
  .scene-presentation > .scene-still { display: block; width: 100%; height: auto; margin: 0; border: 0; border-radius: 0; box-shadow: none; }
  .scene-still.concealed { visibility: hidden; }
  .scene-live { position: absolute; inset: 0; overflow: hidden; }
  .model-area { position: absolute; left: 0; top: 12.5%; width: 100%; height: 63.75%; }
  .scene-canvas { width: 100%; height: 100%; }
  .scene-canvas :global(canvas) { width: 100%; height: 100%; display: block; }
  .scene-annotations { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; font-family: Inter, Arial, sans-serif; }
  .scene-controls { padding: 1rem 1.25rem; border-top: 1px solid #334155; font-family: Inter, sans-serif; }
  .main-controls, .control-row { display: flex; align-items: center; flex-wrap: wrap; gap: .5rem; }
  .control-row { margin-top: .75rem; }
  button { min-height: 44px; padding: .55rem .8rem; border-radius: 5px; border: 1px solid #475569; background: #0f172a; color: #f1f5f9; font: 500 .85rem/1.3 Inter, sans-serif; cursor: pointer; }
  button:hover, button[aria-pressed="true"] { border-color: #f59e0b; background: #1e293b; color: #f59e0b; }
  button:focus-visible { outline: 3px solid #3b82f6; outline-offset: 3px; }
  button:disabled { cursor: wait; opacity: .7; }
  button.primary { background: #f59e0b; color: #020617; border-color: #f59e0b; }
  .control-hint { flex: 1 1 12rem; color: #94a3b8; font-size: .8rem; line-height: 1.5; }
  .scene-explanation, .fallback-notice { color: #cbd5e1; font-size: .9rem; line-height: 1.65; margin: .9rem 0 0; }
  @media print { .scene-controls, .scene-live { display: none; } .scene-still.concealed { visibility: visible; } }
  @media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition: none !important; animation: none !important; } }
</style>
