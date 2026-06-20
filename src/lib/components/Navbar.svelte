<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { onMount, onDestroy, tick } from 'svelte';
  import { browser } from '$app/environment';

  export let user = null;
  void user;

  let isOpen = false;
  let drawerEl;
  let overlayEl;
  let hamburgerEl;
  let navEl;
  let lastFocused = null;
  let scrolled = false;

  // Nav structure: flat links for desktop, grouped for drawer
  const desktopLinks = [
    { href: '/agi',       label: 'What is AGI' },
    { href: '/evidence',  label: 'Evidence' },
    { href: '/why',       label: 'Why' },
    { href: '/blueprint', label: 'Blueprint' },
    { href: '/shouse',    label: 'Game' },
    { href: '/book',      label: 'Book' },
    { href: '/blog',      label: 'Blog' },
    { href: '/checklist', label: 'Free Checklist', accent: true },
  ];

  const drawerGroups = [
    {
      label: 'Start here',
      links: [
        {
          href: '/checklist',
          label: 'Free Readiness Checklist',
          sub: '12 moves to make before AGI',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>`,
        },
        {
          href: '/agi',
          label: 'What is AGI?',
          sub: 'The singularity, explained',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>`,
        },
        {
          href: '/evidence',
          label: 'The Evidence',
          sub: 'See it happen: footage + papers',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>`,
        },
        {
          href: '/why',
          label: 'Why Now',
          sub: 'The case for acting before 2027',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>`,
        },
      ],
    },
    {
      label: 'The Work',
      links: [
        {
          href: '/blueprint',
          label: 'Blueprint',
          sub: '8-chapter strategy guide',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
        },
        {
          href: '/shouse',
          label: 'Shouse Builder',
          sub: 'Build the $25k shouse, a 3D strategy game',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 12 2 21 11 21 22 3 22"/><path d="M9 22v-6h6v6"/><path d="M12 8v3"/></svg>`,
        },
        {
          href: '/book',
          label: 'The Book',
          sub: '12 chapters, free sample available',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
        },
        {
          href: '/blog',
          label: 'Blog',
          sub: 'Field notes and dispatches',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>`,
        },
      ],
    },
    {
      label: 'Three Pillars',
      links: [
        {
          href: '/blueprint/local-ai',
          label: 'Learn the Tools',
          sub: 'Teach yourself modern AI',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
        },
        {
          href: '/blueprint/robotics',
          label: 'Open-Source Robotics',
          sub: 'Automate food and labor',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>`,
        },
        {
          href: '/blueprint/physical-exit',
          label: 'The Physical Exit',
          sub: 'Land, shouse, independence',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 12 2 21 11 21 22 15 22 15 15 9 15 9 22 3 22"/></svg>`,
        },
      ],
    },
    {
      label: 'More',
      links: [
        {
          href: '/about',
          label: 'About',
          sub: 'The author and the mission',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
        },
      ],
    },
  ];

  function open() {
    lastFocused = browser ? document.activeElement : null;
    const sbw = browser ? window.innerWidth - document.documentElement.clientWidth : 0;
    if (sbw > 0 && browser) {
      document.body.style.paddingRight = sbw + 'px';
      if (navEl) navEl.style.paddingRight = sbw + 'px';
    }
    isOpen = true;
    if (browser) document.body.style.overflow = 'hidden';
    tick().then(() => {
      if (drawerEl) {
        drawerEl.inert = false;
        drawerEl.classList.add('open');
      }
      if (overlayEl) overlayEl.classList.add('open');
      if (hamburgerEl) {
        hamburgerEl.setAttribute('aria-expanded', 'true');
        hamburgerEl.setAttribute('aria-label', 'Close site menu');
        hamburgerEl.classList.add('is-open');
      }
      // Stagger animation indices
      if (drawerEl) {
        drawerEl.querySelectorAll('.drawer-section-label, .drawer-link, .drawer-divider, .drawer-cta')
          .forEach((el, i) => el.style.setProperty('--i', i));
      }
    });
  }

  function close() {
    if (drawerEl) {
      drawerEl.classList.remove('open');
      drawerEl.inert = true;
    }
    if (overlayEl) overlayEl.classList.remove('open');
    if (hamburgerEl) {
      hamburgerEl.setAttribute('aria-expanded', 'false');
      hamburgerEl.setAttribute('aria-label', 'Open site menu');
      hamburgerEl.classList.remove('is-open');
    }
    isOpen = false;
    if (browser) {
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
      if (navEl) navEl.style.paddingRight = '';
    }
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  function toggle() {
    if (isOpen) close(); else open();
  }

  function navigateTo(path, event) {
    if (event) event.preventDefault();
    close();
    if (path !== $page.url.pathname) goto(path);
  }

  function handleKey(e) {
    if (e.key === 'Escape' && isOpen) { close(); return; }
    if (e.key === 'Tab' && isOpen && drawerEl) {
      const focusable = drawerEl.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }

  function handleScroll() { scrolled = window.scrollY > 20; }

  // Swipe-to-dismiss (right swipe closes drawer)
  function enableSwipe(node) {
    let startX = 0, startY = 0, dx = 0, active = false, axis = null;
    function onStart(e) {
      if (!isOpen || e.touches.length !== 1) return;
      const t = e.touches[0];
      startX = t.clientX; startY = t.clientY; dx = 0; active = true; axis = null;
      node.style.transition = 'none';
    }
    function onMove(e) {
      if (!active) return;
      const t = e.touches[0];
      const mx = t.clientX - startX, my = t.clientY - startY;
      if (axis === null && (Math.abs(mx) > 8 || Math.abs(my) > 8)) {
        axis = Math.abs(mx) > Math.abs(my) ? 'x' : 'y';
      }
      if (axis === 'y') { active = false; node.style.transition = ''; return; }
      if (axis === 'x') {
        dx = Math.max(0, mx);
        node.style.transform = `translateX(${dx}px)`;
        e.preventDefault();
      }
    }
    function onEnd() {
      if (!active) return;
      active = false;
      node.style.transition = '';
      node.style.transform = '';
      if (dx > 80) close();
    }
    node.addEventListener('touchstart', onStart, { passive: true });
    node.addEventListener('touchmove', onMove, { passive: false });
    node.addEventListener('touchend', onEnd);
    node.addEventListener('touchcancel', onEnd);
    return { destroy() {
      node.removeEventListener('touchstart', onStart);
      node.removeEventListener('touchmove', onMove);
      node.removeEventListener('touchend', onEnd);
      node.removeEventListener('touchcancel', onEnd);
    }};
  }

  onMount(() => {
    if (!browser) return;
    if (drawerEl) drawerEl.inert = true;
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('keydown', handleKey);
  });

  onDestroy(() => {
    if (!browser) return;
    window.removeEventListener('scroll', handleScroll);
    window.removeEventListener('keydown', handleKey);
    document.body.style.overflow = '';
  });

  $: currentPath = $page.url.pathname;
  $: isActive = (href) => href === '/' ? currentPath === '/' : currentPath.startsWith(href);
</script>

<nav class="navbar" class:scrolled bind:this={navEl}>
  <div class="navbar-inner">

    <!-- Brand -->
    <a href="/" class="nav-brand" on:click={(e) => navigateTo('/', e)} aria-label="Surviving the Singularity, home">
      <span class="nav-brand-mark">STS</span>
      <span class="nav-brand-divider" aria-hidden="true"></span>
      <span class="nav-brand-text">Surviving the Singularity</span>
    </a>

    <div class="nav-right">
      <!-- Desktop links -->
      <nav class="nav-links-desktop" aria-label="Primary navigation">
        {#each desktopLinks as link}
          <a
            href={link.href}
            class="nav-link"
            class:active={isActive(link.href)}
            class:nav-link-accent={link.accent}
            aria-current={isActive(link.href) ? 'page' : undefined}
            on:click={(e) => navigateTo(link.href, e)}
          >{link.label}</a>
        {/each}
      </nav>

      <!-- Desktop CTA -->
      <a href="/blueprint" class="nav-cta" on:click={(e) => navigateTo('/blueprint', e)}>
        Read Blueprint
        <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>

      <!-- Hamburger -->
      <button
        class="hamburger"
        bind:this={hamburgerEl}
        on:click={toggle}
        aria-label="Open site menu"
        aria-expanded="false"
        aria-controls="site-drawer"
        type="button"
      >
        <span class="h-bar"></span>
        <span class="h-bar"></span>
        <span class="h-bar"></span>
      </button>
    </div>

  </div>
</nav>

<!-- Drawer overlay -->
<div
  class="drawer-overlay"
  bind:this={overlayEl}
  on:click={close}
  aria-hidden="true"
></div>

<!-- Drawer panel -->
<aside
  id="site-drawer"
  class="drawer"
  bind:this={drawerEl}
  role="dialog"
  aria-modal="true"
  aria-label="Site menu"
  aria-hidden={!isOpen}
  use:enableSwipe
>
  <!-- Drawer head -->
  <div class="drawer-head">
    <span class="drawer-head-title">Site Menu</span>
    <button class="drawer-close" on:click={close} aria-label="Close site menu" type="button">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
        <path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>
  </div>

  <!-- Drawer nav -->
  <div class="drawer-nav">
    {#each drawerGroups as group, gi}
      {#if gi > 0}
        <div class="drawer-divider"></div>
      {/if}
      <div class="drawer-section">
        <p class="drawer-section-label">{group.label}</p>
        {#each group.links as link}
          <a
            href={link.href}
            class="drawer-link"
            class:is-current={isActive(link.href)}
            aria-current={isActive(link.href) ? 'page' : undefined}
            on:click={(e) => navigateTo(link.href, e)}
          >
            <span class="drawer-link-icon" aria-hidden="true">{@html link.icon}</span>
            <span class="drawer-link-meta">
              <span class="drawer-link-label">{link.label}</span>
              <span class="drawer-link-sub">{link.sub}</span>
            </span>
          </a>
        {/each}
      </div>
    {/each}
  </div>

  <!-- Drawer footer CTA -->
  <div class="drawer-footer">
    <a href="/blueprint" class="drawer-cta" on:click={(e) => navigateTo('/blueprint', e)}>
      Read the Full Blueprint
      <span class="drawer-cta-arrow">→</span>
    </a>
  </div>
</aside>

<style>
  /* ── NAVBAR ── */
  .navbar {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(2, 6, 23, 0.82);
    backdrop-filter: blur(18px) saturate(150%);
    -webkit-backdrop-filter: blur(18px) saturate(150%);
    border-bottom: 1px solid rgba(148, 163, 184, 0.06);
    transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
  }

  .navbar.scrolled {
    background: rgba(2, 6, 23, 0.96);
    border-bottom-color: rgba(245, 158, 11, 0.15);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
  }

  .navbar-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding-left: max(1rem, env(safe-area-inset-left));
    padding-right: max(1rem, env(safe-area-inset-right));
  }

  /* ── BRAND ── */
  .nav-brand {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    text-decoration: none;
    flex-shrink: 1;
    min-width: 0;
    transition: opacity 0.2s;
  }
  .nav-brand:hover { opacity: 0.8; }

  .nav-brand-mark {
    font-size: 0.8rem;
    font-weight: 800;
    color: #f59e0b;
    letter-spacing: 0.1em;
    font-family: var(--font-primary);
    flex-shrink: 0;
  }

  .nav-brand-divider {
    width: 1px;
    height: 18px;
    background: rgba(148, 163, 184, 0.2);
    flex-shrink: 0;
  }

  .nav-brand-text {
    font-size: 0.88rem;
    font-weight: 600;
    color: #e2e8f0;
    letter-spacing: -0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* ── RIGHT SIDE ── */
  .nav-right {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    flex-shrink: 0;
  }

  /* ── DESKTOP LINKS ── */
  .nav-links-desktop {
    display: none;
    align-items: center;
    gap: 0.15rem;
  }

  .nav-link {
    padding: 0.45rem 0.85rem;
    color: #dde4ef;
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 500;
    border-radius: 7px;
    transition: color 0.15s ease, background 0.15s ease;
    min-height: 36px;
    display: flex;
    align-items: center;
  }
  .nav-link:hover { color: #e2e8f0; background: rgba(255, 255, 255, 0.04); }
  .nav-link.active { color: #f59e0b; background: rgba(245, 158, 11, 0.08); }
  .nav-link-accent {
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
  }
  .nav-link-accent:hover { background: rgba(245, 158, 11, 0.1); color: #fbbf24; }

  /* ── DESKTOP CTA ── */
  .nav-cta {
    display: none;
    align-items: center;
    gap: 0.35rem;
    padding: 0.45rem 1rem;
    min-height: 36px;
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 700;
    text-decoration: none;
    letter-spacing: 0.01em;
    transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .nav-cta:hover {
    background: rgba(245, 158, 11, 0.18);
    border-color: rgba(245, 158, 11, 0.55);
    transform: translateY(-1px);
  }

  /* ── HAMBURGER ── */
  .hamburger {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border: none;
    border-radius: 10px;
    background: transparent;
    color: #dde4ef;
    cursor: pointer;
    flex-shrink: 0;
    -webkit-tap-highlight-color: transparent;
    transition: color 0.15s ease, background 0.15s ease;
  }
  .hamburger:hover { color: #e2e8f0; background: rgba(255, 255, 255, 0.04); }
  .hamburger:active { transform: scale(0.92); }

  .h-bar {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 18px;
    height: 2px;
    border-radius: 2px;
    background: currentColor;
    transform-origin: center;
    transform: translate(-50%, -50%);
    transition: transform 0.32s cubic-bezier(0.68, -0.25, 0.27, 1.25), opacity 0.18s ease;
  }
  .h-bar:nth-child(1) { transform: translate(-50%, -6px); transition-delay: 0.05s; }
  .h-bar:nth-child(2) { transform: translate(-50%, 0); }
  .h-bar:nth-child(3) { transform: translate(-50%, 6px); transition-delay: 0.05s; }

  .hamburger.is-open .h-bar:nth-child(1) { transform: translate(-50%, 0) rotate(45deg); transition-delay: 0.03s; }
  .hamburger.is-open .h-bar:nth-child(2) { opacity: 0; transform: translate(-50%, 0) scaleX(0); }
  .hamburger.is-open .h-bar:nth-child(3) { transform: translate(-50%, 0) rotate(-45deg); transition-delay: 0.03s; }

  /* ── OVERLAY ── */
  .drawer-overlay {
    position: fixed;
    inset: 0;
    z-index: 200;
    background: rgba(2, 6, 23, 0.6);
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }
  .drawer-overlay:global(.open) {
    opacity: 1;
    pointer-events: all;
  }

  /* ── DRAWER PANEL ── */
  .drawer {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 201;
    width: min(320px, 88vw);
    background: rgba(10, 15, 35, 0.98);
    border-left: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 18px 0 0 18px;
    box-shadow: -4px 0 0 0 rgba(245, 158, 11, 0.1), -20px 0 60px rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    transform: translateX(calc(100% + 4px));
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    font-family: 'Inter', system-ui, sans-serif;
    padding-bottom: env(safe-area-inset-bottom);
  }
  .drawer:global(.open) { transform: translateX(0); }

  /* ── DRAWER HEAD ── */
  .drawer-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    height: 60px;
    flex-shrink: 0;
  }

  .drawer-head-title {
    font-size: 0.76rem;
    font-weight: 800;
    color: rgba(245, 158, 11, 0.7);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-family: var(--font-primary);
  }

  .drawer-close {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.03);
    color: #dde4ef;
    cursor: pointer;
    transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.08);
  }
  .drawer-close:hover {
    color: #e2e8f0;
    border-color: rgba(245, 158, 11, 0.25);
    background: rgba(245, 158, 11, 0.05);
    box-shadow: 1px 1px 0 rgba(245, 158, 11, 0.1);
  }

  /* ── DRAWER NAV ── */
  .drawer-nav {
    flex: 1;
    overflow-y: auto;
    overscroll-behavior: contain;
    -webkit-overflow-scrolling: touch;
    padding: 10px 10px 16px;
  }

  .drawer-section { margin-bottom: 16px; }

  .drawer-section-label {
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(245, 158, 11, 0.55);
    padding: 0 8px;
    margin-bottom: 4px;
    font-family: var(--font-primary);
    /* stagger animation */
    animation: drawerItemIn 0.44s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.08s);
  }

  .drawer-divider {
    height: 1px;
    background: rgba(255, 255, 255, 0.05);
    margin: 4px 8px 14px;
    /* stagger animation */
    animation: drawerItemIn 0.44s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.08s);
  }

  @keyframes drawerItemIn {
    from { opacity: 0; transform: translateX(16px); }
    to   { opacity: 1; transform: translateX(0); }
  }

  .drawer-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 10px;
    text-decoration: none;
    color: #e9eef5;
    font-size: 0.95rem;
    font-weight: 600;
    border: 1px solid transparent;
    border-radius: 12px;
    transition: border-color 0.12s ease, background 0.12s ease, color 0.12s ease, box-shadow 0.12s ease, transform 0.12s ease;
    min-height: 48px;
    /* stagger animation */
    animation: drawerItemIn 0.44s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.08s);
  }

  .drawer-link:hover {
    background: rgba(245, 158, 11, 0.05);
    border-color: rgba(245, 158, 11, 0.15);
    color: #f1f5f9;
    box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.08);
    transform: translate(-1px, -1px);
  }

  .drawer-link.is-current {
    background: rgba(245, 158, 11, 0.06);
    border-color: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
    box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.12);
  }

  .drawer-link-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 9px;
    color: #dde4ef;
    transition: background 0.12s ease, border-color 0.12s ease, color 0.12s ease, transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .drawer-link-icon :global(svg) { width: 15px; height: 15px; }

  .drawer-link:hover .drawer-link-icon {
    background: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
    transform: rotate(-4deg) scale(1.1);
  }
  .drawer-link.is-current .drawer-link-icon {
    background: rgba(245, 158, 11, 0.12);
    border-color: rgba(245, 158, 11, 0.25);
    color: #f59e0b;
  }

  .drawer-link-meta {
    display: flex;
    flex-direction: column;
    gap: 1px;
    min-width: 0;
  }

  .drawer-link-label { font-weight: 700; color: inherit; line-height: 1.2; }

  .drawer-link-sub {
    font-size: 0.82rem;
    font-weight: 500;
    color: #dde4ef;
    line-height: 1.3;
  }
  .drawer-link.is-current .drawer-link-sub { color: rgba(245, 158, 11, 0.55); }

  /* ── DRAWER FOOTER ── */
  .drawer-footer {
    padding: 12px 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    flex-shrink: 0;
  }

  .drawer-cta {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    min-height: 50px;
    padding: 13px 20px;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 700;
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    box-shadow: 3px 3px 0 rgba(245, 158, 11, 0.12);
    transition: background 0.12s ease, box-shadow 0.12s ease, transform 0.12s ease, border-color 0.12s ease;
    /* stagger animation */
    animation: drawerItemIn 0.44s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.08s);
  }
  .drawer-cta:hover {
    background: rgba(245, 158, 11, 0.16);
    border-color: rgba(245, 158, 11, 0.5);
    box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.15);
    transform: translate(1px, 1px);
  }

  .drawer-cta-arrow {
    display: inline-block;
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .drawer-cta:hover .drawer-cta-arrow { transform: translateX(4px); }

  /* ── BREAKPOINTS ── */
  @media (min-width: 640px) {
    .navbar-inner { padding: 0 1.5rem; height: 64px; }
    .drawer-head { height: 64px; }
  }

  @media (min-width: 768px) {
    .nav-links-desktop { display: flex; }
    .nav-cta { display: flex; }
  }

  @media (max-width: 480px) {
    .nav-brand-text { display: none; }
    .nav-brand-divider { display: none; }
  }

  /* ── REDUCED MOTION ── */
  @media (prefers-reduced-motion: reduce) {
    .drawer { transition: transform 0.001s linear; }
    .h-bar { transition: transform 0.001s, opacity 0.001s; }
    .drawer-overlay { transition: opacity 0.12s ease; }
    .drawer-section-label,
    .drawer-link,
    .drawer-divider,
    .drawer-cta { animation: none; }
    .drawer-link-icon { transition: none; }
    .drawer-cta-arrow { transition: none; }
  }
</style>
