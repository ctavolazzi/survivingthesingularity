<script>
  import { Navbar, NavBrand, NavUl, NavLi } from 'flowbite-svelte';
  import { darkMode } from '$lib/stores/darkMode';
  import { gotoAndScrollTop } from '$lib/utils/navigation';
  import { page } from '$app/stores';
  import { IconHome, IconAbout, IconBlog, IconContact, IconSample, IconData, IconNewsletter } from '$lib/assets/Icons.svelte';
  import { onMount } from 'svelte';
  import { slide, fade } from 'svelte/transition';

  let navbar;
  let isMenuOpen = false;
  let isLargeScreen = false;
  // Define links that will only be shown in the hamburger menu
  const hamburgerOnlyLinks = ['/sample', '/data-warehouse'];

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

  // Custom navigation handler to ensure scroll to top
  function navigateTo(path, event) {
    if (event) event.preventDefault();

    // Only navigate if it's a different path
    if (path !== $page.url.pathname) {
      // Close menu if open
      if (isMenuOpen) closeMenu();

      // Navigate and scroll to top
      gotoAndScrollTop(path);
    }

    return false;
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
  <NavBrand href="/" on:click={(e) => navigateTo('/', e)}>
    <img src="/android-chrome-192x192.png" class="mr-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" loading="lazy">
    <span class="self-center whitespace-nowrap text-xl font-semibold text-white">
      Surviving the Singularity
    </span>
  </NavBrand>

  <div class="flex items-center lg:order-2">
    <!-- Always show hamburger menu button regardless of screen size -->
    <button
      class="hamburger-button ml-2 text-gray-300 hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-600 rounded-lg text-sm p-2.5 inline-flex items-center"
      on:click={toggleMenu}
      aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
      aria-expanded={isMenuOpen}
    >
      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
    </button>
  </div>

  {#if isLargeScreen}
    <NavUl class="flex items-center justify-end w-full lg:w-auto lg:order-1">
      <NavLi href="/about" class="nav-item {currentPath === '/about' ? 'active' : ''}" on:click={(e) => navigateTo('/about', e)}>
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">About</span>
          <span class="nav-icon ml-2">{@html IconAbout.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/blog" class="nav-item {currentPath === '/blog' ? 'active' : ''}" on:click={(e) => navigateTo('/blog', e)}>
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Blog</span>
          <span class="nav-icon ml-2">{@html IconBlog.svg}</span>
        </span>
      </NavLi>
      <!-- Data Warehouse and Sample links removed from desktop nav -->
      <NavLi href="/newsletter" class="nav-item {currentPath === '/newsletter' ? 'active' : ''}" on:click={(e) => navigateTo('/newsletter', e)}>
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Newsletter</span>
          <span class="nav-icon ml-2">{@html IconNewsletter.svg}</span>
        </span>
      </NavLi>
      <NavLi href="/contact" class="nav-item {currentPath === '/contact' ? 'active' : ''}" on:click={(e) => navigateTo('/contact', e)}>
        <span class="nav-button flex items-center h-full w-full">
          <span class="flex-grow text-left">Contact</span>
          <span class="nav-icon ml-2">{@html IconContact.svg}</span>
        </span>
      </NavLi>
    </NavUl>
  {/if}
</Navbar>

{#if isMenuOpen}
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
    <div class="container mx-auto px-4 py-6">
      <div class="flex justify-between items-center mb-6">
        <a href="/" class="flex items-center" on:click={(e) => navigateTo('/', e)}>
          <img src="/android-chrome-192x192.png" class="mr-3 h-8" alt="Surviving the Singularity Logo" loading="lazy">
          <span class="self-center text-xl font-semibold text-white">Surviving the Singularity</span>
        </a>
        <button
          class="text-gray-300 hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-600 rounded-lg text-sm p-2.5"
          on:click={closeMenu}
          aria-label="Close menu"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <nav class="space-y-4">
        <a
          href="/about"
          class="mobile-nav-item {currentPath === '/about' ? 'active' : ''}"
          on:click={(e) => navigateTo('/about', e)}
        >
          <span class="flex items-center">
            <span class="mr-3">{@html IconAbout.svg}</span>
            <span>About</span>
          </span>
        </a>
        <a
          href="/blog"
          class="mobile-nav-item {currentPath === '/blog' ? 'active' : ''}"
          on:click={(e) => navigateTo('/blog', e)}
        >
          <span class="flex items-center">
            <span class="mr-3">{@html IconBlog.svg}</span>
            <span>Blog</span>
          </span>
        </a>
        <a
          href="/sample"
          class="mobile-nav-item {currentPath === '/sample' ? 'active' : ''}"
          on:click={(e) => navigateTo('/sample', e)}
        >
          <span class="flex items-center">
            <span class="mr-3">{@html IconSample.svg}</span>
            <span>Sample</span>
          </span>
        </a>
        <a
          href="/data-warehouse"
          class="mobile-nav-item {currentPath.startsWith('/data-warehouse') ? 'active' : ''}"
          on:click={(e) => navigateTo('/data-warehouse', e)}
        >
          <span class="flex items-center">
            <span class="mr-3">{@html IconData.svg}</span>
            <span>Data Warehouse</span>
          </span>
        </a>
        <a
          href="/newsletter"
          class="mobile-nav-item {currentPath === '/newsletter' ? 'active' : ''}"
          on:click={(e) => navigateTo('/newsletter', e)}
        >
          <span class="flex items-center">
            <span class="mr-3">{@html IconNewsletter.svg}</span>
            <span>Newsletter</span>
          </span>
        </a>
        <a
          href="/contact"
          class="mobile-nav-item {currentPath === '/contact' ? 'active' : ''}"
          on:click={(e) => navigateTo('/contact', e)}
        >
          <span class="flex items-center">
            <span class="mr-3">{@html IconContact.svg}</span>
            <span>Contact</span>
          </span>
        </a>
      </nav>
    </div>
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

  /* Mobile navigation styles */
  .mobile-nav-item {
    display: block;
    padding: 0.75rem 1rem;
    color: #e5e7eb;
    border-radius: 0.5rem;
    transition: background-color 0.2s;
  }

  .mobile-nav-item:hover {
    background-color: #374151;
  }

  .mobile-nav-item.active {
    background-color: #4b5563;
    font-weight: 500;
  }
</style>