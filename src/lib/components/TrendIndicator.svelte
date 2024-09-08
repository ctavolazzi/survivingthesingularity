<script>
    export let value = 0;
  
    $: isPositive = value > 0;
    $: absValue = Math.abs(value);
  </script>
  
  <span class="inline-flex items-center px-2 py-1 rounded text-sm {isPositive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
    {#if isPositive}
      <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
      </svg>
    {:else}
      <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
    {/if}
    {absValue}%
  </span>