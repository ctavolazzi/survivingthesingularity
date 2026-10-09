<script>
  import '../app.css';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import DisclaimerBanner from '$lib/components/DisclaimerBanner.svelte';
  import ToastContainer from '$lib/components/ToastContainer.svelte';
  import CommandPalette from '$lib/components/CommandPalette.svelte';
  import InfoModal from '$lib/components/InfoModal.svelte';
  import WhiteRabbitPanel from '$lib/components/WhiteRabbitPanel.svelte';
  import SplashLoader from '$lib/components/SplashLoader.svelte';
  import { createRabbit } from '$lib/debug/white-rabbit.js';
  import { browser, dev } from '$app/environment';
  import { afterNavigate, beforeNavigate } from '$app/navigation';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';

  // Self-referential canonical URL for every page. Strips query/hash and any
  // trailing slash so duplicate-content variants resolve to one canonical.
  const SITE = 'https://survivingthesingularity.com';
  $: canonicalPath = $page.url.pathname.replace(/\/+$/, '') || '/';
  $: canonical = SITE + canonicalPath;

  // The continuous reader (/read) is a reading surface, not a page of the
  // marketing site: it brings its own sticky chapter bar, and the floating
  // navbar would sit on top of it. Site chrome steps aside there. The reader
  // links back out from its own chapter drawer.
  $: isReader = $page.url.pathname === '/read';

  // The auth surfaces (/signup and the /auth/* endpoints it redirects through)
  // are the same kind of exception, for the same reason: the signup page was
  // designed as a standalone full-page surface and brings its own masthead,
  // its own footer, and its own consent language. Rendered inside the site
  // chrome it produced two headers stacked on each other and the fixed consent
  // banner sitting across the submit button.
  //
  // The DisclaimerBanner is the one worth spelling out. It is a passive "by
  // using this site you agree" notice, and on this page it competed with an
  // explicit "I agree to the Terms and the Privacy Policy" checkbox that gates
  // the form. Two consent affordances disagreeing about what you have agreed
  // to is worse than either alone, and the checkbox is the stronger record:
  // it is per-account, it is refused if unticked, and sql/016 stamps the time
  // it happened. The page also links Terms and Privacy in its own footer, so
  // nothing becomes unreachable.
  //
  // SplashLoader steps aside too. A 1.56s boot animation in front of a signup
  // form is friction on the one page whose whole job is a conversion.
  $: isAuthSurface =
    $page.url.pathname === '/signup' || $page.url.pathname.startsWith('/auth/');

  // Routes that supply their own chrome and want the site's out of the way.
  $: isBareSurface = isReader || isAuthSurface;

  // White-rabbit is a debug instrumentation system - only enabled in dev so we
  // don't ship behavioral tracking or expose internals to production visitors.
  let sessionRabbit = null;

  export let data;

  let commandPaletteOpen = false;
  let navigating = false;
  let thankYouOpen = false;

  // Force dark mode
  $: if (browser) {
    document.documentElement.classList.add('dark');
  }

  beforeNavigate(() => {
    navigating = true;
  });

  afterNavigate(({ from, to }) => {
    navigating = false;
    if (browser) {
      if (dev && sessionRabbit && from && to && from.url.pathname !== to.url.pathname) {
        sessionRabbit.watchNavigation(from.url.pathname, to.url.pathname);
      }
      const fromPath = from?.url.pathname;
      const toPath = to?.url.pathname;
      const toHash = to?.url.hash;
      if ((!fromPath || fromPath !== toPath) && !toHash) {
        window.scrollTo({ top: 0, behavior: 'instant' });
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
      }
    }
  });

  onMount(() => {
    if (browser) {
      if (dev) {
        sessionRabbit = createRabbit('session', { userAgent: navigator.userAgent });
        sessionRabbit.mark('app-mounted');
        sessionRabbit.info('Session started', { path: window.location.pathname });
      }
      if (!window.location.hash) {
        window.scrollTo(0, 0);
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
      }
    }
  });
</script>

<svelte:head>
  <link rel="canonical" href={canonical} />
</svelte:head>

