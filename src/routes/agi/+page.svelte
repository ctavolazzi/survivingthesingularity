<script>
  import { onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';
  import AGICountdown from '$lib/components/AGICountdown.svelte';

  let heroVisible = false;
  onMount(() => { heroVisible = true; });

  function observe(node) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.06, rootMargin: '0px 0px -40px 0px' }
    );
    io.observe(node);
    return { destroy: () => io.disconnect() };
  }

  const aiLevels = [
    {
      id: 'narrow',
      label: 'Narrow AI',
      status: 'now',
      statusLabel: 'We are here',
      color: '#3b82f6',
      description: 'AI that does one thing very well: image recognition, language generation, game playing. Every AI product you use today is narrow AI. Incredibly capable within its domain, completely helpless outside it.',
      examples: ['ChatGPT / Claude / Gemini', 'DALL-E / Midjourney', 'AlphaFold', 'Tesla Autopilot'],
    },
    {
      id: 'agi',
      label: 'AGI',
      status: 'coming',
      statusLabel: 'Coming soon',
      color: '#f59e0b',
      description: 'Artificial General Intelligence, meaning AI that can learn, reason, and perform at human level across any intellectual task. No domain restrictions. It can read a biology paper, write code, design an experiment, and critique the results, all without task-specific training.',
      examples: ['Autonomous research agents', 'Self-improving systems', 'Full economic automation', 'Scientific discovery at scale'],
    },
    {
      id: 'asi',
      label: 'ASI',
      status: 'after',
      statusLabel: 'Beyond AGI',
      color: '#fb923c',
      description: 'Artificial Superintelligence, meaning AI that exceeds the combined cognitive capacity of all humans. Once AGI exists and can improve itself, the path to ASI may be very short. This is the event horizon where most predictions break down.',
      examples: ['Self-directed improvement', 'Problems no human could solve', 'Civilizational restructuring'],
    },
  ];

  const timelineForecasts = [
    { source: 'Sam Altman (OpenAI CEO)', year: '2025–2027', confidence: 'AGI within this decade, possibly years', color: '#f59e0b' },
    { source: 'Demis Hassabis (Google DeepMind)', year: '5–10 years', confidence: 'High confidence AGI before 2030', color: '#3b82f6' },
    { source: 'Yoshua Bengio', year: '2033–2060', confidence: 'More cautious: many unsolved problems', color: '#8b5cf6' },
    { source: 'Dario Amodei (Anthropic CEO)', year: '2026–2028', confidence: '"Powerful AI" equivalent to AGI very soon', color: '#f59e0b' },
    { source: 'Geoffrey Hinton', year: '5–20 years', confidence: 'Faster than expected; recently more alarmed', color: '#fb923c' },
    { source: 'Yann LeCun (Meta AI)', year: '20–50 years', confidence: 'Skeptical current approaches reach AGI at all', color: '#dde4ef' },
  ];

  const humanityPotential = [
    {
      domain: 'Medicine',
      icon: '⚕',
      color: '#10b981',
      headline: 'Compress centuries of medical research into years',
      body: 'AGI could model every protein interaction, simulate every drug combination, and personalize treatment protocols for every patient simultaneously. Cancer, Alzheimer\'s, and aging itself, problems too complex for human researchers to hold in their heads, all become tractable.',
    },
    {
      domain: 'Science',
      icon: '🔬',
      color: '#3b82f6',
      headline: 'Run experiments 24/7 at machine speed',
      body: 'Science is bottlenecked by human cognitive bandwidth and the linear pace of experiment cycles. AGI eliminates that bottleneck. Climate models, fusion energy, materials science: the 100-year roadmaps compress to a decade.',
    },
    {
      domain: 'Economics',
      icon: '⚡',
      color: '#f59e0b',
      headline: 'Produce abundance for the cost of energy',
      body: 'When intelligence is no longer scarce, the economics of production transform. Software, analysis, design, strategy, and coordination approach zero marginal cost. The question becomes: who owns the systems, and who benefits?',
    },
    {
      domain: 'Education',
      icon: '🧠',
      color: '#8b5cf6',
      headline: 'Every person gets a world-class tutor, always',
      body: 'An AGI tutor that knows your learning style, your gaps, your pace, and has unlimited patience and expertise in every subject, is more than a tool. It\'s access to the quality of education currently reserved for the global elite.',
    },
    {
      domain: 'Labor',
      icon: '🤖',
      color: '#f59e0b',
      headline: 'Automation scales from routine to cognitive',
      body: 'Narrow AI already automates routine tasks. AGI extends automation to complex cognitive work: legal analysis, financial planning, engineering design, medical diagnosis. No profession is fully immune. The transition will be faster than any previous labor shift.',
    },
    {
      domain: 'Climate',
      icon: '🌍',
      color: '#10b981',
      headline: 'Solve problems humans can\'t coordinate around',
      body: 'Climate change is a coordination and complexity problem at a scale humans struggle with. AGI could model planetary systems, optimize grids, design carbon capture at scale, and coordinate logistics across nations, without the friction of human politics.',
    },
  ];

  const prepActions = [
    {
      num: '01',
      title: 'Understand what\'s actually coming',
      body: 'Not the hype, not the doom. The realistic middle. Read primary sources. Follow the researchers building these systems, not just the commentators. The people closest to the work are the most informative and often the most alarmed.',
      cta: null,
    },
    {
      num: '02',
      title: 'Build leverage that survives automation',
      body: 'Skills that rely on human judgment, physical presence, relationship trust, and creative direction are more durable than pure information processing. The question isn\'t "will my job exist?" It\'s "what value do I provide that a system can\'t?"',
      cta: null,
    },
    {
      num: '03',
      title: 'Reduce dependency on fragile systems',
      body: 'If the economic disruption from AGI is fast and uneven, and it may well be, the people who fare best will be those with the lowest structural exposure. Lower fixed costs, diversified income, owned assets, and local resilience matter more than they did a decade ago.',
      cta: { label: 'See the Blueprint →', href: '/blueprint' },
    },
    {
      num: '04',
      title: 'Engage now, not when it\'s obvious',
      body: 'The window for preparation is before the inflection point, not after. By the time AGI\'s impacts are obvious to everyone, the best positions will already be taken. Engagement while it\'s still early is the differentiator.',
      cta: { label: 'Read the Book →', href: '/book' },
    },
  ];

  // ─── SCENARIO EXPLORER (ported + compressed from /timeline) ───
  // Everything here is illustrative conjecture, not a forecast or advice.
  const incomeOptions = [
    { label: '$2K', value: 2000 },
    { label: '$3.5K', value: 3500 },
    { label: '$5K', value: 5000 },
    { label: '$8K', value: 8000 },
    { label: '$12K', value: 12000 },
    { label: '$20K+', value: 20000 },
  ];
  const savingsRateOptions = [
    { label: '5%', pct: 0.05 }, { label: '10%', pct: 0.10 }, { label: '15%', pct: 0.15 },
    { label: '20%', pct: 0.20 }, { label: '30%', pct: 0.30 }, { label: '40%', pct: 0.40 },
  ];
  const regionOptions = [
    { label: 'Rural South / Midwest', landMultiplier: 0.5 },
    { label: 'Rural West', landMultiplier: 1.0 },
    { label: 'Rural Northeast', landMultiplier: 1.6 },
    { label: 'International (low-cost)', landMultiplier: 0.25 },
    { label: 'Suburban edge', landMultiplier: 2.2 },
  ];
  const shouseSizeOptions = [
    { label: 'Minimal (1,000 sq ft)', buildMultiplier: 0.6 },
    { label: 'Medium (2,000 sq ft)', buildMultiplier: 1.0 },
    { label: 'Large (3,500 sq ft)', buildMultiplier: 1.6 },
  ];

  let selIncome = 2, selRate = 2, selRegion = 0, selSize = 1;

  const BASE_LAND = 18000, BASE_SHOUSE = 60000, BASE_SOLAR = 12000, BASE_WATER = 6000,
        BASE_FARMBOT = 4500, BASE_LOCAL_AI = 3500, BASE_MISC = 8000;

  $: monthlySavings = Math.round(incomeOptions[selIncome].value * savingsRateOptions[selRate].pct);
  $: costs = {
    land: Math.round(BASE_LAND * regionOptions[selRegion].landMultiplier),
    shouse: Math.round(BASE_SHOUSE * shouseSizeOptions[selSize].buildMultiplier),
    solar: BASE_SOLAR, water: BASE_WATER, farmbot: BASE_FARMBOT, localAI: BASE_LOCAL_AI, misc: BASE_MISC,
  };
  $: totalCost = Object.values(costs).reduce((a, b) => a + b, 0);
  $: yearsToTotal = monthlySavings > 0 ? Math.ceil(totalCost / monthlySavings) / 12 : Infinity;

  function fmt(n) { return isFinite(n) ? '$' + n.toLocaleString() : 'n/a'; }
  function fmtY(y) {
    if (!isFinite(y)) return 'n/a';
    return y < 1 ? Math.round(y * 12) + ' months' : y.toFixed(1) + ' years';
  }

  const costCategories = [
    { key: 'land', label: 'Land', icon: '🌾', note: 'Varies wildly by region and parcel. Rural farmland median ~$3.6K/acre nationally (USDA 2023), but ranges from hundreds to hundreds of thousands per acre by location.' },
    { key: 'shouse', label: 'Shop/House', icon: '🏗️', note: 'Steel kit + rough finish. Excludes permits, foundation, HVAC, electrical, plumbing, finished interiors, all of which add cost that varies by county and contractor.' },
    { key: 'solar', label: 'Solar + Battery', icon: '☀️', note: 'Rough 6kW + storage estimate. Real cost depends on system size, incentives, installer, site. Federal ITC may apply; consult a tax professional.' },
    { key: 'water', label: 'Water', icon: '💧', note: 'Well drilling varies enormously by depth and geology, roughly $15–$50+/foot. Rainwater collection may be an option depending on local law.' },
    { key: 'farmbot', label: 'FarmBot', icon: '🤖', note: 'FarmBot Genesis retail estimate. One unit covers a small raised bed, not a farm. Real food production needs more land, labor, and a longer learning curve.' },
    { key: 'localAI', label: 'Local AI Rig', icon: '💻', note: 'GPU workstation for 70B+ local models. Hardware capability shifts rapidly; check current benchmarks before buying.' },
    { key: 'misc', label: 'Permits + Tools', icon: '🔧', note: 'Permits, basic tools, contingency. Permit costs alone range from hundreds to tens of thousands by jurisdiction. Always budget a buffer.' },
  ];

  // ─── TECHNOLOGY WATCH LIST (ported + compressed from /timeline) ───
  const techItems = [
    { name: 'Unitree H1 / G1', category: 'Robotics · General', color: '#f59e0b', status: 'Commercial (limited)', priceRange: '$16K–$90K (est., varies)', availability: 'Select markets, 2024–2025', relevance: 'One of the first sub-$100K humanoids reaching commercial availability. Research-grade, not consumer. Requires technical integration skill.', cautions: 'High cost, thin software ecosystem, physically delicate, rapid version churn. Not a farm-labor replacement today.', links: [{ label: 'Unitree', href: 'https://www.unitree.com/' }] },
    { name: 'Figure AI (Figure 02)', category: 'Robotics · General', color: '#f59e0b', status: 'Pre-commercial', priceRange: 'Not disclosed; BMW partnership 2024', availability: 'Industrial pilots only as of 2025', relevance: 'Well-funded humanoid company, OpenAI partnership 2024. Targets general-purpose manipulation. May matter for small-holder land work on a 5–10 year horizon.', cautions: 'Not consumer-available. Funding ≠ product readiness. Affordable general-purpose timeline is speculative.', links: [{ label: 'Figure AI', href: 'https://www.figure.ai/' }] },
    { name: 'Agility Robotics (Digit)', category: 'Robotics · Logistics', color: '#f59e0b', status: 'Commercial (warehouse)', priceRange: 'Not disclosed; Amazon partnership', availability: 'Warehouse deployment, 2024–2025', relevance: 'Amazon-backed humanoid for pick-and-place. Not built for outdoor/ag use, but proves commercial viability of general manipulation.', cautions: 'Designed for structured indoor environments. Outdoor unstructured work (farming, construction) is a harder problem.', links: [{ label: 'Agility', href: 'https://agilityrobotics.com/' }] },
    { name: 'FarmBot Genesis / Express', category: 'Robotics · Ag CNC', color: '#10b981', status: 'Commercial (consumer)', priceRange: 'Genesis ~$4,495 | Express ~$2,995 (2025 est.)', availability: 'Ships globally. Open-source HW + SW.', relevance: 'CNC food-growing robot: seeds, waters, weeds raised beds up to ~18 sq ft. Open-source, hackable, active community. The realistic near-term automated-growing option.', cautions: 'Covers a garden bed, not a farm. Needs power, water, Wi-Fi. Not a food-security solution alone.', links: [{ label: 'FarmBot.io', href: 'https://farm.bot/' }, { label: 'GitHub', href: 'https://github.com/FarmBot' }] },
    { name: 'Open-weights LLMs', category: 'Local AI · Models', color: '#8b5cf6', status: 'Active development', priceRange: 'Free models. Hardware $800–$5K+ for useful local inference', availability: 'Now: Llama, Mistral, Phi, Qwen, Gemma, etc.', relevance: 'Capable language models run locally on consumer hardware today: writing, code, research synthesis, private Q&A with no cloud dependency.', cautions: 'Capability changes monthly; specific picks go stale fast. Useful local models want 16GB+ RAM. Not equal to frontier cloud models for hard tasks.', links: [{ label: 'Ollama', href: 'https://ollama.com/' }, { label: 'LM Studio', href: 'https://lmstudio.ai/' }] },
    { name: 'RTX 5090 / 5080', category: 'Local AI · Hardware', color: '#8b5cf6', status: 'Active landscape', priceRange: '$1,000–$2,500+ by model/availability', availability: 'RTX 5090 announced CES 2025', relevance: 'Consumer GPUs that run 70B+ models locally. A meaningful jump over the prior generation for local inference.', cautions: 'Stock and prices fluctuate. AMD/Intel are competitive. A GPU bought today may be outperformed by model/software gains within 12 months.', links: [{ label: 'NVIDIA 50 series', href: 'https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/' }] },
    { name: 'Mobile Aloha (Stanford)', category: 'Robotics · Research', color: '#f59e0b', status: 'Research only', priceRange: '~$32K research build (2024)', availability: 'Open-source plans, not a product', relevance: 'Demonstrated two-handed home tasks (cooking, laundry) via imitation learning. The research frontier of affordable dexterous robots.', cautions: 'Research project, not a product. Needs real robotics expertise to replicate. Not ready for general use.', links: [{ label: 'Mobile Aloha', href: 'https://mobile-aloha.github.io/' }] },
    { name: 'Off-grid solar', category: 'Energy Independence', color: '#fbbf24', status: 'Mature commercial', priceRange: '$8K–$25K installed, basic home system (varies)', availability: 'Widely available, many vendors', relevance: 'Solar + battery is well-established with a long track record. Costs down 80%+ at utility scale since 2010 (LBNL/NREL). Viable in most US regions.', cautions: 'DIY has legal/safety requirements. Pro install costs more but cuts risk. LiFePO4 storage adds notable cost. Sizing is site-specific.', links: [{ label: 'NREL solar', href: 'https://www.nrel.gov/solar/' }] },
  ];

  let techOpen = techItems.map(() => false);
  function toggleTech(i) { techOpen[i] = !techOpen[i]; techOpen = [...techOpen]; }
