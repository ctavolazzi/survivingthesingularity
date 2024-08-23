<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/utils/supabaseClient';
  import { goto } from '$app/navigation';

  let user = null;
  let loading = true;

  onMount(async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (user) {
      // User is authenticated
      console.log('User authenticated:', user);
    } else {
      // No user, redirect to login
      console.log('No user found, redirecting to login');
      goto('/login');
    }
    loading = false;
  });

  async function handleSignOut() {
    const { error } = await supabase.auth.signOut();
    if (error) console.error('Error signing out:', error);
    goto('/login');
  }
</script>

{#if loading}
  <p>Loading...</p>
{:else if user}
  <h1>Welcome to your Dashboard, {user.email}!</h1>
  <p>This is your personal dashboard. You can add more content and features here.</p>
  <button on:click={handleSignOut}>Sign Out</button>
{:else}
  <p>You need to be logged in to view this page. Redirecting...</p>
{/if}

<style>
  h1 {
    color: #333;
    font-size: 2em;
    margin-bottom: 1em;
  }
  button {
    background-color: #f44336;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button:hover {
    background-color: #d32f2f;
  }
</style>