<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- 1.56s cold-start boot sequence. Overlays the page rather than blocking it,
     so the site loads underneath and is ready the moment the wipe clears. -->
{#if !isAuthSurface}
  <SplashLoader />
{/if}

<div class="app">
  {#if !isAuthSurface}
    <DisclaimerBanner />
  {/if}
  {#if !isBareSurface}
    <Navbar user={data?.user} />
  {/if}

  <!-- Page transition loading bar -->
  {#if navigating}
    <div class="page-loading-bar" in:fade={{ duration: 100 }}>
      <div class="page-loading-fill"></div>
    </div>
  {/if}

  <main id="main-content" tabindex="-1">
    <slot />
  </main>
  {#if !isBareSurface}
    <button type="button" class="site-thankyou" on:click={() => thankYouOpen = true}>
      Thank you for being here ❣️
    </button>
  {/if}
  <InfoModal open={thankYouOpen} title="Thank You" on:close={() => thankYouOpen = false}>
    <p>Most people look away from what's coming. You didn't.</p>
    <p>You're willing to sit with hard ideas instead of dismissing them. Willing to ask what to build instead of who to blame. That's rarer than it should be, and it matters more than you think.</p>
    <p>You don't need every answer. You just need to keep paying attention and keep building.</p>
    <p>That's how hope actually comes back: not from certainty, but from people like you staying in the room.</p>
    <p>Thank you for being here.</p>
  </InfoModal>
  {#if !isBareSurface}
    <Footer />
  {/if}
  <ToastContainer />
  <CommandPalette bind:open={commandPaletteOpen} />
  {#if dev}
    <WhiteRabbitPanel />
  {/if}
</div>

<style>
  :global(html, body) {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    background-color: #020617;
    color: #e2e8f0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  .app {
    display: grid;
    grid-template-rows: auto 1fr auto;
    /* Without an explicit column the implicit grid column is sized to
       max-content, so wide content expands the page past the viewport and
       gets clipped by overflow-x:hidden. minmax(0,1fr) clamps it to the
       viewport and lets content reflow. */
    grid-template-columns: minmax(0, 1fr);
    min-height: 100vh;
    min-height: 100dvh;
    /* Space claimed by the fixed consent banner. Set by DisclaimerBanner while
       it is on screen, 0 otherwise. Custom properties inherit, so the banner can
       set it on <body> and it resolves here.
       Applied on .app rather than on body: an identical declaration on body
       computed to 0px no matter how it was written, while the same expression
       resolved correctly on other elements, so something in the cascade there
       wins in a way that was not worth chasing. This element is owned entirely
       by this file, which makes the outcome predictable. */
    padding-bottom: var(--consent-reserve, 0px);
  }

  /* DisclaimerBanner is fixed-position, so it reserves no layout space of its
     own. Until 2026-07-29 nothing reserved space for it either, and at the end
     of a page it simply sat on top of whatever was there. See the padding-bottom
     above and the comment block in DisclaimerBanner.svelte. */

  main {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-width: 0;
    box-sizing: border-box;
  }

  .site-thankyou {
    display: block;
    width: 100%;
    text-align: center;
    padding: clamp(24px, 4vw, 40px) 20px;
    font-size: clamp(0.9rem, 2vw, 1rem);
    font-family: inherit;
    color: rgba(148, 163, 184, 0.5);
    letter-spacing: 0.02em;
    background: none;
    border: none;
    cursor: pointer;
    transition: color 0.2s ease;
  }
  .site-thankyou:hover,
  .site-thankyou:focus-visible {
    color: rgba(245, 158, 11, 0.75);
  }

  /* Page loading bar */
  .page-loading-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    z-index: 9999;
    background: transparent;
  }

  .page-loading-fill {
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #f97316, #f59e0b);
    background-size: 200% 100%;
    animation: loading-shimmer 1s ease-in-out infinite, loading-grow 2s ease forwards;
    border-radius: 0 1px 1px 0;
    box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
  }

  @keyframes loading-grow {
    0% { width: 0%; }
    20% { width: 30%; }
    50% { width: 60%; }
    80% { width: 85%; }
    100% { width: 95%; }
  }

  @keyframes loading-shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }

  /* Global micro-interaction utilities */
  :global(.magnetic-hover) {
    transition: transform 0.2s ease;
  }

  :global(.magnetic-hover:hover) {
    transform: translateY(-2px);
  }

  /* Global button ripple effect */
  :global(.ripple) {
    position: relative;
    overflow: hidden;
  }

  :global(.ripple::after) {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at var(--ripple-x, 50%) var(--ripple-y, 50%), rgba(255,255,255,0.15) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.3s;
  }

  :global(.ripple:active::after) {
    opacity: 1;
  }

  /* Smooth link underline animation */
  :global(.link-fancy) {
    text-decoration: none;
    background-image: linear-gradient(#f59e0b, #f59e0b);
    background-size: 0% 1px;
    background-repeat: no-repeat;
    background-position: left bottom;
    transition: background-size 0.3s ease;
  }

  :global(.link-fancy:hover) {
    background-size: 100% 1px;
  }

  /* Card tilt effect */
  :global(.tilt-card) {
    transition: transform 0.3s ease;
    transform-style: preserve-3d;
    perspective: 800px;
  }

  :global(.tilt-card:hover) {
    transform: perspective(800px) rotateX(2deg) rotateY(-2deg) translateY(-4px);
    box-shadow: 8px 8px 30px rgba(0, 0, 0, 0.3);
  }

  /* Focus ring */
  :global(*:focus-visible) {
    outline: 2px solid rgba(245, 158, 11, 0.5);
    outline-offset: 2px;
    border-radius: 4px;
  }

  /* Selection color */
  :global(::selection) {
    background: rgba(245, 158, 11, 0.25);
    color: #f1f5f9;
  }

  /* Skip-to-content link (a11y) */
  :global(.skip-link) {
    position: absolute;
    left: 0.5rem;
    top: 0.5rem;
    transform: translateY(-200%);
    z-index: 10000;
    padding: 0.6rem 1rem;
    background: #f59e0b;
    color: #1a0f00;
    font-weight: 700;
    border-radius: 6px;
    text-decoration: none;
    transition: transform 0.2s ease;
  }
  :global(.skip-link:focus) {
    transform: translateY(0);
  }
  :global(main:focus) {
    outline: none;
  }

  /* Scrollbar styling */
  :global(::-webkit-scrollbar) {
    width: 6px;
  }

  :global(::-webkit-scrollbar-track) {
    background: transparent;
  }

  :global(::-webkit-scrollbar-thumb) {
    background: rgba(148, 163, 184, 0.1);
    border-radius: 3px;
  }

  :global(::-webkit-scrollbar-thumb:hover) {
    background: rgba(148, 163, 184, 0.2);
  }
</style>
