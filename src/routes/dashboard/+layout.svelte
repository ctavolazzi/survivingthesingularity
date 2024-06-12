<!-- src/routes/dashboard/+layout.svelte -->
<script>
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import { goto } from '$app/navigation';
  import { user } from '$lib/userStore';

  onMount(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (session) {
        user.set(session.user);
      } else {
        user.set(null);
        goto('/auth');
      }
    });

    return () => {
      subscription.unsubscribe();
    };
  });
</script>

{#if $user}
  <slot />
{:else}
  <p>Loading...</p>
{/if}