<script>
  import { toasts } from '$lib/stores/toasts.js';

  // Optional props for reusing this component in multiple contexts (e.g. /book preorder).
  // Defaults preserve original behavior so existing usages don't break.
  export let source = 'general';
  export let cta = 'Join the Build';
  export let loadingCta = 'Joining...';
  export let placeholder = 'builder@example.com';
  export let successMessage = "You're in! We'll keep you posted.";
  export let alreadyMessage = "You're already signed up!";
  export let note = 'No spam. Unsubscribe anytime. We respect your sovereignty.';

  let email = '';
  let loading = false;

  async function handleSubmit() {
    if (!email || !email.includes('@')) {
      toasts.error('Please enter a valid email.');
      return;
    }

    loading = true;
    try {
      // Store in localStorage as fallback (works without Supabase). Key includes
      // source so a user signed up to one CTA can still sign up to another.
      const storageKey = source === 'general' ? 'sts-newsletter-signups' : `sts-newsletter-signups-${source}`;
      const stored = JSON.parse(localStorage.getItem(storageKey) || '[]');
      if (stored.includes(email)) {
        toasts.info(alreadyMessage);
        loading = false;
        return;
      }
      stored.push(email);
      localStorage.setItem(storageKey, JSON.stringify(stored));

      // Try Supabase if available. Insert with source for filtering;
      // if the column doesn't exist, the call falls back to {email} only.
      try {
        const { createSupabaseBrowserClient } = await import('$lib/supabase.js');
        const supabase = createSupabaseBrowserClient();
        const { error } = await supabase.from('newsletter_signups').insert({ email, source });
        if (error && error.message && /column.*source/i.test(error.message)) {
          // Column missing - retry without source so signups still land.
          await supabase.from('newsletter_signups').insert({ email });
        }
      } catch {
        // Supabase not available - localStorage fallback is fine
      }

      toasts.success(successMessage);
      email = '';
    } catch (err) {
      toasts.error('Something went wrong. Try again.');
    } finally {
      loading = false;
    }
  }
</script>

<form class="newsletter-form" on:submit|preventDefault={handleSubmit}>
  <div class="newsletter-input-group">
    <input
      type="email"
      bind:value={email}
      {placeholder}
      class="newsletter-input"
      disabled={loading}
    />
    <button type="submit" class="newsletter-btn" disabled={loading}>
      {loading ? loadingCta : cta}
    </button>
  </div>
  {#if note}
    <p class="newsletter-note">{note}</p>
  {/if}
</form>

<style>
  .newsletter-form {
    max-width: 480px;
  }

  .newsletter-input-group {
    display: flex;
    gap: 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.12);
    background: rgba(15, 23, 42, 0.5);
    transition: border-color 0.2s;
  }

  .newsletter-input-group:focus-within {
    border-color: rgba(245, 158, 11, 0.4);
  }

  .newsletter-input {
    flex: 1;
    padding: 0.85rem 1rem;
    background: transparent;
    border: none;
    color: #f1f5f9;
    font-size: 0.95rem;
    font-family: inherit;
    outline: none;
    min-width: 0;
  }

  .newsletter-input::placeholder {
    color: #475569;
  }

  .newsletter-btn {
    padding: 0.85rem 1.5rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-weight: 600;
    font-size: 0.88rem;
    border: none;
    cursor: pointer;
    font-family: inherit;
    white-space: nowrap;
    transition: all 0.2s;
  }

  .newsletter-btn:hover:not(:disabled) {
    filter: brightness(1.1);
  }

  .newsletter-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .newsletter-note {
    font-size: 0.72rem;
    color: #475569;
    margin: 0.5rem 0 0 0;
  }

  @media (max-width: 480px) {
    .newsletter-input-group {
      flex-direction: column;
      border-radius: 12px;
    }

    .newsletter-btn {
      border-radius: 0 0 11px 11px;
    }
  }
</style>
