<script lang="ts">
  import { enhance } from '$app/forms';
  import { user } from '$lib/stores/userStore';
  import Avatar from './Avatar.svelte';
  import { supabase } from '$lib/utils/supabaseClient';

  export let data;

  let { session, profile } = data;
  $: ({ session, profile } = data);

  let loading = false;
  let message = '';

  const handleSubmit = () => {
    loading = true;
    message = '';
    return async ({ result }) => {
      loading = false;
      if (result.type === 'success') {
        message = 'Profile updated successfully!';
      } else {
        message = 'Error updating profile. Please try again.';
      }
    };
  };
</script>

<div class="user-profile">
  <h2>User Profile</h2>

  <form method="POST" action="?/update" use:enhance={handleSubmit}>
    <Avatar 
      bind:url={profile.avatar_url} 
      size={10} 
      on:upload={() => {
        message = 'Avatar updated. Save profile to confirm changes.';
      }} 
    />

    <div class="form-field">
      <label for="email">Email</label>
      <input id="email" type="email" value={session.user.email} disabled />
    </div>

    <div class="form-field">
      <label for="firstName">First Name</label>
      <input id="firstName" name="firstName" type="text" value={profile.first_name || ''} />
    </div>

    <div class="form-field">
      <label for="lastName">Last Name</label>
      <input id="lastName" name="lastName" type="text" value={profile.last_name || ''} />
    </div>

    <div class="form-field">
      <label for="website">Website</label>
      <input id="website" name="website" type="url" value={profile.website || ''} />
    </div>

    {#if message}
      <p class="message">{message}</p>
    {/if}

    <button type="submit" class="button primary" disabled={loading}>
      {loading ? 'Saving...' : 'Update Profile'}
    </button>
  </form>

  <form method="POST" action="?/signout" use:enhance={() => {
    loading = true;
    return async () => {
      loading = false;
      user.set(null);
    };
  }}>
    <button type="submit" class="button secondary" disabled={loading}>
      Sign Out
    </button>
  </form>
</div>

<style>
  .user-profile {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
  }
  .form-field {
    margin-bottom: 15px;
  }
  label {
    display: block;
    margin-bottom: 5px;
  }
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .button {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .primary {
    background-color: #4CAF50;
    color: white;
  }
  .secondary {
    background-color: #f44336;
    color: white;
    margin-top: 10px;
  }
  .message {
    margin-top: 10px;
    padding: 10px;
    background-color: #dff0d8;
    border: 1px solid #d6e9c6;
    color: #3c763d;
    border-radius: 4px;
  }
</style>