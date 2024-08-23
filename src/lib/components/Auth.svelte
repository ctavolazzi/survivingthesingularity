<script lang="ts">
  import { enhance } from '$app/forms';
  export let form;
  let loading = false;
  let isLogin = true;

  const handleSubmit = () => {
    loading = true;
    return async ({ update }) => {
      update();
      loading = false;
    };
  };
</script>

<form class="auth-form" method="POST" use:enhance={handleSubmit}>
  <h2>{isLogin ? 'Login' : 'Register'}</h2>
  {#if form?.message}
    <div class="message {form.success ? 'success' : 'error'}">{form.message}</div>
  {/if}
  <input name="email" type="email" placeholder="Email" required />
  <input name="password" type="password" placeholder="Password" required />
  {#if !isLogin}
    <input name="firstName" type="text" placeholder="First Name" />
    <input name="lastName" type="text" placeholder="Last Name" />
  {/if}
  <button type="submit" disabled={loading}>
    {loading ? 'Processing...' : isLogin ? 'Login' : 'Register'}
  </button>
  <p>
    {isLogin ? "Don't have an account?" : "Already have an account?"}
    <a href="#" on:click|preventDefault={() => (isLogin = !isLogin)}>
      {isLogin ? 'Register' : 'Login'}
    </a>
  </p>
</form>

<style>
  /* Add styles for the auth form */
</style>
