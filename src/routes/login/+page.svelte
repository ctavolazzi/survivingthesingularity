<script>
  import { supabase } from '$lib/utils/supabaseClient';
  import { goto } from '$app/navigation';
  import { darkMode } from '$lib/stores/darkMode';
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';

  let email = '';
  let password = '';
  let loading = false;
  /** @type {string|null} */
  let error = null;
  let signUpAttempts = 0;
  let lastSignUpAttemptTime = 0;
  const SIGN_UP_RATE_LIMIT_DELAY = 5000;
  const MAX_SIGN_UP_ATTEMPTS = 4;
  let isLoginMode = true;

  $: isFormValid = email.trim() && password.trim();

  onMount(() => {
    // Check if user is already logged in
    supabase.auth.getUser().then(({ data: { user } }) => {
      if (user) goto('/');
    });
  });

  /**
   * @param {boolean} isLogin
   */
  async function handleAuth(isLogin) {
    if (!email || !password) return;

    loading = true;
    error = null;

    try {
      if (isLogin) {
        const { data, error: authError } = await supabase.auth.signInWithPassword({ email, password });
        if (authError) throw authError;
        if (data.user) goto('/dashboard');
      } else {
        // Sign up process
        const { data, error: signUpError } = await supabase.auth.signUp({ 
          email, 
          password,
          options: {
            data: {
              email: email
            }
          }
        });
        
        if (signUpError) throw signUpError;
        
        if (data.user) {
          // User is created in auth system, now add to 'users' table
          const { error: insertError } = await supabase
            .from('users')
            .insert({ id: data.user.id, email: data.user.email });
          
          if (insertError) {
            console.error('Error inserting user into users table:', insertError);
            throw new Error('Failed to create user profile');
          }

          // Check if email confirmation is required
          if (data.user.confirmed_at) {
            // Email is confirmed, redirect to dashboard
            goto('/dashboard');
          } else {
            // Email confirmation required
            error = "Please check your email for the confirmation link.";
          }
        } else {
          throw new Error('Failed to create user');
        }
      }
    } catch (e) {
      error = e.message;
      console.error('Auth error:', e);
    } finally {
      loading = false;
    }
  }

  /**
   * @param {KeyboardEvent} event
   */
  function handleKeydown(event) {
    if (event.key === 'Enter' && !loading && isFormValid) {
      handleAuth(isLoginMode);
    }
  }

  function toggleMode() {
    isLoginMode = !isLoginMode;
    error = null;
  }
</script>

<svelte:head>
  <title>Login - Surviving the Singularity</title>
</svelte:head>

<div class="flex justify-center items-center min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300">
  <div class="w-full max-w-md p-8 bg-white dark:bg-gray-800 rounded-lg shadow-md transition-colors duration-300">
    <h2 class="text-3xl font-bold mb-6 text-center text-gray-900 dark:text-white">
      {isLoginMode ? 'Login' : 'Sign Up'}
    </h2>
    <form on:submit|preventDefault={() => handleAuth(isLoginMode)} class="space-y-6">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
        <input 
          id="email" 
          type="email" 
          bind:value={email} 
          required 
          class="mt-1 block w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
          on:keydown={handleKeydown}
        />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
        <input 
          id="password" 
          type="password" 
          bind:value={password} 
          required 
          class="mt-1 block w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
          on:keydown={handleKeydown}
        />
      </div>
      <div class="flex flex-col space-y-4">
        <button 
          type="submit" 
          class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-offset-gray-800 transition-colors duration-300" 
          disabled={loading || !isFormValid}
        >
          {loading ? 'Processing...' : (isLoginMode ? 'Login' : 'Sign Up')}
        </button>
      </div>
    </form>
    <p class="mt-4 text-sm text-center">
      {isLoginMode ? "Don't have an account?" : "Already have an account?"}
      <button 
        on:click={toggleMode}
        class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
      >
        {isLoginMode ? 'Sign up' : 'Log in'}
      </button>
    </p>
    {#if error}
      <p class="mt-4 text-sm text-red-600 dark:text-red-400" transition:fade>{error}</p>
    {/if}
  </div>
</div>