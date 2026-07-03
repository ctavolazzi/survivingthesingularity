<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import { invalidateAll } from '$app/navigation';
    import Spacer from '$lib/components/Spacer.svelte';
    import SimpleBookCallout from '$lib/components/SimpleBookCallout.svelte';
    import { page } from '$app/stores';

    export let data;

    let showLowerSections = false;
    let password = '';
    let submitting = false;
    let formError = '';

    $: isBookRoot = $page.url.pathname === '/book';

    onMount(() => {
        setTimeout(() => {
            showLowerSections = true;
        }, 1000);
    });

    async function submitPassword() {
        if (submitting) return;
        submitting = true;
        formError = '';
        try {
            const res = await fetch('/api/verify-book-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });
            const body = await res.json().catch(() => ({}));
            if (!res.ok) {
                formError = body.error || 'Incorrect password.';
                return;
            }
            password = '';
            await invalidateAll();
        } catch {
            formError = 'Something went wrong. Try again.';
        } finally {
            submitting = false;
        }
    }
</script>

{#if !data.unlocked}
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
        disabled={submitting}
      />
      {#if formError}<p class="gate-error">{formError}</p>{/if}
      <button type="submit" class="gate-submit" disabled={submitting || !password}>
        {submitting ? 'Checking…' : 'Unlock'}
      </button>
      <p class="gate-hint">Don't have a password yet? Click "Get Early Access" above to get your code.</p>
    </form>
  </main>
{:else if isBookRoot}
  <!-- Main /book page has its own full-width layout — no wrapper needed -->
  <slot />
{:else}
  <!-- Section sub-pages (/book/[sectionId]) need the prose reader layout -->
  <main class="bg-gray-950 text-gray-100 reader-main">
    <div class="reader-container" in:fade="{{ duration: 500 }}">
      <div class="prose prose-lg dark:prose-invert reader-prose">
        <slot />
      </div>

      {#if showLowerSections}
        <Spacer height="48px" />
        <SimpleBookCallout
          title="Navigate the Path to Singularity"
          description="Get the insights and strategies you need to prepare for the technological changes that will reshape our world."
          buttonText="Explore the Book"
          buttonLink="/book"
        />
      {/if}
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
</style>
