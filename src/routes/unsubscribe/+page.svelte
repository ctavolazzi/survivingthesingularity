<script>
  export let data;

  let state = 'idle'; // idle | loading | done | error | already_done
  let errorMsg = '';

  // If the server already knows it's done, skip the confirmation step.
  $: if (data.status === 'already_done') state = 'already_done';

  async function confirm() {
    if (state === 'loading') return;
    state = 'loading';
    errorMsg = '';

    try {
      const res = await fetch('/api/unsubscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: data.token }),
      });
      const json = await res.json();

      if (res.ok) {
        state = 'done';
      } else if (res.status === 409) {
        state = 'already_done';
      } else {
        state = 'error';
        errorMsg = json.error || 'Something went wrong. Try again.';
      }
    } catch {
      state = 'error';
      errorMsg = 'Network error. Try again.';
    }
  }
</script>

<svelte:head>
  <title>Unsubscribe | Surviving the Singularity</title>
  <meta name="robots" content="noindex" />
</svelte:head>

<div class="page">
  <div class="card">
    <p class="brand">Surviving the Singularity</p>

    {#if data.status === 'invalid' || data.status === 'not_found'}
      <h1 class="heading">Link not found</h1>
      <p class="body">This unsubscribe link is invalid or has expired. If you need help, reply to any email we've sent you.</p>

    {:else if data.status === 'error'}
      <h1 class="heading">Something went wrong</h1>
      <p class="body">We couldn't process your request right now. Try again later or reply to any email we've sent you.</p>

    {:else if state === 'done'}
      <h1 class="heading">You're unsubscribed.</h1>
      <p class="body">We've removed <strong>{data.email}</strong> from our list. You won't hear from us again.</p>
      <a href="/" class="link">Back to the site</a>

    {:else if state === 'already_done'}
      <h1 class="heading">Already unsubscribed.</h1>
      <p class="body"><strong>{data.email}</strong> has already been removed from our list.</p>
      <a href="/" class="link">Back to the site</a>

    {:else if state === 'error'}
      <h1 class="heading">Something went wrong</h1>
      <p class="body">{errorMsg}</p>
      <button class="btn" on:click={confirm}>Try again</button>

    {:else}
      <!-- state === 'idle' && data.status === 'pending' -->
      <h1 class="heading">Unsubscribe</h1>
      <p class="body">
        Confirm that you'd like to remove <strong>{data.email}</strong> from our list.
        You won't receive newsletters or book-release notifications from us.
      </p>
      <button
        class="btn"
        on:click={confirm}
        disabled={state === 'loading'}
      >
        {#if state === 'loading'}
          <span class="spinner" aria-hidden="true"></span>
          <span class="sr-only">Processing…</span>
        {:else}
          Confirm unsubscribe
        {/if}
      </button>
      <a href="/" class="cancel">Never mind</a>
    {/if}
  </div>
</div>

<style>
  .page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
    background: #020617;
  }

  .card {
    width: 100%;
    max-width: 480px;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .brand {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0;
  }

  .heading {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
    line-height: 1.25;
  }

  .body {
    font-size: 0.95rem;
    line-height: 1.65;
    color: #94a3b8;
    margin: 0;
  }

  .body strong {
    color: #e2e8f0;
    font-weight: 600;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    padding: 0.7rem 1.4rem;
    background: #ef4444;
    color: #fff;
    font-weight: 700;
    font-size: 0.9rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    width: fit-content;
    transition: opacity 0.15s ease;
  }
  .btn:hover:not(:disabled) { opacity: 0.85; }
  .btn:disabled { opacity: 0.55; cursor: not-allowed; }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .link {
    font-size: 0.85rem;
    color: #64748b;
    text-decoration: underline;
    text-underline-offset: 2px;
    width: fit-content;
  }
  .link:hover { color: #94a3b8; }

  .cancel {
    font-size: 0.82rem;
    color: #475569;
    text-decoration: underline;
    text-underline-offset: 2px;
    width: fit-content;
    cursor: pointer;
  }
  .cancel:hover { color: #64748b; }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    white-space: nowrap;
    border: 0;
  }
</style>
