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

  // Desktop nav links — minimal: free value + depth
  const desktopLinks = [
    { href: '/blueprint', label: 'Blueprint' },
    { href: '/checklist', label: 'Checklist' },
  ];

  // Drawer — focused: free path and context only
  const drawerGroups = [
    {
      label: 'Start here',
      links: [
        {
          href: '/checklist',
          label: 'Free Readiness Checklist',
          sub: '7 moves. Free.',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>`,
        },
        {
          href: '/book',
          label: 'The Book',
          sub: 'Full draft, open now. Read it as it gets written.',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
        },
      ],
    },
    {
      label: 'More',
      links: [
        {
          href: '/book',
          label: 'The Book',
          sub: 'Full draft, read it as it\'s being written',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
        },
        {
          href: '/about',
          label: 'About',
          sub: 'The author and why this project exists',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
        },
      ],
    },
  ];

  // Context-aware CTA: changes based on where the user is in their journey
  $: currentPath = $page.url.pathname;
  $: ctaConfig = (() => {
    if (currentPath.startsWith('/early-access')) {
      return { label: 'Start Here Free', href: '/checklist' };
    }
    if (currentPath.startsWith('/checklist')) {
      return { label: 'Unlock Everything', href: '/early-access' };
    }
    if (currentPath.startsWith('/launch')) {
      return { label: 'Back the Book', href: '/launch#authors-edition' };
    }
    return { label: 'Get Early Access', href: '/early-access' };
  })();

  $: isActive = (href) => href === '/' ? currentPath === '/' : currentPath.startsWith(href);

  function open() {
    lastFocused = browser ? document.activeElement : null;
    const sbw = browser ? window.innerWidth - document.documentElement.clientWidth : 0;
    if (sbw > 0 && browser) document.body.style.paddingRight = sbw + 'px';
    isOpen = true;
    if (browser) document.body.style.overflow = 'hidden';
    tick().then(() => {
      if (drawerEl) {
        drawerEl.inert = false;
        drawerEl.classList.add('open');
        drawerEl.querySelectorAll('.drawer-section-label, .drawer-link, .drawer-divider, .drawer-cta')
          .forEach((el, i) => el.style.setProperty('--i', i));
      }
      if (overlayEl) overlayEl.classList.add('open');
      if (hamburgerEl) {
        hamburgerEl.setAttribute('aria-expanded', 'true');
        hamburgerEl.setAttribute('aria-label', 'Close menu');
        hamburgerEl.classList.add('is-open');
      }
    });
  }

  function close() {
    if (drawerEl) { drawerEl.classList.remove('open'); drawerEl.inert = true; }
    if (overlayEl) overlayEl.classList.remove('open');
    if (hamburgerEl) {
      hamburgerEl.setAttribute('aria-expanded', 'false');
      hamburgerEl.setAttribute('aria-label', 'Open menu');
      hamburgerEl.classList.remove('is-open');
    }
    isOpen = false;
    if (browser) {
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    }
    if (lastFocused?.focus) lastFocused.focus();
  }

  function toggle() { isOpen ? close() : open(); }

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
      if (axis === 'x') { dx = Math.max(0, mx); node.style.transform = `translateX(${dx}px)`; e.preventDefault(); }
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
</script>

<!-- Floating pill wrapper -->
<div class="nav-float" class:scrolled bind:this={navEl}>
  <nav class="nav-pill" aria-label="Main navigation">

    <!-- Brand -->
    <a href="/" class="nav-brand" on:click={(e) => navigateTo('/', e)} aria-label="Surviving the Singularity, home">
      <span class="nav-brand-mark">STS</span>
    </a>

    <div class="nav-sep" aria-hidden="true"></div>

    <!-- Desktop links -->
    <div class="nav-links" role="list">
      {#each desktopLinks as link}
        <a
          href={link.href}
          class="nav-link"
          class:active={isActive(link.href)}
          role="listitem"
          aria-current={isActive(link.href) ? 'page' : undefined}
          on:click={(e) => navigateTo(link.href, e)}
        >{link.label}</a>
      {/each}
    </div>

    <!-- Context-aware CTA -->
    <a
      href={ctaConfig.href}
      class="nav-cta"
      on:click={(e) => navigateTo(ctaConfig.href, e)}
    >
      {ctaConfig.label}
      <span class="nav-cta-icon" aria-hidden="true">
        <svg width="10" height="10" viewBox="0 0 12 12" fill="none">
          <path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
    </a>

    <!-- Hamburger (mobile) -->
    <button
      class="hamburger"
      bind:this={hamburgerEl}
      on:click={toggle}
      aria-label="Open menu"
      aria-expanded="false"
      aria-controls="site-drawer"
      type="button"
    >
      <span class="h-bar"></span>
      <span class="h-bar"></span>
      <span class="h-bar"></span>
    </button>

  </nav>
</div>

<!-- Overlay -->
<div class="drawer-overlay" bind:this={overlayEl} on:click={close} aria-hidden="true"></div>

<!-- Drawer -->
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
  <div class="drawer-head">
    <a href="/" class="drawer-head-brand" on:click={(e) => navigateTo('/', e)}>STS</a>
    <button class="drawer-close" on:click={close} aria-label="Close menu" type="button">
      <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
        <path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>
  </div>

  <div class="drawer-nav">
    {#each drawerGroups as group, gi}
      {#if gi > 0}<div class="drawer-divider"></div>{/if}
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

  <div class="drawer-footer">
    <a href={ctaConfig.href} class="drawer-cta" on:click={(e) => navigateTo(ctaConfig.href, e)}>
      {ctaConfig.label}
      <span class="drawer-cta-arrow">
        <svg width="14" height="14" viewBox="0 0 12 12" fill="none">
          <path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
    </a>
    <a href="/checklist" class="drawer-secondary-cta" on:click={(e) => navigateTo('/checklist', e)}>
      Free Checklist first
    </a>
  </div>
</aside>

<style>
  /* ── FLOAT WRAPPER ── */
  .nav-float {
    position: sticky;
    top: 0;
    z-index: 50;
    padding: 12px 16px;
    pointer-events: none; /* clicks pass through transparent area */
    background: transparent;
    transition: padding 0.3s ease;
  }
  .nav-float.scrolled {
    padding: 8px 16px;
  }

  /* ── PILL ── */
  .nav-pill {
    pointer-events: all; /* re-enable on the pill itself */
    display: flex;
    align-items: center;
    gap: 4px;
    max-width: max-content;
    margin: 0 auto;
    padding: 6px 6px 6px 16px;
    background: rgba(9, 14, 32, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 999px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    transition: background 0.3s ease, box-shadow 0.3s ease;
  }
  .nav-float.scrolled .nav-pill {
    background: rgba(4, 10, 26, 0.94);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }

  /* ── BRAND ── */
  .nav-brand {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: 0.08em;
    text-decoration: none;
    white-space: nowrap;
    padding-right: 4px;
    transition: opacity 0.15s ease;
  }
  .nav-brand:hover { opacity: 0.8; }

  .nav-sep {
    width: 1px;
    height: 16px;
    background: rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
    margin: 0 4px;
  }

  /* ── DESKTOP LINKS — hidden below 680px via media query ── */
  .nav-links {
    display: none; /* shown at 680px+ */
    align-items: center;
    gap: 2px;
  }

  .nav-link {
    padding: 6px 11px;
    font-size: 0.88rem;
    font-weight: 500;
    color: rgba(203, 213, 225, 0.75);
    text-decoration: none;
    border-radius: 999px;
    white-space: nowrap;
    transition: color 0.15s ease, background 0.15s ease;
  }
  .nav-link:hover { color: #f1f5f9; background: rgba(255, 255, 255, 0.05); }
  .nav-link.active { color: #f59e0b; background: rgba(245, 158, 11, 0.1); }

  /* ── CTA — always visible, even on mobile ── */
  .nav-cta {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 6px 6px 14px;
    background: #f59e0b;
    color: #0a0a0a;
    font-size: 0.95rem;
    font-weight: 800;
    border-radius: 999px;
    text-decoration: none;
    white-space: nowrap;
    flex-shrink: 0;
    margin-left: 4px;
    box-shadow: 0 2px 16px rgba(245, 158, 11, 0.35);
    transition: filter 0.15s ease, transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .nav-cta:hover { filter: brightness(1.08); transform: translateY(-1px); }
  .nav-cta:active { transform: scale(0.97); }
  .nav-cta-icon {
    width: 24px; height: 24px;
    background: rgba(0, 0, 0, 0.15);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .nav-cta:hover .nav-cta-icon { transform: translate(1px, -1px); }

  /* ── HAMBURGER — sized to balance STS on the opposite end ── */
  .hamburger {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.07);
    color: #94a3b8;
    cursor: pointer;
    flex-shrink: 0;
    margin-left: 2px;
    -webkit-tap-highlight-color: transparent;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .hamburger:hover { background: rgba(255, 255, 255, 0.12); color: #f1f5f9; }
  .hamburger:active { transform: scale(0.9); }

  .h-bar {
    position: absolute;
    left: 50%; top: 50%;
    width: 15px; height: 1.5px;
    border-radius: 1px;
    background: currentColor;
    transform-origin: center;
    transform: translate(-50%, -50%);
    transition: transform 0.3s cubic-bezier(0.68, -0.25, 0.27, 1.25), opacity 0.18s ease;
  }
  .h-bar:nth-child(1) { transform: translate(-50%, -5px); }
  .h-bar:nth-child(2) { transform: translate(-50%, 0); }
  .h-bar:nth-child(3) { transform: translate(-50%, 5px); }
  .hamburger.is-open .h-bar:nth-child(1) { transform: translate(-50%, 0) rotate(45deg); }
  .hamburger.is-open .h-bar:nth-child(2) { opacity: 0; transform: translate(-50%, 0) scaleX(0); }
  .hamburger.is-open .h-bar:nth-child(3) { transform: translate(-50%, 0) rotate(-45deg); }

  /* ── OVERLAY ── */
  .drawer-overlay {
    position: fixed; inset: 0; z-index: 200;
    background: rgba(2, 6, 23, 0.72);
    opacity: 0; pointer-events: none;
    transition: opacity 0.3s ease;
    backdrop-filter: blur(2px);
  }
  .drawer-overlay:global(.open) { opacity: 1; pointer-events: all; }

  /* ── DRAWER ── */
  .drawer {
    position: fixed; top: 0; right: 0; bottom: 0; z-index: 201;
    width: min(340px, 90vw);
    background: #070d1e;
    border-left: 1px solid rgba(245, 158, 11, 0.18);
    display: flex; flex-direction: column;
    transform: translateX(calc(100% + 4px));
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: -8px 0 40px rgba(0, 0, 0, 0.5);
    padding-bottom: env(safe-area-inset-bottom);
  }
  .drawer:global(.open) { transform: translateX(0); }

  .drawer-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    flex-shrink: 0;
  }
  .drawer-head-brand {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem; font-weight: 700;
    color: #f59e0b; letter-spacing: 0.08em;
    text-decoration: none;
  }
  .drawer-close {
    display: inline-flex; align-items: center; justify-content: center;
    width: 34px; height: 34px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.03);
    color: #94a3b8; cursor: pointer;
    transition: border-color 0.15s, color 0.15s, background 0.15s;
  }
  .drawer-close:hover { color: #f1f5f9; border-color: rgba(245, 158, 11, 0.3); background: rgba(245, 158, 11, 0.05); }

  .drawer-nav {
    flex: 1; overflow-y: auto;
    overscroll-behavior: contain;
    -webkit-overflow-scrolling: touch;
    padding: 12px 12px 16px;
  }

  .drawer-section { margin-bottom: 8px; }
  .drawer-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(245, 158, 11, 0.45);
    padding: 8px 10px 4px;
    animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.06s);
  }
  .drawer-divider {
    height: 1px; background: rgba(255, 255, 255, 0.04);
    margin: 4px 10px 10px;
    animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.06s);
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translateX(12px); }
    to   { opacity: 1; transform: translateX(0); }
  }

  .drawer-link {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 10px; min-height: 52px;
    text-decoration: none; color: #e2e8f0;
    border: 1px solid transparent;
    border-radius: 12px;
    transition: border-color 0.12s, background 0.12s, color 0.12s;
    animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.06s);
  }
  .drawer-link:hover { background: rgba(245, 158, 11, 0.04); border-color: rgba(245, 158, 11, 0.12); }
  .drawer-link.is-current { background: rgba(245, 158, 11, 0.06); border-color: rgba(245, 158, 11, 0.2); color: #f59e0b; }

  .drawer-link-icon {
    width: 34px; height: 34px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 9px; color: #94a3b8;
    transition: background 0.12s, border-color 0.12s, color 0.12s;
  }
  .drawer-link-icon :global(svg) { width: 14px; height: 14px; }
  .drawer-link:hover .drawer-link-icon { background: rgba(245, 158, 11, 0.08); border-color: rgba(245, 158, 11, 0.18); color: #f59e0b; }
  .drawer-link.is-current .drawer-link-icon { background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.22); color: #f59e0b; }

  .drawer-link-meta { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
  .drawer-link-label { font-size: 0.88rem; font-weight: 700; color: inherit; line-height: 1.25; }
  .drawer-link-sub { font-size: 0.78rem; font-weight: 400; color: #64748b; line-height: 1.3; }
  .drawer-link.is-current .drawer-link-sub { color: rgba(245, 158, 11, 0.5); }

  /* ── DRAWER FOOTER ── */
  .drawer-footer {
    padding: 14px 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    flex-shrink: 0;
    display: flex; flex-direction: column; gap: 8px;
  }
  .drawer-cta {
    display: flex; align-items: center; justify-content: center; gap: 8px;
    width: 100%; min-height: 48px; padding: 12px 20px;
    text-decoration: none; font-size: 0.9rem; font-weight: 800;
    background: #f59e0b; color: #0a0a0a;
    border-radius: 999px;
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
    transition: filter 0.15s, transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    animation-delay: calc(var(--i, 0) * 0.03s + 0.06s);
  }
  .drawer-cta:hover { filter: brightness(1.08); transform: translateY(-1px); }
  .drawer-cta-arrow { display: inline-flex; align-items: center; transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); }
  .drawer-cta:hover .drawer-cta-arrow { transform: translate(2px, -2px); }

  .drawer-secondary-cta {
    display: block; text-align: center;
    font-size: 0.8rem; font-weight: 600; color: #64748b;
    text-decoration: none;
    padding: 6px;
    transition: color 0.15s;
  }
  .drawer-secondary-cta:hover { color: #94a3b8; }

  /* ── RESPONSIVE ── */
  /* CTA is always visible. Links and sep hide below 960px. Hamburger always visible. */
  @media (min-width: 960px) {
    .nav-links { display: flex; }
    .nav-sep { display: block; }
  }

  @media (max-width: 959px) {
    .nav-pill { padding: 5px 5px 5px 12px; gap: 2px; }
    .nav-sep { display: none; }
    .nav-cta { font-size: 0.82rem; padding: 5px 5px 5px 11px; }
    .nav-cta-icon { width: 20px; height: 20px; }
  }

  /* ── REDUCED MOTION ── */
  @media (prefers-reduced-motion: reduce) {
    .drawer { transition: transform 0.001s; }
    .drawer-overlay { transition: opacity 0.12s; }
    .h-bar { transition: transform 0.001s, opacity 0.001s; }
    .drawer-section-label, .drawer-link, .drawer-divider, .drawer-cta { animation: none; }
    .nav-cta, .drawer-cta { transition: filter 0.001s; }
  }
</style>
