<script>
  import { Navbar, NavBrand, NavUl, NavLi, DarkMode } from 'flowbite-svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { onMount } from 'svelte';
  import { supabase } from '$lib/utils/supabaseClient';
  import { goto } from '$app/navigation';

  console.log('Navbar.svelte');

  let isFloating = false;
  let navbarHeight = 0;
  let navbar;
  let menuElement;
  let isMenuOpen = false;
  let session = null;

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

  function handleLogin() {
    goto('/login');
    closeMenu();
  }

  async function handleLogout() {
    const { error } = await supabase.auth.signOut();
    if (error) console.error('Error logging out:', error);
    session = null;
    closeMenu();
    goto('/');
  }

  onMount(async () => {
    const handleScroll = () => {
      isFloating = window.scrollY > 0;
    };

    window.addEventListener('scroll', handleScroll);
    navbarHeight = navbar.offsetHeight;

    document.addEventListener('click', (event) => {
      const navbarElement = document.querySelector('.navbar-container');
      if (!navbarElement.contains(event.target) && isMenuOpen) {
        closeMenu();
      }
    });

    // Get initial session
    const { data } = await supabase.auth.getSession();
    session = data.session;

    // Listen for auth changes
    supabase.auth.onAuthStateChange((_, _session) => {
      session = _session;
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
    class="bg-white dark:bg-gray-800 transition-all duration-300 w-full {isFloating ? 'fixed' : 'absolute'} top-0 left-0 right-0 z-50 shadow-lg"
  >
    <NavBrand href="/">
      <img src="/android-chrome-192x192.png" class="mr-3 h-6 sm:h-9" alt="Surviving the Singularity Logo"  loading="lazy" \/\>
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
      <NavLi href="/" class="nav-item" on:click={closeMenu}>Home</NavLi>
      <NavLi href="/about" class="nav-item" on:click={closeMenu}>About</NavLi>
      <NavLi href="/contact" class="nav-item" on:click={closeMenu}>Contact</NavLi>
      <NavLi href="/blog" class="nav-item" on:click={closeMenu}>Blog</NavLi>
      <NavLi href="/sample" class="nav-item" on:click={closeMenu}>Read a Sample</NavLi>
      <NavLi href="/" class="nav-item" on:click={() => { closeMenu(); window.location.href = '/download'; }}>Download</NavLi>
      <NavLi href="/" class="nav-item" on:click={() => { closeMenu(); handleBackBook(); }}>Back the Book</NavLi>
      <NavLi href="/" class="nav-item" on:click={() => { closeMenu(); handleJoinSkool(); }}>Join the Skool Community</NavLi>
      {#if session}
        <NavLi href="/" class="nav-item" on:click={handleLogout}>Logout</NavLi>
      {:else}
        <NavLi href="/login" class="nav-item" on:click={handleLogin}>Login</NavLi>
      {/if}
    </NavUl>
  </Navbar>
</div>

<div class="mobile-menu md:hidden w-full bg-white dark:bg-gray-800 fixed top-[navbarHeight]px left-0 right-0 z-40" style="display: none;">
  <ul class="flex flex-col items-end p-6">
    <li class="w-full text-right py-3"><a href="/" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>Home</a></li>
    <li class="w-full text-right py-3"><a href="/about" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>About</a></li>
    <li class="w-full text-right py-3"><a href="/contact" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>Contact</a></li>
    <li class="w-full text-right py-3"><a href="/blog" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>Blog</a></li>
    <li class="w-full text-right py-3"><a href="/sample" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white text-lg" on:click={closeMenu}>Read a Sample</a></li>
    <li class="w-full text-right py-3">
      <button class="mobile-menu-button" on:click={() => { closeMenu(); window.location.href = '/download'; }}>
        Download
      </button>
    </li>
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
    {#if session}
      <li class="w-full text-right py-3">
        <button class="mobile-menu-button" on:click={handleLogout}>
          Logout
        </button>
      </li>
    {:else}
      <li class="w-full text-right py-3">
        <button class="mobile-menu-button" on:click={handleLogin}>
          Login
        </button>
      </li>
    {/if}
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
    transition: opacity 0.2s ease-out, box-shadow 0.2s ease-out;
    opacity: 0;
    box-shadow: none;
  }
  .mobile-menu:not([style*="display: none"]) {
    opacity: 1;
    box-shadow: 
      0 4px 6px -1px rgba(0, 0, 0, 0.1), 
      0 2px 4px -1px rgba(0, 0, 0, 0.06),
      0 8px 8px -8px rgba(0, 0, 0, 0.8);
  }

  :global(.dark .mobile-menu:not([style*="display: none"])) {
    box-shadow: 
      0 4px 6px -1px rgba(0, 0, 0, 0.1), 
      0 2px 4px -1px rgba(0, 0, 0, 0.06),
      0 8px 8px -8px rgba(255, 255, 255, 0.8);
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

  :global(.mobile-menu li a, .mobile-menu li button) {
    transition: transform 0.3s ease, margin-right 0.3s ease;
    display: inline-block;
  }

  :global(.mobile-menu li a:hover, .mobile-menu li button:hover) {
    transform: scale(1.05);
    margin-right: 5px;
  }

  :global(.nav-item) {
    transition: transform 0.3s ease, margin-left 0.3s ease;
  }

  :global(.nav-item:hover) {
    transform: scale(1.05);
    margin-left: -5px;
  }
</style>