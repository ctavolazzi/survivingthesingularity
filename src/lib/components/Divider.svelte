<!-- Divider.svelte -->
<script>
    export let width = '90%';
    export let color = 'gradient'; // 'gradient', 'orange', or 'light'
</script>

<div class="stylish-divider {color}" style="width: {width};"></div>

<style>
  .stylish-divider {
    height: 2px;
    margin: 3rem auto;
    position: relative;
    border-radius: 1px;
  }

  .stylish-divider.gradient {
    background-image: linear-gradient(to right,
      rgba(0, 0, 0, 0),
      rgba(255, 153, 51, 0.7),
      rgba(0, 0, 0, 0)
    );
  }

  .stylish-divider.orange {
    background-color: rgba(255, 153, 51, 0.4);
  }

  .stylish-divider.light {
    background-color: rgba(255, 255, 255, 0.1);
  }

  :global(.dark) .stylish-divider.gradient {
    background-image: linear-gradient(to right,
      rgba(0, 0, 0, 0),
      rgba(255, 153, 51, 0.7),
      rgba(0, 0, 0, 0)
    );
  }

  :global(.dark) .stylish-divider.orange {
    background-color: rgba(255, 153, 51, 0.3);
  }

  :global(.dark) .stylish-divider.light {
    background-color: rgba(255, 255, 255, 0.05);
  }
</style>