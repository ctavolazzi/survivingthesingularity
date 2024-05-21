<script>
  import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';

  async function handleBuyBook() {
    try {
      const response = await fetch('/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ priceId: 'price_1PIz8QJ0IdEZ0VwUhLugZtTL' }),
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

<!-- Rest of the Navbar code remains the same -->

<Navbar let:NavContainer color="primary">
  <NavContainer class="border px-5 py-2 rounded-lg bg-white dark:bg-gray-600">
    <NavBrand href="/">
      <img src="/src/images/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
    </NavBrand>
    <NavHamburger />
    <NavUl>
      <NavLi href="/about">About</NavLi>
      <NavLi href="/contact">Contact</NavLi>
      <NavLi href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</NavLi>
      <NavLi href="javascript:void(0);" on:click={handleBuyBook} style="font-weight: bold;">Buy the Book</NavLi>
    </NavUl>
  </NavContainer>
</Navbar>

<style>
  .me-3 {
    margin-right: 1rem;
  }
</style>