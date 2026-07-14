<script>
  let name = '';
  let email = '';
  let answer = '';
  let honeypot = '';
  let state = 'idle'; // idle | loading | success | error
  let errorMsg = '';

  async function submit(e) {
    e.preventDefault();
    if (state === 'loading') return;
    state = 'loading';
    errorMsg = '';
    try {
      const res = await fetch('/api/discord-application', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, answer, _hp: honeypot }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        state = 'success';
      } else {
        state = 'error';
        errorMsg = data.error || 'Something went wrong. Try again.';
      }
    } catch {
      state = 'error';
      errorMsg = 'Network error. Try again.';
    }
  }
</script>

<div class="da-wrap">
  {#if state === 'success'}
    <div class="da-success" role="status">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      Application received. We review every one by hand, check your inbox.
    </div>
  {:else}
    <p class="da-label">Want to join for good?</p>
    <p class="da-sub">Tell us a bit about yourself. We review every application by hand.</p>

    <form class="da-form" on:submit={submit} novalidate>
      <input
        type="text"
        bind:value={honeypot}
        tabindex="-1"
        autocomplete="off"
        aria-hidden="true"
        style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none;"
      />
      <div class="da-row">
        <input
          type="text"
          class="da-input"
          bind:value={name}
          placeholder="Your name"
          required
          maxlength="120"
          autocomplete="name"
          disabled={state === 'loading'}
        />
        <input
          type="email"
          class="da-input"
          bind:value={email}
          placeholder="your@email.com"
          required
          maxlength="254"
          autocomplete="email"
          disabled={state === 'loading'}
        />
      </div>
      <textarea
        class="da-textarea"
        bind:value={answer}
        placeholder="What are you working on, and why do you want in?"
        maxlength="2000"
        rows="3"
        disabled={state === 'loading'}
      ></textarea>

      {#if state === 'error'}
        <p class="da-error" role="alert">{errorMsg}</p>
      {/if}

      <button type="submit" class="da-btn" disabled={state === 'loading' || !name.trim() || !email.trim() || !answer.trim()}>
        {state === 'loading' ? 'Sending…' : 'Apply to join'}
      </button>
    </form>
  {/if}
</div>

<style>
  .da-wrap {
    margin-top: 1.25rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(88, 101, 242, 0.15);
  }
  .da-label {
    font-size: 0.9rem; font-weight: 700; color: #f1f5f9; margin: 0 0 4px;
  }
  .da-sub {
    font-size: 0.82rem; color: #94a3b8; line-height: 1.5; margin: 0 0 12px;
  }
  .da-form { display: flex; flex-direction: column; gap: 8px; }
  .da-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .da-input, .da-textarea {
    flex: 1; min-width: 160px;
    padding: 10px 12px;
    background: rgba(2, 6, 23, 0.5);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: #f1f5f9;
    font-size: 0.88rem;
    font-family: inherit;
    outline: none;
    transition: border-color 0.15s ease;
  }
  .da-textarea { width: 100%; resize: vertical; }
  .da-input::placeholder, .da-textarea::placeholder { color: #64748b; }
  .da-input:focus, .da-textarea:focus { border-color: rgba(88, 101, 242, 0.5); }
  .da-input:disabled, .da-textarea:disabled { opacity: 0.5; }

  .da-btn {
    align-self: flex-start;
    padding: 9px 18px;
    background: #5865f2;
    color: #fff;
    font-size: 0.85rem;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: filter 0.15s ease;
  }
  .da-btn:hover:not(:disabled) { filter: brightness(1.1); }
  .da-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  .da-error { font-size: 0.8rem; color: #f87171; margin: 0; }

  .da-success {
    display: flex; align-items: center; gap: 9px;
    font-size: 0.88rem; font-weight: 600; color: #10b981;
  }

  @media (max-width: 480px) {
    .da-row { flex-direction: column; }
    .da-btn { width: 100%; text-align: center; }
  }
</style>
