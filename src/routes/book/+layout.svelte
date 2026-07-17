<script>
    import { fade } from 'svelte/transition';
    import { page } from '$app/stores';
    import { BOOK_ACCESS_PASSWORD } from '$lib/bookAccessCode.js';

    let password = '';
    let formError = '';
    // Deliberately in-memory only, never persisted to storage: the unlock
    // is meant to reset on any full page load (refresh, closed-and-reopened
    // tab, new tab), not just on demand. Reading position is a separate
    // store (bookPage.js) backed by localStorage, so that keeps surviving
    // a re-lock even though the gate itself doesn't.
    let unlocked = false;

    $: isBookRoot = $page.url.pathname === '/book';

    function submitPassword() {
        formError = '';
        if (password === BOOK_ACCESS_PASSWORD) {
            unlocked = true;
            password = '';
        } else {
            formError = 'Incorrect password.';
        }
    }
</script>

{#if !unlocked}
  <main class="gate-main">
    <form class="gate-form" on:submit|preventDefault={submitPassword}>
      <p class="gate-eyebrow">Surviving the Singularity</p>
      <h1 class="gate-title">This page is locked</h1>
      <p class="gate-sub">Enter the password from your confirmation email to read the book.</p>
      <input
        type="password"
        bind:value={password}
        placeholder="Password"
        autocomplete="off"
        class="gate-input"
      />
      {#if formError}<p class="gate-error">{formError}</p>{/if}
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
{:else if isBookRoot}
  <!-- /book (unlocked): the reader's own layout - preface + table of
       contents, no wrapper needed. -->
  <slot />
{:else}
  <!-- Chapter pages (/book/[sectionId]) get the prose reader layout -->
  <main class="bg-gray-950 text-gray-100 reader-main">
    <div class="reader-container" in:fade="{{ duration: 500 }}">
      <div class="prose prose-lg dark:prose-invert reader-prose">
        <slot />
      </div>
    </div>
  </main>
{/if}

<style>
  .reader-main {
    width: 100%;
    min-height: 60vh;
  }
  .reader-container {
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
    padding: clamp(32px, 5vw, 64px) clamp(20px, 5vw, 40px);
    box-sizing: border-box;
  }
  :global(.reader-prose) {
    max-width: none;
  }
  :global(.toc-link) {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    background: rgba(30, 41, 59, 0.5);
    color: #f1f5f9;
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1rem;
    transition: border-color 150ms ease, background 150ms ease;
  }
  :global(.toc-link:hover) {
    background: rgba(30, 41, 59, 0.8);
    border-color: #f59e0b;
    color: #f59e0b;
  }

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
