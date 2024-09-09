<script>
  import { Navbar, NavBrand, NavUl, NavLi, DarkMode } from 'flowbite-svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { IconHome, IconAbout, IconBlog, IconContact, IconSample, IconPreorder, IconResources, IconData } from '$lib/assets/Icons.svelte';
  import { onMount } from 'svelte';
  import DarkModeToggle from './DarkModeToggle.svelte';

  let navbar;
  let isMenuOpen = false;
  let isDropdownOpen = false;
  let isMobileMoreOpen = false;
  let isLargeScreen = false;

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }

  function closeMenu() {
    isMenuOpen = false;
    isDropdownOpen = false;
    isMobileMoreOpen = false;
  }

  function toggleDropdown(event) {
    event.stopPropagation();
    isDropdownOpen = !isDropdownOpen;
    console.log("Dropdown open:", isDropdownOpen);
  }

  function toggleMobileMore(event) {
    event.stopPropagation();
    isMobileMoreOpen = !isMobileMoreOpen;
    console.log("Mobile more open:", isMobileMoreOpen);
  }

  function toggleDarkMode() {
    darkMode.update(current => !current);
    console.log("Dark mode toggled. New value:", $darkMode);
  }

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  function handleDataWarehouseClick() {
    goto('/data-warehouse');
    closeMenu();
  }

  function handleNewsletterClick() {
    goto('/newsletter');
    closeMenu();
  }

  onMount(() => {
    const closeDropdown = (event) => {
      if (isDropdownOpen && !event.target.closest('.nav-item')) {
        isDropdownOpen = false;
      }
    };

    document.addEventListener('click', closeDropdown);

    const mediaQuery = window.matchMedia('(min-width: 1280px)');
    isLargeScreen = mediaQuery.matches;
    
    const handler = (e) => isLargeScreen = e.matches;
    mediaQuery.addListener(handler);
    
    return () => {
      document.removeEventListener('click', closeDropdown);
      mediaQuery.removeListener(handler);
    };
  });

  let currentPath;
  $: currentPath = $page.url.pathname;

  $: if (typeof document !== 'undefined') {
    document.documentElement.classList.toggle('dark', $darkMode);
  }

  $: console.log("Dark mode value in Navbar:", $darkMode);
</script>

<Navbar
  class="bg-white dark:bg-gray-800 transition-all duration-300 w-full fixed top-0 left-0 right-0 z-50 shadow-lg"
