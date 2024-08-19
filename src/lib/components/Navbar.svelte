<script>
  import { Navbar, NavBrand, NavUl, NavLi, DarkMode } from 'flowbite-svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { onMount } from 'svelte';

  let isFloating = false;
  let navbarHeight = 0;
  let navbar;
  let menuElement;
  let isMenuOpen = false;

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
    const menu = document.querySelector('.mobile-menu');
    menu.style.display = isMenuOpen ? 'block' : 'none';
  }

  function closeMenu() {
    isMenuOpen = false;
    const menu = document.querySelector('.mobile-menu');
    menu.style.display = 'none';
  }

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  function toggleDarkMode() {
    darkMode.update(d => !d);
    localStorage.setItem('darkMode', $darkMode);
  }

  onMount(() => {
    const handleScroll = () => {
      isFloating = window.scrollY > 0;
    };

    window.addEventListener('scroll', handleScroll);
    navbarHeight = navbar.offsetHeight;

    // Add click event listener to the document
    document.addEventListener('click', (event) => {
      const navbarElement = document.querySelector('.navbar-container');
      if (!navbarElement.contains(event.target) && isMenuOpen) {
        closeMenu();
      }
    });

    return () => {
      window.removeEventListener('scroll', handleScroll);
      document.removeEventListener('click', closeMenu);
    };
  });
</script>

<div class="navbar-container" style="height: {navbarHeight}px">
  <Navbar 
    bind:this={navbar}
    class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 transition-all duration-300 w-full {isFloating ? 'fixed' : 'absolute'} top-0 left-0 right-0 z-50"
  >
    <NavBrand href="/">
      <img src="/android-chrome-192x192.png" class="mr-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
        Surviving the Singularity
      </span>
    </NavBrand>
    <div class="flex items-center md:order-2">
      <DarkMode on:change={toggleDarkMode} class="mr-3" />
      <button on:click={toggleMenu} class="text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-4 focus:ring-gray-200 rounded-lg text-sm p-2.5 inline-flex items-center dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600 md:hidden">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
      </button>
    </div>
    <NavUl class="md:flex md:items-center md:justify-end w-full md:w-auto md:order-1 hidden">
      <NavLi href="/about" class="md:text-right" on:click={closeMenu}>About</NavLi>
      <NavLi href="/contact" class="md:text-right" on:click={closeMenu}>Contact</NavLi>
      <NavLi href="/blog" class="md:text-right" on:click={closeMenu}>Blog</NavLi>
      <NavLi href="/sample" class="md:text-right" on:click={closeMenu}>Read a Sample</NavLi>
      <NavLi href="/" on:click={() => { closeMenu(); handleBackBook(); }} class="md:text-right">Back the Book</NavLi>
      <NavLi href="/" on:click={() => { closeMenu(); handleJoinSkool(); }} class="md:text-right">Join the Skool Community</NavLi>
    </NavUl>
  </Navbar>
</div>

<div class="mobile-menu md:hidden w-full bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 fixed top-[navbarHeight]px left-0 right-0 z-40" style="display: none;">
  <ul class="flex flex-col items-end p-6">
    <li class="w-full text-right py-3"><a href="/about" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>About</a></li>
    <li class="w-full text-right py-3"><a href="/about" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>About</a></li>
    <li class="w-full text-right py-3"><a href="/contact" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>Contact</a></li>
    <li class="w-full text-right py-3"><a href="/blog" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>Blog</a></li>
    <li class="w-full text-right py-3"><a href="/sample" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>Read a Sample</a></li>
    <li class="w-full text-right py-3">
      <button class="mobile-menu-button" on:click={() => { closeMenu(); handleBackBook(); }}>
        Back the Book
      </button>
    </li>
    <li class="w-full text-right py-3">
      <button class="mobile-menu-button" on:click={() => { closeMenu(); handleJoinSkool(); }}>
        Join the Skool Community
      </button>
    </li>
  </ul>
</div>

<style>
  .navbar-container {
    position: relative;
    z-index: 50;
  }

  :global(body) {
    overflow-x: hidden; /* Prevent horizontal scrolling */
  }

  .mobile-menu {
    transition: opacity 0.2s ease-out;
    opacity: 0;
  }
  .mobile-menu:not([style*="display: none"]) {
    opacity: 1;
  }
  
  :global(.mobile-menu-button) {
    background-color: white;
    color: black;
    border: 2px solid black;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
    float: right;
    clear: both;
  }

  :global(.dark .mobile-menu-button) {
    background-color: #1f2937; /* Tailwind's gray-800 */
    color: white;
    border-color: white;
  }
  
  :global(.mobile-menu-button:hover) {
    opacity: 0.8;
  }

  :global(.mobile-menu a, .mobile-menu button) {
    display: inline-block;
  }
</style>