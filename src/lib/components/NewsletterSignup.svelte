<script>
  import { toasts } from '$lib/stores/toasts.js';

  let email = '';
  let loading = false;

  async function handleSubmit() {
    if (!email || !email.includes('@')) {
      toasts.error('Please enter a valid email.');
      return;
    }

    loading = true;
    try {
      // Store in localStorage as fallback (works without Supabase)
      const stored = JSON.parse(localStorage.getItem('sts-newsletter-signups') || '[]');
      if (stored.includes(email)) {
        toasts.info('You\'re already signed up!');
        loading = false;
        return;
      }
      stored.push(email);
      localStorage.setItem('sts-newsletter-signups', JSON.stringify(stored));

      // Try Supabase if available
      try {
        const { createSupabaseBrowserClient } = await import('$lib/supabase.js');
        const supabase = createSupabaseBrowserClient();
        await supabase.from('newsletter_signups').insert({ email });
      } catch {
        // Supabase not available or table doesn't exist — localStorage fallback is fine
      }

      toasts.success('You\'re in! We\'ll keep you posted.');
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
      placeholder="builder@example.com"
      class="newsletter-input"
      disabled={loading}
    />
    <button type="submit" class="newsletter-btn" disabled={loading}>
      {loading ? 'Joining...' : 'Join the Build'}
    </button>
  </div>
  <p class="newsletter-note">No spam. Unsubscribe anytime. We respect your sovereignty.</p>
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
