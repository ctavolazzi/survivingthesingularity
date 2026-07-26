<script>
  // The password gate in front of the book. Shared by /book and /read so both
  // doors take the same keys and clearing one clears the other.
  //
  // Pure client-side check (see $lib/bookAccessCode.js) - no server env var to
  // misconfigure across environments. The unlock lives in an in-memory store,
  // never persisted, so it resets on any full page load: refresh, new tab,
  // closed-and-reopened tab. Reading position is stored separately, so a
  // re-lock never costs anyone their place.
  import { isValidBookPassword } from '$lib/bookAccessCode.js';
  import { bookUnlocked } from '$lib/stores/bookAccess.js';

  /** Line under the title. Each surface says why you'd have a password. */
  export let subtitle = 'Enter the password from your confirmation email to read the book.';

  let password = '';
  let formError = '';

  function submitPassword() {
    formError = '';
    if (isValidBookPassword(password)) {
      bookUnlocked.set(true);
      password = '';
    } else {
      formError = 'Incorrect password.';
    }
  }
</script>

<main class="gate-main">
  <form class="gate-form" on:submit|preventDefault={submitPassword}>
    <p class="gate-eyebrow">Surviving the Singularity</p>
    <h1 class="gate-title">This page is locked</h1>
    <p class="gate-sub">{subtitle}</p>
    <input
      type="password"
      bind:value={password}
      placeholder="Password"
      autocomplete="off"
      autocapitalize="off"
      spellcheck="false"
      class="gate-input"
    />
    {#if formError}<p class="gate-error" role="alert">{formError}</p>{/if}
    <button type="submit" class="gate-submit" disabled={!password}>
      Unlock
    </button>
    <p class="gate-hint">
      Don't have a password yet?
      <a href="/early-access" class="gate-hint-link">Preorder for $5</a>
      and your code arrives by email.
    </p>
  </form>
</main>

<style>
  .gate-main {
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: clamp(32px, 6vw, 64px) 20px;
  }
  .gate-form {
    width: 100%;
    max-width: 360px;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    text-align: center;
  }
  .gate-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #f59e0b;
    margin: 0;
  }
  .gate-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0;
  }
  .gate-sub {
    font-size: 0.9rem;
    color: #94a3b8;
    margin: 0 0 0.5rem;
  }
  .gate-input {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    background: rgba(30, 41, 59, 0.5);
    color: #f1f5f9;
    font-size: 1rem;
    min-height: 44px;
  }
  .gate-error {
    color: #f87171;
    font-size: 0.85rem;
    margin: 0;
  }
  .gate-submit {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: none;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 700;
    cursor: pointer;
    min-height: 44px;
  }
  .gate-submit:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .gate-hint {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0.5rem 0 0;
  }
  .gate-hint-link {
    color: #f59e0b;
    font-weight: 600;
    text-decoration: underline;
    text-underline-offset: 2px;
    /* Inline link in a sentence: grow the touch target invisibly. */
    display: inline-block;
    padding: 0.35rem 0.2rem;
    margin: -0.35rem -0.2rem;
  }
  .gate-hint-link:hover { color: #fbbf24; }
</style>
