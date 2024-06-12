<script>
  import { supabase } from '$lib/supabaseClient';
  import { Card, Button, Label, Input, Alert } from 'flowbite-svelte';

  let email = '';
  let successMessage = '';
  let errorMessage = '';
  let isLoading = false;

  async function handleResetPassword() {
    isLoading = true;
    const { data, error } = await supabase.auth.resetPasswordForEmail(email);

    if (error) {
      errorMessage = error.message;
    } else {
      successMessage = 'Password reset email sent. Please check your inbox.';
    }
    isLoading = false;
  }
</script>

<div class="reset-password-page">
  <Card class="p-8">
    <h2 class="text-3xl font-bold mb-6 text-black">Reset Password</h2>
    {#if successMessage}
      <Alert color="green" class="mb-6 text-black">
        <span class="font-medium">Success:</span> {successMessage}
      </Alert>
    {:else}
      {#if errorMessage}
        <Alert color="red" class="mb-6 text-black">
          <span class="font-medium">Error:</span> {errorMessage}
        </Alert>
      {/if}
      <form on:submit|preventDefault={handleResetPassword}>
        <div class="mb-6">
          <Label for="email" class="mb-2 text-black">Email</Label>
          <Input type="email" id="email" bind:value={email} required class="text-black" />
        </div>
        <Button type="submit" color="dark" class="w-full" disabled={isLoading}>
          {#if isLoading}
            <span class="animate-spin mr-2">&#9696;</span>
          {/if}
          Reset Password
        </Button>
      </form>
    {/if}
  </Card>
</div>

<style>
  .reset-password-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>