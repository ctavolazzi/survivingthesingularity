<script>
  import { page } from '$app/stores';
</script>

<svelte:head>
  <title>{$page.status} · Surviving the Singularity</title>
  <meta name="robots" content="noindex" />
</svelte:head>

<div class="error-page">
  <div class="err-inner">
    <p class="err-code">{$page.status}</p>
    <h1 class="err-title">
      {#if $page.status === 404}
        Page not found
      {:else}
        Something went wrong
      {/if}
    </h1>
    <p class="err-msg">
      {#if $page.status === 404}
        That route doesn't exist or was moved. Head back to the start.
      {:else}
        {$page.error?.message || 'An unexpected error occurred.'}
      {/if}
    </p>
    <div class="err-actions">
      <a class="err-btn err-btn-primary" href="/">Home</a>
      <a class="err-btn" href="/blueprint">The Blueprint</a>
      <a class="err-btn" href="/disclaimer">Disclaimer</a>
    </div>
  </div>
</div>

<style>
  .error-page {
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 1.5rem;
  }
  .err-inner {
    max-width: 520px;
    text-align: center;
  }
  .err-code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #f59e0b;
    letter-spacing: 0.15em;
    margin: 0 0 1rem 0;
    text-transform: uppercase;
    font-weight: 700;
  }
  .err-title {
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 800;
    color: #fafafa;
    margin: 0 0 1rem 0;
    letter-spacing: -0.03em;
  }
  .err-msg {
    color: #94a3b8;
    font-size: 1rem;
    line-height: 1.7;
    margin: 0 0 2rem 0;
  }
  .err-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
  }
  .err-btn {
    padding: 0.7rem 1.4rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    text-decoration: none;
    color: #a1a1aa;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.15s ease;
  }
  .err-btn:hover {
    color: #fafafa;
    border-color: rgba(255, 255, 255, 0.2);
  }
  .err-btn-primary {
    background: rgba(245, 158, 11, 0.08);
    color: #f59e0b;
    border-color: rgba(245, 158, 11, 0.35);
  }
  .err-btn-primary:hover {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
  }
</style>
