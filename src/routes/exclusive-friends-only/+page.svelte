<script>
  import { fade } from 'svelte/transition';
  import { onMount, tick } from 'svelte';
  import { sectionsWithMeta, book } from '$lib/bookContent';
  import { isValidFriendsPassword } from '$lib/bookAccessCode.js';
  import { bookUnlocked } from '$lib/stores/bookAccess.js';
  import BookCover from '$lib/components/BookCover.svelte';
  import { offer } from '$lib/offer';

  const pdfHref = `/downloads/Surviving-the-Singularity-v${book.version}.pdf`;
  const epubHref = `/downloads/Surviving-the-Singularity-v${book.version}.epub`;

  let password = '';
  let formError = '';
  let passwordInput;

  // The friends gate rides the same in-memory unlock the /book reader uses, so
  // clearing it here also opens every chapter page - one password, not two.
  // Still resets on a full page load, same as the book gate always has.
  $: unlocked = $bookUnlocked;

  const totalWords = sectionsWithMeta.reduce((sum, s) => sum + s.wordCount, 0);

  // Group the flat section list into Front Matter / Part I / II / III / Back
  // Matter, using the "part-N" divider entries in book.json as boundaries.
  // Same grouping the /book table of contents uses.
  const tocGroups = (() => {
    const groups = [];
    let current = { label: 'Front Matter', items: [] };
    for (const section of sectionsWithMeta) {
      if (section.id.startsWith('part-')) {
        if (current.items.length) groups.push(current);
        current = { label: section.title, items: [] };
      } else {
        current.items.push(section);
      }
    }
    if (current.items.length) groups.push(current);
    return groups;
  })();

  let visible = false;
  onMount(() => {
    visible = true;
    passwordInput?.focus();
  });

  async function submitPassword() {
    formError = '';
    if (isValidFriendsPassword(password)) {
      bookUnlocked.set(true);
      password = '';
      await tick();
      window.scrollTo({ top: 0, behavior: 'instant' });
    } else {
      formError = "That's not it. Ask me for the code.";
    }
  }
</script>

<svelte:head>
  <title>Friends Only | Surviving the Singularity</title>
  <meta name="description" content="A private page for friends of the book. Password required." />
  <!-- noindex keeps this out of search results. It does NOT stop iMessage,
       Discord, Slack, or WhatsApp from rendering a link preview - those read
       the og: tags below, which is exactly what we want when the link gets
       texted to someone. Absolute URLs, hardcoded rather than derived from
       $page.url, because every social crawler requires them. -->
  <meta name="robots" content="noindex, nofollow" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Surviving the Singularity" />
  <meta property="og:title" content="The whole book. One password." />
  <meta property="og:description" content="Surviving the Singularity, complete current draft. Read it online or take the PDF and EPUB with you. You'll need the code." />
  <meta property="og:url" content="https://survivingthesingularity.com/exclusive-friends-only" />
  <meta property="og:image" content="https://survivingthesingularity.com/images/og/exclusive-friends-only.png" />
  <meta property="og:image:secure_url" content="https://survivingthesingularity.com/images/og/exclusive-friends-only.png" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="2400" />
  <meta property="og:image:height" content="1260" />
  <meta property="og:image:alt" content="Surviving the Singularity, friends and family edition. The whole book, one password." />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="The whole book. One password." />
  <meta name="twitter:description" content="Surviving the Singularity, complete current draft. Read it online or take the PDF and EPUB with you. You'll need the code." />
  <meta name="twitter:image" content="https://survivingthesingularity.com/images/og/exclusive-friends-only.png" />
  <meta name="twitter:image:alt" content="Surviving the Singularity, friends and family edition. The whole book, one password." />
</svelte:head>

