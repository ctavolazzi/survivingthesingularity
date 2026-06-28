<script>
  import EmailGate from '$lib/components/EmailGate.svelte';

  // Category groupings with colors
  const categories = {
    foundation: { label: 'Foundation', color: '#f59e0b', desc: 'Understand your actual situation before you change anything.' },
    infrastructure: { label: 'Infrastructure', color: '#3b82f6', desc: 'Build the systems that run without you needing to think about them.' },
    autonomy: { label: 'Autonomy', color: '#10b981', desc: 'Go from dependent to capable in the areas that matter most.' },
    network: { label: 'Network', color: '#a78bfa', desc: 'The social and financial layer that makes everything else stick.' },
  };

  const allItems = [
    {
      n: '01', cat: 'foundation',
      title: 'Audit your single points of failure',
      body: 'List every essential (food, water, power, income, shelter) that depends on one provider you do not control. That list is your real risk map — not a hypothetical one.',
      action: 'Write down 5 things that would stop working if one company or provider disappeared.',
      cost: '$0', effort: 'low',
      free: true,
    },
    {
      n: '02', cat: 'foundation',
      title: 'Run one local AI model this week',
      body: 'Install Ollama, pull a small model (llama3, mistral, or phi3), and prove you can get useful answers with no cloud, no subscription, no permission. The tools are already free and run on most laptops.',
      action: 'Install Ollama from ollama.com and run: ollama pull llama3 && ollama run llama3',
      cost: '$0', effort: 'low',
      free: true,
    },
    {
      n: '03', cat: 'foundation',
      title: 'Calculate your freedom number',
      body: 'The monthly cost to cover your essentials if your income vanished tomorrow. Rent, food, utilities, insurance, debt minimums. Write it down. Everything else you do is a campaign to lower that number or cover it differently.',
      action: 'Add up last month\'s fixed costs. That number is what you\'re working against.',
      cost: '$0', effort: 'low',
      free: true,
    },
    {
      n: '04', cat: 'infrastructure',
      title: 'Start a skill that compounds',
      body: 'Pick one high-leverage skill (AI tooling, electronics repair, fabrication, growing food, video editing) and commit 30 minutes a day. Compounding beats intensity — the person who does 30 minutes daily outperforms the weekend warrior in 6 months.',
      action: 'Name the skill. Schedule the first 30 minutes on your calendar for today.',
      cost: '$0-50', effort: 'medium',
      free: false,
    },
    {
      n: '05', cat: 'infrastructure',
      title: 'Build a 30-day food buffer',
      body: 'This is not prepping. It\'s decoupling. A month of staples (rice, lentils, oats, canned goods) removes the weekly grocery dependency and the anxiety that rides with it. Cost is about $150-250 for one person.',
      action: 'Buy 10 lbs of rice, 5 lbs of lentils, and a case of canned beans this week.',
      cost: '$150-250', effort: 'low',
      free: false,
    },
    {
      n: '06', cat: 'infrastructure',
      title: 'Open a second income that needs no permission',
      body: 'A digital product, a service, content you own — anything that can generate $1 without requiring an employer\'s approval. The first dollar matters more than the amount. It proves the channel exists and that you control it.',
      action: 'Identify one thing you know that other people would pay to learn. Price it at $10.',
      cost: '$0-20', effort: 'medium',
      free: false,
    },
    {
      n: '07', cat: 'infrastructure',
      title: 'Map your water and power',
      body: 'Know where they come from and what a 72-hour interruption actually looks like for your household. A $40 water filter and a $200 power station covers most scenarios. You cannot harden what you have not mapped.',
      action: 'Google your utility provider and find the outage history for your area in the last 2 years.',
      cost: '$50-250', effort: 'low',
      free: false,
    },
    {
      n: '08', cat: 'autonomy',
      title: 'Learn to grow one thing you eat',
      body: 'A single pot of something edible is a proof of concept for food autonomy. Cherry tomatoes on a windowsill. Herbs on a counter. Start absurdly small. The skill transfers — once you understand one plant, the rest get easier fast.',
      action: 'Buy one packet of seeds for something you actually eat. Plant it today.',
      cost: '$5-15', effort: 'low',
      free: false,
    },
    {
      n: '09', cat: 'autonomy',
      title: 'Price out a physical exit',
      body: 'Land cost per acre in three regions you would actually move to. Not fantasize about — actually move to. Turn a vague "someday" into three real numbers. This converts an idea into a plan with a price tag.',
      action: 'Search land prices in 3 rural counties within 200 miles of where you are. Write the numbers down.',
      cost: '$0', effort: 'low',
      free: false,
    },
    {
      n: '10', cat: 'autonomy',
      title: 'Automate one recurring task with AI',
      body: 'Pick something you do every week that\'s repetitive and mechanical. Summarizing reports, drafting emails, categorizing data, generating outlines. Reclaim the hours and build the muscle of delegating to machines you control.',
      action: 'Pick one weekly task. Spend 20 minutes building a prompt that handles 80% of it.',
      cost: '$0-20/mo', effort: 'medium',
      free: false,
    },
    {
      n: '11', cat: 'network',
      title: 'Cut fixed monthly obligations by 10%',
      body: 'Every dollar of recurring cost you remove permanently lowers your freedom number. Subscriptions, memberships, fees you forgot about — audit them. Fixed costs are the enemy of optionality.',
      action: 'Pull up your bank statement. Find every recurring charge. Cancel one this week.',
      cost: '$0', effort: 'low',
      free: false,
    },
    {
      n: '12', cat: 'network',
      title: 'Find three people building the same way',
      body: 'Independence is not isolation. A small group going the same direction is the difference between a phase and a life. You don\'t need a community of thousands — you need three people who are actually doing the work.',
      action: 'Message one person today who you think is building toward real independence. Tell them what you\'re doing.',
      cost: '$0', effort: 'low',
      free: false,
    },
  ];

  const teaser = allItems.filter(i => i.free);
  const gated = allItems.filter(i => !i.free);

  // Blueprint chapters that connect to checklist themes
  const relatedChapters = [
    { n: '01', title: 'The AGI Transition', slug: 'agi-transition', tag: 'Foundation', color: '#f59e0b' },
    { n: '02', title: 'Local AI Infrastructure', slug: 'local-ai', tag: 'Foundation', color: '#f59e0b' },
    { n: '04', title: 'Food Security Systems', slug: 'food-security', tag: 'Autonomy', color: '#10b981' },
    { n: '06', title: 'Digital Leverage', slug: 'digital-leverage', tag: 'Infrastructure', color: '#3b82f6' },
    { n: '07', title: 'Energy Independence', slug: 'energy', tag: 'Infrastructure', color: '#3b82f6' },
    { n: '08', title: 'Physical Automation', slug: 'physical-automation', tag: 'Autonomy', color: '#10b981' },
  ];
