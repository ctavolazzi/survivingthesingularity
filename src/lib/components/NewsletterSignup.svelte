<script>
  export let source = 'homepage';
  export let label = 'Stay in the loop';
  export let placeholder = 'your@email.com';
  export let buttonText = 'Sign Up';
  export let bookUrl = '';

  let email = '';
  let newsletterConsent = false; // opt-in: unchecked by default (GDPR)
  let bookReleaseConsent = false; // opt-in: unchecked by default (GDPR)
  let honeypot = ''; // hidden, should stay empty
  let state = 'idle'; // idle | loading | success | duplicate | error
  let errorMsg = '';

  $: atLeastOne = newsletterConsent || bookReleaseConsent;

  async function submit(e) {
    e.preventDefault();
    if (state === 'loading') return;
    state = 'loading';
    errorMsg = '';

    try {
      const res = await fetch('/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          source,
          newsletter_consent: newsletterConsent,
          book_release_consent: bookReleaseConsent,
          _hp: honeypot, // send honeypot value; server silently drops if filled
        }),
      });

      const data = await res.json();

      if (res.status === 201) {
        state = 'success';
      } else if (res.status === 409) {
        state = 'duplicate';
      } else {
        state = 'error';
        errorMsg = data.error || 'Something went wrong.';
      }
    } catch {
      state = 'error';
      errorMsg = 'Network error. Try again.';
    }
  }
</script>

<div class="waitlist-wrap">
  {#if state === 'success'}
    <div class="waitlist-success" role="status">
      <span class="success-icon" aria-hidden="true">✓</span>
      <div>
        <p class="success-title">You're on the list.</p>
        <p class="success-sub">
          {#if newsletterConsent && bookReleaseConsent}
            We'll send you updates and notify you when the book drops.
          {:else if newsletterConsent}
            Newsletter updates coming your way.
          {:else}
            We'll notify you when the book releases.
          {/if}
        </p>
      </div>
    </div>

  {:else if state === 'duplicate'}
    <div class="waitlist-success waitlist-duplicate" role="status">
      <span class="success-icon" aria-hidden="true">✓</span>
      <div>
        <p class="success-title">Already signed up.</p>
        <p class="success-sub">We have your email. We'll be in touch.</p>
      </div>
    </div>

  {:else}
    {#if label}
      <p class="waitlist-label">{label}</p>
    {/if}

    <form class="waitlist-form" on:submit={submit} novalidate>
      <!-- Honeypot: visually hidden, aria-hidden, tab -1 -->
      <input
        class="hp-field"
        type="text"
        name="_hp"
        bind:value={honeypot}
        tabindex="-1"
        autocomplete="off"
        aria-hidden="true"
      />

      <div class="waitlist-input-row">
        <input
          class="waitlist-input"
          class:has-error={state === 'error'}
          type="email"
          bind:value={email}
          {placeholder}
          required
          autocomplete="email"
          disabled={state === 'loading'}
          aria-label="Email address"
          maxlength="254"
        />
        <button
          class="waitlist-btn"
          type="submit"
          disabled={state === 'loading' || !email || !atLeastOne}
        >
          {#if state === 'loading'}
            <span class="spinner" aria-hidden="true"></span>
            <span class="sr-only">Submitting…</span>
          {:else}
            {buttonText}
          {/if}
        </button>
      </div>

      <p class="consent-prompt">What should we send you?</p>
      <div class="consent-row">
        <label class="consent-label">
          <input type="checkbox" bind:checked={newsletterConsent} />
          <span>Newsletter updates</span>
        </label>
        <label class="consent-label">
          <input type="checkbox" bind:checked={bookReleaseConsent} />
          <span>Notify me when {#if bookUrl}<a href={bookUrl} class="book-link">the book</a>{:else}the book{/if} drops</span>
        </label>
      </div>

      {#if state === 'error'}
        <p class="waitlist-error" role="alert">{errorMsg}</p>
      {/if}
    </form>

    <p class="waitlist-meta">No spam. Unsubscribe any time. See our <a href="/policies" class="meta-link">privacy policy</a>.</p>
  {/if}
</div>

<style>
  .waitlist-wrap {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
    width: 100%;
  }

  .waitlist-label {
    font-size: 0.88rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0 0 0.1rem;
  }

  .waitlist-form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  /* Honeypot — must be visually gone but not display:none (some bots check) */
  .hp-field {
    position: absolute;
    left: -9999px;
    width: 1px;
    height: 1px;
    opacity: 0;
    pointer-events: none;
  }

  .waitlist-input-row {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .waitlist-input {
    width: 100%;
    min-width: 0;
    padding: 0.65rem 0.9rem;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 8px;
    color: #f1f5f9;
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
  }
  .waitlist-input::placeholder { color: #64748b; }
  .waitlist-input:focus {
    border-color: rgba(245, 158, 11, 0.5);
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
  }
  .waitlist-input.has-error { border-color: rgba(239, 68, 68, 0.5); }
  .waitlist-input:disabled { opacity: 0.6; cursor: not-allowed; }

  .waitlist-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    width: 100%;
    padding: 0.75rem 1.25rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-weight: 700;
    font-size: 0.88rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: opacity 0.15s ease, transform 0.15s ease;
  }
  .waitlist-btn:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
  .waitlist-btn:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(15, 23, 42, 0.3);
    border-top-color: #0f172a;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Consent checkboxes */
  .consent-prompt {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8;
    margin: 0 0 0.4rem;
  }
  .consent-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem 1.25rem;
  }

  .consent-label {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    color: #94a3b8;
    cursor: pointer;
    user-select: none;
  }

  .consent-label input[type="checkbox"] {
    width: 15px;
    height: 15px;
    accent-color: #f59e0b;
    cursor: pointer;
    flex-shrink: 0;
  }

  .consent-label span { line-height: 1.3; }

  .waitlist-error {
    font-size: 0.82rem;
    color: #f87171;
    margin: 0;
    padding-left: 0.1rem;
  }

  .waitlist-meta {
    font-size: 0.75rem;
    color: #475569;
    margin: 0;
  }
  .book-link {
    color: #f59e0b;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .book-link:hover { opacity: 0.8; }

  .meta-link {
    color: #64748b;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .meta-link:hover { color: #94a3b8; }

  /* Success states */
  .waitlist-success {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1.1rem;
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 10px;
    width: 100%;
  }
  .waitlist-duplicate {
    background: rgba(245, 158, 11, 0.07);
    border-color: rgba(245, 158, 11, 0.25);
  }

  .success-icon {
    font-size: 1.1rem;
    color: #34d399;
    flex-shrink: 0;
    font-weight: 700;
  }
  .waitlist-duplicate .success-icon { color: #f59e0b; }

  .success-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.1rem;
  }
  .success-sub {
    font-size: 0.8rem;
    color: #94a3b8;
    margin: 0;
  }

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
