<script>
  import { slide } from 'svelte/transition';

  // ── DISCLAIMER ──────────────────────────────────────────────────────────────
  // Everything on this page is conjecture and supposition based on one author's
  // research and publicly available information as of mid-2025. Prices, product
  // availability, timelines, and technology capabilities all change rapidly and
  // unpredictably. Nothing here is financial, legal, construction, or professional
  // advice of any kind. No outcome is guaranteed or projected. Treat all numbers
  // as illustrative placeholders only, not as forecasts or recommendations.
  // ────────────────────────────────────────────────────────────────────────────

  // --- Scenario builder ---
  const incomeOptions = [
    { label: '$2K', value: 2000 },
    { label: '$3.5K', value: 3500 },
    { label: '$5K', value: 5000 },
    { label: '$8K', value: 8000 },
    { label: '$12K', value: 12000 },
    { label: '$20K+', value: 20000 },
  ];

  const savingsRateOptions = [
    { label: '5%', pct: 0.05 },
    { label: '10%', pct: 0.10 },
    { label: '15%', pct: 0.15 },
    { label: '20%', pct: 0.20 },
    { label: '30%', pct: 0.30 },
    { label: '40%', pct: 0.40 },
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

  let selIncome = 2;
  let selRate = 2;
  let selRegion = 0;
  let selSize = 1;

  // Base cost estimates (illustrative only, varies wildly in reality)
  const BASE_LAND = 18000;     // ~5 acres rural
  const BASE_SHOUSE = 60000;   // steel kit + rough finish
  const BASE_SOLAR = 12000;    // 6kW off-grid system
  const BASE_WATER = 6000;     // well + storage
  const BASE_FARMBOT = 4500;   // FarmBot Genesis v1.7 kit (est. 2025 MSRP)
  const BASE_LOCAL_AI = 3500;  // GPU workstation for local models
  const BASE_MISC = 8000;      // permits, tools, contingency

  $: monthlyIncome = incomeOptions[selIncome].value;
  $: savingsRate = savingsRateOptions[selRate].pct;
  $: monthlySavings = Math.round(monthlyIncome * savingsRate);
  $: landMult = regionOptions[selRegion].landMultiplier;
  $: buildMult = shouseSizeOptions[selSize].buildMultiplier;

  $: costs = {
    land: Math.round(BASE_LAND * landMult),
    shouse: Math.round(BASE_SHOUSE * buildMult),
    solar: BASE_SOLAR,
    water: BASE_WATER,
    farmbot: BASE_FARMBOT,
    localAI: BASE_LOCAL_AI,
    misc: BASE_MISC,
  };

  $: totalCost = Object.values(costs).reduce((a, b) => a + b, 0);
  $: monthsToTotal = monthlySavings > 0 ? Math.ceil(totalCost / monthlySavings) : Infinity;
  $: yearsToTotal = monthsToTotal / 12;

  function fmt(n) {
    if (!isFinite(n)) return 'n/a';
    return '$' + n.toLocaleString();
  }
  function fmtY(y) {
    if (!isFinite(y)) return 'n/a';
    if (y < 1) return Math.round(y * 12) + ' months';
    return y.toFixed(1) + ' years';
  }

  // --- Technology watch list ---
  const techItems = [
    {
      name: 'Unitree H1 / G1',
      category: 'Robotics · General Purpose',
      color: '#f59e0b',
      status: 'Commercial (limited)',
      priceRange: '$16K–$90K (estimated, varies)',
      availability: 'Available in select markets, 2024–2025',
      relevance: 'One of the first sub-$100K humanoid robots reaching commercial availability. Research-grade; not a consumer product. Requires technical integration skill.',
      cautions: 'High cost, limited software ecosystem, physically delicate, no "plug and play" capability, rapid version churn. Not a farm labor replacement today.',
      links: [{ label: 'Unitree Robotics', href: 'https://www.unitree.com/' }],
      open: false,
    },
    {
      name: 'Figure AI (Figure 02)',
      category: 'Robotics · General Purpose',
      color: '#f59e0b',
      status: 'Pre-commercial / pilot partners',
      priceRange: 'Not publicly disclosed; BMW partnership announced 2024',
      availability: 'Industrial pilots only as of 2025',
      relevance: 'Well-funded humanoid robot company. OpenAI partnership announced 2024. Target is general-purpose manipulation. May matter for small-holder land work in 5–10 year horizon.',
      cautions: 'Not consumer-available. Funding does not equal product readiness. Timeline to affordable general-purpose use is speculative.',
      links: [{ label: 'Figure AI', href: 'https://www.figure.ai/' }],
      open: false,
    },
    {
      name: 'Agility Robotics (Digit)',
      category: 'Robotics · Logistics Focus',
      color: '#f59e0b',
      status: 'Commercial (logistics/warehouse)',
      priceRange: 'Not publicly disclosed; Amazon partnership',
      availability: 'Warehouse deployment, 2024–2025',
      relevance: 'Amazon-backed humanoid optimized for pick-and-place logistics. Not designed for outdoor/agricultural use but demonstrates commercial viability of general manipulation.',
      cautions: 'Designed for structured indoor environments. Outdoor unstructured use (farming, construction) is a harder problem.',
      links: [{ label: 'Agility Robotics', href: 'https://agilityrobotics.com/' }],
      open: false,
    },
    {
      name: 'Asimov (stealth)',
      category: 'Robotics · General Purpose',
      color: '#f59e0b',
      status: 'Stealth / unconfirmed',
      priceRange: 'Unknown',
      availability: 'No public product as of mid-2025',
      relevance: 'Referenced in AI/robotics circles. As of this writing, no confirmed product exists publicly. Worth watching.',
      cautions: 'Treat with extreme skepticism until public product release. Stealth-stage companies often pivot, fold, or ship something very different from early positioning.',
      links: [],
      open: false,
    },
    {
      name: 'FarmBot Genesis / Express',
      category: 'Robotics · Agricultural CNC',
      color: '#10b981',
      status: 'Commercial (consumer)',
      priceRange: 'Genesis: ~$4,495 | Express: ~$2,995 (2025 est.)',
      availability: 'Ships globally. Open-source hardware + software.',
      relevance: 'CNC food growing robot that automates seeding, watering, and weeding for raised-bed gardens up to ~18 sq ft (Genesis). Open-source, hackable, active community. Represents the realistic near-term option for automated food growing.',
      cautions: 'Covers a small garden bed, not a farm. Requires power, water, Wi-Fi. Not a food-security solution alone. Expansion to larger plots requires multiple units or DIY derivatives.',
      links: [
        { label: 'FarmBot.io', href: 'https://farm.bot/' },
        { label: 'GitHub', href: 'https://github.com/FarmBot' },
      ],
      open: false,
    },
    {
      name: 'Open-weights LLMs (Llama, Mistral, etc.)',
      category: 'Local AI · Language Models',
      color: '#8b5cf6',
      status: 'Active / rapid development',
      priceRange: 'Free (models). Hardware: $800–$5K+ for useful local inference',
      availability: 'Now: Llama 3.x, Mistral, Phi-4, Qwen, Gemma and many others',
      relevance: 'Running capable language models locally on consumer hardware is possible today. Useful for: writing assistance, code generation, research synthesis, private question answering without cloud dependency.',
      cautions: 'Capability changes monthly. A specific model recommendation will be outdated quickly. Local inference requires significant RAM (16GB+ for useful models). Not equivalent to frontier cloud models for complex tasks.',
      links: [
        { label: 'Ollama (local runner)', href: 'https://ollama.com/' },
        { label: 'LM Studio', href: 'https://lmstudio.ai/' },
      ],
      open: false,
    },
    {
      name: 'RTX 5090 / 5080 (or AMD equiv.)',
      category: 'Local AI · Hardware',
      color: '#8b5cf6',
      status: 'Available (NVIDIA) / competitive landscape active',
      priceRange: '$1,000–$2,500+ depending on model and availability',
      availability: 'RTX 5090 announced CES 2025; availability varies',
      relevance: 'Consumer GPUs that can run 70B+ parameter models locally. Representing a meaningful capability jump over previous generation for local AI inference.',
      cautions: 'Stock availability variable. Prices fluctuate. AMD, Intel, and other vendors are competitive alternatives worth evaluating. A GPU bought today may be outperformed by software/model improvements within 12 months.',
      links: [
        { label: 'NVIDIA RTX 50 series', href: 'https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/' },
      ],
      open: false,
    },
    {
      name: 'Mobile Aloha (Stanford research)',
      category: 'Robotics · Research Platform',
      color: '#f59e0b',
      status: 'Research only',
      priceRange: '~$32K (research build cost, 2024)',
      availability: 'Open-source plans. Not a commercial product.',
      relevance: 'Demonstrated bimanual manipulation tasks in home environments (cooking, laundry). Imitation learning approach. Represents the research frontier of affordable dexterous robots.',
      cautions: 'Research project, not a product. Requires significant robotics expertise to replicate. Cost estimate from 2024 paper; actual build cost varies. Not ready for general use.',
      links: [
        { label: 'Mobile Aloha paper', href: 'https://mobile-aloha.github.io/' },
      ],
      open: false,
    },
    {
      name: 'Off-grid solar systems',
      category: 'Energy Independence',
      color: '#fbbf24',
      status: 'Mature commercial technology',
      priceRange: '$8K–$25K installed for a basic home system (varies enormously)',
      availability: 'Widely available. Many vendors.',
      relevance: 'Solar + battery storage is a well-established technology with a long track record. Costs have dropped dramatically since 2010 (80%+ utility-scale, per LBNL/NREL data). Viable for most regions in the US.',
      cautions: 'DIY installation has legal/safety requirements. Professional installation adds cost but reduces risk. Battery storage (LiFePO4 preferred) adds significantly to total cost. Sizing is site- and use-case-specific.',
      links: [
        { label: 'NREL solar resources', href: 'https://www.nrel.gov/solar/' },
        { label: 'EnergySage', href: 'https://news.energysage.com/' },
      ],
      open: false,
    },
  ];

  let techOpen = techItems.map(() => false);

  function toggleTech(i) {
    techOpen[i] = !techOpen[i];
    techOpen = [...techOpen];
  }

  // --- Cost breakdown categories ---
  const costCategories = [
    { key: 'land', label: 'Land', icon: '🌾', note: 'Varies wildly by region, parcel, and market conditions. Rural farmland median ~$3.6K/acre nationally (USDA 2023) but ranges from hundreds to hundreds of thousands per acre depending on location.' },
    { key: 'shouse', label: 'Shop/House (Shouse)', icon: '🏗️', note: 'Steel building kit + rough interior finish. Does not include permits, foundation, HVAC, electrical, plumbing, or finished interiors. All of those add cost that varies by county and contractor.' },
    { key: 'solar', label: 'Solar + Battery', icon: '☀️', note: 'Rough estimate for 6kW system with storage. Real cost depends on system size, local incentives, installer, and site conditions. Federal ITC (30% as of 2025) may apply; consult a tax professional.' },
    { key: 'water', label: 'Water (Well + Storage)', icon: '💧', note: 'Well drilling cost varies enormously by depth, geology, and location, roughly $15–$50+ per foot. Rainwater collection may be an option depending on local law. Consult local professionals.' },
    { key: 'farmbot', label: 'FarmBot (food automation)', icon: '🤖', note: 'FarmBot Genesis retail kit estimate. One unit covers a small raised bed. Real food production requires more land, more labor, and a longer learning curve than any machine can substitute.' },
    { key: 'localAI', label: 'Local AI Workstation', icon: '💻', note: 'GPU workstation capable of running 70B+ parameter models locally. Hardware capability changes rapidly; consult current benchmarks before purchasing.' },
    { key: 'misc', label: 'Permits, Tools, Contingency', icon: '🔧', note: 'Building permits, basic tool set, and a contingency buffer. Permit costs alone can range from hundreds to tens of thousands depending on jurisdiction. Always budget a contingency.' },
  ];
</script>

<svelte:head>
  <title>Timeline Deep Dive | Surviving the Singularity</title>
  <meta name="description" content="Comprehensive scenario explorer: tech products, cost ranges, and timelines. Conjecture and supposition only. Not financial or professional advice." />
</svelte:head>

<div class="page">

  <!-- Header -->
  <div class="page-header">
    <a href="/#timeline" class="back-link">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M9 2L4 7l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      Back
    </a>
    <div class="header-inner">
      <span class="header-eyebrow">Deep Dive · Conjecture Only</span>
      <h1 class="header-title">Timeline & Cost Explorer</h1>
      <p class="header-sub">A more comprehensive scenario tool. Emerging tech products, rough cost ranges, and what the research suggests about the next 5–10 years. <strong>None of this is a forecast, projection, or recommendation.</strong></p>
    </div>
  </div>

  <p class="page-note">All numbers are illustrative. Do your own research. Not legal or financial advice. <a href="/disclaimer">Read our disclaimers and terms.</a></p>

  <!-- SCENARIO BUILDER -->
  <section class="section" id="scenario">
    <div class="section-inner">
      <div class="section-head">
        <span class="section-num">01</span>
        <div>
          <h2 class="section-title">Scenario Explorer</h2>
          <p class="section-desc">Adjust the chips below to see how different assumptions shift the illustrative arithmetic. Numbers shown are rough estimates; real costs will differ, often significantly.</p>
        </div>
      </div>

      <div class="scenario-grid">
        <!-- Inputs column -->
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
            <span class="chip-label">Region (affects land estimate)</span>
            <div class="chips chips-col">
              {#each regionOptions as opt, i}
                <button class="chip chip-wide" class:chip-on={selRegion === i} on:click={() => selRegion = i}>{opt.label}</button>
              {/each}
            </div>
          </div>

          <div class="chip-section">
            <span class="chip-label">Shouse size (affects build estimate)</span>
            <div class="chips chips-col">
              {#each shouseSizeOptions as opt, i}
                <button class="chip chip-wide" class:chip-on={selSize === i} on:click={() => selSize = i}>{opt.label}</button>
              {/each}
            </div>
          </div>

        </div>

        <!-- Results column -->
        <div class="scenario-results">
          <div class="result-headline">
            <span class="result-label">Illustrative total (all-in rough estimate)</span>
            <span class="result-total">{fmt(totalCost)}</span>
            <span class="result-caveat">Real costs could be 2–5× higher or lower</span>
          </div>

          <div class="result-monthly">
            <div class="rm-row">
              <span class="rm-label">Saving per month</span>
              <span class="rm-val">{fmt(monthlySavings)}</span>
            </div>
            <div class="rm-row">
              <span class="rm-label">Rough time to total (simple arithmetic)</span>
              <span class="rm-val rm-highlight">{fmtY(yearsToTotal)}</span>
            </div>
          </div>

          <div class="cost-breakdown">
            {#each costCategories as cat}
              <div class="cb-row">
                <span class="cb-icon">{cat.icon}</span>
                <span class="cb-label">{cat.label}</span>
                <div class="cb-bar-bg">
                  <div class="cb-bar" style="width: {Math.min(100, (costs[cat.key] / totalCost) * 100)}%; background: #f59e0b22; border-right: 2px solid #f59e0b55;"></div>
                </div>
                <span class="cb-val">{fmt(costs[cat.key])}</span>
              </div>
            {/each}
          </div>

          <div class="breakdown-notes">
            <p class="bn-title">What the estimates don't include:</p>
            <ul class="bn-list">
              <li>Finished interior fit-out (flooring, kitchen, bathroom)</li>
              <li>HVAC, electrical wiring, plumbing rough-in</li>
              <li>Septic system (can be $5K–$30K+)</li>
              <li>Driveway, site prep, clearing</li>
              <li>Property taxes (ongoing)</li>
              <li>Homeowner's insurance</li>
              <li>Food, fuel, living expenses during build phase</li>
              <li>Learning curve cost (time is money)</li>
              <li>Anything that goes wrong (and something will)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- TECH WATCH LIST -->
  <section class="section" id="tech">
    <div class="section-inner">
      <div class="section-head">
        <span class="section-num">02</span>
        <div>
          <h2 class="section-title">Technology Watch List</h2>
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
                <span class="tech-status-chip" class:status-commercial={item.status.startsWith('Commercial')} class:status-research={item.status.startsWith('Research')} class:status-pre={item.status.startsWith('Pre')} class:status-active={item.status.startsWith('Active')} class:status-stealth={item.status.startsWith('Stealth')}>{item.status}</span>
              </div>
              <span class="tech-chevron" class:open={techOpen[i]} aria-hidden="true">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </span>
            </button>

            {#if techOpen[i]}
              <div class="tech-body" transition:slide={{ duration: 220 }}>
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
                  <div class="tech-section">
                    <p class="tech-section-label">Why it might matter</p>
                    <p class="tech-text">{item.relevance}</p>
                  </div>
                  <div class="tech-section tech-cautions">
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
        <p>This list will go stale quickly. The robotics and AI landscape changes faster than any static page can track. Before drawing conclusions from anything above, verify current status independently. The fact that a company or product is listed here implies nothing about its quality, viability, or suitability for your situation.</p>
      </div>
    </div>
  </section>

  <!-- COST DEEP NOTES -->
  <section class="section" id="costs">
    <div class="section-inner">
      <div class="section-head">
        <span class="section-num">03</span>
        <div>
          <h2 class="section-title">What the Numbers Can't Tell You</h2>
          <p class="section-desc">The costs in the scenario above are simplified arithmetic. Here's what the model omits, and why reality is always more complicated.</p>
        </div>
      </div>

      <div class="notes-grid">
        {#each costCategories as cat}
          <div class="note-card">
            <span class="note-icon">{cat.icon}</span>
            <div class="note-body">
              <p class="note-label">{cat.label}</p>
              <p class="note-text">{cat.note}</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <p class="page-note">Do your own research. Not legal or financial advice. <a href="/disclaimer">Read our disclaimers and terms.</a></p>

</div>

<style>
  .page {
    width: 100%;
    max-width: 1040px;
    margin: 0 auto;
    padding: 0 1.5rem 6rem;
  }

  /* Header */
  .page-header {
    padding: 3rem 0 2rem;
  }

  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: #dde4ef;
    text-decoration: none;
    margin-bottom: 1.5rem;
    transition: color 0.15s;
  }
  .back-link:hover { color: #dde4ef; }

  .header-inner { max-width: 700px; }

  .header-eyebrow {
    display: inline-block;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #fb923c;
    font-family: var(--font-primary);
    margin-bottom: 0.75rem;
    padding: 0.2rem 0.6rem;
    background: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.12);
    border-radius: 4px;
  }

  .header-title {
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-weight: 900;
    color: #fafafa;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin: 0 0 0.75rem;
  }

  .header-sub {
    font-size: 1rem;
    color: #e9eef5;
    line-height: 1.7;
    margin: 0;
  }

  .header-sub strong { color: #e9eef5; }

  /* Master disclaimer */
  .master-disclaimer {
    display: flex;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    background: rgba(120, 53, 15, 0.2);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    margin-bottom: 3rem;
  }

  .md-icon {
    font-size: 1.2rem;
    flex-shrink: 0;
    line-height: 1;
    padding-top: 0.15rem;
  }

  .md-body p {
    font-size: 0.88rem;
    color: #fcd34d;
    line-height: 1.7;
    margin: 0;
  }

  .md-title {
    font-weight: 700 !important;
    color: #fde9c8 !important;
    margin-bottom: 0.4rem !important;
    font-family: var(--font-primary);
    font-size: 0.86rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .md-body a { color: #fcd34d; text-decoration: underline; text-underline-offset: 2px; }
  .md-body a:hover { color: #fdf6ec; }
  .md-body strong { color: #fdf6ec; }

  /* Sections */
  .section {
    margin-bottom: 4rem;
    padding-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.04);
  }

  .section-inner { max-width: 100%; }

  .section-head {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 2rem;
  }

  .section-num {
    font-size: 0.85rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: var(--font-primary);
    opacity: 0.6;
    padding-top: 0.2rem;
    min-width: 26px;
  }

  .section-title {
    font-size: clamp(1.3rem, 3vw, 1.9rem);
    font-weight: 800;
    color: #fafafa;
    letter-spacing: -0.03em;
    margin: 0 0 0.3rem;
  }

  .section-desc {
    font-size: 0.88rem;
    color: #dde4ef;
    line-height: 1.65;
    margin: 0;
    max-width: 600px;
  }

  /* Scenario builder */
  .scenario-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: start;
  }

  .scenario-inputs {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    position: sticky;
    top: 1.5rem;
  }

  .chip-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .chip-label {
    font-size: 0.86rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #dde4ef;
    font-family: var(--font-primary);
  }

  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .chips-col {
    flex-direction: column;
    align-items: flex-start;
  }

  .chip {
    padding: 0.32rem 0.7rem;
    border-radius: 6px;
    font-size: 0.86rem;
    font-weight: 600;
    font-family: var(--font-primary);
    border: 1px solid rgba(148, 163, 184, 0.1);
    background: rgba(30, 41, 59, 0.5);
    color: #dde4ef;
    cursor: pointer;
    transition: all 0.15s ease;
    line-height: 1;
  }

  .chip-wide { width: 100%; text-align: left; }

  .chip:hover {
    border-color: rgba(245, 158, 11, 0.3);
    color: #dde4ef;
  }

  .chip-on {
    background: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.4);
    color: #f59e0b;
  }

  /* Results */
  .scenario-results {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .result-headline {
    padding: 1.25rem;
    background: rgba(245, 158, 11, 0.05);
    border: 1px solid rgba(245, 158, 11, 0.12);
    border-radius: 12px;
    text-align: center;
  }

  .result-label {
    display: block;
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #dde4ef;
    font-weight: 600;
    margin-bottom: 0.4rem;
  }

  .result-total {
    display: block;
    font-size: 2.2rem;
    font-weight: 900;
    color: #f59e0b;
    font-family: var(--font-primary);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.3rem;
  }

  .result-caveat {
    display: block;
    font-size: 0.86rem;
    color: #dde4ef;
    font-style: italic;
  }

  .result-monthly {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .rm-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    gap: 1rem;
  }

  .rm-label {
    font-size: 0.86rem;
    color: #dde4ef;
  }

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

  .cb-icon { font-size: 0.8rem; }

  .cb-label {
    font-size: 0.85rem;
    color: #dde4ef;
  }

  .cb-bar-bg {
    height: 4px;
    background: rgba(255,255,255,0.04);
    border-radius: 2px;
    overflow: hidden;
  }

  .cb-bar {
    height: 100%;
    border-radius: 2px;
    transition: width 0.5s ease;
  }

  .cb-val {
    font-size: 0.82rem;
    font-weight: 700;
    color: #e9eef5;
    font-family: var(--font-primary);
    white-space: nowrap;
    text-align: right;
    min-width: 55px;
  }

  .breakdown-notes {
    padding: 1rem;
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.05);
    border-radius: 8px;
  }

  .bn-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #dde4ef;
    margin: 0 0 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .bn-list {
    margin: 0;
    padding-left: 1rem;
  }

  .bn-list li {
    font-size: 0.86rem;
    color: #dde4ef;
    line-height: 1.7;
  }

  /* Tech list */
  .tech-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .tech-item {
    border: 1px solid rgba(148, 163, 184, 0.07);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.4);
    transition: border-color 0.2s;
  }

  .tech-item:hover { border-color: rgba(148, 163, 184, 0.13); }
  .tech-open { border-color: rgba(148, 163, 184, 0.18) !important; background: rgba(30, 41, 59, 0.5); }

  .tech-trigger {
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
    font-family: inherit;
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    text-align: left;
  }

  .tech-trigger:focus-visible {
    outline: 2px solid #f59e0b;
    outline-offset: -2px;
    border-radius: 11px;
  }

  .tech-trigger-left {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    min-width: 0;
  }

  .tech-category {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    border: 1px solid;
    font-family: var(--font-primary);
    white-space: nowrap;
  }

  .tech-name {
    font-size: 0.92rem;
    font-weight: 700;
    color: #e2e8f0;
  }

  .tech-status-chip {
    font-size: 0.82rem;
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
  .status-stealth { background: rgba(100,116,139,0.1); color: #dde4ef; border: 1px solid rgba(100,116,139,0.2); }

  .tech-chevron {
    flex-shrink: 0;
    color: #dde4ef;
    transition: transform 0.22s ease, color 0.15s;
    display: flex;
  }
  .tech-chevron.open { transform: rotate(180deg); color: #dde4ef; }

  .tech-body {
    border-top: 1px solid rgba(148, 163, 184, 0.06);
  }

  .tech-body-inner {
    padding: 1.1rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .tech-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }

  .tech-meta-item {
    background: rgba(30, 41, 59, 0.4);
    border-radius: 8px;
    padding: 0.65rem 0.85rem;
  }

  .tmi-label {
    display: block;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #dde4ef;
    font-weight: 700;
    margin-bottom: 0.2rem;
    font-family: var(--font-primary);
  }

  .tmi-val {
    display: block;
    font-size: 0.8rem;
    color: #dde4ef;
    line-height: 1.4;
  }

  .tech-section { }

  .tech-section-label {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #dde4ef;
    margin: 0 0 0.3rem;
    font-family: var(--font-primary);
  }

  .tech-cautions .tech-section-label { color: #92400e; }
  .tech-cautions .tech-text { color: #fbbf24; }

  .tech-text {
    font-size: 0.85rem;
    color: #dde4ef;
    line-height: 1.7;
    margin: 0;
  }

  .tech-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .tech-link {
    font-size: 0.85rem;
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
    font-size: 0.86rem;
    color: #dde4ef;
    line-height: 1.65;
    margin: 0;
    font-style: italic;
  }

  /* Cost deep notes */
  .notes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 0.75rem;
  }

  .note-card {
    display: flex;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 10px;
  }

  .note-icon { font-size: 1.1rem; flex-shrink: 0; line-height: 1.4; }

  .note-label {
    font-size: 0.86rem;
    font-weight: 700;
    color: #dde4ef;
    margin: 0 0 0.3rem;
  }

  .note-text {
    font-size: 0.86rem;
    color: #dde4ef;
    line-height: 1.6;
    margin: 0;
  }

  /* Bottom disclaimer */
  .bottom-disclaimer {
    padding: 1.5rem;
    background: rgba(120, 53, 15, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 12px;
    margin-top: 2rem;
  }

  .bottom-disclaimer p {
    font-size: 0.82rem;
    color: #fcd34d;
    line-height: 1.7;
    margin: 0;
  }

  .bottom-disclaimer strong { color: #fdf6ec; }
  .bottom-disclaimer a { color: #fcd34d; text-decoration: underline; text-underline-offset: 2px; }
  .bottom-disclaimer a:hover { color: #fdf6ec; }

  /* Responsive */
  @media (max-width: 768px) {
    .scenario-grid { grid-template-columns: 1fr; }
    .scenario-inputs { position: static; }
    .tech-meta-grid { grid-template-columns: 1fr; }
    .tech-trigger-left { gap: 0.35rem; }
  }

  @media (max-width: 480px) {
    .page { padding: 0 1rem 4rem; }
    .notes-grid { grid-template-columns: 1fr; }
  }
</style>
