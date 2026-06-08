<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import AGICountdown from '$lib/components/AGICountdown.svelte';
  import UrgencyBanner from '$lib/components/UrgencyBanner.svelte';

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
</script>

<svelte:head>
  <title>What is AGI? | Surviving the Singularity</title>
  <meta name="description" content="What is AGI, what could it do for humanity, and why you need to lock in now. A clear-eyed breakdown. No hype, no doom, just signal." />
</svelte:head>

<div class="page">

  <UrgencyBanner />

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
        </div>
      </div>
    {/if}
  </section>

  <!-- Conjecture / not-advice notice -->
  <div class="page-disclaimer">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="6" stroke="#dde4ef" stroke-width="1.2"/><path d="M7 4v3.5M7 9.5v.5" stroke="#dde4ef" stroke-width="1.5" stroke-linecap="round"/></svg>
    <p>This page is <strong>commentary and conjecture</strong> synthesized from publicly available information. It is <strong>not financial, career, legal, medical, or preparedness advice</strong>, and nothing here is promised, projected, or guaranteed. Timelines and capabilities are uncertain and contested. Evaluate everything independently and consult qualified professionals before acting. <a href="/disclaimer">Full disclaimer →</a></p>
  </div>

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
        <p class="forecasts-caveat">Paraphrased characterizations as of 2025, not verbatim quotes or endorsements by the named individuals. They are subjective estimates, not forecasts or professional advice, and may misrepresent any person's current view. Verify against primary sources before relying on anything here. <a href="/disclaimer">Full disclaimer →</a></p>
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
      <p class="urgency-caveat">Illustrative figures drawn from public statements and reporting as of 2025, rounded and approximate. Not verified totals, forecasts, or advice. <a href="/disclaimer">Full disclaimer →</a></p>

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

  <!-- ─── CTA ─── -->
  <section class="cta-section" use:observe>
    <div class="cta-inner">
      <p class="cta-eyebrow">Start here</p>
      <h2 class="cta-title">Ready to act on this?</h2>
      <p class="cta-desc">The Blueprint lays out a concrete strategy for material independence before the transition. The book gives you the full mental model. Both are available now, no paywall.</p>
      <div class="cta-buttons">
        <a href="/blueprint" class="cta-btn cta-btn-primary">Read the Blueprint</a>
        <a href="/book" class="cta-btn cta-btn-secondary">Read the Book</a>
        <a href="/timeline" class="cta-btn cta-btn-ghost">See the Timeline →</a>
      </div>
    </div>
  </section>

  <!-- Bottom disclaimer -->
  <div class="bottom-disclaimer">
    <p><strong>Remember:</strong> everything above is one author's synthesis and conjecture about an uncertain future. Not a forecast. Not advice of any kind. Expert timelines are contested and frequently wrong. Before making any financial, career, or life decision based on these ideas, consult qualified professionals who know your situation. <a href="/disclaimer">Read the full disclaimer →</a></p>
  </div>

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

  /* Responsive */
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
  }
</style>
