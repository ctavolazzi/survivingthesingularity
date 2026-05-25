<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { slide, fade } from 'svelte/transition';

  // Auth removed by design. Site is read-only - no user accounts, no sessions.
  // The `user` prop is kept as a no-op so existing call sites don't break;
  // it's never rendered or branched on anywhere in this component.
  export let user = null;
  void user;

  let isMenuOpen = false;
  let scrolled = false;

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }

  function closeMenu() {
    isMenuOpen = false;
    document.body.style.overflow = '';
  }

  function navigateTo(path, event) {
    if (event) event.preventDefault();
    if (path !== $page.url.pathname) {
      if (isMenuOpen) closeMenu();
      goto(path);
    }
    return false;
  }

  onMount(() => {
    const handleScroll = () => {
      scrolled = window.scrollY > 20;
    };
    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  });

  $: currentPath = $page.url.pathname;

  const navLinks = [
    { href: '/why', label: 'Why' },
    { href: '/book', label: 'Book' },
    { href: '/blueprint', label: 'Blueprint' },
    { href: '/blog', label: 'Blog' },
  ];
</script>

<nav class="navbar" class:scrolled>
  <div class="navbar-inner">
    <a href="/" class="nav-brand" on:click={(e) => navigateTo('/', e)}>
      <span class="nav-brand-mark">STS</span>
      <span class="nav-brand-divider"></span>
      <span class="nav-brand-text">Surviving the Singularity</span>
    </a>

    <div class="nav-links-desktop">
      {#each navLinks as link}
        <a
          href={link.href}
          class="nav-link"
          class:active={currentPath.startsWith(link.href)}
          on:click={(e) => navigateTo(link.href, e)}
        >
          {link.label}
        </a>
      {/each}
    </div>

    <div class="nav-right">
      <button
        class="hamburger-button"
        on:click={toggleMenu}
        aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
        aria-expanded={isMenuOpen}
      >
        <span class="hamburger-line" class:open={isMenuOpen}></span>
        <span class="hamburger-line" class:open={isMenuOpen}></span>
        <span class="hamburger-line" class:open={isMenuOpen}></span>
      </button>
    </div>
  </div>
</nav>

{#if isMenuOpen}
  <div
    class="menu-overlay"
    on:click={closeMenu}
    on:keydown={(e) => e.key === 'Escape' && closeMenu()}
    role="button"
    tabindex="0"
    aria-label="Close menu"
    transition:fade={{ duration: 200 }}
  ></div>

  <div class="mobile-menu" transition:slide={{ duration: 300 }}>
    <div class="mobile-menu-inner">
      {#each navLinks as link, i}
        <a
          href={link.href}
          class="mobile-link"
          class:active={currentPath.startsWith(link.href)}
          on:click={(e) => navigateTo(link.href, e)}
          style="animation-delay: {i * 50}ms"
        >
          <span class="mobile-link-text">{link.label}</span>
          <svg class="mobile-link-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 4L10 8L6 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
      {/each}
    </div>
  </div>
{/if}

<style>
  .navbar {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(2, 6, 23, 0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(148, 163, 184, 0.06);
    transition: all 0.3s ease;
  }

  .navbar.scrolled {
    background: rgba(2, 6, 23, 0.95);
    border-bottom-color: rgba(245, 158, 11, 0.15);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
  }

  .navbar-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    transition: opacity 0.2s;
  }

  .nav-brand:hover {
    opacity: 0.85;
  }

  .nav-brand-mark {
    font-size: 0.85rem;
    font-weight: 800;
    color: #f59e0b;
    letter-spacing: 0.08em;
    font-family: 'JetBrains Mono', monospace;
  }

  .nav-brand-divider {
    width: 1px;
    height: 20px;
    background: rgba(148, 163, 184, 0.2);
  }

  .nav-brand-text {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e2e8f0;
    letter-spacing: -0.01em;
  }

  .nav-links-desktop {
    display: none;
    align-items: center;
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.5rem 1rem;
    color: #94a3b8;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    border-radius: 8px;
    transition: all 0.2s ease;
  }

  .nav-link:hover {
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.05);
  }

  .nav-link.active {
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
  }

  .hamburger-button {
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding: 0.5rem;
    background: none;
    border: none;
    cursor: pointer;
    width: 40px;
    height: 40px;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    transition: background 0.2s;
  }

  .hamburger-button:hover {
    background: rgba(255, 255, 255, 0.05);
  }

  .hamburger-line {
    display: block;
    width: 20px;
    height: 2px;
    background: #94a3b8;
    border-radius: 2px;
    transition: all 0.3s ease;
  }

  .hamburger-line.open:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
  }

  .hamburger-line.open:nth-child(2) {
    opacity: 0;
  }

  .hamburger-line.open:nth-child(3) {
    transform: rotate(-45deg) translate(5px, -5px);
  }

  .menu-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    z-index: 40;
  }

  .mobile-menu {
    position: fixed;
    top: 64px;
    left: 0;
    right: 0;
    background: rgba(15, 23, 42, 0.98);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(245, 158, 11, 0.15);
    z-index: 45;
    max-height: calc(100vh - 64px);
    overflow-y: auto;
  }

  .mobile-menu-inner {
    padding: 1rem 1.5rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .mobile-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    color: #cbd5e1;
    text-decoration: none;
    font-size: 1rem;
    font-weight: 500;
    border-radius: 12px;
    transition: all 0.2s ease;
    animation: slideIn 0.3s ease forwards;
    opacity: 0;
  }

  @keyframes slideIn {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
  }

  .mobile-link:hover {
    background: rgba(245, 158, 11, 0.08);
    color: #f1f5f9;
  }

  .mobile-link.active {
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
  }

  .mobile-link-arrow {
    color: #475569;
    transition: transform 0.2s;
  }

  .mobile-link:hover .mobile-link-arrow {
    transform: translateX(3px);
    color: #f59e0b;
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  @media (min-width: 768px) {
    .nav-links-desktop {
      display: flex;
    }

    .hamburger-button {
      display: none;
    }
  }

  @media (max-width: 480px) {
    .nav-brand-text {
      display: none;
    }

    .nav-brand-divider {
      display: none;
    }
  }
</style>
