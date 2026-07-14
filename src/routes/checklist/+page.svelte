<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import EmailGate from '$lib/components/EmailGate.svelte';
  import DiscordApplication from '$lib/components/DiscordApplication.svelte';

  const categories = {
    foundation:     { label: 'Foundation',     color: '#f59e0b', desc: 'Understand your actual situation before you change anything.' },
    infrastructure: { label: 'Infrastructure', color: '#3b82f6', desc: 'Build the systems that run without you needing to think about them.' },
    autonomy:       { label: 'Autonomy',       color: '#10b981', desc: 'Go from dependent to capable in the areas that matter most.' },
    network:        { label: 'Network',        color: '#a78bfa', desc: 'The social and financial layer that makes everything else stick.' },
  };

  const allItems = [
    {
      n: '01', cat: 'foundation',
      title: 'Understand what is actually happening',
      body: 'AI is not a future problem. It is reshaping industries, displacing roles, and creating new power gaps right now. Most people are still treating it as a news story.',
      action: 'Search your job title + "AI automation 2026" and spend a few minutes absorbing what you find. Be honest about it.',
      cost: '$0', effort: 'low', free: true,
    },
    {
      n: '02', cat: 'foundation',
      title: 'Calculate your freedom number',
      body: 'The monthly cost to cover your essentials if your income stopped tomorrow. Know this number. Everything you do from here is a campaign to lower it or replace it.',
      action: "Add up last month's fixed costs: rent, food, utilities, insurance, debt minimums. Write that number down.",
      cost: '$0', effort: 'low', free: true,
    },
    {
      n: '03', cat: 'foundation',
      title: 'Turn your biggest threat into your next advantage',
      body: 'Every technology that wiped out one group of workers created a new group of winners. The difference was always who picked up the tool first. You are reading this because you already sense that.',
      action: 'Write down one specific thing AI could do for you that you currently struggle with, pay someone else for, or just avoid entirely.',
      cost: '$0', effort: 'low', free: true,
    },
    {
      n: '04', cat: 'infrastructure',
      title: 'Start a skill that compounds',
      body: '30 minutes a day in one high-leverage skill beats every weekend warrior in 6 months. Compounding is the only shortcut that actually works.',
      action: 'Name the skill. Schedule the first 30 minutes on your calendar for today.',
      cost: '$0-50', effort: 'medium', free: false,
    },
    {
      n: '05', cat: 'infrastructure',
      title: 'Use AI to cut something you currently pay for',
      body: 'Every tool in this era can eliminate a dependency if you know how to use it. Legal questions, design work, research, writing: things that used to cost money or time can now cost neither.',
      action: 'Pick one thing you pay for or avoid because it\'s too expensive. Spend 20 minutes seeing how far a free AI tool gets you.',
      cost: '$0', effort: 'low', free: false,
    },
    {
      n: '06', cat: 'autonomy',
      title: 'Automate one recurring task with AI',
      body: 'Pick one weekly task that is mechanical and spend 20 minutes building a prompt that handles 80% of it. Reclaim those hours. Build the habit of automating your own work.',
      action: 'Pick one weekly task. Spend 20 minutes building a prompt that handles 80% of it.',
      cost: '$0-20/mo', effort: 'medium', free: false,
    },
    {
      n: '07', cat: 'network',
      title: 'Find three people building the same way',
      body: 'You do not need thousands. You need three people who are actually doing the work. That is the difference between a phase and a life.',
      action: 'Message one person today who you think is building toward real independence. Tell them what you\'re doing.',
      cost: '$0', effort: 'low', free: false,
    },
  ];

  const teaser = allItems.filter(i => i.free);
  const gated  = allItems.filter(i => !i.free);

  const relatedChapters = [
    { n: '01', title: 'The AGI Transition',    slug: 'agi-transition',      tag: 'Foundation',     color: '#f59e0b' },
    { n: '02', title: 'Local AI Infrastructure', slug: 'local-ai',          tag: 'Foundation',     color: '#f59e0b' },
    { n: '04', title: 'Food Security Systems',  slug: 'food-security',       tag: 'Autonomy',       color: '#10b981' },
    { n: '06', title: 'Digital Leverage',       slug: 'digital-leverage',    tag: 'Infrastructure', color: '#3b82f6' },
    { n: '07', title: 'Energy Independence',    slug: 'energy',              tag: 'Infrastructure', color: '#3b82f6' },
    { n: '08', title: 'Physical Automation',    slug: 'physical-automation', tag: 'Autonomy',       color: '#10b981' },
  ];

  // ── Interactive state ──────────────────────────────────────────────────────
  let answers = Object.fromEntries(
    allItems.map(item => [item.n, { checked: false, notes: '' }])
  );

  $: checkedCount = Object.values(answers).filter(a => a.checked).length;

  // Persist progress in localStorage
  onMount(() => {
    if (!browser) return;
    try {
      const saved = localStorage.getItem('sts_checklist_progress');
      if (saved) {
        const parsed = JSON.parse(saved);
        for (const [k, v] of Object.entries(parsed)) {
          if (answers[k]) answers[k] = { checked: !!v.checked, notes: String(v.notes ?? '') };
        }
      }
    } catch {}
  });

  $: if (browser) {
    try { localStorage.setItem('sts_checklist_progress', JSON.stringify(answers)); } catch {}
  }

  // Auto-resize textarea to content height
  function autoresize(node) {
    function resize() {
      node.style.height = 'auto';
      node.style.height = node.scrollHeight + 'px';
    }
    resize();
    node.addEventListener('input', resize);
    return { destroy() { node.removeEventListener('input', resize); } };
  }

  // ── Discord preview - free, no-commitment, temporary invite. Does NOT
  // unlock the checklist; that's EmailGate's job, gated on a real email. ────
  const DISCORD_KEY = 'sts_discord_previewed';
  let discordPreviewed = false;

  onMount(() => {
    if (!browser) return;
    if (localStorage.getItem(DISCORD_KEY)) discordPreviewed = true;
  });

  function previewDiscord() {
    if (browser) {
      localStorage.setItem(DISCORD_KEY, '1');
    }
    discordPreviewed = true;
    window.open('https://discord.gg/DVKhj6Vxge', '_blank', 'noopener,noreferrer');
  }

  // ── Send checklist email - fires automatically the moment the visitor
  // unlocks with their email; also reusable as a manual resend after they
  // update their notes. ────────────────────────────────────────────────────
  let emailToSend = '';
  let sending = false;
  let sent = false;
  let sendError = '';

  // EmailGate fires 'unlock' only on a brand-new submission (auto-send) and
  // 'restore' on page load for already-unlocked visitors (capture the email
  // for manual resends, never auto-send).
  function onUnlock(e) {
    if (e.detail?.email) {
      emailToSend = e.detail.email;
      sendChecklist();
    }
  }

  function onRestore(e) {
    if (e.detail?.email) emailToSend = e.detail.email;
  }

  async function sendChecklist() {
    if (sending || !emailToSend.trim()) return;
    sending = true;
    sendError = '';
    try {
      const res = await fetch('/api/checklist-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: emailToSend.trim(),
          answers: allItems.map(item => ({
            n:       item.n,
            title:   item.title,
            cat:     item.cat,
            body:    item.body,
            action:  item.action,
            cost:    item.cost,
            effort:  item.effort,
            checked: answers[item.n].checked,
            notes:   answers[item.n].notes,
          })),
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        sendError = data.error || 'Something went wrong. Try again.';
      } else {
        sent = true;
      }
    } catch {
      sendError = 'Network error. Please try again.';
    } finally {
      sending = false;
    }
  }
