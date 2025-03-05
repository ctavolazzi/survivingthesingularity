<script>
  import { Navbar, NavBrand, NavUl, NavLi } from 'flowbite-svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { IconHome, IconAbout, IconBlog, IconContact, IconSample, IconData, IconNewsletter } from '$lib/assets/Icons.svelte';
  import { onMount } from 'svelte';
  import { slide, fade } from 'svelte/transition';

  let navbar;
  let isMenuOpen = false;
  let isLargeScreen = false;

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
    if (isMenuOpen) {
      // Prevent scrolling when menu is open
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }

  function closeMenu() {
    isMenuOpen = false;
    document.body.style.overflow = '';
  }

  function handleClickOutside(event) {
    const mobileMenu = document.querySelector('.mobile-menu');
    const hamburgerButton = document.querySelector('.hamburger-button');

    if (isMenuOpen && mobileMenu && hamburgerButton) {
      if (!mobileMenu.contains(event.target) && !hamburgerButton.contains(event.target)) {
        closeMenu();
      }
    }
  }

  onMount(() => {
    const mediaQuery = window.matchMedia('(min-width: 1024px)');
    isLargeScreen = mediaQuery.matches;

    const handler = (e) => {
      isLargeScreen = e.matches;
      if (isLargeScreen) {
        closeMenu();
      }
    };

    mediaQuery.addEventListener('change', handler);
    document.addEventListener('click', handleClickOutside);

    return () => {
      mediaQuery.removeEventListener('change', handler);
      document.removeEventListener('click', handleClickOutside);
    };
  });

  let currentPath;
  $: currentPath = $page.url.pathname;

  $: if (typeof document !== 'undefined') {
    document.documentElement.classList.toggle('dark', $darkMode);
  }
</script>

<Navbar
  class="bg-gray-800 transition-all duration-300 w-full sticky top-0 left-0 right-0 z-50 shadow-lg"
