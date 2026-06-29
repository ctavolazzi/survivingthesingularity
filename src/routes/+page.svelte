<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  export let data;

  let agiYears = '--';
  let agiDays = '---';
  let agiHours = '--';
  let agiMins = '--';
  let agiSecs = '--';
  let countdownReady = false;
  let edition = 'limited';

  function handleCTASubmit(e) {
    e.preventDefault();
    window.location.href = `/book?edition=${edition}`;
  }

  onMount(() => {
    const agiTarget = new Date('2027-11-25T00:00:00Z');
    function updateAGI() {
      const diff = agiTarget - Date.now();
      if (diff <= 0) {
        agiYears = '0'; agiDays = '0'; agiHours = '00'; agiMins = '00'; agiSecs = '00';
        return;
      }
      let s = Math.floor(diff / 1000);
      const secs = s % 60; s = Math.floor(s / 60);
      const mins = s % 60; s = Math.floor(s / 60);
      const hours = s % 24; s = Math.floor(s / 24);
      const years = Math.floor(s / 365);
      const days = s % 365;
      agiYears = years.toLocaleString();
      agiDays = days.toLocaleString();
      agiHours = String(hours).padStart(2, '0');
      agiMins = String(mins).padStart(2, '0');
      agiSecs = String(secs).padStart(2, '0');
    }
    updateAGI();
    const agiInterval = setInterval(updateAGI, 1000);
    setTimeout(() => countdownReady = true, 100);

    const revealObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); }
      });
    }, { threshold: 0.07, rootMargin: '0px 0px -36px 0px' });
    document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

    const countObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        countObs.unobserve(e.target);
        const el = e.target;
        const target = parseFloat(el.dataset.target);
        const prefix = el.dataset.prefix || '';
        const suffix = el.dataset.suffix || '';
        const t0 = performance.now();
        const dur = 1600;
        function tick(now) {
          const p = Math.min((now - t0) / dur, 1);
          const ease = 1 - Math.pow(1 - p, 4);
          el.textContent = prefix + Math.round(target * ease).toLocaleString() + suffix;
          if (p < 1) requestAnimationFrame(tick);
          else el.textContent = prefix + target.toLocaleString() + suffix;
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.count-up').forEach(el => countObs.observe(el));

    return () => clearInterval(agiInterval);
  });
</script>

<svelte:head>
  <title>Surviving the Singularity: New Era, New Playbook</title>
</svelte:head>

