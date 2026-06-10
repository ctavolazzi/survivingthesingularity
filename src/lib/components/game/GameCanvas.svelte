<script>
  import { onMount } from 'svelte';
  import { shouseGame } from '$lib/stores/shouseGame.js';

  export let game;

  let canvas;
  let wrapper;
  let renderer = null;
  let raf = 0;
  let last = 0;
  let frameCount = 0;
  let autoPaused = false;

  export function rotate(dir) {
    renderer?.rotate(dir);
  }

  export function toggleCutaway() {
    return renderer ? renderer.toggleCutaway() : false;
  }

  function resize() {
    if (!renderer || !wrapper) return;
    renderer.resize(wrapper.clientWidth, wrapper.clientHeight);
  }

  onMount(() => {
    let disposed = false;
    let ro = null;

    shouseGame.sync(game.getState());

    // Dynamic import is the SSR guard: three never executes server-side.
    (async () => {
      const mod = await import('$lib/game/shouse/renderer/createRenderer.js');
      if (disposed) return;
      renderer = mod.createShouseRenderer(canvas);
      resize();
      ro = new ResizeObserver(resize);
      ro.observe(wrapper);

      last = performance.now();
      const loop = (now) => {
        raf = requestAnimationFrame(loop);
        const dt = Math.min(0.1, (now - last) / 1000);
        last = now;
        game.tick();
        renderer.render(game.getState(), dt);
        if (++frameCount % 6 === 0) shouseGame.sync(game.getState());
      };
      raf = requestAnimationFrame(loop);
    })();

    function onVisibility() {
      const s = game.getState();
      if (document.hidden) {
        if (!s.paused && !s.won && !s.lost) {
          game.togglePause();
          autoPaused = true;
        }
      } else if (autoPaused) {
        autoPaused = false;
        if (s.paused && !s.won && !s.lost) game.togglePause();
        last = performance.now();
      }
    }

    function onKey(e) {
      if (e.repeat) return;
      if (e.code === 'Space') {
        e.preventDefault();
        game.togglePause();
      } else if (e.key === '1' || e.key === '2' || e.key === '3') {
        game.setSpeed(Number(e.key));
      } else if (e.key === 'q' || e.key === 'Q') {
        rotate(-1);
      } else if (e.key === 'e' || e.key === 'E') {
        rotate(1);
      } else if (e.key === 'c' || e.key === 'C') {
        toggleCutaway();
      }
    }

    document.addEventListener('visibilitychange', onVisibility);
    window.addEventListener('keydown', onKey);

    return () => {
      disposed = true;
      cancelAnimationFrame(raf);
      document.removeEventListener('visibilitychange', onVisibility);
      window.removeEventListener('keydown', onKey);
      ro?.disconnect();
      renderer?.dispose();
      renderer = null;
    };
  });
</script>

<div class="canvas-wrap" bind:this={wrapper}>
  <canvas bind:this={canvas} aria-label="Shouse Builder 3D scene"></canvas>
</div>

<style>
  .canvas-wrap {
    position: absolute;
    inset: 0;
    overflow: hidden;
  }
  canvas {
    display: block;
    width: 100%;
    height: 100%;
    touch-action: none;
    cursor: grab;
  }
  canvas:active {
    cursor: grabbing;
  }
</style>
