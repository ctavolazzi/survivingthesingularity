<script>
  import { supabase } from '$lib/supabaseClient';
  import { user } from '$lib/userStore';
  import { Card, Button, Label, Input, Alert, Avatar, Spinner } from 'flowbite-svelte';

  export let data;
  let { profile } = data;

  let username = profile?.username || '';
  let fullName = profile?.full_name || '';
  let bio = profile?.bio || '';
  let avatarUrl = profile?.avatar_url || 'https://i.pravatar.cc/150?img=3';
  let email = $user?.email || '';

  let successMessage = '';
  let errorMessage = '';
  let loading = false;

  async function handleUpdateProfile() {
    loading = true;
    const { data: updatedProfile, error } = await supabase
      .from('profiles')
      .update({ username, full_name: fullName, bio, avatar_url: avatarUrl })
      .eq('id', $user.id)
      .single();

    if (error) {
      errorMessage = error.message;
    } else {
      profile = updatedProfile;
      successMessage = 'Profile updated successfully.';
      setTimeout(() => {
        successMessage = '';
      }, 3000);
    }
    loading = false;
  }
</script>

<div class="profile-page">
  <Card>
    <div class="flex justify-center mb-6">
      <Avatar src={avatarUrl} size="xl" />
    </div>
    <h2 class="text-2xl font-bold mb-4 text-center">{username}'s Profile</h2>
    {#if successMessage}
      <Alert color="green" class="mb-4">
        <span class="font-medium">Success:</span> {successMessage}
      </Alert>
    {:else if errorMessage}
      <Alert color="red" class="mb-4">
        <span class="font-medium">Error:</span> {errorMessage}
      </Alert>
    {/if}
    <form on:submit|preventDefault={handleUpdateProfile}>
      <div class="mb-6">
        <Label for="username" class="mb-2">Username</Label>
        <Input type="text" id="username" bind:value={username} required />
      </div>
      <div class="mb-6">
        <Label for="fullName" class="mb-2">Full Name</Label>
        <Input type="text" id="fullName" bind:value={fullName} />
      </div>
      <div class="mb-6">
        <Label for="email" class="mb-2">Email</Label>
        <Input type="email" id="email" bind:value={email} disabled />
      </div>
      <div class="mb-6">
        <Label for="bio" class="mb-2">Bio</Label>
        <Input type="text" id="bio" bind:value={bio} />
      </div>
      <div class="mb-6">
        <Label for="avatarUrl" class="mb-2">Avatar URL</Label>
        <Input type="url" id="avatarUrl" bind:value={avatarUrl} />
      </div>
      <Button type="submit" color="black" class="w-full" disabled={loading}>
        {#if loading}
          <Spinner class="mr-3" size="4" color="white" />
        {/if}
        Update Profile
      </Button>
    </form>
  </Card>
</div>

<style>
  .profile-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>