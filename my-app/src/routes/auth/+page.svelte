<script>
  import { supabase } from '$lib/supabaseClient';
  import { goto } from '$app/navigation';
  import { Card, Button, Label, Input, Tabs, TabItem, Alert, Spinner } from 'flowbite-svelte';
  import { user } from '$lib/userStore';

  let email = '';
  let password = '';
  let isRegistering = false;
  let errorMessage = '';
  let successMessage = '';
  let isLoading = false;

  async function handleSubmit() {
    if (isRegistering) {
      await registerUser();
    } else {
      await loginUser();
    }
  }

  async function loginUser() {
    isLoading = true;
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) {
      errorMessage = error.message;
    } else {
      user.set(data.user);
      goto('/dashboard');
    }
    isLoading = false;
  }

  async function registerUser() {
    isLoading = true;
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });
    if (error) {
      errorMessage = error.message;
    } else {
      successMessage = 'Registration successful. Please check your email for a confirmation link.';
    }
    isLoading = false;
  }

  function isValidEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
  }

  $: isValidForm = email && password && isValidEmail(email) && password.length >= 6;
 </script>

 <div class="auth-page">
  <Card class="p-8">
    <h2 class="text-3xl font-bold mb-6 text-black">Welcome</h2>
    <Tabs style="underline" color="black" class="mb-6">
      <TabItem title="Login" open={!isRegistering} on:click={() => (isRegistering = false)}>
        Login
      </TabItem>
      <TabItem title="Register" open={isRegistering} on:click={() => (isRegistering = true)}>
        Register
      </TabItem>
    </Tabs>
    {#if errorMessage}
      <Alert color="red" class="mb-6 text-black">
        <span class="font-medium">Error:</span> {errorMessage}
      </Alert>
    {/if}
    {#if successMessage}
      <Alert color="green" class="mb-6 text-black">
        <span class="font-medium">Success:</span> {successMessage}
      </Alert>
    {/if}
    <form on:submit|preventDefault={handleSubmit}>
      <div class="mb-6">
        <Label for="email" class="mb-2 text-black">Email</Label>
        <Input type="email" id="email" bind:value={email} required class="text-black" />
        {#if email && !isValidEmail(email)}
          <p class="text-red-500 text-sm mt-1">Please enter a valid email address.</p>
        {/if}
      </div>
      <div class="mb-6">
        <Label for="password" class="mb-2 text-black">Password</Label>
        <Input type="password" id="password" bind:value={password} required minlength="6" class="text-black" />
        {#if password && password.length < 6}
          <p class="text-red-500 text-sm mt-1">Password must be at least 6 characters long.</p>
        {/if}
      </div>
      <Button type="submit" color="dark" class="w-full" disabled={!isValidForm}>
        {isRegistering ? 'Register' : 'Login'}
      </Button>
    </form>
    <div class="text-center mt-6">
      <a href="/reset-password" class="text-blue-600 hover:underline">Forgot password?</a>
    </div>
    {#if isLoading}
      <div class="flex justify-center mt-6">
        <Spinner color="black" />
      </div>
    {/if}
  </Card>
 </div>

 <style>
  .auth-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
 </style>