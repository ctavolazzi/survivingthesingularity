<script>
  import { Navbar, NavBrand, NavHamburger } from 'flowbite-svelte';
  import { slide } from 'svelte/transition';

  let isOpen = false;

  function toggleMenu() {
    isOpen = !isOpen;
  }

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }
</script>

<Navbar color="white" class="px-4 py-2.5">
  <div class="flex justify-between items-center w-full">
    <NavBrand href="/">
      <img src="/android-chrome-192x192.png" class="mr-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
    </NavBrand>
    <button on:click={toggleMenu} class="text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 rounded-lg text-sm p-2.5">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
      </svg>
    </button>
  </div>
</Navbar>

{#if isOpen}
  <div transition:slide={{ duration: 300 }} class="w-full bg-white border-b border-gray-200">
    <ul class="flex flex-col items-end p-4">
      <li class="w-full text-right py-2"><a href="/about">About</a></li>
      <li class="w-full text-right py-2"><a href="/contact">Contact</a></li>
      <li class="w-full text-right py-2"><a href="/blog">Blog</a></li>
      <li class="w-full text-right py-2"><a href="/sample">Read a Sample</a></li>
      <li class="w-full text-right py-2">
        <button class="buy-button" on:click={handleBackBook}>Back the Book</button>
      </li>
      <li class="w-full text-right py-2">
        <button class="buy-button" on:click={handleJoinSkool}>Join the Skool Community</button>
      </li>
    </ul>
  </div>
{/if}

<style>
  .nav-link, .buy-button {
    color: black !important;
    transition: background-color 0.1s ease;
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
    display: inline-block;
    padding: 0.5rem 1rem;
    text-align: center;
    width: auto;
  }

  .buy-button:hover {
    background-color: #e2e6ea;
  }
</style>