>
  <NavBrand href="/">
    <img src="/android-chrome-192x192.png" class="mr-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
    <span class="self-center whitespace-nowrap text-xl font-semibold text-white">
      Surviving the Singularity
    </span>
  </NavBrand>

  <div class="flex items-center lg:order-2">
    {#if !isLargeScreen}
      <button
        class="hamburger-button ml-2 text-gray-300 hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-600 rounded-lg text-sm p-2.5 inline-flex items-center"
        on:click={toggleMenu}
        aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
        aria-expanded={isMenuOpen}
      >
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
      </button>
    {/if}
  </div>

  {#if isLargeScreen}
    <NavUl class="flex items-center justify-end w-full lg:w-auto lg:order-1">
      <NavLi href="/about" class="nav-item {currentPath === '/about' ? 'active' : ''}">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">About</span>
          <span class="nav-icon ml-2">{@html IconAbout.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/blog" class="nav-item {currentPath === '/blog' ? 'active' : ''}">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Blog</span>
          <span class="nav-icon ml-2">{@html IconBlog.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/sample" class="nav-item {currentPath === '/sample' ? 'active' : ''}">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Sample</span>
          <span class="nav-icon ml-2">{@html IconSample.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/data-warehouse" class="nav-item {currentPath.startsWith('/data-warehouse') ? 'active' : ''}">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Data Warehouse</span>
          <span class="nav-icon ml-2">{@html IconData.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/newsletter" class="nav-item {currentPath === '/newsletter' ? 'active' : ''}">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Newsletter</span>
          <span class="nav-icon ml-2">{@html IconNewsletter.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/contact" class="nav-item {currentPath === '/contact' ? 'active' : ''}">
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Contact</span>
          <span class="nav-icon ml-2">{@html IconContact.svg}</span>
        </span>
      </NavLi>
    </NavUl>
  {/if}
</Navbar>

{#if !isLargeScreen && isMenuOpen}
  <!-- Overlay background -->
  <div
    class="fixed inset-0 bg-black bg-opacity-50 z-30"
    on:click={closeMenu}
    on:keydown={(e) => e.key === 'Escape' && closeMenu()}
    role="button"
    tabindex="0"
    aria-label="Close menu overlay"
    transition:fade={{ duration: 200 }}
  ></div>

  <div
    class="mobile-menu w-full bg-gray-800 z-40 shadow-lg overflow-y-auto"
    transition:slide={{ duration: 300 }}
  >
    <ul class="flex flex-col p-4 space-y-2">
      <li class="w-full p-2 rounded-lg hover:bg-gray-700">
        <a
          href="/"
          class="mobile-menu-link {currentPath === '/' ? 'active' : ''}"
          on:click={closeMenu}
          aria-label="Home"
        >
          <span class="nav-icon mr-3">{@html IconHome.svg}</span>
          Home
        </a>
      </li>
      <li class="w-full p-2 rounded-lg hover:bg-gray-700">
        <a
          href="/about"
          class="mobile-menu-link {currentPath === '/about' ? 'active' : ''}"
          on:click={closeMenu}
          aria-label="About"
        >
          <span class="nav-icon mr-3">{@html IconAbout.svg}</span>
          About
        </a>
      </li>
      <li class="w-full p-2 rounded-lg hover:bg-gray-700">
        <a
          href="/blog"
          class="mobile-menu-link {currentPath === '/blog' ? 'active' : ''}"
          on:click={closeMenu}
          aria-label="Blog"
        >
          <span class="nav-icon mr-3">{@html IconBlog.svg}</span>
          Blog
        </a>
      </li>
      <li class="w-full p-2 rounded-lg hover:bg-gray-700">
        <a
          href="/sample"
          class="mobile-menu-link {currentPath === '/sample' ? 'active' : ''}"
          on:click={closeMenu}
          aria-label="Sample"
        >
          <span class="nav-icon mr-3">{@html IconSample.svg}</span>
          Sample
        </a>
      </li>
      <li class="w-full p-2 rounded-lg hover:bg-gray-700">
        <a
          href="/data-warehouse"
          class="mobile-menu-link {currentPath.startsWith('/data-warehouse') ? 'active' : ''}"
          on:click={closeMenu}
          aria-label="Data Warehouse"
        >
          <span class="nav-icon mr-3">{@html IconData.svg}</span>
          Data Warehouse
        </a>
      </li>
      <li class="w-full p-2 rounded-lg hover:bg-gray-700">
        <a
          href="/newsletter"
          class="mobile-menu-link {currentPath === '/newsletter' ? 'active' : ''}"
          on:click={closeMenu}
          aria-label="Newsletter"
        >
          <span class="nav-icon mr-3">{@html IconNewsletter.svg}</span>
          Newsletter
        </a>
      </li>
      <li class="w-full p-2 rounded-lg hover:bg-gray-700">
        <a
          href="/contact"
          class="mobile-menu-link {currentPath === '/contact' ? 'active' : ''}"
          on:click={closeMenu}
          aria-label="Contact"
        >
          <span class="nav-icon mr-3">{@html IconContact.svg}</span>
          Contact
        </a>
      </li>
    </ul>
  </div>
{/if}

<style>
  /* Remove body styling that was adding spacing */
  .mobile-menu {
    transition: all 0.3s ease;
    position: fixed;
    top: 64px; /* Match the height of the navbar */
    left: 0;
    right: 0;
    max-height: calc(100vh - 64px); /* Adjust based on navbar height */
    overflow-y: auto;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    z-index: 40;
  }

  .mobile-menu-link {
    display: flex;
    align-items: center;
    width: 100%;
    font-size: 1.125rem;
    color: #e2e8f0;
    transition: all 0.2s ease-in-out;
  }

  /* These styles are used in desktop view by NavLi elements */
  :global(.nav-item) {
    display: flex;
    align-items: stretch;
    transition: all 0.2s ease;
    border-radius: 0.375rem;
    margin: 0 0.25rem;
  }

  :global(.nav-item:hover) {
    background-color: rgba(255, 255, 255, 0.05);
  }

  .nav-button {
    padding: 0.75rem 1rem;
    color: #e2e8f0;
  }

  .active {
    font-weight: 600;
    color: #63b3ed;
  }

  .nav-icon {
    width: 1.25rem;
    height: 1.25rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
</style>