<script>
  // The continuous reader. One scroll, the whole book, in order.
  //
  // Three things make this different from /book/[sectionId]:
  //   1. No pagination. Chapters flow into each other so a reader can settle in.
  //   2. It remembers where you were, by section + how far into it, so coming
  //      back days later lands you in the same paragraph even after the draft
  //      has been re-edited underneath you.
  //   3. Chapters mount progressively. The full book is ~86k words; rendering
  //      all of it on load would cost seconds on a phone, so we render a few
  //      sections and extend as the reader approaches the end of what's built.
  import { onMount, tick } from 'svelte';
  import { marked } from 'marked';
  import DOMPurify from 'isomorphic-dompurify';
  import { sectionsWithBody, book } from '$lib/bookContent';
  import imageDimensions from '$lib/data/book/image-dimensions.json';
  import { readingPosition } from '$lib/stores/readingPosition';
  import { readerFontSize } from '$lib/stores/readerFontSize';

  // "part-N" entries are structural dividers, not prose. They stay in the flow
  // as section breaks, which is what they are in the printed book too.
  const sections = sectionsWithBody;
  const isDivider = (s) => s.id.startsWith('part-');

  // Cumulative word counts drive the progress meter. Scroll height would be
  // wrong here: the document grows as chapters mount, so a scrollY-based
  // percentage would jump backwards every time we render more.
  const totalWords = sections.reduce((sum, s) => sum + s.wordCount, 0);
  const wordsBefore = (() => {
    const out = [];
    let run = 0;
    for (const s of sections) { out.push(run); run += s.wordCount; }
    return out;
  })();

  function renderMarkdown(raw) {
    if (!raw) return '';
    const html = DOMPurify.sanitize(marked(raw));
    // Applied to the sanitized output - after DOMPurify, never before, so we
    // are not handing it markup to re-parse.
    //
    // The width/height pair is what makes "put me back where I was" work. The
    // markdown carries no dimensions, so without these the browser cannot
    // reserve space for an image until it downloads it, and every arrival
    // shoves the prose below it down the page. Restoring a position against a
    // document that is still growing lands the reader in the wrong chapter.
    // With the intrinsic size declared (and CSS keeping width:100%;height:auto)
    // the box is correct before a single byte arrives, so nothing shifts.
    return html.replace(/<img ([^>]*?)src="([^"]+)"/g, (match, pre, src) => {
      const name = src.split('/').pop();
      const size = imageDimensions[name];
      const dims = size ? ` width="${size[0]}" height="${size[1]}"` : '';
      return `<img loading="lazy" decoding="async"${dims} ${pre}src="${src}"`;
    });
  }

  const INITIAL_MOUNT = 3;
  const MOUNT_STEP = 2;

  let mountedCount = INITIAL_MOUNT;
  let currentIndex = 0;
  let progress = 0;
  let tocOpen = false;
  let restoredFrom = null;   // section title we jumped back to, for the notice
  let sectionEls = [];
  let sentinel;
  let ready = false;

  // The site layout sets `html, body { height: 100%; overflow-x: hidden }`,
  // which makes BODY the scrolling box rather than the viewport. So window.scrollY
  // is permanently 0 here and window 'scroll' never fires. Resolve the real
  // scroller instead of assuming, so this keeps working if that CSS ever changes.
  let scroller = null;

  function resolveScroller() {
    const doc = document.scrollingElement || document.documentElement;
    if (doc && doc.scrollHeight > doc.clientHeight + 1) return doc;
    if (document.body.scrollHeight > document.body.clientHeight + 1) return document.body;
    return doc || document.body;
  }

  const scrollTop = () => (scroller ? scroller.scrollTop : 0);
  const viewportH = () => (scroller ? scroller.clientHeight : window.innerHeight);

  $: currentSection = sections[currentIndex] ?? sections[0];
  $: mounted = sections.slice(0, mountedCount);
  $: allMounted = mountedCount >= sections.length;

  function mountUpTo(index) {
    mountedCount = Math.max(mountedCount, Math.min(sections.length, index + 2));
  }

  // Which section is under the top third of the viewport, and how far into it.
  function measure() {
    const probe = viewportH() * 0.3;
    let idx = 0;
    let ratio = 0;
    for (let i = 0; i < mountedCount; i++) {
      const el = sectionEls[i];
      if (!el) continue;
      const rect = el.getBoundingClientRect();
      if (rect.top <= probe) {
        idx = i;
        const travelled = probe - rect.top;
        ratio = rect.height > 0 ? Math.min(1, Math.max(0, travelled / rect.height)) : 0;
      } else {
        break;
      }
    }
    currentIndex = idx;
    const consumed = wordsBefore[idx] + sections[idx].wordCount * ratio;
    progress = totalWords > 0 ? Math.min(100, (consumed / totalWords) * 100) : 0;
    return { idx, ratio };
  }

  let ticking = false;
  let lastSave = 0;
  // "Start from the beginning" animates a long way back up, and every frame of
  // that animation fires a scroll event that would re-save the place we just
  // cleared. Suppress saving until it settles, with a hard time bound so a
  // reader who grabs the scrollbar mid-animation isn't stuck not saving.
  let suppressSaveUntil = 0;

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      if (!ready) return;
      const { idx, ratio } = measure();

      // Sitting at the very beginning is not a place worth returning to, and
      // treating it as one breaks "start from the beginning": that button
      // clears the position, then its own smooth scroll fires scroll events on
      // the way up and would write a new one. Clearing here is also cheap and
      // deliberately outside the throttle, so the last event of a scroll-to-top
      // always wins over a save made moments earlier.
      // Tested against the scroll offset, not the measured ratio: the ratio is
      // taken from a probe 30% down the viewport, so at a true scrollTop of 0
      // it already reads ~0.03 and no small epsilon on it means "the top".
      if (scrollTop() <= 4) {
        suppressSaveUntil = 0;
        if ($readingPosition) readingPosition.clear();
        return;
      }

      // Throttle the write, not the measurement: the progress bar should track
      // the scroll exactly, but localStorage doesn't need 60 writes a second.
      const now = Date.now();
      if (now < suppressSaveUntil) return;
      if (now - lastSave > 900) {
        lastSave = now;
        readingPosition.save(sections[idx].id, ratio, now);
      }
    });
  }

  async function scrollToSection(index, ratio = 0, behavior = 'auto') {
    mountUpTo(index);
    await tick();
    // Two frames: one for Svelte to place the nodes, one for the browser to
    // lay out any images/fonts above the target so the offset is real.
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    const el = sectionEls[index];
    if (!el || !scroller) return;
    const rect = el.getBoundingClientRect();
    const top = scrollTop() + rect.top + rect.height * ratio - viewportH() * 0.3;
    scroller.scrollTo({ top: Math.max(0, top), behavior });
  }

  // Put the reader back roughly where they were. "Roughly" is the whole spec:
  // the chapter they were in, and about how far through it. Getting even that
  // right needs the layout to stop moving first - the chapter images are lazy
  // and declare no size, so an offset computed while they're still arriving is
  // measured against a document that is still growing, and the reader lands in
  // the wrong chapter entirely.
  async function restoreTo(index, ratio) {
    // One scroll is enough now that every image declares its size: the layout
    // above the target is already its final height, loaded or not. Fonts are
    // the only remaining reflow, and they are usually cached by the time
    // anyone returns to the book, so this waits on them only briefly.
    await Promise.race([
      document.fonts?.ready ?? Promise.resolve(),
      new Promise((r) => setTimeout(r, 600))
    ]).catch(() => {});
    await scrollToSection(index, ratio, 'auto');
  }

  async function jumpTo(index) {
    tocOpen = false;
    restoredFrom = null;
    await scrollToSection(index, 0, 'smooth');
  }

  function startOver() {
    restoredFrom = null;
    readingPosition.clear();
    mountedCount = INITIAL_MOUNT;
    suppressSaveUntil = Date.now() + 2500;
    scroller?.scrollTo({ top: 0, behavior: 'smooth' });
  }

  onMount(() => {
    const saved = $readingPosition;
    scroller = resolveScroller();

    const observer = new IntersectionObserver(
      (entries) => {
        if (!entries.some((e) => e.isIntersecting) || mountedCount >= sections.length) return;
        mountedCount = Math.min(sections.length, mountedCount + MOUNT_STEP);
        // The sentinel usually stays inside the 1200px margin after mounting,
        // and IntersectionObserver only reports threshold *crossings* - without
        // re-observing, a fast scroller would stall until they scrolled again.
        tick().then(() => {
          if (sentinel && mountedCount < sections.length) {
            observer.unobserve(sentinel);
            observer.observe(sentinel);
          }
        });
      },
      {
        // When BODY is the scroll box it must be named as the root explicitly;
        // the implicit root is the viewport, which isn't the thing scrolling.
        root: scroller === document.documentElement ? null : scroller,
        rootMargin: '1200px 0px'
      }
    );

    (async () => {
      if (saved) {
        const index = sections.findIndex((s) => s.id === saved.sectionId);
        // A section that no longer exists (renamed/removed between drafts)
        // shouldn't strand the reader at the top with no explanation - just
        // start clean. Anything else is worth restoring, including a spot deep
        // inside the first chapter: the scroll handler already refuses to save
        // a position at the very beginning, so a stored one always means the
        // reader had genuinely started reading.
        if (index >= 0) {
          await restoreTo(index, saved.ratio);
          restoredFrom = sections[index].title;
        }
      }
      // `ready` gates position saving, so it flips only once the restore has
      // landed: the scroll that restores a position must never overwrite it.
      ready = true;
      measure();
      if (sentinel) observer.observe(sentinel);
    })();

    // Listen on the resolved scroller AND the window: scroll events fire on
    // whichever element is actually the scroll box, and they don't bubble to
    // window when that box is BODY.
    scroller.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });

    return () => {
      observer.disconnect();
      scroller?.removeEventListener('scroll', onScroll);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
    };
  });

  // Re-observe when the sentinel node is replaced (it moves as sections mount).
  $: if (sentinel && ready) { /* referenced so Svelte tracks the binding */ }
