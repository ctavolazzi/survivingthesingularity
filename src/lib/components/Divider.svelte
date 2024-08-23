<!-- Divider.svelte -->
<script>
    export let width = '80%';
  </script>
  
  <div class="stylish-divider" style="width: {width};"></div>
  
  <style>
    .stylish-divider {
      height: 1px;
      background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
      margin: 2rem auto;
    }
  
    :global(.dark) .stylish-divider {
      background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
    }
  </style>