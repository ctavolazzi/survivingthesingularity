<script>
  import { Navbar, NavBrand, NavUl, NavLi, DarkMode } from 'flowbite-svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { IconHome, IconAbout, IconBlog, IconContact, IconSample, IconMore } from '$lib/assets/Icons.svelte';
  import { onMount } from 'svelte';

  let navbar;
  let isMenuOpen = false;
  let isDropdownOpen = false;
  let isMobileMoreOpen = false;

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
  }

  function toggleMobileMore(event) {
    event.stopPropagation();
    isMobileMoreOpen = !isMobileMoreOpen;
  }

  function toggleDarkMode() {
    darkMode.update(d => !d);
  }

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  onMount(() => {
    document.addEventListener('click', (event) => {
      if (navbar && !navbar.contains(event.target) && isMenuOpen) {
        closeMenu();
      }
    });

    return () => {
      document.removeEventListener('click', closeMenu);
    };
  });

  let currentPath;
  $: currentPath = $page.url.pathname;
</script>

<div class="navbar-container" bind:this={navbar}>
  <Navbar 
    class="bg-white dark:bg-gray-800 transition-all duration-300 w-full fixed top-0 left-0 right-0 z-50 shadow-lg"
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
      <NavLi href="/" class="nav-item" on:click={closeMenu}>Home</NavLi>
      <NavLi href="/about" class="nav-item" on:click={closeMenu}>About</NavLi>
      <NavLi href="/blog" class="nav-item" on:click={closeMenu}>Blog</NavLi>
      <NavLi href="/contact" class="nav-item" on:click={closeMenu}>Contact</NavLi>
      <NavLi href="/sample" class="nav-item" on:click={closeMenu}>Sample</NavLi>
      <NavLi class="nav-item relative dropdown">
        <button class="dropdown-toggle" on:click={toggleDropdown}>Resources</button>
        {#if isDropdownOpen}
          <ul class="dropdown-menu show">
            <li><a href="/download" class="dropdown-item highlight" on:click={closeMenu}>Download FREE Guide</a></li>
            <li><button class="dropdown-item" on:click={() => { closeMenu(); handleBackBook(); }}>Support on Kickstarter</button></li>
            <li><button class="dropdown-item" on:click={() => { closeMenu(); handleJoinSkool(); }}>Join the Skool Community</button></li>
          </ul>
        {/if}
      </NavLi>
    </NavUl>
  </Navbar>
</div>

{#if isMenuOpen}
  <div class="mobile-menu md:hidden w-full bg-white dark:bg-gray-800 fixed top-[64px] left-0 right-0 z-40">
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
        <button class="mobile-menu-link flex items-center justify-between w-full" on:click={toggleMobileMore} aria-expanded={isMobileMoreOpen} data-tracking="nav-resources">
          Resources
          <span class="nav-icon">{@html IconMore.svg}</span>
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
          </ul>
        {/if}
      </li>
    </ul>
  </div>
{/if}

<style>
  :global(body) {
    padding-top: 30px; /* Adjust this value based on your navbar height */
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

  .dropdown-toggle {
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    font: inherit;
    outline: inherit;
  }

  .dropdown-menu {
    display: none;
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

  .dropdown-menu.show {
    display: block;
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

  .dropdown-item.highlight {
    font-weight: 600;
    color: #3182ce;
  }

  .dropdown-item.highlight:hover {
    color: #2c5282;
    background-color: #bee3f8;
  }

  :global(.dark) .dropdown-menu {
    background-color: #2d3748;
    border-color: rgba(255,255,255,0.1);
  }

  :global(.dark) .dropdown-item {
    color: #e2e8f0;
  }

  :global(.dark) .dropdown-item:hover, :global(.dark) .dropdown-item:focus {
    color: #fff;
    background-color: #4a5568;
  }

  :global(.dark) .dropdown-item.highlight {
    color: #63b3ed;
  }

  :global(.dark) .dropdown-item.highlight:hover {
    color: #90cdf4;
    background-color: #2c5282;
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
</style>