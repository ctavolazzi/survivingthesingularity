<!-- src/components/BackBookButton.svelte -->
<script>
  import { supabase } from '$lib/supabaseClient';

  export let className = ""; // Accept className prop

  async function handleBackBook() {
    // Log the button click to the database
    supabase.from('back_book_clicks').insert({
      timestamp: new Date(),
      referrer: document.referrer,
      user_agent: navigator.userAgent,
    });

    // Open the Kickstarter campaign in a new tab
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
  }
</script>

<button class:className={className} on:click={handleBackBook}>
  <slot>Back the Book</slot>
</button>