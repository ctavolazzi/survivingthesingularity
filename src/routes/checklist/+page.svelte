<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import EmailGate from '$lib/components/EmailGate.svelte';

  const categories = {
    foundation:     { label: 'Foundation',     color: '#f59e0b', desc: 'Understand your actual situation before you change anything.' },
    infrastructure: { label: 'Infrastructure', color: '#3b82f6', desc: 'Build the systems that run without you needing to think about them.' },
    autonomy:       { label: 'Autonomy',       color: '#10b981', desc: 'Go from dependent to capable in the areas that matter most.' },
    network:        { label: 'Network',        color: '#a78bfa', desc: 'The social and financial layer that makes everything else stick.' },
  };

  const allItems = [
    {
      n: '01', cat: 'foundation',
      title: 'Audit your single points of failure',
      body: 'List every essential (food, water, power, income, shelter) that depends on one provider you do not control. That list is your real risk map. Not a hypothetical one.',
      action: 'Write down 5 things that would stop working if one company or provider disappeared.',
      cost: '$0', effort: 'low', free: true,
    },
    {
      n: '02', cat: 'foundation',
      title: 'Run one local AI model this week',
      body: 'Install Ollama, pull a small model (llama3, mistral, or phi3), and prove you can get useful answers with no cloud, no subscription, no permission. The tools are already free and run on most laptops.',
      action: 'Install Ollama from ollama.com and run: ollama pull llama3 && ollama run llama3',
      cost: '$0', effort: 'low', free: true,
    },
    {
      n: '03', cat: 'foundation',
      title: 'Calculate your freedom number',
      body: 'The monthly cost to cover your essentials if your income vanished tomorrow. Rent, food, utilities, insurance, debt minimums. Write it down. Everything else you do is a campaign to lower that number or cover it differently.',
      action: "Add up last month's fixed costs. That number is what you're working against.",
      cost: '$0', effort: 'low', free: true,
    },
    {
      n: '04', cat: 'infrastructure',
      title: 'Start a skill that compounds',
      body: 'Pick one high-leverage skill (AI tooling, electronics repair, fabrication, growing food, video editing) and commit 30 minutes a day. Compounding beats intensity. The person who does 30 minutes daily outperforms the weekend warrior in 6 months.',
      action: 'Name the skill. Schedule the first 30 minutes on your calendar for today.',
      cost: '$0-50', effort: 'medium', free: false,
    },
    {
      n: '05', cat: 'infrastructure',
      title: 'Build a 30-day food buffer',
      body: "This is not prepping. It's decoupling. A month of staples (rice, lentils, oats, canned goods) removes the weekly grocery dependency and the anxiety that rides with it. Cost is about $150-250 for one person.",
      action: 'Buy 10 lbs of rice, 5 lbs of lentils, and a case of canned beans this week.',
      cost: '$150-250', effort: 'low', free: false,
    },
    {
      n: '06', cat: 'infrastructure',
      title: 'Open a second income that needs no permission',
      body: "A digital product, a service, content you own: anything that can generate $1 without requiring an employer's approval. The first dollar matters more than the amount. It proves the channel exists and that you control it.",
      action: 'Identify one thing you know that other people would pay to learn. Price it at $10.',
      cost: '$0-20', effort: 'medium', free: false,
    },
    {
      n: '07', cat: 'infrastructure',
      title: 'Map your water and power',
      body: 'Know where they come from and what a 72-hour interruption actually looks like for your household. A $40 water filter and a $200 power station covers most scenarios. You cannot harden what you have not mapped.',
      action: 'Google your utility provider and find the outage history for your area in the last 2 years.',
      cost: '$50-250', effort: 'low', free: false,
    },
    {
      n: '08', cat: 'autonomy',
      title: 'Learn to grow one thing you eat',
      body: 'A single pot of something edible is a proof of concept for food autonomy. Cherry tomatoes on a windowsill. Herbs on a counter. Start absurdly small. The skill transfers. Once you understand one plant, the rest get easier fast.',
      action: 'Buy one packet of seeds for something you actually eat. Plant it today.',
      cost: '$5-15', effort: 'low', free: false,
    },
    {
      n: '09', cat: 'autonomy',
      title: 'Price out a physical exit',
      body: 'Land cost per acre in three regions you would actually move to. Not fantasize about. Actually move to. Turn a vague "someday" into three real numbers. This converts an idea into a plan with a price tag.',
      action: 'Search land prices in 3 rural counties within 200 miles of where you are. Write the numbers down.',
      cost: '$0', effort: 'low', free: false,
    },
    {
      n: '10', cat: 'autonomy',
      title: 'Automate one recurring task with AI',
      body: "Pick something you do every week that's repetitive and mechanical. Summarizing reports, drafting emails, categorizing data, generating outlines. Reclaim the hours and build the muscle of delegating to machines you control.",
      action: 'Pick one weekly task. Spend 20 minutes building a prompt that handles 80% of it.',
      cost: '$0-20/mo', effort: 'medium', free: false,
    },
    {
      n: '11', cat: 'network',
      title: 'Cut fixed monthly obligations by 10%',
      body: 'Every dollar of recurring cost you remove permanently lowers your freedom number. Subscriptions, memberships, fees you forgot about. Audit them. Fixed costs are the enemy of optionality.',
      action: 'Pull up your bank statement. Find every recurring charge. Cancel one this week.',
      cost: '$0', effort: 'low', free: false,
    },
    {
      n: '12', cat: 'network',
      title: 'Find three people building the same way',
      body: "Independence is not isolation. A small group going the same direction is the difference between a phase and a life. You don't need a community of thousands. You need three people who are actually doing the work.",
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

  // ── Send form ──────────────────────────────────────────────────────────────
  let emailToSend = '';
  let honeypot = '';
  let sending = false;
  let sent = false;
  let sendError = '';

  function onUnlock(e) {
    if (e.detail?.email) emailToSend = e.detail.email;
  }

  async function handleSend(e) {
    e.preventDefault();
    if (honeypot || sending || sent) return;
    sending = true;
    sendError = '';
    try {
      const res = await fetch('/api/checklist-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: emailToSend.trim(),
          honeypot,
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
  <meta name="description" content="12 concrete moves to build real independence before AGI changes everything. Check off steps, add your own notes, and email yourself the results." />
</svelte:head>

<div class="cl-page">

  <!-- ── HERO ── -->
  <header class="cl-hero">
    <h1 class="cl-title">The Singularity<br>Readiness Checklist</h1>
    <p class="cl-lede">
      12 concrete moves to build real independence before the window closes.<br>Check off steps, add your own notes, and email yourself everything you filled in.
    </p>

    <div class="cl-stats">
      <div class="cl-stat">
        <span class="cl-stat-n">12</span>
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
        <span class="cl-stat-n cl-stat-progress" aria-live="polite">{checkedCount}/12</span>
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
  <div class="cl-primer">
    <div class="cl-primer-body">
      <p class="cl-primer-quote">
        12 steps toward real independence. Each one has a concrete action you can take this week.
      </p>
      <ol class="cl-primer-how">
        <li>Check each step off after you've done the action</li>
        <li>Add your notes as you go</li>
        <li>Email yourself the results at the end</li>
      </ol>
      <p class="cl-primer-cta">Start with step 01.</p>
    </div>
  </div>

  <!-- ── CHECKLIST with EmailGate ── -->
  <EmailGate
    storageKey="checklist"
    source="checklist"
    headline="Unlock all 12 steps"
    sub="You've seen the first three. Enter your email and the rest open right here, plus you can email yourself your notes when you're done."
    buttonText="Unlock the Full Checklist"
    on:unlock={onUnlock}
  >
    <!-- Free teaser items — always interactive -->
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

    <!-- Book preview inside the gate card, below the email form -->
    <div slot="gate-extra" class="cl-book-callout">
      <img
        src="/images/surviving_the_singularity_cover_1200.png"
        alt="Surviving the Singularity book cover"
        class="cl-book-cover"
        loading="lazy"
      />
      <div class="cl-book-info">
        <p class="cl-book-eyebrow">The Book</p>
        <h3 class="cl-book-title">Surviving the Singularity</h3>
        <p class="cl-book-desc">A field guide to building real independence before AGI reshapes work, income, and daily life. The checklist above is drawn directly from it.</p>
        <p class="cl-book-release">Coming August 2026 · <a href="/launch" class="cl-book-link">See the launch plan</a></p>
      </div>
    </div>

    <!-- Gated: items 4-12 + send section + deeper content -->
    <div slot="gated">
      <ol class="cl-list cl-list-gated" start="4" aria-label="Remaining nine checklist items">
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

      <!-- ── EMAIL YOUR ANSWERS ── -->
      <section class="cl-send" aria-label="Email your checklist">
        <div class="cl-send-inner">
          <div class="cl-send-header">
            <div class="cl-send-icon" aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
              </svg>
            </div>
            <div>
              <p class="cl-section-label">Save your progress</p>
              <h2 class="cl-send-heading">Email yourself your answers + the full checklist.</h2>
            </div>
          </div>
          <p class="cl-send-sub">
            We'll send everything you checked and wrote, plus the complete 12 steps, formatted for your inbox. Nothing is stored on our end beyond the send.
          </p>

          {#if sent}
            <div class="cl-send-success" role="status">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
              Sent! Check your inbox. ({checkedCount}/12 steps in the email.)
            </div>
          {:else}
            <form class="cl-send-form" on:submit={handleSend} novalidate>
              <!-- Honeypot — hidden from humans, visible to bots -->
              <input
                type="text"
                name="website"
                bind:value={honeypot}
                tabindex="-1"
                aria-hidden="true"
                autocomplete="off"
                style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none;"
              />
              <div class="cl-send-row">
                <input
                  type="email"
                  class="cl-send-input"
                  bind:value={emailToSend}
                  placeholder="your@email.com"
                  required
                  maxlength="254"
                  autocomplete="email"
                  disabled={sending}
                  aria-label="Your email address"
                />
                <button
                  type="submit"
                  class="cl-send-btn"
                  disabled={sending || !emailToSend.trim()}
                >
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
              </div>
              {#if sendError}
                <p class="cl-send-error" role="alert">{sendError}</p>
              {/if}
            </form>
          {/if}

          <p class="cl-send-meta">
            {checkedCount} of 12 steps checked · {allItems.filter(i => answers[i.n].notes.trim()).length} with notes · Zero spam, reply to unsubscribe.
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
            <a href="/blueprint/{ch.slug}" class="cl-chapter-card">
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
            <p class="cl-upgrade-sub">Unlock all 8 blueprint chapters, the live research signal feed, the book draft, and every tool I build next. One payment, instant access.</p>
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

  .cl-lede {
    font-size: clamp(0.95rem, 2.5vw, 1.05rem);
    color: #cbd5e1; line-height: 1.65;
    margin: 0 auto 28px; max-width: 560px;
  }

  .cl-stats {
    display: inline-flex; align-items: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 12px 24px;
    flex-wrap: wrap; justify-content: center; gap: 0;
  }
  .cl-stat {
    display: flex; flex-direction: column; align-items: center;
    padding: 0 20px;
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

  .cl-send-form { display: flex; flex-direction: column; gap: 8px; }
  .cl-send-row {
    display: flex; gap: 8px; flex-wrap: wrap;
  }
  .cl-send-input {
    flex: 1; min-width: 0;
    padding: 10px 14px;
    background: rgba(2, 6, 23, 0.6);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    color: #f1f5f9;
    font-size: 0.9rem;
    transition: border-color 0.15s ease;
    outline: none;
  }
  .cl-send-input::placeholder { color: #64748b; }
  .cl-send-input:focus { border-color: rgba(245, 158, 11, 0.5); }
  .cl-send-input:disabled { opacity: 0.5; }

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

  /* ── BOOK CALLOUT ── */
  .cl-book-callout {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.07);
  }
  .cl-book-cover {
    width: 72px;
    flex-shrink: 0;
    border-radius: 4px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
  }
  .cl-book-info { flex: 1; min-width: 0; }
  .cl-book-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: #f59e0b; margin: 0 0 4px;
  }
  .cl-book-title {
    font-size: 1rem; font-weight: 800;
    color: #f8fafc; margin: 0 0 6px; line-height: 1.2;
  }
  .cl-book-desc {
    font-size: 0.84rem; color: #cbd5e1;
    line-height: 1.6; margin: 0 0 8px;
  }
  .cl-book-release {
    font-size: 0.78rem; color: #94a3b8; margin: 0;
  }
  .cl-book-link {
    color: #f59e0b; text-decoration: none;
    font-weight: 600;
  }
  .cl-book-link:hover { text-decoration: underline; }

  @media (max-width: 480px) {
    .cl-book-callout { flex-direction: column; align-items: flex-start; }
    .cl-book-cover { width: 56px; }
  }

  /* ── PRIMER ── */
  .cl-primer {
    margin-bottom: 2rem;
    background: rgba(245, 158, 11, 0.04);
    border: 1px solid rgba(245, 158, 11, 0.14);
    border-left: 3px solid rgba(245, 158, 11, 0.6);
    border-radius: 14px;
    overflow: hidden;
  }
  .cl-primer-body {
    padding: 22px 24px 18px;
  }
  .cl-primer-quote {
    font-size: clamp(1rem, 2.5vw, 1.15rem);
    font-weight: 600;
    color: #e2e8f0;
    line-height: 1.55;
    margin: 0 0 10px;
  }
  .cl-primer-quote strong { color: #f8fafc; font-weight: 800; }
  .cl-primer-how {
    list-style: none;
    counter-reset: step;
    margin: 0 0 12px;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .cl-primer-how li {
    counter-increment: step;
    display: flex;
    align-items: baseline;
    gap: 10px;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.5;
  }
  .cl-primer-how li::before {
    content: counter(step);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    color: #f59e0b;
    flex-shrink: 0;
    min-width: 14px;
  }
  .cl-primer-cta {
    font-size: 0.88rem;
    font-weight: 700;
    color: #f59e0b;
    margin: 0;
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
    .cl-send-row { flex-direction: column; }
    .cl-send-btn { width: 100%; justify-content: center; }
    .cl-send-input { width: 100%; }
  }
</style>
