<script>
    import { inview } from 'svelte-inview';
  
    export let options = {
      unobserveOnEnter: true,
      rootMargin: '-20%',
    };
  
    let isInView = false;
  </script>
  
  <div use:inview={options} on:inview_enter={() => { isInView = true; }} on:inview_leave={() => { isInView = false; }}>
    {#if isInView}
      <slot></slot>
    {/if}
  </div>