</script>

<svelte:head>
  <title>Reader | Surviving the Singularity</title>
  <meta name="description" content="The full draft of Surviving the Singularity in one continuous, readable scroll." />
  <meta name="robots" content="noindex" />
</svelte:head>

<div class="reader" data-size={$readerFontSize}>

  <!-- ── STICKY BAR ── -->
  <header class="bar">
    <div class="bar-inner">
      <button class="bar-btn" on:click={() => (tocOpen = !tocOpen)} aria-expanded={tocOpen} aria-controls="reader-toc">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
        <span class="bar-btn-label">Chapters</span>
      </button>

      <p class="bar-title" title={currentSection?.title}>{currentSection?.title ?? ''}</p>

      <div class="bar-size" role="group" aria-label="Text size">
        <button class="size-btn" on:click={() => readerFontSize.decrease()} aria-label="Smaller text">A<span class="size-minus">&minus;</span></button>
        <button class="size-btn" on:click={() => readerFontSize.increase()} aria-label="Larger text">A<span class="size-plus">+</span></button>
      </div>
    </div>
    <div class="bar-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow={Math.round(progress)} aria-label="Reading progress">
      <div class="bar-progress-fill" style="width: {progress}%"></div>
    </div>
  </header>

  <!-- ── TOC DRAWER ── -->
  {#if tocOpen}
    <button class="toc-scrim" on:click={() => (tocOpen = false)} aria-label="Close chapter list"></button>
  {/if}
  <nav id="reader-toc" class="toc" class:is-open={tocOpen} aria-hidden={!tocOpen}>
    <div class="toc-head">
      <p class="toc-heading">Chapters</p>
      <button class="toc-close" on:click={() => (tocOpen = false)} aria-label="Close">&times;</button>
    </div>
    <ol class="toc-list">
      {#each sections as section, i}
        <li>
          <button
            class="toc-item"
            class:is-divider={isDivider(section)}
            class:is-current={i === currentIndex}
            on:click={() => jumpTo(i)}
          >
            <span class="toc-item-title">{section.title}</span>
            {#if !isDivider(section)}
              <span class="toc-item-words">{section.wordCount.toLocaleString()}</span>
            {/if}
          </button>
        </li>
      {/each}
    </ol>
    <div class="toc-foot">
      <a href="/book" class="toc-foot-link">Back to the book page</a>
    </div>
  </nav>

  <!-- ── RESUME NOTICE ── -->
  {#if restoredFrom}
    <div class="resume" role="status">
      <span>Picked up where you left off, in <strong>{restoredFrom}</strong>.</span>
      <button class="resume-btn" on:click={startOver}>Start from the beginning</button>
    </div>
  {/if}

  <!-- ── PROSE ── -->
  <main class="prose-wrap">
    {#each mounted as section, i (section.id)}
      <section class="section" class:is-divider={isDivider(section)} bind:this={sectionEls[i]} id="s-{section.id}">
        {#if isDivider(section)}
          <div class="divider">
            <span class="divider-rule" aria-hidden="true"></span>
            <h2 class="divider-title">{section.title}</h2>
            <span class="divider-rule" aria-hidden="true"></span>
          </div>
        {:else}
          <article class="prose">
            {@html renderMarkdown(section.raw)}
          </article>
        {/if}
      </section>
    {/each}

    {#if !allMounted}
      <div class="sentinel" bind:this={sentinel} aria-hidden="true">
        <span class="sentinel-dot"></span>
        <span class="sentinel-dot"></span>
        <span class="sentinel-dot"></span>
      </div>
    {:else}
      <footer class="end">
        <p class="end-line">That's the current draft.</p>
        <p class="end-sub">Draft v{book.version} &middot; {totalWords.toLocaleString()} words. It updates as it's written.</p>
        <div class="end-actions">
          <button class="end-btn" on:click={startOver}>Back to the top</button>
          <a href="/book" class="end-link">Leave the reader</a>
        </div>
      </footer>
    {/if}
  </main>
</div>

<style>
  .reader {
    --amber: #f59e0b;
    --text-1: #f1f5f9;
    --text-2: #d7dee8;
    --text-3: #94a3b8;
    --text-4: #64748b;
    --border: rgba(148, 163, 184, 0.12);
    --bar-h: 52px;
    --prose-size: 1.06rem;
    font-family: 'Outfit', system-ui, sans-serif;
    background: #020617;
  }
  .reader[data-size='small']  { --prose-size: 0.96rem; }
  .reader[data-size='large']  { --prose-size: 1.2rem; }
  .reader[data-size='xlarge'] { --prose-size: 1.35rem; }

  /* ── STICKY BAR ── */
  .bar {
    position: sticky;
    top: 0;
    z-index: 30;
    background: rgba(2, 6, 23, 0.92);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border);
  }
  .bar-inner {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    height: var(--bar-h);
    max-width: 780px;
    margin: 0 auto;
    padding: 0 0.75rem;
  }
  .bar-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: none;
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-2);
    padding: 0.45rem 0.6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    cursor: pointer;
    min-height: 38px;
    flex-shrink: 0;
  }
  .bar-btn:hover { color: var(--amber); border-color: rgba(245,158,11,0.4); }
  .bar-btn-label { display: none; }

  .bar-title {
    flex: 1;
    margin: 0;
    text-align: center;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-3);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .bar-size { display: flex; gap: 0.25rem; flex-shrink: 0; }
  .size-btn {
    background: none;
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-2);
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.35rem 0.5rem;
    cursor: pointer;
    min-width: 38px;
    min-height: 38px;
  }
  .size-btn:hover { color: var(--amber); border-color: rgba(245,158,11,0.4); }
  .size-minus, .size-plus { font-size: 0.65em; vertical-align: super; }

  .bar-progress { height: 2px; background: rgba(148,163,184,0.12); }
  .bar-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--amber), #f97316);
    transition: width 0.12s linear;
  }

  @media (min-width: 640px) {
    .bar-btn-label { display: inline; }
    .bar-inner { padding: 0 1.25rem; }
  }

  /* ── TOC DRAWER ── */
  .toc-scrim {
    position: fixed;
    inset: 0;
    z-index: 40;
    background: rgba(2, 6, 23, 0.6);
    border: none;
    cursor: pointer;
  }
  .toc {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 50;
    width: min(88vw, 340px);
    background: #0b1220;
    border-right: 1px solid var(--border);
    transform: translateX(-100%);
    transition: transform 0.22s ease;
    display: flex;
    flex-direction: column;
    visibility: hidden;
  }
  .toc.is-open { transform: translateX(0); visibility: visible; }

  .toc-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1rem;
    border-bottom: 1px solid var(--border);
  }
  .toc-heading {
    margin: 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--amber);
  }
  .toc-close {
    background: none;
    border: none;
    color: var(--text-3);
    font-size: 1.5rem;
    line-height: 1;
    cursor: pointer;
    padding: 0 0.4rem;
    min-height: 44px;
    min-width: 44px;
  }
  .toc-close:hover { color: var(--text-1); }

  .toc-list {
    list-style: none;
    margin: 0;
    padding: 0.5rem 0 1rem;
    overflow-y: auto;
    flex: 1;
    counter-reset: none;
  }
  .toc-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    width: 100%;
    background: none;
    border: none;
    text-align: left;
    padding: 0.7rem 1rem;
    color: var(--text-2);
    font-size: 0.9rem;
    cursor: pointer;
    min-height: 44px;
  }
  .toc-item:hover { background: rgba(245, 158, 11, 0.08); color: var(--amber); }
  .toc-item.is-current { color: var(--amber); box-shadow: inset 3px 0 0 var(--amber); }
  .toc-item.is-divider {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-4);
    margin-top: 0.5rem;
  }
  .toc-item-words {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-4);
    flex-shrink: 0;
  }
  .toc-foot { padding: 0.85rem 1rem; border-top: 1px solid var(--border); }
  .toc-foot-link { color: var(--text-3); font-size: 0.82rem; text-decoration: none; }
  .toc-foot-link:hover { color: var(--amber); }

  /* ── RESUME NOTICE ── */
  .resume {
    position: sticky;
    top: var(--bar-h);
    z-index: 20;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.5rem 0.9rem;
    max-width: 780px;
    margin: 0 auto;
    padding: 0.7rem 1rem;
    background: rgba(245, 158, 11, 0.1);
    border-bottom: 1px solid rgba(245, 158, 11, 0.25);
    font-size: 0.85rem;
    color: var(--text-2);
    text-align: center;
  }
  .resume strong { color: var(--amber); font-weight: 700; }
  .resume-btn {
    background: none;
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: 6px;
    color: var(--amber);
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.35rem 0.7rem;
    cursor: pointer;
    min-height: 34px;
  }
  .resume-btn:hover { background: rgba(245, 158, 11, 0.15); }

  /* ── PROSE ── */
  .prose-wrap {
    max-width: 680px;
    margin: 0 auto;
    padding: clamp(24px, 5vw, 48px) clamp(18px, 5vw, 32px) 0;
  }
  .section { scroll-margin-top: calc(var(--bar-h) + 16px); }

  .divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: clamp(48px, 10vw, 96px) 0;
  }
  .divider-rule { flex: 1; height: 1px; background: var(--border); }
  .divider-title {
    margin: 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--amber);
    text-align: center;
  }

  .prose {
    font-size: var(--prose-size);
    line-height: 1.78;
    color: var(--text-2);
    padding-bottom: clamp(40px, 8vw, 72px);
  }

  .prose :global(h1) {
    /* Chapter titles are long ("Introduction: The Uncompromising Truth") and
       these scale with the reader's chosen text size, so on a narrow phone at
       the largest setting a single word can outrun the column and break
       mid-word. Smaller on small screens, and allow a clean break as a floor. */
    font-size: 1.5em;
    font-weight: 900;
    line-height: 1.15;
    letter-spacing: -0.03em;
    color: var(--text-1);
    margin: 2.2em 0 0.8em;
    text-wrap: balance;
    overflow-wrap: break-word;
    hyphens: auto;
  }
  @media (min-width: 560px) {
    .prose :global(h1) { font-size: 1.9em; }
  }
  .prose :global(h2) {
    font-size: 1.35em;
    font-weight: 800;
    line-height: 1.25;
    letter-spacing: -0.02em;
    color: var(--text-1);
    margin: 2em 0 0.7em;
  }
  .prose :global(h3) {
    font-size: 1.1em;
    font-weight: 700;
    color: var(--text-1);
    margin: 1.7em 0 0.6em;
  }
  .prose :global(p) { margin: 0 0 1.25em; }
  .prose :global(strong) { color: var(--text-1); font-weight: 700; }
  .prose :global(em) { color: var(--text-1); }
  .prose :global(a) {
    color: var(--amber);
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .prose :global(ul), .prose :global(ol) { margin: 0 0 1.4em; padding-left: 1.4em; }
  .prose :global(li) { margin-bottom: 0.55em; }
  .prose :global(blockquote) {
    margin: 1.8em 0;
    padding: 0.2em 0 0.2em 1.2em;
    border-left: 3px solid var(--amber);
    color: var(--text-1);
    font-style: italic;
  }
  .prose :global(img) {
    display: block;
    width: 100%;
    height: auto;
    margin: 2em auto;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: #0b1220;
  }
  .prose :global(hr) {
    border: none;
    height: 1px;
    background: var(--border);
    margin: 2.6em 0;
  }
  .prose :global(code) {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.86em;
    background: rgba(148, 163, 184, 0.12);
    padding: 0.15em 0.4em;
    border-radius: 4px;
    color: var(--text-1);
  }
  .prose :global(pre) {
    background: #0b1220;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1em 1.1em;
    overflow-x: auto;
    margin: 1.8em 0;
  }
  .prose :global(pre code) { background: none; padding: 0; }
  .prose :global(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 1.8em 0;
    font-size: 0.9em;
    display: block;
    overflow-x: auto;
  }
  .prose :global(th), .prose :global(td) {
    border: 1px solid var(--border);
    padding: 0.6em 0.75em;
    text-align: left;
  }
  .prose :global(th) { color: var(--text-1); font-weight: 700; background: rgba(148,163,184,0.06); }

  /* ── SENTINEL / END ── */
  .sentinel {
    display: flex;
    justify-content: center;
    gap: 0.4rem;
    padding: 3rem 0 5rem;
  }
  .sentinel-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--text-4);
    animation: pulse 1.2s ease-in-out infinite;
  }
  .sentinel-dot:nth-child(2) { animation-delay: 0.15s; }
  .sentinel-dot:nth-child(3) { animation-delay: 0.3s; }
  @keyframes pulse {
    0%, 100% { opacity: 0.25; transform: translateY(0); }
    50% { opacity: 1; transform: translateY(-3px); }
  }

  .end {
    text-align: center;
    padding: 3rem 0 6rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
  }
  .end-line { font-size: 1.1rem; font-weight: 700; color: var(--text-1); margin: 0 0 0.4rem; }
  .end-sub { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--text-4); margin: 0 0 1.4rem; }
  .end-btn {
    background: var(--amber);
    color: #020617;
    border: none;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.7rem 1.2rem;
    cursor: pointer;
    min-height: 44px;
  }
  .end-btn:hover { background: #fbbf24; }
  .end-actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.75rem 1.25rem;
  }
  .end-link {
    color: var(--text-3);
    font-size: 0.85rem;
    text-decoration: underline;
    text-underline-offset: 3px;
    padding: 0.5rem;
  }
  .end-link:hover { color: var(--amber); }

  @media (prefers-reduced-motion: reduce) {
    .toc { transition: none; }
    .bar-progress-fill { transition: none; }
    .sentinel-dot { animation: none; }
  }
</style>