<div class="home">

  <div class="ambient" aria-hidden="true">
    <div class="ambient-orb ambient-orb-1"></div>
    <div class="ambient-orb ambient-orb-2"></div>
  </div>
  <div class="noise" aria-hidden="true"></div>

  <!-- AGI COUNTDOWN -->
  <section class="agi-section" aria-label="AGI Countdown">
    <div class="section-inner">
      <a href="/agi" class="agi-countdown ac-clickable" aria-label="Countdown to AGI: tap to learn why 2027">
        <div class="ac-eyebrow">
          <span class="ac-dot"></span>
          <span>The Clock Is Running</span>
        </div>
        <h2 class="ac-heading">Countdown to <span class="ac-highlight">AGI</span></h2>
        <div class="ac-display" class:ac-ready={countdownReady} role="timer" aria-label="Time remaining until AGI horizon">
          <div class="ac-block ac-block-accent">
            <span class="ac-value">{agiYears}</span>
            <span class="ac-label">Years</span>
          </div>
          <div class="ac-sep" aria-hidden="true">:</div>
          <div class="ac-block">
            <span class="ac-value">{agiDays}</span>
            <span class="ac-label">Days</span>
          </div>
          <div class="ac-sep" aria-hidden="true">:</div>
          <div class="ac-block">
            <span class="ac-value">{agiHours}</span>
            <span class="ac-label">Hrs</span>
          </div>
          <div class="ac-sep" aria-hidden="true">:</div>
          <div class="ac-block">
            <span class="ac-value">{agiMins}</span>
            <span class="ac-label">Min</span>
          </div>
          <div class="ac-sep" aria-hidden="true">:</div>
          <div class="ac-block ac-block-sec">
            <span class="ac-value">{agiSecs}</span>
            <span class="ac-label">Sec</span>
          </div>
        </div>
      </a>
    </div>
  </section>

  <!-- HERO -->
  <section id="hero" aria-labelledby="hero-heading">
    <div class="hero section-inner">

      <div class="hero-video-wrap reveal">
        <div class="hero-video-ratio">
          <iframe
            src="https://www.youtube.com/embed/YZH1csMhnDo"
            title="BotQ: Figure ramping F.03 production"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
      </div>

      <div class="hero-text reveal reveal-d1">
        <h1 class="hero-headline" id="hero-heading">
          The future<br><span class="headline-nowrap">isn't coming&hellip;</span>
          <em>It's here.</em>
        </h1>
        <div class="hero-sub-stack">
          <p class="hero-sub-line">AI is ending careers. Rewriting industries.</p>
          <p class="hero-sub-line hero-sub-punch">Most people have no idea what's coming.</p>
          <p class="hero-sub-line">You can be the one who does.</p>
          <p class="hero-sub-line">Before the window closes.</p>
        </div>
        <div class="hero-actions">
          <a href="/early-access" class="btn-primary">
            Get Early Access: $5
            <span class="btn-icon" aria-hidden="true">
              <svg width="13" height="13" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M11 3H5M11 3V9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </span>
          </a>
          <a href="/blueprint" class="btn-ghost">Read the Blueprint</a>
        </div>
        <p class="hero-disclaimer">
          For informational and educational purposes only. Not legal, financial, or professional advice.
          <br><a href="/disclaimer">Full disclaimer.</a>
        </p>
      </div>

    </div>
  </section>

  <!-- STATS -->
  <section class="stat-strip" aria-label="By the numbers">
    <div class="section-inner">
      <div class="ss-grid reveal">
        <div class="ss-item">
          <span class="ss-num">300M</span>
          <span class="ss-desc">full-time jobs globally at risk from AI</span>
          <a href="https://www.google.com/search?q=Goldman+Sachs+300+million+jobs+AI+generative" target="_blank" rel="noopener noreferrer" class="ss-src ss-src-link">Goldman Sachs</a>
        </div>
        <div class="ss-item">
          <span class="ss-num">99%</span>
          <span class="ss-desc">of business leaders plan AI-driven headcount cuts within 2 years</span>
          <a href="https://www.google.com/search?q=Mercer+2026+survey+AI+headcount+cuts+business+leaders" target="_blank" rel="noopener noreferrer" class="ss-src ss-src-link">Mercer, 2026</a>
        </div>
        <div class="ss-item">
          <div class="ss-price-compare">
            <span class="ss-num ss-num-old">$100,000</span>
            <span class="ss-num">$1,000</span>
          </div>
          <span class="ss-desc">Robot capability now available in your own home</span>
          <a href="https://www.google.com/search?q=open+source+robot+arm+$1000+home+2026+LeRobot+SO-100" target="_blank" rel="noopener noreferrer" class="ss-src ss-src-link">Open-source robotics</a>
        </div>
        <div class="ss-item">
          <span class="ss-num">0</span>
          <span class="ss-desc">years of preparation. The first government responses to AI displacement are appearing right now. They are nowhere near enough.</span>
          <a href="https://www.google.com/search?q=government+AI+displacement+worker+protection+plan+2026" target="_blank" rel="noopener noreferrer" class="ss-src ss-src-link">No one is coming to save you.</a>
        </div>
      </div>
    </div>
  </section>

  <!-- BEFORE / AFTER -->
  <section class="reality-section" aria-label="Without a plan vs with a plan">
    <div class="reality-inner reveal">
      <h2 class="reality-heading">Most people will get steamrolled.<br>You don't have to be one of them.</h2>
      <div class="reality-cols">
        <div class="reality-col reality-col-bad">
          <span class="reality-col-label">Without a plan</span>
          <ul class="reality-list">
            <li>You fall behind while others win</li>
            <li>Every disruption makes your position worse</li>
            <li>You scramble when others capitalize</li>
            <li>You're the last to adapt. First to suffer.</li>
          </ul>
        </div>
        <div class="reality-col reality-col-good">
          <span class="reality-col-label">With a plan</span>
          <ul class="reality-list">
            <li>You see what's coming while others are blindsided</li>
            <li>You build leverage most people won't even know exists</li>
            <li>Disruptions become advantages. For you.</li>
            <li>You level up while everyone else is still catching on.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- MIDDLE -->
  <section class="middle-section" aria-label="Why this matters">
    <div class="section-inner">
      <div class="middle-inner">

        <div class="middle-facts reveal">
          <h2 class="middle-heading">They don't want you to know the truth...<br>so here it is.</h2>
          <ul class="middle-list">
            <li>AI is displacing workers right now. CEOs are tripping over themselves to cut headcount. It is not stopping.</li>
            <li>Robot capabilities that cost $100K in 2022 are available for under $1,000 today.</li>
            <li>Most people are treating AI like the enemy. Fighting it. Resisting it. That is not going to work.</li>
            <li>You can use the same tools ending other people's careers to build yours. Automate your survival. Get ahead.</li>
          </ul>
        </div>

        <div class="middle-offer reveal reveal-d1">
          <p class="middle-offer-label">Here's what you do about it</p>
          <ul class="middle-offer-list">
            <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>12-step readiness checklist</li>
            <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Full blueprint, all 8 chapters</li>
            <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Research bundle: the papers and sources behind the book</li>
            <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Book draft, updated as it's written</li>
          </ul>
          <a href="/early-access" class="middle-btn">Get all of it: $5</a>
          <p class="middle-fine">One-time. Price goes up at launch.</p>
        </div>

      </div>
    </div>
  </section>

  <!-- STAGES -->
  <section id="timeline" aria-label="What's coming and when">
    <div class="section-inner">
      <div class="timeline-header reveal">
        <div>
          <span class="section-label">The Stages</span>
          <h2 class="section-heading">This is already in motion.</h2>
        </div>
        <p class="section-sub">Every stage below is documented. The question is where you'll be standing when each one hits.</p>
      </div>
      <div class="timeline-track reveal reveal-d1">
        <div class="timeline-item">
          <div class="timeline-dot-row">
            <div class="timeline-dot past"></div>
            <span class="timeline-period">2024</span>
          </div>
          <p class="timeline-label">The Warning Signs</p>
          <p class="timeline-desc">AI tools go mainstream. Early job cuts begin. The people paying attention start preparing. Most people ignore it.</p>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot-row">
            <div class="timeline-dot past"></div>
            <span class="timeline-period">2025</span>
          </div>
          <p class="timeline-label">The Threshold Crossed</p>
          <p class="timeline-desc">AI model capabilities exceeded the average person in key areas. The intelligence gap closed. Most people missed it completely.</p>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot-row">
            <div class="timeline-dot now"></div>
            <span class="timeline-period">2026 — Now</span>
          </div>
          <p class="timeline-label">Physical AI Arrives</p>
          <p class="timeline-desc">Humanoid robots are entering workplaces. The social contract is being dismantled. Most people still think this is someone else's problem.</p>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot-row">
            <div class="timeline-dot"></div>
            <span class="timeline-period">2027+</span>
          </div>
          <p class="timeline-label">AGI Horizon</p>
          <p class="timeline-desc">Median expert estimate for AGI. Prepared people thrive. Don't be blindsided - be ready.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- VIDEO -->
  <section class="video-section" aria-label="Watch">
    <div class="video-wrap reveal">
      <div class="video-ratio">
        <iframe
          src="https://www.youtube.com/embed/6K_bGH54ltI"
          title="AI capabilities — Surviving the Singularity"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>
  </section>

  <!-- BOOK STRUCTURE -->
  <section id="chapters" aria-label="What's in the book">
    <div class="section-inner">
      <div class="chapters-header reveal">
        <span class="section-label">The Book</span>
        <h2 class="section-heading">Three parts. The complete picture.</h2>
        <p class="section-sub">What's happening. How people react. What you can do. In that order.</p>
      </div>
      <div class="book-parts reveal reveal-d1">
        <div class="book-part book-part-1">
          <span class="book-part-num">Part I</span>
          <h3 class="book-part-title">What's Happening</h3>
          <p class="book-part-sub">The Nine Stages of Intelligence Scaling</p>
          <p class="book-part-desc">From the AI tools you're using today to systems that outperform humans at everything. Stage by stage. So you understand exactly what you're looking at before it lands on you.</p>
        </div>
        <div class="book-part book-part-2">
          <span class="book-part-num">Part II</span>
          <h3 class="book-part-title">How People Will React</h3>
          <p class="book-part-sub">Denial. Panic. Opportunism.</p>
          <p class="book-part-desc">Most people follow predictable patterns when disruption hits. Understanding those patterns puts you ahead of the reaction before it happens. You don't have to be one of the ones who panics.</p>
        </div>
        <div class="book-part book-part-3">
          <span class="book-part-num">Part III</span>
          <h3 class="book-part-title">What You Can Do</h3>
          <p class="book-part-sub">Concrete Moves. Actual Steps.</p>
          <p class="book-part-desc">Not abstract advice. The specific moves to build leverage, protect your position, and come out ahead while everyone else is still figuring out what happened.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section id="act" aria-labelledby="act-heading">
    <div class="section-inner">
      <div class="cta-inner reveal">
        <div class="cta-glow" aria-hidden="true"></div>
        <h2 class="cta-heading" id="act-heading">Get ready.<br><em>Five dollars.</em></h2>
        <p class="cta-sub">The blueprint. The research bundle. The book draft. Get ahead of everyone else. One payment.<br><br>Limited time offer. Price goes up at launch.</p>
        <a href="/early-access" class="btn-primary" style="font-size:1.1rem; padding:16px 36px;">
          Get Early Access: $5
          <span class="btn-icon" aria-hidden="true">
            <svg width="13" height="13" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M11 3H5M11 3V9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </span>
        </a>
        <p style="font-size:0.8rem; color:#64748b; margin-top:14px;">No upsells. No subscription. Just the stuff that matters.</p>
      </div>
    </div>
  </section>

  <!-- WELCOME VIDEO -->
  <section class="video-section" aria-label="Welcome to the community">
    <div class="video-wrap reveal">
      <div class="video-ratio">
        <iframe
          src="https://www.youtube.com/embed/NKENM_J-rEg"
          title="Welcome to the Surviving the Singularity community"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>
  </section>

  <div class="thanks-wrap">
    <p class="thanks-text">Thank you for being here ❣️</p>
  </div>

</div>

