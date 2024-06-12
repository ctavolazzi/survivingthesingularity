<!-- src/components/BuyButton.svelte -->
<script>
  export let priceId = 'price_1PJ1TsJ0IdEZ0VwUNRWjALBU';
  export let className = ""; // Accept className prop


  async function handleBuyBook() {
    try {
      const response = await fetch('/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ priceId }),
      });

      const data = await response.json();
      if (data.url) {
        window.location.href = data.url;
      } else {
        throw new Error('Failed to get session URL');
      }
    } catch (err) {
      console.error('Error during payment initiation:', err);
      alert('Payment initiation failed. Please try again.');
    }
  }
</script>

<button class={className} on:click={handleBuyBook}>
  <slot>Buy the Book</slot>
</button>

