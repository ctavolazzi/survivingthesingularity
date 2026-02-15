<script>
  import { createSupabaseBrowserClient } from '$lib/supabase.js';
  import { goto } from '$app/navigation';
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';

  let mode = 'login'; // 'login' | 'signup' | 'forgot'
  let email = '';
  let password = '';
  let loading = false;
  let message = '';
  let messageType = ''; // 'success' | 'error'
  let visible = false;

  onMount(() => { visible = true; });

  async function handleSubmit() {
    loading = true;
    message = '';

    try {
      const supabase = createSupabaseBrowserClient();

      if (mode === 'login') {
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
        goto('/profile');
      } else if (mode === 'signup') {
        const { error } = await supabase.auth.signUp({
          email,
          password,
          options: {
            emailRedirectTo: `${window.location.origin}/auth/callback`,
          },
        });
        if (error) throw error;
        message = 'Check your email for a confirmation link.';
        messageType = 'success';
      } else if (mode === 'forgot') {
        const { error } = await supabase.auth.resetPasswordForEmail(email, {
          redirectTo: `${window.location.origin}/auth/callback`,
        });
        if (error) throw error;
        message = 'Password reset link sent to your email.';
        messageType = 'success';
      }
    } catch (err) {
      message = err.message || 'Something went wrong.';
      messageType = 'error';
    } finally {
      loading = false;
    }
  }

  async function handleOAuth(provider) {
    loading = true;
    try {
      const supabase = createSupabaseBrowserClient();
      const { error } = await supabase.auth.signInWithOAuth({
        provider,
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      if (error) throw error;
    } catch (err) {
      message = err.message || 'OAuth failed.';
      messageType = 'error';
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>{mode === 'signup' ? 'Sign Up' : mode === 'forgot' ? 'Reset Password' : 'Sign In'} — Surviving the Singularity</title>
</svelte:head>

{#if visible}
  <div class="auth-page" in:fade={{ duration: 400 }}>
    <div class="auth-card">
      <div class="auth-header">
        <span class="auth-mark">STS</span>
        <h1 class="auth-title">
          {#if mode === 'login'}Sign in to your account
          {:else if mode === 'signup'}Create your account
          {:else}Reset your password
          {/if}
        </h1>
        <p class="auth-subtitle">
          {#if mode === 'login'}Track your blueprint progress and save your work.
          {:else if mode === 'signup'}Join the builder community. Free forever.
          {:else}We'll send a reset link to your email.
          {/if}
        </p>
      </div>

      {#if message}
        <div class="auth-message" class:success={messageType === 'success'} class:error={messageType === 'error'}>
          {message}
        </div>
      {/if}

      <form on:submit|preventDefault={handleSubmit} class="auth-form">
        <div class="form-field">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            type="email"
            bind:value={email}
            required
            placeholder="you@example.com"
            class="form-input"
            autocomplete="email"
          />
        </div>

        {#if mode !== 'forgot'}
          <div class="form-field">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              type="password"
              bind:value={password}
              required
              placeholder="Min. 6 characters"
              class="form-input"
              minlength="6"
              autocomplete={mode === 'signup' ? 'new-password' : 'current-password'}
            />
          </div>
        {/if}

        <button type="submit" class="auth-submit" disabled={loading}>
          {#if loading}
            <span class="spinner"></span>
          {:else}
            {mode === 'login' ? 'Sign In' : mode === 'signup' ? 'Create Account' : 'Send Reset Link'}
          {/if}
        </button>
      </form>

      {#if mode !== 'forgot'}
        <div class="auth-divider">
          <span>or continue with</span>
        </div>

        <div class="oauth-buttons">
          <button class="oauth-btn" on:click={() => handleOAuth('github')} disabled={loading}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            GitHub
          </button>
          <button class="oauth-btn" on:click={() => handleOAuth('google')} disabled={loading}>
            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            Google
          </button>
        </div>
      {/if}

      <div class="auth-switch">
        {#if mode === 'login'}
          <button class="switch-btn" on:click={() => { mode = 'forgot'; message = ''; }}>Forgot password?</button>
          <span class="switch-divider">&middot;</span>
          <button class="switch-btn" on:click={() => { mode = 'signup'; message = ''; }}>Create account</button>
        {:else if mode === 'signup'}
          <span class="switch-text">Already have an account?</span>
          <button class="switch-btn" on:click={() => { mode = 'login'; message = ''; }}>Sign in</button>
        {:else}
          <button class="switch-btn" on:click={() => { mode = 'login'; message = ''; }}>Back to sign in</button>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .auth-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    padding: 2rem 1rem;
  }

  .auth-card {
    width: 100%;
    max-width: 420px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 20px;
    padding: 2.5rem;
  }

  .auth-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .auth-mark {
    font-size: 0.85rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
  }

  .auth-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0.75rem 0 0.5rem;
  }

  .auth-subtitle {
    font-size: 0.9rem;
    color: #64748b;
    margin: 0;
  }

  .auth-message {
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-size: 0.85rem;
    margin-bottom: 1.25rem;
    text-align: center;
  }

  .auth-message.success {
    background: rgba(16, 185, 129, 0.1);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.2);
  }

  .auth-message.error {
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.2);
  }

  .auth-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .form-field {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .form-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .form-input {
    padding: 0.75rem 1rem;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 10px;
    color: #f1f5f9;
    font-size: 0.95rem;
    font-family: inherit;
    transition: border-color 0.2s;
    outline: none;
  }

  .form-input::placeholder {
    color: #475569;
  }

  .form-input:focus {
    border-color: rgba(245, 158, 11, 0.4);
  }

  .auth-submit {
    padding: 0.85rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    font-weight: 700;
    font-size: 0.95rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }

  .auth-submit:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
  }

  .auth-submit:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .spinner {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(15, 23, 42, 0.3);
    border-top-color: #0f172a;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .auth-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.5rem 0;
    color: #475569;
    font-size: 0.8rem;
  }

  .auth-divider::before,
  .auth-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(148, 163, 184, 0.1);
  }

  .oauth-buttons {
    display: flex;
    gap: 0.75rem;
  }

  .oauth-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.7rem;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 10px;
    color: #cbd5e1;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
  }

  .oauth-btn:hover:not(:disabled) {
    background: rgba(30, 41, 59, 0.8);
    border-color: rgba(148, 163, 184, 0.2);
  }

  .auth-switch {
    text-align: center;
    margin-top: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .switch-text {
    font-size: 0.85rem;
    color: #64748b;
  }

  .switch-btn {
    font-size: 0.85rem;
    color: #f59e0b;
    background: none;
    border: none;
    cursor: pointer;
    font-family: inherit;
    padding: 0;
    transition: color 0.2s;
  }

  .switch-btn:hover {
    color: #fbbf24;
  }

  .switch-divider {
    color: #334155;
  }

  @media (max-width: 480px) {
    .auth-card {
      padding: 2rem 1.5rem;
      border-radius: 16px;
    }
  }
</style>