</script>

<svelte:head>
  <title>What is AGI? | Surviving the Singularity</title>
  <meta name="description" content="What is AGI, what could it do for humanity, and why you need to lock in now. A clear-eyed breakdown. No hype, no doom, just signal." />
</svelte:head>

<div class="page">

  <!-- ─── BIG AGI COUNTDOWN (top of page) ─── -->
  <div class="countdown-wrap">
    <AGICountdown />
  </div>

  <!-- Hero -->
  <section class="hero">
    <div class="hero-bg">
      <div class="hero-grid"></div>
      <div class="hero-glow"></div>
    </div>
    {#if heroVisible}
      <div class="hero-content" in:fade={{ duration: 600, delay: 80 }}>
        <a href="/" class="back-link">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M9 2L4 7l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Surviving the Singularity
        </a>
        <div class="hero-eyebrow">
          <span class="eyebrow-dot"></span>
          <span>The Singularity Explained</span>
        </div>
        <h1 class="hero-title">
          The most important event in human history is <span class="hero-highlight">right around the corner.</span>
        </h1>
        <p class="hero-desc">
          Artificial General Intelligence, AI that can think across any domain at human level, is no longer science fiction. The researchers building it think it's close. Here's what it is, what it could change, and why the time to engage is now.
        </p>
        <div class="hero-nav">
          <a href="#what" class="hero-nav-link">What is AGI</a>
          <span class="hero-nav-sep">·</span>
          <a href="#humanity" class="hero-nav-link">What it could do</a>
          <span class="hero-nav-sep">·</span>
          <a href="#prepare" class="hero-nav-link">Why prepare now</a>
          <span class="hero-nav-sep">·</span>
          <a href="#scenario" class="hero-nav-link">Run a scenario</a>
          <span class="hero-nav-sep">·</span>
          <a href="#tech" class="hero-nav-link">Tech watch</a>
        </div>
      </div>
    {/if}
  </section>

  <p class="page-note">Do your own research. Not legal or financial advice. <a href="/disclaimer">Read our disclaimers and terms.</a></p>

  <!-- ─── SECTION 1: What is AGI ─── -->
  <section class="section" id="what" use:observe>
    <div class="section-inner">
      <div class="section-head">
        <span class="section-num">01</span>
        <div>
          <h2 class="section-title">What is AGI?</h2>
          <p class="section-desc">The spectrum from today's AI to what's coming next, and where the line gets crossed.</p>
        </div>
      </div>

      <!-- AI Level Cards -->
      <div class="levels-stack">
        {#each aiLevels as level}
          <div class="level-card" style="--level-color: {level.color}">
            <div class="level-header">
              <div class="level-label-group">
                <span class="level-name" style="color: {level.color}">{level.label}</span>
                <span class="level-status-chip status-{level.status}">{level.statusLabel}</span>
              </div>
            </div>
            <p class="level-desc">{level.description}</p>
            <div class="level-examples">
              {#each level.examples as ex}
                <span class="example-tag" style="border-color: {level.color}18; color: {level.color}; background: {level.color}0a">{ex}</span>
              {/each}
            </div>
          </div>
        {/each}
      </div>

      <!-- The key distinction -->
      <div class="callout-box">
        <div class="callout-icon">⚡</div>
        <div class="callout-body">
          <p class="callout-title">The critical difference</p>
          <p class="callout-text">Current AI systems, no matter how impressive, are fundamentally narrow. They do what they were trained for. AGI is qualitatively different: a system that can <strong>learn anything, reason across domains, and apply judgment the way a skilled human expert would</strong>, but without the physical, cognitive, or temporal limits that constrain humans. That difference is not incremental. It's civilizational.</p>
        </div>
      </div>

      <!-- Expert Forecasts -->
      <div class="forecasts-block">
        <h3 class="forecasts-title">What the builders are saying</h3>
        <p class="forecasts-note">The ranges below are <strong>our plain-language paraphrase</strong> of positions these researchers and executives have expressed publicly, not direct quotes, and not their exact words. People building AI systems tend to give shorter timelines than outside commentators. Timelines vary widely, and any individual's view may have shifted since.</p>
        <div class="forecasts-list">
          {#each timelineForecasts as forecast}
            <div class="forecast-row">
              <div class="forecast-bar" style="background: {forecast.color}18; border-left: 3px solid {forecast.color}50">
                <div class="forecast-source">{forecast.source}</div>
                <div class="forecast-year" style="color: {forecast.color}">{forecast.year}</div>
                <div class="forecast-conf">{forecast.confidence}</div>
              </div>
            </div>
          {/each}
        </div>
        <a href="/why" class="timeline-link-btn">
          <span class="tlb-pulse"></span>
          View the full timeline &amp; reasoning
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><path d="M3 6.5H10M10 6.5L7 3.5M10 6.5L7 9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
        <p class="page-note">Paraphrased from public statements — not direct quotes. <a href="/disclaimer">Read our disclaimers and terms.</a></p>
      </div>
    </div>
  </section>

  <!-- ─── SECTION 2: What it could do for humanity ─── -->
  <section class="section section-alt" id="humanity" use:observe>
    <div class="section-inner">
      <div class="section-head">
        <span class="section-num">02</span>
        <div>
          <h2 class="section-title">What AGI could do for humanity</h2>
          <p class="section-desc">The potential upside is genuinely staggering. Understanding it matters, because the disruption to get there is real too.</p>
        </div>
      </div>

      <div class="potential-grid">
        {#each humanityPotential as item}
          <div class="potential-card" use:observe>
            <div class="potential-icon" style="background: {item.color}12; border-color: {item.color}20">
              <span style="font-size:1.4rem">{item.icon}</span>
            </div>
            <div class="potential-body">
              <div class="potential-domain" style="color: {item.color}">{item.domain}</div>
              <h3 class="potential-headline">{item.headline}</h3>
              <p class="potential-text">{item.body}</p>
            </div>
          </div>
        {/each}
      </div>

      <div class="callout-box callout-caution">
        <div class="callout-icon">⚠</div>
        <div class="callout-body">
          <p class="callout-title">The distribution problem</p>
          <p class="callout-text">AGI's potential benefits are real, but they aren't automatic or evenly distributed. Every previous wave of transformative technology created enormous value while also concentrating power and displacing workers who couldn't adapt fast enough. <strong>The transition matters as much as the destination.</strong> That's the argument for engaging now rather than waiting to see what happens.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ─── SECTION 3: Why prepare now ─── -->
  <section class="section" id="prepare" use:observe>
    <div class="section-inner">
      <div class="section-head">
        <span class="section-num">03</span>
        <div>
          <h2 class="section-title">Why you need to lock in now</h2>
          <p class="section-desc">The preparation window is open. It won't stay open.</p>
        </div>
      </div>

      <!-- Urgency block -->
      <div class="urgency-strip">
        <div class="urgency-col">
          <span class="urgency-num">2–7</span>
          <span class="urgency-label">Rough span of years some AI-lab leaders have publicly floated for AGI</span>
        </div>
        <div class="urgency-divider"></div>
        <div class="urgency-col">
          <span class="urgency-num">$100B+</span>
          <span class="urgency-label">Scale of AI-infrastructure commitments announced by major players, per public reports</span>
        </div>
        <div class="urgency-divider"></div>
        <div class="urgency-col">
          <span class="urgency-num">Now</span>
          <span class="urgency-label">The time to build structural resilience, not after the inflection</span>
        </div>
      </div>
      <p class="page-note">Illustrative figures only. Do your own research. <a href="/disclaimer">Read our disclaimers and terms.</a></p>

      <!-- Why the timing matters -->
      <div class="timing-prose" use:observe>
        <p>Economic disruptions don't give advance warning. The internet didn't announce which industries it would hollow out. Smartphones didn't send a memo before destroying Blockbuster, Kodak, and the entire newspaper ad model.</p>
        <p>AGI will move faster than those transitions, because it's a general-purpose cognitive technology. It improves everything it touches simultaneously, not sector by sector.</p>
        <p><strong>The people positioned to benefit from that transition are the ones building resilience before it's obvious that they need to.</strong> That's not pessimism. It's the same logic that drives buying insurance, building savings, and learning marketable skills.</p>
      </div>

      <!-- 4 Actions -->
      <div class="actions-list">
        {#each prepActions as action, i}
          <div class="action-row" use:observe style="transition-delay: {i * 80}ms">
            <div class="action-num">{action.num}</div>
            <div class="action-body">
              <h3 class="action-title">{action.title}</h3>
              <p class="action-text">{action.body}</p>
              {#if action.cta}
                <a href={action.cta.href} class="action-cta">{action.cta.label}</a>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ─── SECTION 4: Scenario & cost explorer (from timeline) ─── -->
  <section class="section section-alt" id="scenario" use:observe>
    <div class="section-inner">
      <div class="section-head">
        <span class="section-num">04</span>
        <div>
          <h2 class="section-title">Run your own scenario</h2>
          <p class="section-desc">Adjust the chips to see how assumptions shift the illustrative arithmetic of building toward independence. Rough estimates only, real costs will differ, often by a lot.</p>
        </div>
      </div>

      <div class="scenario-grid">
        <div class="scenario-inputs">
          <div class="chip-section">
            <span class="chip-label">Monthly income (after tax)</span>
            <div class="chips">
              {#each incomeOptions as opt, i}
                <button class="chip" class:chip-on={selIncome === i} on:click={() => selIncome = i}>{opt.label}</button>
              {/each}
            </div>
          </div>
          <div class="chip-section">
            <span class="chip-label">Savings rate</span>
            <div class="chips">
              {#each savingsRateOptions as opt, i}
                <button class="chip" class:chip-on={selRate === i} on:click={() => selRate = i}>{opt.label}</button>
              {/each}
            </div>
          </div>
          <div class="chip-section">
            <span class="chip-label">Region (affects land)</span>
            <div class="chips chips-col">
              {#each regionOptions as opt, i}
                <button class="chip chip-wide" class:chip-on={selRegion === i} on:click={() => selRegion = i}>{opt.label}</button>
              {/each}
            </div>
          </div>
          <div class="chip-section">
            <span class="chip-label">Shouse size (affects build)</span>
            <div class="chips chips-col">
              {#each shouseSizeOptions as opt, i}
                <button class="chip chip-wide" class:chip-on={selSize === i} on:click={() => selSize = i}>{opt.label}</button>
              {/each}
            </div>
          </div>
        </div>

        <div class="scenario-results">
          <div class="result-headline">
            <span class="result-label">Illustrative all-in (rough estimate)</span>
            <span class="result-total">{fmt(totalCost)}</span>
            <span class="result-caveat">Real costs could be 2–5× higher or lower</span>
          </div>
          <div class="result-monthly">
            <div class="rm-row">
              <span class="rm-label">Saving per month</span>
              <span class="rm-val">{fmt(monthlySavings)}</span>
            </div>
            <div class="rm-row">
              <span class="rm-label">Rough time to total</span>
              <span class="rm-val rm-highlight">{fmtY(yearsToTotal)}</span>
            </div>
          </div>
          <div class="cost-breakdown">
            {#each costCategories as cat}
              <div class="cb-row">
                <span class="cb-icon">{cat.icon}</span>
                <span class="cb-label">{cat.label}</span>
                <div class="cb-bar-bg">
                  <div class="cb-bar" style="width: {Math.min(100, (costs[cat.key] / totalCost) * 100)}%"></div>
                </div>
                <span class="cb-val">{fmt(costs[cat.key])}</span>
              </div>
            {/each}
          </div>
        </div>
      </div>

      <!-- Compressed cost notes -->
      <details class="cost-notes">
        <summary>What these numbers can't tell you</summary>
        <div class="cost-notes-grid">
          {#each costCategories as cat}
            <div class="note-card">
              <span class="note-icon">{cat.icon}</span>
              <div>
                <p class="note-label">{cat.label}</p>
                <p class="note-text">{cat.note}</p>
              </div>
            </div>
          {/each}
        </div>
        <p class="cost-notes-omits"><strong>Not included:</strong> finished interior, HVAC/electrical/plumbing rough-in, septic ($5K–$30K+), driveway and site prep, property taxes, insurance, living expenses during build, the learning-curve cost, and whatever goes wrong (something will).</p>
      </details>
      <p class="page-note">All numbers illustrative. Do your own research. <a href="/disclaimer">Read our disclaimers and terms.</a></p>
    </div>
  </section>

  <!-- ─── SECTION 5: Technology watch list (from timeline) ─── -->
  <section class="section" id="tech" use:observe>
    <div class="section-head">
      <span class="section-num">05</span>
      <div>
        <h2 class="section-title">Technology watch list</h2>
        <p class="section-desc">Products and platforms worth tracking. Status and prices as of mid-2025; this space moves fast. Mentions are references, not endorsements. Verify everything independently.</p>
      </div>
    </div>

    <div class="tech-list">
      {#each techItems as item, i}
        <div class="tech-item" class:tech-open={techOpen[i]}>
          <button class="tech-trigger" on:click={() => toggleTech(i)} aria-expanded={techOpen[i]}>
            <div class="tech-trigger-left">
              <span class="tech-category" style="color:{item.color}; border-color:{item.color}25; background:{item.color}0d">{item.category}</span>
              <span class="tech-name">{item.name}</span>
              <span class="tech-status-chip"
                class:status-commercial={item.status.startsWith('Commercial')}
                class:status-research={item.status.startsWith('Research')}
                class:status-pre={item.status.startsWith('Pre')}
                class:status-active={item.status.startsWith('Active')}
                class:status-mature={item.status.startsWith('Mature')}>{item.status}</span>
            </div>
            <span class="tech-chevron" class:open={techOpen[i]} aria-hidden="true">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </span>
          </button>
          {#if techOpen[i]}
            <div class="tech-body" transition:slide={{ duration: 200 }}>
              <div class="tech-body-inner">
                <div class="tech-meta-grid">
                  <div class="tech-meta-item">
                    <span class="tmi-label">Price range</span>
                    <span class="tmi-val">{item.priceRange}</span>
                  </div>
                  <div class="tech-meta-item">
                    <span class="tmi-label">Availability</span>
                    <span class="tmi-val">{item.availability}</span>
                  </div>
                </div>
                <div>
                  <p class="tech-section-label">Why it might matter</p>
                  <p class="tech-text">{item.relevance}</p>
                </div>
                <div class="tech-cautions">
                  <p class="tech-section-label">Cautions</p>
                  <p class="tech-text">{item.cautions}</p>
                </div>
                {#if item.links.length > 0}
                  <div class="tech-links">
                    {#each item.links as link}
                      <a href={link.href} target="_blank" rel="noopener noreferrer" class="tech-link">{link.label} →</a>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
          {/if}
        </div>
      {/each}
    </div>

    <div class="tech-footer-note">
      <p>This list goes stale quickly. The robotics and AI landscape changes faster than any static page can track. Verify current status independently before drawing conclusions. Listing here implies nothing about quality, viability, or fit for your situation.</p>
    </div>
  </section>

  <!-- ─── CTA ─── -->
  <section class="cta-section" use:observe>
    <div class="cta-inner">
      <p class="cta-eyebrow">Start here</p>
      <h2 class="cta-title">Ready to act on this?</h2>
      <p class="cta-desc">The Blueprint lays out a concrete strategy for material independence before the transition. The book gives you the full mental model. Both are available now, no paywall.</p>
      <div class="cta-buttons">
        <a href="/blueprint" class="cta-btn cta-btn-primary">Read the Blueprint</a>
        <a href="/book" class="cta-btn cta-btn-secondary">Read the Book</a>
        <a href="#scenario" class="cta-btn cta-btn-ghost">Run a Scenario →</a>
      </div>
    </div>
  </section>

  <p class="page-note">Do your own research. Not legal or financial advice. <a href="/disclaimer">Read our disclaimers and terms.</a></p>

  <p class="page-evidence-link">Want the primary sources? <a href="/evidence">The Evidence page has the footage and papers behind every claim on this site.</a></p>

</div>

<style>
  .page {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 1.5rem 6rem;
  }

  .countdown-wrap {
    margin: 1.5rem 0 0.5rem;
  }

  /* Hero */
  .hero {
    position: relative;
    padding: 4rem 0 3rem;
    overflow: hidden;
  }

  .hero-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
  }

  .hero-grid {
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(245,158,11,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(245,158,11,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 0%, black 30%, transparent 100%);
  }

  .hero-glow {
    position: absolute;
    top: -20%;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 400px;
    background: radial-gradient(ellipse, rgba(245,158,11,0.07) 0%, transparent 70%);
    pointer-events: none;
  }

  .hero-content {
    position: relative;
    z-index: 1;
  }

  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.86rem;
    color: #dde4ef;
    text-decoration: none;
    margin-bottom: 1.75rem;
    transition: color 0.15s;
    font-family: var(--font-primary);
  }
  .back-link:hover { color: #dde4ef; }

  .hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #f59e0b;
    font-family: var(--font-primary);
    margin-bottom: 1.25rem;
  }

  .eyebrow-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #f59e0b;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
  }

  .hero-title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    color: #f8fafc;
    letter-spacing: -0.04em;
    line-height: 1.08;
    margin: 0 0 1.25rem;
    /* Let the browser balance line lengths instead of hardcoded <br>,
       so no single word is orphaned on its own line. */
    text-wrap: balance;
  }

  .hero-highlight {
    color: #f59e0b;
    position: relative;
  }

  .hero-desc {
    font-size: clamp(0.95rem, 2vw, 1.1rem);
    color: #dde4ef;
    line-height: 1.75;
    max-width: 640px;
    margin: 0 0 2rem;
  }

  .hero-nav {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .hero-nav-link {
    font-size: 0.82rem;
    font-weight: 600;
    color: #dde4ef;
    text-decoration: none;
    transition: color 0.15s;
    font-family: var(--font-primary);
  }
  .hero-nav-link:hover { color: #f59e0b; }

  .hero-nav-sep {
    color: #334155;
    font-size: 0.85rem;
  }

  /* Sections */
  .section {
    padding: 4rem 0;
    border-top: 1px solid rgba(255,255,255,0.04);
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  .section.revealed {
    opacity: 1;
    transform: none;
  }

  .section-alt {
    background: rgba(15,23,42,0.4);
    margin: 0 -1.5rem;
    padding: 4rem 1.5rem;
  }

  .section-inner { max-width: 100%; }

  .section-head {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 2.5rem;
  }

  .section-num {
    font-size: 0.82rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: var(--font-primary);
    opacity: 0.5;
    padding-top: 0.25rem;
    min-width: 26px;
  }

  .section-title {
    font-size: clamp(1.5rem, 3.5vw, 2.2rem);
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.03em;
    margin: 0 0 0.4rem;
  }

  .section-desc {
    font-size: 0.9rem;
    color: #dde4ef;
    line-height: 1.65;
    margin: 0;
    max-width: 560px;
  }

  /* AI Level Cards */
  .levels-stack {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 2rem;
  }

  .level-card {
    padding: 1.5rem;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid var(--level-color);
    border-radius: 12px;
    transition: border-color 0.2s;
  }
  .level-card:hover { border-color: rgba(255,255,255,0.1); }

  .level-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
  }

  .level-label-group {
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .level-name {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
  }

  .level-status-chip {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.18rem 0.5rem;
    border-radius: 4px;
    font-family: var(--font-primary);
  }

  .status-now {
    background: rgba(59,130,246,0.1);
    color: #3b82f6;
    border: 1px solid rgba(59,130,246,0.25);
  }
  .status-coming {
    background: rgba(245,158,11,0.1);
    color: #f59e0b;
    border: 1px solid rgba(245,158,11,0.25);
    animation: chip-pulse 2.5s ease-in-out infinite;
  }
  .status-after {
    background: rgba(245, 158, 11,0.08);
    color: #fb923c;
    border: 1px solid rgba(245, 158, 11,0.2);
  }

  @keyframes chip-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.65; }
  }

  .level-desc {
    font-size: 0.88rem;
    color: #dde4ef;
    line-height: 1.7;
    margin: 0 0 0.9rem;
  }

  .level-examples {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .example-tag {
    font-size: 0.76rem;
    font-weight: 600;
    padding: 0.18rem 0.55rem;
    border-radius: 5px;
    border: 1px solid;
    font-family: var(--font-primary);
  }

  /* Callout */
  .callout-box {
    display: flex;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    background: rgba(245,158,11,0.04);
    border: 1px solid rgba(245,158,11,0.12);
    border-radius: 12px;
    margin-bottom: 2.5rem;
  }

  .callout-caution {
    background: rgba(245, 158, 11,0.04);
    border-color: rgba(245, 158, 11,0.12);
  }

  .callout-icon {
    font-size: 1.2rem;
    flex-shrink: 0;
    padding-top: 0.1rem;
    line-height: 1;
  }

  .callout-title {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #f59e0b;
    margin: 0 0 0.4rem;
    font-family: var(--font-primary);
  }

  .callout-caution .callout-title { color: #fb923c; }

  .callout-text {
    font-size: 0.88rem;
    color: #dde4ef;
    line-height: 1.7;
    margin: 0;
  }

  .callout-text strong { color: #e2e8f0; }

  /* Forecasts */
  .forecasts-block { margin-top: 2rem; }

  .forecasts-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.02em;
    margin: 0 0 0.4rem;
  }

  .forecasts-note {
    font-size: 0.85rem;
    color: #dde4ef;
    line-height: 1.65;
    margin: 0 0 1.25rem;
    max-width: 580px;
  }

  .forecasts-note strong { color: #e2e8f0; }

  .forecasts-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .timeline-link-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.25rem 0 1rem;
    padding: 0.6rem 1.1rem;
    border-radius: 8px;
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: #f59e0b;
    font-size: 0.84rem;
    font-weight: 700;
    font-family: var(--font-primary);
    letter-spacing: 0.02em;
    text-decoration: none;
    transition: background 0.15s, border-color 0.15s, transform 0.15s;
  }
  .timeline-link-btn:hover {
    background: rgba(245, 158, 11, 0.14);
    border-color: rgba(245, 158, 11, 0.45);
    transform: translateY(-1px);
  }
  .timeline-link-btn svg { transition: transform 0.15s; }
  .timeline-link-btn:hover svg { transform: translateX(2px); }

  .tlb-pulse {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #f59e0b;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
    animation: pulse 1.5s ease-in-out infinite;
    flex-shrink: 0;
  }

  @keyframes pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
  }

  .forecast-bar {
    display: grid;
    grid-template-columns: 1fr auto 2fr;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
  }

  .forecast-source {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e9eef5;
  }

  .forecast-year {
    font-size: 0.86rem;
    font-weight: 800;
    font-family: var(--font-primary);
    white-space: nowrap;
  }

  .forecast-conf {
    font-size: 0.85rem;
    color: #dde4ef;
    line-height: 1.4;
  }

  .forecasts-caveat {
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.6;
    font-style: italic;
    margin: 0;
  }

  /* Potential grid */
  .potential-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .potential-card {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
    padding: 1.25rem;
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }

  .potential-card.revealed {
    opacity: 1;
    transform: none;
  }

  .potential-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    border: 1px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .potential-domain {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: var(--font-primary);
    margin-bottom: 0.2rem;
  }

  .potential-headline {
    font-size: 0.95rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.02em;
    margin: 0 0 0.4rem;
    line-height: 1.35;
  }

  .potential-text {
    font-size: 0.82rem;
    color: #dde4ef;
    line-height: 1.7;
    margin: 0;
  }

  /* Urgency strip */
  .urgency-strip {
    display: flex;
    gap: 0;
    background: rgba(245,158,11,0.04);
    border: 1px solid rgba(245,158,11,0.12);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2.5rem;
  }

  .urgency-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1.5rem 1rem;
    gap: 0.4rem;
  }

  .urgency-divider {
    width: 1px;
    background: rgba(245,158,11,0.1);
    margin: 1rem 0;
  }

  .urgency-num {
    font-size: clamp(1.5rem, 3vw, 2.2rem);
    font-weight: 900;
    color: #f59e0b;
    font-family: var(--font-primary);
    letter-spacing: -0.03em;
    line-height: 1;
  }

  .urgency-label {
    font-size: 0.82rem;
    color: #dde4ef;
    line-height: 1.4;
    max-width: 140px;
  }

  /* Timing prose */
  .timing-prose {
    max-width: 680px;
    margin-bottom: 2.5rem;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  .timing-prose.revealed { opacity: 1; transform: none; }

  .timing-prose p {
    font-size: 0.95rem;
    color: #dde4ef;
    line-height: 1.8;
    margin: 0 0 1rem;
  }

  .timing-prose p:last-child { margin-bottom: 0; }
  .timing-prose strong { color: #e2e8f0; }

  /* Actions */
  .actions-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .action-row {
    display: flex;
    gap: 1.25rem;
    padding: 1.5rem;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }

  .action-row.revealed {
    opacity: 1;
    transform: none;
  }

  .action-num {
    font-size: 0.8rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: var(--font-primary);
    opacity: 0.6;
    padding-top: 0.2rem;
    min-width: 26px;
  }

  .action-title {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem;
  }

  .action-text {
    font-size: 0.85rem;
    color: #dde4ef;
    line-height: 1.7;
    margin: 0 0 0.75rem;
  }

  .action-cta {
    font-size: 0.8rem;
    font-weight: 700;
    color: #f59e0b;
    text-decoration: none;
    font-family: var(--font-primary);
    letter-spacing: 0.02em;
    transition: opacity 0.15s;
  }
  .action-cta:hover { opacity: 0.75; }

  /* CTA Section */
  .cta-section {
    margin: 2rem -1.5rem 0;
    padding: 4rem 1.5rem;
    background: linear-gradient(135deg, rgba(245,158,11,0.06) 0%, rgba(15,23,42,0.8) 60%);
    border-top: 1px solid rgba(245,158,11,0.12);
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.6s ease, transform 0.6s ease;
    text-align: center;
  }

  .cta-section.revealed {
    opacity: 1;
    transform: none;
  }

  .cta-inner {
    max-width: 600px;
    margin: 0 auto;
  }

  .cta-eyebrow {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #f59e0b;
    font-family: var(--font-primary);
    margin: 0 0 0.75rem;
  }

  .cta-title {
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 900;
    color: #f8fafc;
    letter-spacing: -0.04em;
    margin: 0 0 0.75rem;
  }

  .cta-desc {
    font-size: 0.9rem;
    color: #dde4ef;
    line-height: 1.7;
    margin: 0 0 2rem;
  }

  .cta-buttons {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .cta-btn {
    display: inline-flex;
    align-items: center;
    padding: 0.65rem 1.4rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 700;
    text-decoration: none;
    transition: all 0.15s ease;
    font-family: var(--font-primary);
    letter-spacing: 0.02em;
    white-space: nowrap;
  }

  .cta-btn-primary {
    background: #f59e0b;
    color: #0f172a;
  }
  .cta-btn-primary:hover { background: #fbbf24; transform: translateY(-1px); }

  .cta-btn-secondary {
    background: rgba(59,130,246,0.1);
    color: #60a5fa;
    border: 1px solid rgba(59,130,246,0.2);
  }
  .cta-btn-secondary:hover { background: rgba(59,130,246,0.15); }

  .cta-btn-ghost {
    color: #dde4ef;
    border: 1px solid rgba(255,255,255,0.06);
  }
  .cta-btn-ghost:hover { color: #dde4ef; border-color: rgba(255,255,255,0.1); }

  /* Disclaimers */
  .page-disclaimer {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    padding: 0.9rem 1.1rem;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 10px;
    margin-top: 1rem;
  }

  .page-disclaimer svg { flex-shrink: 0; margin-top: 0.15rem; }

  .page-disclaimer p {
    font-size: 0.86rem;
    color: #dde4ef;
    line-height: 1.65;
    margin: 0;
  }
  .page-disclaimer strong { color: #e9eef5; }
  .page-disclaimer a,
  .urgency-caveat a {
    color: #dde4ef;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .page-disclaimer a:hover,
  .urgency-caveat a:hover { color: #f59e0b; }

  .urgency-caveat {
    font-size: 0.8rem;
    color: #475569;
    line-height: 1.6;
    font-style: italic;
    margin: -1.75rem 0 2.5rem;
  }

  .bottom-disclaimer {
    margin: 0 -1.5rem;
    padding: 2rem 1.5rem 0;
  }

  .bottom-disclaimer p {
    max-width: 680px;
    margin: 0 auto;
    font-size: 0.86rem;
    color: #dde4ef;
    line-height: 1.7;
    text-align: center;
  }
  .bottom-disclaimer strong { color: #dde4ef; }
  .bottom-disclaimer a {
    color: #dde4ef;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .bottom-disclaimer a:hover { color: #f59e0b; }

  .forecasts-caveat a {
    color: #475569;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .forecasts-caveat a:hover { color: #dde4ef; }

  /* ─── Scenario explorer ─── */
  .scenario-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.75rem;
    align-items: start;
  }

  .scenario-inputs {
    display: flex;
    flex-direction: column;
    gap: 1.1rem;
    position: sticky;
    top: 1.5rem;
  }

  .chip-section { display: flex; flex-direction: column; gap: 0.5rem; }

  .chip-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #dde4ef;
    font-family: var(--font-primary);
  }

  .chips { display: flex; flex-wrap: wrap; gap: 0.35rem; }
  .chips-col { flex-direction: column; align-items: stretch; }

  .chip {
    padding: 0.4rem 0.7rem;
    border-radius: 6px;
    font-size: 0.84rem;
    font-weight: 600;
    font-family: var(--font-primary);
    border: 1px solid rgba(148, 163, 184, 0.1);
    background: rgba(30, 41, 59, 0.5);
    color: #dde4ef;
    cursor: pointer;
    transition: all 0.15s ease;
    line-height: 1.1;
    min-height: 38px;
  }
  .chip-wide { width: 100%; text-align: left; }
  .chip:hover { border-color: rgba(245, 158, 11, 0.3); }
  .chip-on {
    background: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.4);
    color: #f59e0b;
  }

  .scenario-results { display: flex; flex-direction: column; gap: 1.25rem; }

  .result-headline {
    padding: 1.25rem;
    background: rgba(245, 158, 11, 0.05);
    border: 1px solid rgba(245, 158, 11, 0.12);
    border-radius: 12px;
    text-align: center;
  }

  .result-label {
    display: block;
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #dde4ef;
    font-weight: 600;
    margin-bottom: 0.4rem;
  }

  .result-total {
    display: block;
    font-size: clamp(1.8rem, 6vw, 2.2rem);
    font-weight: 900;
    color: #f59e0b;
    font-family: var(--font-primary);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.3rem;
  }

  .result-caveat { display: block; font-size: 0.84rem; color: #dde4ef; font-style: italic; }

  .result-monthly { display: flex; flex-direction: column; gap: 0.5rem; }

  .rm-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    gap: 1rem;
  }
  .rm-label { font-size: 0.84rem; color: #dde4ef; }
  .rm-val {
    font-size: 0.9rem;
    font-weight: 700;
    color: #e2e8f0;
    font-family: var(--font-primary);
    white-space: nowrap;
  }
  .rm-highlight { color: #f59e0b; font-size: 1.1rem; }

  .cost-breakdown {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 10px;
    padding: 1rem;
  }

  .cb-row {
    display: grid;
    grid-template-columns: 1.2rem 1fr auto auto;
    align-items: center;
    gap: 0.6rem;
  }
  .cb-icon { font-size: 0.85rem; }
  .cb-label { font-size: 0.84rem; color: #dde4ef; }
  .cb-bar-bg { height: 4px; background: rgba(255,255,255,0.04); border-radius: 2px; overflow: hidden; }
  .cb-bar {
    height: 100%;
    border-radius: 2px;
    background: rgba(245,158,11,0.22);
    border-right: 2px solid rgba(245,158,11,0.55);
    transition: width 0.4s ease;
  }
  .cb-val {
    font-size: 0.8rem;
    font-weight: 700;
    color: #e9eef5;
    font-family: var(--font-primary);
    white-space: nowrap;
    text-align: right;
    min-width: 52px;
  }

  /* Cost notes (collapsible) */
  .cost-notes {
    margin-top: 1.5rem;
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.4);
    overflow: hidden;
  }

  .cost-notes summary {
    cursor: pointer;
    padding: 0.9rem 1.25rem;
    font-size: 0.84rem;
    font-weight: 700;
    color: #e2e8f0;
    font-family: var(--font-primary);
    letter-spacing: 0.02em;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .cost-notes summary::-webkit-details-marker { display: none; }
  .cost-notes summary::before {
    content: '+';
    color: #f59e0b;
    font-weight: 900;
    font-size: 1rem;
  }
  .cost-notes[open] summary::before { content: '–'; }

  .cost-notes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 0.6rem;
    padding: 0 1.25rem 0.5rem;
  }

  .note-card {
    display: flex;
    gap: 0.65rem;
    padding: 0.85rem;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 10px;
  }
  .note-icon { font-size: 1rem; flex-shrink: 0; line-height: 1.4; }
  .note-label { font-size: 0.84rem; font-weight: 700; color: #e9eef5; margin: 0 0 0.25rem; }
  .note-text { font-size: 0.82rem; color: #dde4ef; line-height: 1.55; margin: 0; }

  .cost-notes-omits {
    padding: 0.75rem 1.25rem 1.25rem;
    font-size: 0.84rem;
    color: #dde4ef;
    line-height: 1.65;
    margin: 0;
  }
  .cost-notes-omits strong { color: #e9eef5; }

  /* ─── Tech watch list ─── */
  .tech-list { display: flex; flex-direction: column; gap: 0.5rem; }

  .tech-item {
    border: 1px solid rgba(148, 163, 184, 0.07);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.4);
    transition: border-color 0.2s;
  }
  .tech-item:hover { border-color: rgba(148, 163, 184, 0.13); }
  .tech-open { border-color: rgba(148, 163, 184, 0.18); background: rgba(30, 41, 59, 0.5); }

  .tech-trigger {
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
    font-family: inherit;
    padding: 0.9rem 1.1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    text-align: left;
  }
  .tech-trigger:focus-visible { outline: 2px solid #f59e0b; outline-offset: -2px; border-radius: 11px; }

  .tech-trigger-left {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    min-width: 0;
  }

  .tech-category {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    border: 1px solid;
    font-family: var(--font-primary);
    white-space: nowrap;
  }
  .tech-name { font-size: 0.9rem; font-weight: 700; color: #e2e8f0; }

  .tech-status-chip {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-family: var(--font-primary);
    white-space: nowrap;
  }
  .status-commercial { background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.2); }
  .status-research { background: rgba(139,92,246,0.1); color: #8b5cf6; border: 1px solid rgba(139,92,246,0.2); }
  .status-pre { background: rgba(245,158,11,0.08); color: #f59e0b; border: 1px solid rgba(245,158,11,0.2); }
  .status-active { background: rgba(59,130,246,0.08); color: #60a5fa; border: 1px solid rgba(59,130,246,0.2); }
  .status-mature { background: rgba(100,116,139,0.1); color: #dde4ef; border: 1px solid rgba(100,116,139,0.2); }

  .tech-chevron { flex-shrink: 0; color: #dde4ef; transition: transform 0.22s ease; display: flex; }
  .tech-chevron.open { transform: rotate(180deg); }

  .tech-body { border-top: 1px solid rgba(148, 163, 184, 0.06); }
  .tech-body-inner {
    padding: 1rem 1.1rem;
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }

  .tech-meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; }
  .tech-meta-item { background: rgba(30, 41, 59, 0.4); border-radius: 8px; padding: 0.6rem 0.8rem; }

  .tmi-label {
    display: block;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #dde4ef;
    font-weight: 700;
    margin-bottom: 0.2rem;
    font-family: var(--font-primary);
  }
  .tmi-val { display: block; font-size: 0.8rem; color: #dde4ef; line-height: 1.4; }

  .tech-section-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #dde4ef;
    margin: 0 0 0.3rem;
    font-family: var(--font-primary);
  }
  .tech-cautions .tech-section-label { color: #fbbf24; }
  .tech-cautions .tech-text { color: #fcd34d; }
  .tech-text { font-size: 0.84rem; color: #dde4ef; line-height: 1.65; margin: 0; }

  .tech-links { display: flex; flex-wrap: wrap; gap: 0.75rem; }
  .tech-link {
    font-size: 0.84rem;
    color: #dde4ef;
    text-decoration: underline;
    text-underline-offset: 2px;
    transition: color 0.15s;
  }
  .tech-link:hover { color: #f59e0b; }

  .tech-footer-note {
    margin-top: 1.25rem;
    padding: 1rem 1.25rem;
    background: rgba(30, 41, 59, 0.3);
    border-radius: 8px;
    border: 1px solid rgba(148, 163, 184, 0.06);
  }
  .tech-footer-note p {
    font-size: 0.84rem;
    color: #dde4ef;
    line-height: 1.6;
    margin: 0;
    font-style: italic;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .scenario-grid { grid-template-columns: 1fr; gap: 1.25rem; }
    .scenario-inputs { position: static; }
    .tech-meta-grid { grid-template-columns: 1fr; }
    .tech-trigger-left { gap: 0.4rem; }
  }

  @media (max-width: 640px) {
    .forecast-bar {
      grid-template-columns: 1fr auto;
      grid-template-rows: auto auto;
    }
    .forecast-conf { grid-column: 1 / -1; }
    .urgency-strip { flex-direction: column; }
    .urgency-divider { width: 100%; height: 1px; margin: 0; }
    .potential-grid { grid-template-columns: 1fr; }

    /* Pull the value prop above the fold: kill the dead gap below the
       countdown card and tighten the hero intro. */
    .countdown-wrap { margin: 0.75rem 0 0.25rem; }
    .hero { padding: 1.25rem 0 1.5rem; }
    .back-link { margin-bottom: 0.9rem; }
    .hero-eyebrow { margin-bottom: 0.85rem; letter-spacing: 0.08em; }
    .hero-title { margin-bottom: 0.85rem; }
    .hero-desc { margin-bottom: 1rem; }

    /* Timeline content tightened for phones */
    .cost-notes-grid { grid-template-columns: 1fr; }
    .chips { gap: 0.4rem; }
    .chip { flex: 1 1 auto; min-width: calc(33.333% - 0.4rem); text-align: center; }
    .chip-wide { flex-basis: 100%; text-align: left; }
    .tech-trigger { padding: 0.85rem 0.9rem; }
    .tech-body-inner { padding: 0.9rem; }
  }
</style>
