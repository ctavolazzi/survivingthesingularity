<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { browser } from '$app/environment';

  const dispatch = createEventDispatcher();

  /**
   * Soft email gate. Renders the default slot (teaser) always; renders the
   * "gated" slot only after the visitor unlocks with their email. Unlock is
   * persisted in localStorage so returning visitors aren't re-gated.
   *
   * Usage:
   *   <EmailGate storageKey="checklist" source="checklist" headline="...">
   *     <div slot="default">...teaser always visible...</div>
   *     <div slot="gated">...revealed after unlock...</div>
   *   </EmailGate>
   */
  export let storageKey;                 // unique per gated asset
  export let source = 'gate';            // waitlist source tag
  export let headline = 'Unlock the rest';
  export let sub = 'Enter your email and the full version opens right here.';
  export let buttonText = 'Unlock Free';

  const LS_KEY = `sts_unlock_${storageKey}`;

  let unlocked = false;
  let email = '';
  let subscribe = false; // opt-in: unchecked. Email still captured to unlock.
  let honeypot = '';
  let state = 'idle'; // idle | loading | error
  let errorMsg = '';

  onMount(() => {
    if (browser && localStorage.getItem(LS_KEY)) {
      unlocked = true;
      dispatch('unlock');
    }
  });

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
          newsletter_consent: subscribe,
          book_release_consent: subscribe,
          _hp: honeypot,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.status === 201 || res.status === 409) {
        if (browser) localStorage.setItem(LS_KEY, '1');
        unlocked = true; // reveal
        dispatch('unlock');
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

<!-- Always-visible teaser -->
<slot />

{#if unlocked}
  <div class="gate-reveal">
    <slot name="gated" />
  </div>
{:else}
  <div class="gate">
    <div class="gate-fade" aria-hidden="true"></div>
    <div class="gate-card">
      <div class="gate-lock" aria-hidden="true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
      </div>
      <p class="gate-headline">{headline}</p>
      <p class="gate-sub">{sub}</p>

      <form class="gate-form" on:submit={submit} novalidate>
        <input
          class="hp-field"
          type="text"
          bind:value={honeypot}
          tabindex="-1"
          autocomplete="off"
          aria-hidden="true"
        />
        <input
          class="gate-input"
          type="email"
          bind:value={email}
          placeholder="your@email.com"
          required
          autocomplete="email"
          maxlength="254"
          disabled={state === 'loading'}
          aria-label="Email address"
        />
        <button class="gate-btn" type="submit" disabled={state === 'loading' || !email}>
          {#if state === 'loading'}Unlocking…{:else}{buttonText}{/if}
        </button>
      </form>

      <label class="gate-consent">
        <input type="checkbox" bind:checked={subscribe} />
        <span>Email me when the book drops + occasional updates</span>
      </label>

      {#if state === 'error'}
        <p class="gate-err" role="alert">{errorMsg}</p>
      {/if}
      <p class="gate-meta">Instant access to the checklist. Unsubscribe anytime. <a href="/policies">Privacy</a>.</p>
    </div>
  </div>
{/if}

<style>
  .gate {
    position: relative;
    margin-top: -3.5rem; /* pull fade up over the tail of the teaser */
    padding-top: 3.5rem;
  }

  .gate-fade {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3.5rem;
    background: linear-gradient(180deg, rgba(2, 6, 23, 0) 0%, #020617 100%);
    pointer-events: none;
  }

  .gate-card {
    position: relative;
    text-align: center;
    max-width: 460px;
    margin: 0 auto;
    padding: 1.75rem 1.5rem 1.5rem;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-left: 3px solid rgba(245, 158, 11, 0.5);
    border-radius: 0;
    box-shadow: 4px 4px 0 rgba(245, 158, 11, 0.12);
  }

  .gate-lock {
    width: 44px;
    height: 44px;
    margin: 0 auto 0.85rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 0;
  }

  .gate-headline {
    font-size: 1.2rem;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 0.4rem;
    letter-spacing: -0.01em;
  }

  .gate-sub {
    font-size: 0.92rem;
    color: #94a3b8;
    margin: 0 0 1.25rem;
    line-height: 1.5;
  }

  .gate-form {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .hp-field {
    position: absolute;
    left: -9999px;
    width: 1px;
    height: 1px;
    opacity: 0;
    pointer-events: none;
  }

  .gate-input {
    flex: 1;
    min-width: 0;
    padding: 0.7rem 0.9rem;
    background: rgba(2, 6, 23, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 0;
    color: #f1f5f9;
    font-size: 0.92rem;
    outline: none;
    transition: border-color 0.15s ease;
  }
  .gate-input::placeholder { color: #64748b; }
  .gate-input:focus {
    border-color: rgba(245, 158, 11, 0.6);
  }

  .gate-btn {
    flex-shrink: 0;
    padding: 0.7rem 1.3rem;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 800;
    font-size: 0.9rem;
    border: none;
    border-radius: 0;
    cursor: pointer;
    white-space: nowrap;
    box-shadow: 3px 3px 0 rgba(120, 53, 15, 0.4);
    transition: opacity 0.15s ease, transform 0.15s ease;
  }
  .gate-btn:hover:not(:disabled) { opacity: 0.92; transform: translateY(-1px); }
  .gate-btn:disabled { opacity: 0.55; cursor: not-allowed; }

  .gate-consent {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    text-align: left;
    font-size: 0.82rem;
    color: #94a3b8;
    margin: 0 0 0.75rem;
    cursor: pointer;
    user-select: none;
  }
  .gate-consent input[type="checkbox"] {
    width: 15px;
    height: 15px;
    margin-top: 1px;
    accent-color: #f59e0b;
    cursor: pointer;
    flex-shrink: 0;
  }

  .gate-err { color: #f87171; font-size: 0.84rem; margin: 0 0 0.4rem; }

  .gate-meta {
    font-size: 0.76rem;
    color: #64748b;
    margin: 0;
  }
  .gate-meta a { color: #94a3b8; text-decoration: underline; text-underline-offset: 2px; }

  .gate-reveal {
    animation: gate-in 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes gate-in {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  @media (max-width: 480px) {
    .gate-form { flex-direction: column; }
    .gate-btn { width: 100%; }
  }
  @media (prefers-reduced-motion: reduce) {
    .gate-reveal { animation: none; }
  }
</style>
