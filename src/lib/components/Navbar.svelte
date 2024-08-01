<script>
  import { Navbar, NavBrand, NavLi, NavUl } from 'flowbite-svelte';
  import { slide } from 'svelte/transition';

  let isOpen = false;

  function toggleMenu() {
    isOpen = !isOpen;
  }

  function closeMenu() {
    isOpen = false;
  }

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
  }

  function handleJoinSkool() {
    window.location.href = '/coming-soon'
  }
</script>

<Navbar let:NavContainer color="white">
  <NavContainer class="px-5 py-2 bg-white flex justify-between items-center">
    <NavBrand href="/">
      <img src="/android-chrome-192x192.png" class="mr-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
    </NavBrand>
    <button on:click={toggleMenu} class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200">
      <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
      </svg>
    </button>
  </NavContainer>
</Navbar>

{#if isOpen}
<div transition:slide class="px-5 py-2 bg-white">
  <NavUl class="flex flex-col items-end space-y-2">
    <NavLi>
      <a class="nav-link block w-full text-right py-2" href="/about" on:click={closeMenu}>About</a>
    </NavLi>
    <NavLi>
      <a class="nav-link block w-full text-right py-2" href="/contact" on:click={closeMenu}>Contact</a>
    </NavLi>
    <NavLi>
      <a class="nav-link block w-full text-right py-2" href="/sample" on:click={closeMenu}>Read a Sample</a>
    </NavLi>
    <NavLi class="w-full">
      <button class="buy-button w-full text-right py-2 px-4" on:click={handleBackBook}>Back the Book</button>
    </NavLi>
    <NavLi class="w-full">
      <button class="buy-button w-full text-right py-2 px-4" on:click={handleJoinSkool}>Join the Skool Community</button>
    </NavLi>
  </NavUl>
</div>
{/if}

<style>
  .nav-link, .buy-button {
    color: black !important;
    transition: background-color 0.3s ease;
  }

  .nav-link:hover, .buy-button:hover {
    background-color: #f0f0f0;
  }

  .buy-button {
    font-weight: bold;
    background-color: #f8f9fa;
    border: 1px solid #000000;
    border-radius: 4px;
    cursor: pointer;
    margin-left: auto;
    display: inline-block;
  }

  .buy-button:hover {
    background-color: #e2e6ea;
  }
</style>