</script>

<svelte:head>
  <title>Free Readiness Checklist — Surviving the Singularity</title>
  <meta name="description" content="12 concrete moves to build real independence before AGI changes everything. Free, specific, start this week. Includes cost estimates and first actions per step." />
</svelte:head>

<div class="cl-page">

  <!-- ── HERO ── -->
  <header class="cl-hero">
    <p class="cl-eyebrow">
      <span class="cl-eyebrow-dot" aria-hidden="true"></span>
      Free · No account needed
    </p>
    <h1 class="cl-title">The Singularity<br>Readiness Checklist</h1>
    <p class="cl-lede">
      12 concrete moves to build real independence before the window closes. Each one has a specific first action, a cost estimate, and a reason it's here. No theory. Start this week.
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
        <span class="cl-stat-n">Free</span>
        <span class="cl-stat-l">first 3 items</span>
      </div>
    </div>
  </header>

  <!-- ── CATEGORIES KEY ── -->
  <div class="cl-categories">
    {#each Object.entries(categories) as [key, cat]}
      <div class="cl-cat-pill" style="--cat-color: {cat.color}">
        <span class="cl-cat-dot" aria-hidden="true"></span>
        {cat.label}
      </div>
    {/each}
  </div>

  <!-- ── CHECKLIST with EmailGate ── -->
  <EmailGate
    storageKey="checklist"
    source="checklist"
    headline="Unlock all 12 steps"
    sub="You've seen the first three. Enter your email and the rest open right here — cost estimates, first actions, and all."
    buttonText="Unlock the Full Checklist"
  >
    <!-- Free teaser items -->
    <ol class="cl-list" aria-label="First three checklist items, free">
      {#each teaser as item}
        <li class="cl-item" style="--cat-color: {categories[item.cat].color}">
          <div class="cl-item-head">
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
        </li>
      {/each}
    </ol>

    <!-- Gated: all 9 remaining + deeper content -->
    <div slot="gated">
      <ol class="cl-list cl-list-gated" start="4" aria-label="Remaining nine checklist items">
        {#each gated as item}
          <li class="cl-item" style="--cat-color: {categories[item.cat].color}">
            <div class="cl-item-head">
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
          </li>
        {/each}
      </ol>

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

  .cl-eyebrow {
    display: inline-flex; align-items: center; gap: 7px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: #f59e0b; margin-bottom: 16px;
  }
  .cl-eyebrow-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #f59e0b; box-shadow: 0 0 6px #f59e0b;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
  }
  @media (prefers-reduced-motion: reduce) { .cl-eyebrow-dot { animation: none; } }

  .cl-title {
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 900; color: #f8fafc;
    letter-spacing: -0.03em; line-height: 1.05;
    margin: 0 0 16px;
  }

  .cl-lede {
    font-size: clamp(0.95rem, 2.5vw, 1.05rem);
    color: #94a3b8; line-height: 1.65;
    margin: 0 auto 28px; max-width: 560px;
  }

  .cl-stats {
    display: inline-flex; align-items: center; gap: 0;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 12px 24px;
    flex-wrap: wrap; justify-content: center;
  }
  .cl-stat {
    display: flex; flex-direction: column; align-items: center;
    padding: 0 20px;
  }
  .cl-stat-n {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem; font-weight: 700; color: #f59e0b; line-height: 1;
  }
  .cl-stat-l {
    font-size: 0.7rem; color: #64748b;
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
    font-size: 0.78rem; font-weight: 600;
    color: var(--cat-color);
  }
  .cl-cat-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: currentColor;
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
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .cl-item:hover {
    border-color: color-mix(in srgb, var(--cat-color) 35%, transparent);
    border-left-color: var(--cat-color);
    box-shadow: 0 6px 24px rgba(0,0,0,0.2);
  }

  .cl-item-head {
    display: flex; align-items: center; gap: 8px;
    flex-wrap: wrap; margin-bottom: 10px;
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
  .cl-item-meta {
    display: flex; gap: 6px; margin-left: auto;
  }
  .cl-meta-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 600;
    color: #64748b;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 2px 7px; border-radius: 4px;
    white-space: nowrap;
  }

  .cl-item-title {
    font-size: 1rem; font-weight: 700; color: #f1f5f9;
    margin: 0 0 6px; line-height: 1.3;
  }
  .cl-item-text {
    font-size: 0.9rem; color: #94a3b8;
    line-height: 1.65; margin: 0 0 12px;
  }

  .cl-action {
    background: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 8px;
    padding: 10px 14px;
  }
  .cl-action-label {
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em;
    color: #f59e0b; margin-bottom: 4px;
  }
  .cl-action-text {
    font-size: 0.85rem; color: #e2e8f0;
    line-height: 1.5; margin: 0;
  }

  /* ── SECTION LABELS ── */
  .cl-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: #f59e0b; margin-bottom: 8px;
  }

  /* ── GO DEEPER ── */
  .cl-deeper {
    margin: 2.5rem 0;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
  }
  .cl-deeper-heading {
    font-size: clamp(1.3rem, 3vw, 1.8rem); font-weight: 800;
    color: #f8fafc; letter-spacing: -0.02em;
    margin: 0 0 8px;
  }
  .cl-deeper-sub {
    font-size: 0.9rem; color: #64748b;
    line-height: 1.6; margin: 0 0 20px; max-width: 520px;
  }

  .cl-chapters {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  @media (max-width: 520px) { .cl-chapters { grid-template-columns: 1fr; } }

  .cl-chapter-card {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; text-decoration: none;
    transition: border-color 0.15s, background 0.15s, transform 0.15s;
  }
  .cl-chapter-card:hover {
    background: rgba(15, 23, 42, 0.8);
    border-color: rgba(245, 158, 11, 0.2);
    transform: translateX(2px);
  }
  .cl-chapter-n {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem; font-weight: 700; flex-shrink: 0; line-height: 1;
  }
  .cl-chapter-body {
    display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0;
  }
  .cl-chapter-tag {
    font-size: 0.64rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; line-height: 1;
  }
  .cl-chapter-title {
    font-size: 0.85rem; font-weight: 600; color: #e2e8f0; line-height: 1.3;
  }
  .cl-chapter-arrow {
    color: #334155; flex-shrink: 0;
    transition: color 0.15s, transform 0.15s;
  }
  .cl-chapter-card:hover .cl-chapter-arrow { color: #f59e0b; transform: translate(2px, -2px); }

  /* ── UPGRADE CTA ── */
  .cl-upgrade {
    margin: 2rem 0 0;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 2rem;
  }
  .cl-upgrade-inner {
    display: flex; align-items: center; gap: 24px;
    flex-wrap: wrap;
    background: rgba(245, 158, 11, 0.05);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 16px;
    padding: 24px 28px;
  }
  .cl-upgrade-text { flex: 1; min-width: 200px; }
  .cl-upgrade-heading {
    font-size: clamp(1.3rem, 3vw, 1.8rem); font-weight: 900;
    color: #f8fafc; letter-spacing: -0.02em; margin: 0 0 8px;
  }
  .cl-upgrade-sub {
    font-size: 0.88rem; color: #94a3b8; line-height: 1.6; margin: 0;
  }
  .cl-upgrade-btn {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 13px 22px;
    background: #f59e0b; color: #0a0a0a;
    font-size: 0.92rem; font-weight: 800;
    border-radius: 999px; text-decoration: none; white-space: nowrap;
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
    flex-shrink: 0;
    transition: filter 0.15s, transform 0.2s cubic-bezier(0.34,1.56,0.64,1);
  }
  .cl-upgrade-btn:hover { filter: brightness(1.08); transform: translateY(-2px); }

  /* ── DISCLAIMER ── */
  .cl-disclaimer {
    text-align: center; font-size: 0.78rem;
    color: #334155; margin: 2.5rem 0 0;
  }
  .cl-disclaimer a { color: #475569; text-decoration: underline; text-underline-offset: 2px; }
</style>