<div class="friends-page">
{#if !unlocked}

  <!-- ── GATE ── -->
  <main class="gate-main">
    <form class="gate-form" on:submit|preventDefault={submitPassword}>
      <div class="gate-cover">
        <BookCover width="clamp(112px, 30vw, 140px)" loading="eager" />
      </div>
      <p class="eyebrow">Friends &amp; family</p>
      <h1 class="gate-title">You either have the password or you don't.</h1>
      <p class="gate-sub">
        This page isn't linked from anywhere. If you're here, someone gave you the code on
        purpose. Type it in and take the whole book.
      </p>
      <input
        type="password"
        bind:value={password}
        bind:this={passwordInput}
        placeholder="the code"
        autocomplete="off"
        autocapitalize="off"
        spellcheck="false"
        class="gate-input"
      />
      {#if formError}<p class="gate-error" role="alert">{formError}</p>{/if}
      <button type="submit" class="gate-submit" disabled={!password}>
        Let me in
      </button>
      <p class="gate-hint">
        No code? The public door is <a href="/early-access" class="gate-hint-link">right here</a>
        for {offer.price}, and it's worth it.
      </p>
    </form>
  </main>

{:else}

  <!-- ── WELCOME ── -->
  <section class="welcome" in:fade={{ duration: 400 }}>
    <div class="inner-narrow">
      <div class="welcome-cover">
        <BookCover width="clamp(150px, 36vw, 220px)" loading="eager" tilt />
      </div>
      <p class="eyebrow">Access granted</p>
      <h1 class="welcome-title">You're in. Take the whole thing.</h1>
      <p class="welcome-text">
        This is the complete current draft of <em>Surviving the Singularity</em>, v{book.version},
        the same file that goes out to preorders. Download it, read it online, put it on your
        e-reader, hand it to somebody who needs it. No paywall between you and any of it.
      </p>
      <p class="welcome-text">
        It's a draft, so it's still moving. If something reads wrong, or you spot a claim that
        doesn't hold up, tell me. That's the actual reason you have this early.
      </p>
      <p class="welcome-meta">
        Draft v{book.version} &middot; {sectionsWithMeta.length} sections &middot; {totalWords.toLocaleString()} words
      </p>
    </div>
  </section>

  <!-- ── DOWNLOADS ── -->
  <section class="downloads">
    <div class="inner">
      <p class="section-label">Take it with you</p>
      <div class="dl-grid">
        <a href={pdfHref} class="dl-card" download>
          <span class="dl-format">PDF</span>
          <span class="dl-title">The full book, laid out</span>
          <span class="dl-note">Illustrated edition. Reads well on a laptop or printed.</span>
          <span class="dl-action">Download <span aria-hidden="true">&darr;</span></span>
        </a>
        <a href={epubHref} class="dl-card" download>
          <span class="dl-format">EPUB</span>
          <span class="dl-title">For your e-reader</span>
          <span class="dl-note">Kindle, Kobo, Apple Books. Reflows to your screen.</span>
          <span class="dl-action">Download <span aria-hidden="true">&darr;</span></span>
        </a>
        <a href={pdfHref} class="dl-card" target="_blank" rel="noopener">
          <span class="dl-format">Browser</span>
          <span class="dl-title">Just open the PDF</span>
          <span class="dl-note">No download. Opens in a new tab, exactly as printed.</span>
          <span class="dl-action">Open <span aria-hidden="true">&nearr;</span></span>
        </a>
      </div>
    </div>
  </section>

  <!-- ── READ ONLINE ── -->
  <section class="read-online">
    <div class="inner">
      <p class="section-label">Or read it here</p>
      <h2 class="read-title">Every chapter, in order.</h2>
      <p class="read-sub">
        One continuous scroll, already unlocked for you. It remembers your place, so you can
        put it down and come back. Or jump straight to a chapter below.
      </p>
      <div class="read-actions">
        <a href="/read" class="btn-primary">Open the reader</a>
      </div>

      {#each tocGroups as group}
        <div class="toc-group">
          <p class="toc-group-label">{group.label}</p>
          <ul class="toc-list">
            {#each group.items as section}
              <li>
                <a href="/book/{section.id}" class="toc-item">
                  <span class="toc-item-main">
                    <span class="toc-item-title">{section.title}</span>
                    {#if section.inProgress}<span class="toc-item-wip">🚧 Under construction</span>{/if}
                  </span>
                  <span class="toc-item-meta">
                    <span class="toc-item-time">{section.wordCount.toLocaleString()} words</span>
                    <span class="toc-item-arrow" aria-hidden="true">&rarr;</span>
                  </span>
                </a>
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </div>
  </section>

  <!-- ── CLOSING NOTE ── -->
  <section class="closing">
    <div class="inner-narrow">
      <p class="closing-text">
        Pass the code along to anyone you'd actually want in the room. If you'd rather send
        someone through the front door, <a href="/early-access" class="closing-link">early access</a>
        is {offer.price} and it helps the book get finished.
      </p>
      <p class="closing-note">
        Commentary and informational only. Not professional advice of any kind. See the
        <a href="/disclaimer" class="closing-link">Disclaimer</a> and
        <a href="/terms" class="closing-link">Terms</a>.
      </p>
    </div>
  </section>

{/if}
</div>

<style>
  /* ── TOKENS (mirrors /book) ── */
  .friends-page {
    font-family: 'Outfit', system-ui, sans-serif;
    --amber:      #f59e0b;
    --amber-dim:  rgba(245,158,11,0.08);
    --border:     rgba(255,255,255,0.07);
    --border-mid: rgba(255,255,255,0.11);
    --text-1:     #f8fafc;
    --text-2:     #cbd5e1;
    --text-3:     #64748b;
    --mono:       'JetBrains Mono', monospace;
  }

  .inner-narrow {
    max-width: 640px;
    margin: 0 auto;
  }
  .inner {
    max-width: 860px;
    margin: 0 auto;
  }

  .eyebrow {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--amber);
    margin: 0 0 1rem;
  }

  /* ── GATE ── */
  .gate-main {
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: clamp(32px, 6vw, 64px) 20px;
  }
  .gate-form {
    width: 100%;
    max-width: 420px;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    text-align: center;
  }
  .gate-cover {
    display: flex;
    justify-content: center;
    margin-bottom: 0.5rem;
  }
  .gate-title {
    font-size: clamp(1.5rem, 4.5vw, 2rem);
    font-weight: 800;
    color: var(--text-1);
    letter-spacing: -0.02em;
    margin: 0;
    text-wrap: balance;
  }
  .gate-sub {
    font-size: 0.95rem;
    color: var(--text-2);
    line-height: 1.7;
    margin: 0 0 0.5rem;
  }
  .gate-input {
    width: 100%;
    padding: 0.85rem 1rem;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid var(--border-mid);
    border-radius: 8px;
    color: var(--text-1);
    font-family: var(--mono);
    font-size: 0.95rem;
    letter-spacing: 0.06em;
    text-align: center;
    min-height: 44px;
  }
  .gate-input::placeholder {
    color: var(--text-3);
    letter-spacing: 0.04em;
  }
  .gate-input:focus {
    outline: none;
    border-color: var(--amber);
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
  }
  .gate-error {
    font-family: var(--mono);
    font-size: 0.8rem;
    color: #f87171;
    margin: 0;
  }
  .gate-submit {
    padding: 0.8rem 1.25rem;
    background: var(--amber);
    color: #020617;
    border: 1px solid var(--amber);
    border-radius: 8px;
    font-family: var(--mono);
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    cursor: pointer;
    min-height: 44px;
    transition: background 0.15s ease, border-color 0.15s ease;
  }
  .gate-submit:hover:not(:disabled) {
    background: #fbbf24;
    border-color: #fbbf24;
  }
  .gate-submit:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
  .gate-hint {
    font-size: 0.85rem;
    color: var(--text-3);
    line-height: 1.6;
    margin: 0.5rem 0 0;
  }
  .gate-hint-link {
    color: var(--amber);
    text-decoration: none;
    font-weight: 600;
  }
  .gate-hint-link:hover { text-decoration: underline; }

  /* ── WELCOME ── */
  .welcome {
    padding: clamp(48px, 8vw, 80px) clamp(20px, 5vw, 48px) clamp(24px, 4vw, 36px);
    text-align: center;
  }
  .welcome-cover {
    display: flex;
    justify-content: center;
    margin-bottom: clamp(24px, 4vw, 36px);
  }
  .welcome-title {
    font-size: clamp(1.75rem, 5vw, 2.5rem);
    font-weight: 900;
    color: var(--text-1);
    letter-spacing: -0.03em;
    margin: 0 0 1.25rem;
    text-wrap: balance;
  }
  .welcome-text {
    font-size: clamp(1rem, 2.2vw, 1.1rem);
    color: var(--text-2);
    line-height: 1.75;
    margin: 0 0 1rem;
  }
  .welcome-meta {
    font-family: var(--mono);
    font-size: 0.8rem;
    color: var(--text-3);
    margin: 1.25rem 0 0;
  }

  /* ── DOWNLOADS ── */
  .downloads {
    padding: clamp(24px, 4vw, 40px) clamp(20px, 5vw, 48px);
  }
  .section-label {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--text-3);
    margin: 0 0 1rem;
  }
  .dl-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }
  .dl-card {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    padding: 1.25rem;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border);
    border-radius: 12px;
    text-decoration: none;
    transition: border-color 0.15s ease, transform 0.15s ease, background 0.15s ease;
  }
  .dl-card:hover {
    border-color: var(--amber);
    background: rgba(15, 23, 42, 0.9);
    transform: translateY(-2px);
  }
  .dl-format {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--amber);
  }
  .dl-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-1);
  }
  .dl-note {
    font-size: 0.85rem;
    color: var(--text-2);
    line-height: 1.55;
    flex: 1;
  }
  .dl-action {
    font-family: var(--mono);
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--amber);
    margin-top: 0.35rem;
  }

  /* ── READ ONLINE ── */
  .read-online {
    padding: clamp(32px, 5vw, 56px) clamp(20px, 5vw, 48px);
  }
  .read-title {
    font-size: clamp(1.35rem, 3.5vw, 1.75rem);
    font-weight: 800;
    color: var(--text-1);
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem;
  }
  .read-sub {
    font-size: 0.95rem;
    color: var(--text-2);
    line-height: 1.7;
    margin: 0 0 1.5rem;
  }
  .read-actions {
    margin-bottom: 2.5rem;
  }
  .btn-primary {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    background: var(--amber);
    color: #020617;
    border-radius: 8px;
    font-family: var(--mono);
    font-size: 0.85rem;
    font-weight: 700;
    text-decoration: none;
    min-height: 44px;
    transition: background 0.15s ease;
  }
  .btn-primary:hover { background: #fbbf24; }

  .toc-group {
    margin-bottom: 2rem;
  }
  .toc-group-label {
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--text-3);
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
    margin: 0 0 0.5rem;
  }
  .toc-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .toc-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.85rem 0.75rem;
    border-radius: 8px;
    text-decoration: none;
    transition: background 0.15s ease;
    min-height: 44px;
  }
  .toc-item:hover {
    background: var(--amber-dim);
  }
  .toc-item-main {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    min-width: 0;
  }
  .toc-item-title {
    font-size: 0.98rem;
    font-weight: 600;
    color: var(--text-1);
  }
  .toc-item:hover .toc-item-title {
    color: var(--amber);
  }
  .toc-item-wip {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-3);
  }
  .toc-item-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-shrink: 0;
  }
  .toc-item-time {
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--text-3);
    white-space: nowrap;
  }
  .toc-item-arrow {
    color: var(--text-3);
    font-size: 0.9rem;
  }
  .toc-item:hover .toc-item-arrow { color: var(--amber); }

  @media (max-width: 520px) {
    .toc-item-time { display: none; }
  }

  /* ── CLOSING ── */
  .closing {
    padding: clamp(24px, 4vw, 40px) clamp(20px, 5vw, 48px) clamp(48px, 8vw, 80px);
    text-align: center;
  }
  .closing-text {
    font-size: 0.95rem;
    color: var(--text-2);
    line-height: 1.75;
    margin: 0 0 1.25rem;
  }
  .closing-note {
    font-size: 0.82rem;
    color: var(--text-3);
    line-height: 1.7;
    margin: 0;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border);
  }
  .closing-link {
    color: var(--amber);
    text-decoration: none;
    font-weight: 600;
  }
  .closing-link:hover { text-decoration: underline; }
</style>
