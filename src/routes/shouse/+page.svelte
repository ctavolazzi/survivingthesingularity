<script>
  import ShouseGame from '$lib/components/game/ShouseGame.svelte';
</script>

<svelte:head>
  <title>Shouse Builder — Surviving the Singularity</title>
  <meta
    name="description"
    content="Build the ultimate $25k shouse before the deadline: container shell, utilities, local-AI server rack, solar, and a FarmBot bed. A 3D isometric strategy game."
  />
  <meta property="og:title" content="Shouse Builder — Surviving the Singularity" />
  <meta
    property="og:description"
    content="Raw land, $25,000, one season. Build the shouse from Blueprint Chapter 02 in 3D."
  />
</svelte:head>

<div class="game-viewport">
  <ShouseGame />
</div>

<style>
  .game-viewport {
    position: relative;
    width: 100%;
    /* fill viewport below the 60px nav */
    height: calc(100vh - 60px);
    height: calc(100dvh - 60px);
    min-height: 480px;
    overflow: hidden;
    background: #020617;
  }
</style>