<style>
  .home {
    font-family: 'Outfit', system-ui, sans-serif;
    --bg:            #020617;
    --bg-raised:     #060d1f;
    --surface:       #0f172a;
    --surface-2:     #1e293b;
    --border:        rgba(255,255,255,0.05);
    --border-mid:    rgba(255,255,255,0.09);
    --border-strong: rgba(255,255,255,0.14);
    --amber:         #f59e0b;
    --amber-light:   #fbbf24;
    --amber-dim:     rgba(245,158,11,0.12);
    --blue:          #3b82f6;
    --green:         #10b981;
    --text-1:        #f8fafc;
    --text-2:        #cbd5e1;
    --text-3:        #64748b;
    --text-4:        #334155;
    --font-mono:     'JetBrains Mono', monospace;
    --ease-out:      cubic-bezier(0.16, 1, 0.3, 1);
    --ease-spring:   cubic-bezier(0.34, 1.56, 0.64, 1);
    --r-card:        20px;
    --r-pill:        999px;
  }

  /* AMBIENT */
  .ambient { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
  .ambient-orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.35; }
  .ambient-orb-1 {
    width: min(600px, 80vw); height: min(600px, 80vw);
    background: radial-gradient(circle, rgba(245,158,11,0.12) 0%, transparent 70%);
    top: -15%; right: -10%;
    animation: orb-drift 14s ease-in-out infinite alternate;
  }
  .ambient-orb-2 {
    width: min(400px, 60vw); height: min(400px, 60vw);
    background: radial-gradient(circle, rgba(59,130,246,0.07) 0%, transparent 70%);
    bottom: 20%; left: -8%;
    animation: orb-drift 18s ease-in-out infinite alternate-reverse;
  }
  @keyframes orb-drift {
    from { transform: translate(0,0) scale(1); }
    to   { transform: translate(30px, 20px) scale(1.08); }
  }
  .noise {
    position: fixed; inset: 0; z-index: 60;
    pointer-events: none; opacity: 0.025;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    background-size: 128px;
  }

  /* SCROLL REVEAL */
  :global(.reveal) {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.7s var(--ease-out, cubic-bezier(0.16,1,0.3,1)), transform 0.7s var(--ease-out, cubic-bezier(0.16,1,0.3,1));
  }
  :global(.reveal.visible) { opacity: 1; transform: translateY(0); }
  :global(.reveal-d1) { transition-delay: 0.08s; }
  :global(.reveal-d2) { transition-delay: 0.16s; }
  :global(.reveal-d3) { transition-delay: 0.24s; }
  :global(.reveal-d4) { transition-delay: 0.34s; }
  :global(.reveal-d5) { transition-delay: 0.44s; }

  /* SECTION WRAPPER */
  section { position: relative; z-index: 1; }
  .section-inner {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding-left: clamp(20px, 5vw, 60px);
    padding-right: clamp(20px, 5vw, 60px);
    box-sizing: border-box;
  }

  /* BUTTONS */
  .btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 14px 14px 14px 24px;
    background: var(--amber);
    color: #0a0a0a;
    font-family: 'Outfit', system-ui, sans-serif;
    font-weight: 800;
    font-size: 1.05rem;
    border: none;
    border-radius: var(--r-pill);
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none;
    transition: filter 0.2s ease, transform 0.2s var(--ease-spring), box-shadow 0.2s ease;
    box-shadow: 0 4px 20px rgba(245,158,11,0.28);
  }
  .btn-primary:hover { filter: brightness(1.08); transform: translateY(-2px); box-shadow: 0 8px 28px rgba(245,158,11,0.42); }
  .btn-primary:active { transform: scale(0.98); }
  .btn-icon {
    width: 28px; height: 28px;
    background: rgba(0,0,0,0.16);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: transform 0.2s var(--ease-spring);
  }
  .btn-primary:hover .btn-icon { transform: translate(2px,-2px); }
  .btn-ghost {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 14px 22px;
    background: transparent;
    color: var(--text-2);
    font-family: 'Outfit', system-ui, sans-serif;
    font-weight: 600;
    font-size: 1.05rem;
    border: 1px solid var(--border-mid);
    border-radius: var(--r-pill);
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none;
    transition: color 0.2s ease, border-color 0.2s ease, background 0.2s ease;
  }
  .btn-ghost:hover { color: var(--text-1); border-color: var(--border-strong); background: rgba(255,255,255,0.04); }

  /* SECTION HEADINGS */
  .section-label {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--amber);
    opacity: 0.85;
    margin-bottom: 16px;
    display: block;
  }
  .section-heading {
    font-size: clamp(2.2rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.02;
    letter-spacing: -0.03em;
    color: var(--text-1);
    margin-bottom: 16px;
  }
  .section-sub {
    font-size: clamp(1rem, 2.2vw, 1.25rem);
    color: var(--text-2);
    line-height: 1.7;
    max-width: 50ch;
  }

  /* AGI COUNTDOWN */
  .agi-section {
    position: relative; z-index: 1;
    border-bottom: 1px solid var(--border);
    padding-top: clamp(20px, 3vw, 32px);
  }
  .agi-section .section-inner {
    padding-top: clamp(16px, 2.5vw, 28px);
    padding-bottom: clamp(28px, 4vw, 44px);
  }
  .agi-countdown {
    text-align: center;
    display: block;
    text-decoration: none;
    color: inherit;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  .agi-countdown:hover { opacity: 0.85; }
  .ac-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: clamp(0.78rem, 2vw, 0.9rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--amber);
    margin-bottom: 14px;
  }
  .ac-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--amber);
    box-shadow: 0 0 8px var(--amber);
    flex-shrink: 0;
    animation: ac-pulse 2s ease-in-out infinite;
  }
  @keyframes ac-pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.75); }
  }
  .ac-heading {
    font-size: clamp(2rem, 7vw, 4rem);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-1);
    margin-bottom: clamp(20px, 3vw, 32px);
    line-height: 1.0;
  }
  .ac-highlight { color: var(--amber); }
  .ac-display {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    flex-wrap: nowrap;
    gap: clamp(6px, 2vw, 14px);
    margin-bottom: 16px;
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  .ac-display.ac-ready { opacity: 1; transform: none; }
  .ac-block { display: flex; flex-direction: column; align-items: center; gap: clamp(8px, 1.2vw, 12px); min-width: 0; }
  .ac-value {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(60px, 15vw, 100px);
    height: clamp(60px, 15vw, 100px);
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 0;
    font-family: var(--font-mono);
    font-size: clamp(1.4rem, 5.5vw, 2.8rem);
    font-weight: 900;
    color: var(--text-1);
    line-height: 1;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }
  .ac-block-accent .ac-value {
    color: var(--amber);
    border-color: rgba(245,158,11,0.3);
    background: rgba(245,158,11,0.06);
    box-shadow: 2px 2px 0 rgba(245,158,11,0.15);
  }
  .ac-block-sec .ac-value { color: var(--text-2); }
  .ac-label {
    font-family: var(--font-mono);
    font-size: clamp(0.68rem, 1.6vw, 0.82rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-3);
    white-space: nowrap;
  }
  .ac-sep {
    font-family: var(--font-mono);
    font-size: clamp(1.2rem, 4vw, 2rem);
    font-weight: 700;
    color: rgba(245,158,11,0.25);
    align-self: center;
    margin-bottom: clamp(24px, 3.5vw, 36px);
    flex-shrink: 0;
  }

  /* HERO */
  .hero {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(36px, 6vw, 60px);
    padding: clamp(12px, 2vw, 24px) clamp(20px, 5vw, 64px) clamp(64px, 10vw, 100px);
    overflow: hidden;
    max-width: none;
  }
  .hero::before {
    content: '';
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px);
    background-size: 64px 64px;
    pointer-events: none;
  }
  .hero-video-wrap { width: 100%; max-width: min(820px, 100%); display: flex; flex-direction: column; gap: 12px; }
  .hero-video-ratio {
    position: relative; width: 100%; padding-bottom: 56.25%;
    border-radius: 16px; overflow: hidden;
    background: var(--surface); border: 1px solid var(--border-mid);
  }
  .hero-video-ratio iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: none; }
  .hero-text {
    width: 100%; max-width: min(760px, 100%);
    display: flex; flex-direction: column; align-items: center;
    gap: clamp(20px, 3vw, 28px); text-align: center;
  }
  .hero-headline {
    font-size: clamp(2.4rem, 9.5vw, 8rem);
    font-weight: 900;
    line-height: 0.92;
    letter-spacing: -0.04em;
    color: var(--text-1);
  }
  .hero-headline em { font-style: italic; color: var(--amber); display: block; }
  .headline-nowrap { white-space: nowrap; }
  .hero-sub { font-size: clamp(1.1rem, 2.5vw, 1.4rem); color: var(--text-2); line-height: 1.65; max-width: 52ch; }
  .hero-sub-stack { display: flex; flex-direction: column; gap: 12px; max-width: 44ch; text-align: center; }
  .hero-sub-line { font-size: clamp(1.05rem, 2.2vw, 1.25rem); color: var(--text-2); line-height: 1.45; margin: 0; }
  .hero-sub-punch { color: var(--text-1); font-weight: 700; font-size: clamp(1.1rem, 2.5vw, 1.35rem); }
  .hero-actions { display: flex; align-items: center; justify-content: center; gap: 12px; flex-wrap: wrap; }
  .hero-disclaimer { font-size: 0.95rem; color: var(--text-4); line-height: 1.6; max-width: 48ch; }
  .hero-disclaimer a { color: var(--text-3); text-decoration: underline; text-underline-offset: 2px; }

  /* STAT STRIP */
  .stat-strip { border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: clamp(40px, 6vw, 64px) 0; }
  .ss-grid { display: grid; grid-template-columns: repeat(4, 1fr); }
  @media (max-width: 780px) { .ss-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 420px) { .ss-grid { grid-template-columns: 1fr; } }
  .ss-item { display: flex; flex-direction: column; gap: 8px; padding: clamp(24px, 3.5vw, 40px) clamp(20px, 3vw, 32px); border-right: 1px solid var(--border); }
  .ss-item:last-child { border-right: none; }
  @media (max-width: 780px) {
    .ss-item:nth-child(2) { border-right: none; }
    .ss-item:nth-child(n+3) { border-top: 1px solid var(--border); }
    .ss-item:nth-child(4) { border-right: none; }
  }
  @media (max-width: 420px) { .ss-item { border-right: none; border-bottom: 1px solid var(--border); } .ss-item:last-child { border-bottom: none; } }
  .ss-price-compare { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
  .ss-num { font-family: var(--font-mono); font-size: clamp(2.2rem, 6vw, 3.8rem); font-weight: 900; color: var(--amber); letter-spacing: -0.03em; line-height: 1; }
  .ss-num-old { color: var(--text-4); font-size: clamp(1.4rem, 3.5vw, 2.2rem); text-decoration: line-through; text-decoration-color: #ef4444; text-decoration-thickness: 3px; }
  .ss-desc { font-size: clamp(0.88rem, 1.8vw, 1rem); color: var(--text-2); line-height: 1.55; }
  .ss-src { font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-4); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }
  .ss-src-link { color: var(--text-3); text-decoration: underline; text-underline-offset: 2px; transition: color 0.15s ease; }
  .ss-src-link:hover { color: var(--amber); }

  /* BOOK CARD */
  .hero-book-card {
    background: linear-gradient(135deg, rgba(245,158,11,0.06) 0%, rgba(15,23,42,0.6) 60%);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 18px;
    padding: 24px;
    display: flex;
    gap: 22px;
    align-items: flex-start;
    position: relative; overflow: hidden;
    width: 100%; max-width: min(600px, 100%);
  }
  .hero-book-card::before {
    content: ''; position: absolute; top: 0; right: 0;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(245,158,11,0.1) 0%, transparent 70%);
    pointer-events: none;
  }
  .hero-book-card-cover { flex-shrink: 0; width: clamp(64px, 16vw, 88px); }
  .book-outer {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.14);
    box-shadow: 0 0 60px rgba(245,158,11,0.08), 0 32px 64px rgba(0,0,0,0.5);
  }
  .book-inner { background: var(--surface); overflow: hidden; box-shadow: inset 0 1px 0 rgba(255,255,255,0.07); }
  .book-cover { width: 100%; height: auto; display: block; }
  .hero-book-card-body { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
  .hero-book-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.88rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; color: var(--amber);
  }
  .hero-book-title { font-size: clamp(1.25rem, 3vw, 1.5rem); font-weight: 900; color: var(--text-1); letter-spacing: -0.02em; line-height: 1.2; }
  .hero-book-pitch { font-size: 1.05rem; color: var(--text-2); line-height: 1.65; margin-bottom: 2px; }
  .hero-book-bullets { display: flex; flex-direction: column; gap: 6px; margin-bottom: 4px; padding: 0; }
  .hero-book-bullets li {
    font-family: var(--font-mono); font-size: 0.95rem; color: var(--text-3);
    display: flex; align-items: center; gap: 8px;
  }
  .hero-book-bullets li::before {
    content: ''; width: 5px; height: 5px;
    border-radius: 50%; background: var(--amber); flex-shrink: 0;
  }
  .hero-book-editions { display: flex; flex-direction: column; gap: 8px; }
  .hero-book-cta {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--amber); color: #1a0f00;
    font-size: 1.05rem; font-weight: 800;
    padding: 11px 18px; border-radius: 8px;
    letter-spacing: 0.01em; text-decoration: none;
    transition: filter 0.2s var(--ease-out), transform 0.2s var(--ease-out);
    align-self: flex-start;
  }
  .hero-book-cta:hover { filter: brightness(1.1); transform: translateY(-1px); }
  .hero-book-cta-secondary {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.88rem; font-weight: 700;
    color: var(--text-3); text-decoration: none;
    padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);
    transition: color 0.15s ease, border-color 0.15s ease;
  }
  .hero-book-cta-secondary:hover { color: var(--amber); border-color: rgba(245,158,11,0.3); }

  /* ROBOT COST */
  .robot-cost-section { padding: clamp(64px, 10vw, 120px) 0; border-top: 1px solid var(--border); }
  .robot-cost-intro { max-width: 640px; margin: 0 auto clamp(40px, 6vw, 64px); text-align: center; }
  .robot-myth-bar {
    display: flex; align-items: center; justify-content: center;
    gap: clamp(16px, 4vw, 48px); flex-wrap: wrap;
    margin-bottom: clamp(40px, 6vw, 64px);
  }
  .myth-old-price {
    font-family: var(--font-mono);
    font-size: clamp(2.2rem, 8vw, 4.5rem); font-weight: 900;
    color: var(--text-4);
    text-decoration: line-through; text-decoration-color: #ef4444; text-decoration-thickness: 4px;
    letter-spacing: -0.03em; line-height: 1;
  }
  .myth-arrow { font-size: clamp(1.4rem, 4vw, 2.4rem); color: var(--text-4); flex-shrink: 0; }
  .myth-new { display: flex; flex-direction: column; align-items: flex-start; gap: 4px; }
  .myth-new-price {
    font-family: var(--font-mono);
    font-size: clamp(2.2rem, 8vw, 4.5rem); font-weight: 900;
    color: var(--amber); letter-spacing: -0.03em; line-height: 1;
  }
  .myth-new-label {
    font-size: 0.82rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--text-3); font-family: var(--font-mono);
  }
  .robot-opts-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: clamp(12px, 2vw, 20px); margin-bottom: clamp(36px, 6vw, 56px);
  }
  @media (max-width: 700px) { .robot-opts-grid { grid-template-columns: 1fr; } }
  .robot-opt {
    background: var(--surface); border: 1px solid var(--border-mid);
    border-radius: 14px; padding: clamp(18px, 3vw, 28px);
    display: flex; flex-direction: column; gap: 8px;
    transition: border-color 0.15s ease;
  }
  .robot-opt:hover { border-color: var(--border-strong); }
  .robot-opt-featured { border-color: rgba(245,158,11,0.3); background: rgba(245,158,11,0.04); }
  .robot-opt-featured:hover { border-color: rgba(245,158,11,0.5); }
  .robot-opt-img-wrap {
    position: relative; width: 100%; height: 160px;
    border-radius: 8px; overflow: hidden;
    background: rgba(255,255,255,0.03); border: 1px solid var(--border); margin-bottom: 10px;
  }
  .robot-opt-img-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .robot-opt-img-placeholder {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-4);
    text-transform: uppercase; letter-spacing: 0.1em;
    position: absolute; inset: 0;
  }
  .robot-opt-tier {
    font-family: var(--font-mono); font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em; color: var(--text-4);
  }
  .robot-opt-featured .robot-opt-tier { color: var(--amber); }
  .robot-opt-price { font-family: var(--font-mono); font-size: clamp(1.5rem, 3.5vw, 2rem); font-weight: 900; color: var(--text-1); letter-spacing: -0.03em; line-height: 1; }
  .robot-opt-featured .robot-opt-price { color: var(--amber); }
  .robot-opt-name { font-size: 1.05rem; font-weight: 700; color: var(--text-1); margin-top: 2px; }
  .robot-opt-desc { font-size: 0.92rem; color: var(--text-3); line-height: 1.6; }
  .robot-opt-link {
    font-size: 0.8rem; font-weight: 700; color: var(--text-4);
    text-decoration: none; text-transform: uppercase; letter-spacing: 0.08em;
    font-family: var(--font-mono); margin-top: auto; padding-top: 8px;
    border-top: 1px solid var(--border);
    display: flex; align-items: center; gap: 4px;
    transition: color 0.15s ease;
  }
  .robot-opt-link:hover { color: var(--amber); }

  /* VIDEO */
  .video-section { position: relative; z-index: 1; padding: clamp(40px, 6vw, 64px) clamp(20px, 5vw, 60px); border-top: 1px solid var(--border); }
  .video-wrap { max-width: min(720px, 100%); margin: 0 auto; }
  .video-ratio { position: relative; width: 100%; padding-bottom: 56.25%; border-radius: 16px; overflow: hidden; background: var(--surface); border: 1px solid var(--border-mid); }
  .video-ratio iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: none; }
  .video-caption { margin-top: 14px; font-size: 1rem; color: var(--text-3); text-align: center; line-height: 1.6; }
  .video-caption strong { color: var(--text-2); font-weight: 600; }
  .video-credit { font-family: var(--font-mono); font-size: 0.88rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-4); }

  /* BENTO / SITUATION */
  #situation { padding: clamp(64px, 10vw, 120px) 0; border-top: 1px solid var(--border); }
  .situation-header { margin-bottom: clamp(36px, 5vw, 56px); }
  .bento { display: grid; grid-template-columns: repeat(12, 1fr); gap: 10px; }
  .bento-label-row { grid-column: 1 / -1; display: flex; align-items: center; gap: 14px; padding: 8px 0 2px; }
  .row-line { flex: 1; height: 1px; }
  .row-line.danger { background: rgba(251,146,60,0.2); }
  .row-line.opportunity { background: rgba(16,185,129,0.2); }
  .row-badge { font-family: var(--font-mono); font-size: 1rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 5px 14px; border-radius: var(--r-pill); white-space: nowrap; }
  .row-badge.danger { background: rgba(251,146,60,0.12); color: #fb923c; }
  .row-badge.opportunity { background: rgba(16,185,129,0.1); color: var(--green); }
  .bento-cell {
    border-radius: var(--r-card); padding: clamp(20px, 3vw, 28px);
    border: 1px solid var(--border-mid);
    display: flex; flex-direction: column; gap: 8px; min-width: 0; overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s var(--ease-out);
  }
  .bento-cell:hover { border-color: var(--border-strong); transform: translateY(-2px); }
  .cell-p-wide { grid-column: span 5; background: linear-gradient(145deg, rgba(251,146,60,0.07) 0%, rgba(15,23,42,0.3) 100%); }
  .cell-p-mid  { grid-column: span 4; background: linear-gradient(150deg, rgba(251,146,60,0.04) 0%, rgba(15,23,42,0.3) 100%); }
  .cell-p-sm   { grid-column: span 3; background: linear-gradient(150deg, rgba(251,146,60,0.04) 0%, rgba(15,23,42,0.3) 100%); }
  .cell-o-wide { grid-column: span 5; background: linear-gradient(145deg, rgba(16,185,129,0.07) 0%, rgba(15,23,42,0.3) 100%); }
  .cell-o-mid  { grid-column: span 4; background: linear-gradient(150deg, rgba(16,185,129,0.04) 0%, rgba(15,23,42,0.3) 100%); }
  .cell-o-sm   { grid-column: span 3; background: linear-gradient(150deg, rgba(16,185,129,0.04) 0%, rgba(15,23,42,0.3) 100%); }
  @media (max-width: 860px) {
    .bento { grid-template-columns: 1fr 1fr; }
    .cell-p-wide, .cell-p-mid, .cell-p-sm,
    .cell-o-wide, .cell-o-mid, .cell-o-sm { grid-column: span 1; }
  }
  @media (max-width: 540px) { .bento { grid-template-columns: 1fr; } }
  .stat-number { font-family: var(--font-mono); font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 700; line-height: 1; }
  .stat-number.danger { color: #fb923c; }
  .stat-number.opportunity { color: var(--green); }
  .stat-desc { font-size: 1.15rem; color: var(--text-2); line-height: 1.6; flex: 1; }
  .stat-source { font-family: var(--font-mono); font-size: 0.88rem; color: var(--text-4); margin-top: auto; text-decoration: none; }
  .stat-source:hover { color: var(--text-3); }

  /* TELEOP */
  .teleop-section { padding: clamp(64px, 10vw, 120px) 0; border-top: 1px solid var(--border); }
  .teleop-intro { max-width: 680px; margin: 0 auto clamp(48px, 7vw, 72px); text-align: center; }
  .teleop-contrast { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(12px, 2vw, 20px); margin-bottom: clamp(48px, 7vw, 72px); }
  @media (max-width: 600px) { .teleop-contrast { grid-template-columns: 1fr; } }
  .teleop-side { border: 1px solid var(--border-mid); border-radius: 14px; padding: clamp(20px, 3vw, 32px); }
  .teleop-side-now { background: rgba(239,68,68,0.04); border-color: rgba(239,68,68,0.18); }
  .teleop-side-then { background: rgba(16,185,129,0.04); border-color: rgba(16,185,129,0.18); }
  .teleop-side-label { font-family: var(--font-mono); font-size: clamp(0.85rem, 1.6vw, 1rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px; display: block; }
  .teleop-side-now .teleop-side-label { color: #f87171; }
  .teleop-side-then .teleop-side-label { color: #34d399; }
  .teleop-side-headline { font-size: clamp(1.5rem, 3.5vw, 2.2rem); font-weight: 800; color: var(--text-1); line-height: 1.25; margin-bottom: 16px; }
  .teleop-side-body { font-size: clamp(1rem, 2vw, 1.2rem); color: var(--text-1); line-height: 1.65; margin-bottom: 8px; }
  .teleop-pivot { text-align: center; margin-bottom: clamp(48px, 7vw, 72px); }
  .teleop-pivot-q { font-size: clamp(1.6rem, 4.5vw, 2.8rem); font-weight: 900; color: var(--text-1); letter-spacing: -0.03em; line-height: 1.2; margin-bottom: 16px; }
  .teleop-pivot-q em { color: var(--amber); font-style: italic; }
  .teleop-pivot-sub { font-size: clamp(1rem, 2.2vw, 1.25rem); color: var(--text-1); line-height: 1.7; max-width: 52ch; margin: 0 auto 8px; }
  .teleop-jobs-label { font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: var(--text-4); text-align: center; margin-bottom: 20px; display: block; }
  .teleop-jobs-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(10px, 1.8vw, 16px); margin-bottom: clamp(32px, 5vw, 48px); }
  @media (max-width: 580px) { .teleop-jobs-grid { grid-template-columns: 1fr; } }
  .teleop-job {
    background: var(--surface); border: 1px solid var(--border-mid);
    border-radius: 12px; padding: clamp(18px, 2.5vw, 26px);
    display: flex; gap: 14px; align-items: flex-start;
    transition: border-color 0.15s ease;
  }
  .teleop-job:hover { border-color: rgba(245,158,11,0.3); }
  .teleop-job-icon {
    font-size: 1.5rem; flex-shrink: 0;
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.15);
    border-radius: 8px;
  }
  .teleop-job-body { flex: 1; min-width: 0; }
  .teleop-job-title { font-size: clamp(1rem, 2.5vw, 1.2rem); font-weight: 800; color: var(--text-1); margin-bottom: 10px; line-height: 1.2; }
  .teleop-job-bullets { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px; }
  .teleop-job-bullets li { font-size: clamp(0.9rem, 1.8vw, 1rem); color: var(--text-2); line-height: 1.5; padding-left: 16px; position: relative; }
  .teleop-job-bullets li::before { content: ''; position: absolute; left: 0; top: 0.55em; width: 6px; height: 6px; border-radius: 50%; background: var(--amber); }
  .teleop-job-horizon { font-family: var(--font-mono); font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--amber); margin-top: 6px; display: block; }
  .teleop-close { text-align: center; border-top: 1px solid var(--border); padding-top: clamp(28px, 4vw, 40px); }
  .teleop-close-text { font-size: clamp(1.1rem, 2.5vw, 1.4rem); color: var(--text-1); line-height: 1.7; max-width: 54ch; margin: 0 auto 10px; }
  .teleop-close-text strong { color: var(--text-1); }
  .teleop-close .btn-primary { margin-top: 20px; }

  /* PILLARS */
  #pillars { padding: clamp(64px, 10vw, 120px) 0; border-top: 1px solid var(--border); }
  .pillars-intro { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 4vw, 48px); align-items: end; margin-bottom: clamp(36px, 5vw, 56px); }
  @media (max-width: 640px) { .pillars-intro { grid-template-columns: 1fr; } }
  .pillars-grid { display: grid; grid-template-columns: 3fr 2fr; gap: 10px; }
  @media (max-width: 640px) { .pillars-grid { grid-template-columns: 1fr; } }
  .pillar-card {
    position: relative; display: flex; flex-direction: column; gap: 14px;
    padding: clamp(24px, 3vw, 36px); border: 1px solid var(--border-mid);
    border-radius: var(--r-card); text-decoration: none; overflow: hidden; min-width: 0;
    transition: border-color 0.25s ease, transform 0.25s var(--ease-out), box-shadow 0.25s ease;
  }
  .pillar-card:hover { transform: translateY(-3px); }
  .pillar-01 { background: linear-gradient(145deg, rgba(245,158,11,0.07) 0%, rgba(15,23,42,0.4) 100%); }
  .pillar-01:hover { border-color: rgba(245,158,11,0.35); box-shadow: 0 14px 40px rgba(245,158,11,0.09); }
  .pillar-02 { background: linear-gradient(145deg, rgba(59,130,246,0.06) 0%, rgba(15,23,42,0.4) 100%); }
  .pillar-02:hover { border-color: rgba(59,130,246,0.35); box-shadow: 0 14px 40px rgba(59,130,246,0.09); }
  .pillar-03 { grid-column: 1 / -1; flex-direction: row; align-items: center; gap: clamp(20px, 3vw, 40px); background: linear-gradient(145deg, rgba(16,185,129,0.06) 0%, rgba(15,23,42,0.4) 100%); }
  .pillar-03:hover { border-color: rgba(16,185,129,0.35); box-shadow: 0 14px 40px rgba(16,185,129,0.09); }
  @media (max-width: 640px) { .pillar-03 { grid-column: 1; flex-direction: column; align-items: flex-start; } }
  .pillar-num { font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; letter-spacing: 0.1em; }
  .pillar-01 .pillar-num { color: var(--amber); }
  .pillar-02 .pillar-num { color: var(--blue); }
  .pillar-03 .pillar-num { color: var(--green); }
  .pillar-title { font-size: clamp(1.5rem, 3.5vw, 2rem); font-weight: 800; color: var(--text-1); letter-spacing: -0.02em; line-height: 1.2; }
  .pillar-body { font-size: clamp(1rem, 2vw, 1.1rem); color: var(--text-2); line-height: 1.7; flex: 1; }
  .pillar-link { display: inline-flex; align-items: center; gap: 6px; font-size: 1rem; font-weight: 600; margin-top: auto; }
  .pillar-01 .pillar-link { color: var(--amber); }
  .pillar-02 .pillar-link { color: var(--blue); }
  .pillar-03 .pillar-link { color: var(--green); }
  .pillar-03-main { flex: 1; display: flex; flex-direction: column; gap: 14px; }
  .pillar-icon-wrap { width: 52px; height: 52px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; border-radius: 14px; border: 1px solid rgba(16,185,129,0.2); background: rgba(16,185,129,0.08); }

  /* WINDOW / TAKEOFF */
  #window { padding: clamp(64px, 10vw, 120px) 0; border-top: 1px solid var(--border); }
  .takeoff-grid { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(32px, 5vw, 56px); align-items: start; }
  @media (max-width: 720px) { .takeoff-grid { grid-template-columns: 1fr; } }
  .takeoff-statement { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 800; line-height: 1.1; letter-spacing: -0.03em; color: var(--text-1); margin-bottom: 18px; }
  .takeoff-statement strong { color: var(--amber); }
  .takeoff-statement em { font-style: italic; }
  .takeoff-para { font-size: clamp(1rem, 2vw, 1.15rem); color: var(--text-2); line-height: 1.75; margin-bottom: 10px; }
  .takeoff-cards { display: flex; flex-direction: column; gap: 10px; }
  .scenario-outer { border-radius: 22px; padding: 2px; }
  .scenario-soft .scenario-outer { border: 1px solid rgba(59,130,246,0.2); background: rgba(59,130,246,0.04); }
  .scenario-hard .scenario-outer { border: 1px solid rgba(245,158,11,0.2); background: rgba(245,158,11,0.04); }
  .scenario-inner { border-radius: 20px; padding: clamp(18px, 2.5vw, 24px) clamp(20px, 2.5vw, 28px); background: var(--surface); box-shadow: inset 0 1px 0 rgba(255,255,255,0.04); border-top: 3px solid; }
  .scenario-soft .scenario-inner { border-color: var(--blue); }
  .scenario-hard .scenario-inner { border-color: var(--amber); }
  .scenario-tag { font-family: var(--font-mono); font-size: 1rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px; display: block; }
  .scenario-soft .scenario-tag { color: var(--blue); }
  .scenario-hard .scenario-tag { color: var(--amber); }
  .scenario-title { font-size: 1.4rem; font-weight: 700; color: var(--text-1); margin-bottom: 10px; }
  .scenario-body { font-size: 1.1rem; color: var(--text-2); line-height: 1.7; }

  /* STEPS */
  #steps { padding: clamp(64px, 10vw, 120px) 0; border-top: 1px solid var(--border); }
  .steps-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: clamp(36px, 5vw, 56px); }
  @media (max-width: 640px) { .steps-grid { grid-template-columns: 1fr; } }
  .step-outer { background: rgba(255,255,255,0.02); border: 1px solid var(--border-mid); border-radius: 22px; padding: 2px; min-width: 0; overflow: hidden; transition: border-color 0.25s ease, transform 0.25s var(--ease-out); }
  .step-outer:hover { border-color: var(--border-strong); transform: translateY(-3px); }
  .step-inner { background: var(--surface); border-radius: 20px; padding: clamp(22px, 3vw, 32px) clamp(22px, 3vw, 36px); height: 100%; box-shadow: inset 0 1px 0 rgba(255,255,255,0.04); display: flex; flex-direction: column; gap: 12px; box-sizing: border-box; }
  .step-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
  .step-num { font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; letter-spacing: 0.1em; color: var(--amber); }
  .step-cost { font-family: var(--font-mono); font-size: 1rem; font-weight: 700; color: var(--text-3); padding: 5px 12px; background: rgba(255,255,255,0.04); border: 1px solid var(--border); border-radius: 8px; white-space: nowrap; }
  .step-title { font-size: clamp(1.2rem, 2.5vw, 1.5rem); font-weight: 800; color: var(--text-1); letter-spacing: -0.02em; line-height: 1.2; }
  .step-body { font-size: clamp(0.95rem, 1.8vw, 1.05rem); color: var(--text-2); line-height: 1.7; flex: 1; }
  .step-caveat { font-size: 0.95rem; color: var(--text-3); line-height: 1.65; padding: 12px 16px; background: rgba(255,255,255,0.02); border-left: 2px solid var(--border-mid); border-radius: 0 6px 6px 0; }
  .step-link { display: inline-flex; align-items: center; gap: 6px; font-size: 1rem; font-weight: 600; color: var(--amber); margin-top: auto; text-decoration: none; }
  .steps-footer { display: flex; align-items: center; gap: 20px; margin-top: 18px; }
  .steps-footer-line { flex: 1; height: 1px; background: var(--border-mid); }
  .steps-footer-text { font-family: var(--font-mono); font-size: 0.9rem; color: var(--text-4); text-align: center; line-height: 1.6; }

  /* TIMELINE */
  #timeline { padding: clamp(64px, 10vw, 120px) 0; border-top: 1px solid var(--border); }
  .timeline-header { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(24px, 4vw, 48px); align-items: end; margin-bottom: clamp(36px, 5vw, 56px); }
  @media (max-width: 640px) { .timeline-header { grid-template-columns: 1fr; } }
  .timeline-track { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; position: relative; }
  .timeline-track::before { content: ''; position: absolute; top: 9px; left: 8px; right: 8px; height: 1px; background: linear-gradient(90deg, var(--amber), rgba(245,158,11,0.15)); }
  @media (max-width: 680px) { .timeline-track { grid-template-columns: 1fr 1fr; row-gap: 32px; } .timeline-track::before { display: none; } }
  @media (max-width: 400px) { .timeline-track { grid-template-columns: 1fr; row-gap: 28px; } }
  .timeline-item { padding: 0 12px 0 0; min-width: 0; overflow: hidden; }
  .timeline-dot-row { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; }
  .timeline-dot { width: 18px; height: 18px; flex-shrink: 0; border-radius: 50%; border: 3px solid var(--amber); background: var(--bg); position: relative; z-index: 1; }
  .timeline-dot.past { background: rgba(245,158,11,0.5); }
  .timeline-dot.now { background: var(--amber); box-shadow: 0 0 0 6px rgba(245,158,11,0.14); animation: dot-pulse 2s ease-in-out infinite; }
  @keyframes dot-pulse { 0%,100% { box-shadow: 0 0 0 6px rgba(245,158,11,0.14); } 50% { box-shadow: 0 0 0 10px rgba(245,158,11,0.07); } }
  .timeline-period { font-family: var(--font-mono); font-size: 1rem; font-weight: 700; color: var(--amber); letter-spacing: 0.05em; }
  .timeline-label { font-size: 1.2rem; font-weight: 700; color: var(--text-1); margin-bottom: 8px; }
  .timeline-desc { font-size: 1rem; color: var(--text-3); line-height: 1.65; }

  /* CHAPTERS */
  #chapters { padding: clamp(32px, 5vw, 56px) 0; border-top: 1px solid var(--border); }
  .chapters-header { margin-bottom: clamp(28px, 4vw, 48px); }
  .chapter-part-header { display: flex; align-items: baseline; gap: 12px; padding: 8px 0 6px; }
  .chapter-part-label { font-family: var(--font-mono); font-size: 1rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--amber); white-space: nowrap; }
  .chapter-part-title { font-size: 1.15rem; font-weight: 600; color: var(--text-3); }
  .chapters-list { border: 1px solid var(--border-mid); border-radius: var(--r-card); overflow: hidden; }
  .chapter-row { display: flex; align-items: center; gap: 16px; padding: clamp(14px, 2.5vw, 18px) clamp(16px, 3vw, 24px); text-decoration: none; border-bottom: 1px solid var(--border); transition: background 0.15s ease; color: inherit; }
  .chapter-row:last-child { border-bottom: none; }
  .chapter-row:hover { background: rgba(255,255,255,0.025); }
  .chapter-row-here { background: rgba(245,158,11,0.04); border-left: 3px solid var(--amber); }
  .chapter-row-here:hover { background: rgba(245,158,11,0.07); }
  .chapter-num { font-family: var(--font-mono); font-size: 1rem; font-weight: 700; color: var(--amber); letter-spacing: 0.06em; width: 36px; flex-shrink: 0; }
  .chapter-text { flex: 1; min-width: 0; }
  .chapter-title { font-size: clamp(1rem, 2.2vw, 1.2rem); font-weight: 700; color: var(--text-1); margin-bottom: 4px; }
  .chapter-desc { font-size: 0.92rem; color: var(--text-3); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .chapter-here-tag { display: inline-flex; align-items: center; gap: 6px; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--amber); background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25); border-radius: 6px; padding: 3px 8px; white-space: nowrap; flex-shrink: 0; }
  .chapter-here-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--amber); box-shadow: 0 0 6px var(--amber); animation: here-pulse 2s ease-in-out infinite; flex-shrink: 0; }
  @keyframes here-pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.7); } }

  /* BOOK PREORDER SECTION */
  .book-preorder-section { padding: clamp(48px, 8vw, 96px) 0; border-top: 1px solid var(--border); }

  /* CTA */
  /* ── REALITY SECTION ── */
  .reality-section { border-top: 1px solid var(--border); padding: clamp(48px, 8vw, 80px) 0; }
  .reality-inner { max-width: min(900px, 100%); margin: 0 auto; padding: 0 clamp(20px, 5vw, 48px); }
  .reality-heading {
    font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 900; line-height: 1.05;
    letter-spacing: -0.03em; color: var(--text-1); margin-bottom: clamp(28px, 4vw, 44px);
  }
  .reality-cols { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(16px, 3vw, 32px); }
  @media (max-width: 640px) { .reality-cols { grid-template-columns: 1fr; } }
  .reality-col { padding: clamp(20px, 3vw, 28px); border-radius: 16px; display: flex; flex-direction: column; gap: 0; }
  .reality-col-bad { background: rgba(239,68,68,0.04); border: 1px solid rgba(239,68,68,0.12); }
  .reality-col-good { background: rgba(16,185,129,0.04); border: 1px solid rgba(16,185,129,0.15); }
  .reality-col-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 14px; display: block;
  }
  .reality-col-bad .reality-col-label { color: #f87171; }
  .reality-col-good .reality-col-label { color: #34d399; }
  .reality-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }
  .reality-list li { font-size: clamp(0.92rem, 2vw, 1rem); color: var(--text-2); line-height: 1.55; padding-left: 0; }
  .reality-col-bad .reality-list li, .reality-col-good .reality-list li { padding-left: 16px; position: relative; }
  .reality-col-bad .reality-list li::before { content: ''; position: absolute; left: 0; top: 0.6em; width: 6px; height: 6px; border-radius: 50%; background: #f87171; }
  .reality-col-good .reality-list li::before { content: ''; position: absolute; left: 0; top: 0.6em; width: 6px; height: 6px; border-radius: 50%; background: #34d399; }

  /* MIDDLE SECTION */
  .middle-section { border-top: 1px solid var(--border); padding: clamp(56px, 9vw, 96px) 0; }
  .middle-inner { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(32px, 5vw, 64px); align-items: start; }
  @media (max-width: 680px) { .middle-inner { grid-template-columns: 1fr; } }
  .middle-heading { font-size: clamp(1.8rem, 4.5vw, 2.8rem); font-weight: 900; line-height: 1.08; letter-spacing: -0.03em; color: var(--text-1); margin-bottom: 24px; }
  .middle-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 14px; }
  .middle-list li { font-size: clamp(0.95rem, 2vw, 1.1rem); color: var(--text-2); line-height: 1.6; padding-left: 20px; position: relative; }
  .middle-list li::before { content: ''; position: absolute; left: 0; top: 0.62em; width: 8px; height: 1px; background: var(--amber); }
  .middle-offer { display: flex; flex-direction: column; gap: 16px; }
  .middle-offer-label { font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--amber); display: block; margin-bottom: 4px; }
  .middle-offer-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
  .middle-offer-list li { font-size: clamp(0.95rem, 2vw, 1.05rem); color: var(--text-2); line-height: 1.5; display: flex; align-items: center; gap: 10px; }
  .middle-btn { display: inline-flex; align-items: center; gap: 10px; padding: 14px 28px; background: var(--amber); color: #0a0a0a; font-family: 'Outfit', system-ui, sans-serif; font-weight: 800; font-size: 1.05rem; border-radius: var(--r-pill); text-decoration: none; transition: filter 0.2s ease, transform 0.2s var(--ease-spring); box-shadow: 0 4px 20px rgba(245,158,11,0.28); align-self: flex-start; }
  .middle-btn:hover { filter: brightness(1.08); transform: translateY(-2px); }
  .middle-fine { font-size: 0.82rem; color: var(--text-4); margin: 0; }

  /* BOOK PARTS */
  .book-parts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  @media (max-width: 760px) { .book-parts { grid-template-columns: 1fr; } }
  .book-part { padding: clamp(24px, 3vw, 36px); border: 1px solid var(--border-mid); border-radius: var(--r-card); display: flex; flex-direction: column; gap: 10px; transition: border-color 0.2s ease; }
  .book-part-1 { background: linear-gradient(145deg, rgba(245,158,11,0.06) 0%, rgba(15,23,42,0.4) 100%); }
  .book-part-1:hover { border-color: rgba(245,158,11,0.3); }
  .book-part-2 { background: linear-gradient(145deg, rgba(59,130,246,0.05) 0%, rgba(15,23,42,0.4) 100%); }
  .book-part-2:hover { border-color: rgba(59,130,246,0.3); }
  .book-part-3 { background: linear-gradient(145deg, rgba(16,185,129,0.05) 0%, rgba(15,23,42,0.4) 100%); }
  .book-part-3:hover { border-color: rgba(16,185,129,0.3); }
  .book-part-num { font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: var(--text-4); }
  .book-part-1 .book-part-num { color: var(--amber); }
  .book-part-2 .book-part-num { color: var(--blue); }
  .book-part-3 .book-part-num { color: var(--green); }
  .book-part-title { font-size: clamp(1.25rem, 2.8vw, 1.6rem); font-weight: 900; color: var(--text-1); letter-spacing: -0.02em; line-height: 1.15; margin: 0; }
  .book-part-sub { font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-3); letter-spacing: 0.04em; }
  .book-part-desc { font-size: clamp(0.9rem, 1.8vw, 1rem); color: var(--text-2); line-height: 1.65; flex: 1; }

  /* ── TRANSFORMATION SECTION ── */
  .transform-section { border-top: 1px solid var(--border); padding: clamp(48px, 8vw, 80px) 0; }
  .transform-inner { max-width: min(760px, 100%); margin: 0 auto; padding: 0 clamp(20px, 5vw, 48px); }
  .transform-heading {
    font-size: clamp(2.2rem, 6vw, 3.6rem); font-weight: 900; line-height: 1.0;
    letter-spacing: -0.03em; color: var(--text-1); margin-bottom: 20px;
  }
  .transform-heading em { font-style: italic; color: var(--amber); display: block; }
  .transform-sub {
    font-size: clamp(0.95rem, 2vw, 1.1rem); color: var(--text-2); line-height: 1.7;
    max-width: 60ch; margin-bottom: clamp(32px, 5vw, 48px);
  }
  .transform-outcomes { display: flex; flex-direction: column; gap: 24px; }
  .transform-outcome {
    display: flex; gap: 20px; align-items: flex-start;
    padding: 20px; border-radius: 14px;
    background: rgba(255,255,255,0.02); border: 1px solid var(--border-mid);
  }
  .transform-outcome-icon {
    font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 700;
    color: var(--amber); flex-shrink: 0; padding-top: 2px; min-width: 28px;
  }
  .transform-outcome strong { display: block; font-size: 1rem; font-weight: 700; color: var(--text-1); margin-bottom: 4px; }
  .transform-outcome p { font-size: clamp(0.85rem, 2vw, 0.92rem); color: var(--text-3); line-height: 1.6; margin: 0; }

  #act { padding: clamp(32px, 5vw, 56px) 0 clamp(48px, 8vw, 80px); border-top: 1px solid var(--border); }
  .cta-inner {
    position: relative; max-width: min(740px, 100%); margin: 0 auto; text-align: center;
    padding: clamp(40px, 6vw, 64px) clamp(24px, 5vw, 56px);
    border: 1px solid var(--border-mid); border-radius: 28px;
    background: linear-gradient(135deg, rgba(245,158,11,0.04) 0%, rgba(15,23,42,0.5) 100%);
    box-shadow: 0 0 60px rgba(245,158,11,0.05), 0 40px 80px rgba(0,0,0,0.28); overflow: hidden;
  }
  .cta-glow { position: absolute; pointer-events: none; width: 350px; height: 350px; border-radius: 50%; background: radial-gradient(circle, rgba(245,158,11,0.1) 0%, transparent 70%); top: -175px; left: 50%; transform: translateX(-50%); filter: blur(40px); }
  .cta-heading { font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 900; line-height: 1.08; letter-spacing: -0.03em; color: var(--text-1); margin-bottom: 16px; }
  .cta-sub { font-size: clamp(1rem, 2vw, 1.15rem); color: var(--text-2); line-height: 1.7; max-width: 46ch; margin: 0 auto 28px; }
  .cta-actions { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 36px; }
  .cta-divider { height: 1px; background: var(--border); margin: 0 calc(-1 * clamp(24px, 5vw, 56px)) 28px; }
  .cta-email-label { font-size: 1rem; color: var(--text-3); margin-bottom: 16px; display: block; }
  .edition-toggle { display: flex; justify-content: center; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
  .edition-opt { position: relative; }
  .edition-opt input[type="radio"] { position: absolute; opacity: 0; width: 0; height: 0; }
  .edition-opt span { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border: 1px solid var(--border-mid); border-radius: var(--r-pill); font-size: 0.88rem; font-weight: 700; color: var(--text-3); cursor: pointer; transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease; white-space: nowrap; }
  .edition-opt input[type="radio"]:checked + span { color: var(--amber); border-color: rgba(245,158,11,0.45); background: rgba(245,158,11,0.08); }
  .edition-opt span:hover { color: var(--text-1); border-color: var(--border-strong); }
  .edition-limited-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--amber); display: inline-block; flex-shrink: 0; }
  .email-form { display: flex; gap: 8px; max-width: min(420px, 100%); margin: 0 auto; }
  .email-input { flex: 1; min-width: 0; padding: 13px 18px; background: rgba(255,255,255,0.04); border: 1px solid var(--border-mid); border-radius: var(--r-pill); color: var(--text-1); font-family: 'Outfit', system-ui, sans-serif; font-size: 1rem; outline: none; transition: border-color 0.2s ease; }
  .email-input::placeholder { color: var(--text-4); }
  .email-input:focus { border-color: rgba(245,158,11,0.4); }
  .email-submit { flex-shrink: 0; padding: 11px 18px; background: var(--amber); color: #0a0a0a; font-family: 'Outfit', system-ui, sans-serif; font-weight: 800; font-size: 1.05rem; border: none; border-radius: var(--r-pill); cursor: pointer; white-space: nowrap; transition: filter 0.2s ease, transform 0.2s var(--ease-spring); }
  .email-submit:hover { filter: brightness(1.08); transform: translateY(-1px); }
  .email-submit:active { transform: scale(0.98); }
  @media (max-width: 420px) { .email-form { flex-direction: column; } .email-submit { width: 100%; } }

  .thanks-wrap { text-align: center; padding: clamp(32px, 5vw, 56px) clamp(20px, 5vw, 60px); }
  .thanks-text { font-size: clamp(1.1rem, 3vw, 1.5rem); color: var(--text-3); margin: 0; }

  .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }

  @media (prefers-reduced-motion: reduce) {
    .ambient-orb, .ac-dot, .timeline-dot.now, .chapter-here-dot { animation: none; }
  }
</style>
