<!-- <!-- <script>
    import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';

    function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
    }
  </script>
  
  <Navbar let:NavContainer color="white">
    <NavContainer class="border px-5 py-2 rounded-lg bg-white">
      <NavBrand href="/">
        <img src="/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
        <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
      </NavBrand>
      <NavHamburger />
      <NavUl class="nav-items-container">
        <NavLi href="/about">
          <a class="nav-link" href="/about">About</a>
        </NavLi>
        <NavLi href="/contact">
          <a class="nav-link" href="/contact">Contact</a>
        </NavLi>
        <NavLi>
          <a class="nav-link" href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
        </NavLi>
        <NavLi class="custom-buy-button-container">
          <button class="nav-link buy-button" on:click={handleBackBook}>Back the Book</button>
        </NavLi>
      </NavUl>
    </NavContainer>
  </Navbar>
  
  <style>
    .me-3 {
      margin-right: 1rem;
    }
  
    .nav-link {
      display: inline-block;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      transition: background-color 0.3s ease;
    }
  
    .nav-link:hover {
      background-color: #e2e6ea; /* Slightly darker on hover */
    }
  
    .buy-button {
      font-weight: bold;
      background-color: #f8f9fa; /* Light background color */
      border: 1px solid #000000;
      border-radius: 4px;
      padding: 0.5rem 1rem;
      cursor: pointer;
    }
  </style> -->

  <!-- <script>
    import { Navbar, NavBrand, NavLi, NavUl } from 'flowbite-svelte';
    import { slide } from 'svelte/transition';
  
    let isOpen = false;
  
    function toggleMenu() {
      isOpen = !isOpen;
    }
  
    function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
    }
  </script>
  
  <Navbar let:NavContainer color="white">
    <NavContainer class="px-5 py-2 bg-white">
      <NavBrand href="/">
        <img src="/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
        <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
      </NavBrand>
      <button class="lg:hidden" on:click={toggleMenu}>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <NavUl class="hidden lg:flex items-center space-x-4">
        <NavLi href="/about">About</NavLi>
        <NavLi href="/contact">Contact</NavLi>
        <NavLi>
          <a href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
        </NavLi>
        <NavLi>
          <button class="buy-button" on:click={handleBackBook}>Back the Book</button>
        </NavLi>
      </NavUl>
    </NavContainer>
    {#if isOpen}
      <div transition:slide class="lg:hidden">
        <NavUl class="flex flex-col space-y-2 p-4">
          <NavLi href="/about">About</NavLi>
          <NavLi href="/contact">Contact</NavLi>
          <NavLi>
            <a href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
          </NavLi>
          <NavLi>
            <button class="buy-button" on:click={handleBackBook}>Back the Book</button>
          </NavLi>
        </NavUl>
      </div>
    {/if}
  </Navbar>
  
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
  </style> 


  <script>
    import { Navbar, NavBrand, NavLi, NavUl } from 'flowbite-svelte';
    import { slide } from 'svelte/transition';
  
    let isOpen = false;
  
    function toggleMenu() {
      isOpen = !isOpen;
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
      <button class="lg:hidden" on:click={toggleMenu}>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <NavUl class="hidden lg:flex items-center space-x-4">
        <NavLi href="/about">About</NavLi>
        <NavLi href="/contact">Contact</NavLi>
        <NavLi>
          <a href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
        </NavLi>
        <NavLi>
          <button class="buy-button" on:click={handleBackBook}>Back the Book</button>
        </NavLi>
      </NavUl>
    </NavContainer>
    {#if isOpen}
      <div transition:slide class="lg:hidden">
        <NavUl class="flex flex-col items-end space-y-4 px-5 py-4 bg-white">
          <NavLi href="/about" class="text-right">About</NavLi>
          <NavLi href="/contact" class="text-right">Contact</NavLi>
          <NavLi class="text-right">
            <a href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
          </NavLi>
          <NavLi class="text-right">
            <button class="buy-button block w-full" on:click={handleBackBook}>Back the Book</button>
          </NavLi>
        </NavUl>
      </div>
    {/if}
  </Navbar>
  
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
  </style>


  <script>
    import { Navbar, NavBrand, NavLi, NavUl } from 'flowbite-svelte';
    import { slide } from 'svelte/transition';
  
    let isOpen = false;
  
    function toggleMenu() {
      isOpen = !isOpen;
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
      <button class="lg:hidden" on:click={toggleMenu}>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <NavUl class="hidden lg:flex items-center space-x-4">
        <NavLi href="/about">About</NavLi>
        <NavLi href="/contact">Contact</NavLi>
        <NavLi>
          <a href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
        </NavLi>
        <NavLi>
          <button class="buy-button" on:click={handleBackBook}>Back the Book</button>
        </NavLi>
      </NavUl>
    </NavContainer>
  </Navbar>
  
  {#if isOpen}
    <div transition:slide class="lg:hidden">
      <NavUl class="flex flex-col items-end space-y-4 px-5 py-4 bg-white">
        <NavLi href="/about">About</NavLi>
        <NavLi href="/contact">Contact</NavLi>
        <NavLi>
          <a href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
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
  </style> -->

  <!-- WORKING!!! -->
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
      <button on:click={toggleMenu} class="h-6 w-6">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-16 6h16" />
        </svg>
      </button>
    </NavContainer>
</Navbar>

{#if isOpen}
<div transition:slide class="lg:hidden">
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
      text-align: right;
    }
  
    .buy-button:hover {
      background-color: #e2e6ea;
    }

    .nav-link, .buy-button {
        color: black !important; /* Overrides other color properties */
    }

    .nav-link:hover, .buy-button:hover {
        color: rgb(0, 0, 0) !important; /* Adjust based on your design for hover states */
    }

  </style>
  <!-- WORKING!!! -->


<!--  <script>
    import { Navbar, NavBrand, NavLi, NavUl } from 'flowbite-svelte';
    import { slide } from 'svelte/transition';
    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';  // Import to check for client-side
  
    let isOpen = false;
    let menuRef;
  
    function toggleMenu() {
      isOpen = !isOpen;
    }
  
    function closeMenu() {
      isOpen = false;
    }
  
    // Handles outside click only on the client-side
    function handleClickOutside(event) {
      if (browser && menuRef && !menuRef.contains(event.target)) {
        closeMenu();
      }
    }
  
    onMount(() => {
      if (browser) {
        document.addEventListener('mousedown', handleClickOutside);
      }
    });
  
    onDestroy(() => {
      if (browser) {
        document.removeEventListener('mousedown', handleClickOutside);
      }
    });
  </script>
  
  <div bind:this={menuRef} class="navbar-container">
    <Navbar let:NavContainer color="white">
      <NavContainer class="px-5 py-2 bg-white flex justify-between items-center">
        <NavBrand href="/">
          <img src="/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
          <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
        </NavBrand>
        <button on:click={toggleMenu}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-16 6h16" />
          </svg>
        </button>
      </NavContainer>
    </Navbar>
  
    {#if isOpen}
      <div transition:slide class="bg-white flex flex-col items-end space-y-4 px-5 py-4">
        <NavUl>
          <NavLi on:click={closeMenu}><a class="nav-link" href="/about">About</a></NavLi>
          <NavLi on:click={closeMenu}><a class="nav-link" href="/contact">Contact</a></NavLi>
          <NavLi on:click={closeMenu}><a class="nav-link" href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a></NavLi>
          <NavLi on:click={closeMenu}><button class="buy-button w-full">Back the Book</button></NavLi>
        </NavUl>
      </div>
    {/if}
  </div>
  
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
      text-align: right;
    }
    .buy-button:hover {
      background-color: #e2e6ea;
    }
  </style>  -->
  

  <!-- <script>
    import { Navbar, NavBrand, NavLi, NavUl } from 'flowbite-svelte';
    import { slide } from 'svelte/transition';
    import { onMount, onDestroy } from 'svelte';
  
    let isOpen = false;
    let menuRef; // We'll use this to reference the menu element
  
    function toggleMenu() {
      isOpen = !isOpen;
    }
  
    function closeMenu() {
      isOpen = false;
    }
  
    function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
      closeMenu(); // Close the menu after opening the link
    }
  
    // Function to handle outside click
    function handleClickOutside(event) {
      if (menuRef && !menuRef.contains(event.target) && isOpen) {
        closeMenu();
      }
    }
  
    // Adding event listener on the client side
    onMount(() => {
      if (typeof window !== 'undefined') {
        window.addEventListener('click', handleClickOutside);
      }
    });
  
    onDestroy(() => {
      if (typeof window !== 'undefined') {
        window.removeEventListener('click', handleClickOutside);
      }
    });
  
    // Bind the menu DOM element to menuRef
    $: if (isOpen) {
      menuRef = document.querySelector('.menu-container');
    }
  </script>
  
  <Navbar let:NavContainer color="white">
    <NavContainer class="px-5 py-2 bg-white flex justify-between items-center">
      <NavBrand href="/">
        <img src="/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
        <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
      </NavBrand>
      <button on:click={toggleMenu} class="h-6 w-6">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-16 6h16" />
        </svg>
      </button>
    </NavContainer>
  </Navbar>
  
  {#if isOpen}
  <div class="menu-container lg:hidden" transition:slide bind:this={menuRef}>
    <NavUl class="flex flex-col items-end space-y-4 px-5 py-4 bg-white text-right text-black">
      <NavLi><a class="nav-link" href="/about" on:click={closeMenu}>About</a></NavLi>
      <NavLi><a class="nav-link" href="/contact" on:click={closeMenu}>Contact</a></NavLi>
      <NavLi><a class="nav-link" href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank" on:click={closeMenu}>Read a Sample</a></NavLi>
      <NavLi><button class="buy-button block w-full" on:click={handleBackBook}>Back the Book</button></NavLi>
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
      text-align: right;
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
   -->