</script>

<svelte:head>
  <title>Free Readiness Checklist: Surviving the Singularity</title>
  <meta name="description" content="7 concrete moves to build real independence before AGI changes everything. Check off steps, add your own notes, and email yourself the results." />
</svelte:head>

<div class="cl-page">

  <!-- ── HERO ── -->
  <header class="cl-hero">
    <h1 class="cl-title">The Singularity<br>Readiness Checklist</h1>
    <div class="cl-lede-stack">
      <p class="cl-lede-line">Most people won't see it coming.</p>
      <p class="cl-lede-line cl-lede-punch">You will.</p>
      <p class="cl-lede-line">7 moves. Real actions. Start now.</p>
    </div>

    <div class="cl-stats">
      <div class="cl-stat">
        <span class="cl-stat-n">7</span>
        <span class="cl-stat-l">steps</span>
      </div>
      <div class="cl-stat-sep" aria-hidden="true"></div>
      <div class="cl-stat">
        <span class="cl-stat-n">4</span>
        <span class="cl-stat-l">areas</span>
      </div>
      <div class="cl-stat-sep" aria-hidden="true"></div>
      <div class="cl-stat">
        <span class="cl-stat-n">$0</span>
        <span class="cl-stat-l">to start</span>
      </div>
      <div class="cl-stat-sep" aria-hidden="true"></div>
      <div class="cl-stat">
        <span class="cl-stat-n cl-stat-progress" aria-live="polite">{checkedCount}/7</span>
        <span class="cl-stat-l">completed</span>
      </div>
    </div>
  </header>

  <!-- ── WELCOME VIDEO ── -->
  <div class="cl-video-section">
    <div class="cl-video-wrap">
      <iframe
        src="https://www.youtube.com/embed/NKENM_J-rEg?si=EnjKmWQodX5SybA6"
        title="Welcome to the Surviving the Singularity community"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin"
        allowfullscreen
      ></iframe>
    </div>
  </div>

  <!-- ── CATEGORIES KEY ── -->
  <div class="cl-categories">
    {#each Object.entries(categories) as [, cat]}
      <div class="cl-cat-pill" style="--cat-color: {cat.color}">
        <span class="cl-cat-dot" aria-hidden="true"></span>
        {cat.label}
      </div>
    {/each}
  </div>

  <!-- ── PRIMER ── -->
  <p class="cl-primer-single">Each step has one action you can take this week. Check it off when you've done it. Start with 01.</p>

  <!-- ── CHECKLIST with EmailGate ── -->
  <EmailGate
    storageKey="checklist"
    source="checklist"
    headline="Unlock the full checklist"
    sub="Get all 7 steps, your notes emailed to you, and Signal Dispatches: a short, occasional email only when something actually changes your plan (new research, a new tool, a real timeline shift). Not a newsletter."
    buttonText="Unlock Free"
    on:unlock={onUnlock}
    on:restore={onRestore}
  >
    <!-- Free teaser items - always interactive -->
    <ol class="cl-list" aria-label="First three checklist items, free">
      {#each teaser as item}
        <li class="cl-item" class:is-checked={answers[item.n].checked} style="--cat-color: {categories[item.cat].color}">
          <div class="cl-item-head">
            <label class="cl-check-wrap" for="check-{item.n}">
              <input
                type="checkbox"
                class="cl-check-native"
                id="check-{item.n}"
                bind:checked={answers[item.n].checked}
              />
              <span class="cl-checkbox" aria-hidden="true">
                {#if answers[item.n].checked}
                  <svg width="10" height="8" viewBox="0 0 10 8" fill="none" aria-hidden="true">
                    <path d="M1 4l2.5 2.5L9 1" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                {/if}
              </span>
            </label>
            <span class="cl-num">{item.n}</span>
            <span class="cl-cat-tag" style="color: {categories[item.cat].color}; background: color-mix(in srgb, {categories[item.cat].color} 12%, transparent)">
              {categories[item.cat].label}
            </span>
          </div>
          <h2 class="cl-item-title">{item.title}</h2>
          <p class="cl-item-text">{item.body}</p>
          <div class="cl-action">
            <span class="cl-action-label">First action</span>
            <p class="cl-action-text">{item.action}</p>
          </div>
          <div class="cl-notes-wrap">
            <label class="cl-notes-label" for="notes-{item.n}">Your notes</label>
            <textarea
              id="notes-{item.n}"
              class="cl-notes"
              bind:value={answers[item.n].notes}
              placeholder="What's your plan for this step? Any blockers?"
              maxlength="1000"
              rows="2"
              autocomplete="off"
              spellcheck="true"
              use:autoresize
            ></textarea>
          </div>
        </li>
      {/each}
    </ol>

    <!-- Locked preview of item 04 -->
    <div class="cl-locked-preview" aria-hidden="true">
      <div class="cl-item cl-item-locked" style="--cat-color: {categories[gated[0].cat].color}">
        <div class="cl-item-head">
          <span class="cl-checkbox cl-checkbox-locked" aria-hidden="true"></span>
          <span class="cl-num">{gated[0].n}</span>
          <span class="cl-cat-tag" style="color: {categories[gated[0].cat].color}; background: color-mix(in srgb, {categories[gated[0].cat].color} 12%, transparent)">
            {categories[gated[0].cat].label}
          </span>
        </div>
        <h2 class="cl-item-title">{gated[0].title}</h2>
        <p class="cl-item-text">{gated[0].body}</p>
        <div class="cl-action cl-action-blurred">
          <span class="cl-action-label">First action</span>
          <p class="cl-action-text">{gated[0].action}</p>
        </div>
      </div>
      <div class="cl-locked-fade" aria-hidden="true"></div>
      <div class="cl-locked-more" aria-hidden="true">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        3 more steps locked
      </div>
    </div>

    <!-- Book sales pitch - inside the gate card, below the email form -->
    <div slot="gate-extra" class="cl-book-sales">
      <p class="cl-book-sales-eyebrow">The book behind this checklist</p>
      <h3 class="cl-book-sales-title">Surviving the Singularity</h3>

      <img
        src="/images/surviving_the_singularity_cover_1200.png"
        alt="Surviving the Singularity book cover"
        class="cl-book-sales-cover"
        loading="lazy"
      />

      <ul class="cl-book-sales-parts">
        <li><span class="cl-book-part-label">Part I</span> What's happening. The nine stages of AI scaling.</li>
        <li><span class="cl-book-part-label">Part II</span> How people will react. And why most will get it wrong.</li>
        <li><span class="cl-book-part-label">Part III</span> What you can do. Right now. Starting today.</li>
      </ul>

      <a href="/early-access" class="cl-book-sales-btn">
        Get Early Access. $5.
        <svg width="13" height="13" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <p class="cl-book-sales-fine">One payment. Instant access. Price goes up at launch.</p>
    </div>

    <!-- Gated: items 4-12 + send section + deeper content -->
    <div slot="gated">
      <ol class="cl-list cl-list-gated" start="4" aria-label="Remaining four checklist items">
        {#each gated as item}
          <li class="cl-item" class:is-checked={answers[item.n].checked} style="--cat-color: {categories[item.cat].color}">
            <div class="cl-item-head">
              <label class="cl-check-wrap" for="check-{item.n}">
                <input
                  type="checkbox"
                  class="cl-check-native"
                  id="check-{item.n}"
                  bind:checked={answers[item.n].checked}
                />
                <span class="cl-checkbox" aria-hidden="true">
                  {#if answers[item.n].checked}
                    <svg width="10" height="8" viewBox="0 0 10 8" fill="none" aria-hidden="true">
                      <path d="M1 4l2.5 2.5L9 1" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  {/if}
                </span>
              </label>
              <span class="cl-num">{item.n}</span>
              <span class="cl-cat-tag" style="color: {categories[item.cat].color}; background: color-mix(in srgb, {categories[item.cat].color} 12%, transparent)">
                {categories[item.cat].label}
              </span>
              <div class="cl-item-meta">
                <span class="cl-meta-pill">{item.cost}</span>
                <span class="cl-meta-pill">{item.effort} effort</span>
              </div>
            </div>
            <h2 class="cl-item-title">{item.title}</h2>
            <p class="cl-item-text">{item.body}</p>
            <div class="cl-action">
              <span class="cl-action-label">First action</span>
              <p class="cl-action-text">{item.action}</p>
            </div>
            <div class="cl-notes-wrap">
              <label class="cl-notes-label" for="notes-{item.n}">Your notes</label>
              <textarea
                id="notes-{item.n}"
                class="cl-notes"
                bind:value={answers[item.n].notes}
                placeholder="What's your plan for this step? Any blockers?"
                maxlength="1000"
                rows="2"
                autocomplete="off"
                spellcheck="true"
                use:autoresize
              ></textarea>
            </div>
          </li>
        {/each}
      </ol>

      <!-- ── YOUR CHECKLIST, SENT ── -->
      <section class="cl-send" aria-label="Your checklist email">
        <div class="cl-send-inner">
          <div class="cl-send-header">
            <div class="cl-send-icon" aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
              </svg>
            </div>
            <div>
              <p class="cl-section-label">Sent to your inbox</p>
              <h2 class="cl-send-heading">Your answers and the full checklist are on their way to {emailToSend}.</h2>
            </div>
          </div>
          <p class="cl-send-sub">
            Keep adding notes below. When you want an updated copy, resend it.
          </p>

          {#if sent}
            <!-- A failed resend must not show "Sent!" and the error together;
                 the error below takes over until the next successful send. -->
            {#if !sendError}
            <div class="cl-send-success" role="status">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
              Sent! Check your inbox. ({checkedCount}/7 steps in the email.)
            </div>
            {/if}
            <button type="button" class="cl-send-resend" on:click={sendChecklist} disabled={sending}>
              {sending ? 'Resending…' : 'Resend with my latest notes'}
            </button>
          {:else}
            <button type="button" class="cl-send-btn" on:click={sendChecklist} disabled={sending || !emailToSend.trim()}>
              {#if sending}
                <span class="cl-send-spinner" aria-hidden="true"></span>
                Sending…
              {:else}
                Send my checklist
                <svg width="13" height="13" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                  <path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              {/if}
            </button>
          {/if}
          {#if sendError}
            <p class="cl-send-error" role="alert">{sendError}</p>
          {/if}

          <p class="cl-send-meta">
            {checkedCount} of 7 steps checked, {allItems.filter(i => answers[i.n].notes.trim()).length} with notes. Zero spam, reply to unsubscribe.
          </p>
        </div>
      </section>

      <!-- Go deeper: Blueprint chapter links -->
      <section class="cl-deeper">
        <p class="cl-section-label">Go deeper</p>
        <h2 class="cl-deeper-heading">Each step has a full chapter behind it.</h2>
        <p class="cl-deeper-sub">The Blueprint expands every area of this checklist into a full strategy. Start with the chapter that matches where you are right now.</p>
        <div class="cl-chapters">
          {#each relatedChapters as ch}
            <a href="/book" class="cl-chapter-card">
              <span class="cl-chapter-n" style="color: {ch.color}">{ch.n}</span>
              <div class="cl-chapter-body">
                <span class="cl-chapter-tag" style="color: {ch.color}">{ch.tag}</span>
                <span class="cl-chapter-title">{ch.title}</span>
              </div>
              <svg class="cl-chapter-arrow" width="14" height="14" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                <path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </a>
          {/each}
        </div>
      </section>

      <!-- Upgrade CTA -->
      <section class="cl-upgrade">
        <div class="cl-upgrade-inner">
          <div class="cl-upgrade-text">
            <p class="cl-section-label">Want everything</p>
            <h2 class="cl-upgrade-heading">The full kit is $5.</h2>
            <p class="cl-upgrade-sub">All chapters, the book draft, the research bundle, and every tool I build next. One payment. Instant access.</p>
          </div>
          <a href="/early-access" class="cl-upgrade-btn">
            Get Early Access
            <svg width="13" height="13" viewBox="0 0 12 12" fill="none" aria-hidden="true">
              <path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
        </div>
      </section>
    </div>
  </EmailGate>

  <!-- ── LIVE EVENT: same community touchpoint, real-time ── -->
  <section class="cl-discord-block" aria-label="Live weekly event">
    <p class="cl-section-label">A separate thing</p>
    <h2 class="cl-discord-block-heading">Prefer talking to typing?</h2>
    <p class="cl-discord-block-sub">Every Tuesday, free, on Zoom. Live discussion with people working through the same questions you are.</p>

    <div class="cl-discord cl-event">
      <div class="cl-discord-icon cl-event-icon" aria-hidden="true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </div>
      <div class="cl-discord-copy">
        <p class="cl-discord-headline">Tuesdays, 4&ndash;5PM Pacific.</p>
        <p class="cl-discord-sub">Free to join. No book purchase required.</p>
      </div>
      <a href="https://luma.com/event/evt-yQuYOJ1qhrnkvdw" target="_blank" rel="noopener noreferrer" class="cl-discord-btn cl-event-btn">
        Save Your Seat
        <svg width="13" height="13" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </div>
  </section>

  <!-- ── DISCORD: separate community value add, not part of the checklist ── -->
  <section class="cl-discord-block" aria-label="Community">
    <p class="cl-section-label">A separate thing</p>
    <h2 class="cl-discord-block-heading">Want to talk to people doing this too?</h2>
    <p class="cl-discord-block-sub">Not part of the checklist. Just a community, if you want it.</p>

    <div class="cl-discord">
      <div class="cl-discord-icon" aria-hidden="true">
        <svg width="22" height="16" viewBox="0 0 24 18" fill="currentColor" aria-hidden="true">
          <path d="M20.317 1.492A19.825 19.825 0 0 0 15.964.196a.074.074 0 0 0-.079.037c-.34.607-.719 1.396-.984 2.018a18.304 18.304 0 0 0-5.8 0 12.757 12.757 0 0 0-.998-2.018.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 1.492a.07.07 0 0 0-.032.027C.533 6.093-.32 10.555.099 14.961a.083.083 0 0 0 .031.056 19.9 19.9 0 0 0 5.993 3.03.077.077 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.442a.061.061 0 0 0-.031-.028zM8.02 12.278c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
        </svg>
      </div>
      <div class="cl-discord-copy">
        <p class="cl-discord-headline">Come see what it's like.</p>
        <p class="cl-discord-sub">Free preview, no commitment, no email required.</p>
      </div>
      <button class="cl-discord-btn" class:cl-discord-btn-done={discordPreviewed} on:click={previewDiscord} type="button">
        {#if discordPreviewed}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
          Previewed
        {:else}
          Preview the Discord
          <svg width="13" height="13" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
        {/if}
      </button>
    </div>

    <DiscordApplication />
  </section>

  <p class="cl-disclaimer">
    This is a starting point for your own research, not professional advice.
    <a href="/disclaimer">Terms and disclaimers</a>.
  </p>

</div>

<style>
  .cl-page {
    max-width: 760px;
    margin: 0 auto;
    padding: clamp(2rem, 6vw, 4rem) clamp(1rem, 4vw, 1.5rem) 5rem;
  }

  /* ── HERO ── */
  .cl-hero { text-align: center; margin-bottom: 2rem; }

  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.7); }
  }

  .cl-title {
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 900; color: #f8fafc;
    letter-spacing: -0.03em; line-height: 1.05;
    margin: 0 0 16px;
  }

  .cl-lede-stack {
    display: flex; flex-direction: column; align-items: center;
    gap: 4px; margin: 0 auto 28px; max-width: 560px;
  }
  .cl-lede-line {
    font-size: clamp(1rem, 2.5vw, 1.15rem);
    color: #94a3b8; line-height: 1.5; margin: 0;
  }
  .cl-lede-punch {
    font-size: clamp(1.1rem, 3vw, 1.35rem);
    font-weight: 800; color: #f1f5f9;
  }

  .cl-stats {
    display: inline-flex; align-items: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 12px 24px;
    flex-wrap: wrap; justify-content: center; gap: 0;
    row-gap: 16px;
  }
  .cl-stat {
    display: flex; flex-direction: column; align-items: center;
    padding: 4px 20px;
  }
  .cl-stat-n {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem; font-weight: 700; color: #f59e0b; line-height: 1;
  }
  .cl-stat-progress { transition: color 0.3s ease; }
  .cl-stat-l {
    font-size: 0.7rem; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.1em; margin-top: 3px;
  }
  .cl-stat-sep {
    width: 1px; height: 28px; background: rgba(255,255,255,0.07); flex-shrink: 0;
    align-self: center;
  }
  @media (max-width: 420px) {
    .cl-stats { row-gap: 18px; }
    .cl-stat-sep { display: none; }
  }

  /* ── CATEGORIES ── */
  .cl-categories {
    display: flex; flex-wrap: wrap; gap: 8px;
    justify-content: center; margin-bottom: 2rem;
  }
  .cl-cat-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 12px;
    background: color-mix(in srgb, var(--cat-color) 10%, transparent);
    border: 1px solid color-mix(in srgb, var(--cat-color) 25%, transparent);
    border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; color: var(--cat-color);
  }
  .cl-cat-dot {
    width: 5px; height: 5px; border-radius: 50%; background: currentColor;
  }

  /* ── LOCKED PREVIEW ── */
  .cl-locked-preview {
    position: relative; margin: 0 0 16px; user-select: none;
  }
  .cl-item-locked {
    opacity: 0.35; pointer-events: none;
    filter: blur(0.4px);
  }
  .cl-checkbox-locked {
    width: 20px; height: 20px;
    border: 1.5px solid rgba(255,255,255,0.15);
    border-radius: 6px; background: rgba(255,255,255,0.03);
    display: inline-flex; flex-shrink: 0;
  }
  .cl-action-blurred { filter: blur(3px); }
  .cl-locked-fade {
    position: absolute; bottom: 28px; left: 0; right: 0;
    height: 60px;
    background: linear-gradient(to bottom, transparent, #020617);
    pointer-events: none;
  }
  .cl-locked-more {
    display: flex; align-items: center; gap: 7px;
    justify-content: center;
    padding: 10px 0 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #475569;
  }

  /* ── DISCORD: standalone section, separate from the checklist ── */
  .cl-discord-block {
    margin: 3rem 0 0;
    padding-top: 2.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
  }
  .cl-discord-block-heading {
    font-size: clamp(1.3rem, 3vw, 1.8rem); font-weight: 800;
    color: #f8fafc; letter-spacing: -0.02em; margin: 0 0 8px;
  }
  .cl-discord-block-sub {
    font-size: 0.9rem; color: #94a3b8; line-height: 1.6;
    margin: 0 0 20px; max-width: 480px;
  }

  .cl-discord {
    display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
    margin: 0 0 2rem;
    padding: 18px 20px;
    background: rgba(88, 101, 242, 0.07);
    border: 1px solid rgba(88, 101, 242, 0.25);
    border-radius: 14px;
  }
  .cl-discord-icon {
    display: flex; align-items: center; justify-content: center;
    width: 42px; height: 42px; flex-shrink: 0;
    background: rgba(88, 101, 242, 0.12);
    border-radius: 10px; color: #7289da;
  }
  .cl-discord-copy { flex: 1; min-width: 180px; }
  .cl-discord-headline {
    font-size: 0.95rem; font-weight: 800; color: #f1f5f9;
    margin: 0 0 4px;
  }
  .cl-discord-sub {
    font-size: 0.82rem; color: #94a3b8; line-height: 1.55; margin: 0;
  }
  .cl-discord-btn {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 9px 16px; flex-shrink: 0;
    background: #5865f2; color: #fff;
    font-size: 0.85rem; font-weight: 700;
    border: none; border-radius: 8px; text-decoration: none; white-space: nowrap;
    cursor: pointer; transition: filter 0.15s ease;
  }
  .cl-discord-btn:hover { filter: brightness(1.1); }
  .cl-discord-btn-done {
    background: rgba(16,185,129,0.15);
    color: #10b981;
    border: 1px solid rgba(16,185,129,0.3);
    cursor: default;
  }
  .cl-discord-btn-done:hover { filter: none; }
  @media (max-width: 500px) {
    .cl-discord { flex-direction: column; align-items: flex-start; }
    .cl-discord-btn { width: 100%; justify-content: center; }
  }

  .cl-event { background: rgba(245, 158, 11, 0.07); border-color: rgba(245, 158, 11, 0.25); }
  .cl-event-icon { background: rgba(245, 158, 11, 0.12); color: #f59e0b; }
  .cl-event-btn { background: #f59e0b; color: #0f172a; }

  /* ── CHECKLIST ITEMS ── */
  .cl-list {
    list-style: none; padding: 0; margin: 0 0 1.5rem;
    display: flex; flex-direction: column; gap: 12px;
  }
  .cl-list-gated { margin-top: 12px; }

  .cl-item {
    padding: 20px 20px 16px;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid var(--cat-color);
    border-radius: 14px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, opacity 0.25s ease;
  }
  .cl-item:hover {
    border-color: color-mix(in srgb, var(--cat-color) 35%, transparent);
    border-left-color: var(--cat-color);
    box-shadow: 0 6px 24px rgba(0,0,0,0.2);
  }
  .cl-item.is-checked { opacity: 0.7; }
  .cl-item.is-checked:hover { opacity: 0.85; }

  /* ── CHECKBOX ── */
  .cl-item-head {
    display: flex; align-items: center; gap: 8px;
    flex-wrap: wrap; margin-bottom: 10px;
  }
  .cl-check-wrap {
    display: inline-flex; align-items: center; justify-content: center;
    cursor: pointer; flex-shrink: 0;
  }
  .cl-check-native {
    position: absolute;
    width: 1px; height: 1px;
    opacity: 0; pointer-events: none;
  }
  .cl-checkbox {
    display: inline-flex; align-items: center; justify-content: center;
    width: 20px; height: 20px;
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 6px;
    background: rgba(255,255,255,0.03);
    color: #0a0a0a;
    flex-shrink: 0;
    transition: border-color 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
  }
  .cl-check-wrap:hover .cl-checkbox {
    border-color: var(--cat-color);
    background: color-mix(in srgb, var(--cat-color) 8%, transparent);
  }
  .cl-check-native:focus-visible ~ .cl-checkbox {
    outline: 2px solid #f59e0b;
    outline-offset: 2px;
  }
  .cl-item.is-checked .cl-checkbox {
    background: var(--cat-color);
    border-color: var(--cat-color);
    box-shadow: 0 0 8px color-mix(in srgb, var(--cat-color) 45%, transparent);
  }

  .cl-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; font-weight: 700;
    color: var(--cat-color); flex-shrink: 0;
  }
  .cl-cat-tag {
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    padding: 2px 8px; border-radius: 4px;
  }

  .cl-item-title {
    font-size: 1rem; font-weight: 700; color: #f1f5f9;
    margin: 0 0 6px; line-height: 1.3;
    transition: color 0.2s ease;
  }
  .cl-item.is-checked .cl-item-title { color: #94a3b8; text-decoration: line-through; text-decoration-color: rgba(100,116,139,0.4); }

  .cl-item-text {
    font-size: 0.9rem; color: #cbd5e1; line-height: 1.65; margin: 0 0 12px;
  }

  .cl-action {
    background: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;
  }
  .cl-action-label {
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em;
    color: #f59e0b; margin-bottom: 4px;
  }
  .cl-action-text { font-size: 0.85rem; color: #e2e8f0; line-height: 1.5; margin: 0; }

  /* ── NOTES TEXTAREA ── */
  .cl-notes-wrap { margin-top: 4px; }
  .cl-notes-label {
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em;
    color: #64748b; margin-bottom: 5px;
  }
  .cl-notes {
    width: 100%;
    min-height: 52px;
    padding: 9px 12px;
    background: rgba(2, 6, 23, 0.5);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    color: #e2e8f0;
    font-family: inherit;
    font-size: 0.88rem;
    line-height: 1.55;
    resize: none; /* auto-resizes via JS */
    box-sizing: border-box;
    transition: border-color 0.15s ease, background 0.15s ease;
    overflow: hidden;
  }
  .cl-notes::placeholder { color: #64748b; }
  .cl-notes:focus {
    outline: none;
    border-color: rgba(245, 158, 11, 0.4);
    background: rgba(2, 6, 23, 0.75);
  }

  /* ── SECTION LABELS ── */
  .cl-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: #f59e0b; margin-bottom: 8px;
  }

  /* ── SEND SECTION ── */
  .cl-send {
    margin: 2rem 0;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 2rem;
  }
  .cl-send-inner {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 22px 24px;
  }
  .cl-send-header {
    display: flex; align-items: flex-start; gap: 14px; margin-bottom: 8px;
  }
  .cl-send-icon {
    display: flex; align-items: center; justify-content: center;
    width: 38px; height: 38px; flex-shrink: 0;
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 10px; color: #f59e0b;
    margin-top: 2px;
  }
  .cl-send-heading {
    font-size: clamp(1rem, 2.5vw, 1.2rem); font-weight: 800;
    color: #f8fafc; letter-spacing: -0.01em;
    margin: 0;
  }
  .cl-send-sub {
    font-size: 0.88rem; color: #94a3b8; line-height: 1.6;
    margin: 0 0 16px; max-width: 540px;
  }

  .cl-send-resend {
    background: none;
    border: none;
    color: #f59e0b;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    padding: 0;
    margin-top: 8px;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .cl-send-resend:hover:not(:disabled) { color: #fbbf24; }
  .cl-send-resend:disabled { opacity: 0.5; cursor: not-allowed; }

  .cl-send-btn {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 10px 18px;
    background: #f59e0b; color: #0a0a0a;
    font-size: 0.9rem; font-weight: 800;
    border: none; border-radius: 10px; cursor: pointer;
    white-space: nowrap; flex-shrink: 0;
    box-shadow: 0 2px 12px rgba(245, 158, 11, 0.3);
    transition: filter 0.15s ease, transform 0.2s cubic-bezier(0.34,1.56,0.64,1);
  }
  .cl-send-btn:hover:not(:disabled) { filter: brightness(1.08); transform: translateY(-1px); }
  .cl-send-btn:active:not(:disabled) { transform: scale(0.97); }
  .cl-send-btn:disabled { opacity: 0.45; cursor: not-allowed; transform: none; }

  @keyframes spin { to { transform: rotate(360deg); } }
  .cl-send-spinner {
    display: inline-block;
    width: 13px; height: 13px;
    border: 2px solid rgba(0,0,0,0.2);
    border-top-color: #0a0a0a;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }

  .cl-send-success {
    display: flex; align-items: center; gap: 9px;
    padding: 12px 16px;
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 10px;
    color: #10b981;
    font-size: 0.9rem; font-weight: 600;
  }

  .cl-send-error {
    font-size: 0.84rem; color: #f87171; margin: 0;
  }

  .cl-send-meta {
    font-size: 0.75rem; color: #64748b; margin: 10px 0 0;
  }

  /* ── GO DEEPER ── */
  .cl-deeper {
    margin: 2.5rem 0;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
  }
  .cl-deeper-heading {
    font-size: clamp(1.3rem, 3vw, 1.8rem); font-weight: 800;
    color: #f8fafc; letter-spacing: -0.02em; margin: 0 0 8px;
  }
  .cl-deeper-sub {
    font-size: 0.9rem; color: #94a3b8; line-height: 1.6;
    margin: 0 0 20px; max-width: 520px;
  }
  .cl-chapters { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  @media (max-width: 520px) { .cl-chapters { grid-template-columns: 1fr; } }

  .cl-chapter-card {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; text-decoration: none;
    transition: border-color 0.15s, background 0.15s, transform 0.15s;
  }
  .cl-chapter-card:hover { background: rgba(15, 23, 42, 0.8); border-color: rgba(245,158,11,0.2); transform: translateX(2px); }

  .cl-chapter-n {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem; font-weight: 700; flex-shrink: 0; line-height: 1;
  }
  .cl-chapter-body { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
  .cl-chapter-tag {
    font-size: 0.64rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; line-height: 1;
  }
  .cl-chapter-title { font-size: 0.85rem; font-weight: 600; color: #e2e8f0; line-height: 1.3; }
  .cl-chapter-arrow { color: #64748b; flex-shrink: 0; transition: color 0.15s, transform 0.15s; }
  .cl-chapter-card:hover .cl-chapter-arrow { color: #f59e0b; transform: translate(2px, -2px); }

  /* ── UPGRADE CTA ── */
  .cl-upgrade { margin: 2rem 0 0; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 2rem; }
  .cl-upgrade-inner {
    display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
    background: rgba(245, 158, 11, 0.05);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 16px; padding: 24px 28px;
  }
  .cl-upgrade-text { flex: 1; min-width: 0; }
  .cl-upgrade-heading {
    font-size: clamp(1.3rem, 3vw, 1.8rem); font-weight: 900;
    color: #f8fafc; letter-spacing: -0.02em; margin: 0 0 8px;
  }
  .cl-upgrade-sub { font-size: 0.88rem; color: #cbd5e1; line-height: 1.6; margin: 0; }
  .cl-upgrade-btn {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 13px 22px;
    background: #f59e0b; color: #0a0a0a;
    font-size: 0.92rem; font-weight: 800;
    border-radius: 999px; text-decoration: none; white-space: nowrap;
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3); flex-shrink: 0;
    transition: filter 0.15s, transform 0.2s cubic-bezier(0.34,1.56,0.64,1);
  }
  .cl-upgrade-btn:hover { filter: brightness(1.08); transform: translateY(-2px); }
  @media (max-width: 480px) {
    .cl-upgrade-inner { flex-direction: column; align-items: stretch; text-align: center; }
    .cl-upgrade-btn { justify-content: center; }
  }

  /* ── BOOK SALES ── */
  .cl-book-sales {
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.07);
    display: flex; flex-direction: column; gap: 14px;
    text-align: center;
  }
  .cl-book-sales-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: #f59e0b; margin: 0;
  }
  .cl-book-sales-cover {
    display: block;
    width: min(200px, 55%);
    margin: 0 auto;
    border-radius: 6px;
    box-shadow: 0 20px 48px rgba(0,0,0,0.7), 0 4px 12px rgba(0,0,0,0.4);
  }
  .cl-book-sales-title {
    font-size: clamp(1.2rem, 3vw, 1.6rem); font-weight: 900;
    color: #f8fafc; margin: 0; line-height: 1.1;
    letter-spacing: -0.02em;
  }
  .cl-book-sales-parts {
    list-style: none; padding: 0; margin: 0;
    display: flex; flex-direction: column; gap: 8px;
  }
  .cl-book-sales-parts li {
    font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;
  }
  .cl-book-part-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 700;
    color: #f59e0b; margin-right: 8px;
    text-transform: uppercase; letter-spacing: 0.08em;
  }
  .cl-book-sales-btn {
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%;
    padding: 13px 20px;
    background: #f59e0b; color: #0a0a0a;
    font-size: 0.95rem; font-weight: 800;
    border-radius: 8px; text-decoration: none;
    box-shadow: 0 4px 16px rgba(245,158,11,0.3);
    transition: filter 0.15s ease, transform 0.15s ease;
  }
  .cl-book-sales-btn:hover { filter: brightness(1.08); transform: translateY(-1px); }
  .cl-book-sales-fine {
    font-size: 0.75rem; color: #64748b; margin: 0; text-align: center;
  }
  @media (max-width: 480px) {
    .cl-book-sales-cover { width: 80px; }
    .cl-book-sales-btn { width: 100%; justify-content: center; }
  }

  /* ── PRIMER ── */
  .cl-primer-single {
    font-size: 0.9rem; color: #64748b;
    text-align: center; margin: 0 auto 2rem;
    max-width: 480px; line-height: 1.5;
  }

  /* ── WELCOME VIDEO ── */
  .cl-video-section {
    margin: 0 0 2rem;
  }
  .cl-video-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    border-radius: 12px;
    overflow: hidden;
    background: #000;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }
  .cl-video-wrap iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: none;
  }

  /* ── DISCLAIMER ── */
  .cl-disclaimer {
    text-align: center; font-size: 0.78rem; color: #64748b; margin: 2.5rem 0 0;
  }
  .cl-disclaimer a { color: #64748b; text-decoration: underline; text-underline-offset: 2px; }

  @media (max-width: 500px) {
    .cl-send-btn { width: 100%; justify-content: center; }
  }
</style>
