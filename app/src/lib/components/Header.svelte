<script>
  import BuyButton from './BuyButton.svelte';

  let stuck = $state(false);
  /** @type {HTMLElement | undefined} */
  let sentinel = $state();

  // The header buy button is absent until the hero has scrolled past. A visitor
  // who has read nothing has not earned a persistent ask, and two competing buy
  // buttons on one screen split the click.
  //
  // A sentinel plus IntersectionObserver beats a scroll listener: no layout
  // reads, nothing to throttle.
  $effect(() => {
    if (!sentinel) return;
    const io = new IntersectionObserver(
      ([entry]) => {
        stuck = !entry.isIntersecting;
      },
      { rootMargin: '-70px 0px 0px 0px' }
    );
    io.observe(sentinel);
    return () => io.disconnect();
  });
</script>

<div class="sentinel" bind:this={sentinel} aria-hidden="true"></div>

<header class="site-head" class:is-stuck={stuck}>
  <div class="wrap head-inner">
    <a class="wordmark" href="/">Surviving the Singularity</a>
    <nav class="head-nav" aria-label="Primary">
      <a href="/#precedent">The Precedent File</a>
      <a href="/#offer">What $5 buys</a>
      <a href="/#updates">Updates</a>
      <a href="/#book">The book</a>
    </nav>
    <div class="head-cta">
      <BuyButton size="sm" />
    </div>
  </div>
</header>

<style>
  /* Sits at the very top of the document. When it scrolls out of view, the
     header has been passed. */
  .sentinel {
    position: absolute;
    top: 180px;
    height: 1px;
    width: 1px;
  }

  .site-head {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(8, 8, 10, 0.92);
    border-bottom: 1px solid transparent;
    backdrop-filter: saturate(140%) blur(8px);
    transition: border-color 200ms ease;
  }
  .site-head.is-stuck {
    border-bottom-color: var(--border);
  }

  .head-inner {
    display: flex;
    align-items: center;
    gap: 28px;
    min-height: 62px;
  }

  .wordmark {
    font: 600 15.5px/1.2 var(--serif);
    letter-spacing: 0.01em;
    color: var(--text);
    text-decoration: none;
    white-space: nowrap;
  }

  .head-nav {
    display: flex;
    gap: 22px;
    margin-left: auto;
  }
  .head-nav a {
    color: var(--text-2);
    text-decoration: none;
    font-size: 14.5px;
    white-space: nowrap;
    transition: color 140ms ease;
  }
  .head-nav a:hover {
    color: var(--text);
  }

  .head-cta {
    opacity: 0;
    visibility: hidden;
    transform: translateY(-4px);
    transition: opacity 180ms ease, transform 180ms ease, visibility 180ms;
  }
  .site-head.is-stuck .head-cta {
    opacity: 1;
    visibility: visible;
    transform: none;
  }

  @media (max-width: 940px) {
    .head-nav {
      display: none;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .site-head { transition: none; }
    .head-nav a { transition: none; }
    .head-cta { transition: none; transform: none; }
    .site-head.is-stuck .head-cta { transform: none; }
  }
</style>