>
  <NavBrand href="/">
    <img src="/android-chrome-192x192.png" class="mr-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
    <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
      Surviving the Singularity
    </span>
  </NavBrand>
  
  <div class="flex items-center xl:order-2">
    <!-- <DarkMode checked={$darkMode} on:change={toggleDarkMode} class="mr-3" /> -->
    <DarkModeToggle />
    {#if !isLargeScreen}
      <button on:click={toggleMenu} class="text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-4 focus:ring-gray-200 rounded-lg text-sm p-2.5 inline-flex items-center dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
      </button>
    {/if}
  </div>
  
  {#if isLargeScreen}
    <NavUl class="flex items-center justify-end w-full xl:w-auto xl:order-1">
      <NavLi href="/about" class="nav-item">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">About</span>
          <span class="nav-icon ml-2">{@html IconAbout.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/blog" class="nav-item">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Blog</span>
          <span class="nav-icon ml-2">{@html IconBlog.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/contact" class="nav-item">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Contact</span>
          <span class="nav-icon ml-2">{@html IconContact.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/sample" class="nav-item">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Sample</span>
          <span class="nav-icon ml-2">{@html IconSample.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/preorder" class="nav-item">
        <span class="preorder-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Preorder</span>
          <span class="nav-icon ml-2">{@html IconPreorder.svg}</span>
        </span>
      </NavLi>
      <NavLi class="nav-item relative">
        <button
          on:click={toggleDropdown}
          class="nav-button flex items-center h-full w-full"
          aria-expanded={isDropdownOpen}
        >
          <span class="flex-grow text-left">Resources</span>
          <span class="nav-icon ml-2">{@html IconResources.svg}</span>
        </button>
        {#if isDropdownOpen}
          <div class="dropdown-menu absolute right-0 mt-2 py-2 w-48 bg-white rounded-md shadow-xl z-20">
            <a href="/download" class="dropdown-item">Download FREE Guide</a>
            <button on:click={handleBackBook} class="dropdown-item">Support on Kickstarter</button>
            <button on:click={handleJoinSkool} class="dropdown-item">Join Skool Community</button>
            <button on:click={handleNewsletterClick} class="dropdown-item">Newsletter</button>
            <button on:click={handleDataWarehouseClick} class="dropdown-item">Data Warehouse</button>
          </div>
        {/if}
      </NavLi>
    </NavUl>
  {/if}
</Navbar>

{#if !isLargeScreen && isMenuOpen}
  <div class="mobile-menu w-full bg-white dark:bg-gray-800 fixed top-[64px] left-0 right-0 z-40">
    <ul class="flex flex-col items-end p-6">
      <li class="w-full border-b border-gray-200 dark:border-gray-700">
        <a href="/" class="mobile-menu-link {currentPath === '/' ? 'active' : ''}" on:click={closeMenu} aria-label="Home" data-tracking="nav-home">
          Home
          <span class="nav-icon">{@html IconHome.svg}</span>
        </a>
      </li>
      <li class="w-full border-b border-gray-200 dark:border-gray-700">
        <a href="/about" class="mobile-menu-link {currentPath === '/about' ? 'active' : ''}" on:click={closeMenu} aria-label="About" data-tracking="nav-about">
          About
          <span class="nav-icon">{@html IconAbout.svg}</span>
        </a>
      </li>
      <li class="w-full border-b border-gray-200 dark:border-gray-700">
        <a href="/blog" class="mobile-menu-link {currentPath === '/blog' ? 'active' : ''}" on:click={closeMenu} aria-label="Blog" data-tracking="nav-blog">
          Blog
          <span class="nav-icon">{@html IconBlog.svg}</span>
        </a>
      </li>
      <li class="w-full border-b border-gray-200 dark:border-gray-700">
        <a href="/contact" class="mobile-menu-link {currentPath === '/contact' ? 'active' : ''}" on:click={closeMenu} aria-label="Contact" data-tracking="nav-contact">
          Contact
          <span class="nav-icon">{@html IconContact.svg}</span>
        </a>
      </li>
      <li class="w-full border-b border-gray-200 dark:border-gray-700">
        <a href="/sample" class="mobile-menu-link {currentPath === '/sample' ? 'active' : ''}" on:click={closeMenu} aria-label="Sample" data-tracking="nav-sample">
          Sample
          <span class="nav-icon">{@html IconSample.svg}</span>
        </a>
      </li>
      <li class="w-full border-b border-gray-200 dark:border-gray-700">
        <a href="/preorder" class="mobile-menu-link preorder-button flex items-center justify-between w-full" on:click={closeMenu} aria-label="Preorder" data-tracking="nav-preorder">
          Preorder
          <span class="nav-icon">{@html IconPreorder.svg}</span>
        </a>
      </li>
      <li class="w-full border-b border-gray-200 dark:border-gray-700">
        <button class="mobile-menu-link flex items-center justify-between w-full" on:click={toggleMobileMore} aria-expanded={isMobileMoreOpen} data-tracking="nav-resources">
          Resources
          <span class="nav-icon">{@html IconResources.svg}</span>
        </button>
        {#if isMobileMoreOpen}
          <ul class="mt-2 space-y-2 w-full">
            <li>
              <a href="/download" class="mobile-menu-sublink highlight" on:click={closeMenu} aria-label="Download FREE Guide" data-tracking="nav-download">
                Download FREE Guide
              </a>
            </li>
            <li>
              <button class="mobile-menu-sublink external-link" on:click={() => { closeMenu(); handleBackBook(); }} aria-label="Support on Kickstarter" data-tracking="nav-kickstarter">
                Support on Kickstarter
              </button>
            </li>
            <li>
              <button class="mobile-menu-sublink external-link" on:click={() => { closeMenu(); handleJoinSkool(); }} aria-label="Join Skool Community" data-tracking="nav-skool">
                Join Skool Community
              </button>
            </li>
            <li>
              <button class="mobile-menu-sublink" on:click={handleNewsletterClick} aria-label="Newsletter" data-tracking="nav-newsletter">
                Newsletter
              </button>
            </li>
            <li>
              <button class="mobile-menu-sublink" on:click={handleDataWarehouseClick} aria-label="Data Warehouse" data-tracking="nav-data-warehouse">
                Data Warehouse
              </button>
            </li>
          </ul>
        {/if}
      </li>
    </ul>
  </div>
{/if}

<style>
  :global(body) {
    padding-top: 72px; /* Adjust this value based on your navbar height */
    overflow-x: hidden;
  }

  .mobile-menu {
    transition: none;
    opacity: 1;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  :global(.dark) .mobile-menu {
    box-shadow: 0 4px 6px -1px rgba(255, 255, 255, 0.1), 0 2px 4px -1px rgba(255, 255, 255, 0.06);
  }

  .mobile-menu-link,
  .mobile-menu-sublink,
  .mobile-menu-button {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 0.75rem 0;
    text-align: left;
    font-size: 1.125rem;
    color: #4a5568;
    transition: all 0.2s ease-in-out;
    position: relative;
    right: 0;
  }

  .mobile-menu-sublink {
    font-size: 1rem;
    padding: 0.5rem 0;
  }

  .icon {
    width: 1.5em;
    height: 1.5em;
    margin-left: 0.5em;
  }

  :global(.dark) .mobile-menu-link {
    color: #e2e8f0;
  }

  .mobile-menu-link:hover,
  .mobile-menu-sublink:hover {
    color: #2d3748;
    right: 5px;
  }

  :global(.dark) .mobile-menu-link:hover {
    color: #fff;
  }

  :global(.dark) .mobile-menu-sublink {
    color: #a0aec0;
  }

  .mobile-menu-sublink:hover {
    color: #4a5568;
  }

  :global(.dark) .mobile-menu-sublink:hover {
    color: #e2e8f0;
  }

  .mobile-menu-button {
    display: block;
    width: 100%;
    padding: 0.75rem 1.5rem;
    text-align: center;
    font-size: 1.125rem;
    font-weight: 500;
    color: #fff;
    background-color: #4a5568;
    border-radius: 0.375rem;
    transition: all 0.2s ease-in-out;
  }

  :global(.dark) .mobile-menu-button {
    background-color: #2d3748;
  }

  .mobile-menu-button:hover {
    background-color: #2d3748;
  }

  :global(.dark) .mobile-menu-button:hover {
    background-color: #4a5568;
  }

  .icon {
    display: inline-block;
    width: 1.5em;
    text-align: center;
    margin-right: 0.5em;
  }

  .active {
    font-weight: bold;
    color: #2b6cb0;
  }

  :global(.dark) .active {
    color: #63b3ed;
  }

  .highlight {
    font-weight: bold;
    color: #4299e1;
  }

  :global(.dark) .highlight {
    color: #63b3ed;
  }

  .download-link {
    color: #2f855a;
  }

  :global(.dark) .download-link {
    color: #48bb78;
  }

  .external-link {
    color: #805ad5;
  }

  :global(.dark) .external-link {
    color: #b794f4;
  }

  .nav-item {
    display: flex;
    align-items: stretch; /* Ensures child elements stretch to full height */
  }

  .dropdown-toggle {
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    font: inherit;
    outline: inherit;
  }

  .dropdown-menu {
    display: block;
    position: absolute;
    right: 0;
    top: 100%;
    z-index: 50;
    min-width: 220px;
    padding: 0.75rem 0;
    margin: 0.125rem 0 0;
    background-color: #fff;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
  }

  .dropdown-item {
    display: block;
    width: 100%;
    padding: 0.75rem 1.25rem;
    clear: both;
    font-weight: 500;
    color: #4a5568;
    text-align: left;
    white-space: nowrap;
    background-color: transparent;
    border: 0;
    transition: all 0.2s ease-in-out;
  }

  .dropdown-item:hover, .dropdown-item:focus {
    color: #2b6cb0;
    text-decoration: none;
    background-color: #ebf8ff;
  }

  :global(.dark) .dropdown-menu {
    background-color: #2d3748;
    border-color: rgba(255,255,255,0.1);
  }

  :global(.dark) .dropdown-item {
    color: #e2e8f0;
  }

  :global(.dark) .dropdown-item:hover, :global(.dark) .dropdown-item:focus {
    color: #90cdf4;
    background-color: #4a5568;
  }

  .mobile-menu-link:hover,
  .mobile-menu-sublink:hover,
  .dropdown-item:hover {
    background-color: #f7fafc;
    right: 5px;
  }

  :global(.dark) .mobile-menu-link:hover,
  :global(.dark) .mobile-menu-sublink:hover,
  :global(.dark) .dropdown-item:hover {
    background-color: #2d3748;
  }

  .mobile-menu-link:focus,
  .mobile-menu-sublink:focus,
  .dropdown-item:focus {
    outline: 2px solid #4299e1;
    outline-offset: 2px;
  }

  :global(.dark) .mobile-menu-link:focus,
  :global(.dark) .mobile-menu-sublink:focus,
  :global(.dark) .dropdown-item:focus {
    outline-color: #63b3ed;
  }

  .nav-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
  }

  .nav-icon :global(svg) {
    width: 100%;
    height: 100%;
  }

  .nav-item {
    display: flex;
    align-items: stretch;
  }

  .nav-button,
  .preorder-button {
    position: relative;
    color: inherit;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100%;
    width: 100%;
  }

  .nav-button::before,
  .preorder-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: currentColor;
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
  }

  .nav-button:hover::before {
    opacity: 0.1;
  }

  .preorder-button::before {
    opacity: 0.1;
  }

  .preorder-button:hover::before {
    opacity: 0.2;
  }

  .nav-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
  }

  .nav-icon :global(svg) {
    width: 100%;
    height: 100%;
  }

  /* Pulsing animation only for preorder button */
  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(66, 153, 225, 0.4);
    }
    70% {
      box-shadow: 0 0 0 10px rgba(66, 153, 225, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(66, 153, 225, 0);
    }
  }

  .preorder-button {
    animation: pulse 2s infinite;
  }

  :global(.dark) .preorder-button {
    animation: pulse-dark 2s infinite;
  }

  @keyframes pulse-dark {
    0% {
      box-shadow: 0 0 0 0 rgba(99, 179, 237, 0.4);
    }
    70% {
      box-shadow: 0 0 0 10px rgba(99, 179, 237, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(99, 179, 237, 0);
    }
  }
</style>