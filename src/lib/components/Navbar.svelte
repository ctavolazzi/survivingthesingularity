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
</script>

<Navbar let:NavContainer color="white">
  <NavContainer class="px-5 py-2 bg-white flex justify-between items-center">
    <NavBrand href="/">
      <img src="/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
    </NavBrand>
    <button on:click={toggleMenu} class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200">
      <!-- <span class="sr-only">Open main menu</span> -->
      <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
      </svg>
    </button>
  </NavContainer>
</Navbar>

{#if isOpen}
<div transition:slide>
  <NavUl class="flex flex-col items-end px-5 py-1 bg-white text-right text-black">
    <NavLi>
      <a class="nav-link" href="/about" on:click={closeMenu}>About</a>
    </NavLi>
    <NavLi>
      <a class="nav-link" href="/contact" on:click={closeMenu}>Contact</a>
    </NavLi>
    <NavLi>
      <a class="nav-link" on:click={closeMenu} href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
    </NavLi>
    <NavLi>
      <button class="buy-button block w-full" on:click={handleBackBook}>Back the Book</button>
    </NavLi>
  </NavUl>
</div>
{/if}

<style>
  .me-3 {
    margin-right: 1rem;
  }

  .buy-button {
    font-weight: bold;
    background-color: #f8f9fa;
    border: 1px solid #000000;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .buy-button:hover {
    background-color: #e2e6ea;
  }

  .nav-link, .buy-button {
    color: black !important;
  }

  .nav-link:hover, .buy-button:hover {
    color: rgb(0, 0, 0) !important;
  }
</style>