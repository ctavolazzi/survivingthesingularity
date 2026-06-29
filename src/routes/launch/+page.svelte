<script>
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import AuthorsEdition from '$lib/components/AuthorsEdition.svelte';
  import { audience } from '$lib/stores/audienceStore.js';

  let visible = false;
  onMount(() => {
    visible = true;
    if (!window.location.hash) {
      window.scrollTo({ top: 0, behavior: 'instant' });
    }
  });

  // Where/When are factual and constant across audiences.
  const whereA = 'The book launches at <strong>survivingthesingularity.com</strong> and on Amazon in August 2026, with wide availability across major ebook platforms. A signed, hand-bound Author\'s Edition (limited to 100 copies) is available to preorder here now. The goal is wide, cheap access. No membership. No paywall.';
  const whenA  = 'The full manuscript is in progress. A serialized preview (the Blueprint) is live now. The book launches August 2026 on Amazon and this site. Email subscribers get early access and chapter previews first. The limited Author\'s Edition is available to preorder now.';

  const audienceCopy = {
    individual: {
      subtitle: 'Where the book is going, why it exists, and what happens to the proceeds. No mystery, no hype. Just the honest plan.',
      whatA: '<em>Surviving the Singularity</em> is a practical book for people who want to understand what\'s actually happening with AI and act before the window closes. Not a doom manual. Not a utopian hype piece. A framework for building resilience on your own terms, written for real people facing real disruption.',
      whoA:  'Anyone who suspects the old playbook (career ladder, mortgage, retire at 65) was built for a world that no longer exists. Individuals, caregivers, workers facing automation, community organizers, and anyone who wants to understand what\'s coming and do something about it while there\'s still time.',
      whyNowA: 'Because the window is open today and won\'t be forever. Every major AI lab is on record saying systems that outperform experts in most knowledge-work domains are a question of <em>when</em>, not <em>if</em>. The people who prepare before the mainstream conversation catches up will have options the latecomers won\'t.',
      missionLead: 'This project has always been about more than a book. The proceeds fund two things with real-world stakes.',
      pilotEyebrow: 'The New Economy of Work',
      pilotTitle: 'Imagine Your Job Was Piloting a Robot',
      pilotLead: 'Not science fiction. Not a distant hypothetical. Teleoperated robots are already deployed in hospitals, factories, construction sites, and research labs. The missing piece is scale: the workforce trained to operate them.',
      pilotQuote: 'When automation eliminates a job, the honest answer isn\'t retraining for another job that will also be automated. It\'s building new roles that exist precisely because automation isn\'t good enough yet. Training people to fill them before someone else closes the door.',
      pilotContext1: 'Fully autonomous robots are not here yet. They fail at unscripted environments, edge cases, and tasks that require human judgment. That gap, between what robots can do autonomously and what they need a human pilot to do, is a real labor market. One that will grow for years before it shrinks.',
      pilotContext2: 'The retraining program funded by this book\'s proceeds is designed to fill that gap with real people who have skills worth paying for. Here\'s what those jobs look like:',
      pilotFooter1: 'These aren\'t invented categories. Teleoperation roles exist today in oil & gas inspection, surgical assistance, disaster response, and military applications. The civilian expansion of this model, enabled by affordable consumer hardware and 5G connectivity, is what we\'re building the training infrastructure for.',
      pilotFooter2: 'The Johnny Autoseed initiative is part of the same thesis: put robotics in the hands of communities, not just corporations, and train the people who live there to operate them. Food production, home care, infrastructure maintenance: all of it can be done by a distributed workforce of robot pilots working from their own homes.',
      ctaTitle: 'Be Part of the Launch',
      ctaBody: 'Get chapter previews before public release, updates on the teleoperation retraining program, and early access to the full book when it drops.',
      ctaSecondaryLabel: 'Read the Blueprint',
      ctaSecondaryHref: '/blueprint',
    },
    leader: {
      subtitle: 'What the AI transition means for your workforce, your organization, and the decisions that will look obvious in hindsight.',
      whatA: '<em>Surviving the Singularity</em> is a practical book for leaders who want a clear-eyed view of how AI is reshaping organizations, not just individual jobs. Not a doom manual. Not a utopian hype piece. A framework for building organizational resilience in a transition that is already underway, written for decision-makers who need signal, not noise.',
      whoA:  'Business leaders, operations managers, and HR teams responsible for workforces in transition. If you\'re running an organization and haven\'t had a clear-eyed conversation about which roles AI disrupts first and what the replacement labor market looks like, this book starts that conversation. Evidence, not talking points.',
      whyNowA: 'Because your competitors are having this conversation with or without you. Every major AI lab is on record saying systems that outperform experts in most knowledge-work domains are a question of <em>when</em>, not <em>if</em>. The organizations that prepare before the mainstream narrative catches up will have structural advantages the reactive ones will not.',
      missionLead: 'Revenue from the book funds two initiatives with direct economic implications. One builds local food resilience. The other builds the retraining pipeline for a new category of jobs your organization can hire from.',
      pilotEyebrow: 'The Workforce Opportunity',
      pilotTitle: 'The Gap Between Automation and Human Judgment Is a Labor Market',
      pilotLead: 'Your workforce isn\'t going away. Its job descriptions are. Every task that autonomous robots still fail at is a gap that requires a human operator. That gap is large today and will remain large through the end of the decade. Organizations that build pipelines into these roles now will have a structural advantage when the acceleration hits.',
      pilotQuote: 'The organizations that navigate this well aren\'t the ones that automate fastest. They\'re the ones that know exactly where human judgment is still irreplaceable, and build for it.',
      pilotContext1: 'Fully autonomous systems fail at the edges: judgment calls, unscripted environments, care situations. Every failure case requires a human operator. That surface is large today and will remain large through the end of the decade. It is a talent market your organization can hire into before it becomes competitive.',
      pilotContext2: 'The retraining program this book funds is building the training infrastructure for these roles. Here is the hiring surface:',
      pilotFooter1: 'These aren\'t speculative categories. Teleoperation roles exist today in oil & gas inspection, surgical assistance, disaster response, and logistics. The civilian expansion, enabled by affordable hardware and 5G connectivity, creates an entirely new hiring surface that most organizations haven\'t mapped yet.',
      pilotFooter2: 'The Johnny Autoseed initiative demonstrates the workforce model at community scale: distributed robot pilots working from home, providing food production, elder care, and infrastructure services. The same model applies inside organizations. Remote operators. Flexible deployment. No relocation required.',
      ctaTitle: 'Stay Ahead of the Transition',
      ctaBody: 'Get early access to the book and field notes on how organizations are navigating the shift. No noise, only signal.',
      ctaSecondaryLabel: 'See the Evidence',
      ctaSecondaryHref: '/evidence',
    },
    policy: {
      subtitle: 'A case for community-level preparation: the retraining infrastructure, the funding model, and the jobs that make distributed resilience possible.',
      whatA: '<em>Surviving the Singularity</em> is a practical book for community builders who want to understand what AI-driven economic disruption looks like at the local level, and what actions are available before the window closes. Concrete options for community resilience, not abstract theory.',
      whoA:  'Community organizers, local government planners, workforce development officers, and anyone responsible for economic resilience at the neighborhood or city level. The automation wave is a policy problem as much as a technology problem. Communities with a plan will have options. The ones that wait will just have outcomes.',
      whyNowA: 'Because displacement happens before policy catches up. Every major AI lab is on record saying systems that outperform experts in most knowledge-work domains are a question of <em>when</em>, not <em>if</em>. Communities that build resilience infrastructure now will have options when the transition accelerates. The ones that wait will be managing a crisis instead of a transition.',
      missionLead: 'Revenue from the book funds two community-scale initiatives. Both are designed to be open-sourced. Both are replicable by any community willing to do the work.',
      pilotEyebrow: 'Community-Scale Resilience',
      pilotTitle: 'A New Job Category Built for Your Community',
      pilotLead: 'Teleoperated robot pilots could be the first post-automation job category that is remote-friendly, requires weeks not years of training, pays living wages, and can be scaled to communities already hit by manufacturing or service sector decline. The training infrastructure for this workforce doesn\'t exist yet at scale. Building it is a policy intervention, not a market miracle.',
      pilotQuote: 'When automation eliminates a category of work, the honest response isn\'t retraining for another category that will also be automated. It\'s identifying the roles that exist precisely because full automation isn\'t here yet, and building the local infrastructure to fill them before someone else closes the door.',
      pilotContext1: 'Autonomous robots don\'t work without humans at the edges. They need operators for judgment calls, care decisions, and environments that can\'t be fully scripted. That gap is a workforce opportunity for communities willing to build the training infrastructure to staff it.',
      pilotContext2: 'The following roles exist today in specialized industries. The goal is to bring them into communities through the funded retraining program. Here is the workforce these jobs would create:',
      pilotFooter1: 'These aren\'t speculative categories. Teleoperation roles exist today in oil & gas inspection, surgical assistance, disaster response, and logistics. The civilian expansion, enabled by affordable consumer hardware and 5G connectivity, is what the retraining program funded by this book is designed to scale.',
      pilotFooter2: 'The Johnny Autoseed initiative is the proof of concept: distributed robot pilots providing food production, elder care, and infrastructure maintenance within their own community. The model is replicable. The open-source playbook is part of the deliverable.',
      ctaTitle: 'Build the Infrastructure Now',
      ctaBody: 'Communities that prepare for the transition will have options the ones that don\'t won\'t. Get chapter previews and updates on the teleoperation retraining program.',
      ctaSecondaryLabel: 'See the Evidence',
      ctaSecondaryHref: '/evidence',
    },
  };

  $: c = audienceCopy[$audience] ?? audienceCopy.individual;

  $: whyItems = [
    { q: 'What',     a: c.whatA },
    { q: 'Who',      a: c.whoA },
    { q: 'Why now',  a: c.whyNowA },
    { q: 'Where',    a: whereA },
    { q: 'When',     a: whenA },
  ];

  const pilotJobs = [
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
      title: 'Home Care Robot Operator',
      desc: 'Teleoperate a robot inside a client\'s home to cook meals, clean, do laundry, and assist with daily tasks. Your patient never sees a stranger. You work from anywhere.',
      tag: 'Disability Support',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
      title: 'Elder Care Companion Pilot',
      desc: 'Provide hands-on presence for elderly clients without leaving your home. Help them eat, move around, take medications, and stay connected to family, through a robot body in their living room.',
      tag: 'Elder Care',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
      title: 'Infrastructure Maintenance Tech',
      desc: 'Pilot a heavy-duty robot to inspect, clean, and repair public infrastructure: storm drains, utility tunnels, bridges, and roads. Work from a control station at home. No hard hat required.',
      tag: 'Public Works',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>`,
      title: 'Heavy-Lift Demolition Operator',
      desc: 'Remove manhole covers, perform structural demolition, and haul heavy debris using a robot with industrial-grade strength. You control it remotely. The robot takes the physical risk.',
      tag: 'Construction',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
      title: 'Hazmat & Emergency Response Pilot',
      desc: 'Enter chemical spills, collapsed buildings, or active fire zones through a robot. You stay safe. The robot handles the most dangerous first-response tasks so humans don\'t have to.',
      tag: 'Emergency Services',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>`,
      title: 'Last-Mile Delivery & Fulfillment',
      desc: 'Operate warehouse or delivery robots that handle complex, unscripted environments: apartment buildings, crowded sidewalks, tight storage rooms. Judgment calls that pure automation can\'t make yet.',
      tag: 'Logistics',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3h18v18H3z"/><path d="M3 9h18M9 21V9"/></svg>`,
      title: 'Precision Agriculture Operator',
      desc: 'Guide farm robots through delicate harvest tasks, pest inspection, and soil sampling that automated vision systems still get wrong. Farming without the physical toll.',
      tag: 'Agriculture',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>`,
      title: 'Space & Deep-Sea Ops Pilot',
      desc: 'The extreme environments humans can\'t survive: deep ocean floor, radiation zones, orbit. Telepresence robots are already operating in these domains. The jobs will scale as the hardware matures.',
      tag: 'Frontier Operations',
    },
  ];

  const moneyUses = [
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
      title: 'Fund Johnny Autoseed',
      body: 'A portion of every book sale goes directly into Johnny Autoseed, a food-security robotics initiative building closed-loop local food systems in Butte County, California. FarmBot-powered algae cultivation, lawn-to-food-garden conversions, and a community cooperative model designed to prove the concept then publish the open-source playbook so any community can replicate it.',
      link: 'https://johnnyautoseed.com',
      linkLabel: 'Learn about Johnny Autoseed',
    },
    {
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
      title: 'Community Retraining',
      body: 'Real economic disruption requires real alternatives, not platitudes. Part of the mission is funding hands-on retraining programs that teach people to operate teleoperated robots. Not hypothetical retraining: actual jobs that exist now and will grow as the hardware matures. The goal is to give displaced workers a genuine on-ramp to the new economy.',
      link: null,
      linkLabel: null,
    },
  ];
</script>

<svelte:head>
  <title>Book Launch Plan - Surviving the Singularity</title>
  <meta name="description" content="The book launch plan for Surviving the Singularity: the what, who, why, when, and where of the book, the publication roadmap, and what happens with the proceeds." />
</svelte:head>

{#if visible}
<div class="launch-page" in:fade={{ duration: 400 }}>

  <!-- HEADER -->
  <header class="launch-header">
    <p class="launch-label">Book Launch &amp; Mission</p>
    <h1 class="launch-title">The Plan</h1>
    <p class="launch-subtitle">{c.subtitle}</p>
  </header>

  <!-- THE 5 W's -->
  <section class="launch-section">
    <div class="section-eyebrow">The Book</div>
    <h2 class="section-title">What, Who, Why, Where, When</h2>
    <p class="section-lead">The five questions anyone should ask before they spend money or time on a book.</p>

    <div class="wh-grid">
      {#each whyItems as item}
        <div class="wh-card">
          <div class="wh-q">{item.q}</div>
          <p class="wh-a">{@html item.a}</p>
        </div>
      {/each}
    </div>
  </section>

  <!-- PUBLICATION PLAN -->
  <section class="launch-section">
    <div class="section-eyebrow">Publication Plan</div>
    <h2 class="section-title">How the Book Gets Made and Distributed</h2>

    <div class="pub-steps">
      <div class="pub-step pub-step--active">
        <div class="pub-step-num">1</div>
        <div class="pub-step-body">
          <h3>
            <a href="/blueprint">The Blueprint</a>
            <span class="pub-live-badge">Live now</span>
          </h3>
          <p>Eight chapters of the core framework, published free on this site. No paywall, no email required. This is not a teaser. It is the substance. The book goes deeper, but the Blueprint stands alone.</p>
        </div>
      </div>
      <div class="pub-step pub-step--active">
        <div class="pub-step-num">2</div>
        <div class="pub-step-body">
          <h3>
            <a href="/checklist">Early Access List</a>
            <span class="pub-live-badge">Open</span>
          </h3>
          <p>Subscribers get chapters before public release, updates on the launch timeline, and first access to the Author's Edition. No spam cadence. Only content that earned the send.</p>
        </div>
      </div>
      <div class="pub-step">
        <div class="pub-step-num">3</div>
        <div class="pub-step-body">
          <h3>Launch: August 2026</h3>
          <p>The full book launches August 2026 on Amazon and this site, with wide availability across major ebook platforms at the same time. Direct purchase on this site. The priority is access, not margin.</p>
        </div>
      </div>
      <div class="pub-step">
        <div class="pub-step-num">4</div>
        <div class="pub-step-body">
          <h3>Print on Demand</h3>
          <p>A physical edition via print-on-demand. No publisher middleman, no warehouse overhead, no minimum order. Anyone who wants a physical copy can get one at cost.</p>
        </div>
      </div>
      <div class="pub-step">
        <div class="pub-step-num">5</div>
        <div class="pub-step-body">
          <h3>Open Source Core</h3>
          <p>The research, data, and framework underlying the book will be published openly. If this argument is right, it should be replicable and verifiable. If it's wrong, people should be able to show why.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- WHAT WE DO WITH THE MONEY -->
  <section class="launch-section launch-section--alt">
    <div class="section-eyebrow">Revenue &amp; Mission</div>
    <h2 class="section-title">What Happens with the Money</h2>
    <p class="section-lead">{c.missionLead}</p>

    <div class="money-grid">
      {#each moneyUses as item}
        <div class="money-card">
          <div class="money-icon">{@html item.icon}</div>
          <h3 class="money-title">{item.title}</h3>
          <p class="money-body">{item.body}</p>
          {#if item.link}
            <a href={item.link} class="money-link" target="_blank" rel="noopener noreferrer">{item.linkLabel} →</a>
          {/if}
        </div>
      {/each}
    </div>
  </section>

  <!-- TELEOPERATION / PILOT A ROBOT -->
  <section class="launch-section">
    <div class="section-eyebrow">{c.pilotEyebrow}</div>
    <h2 class="section-title">{c.pilotTitle}</h2>
    <p class="section-lead">{c.pilotLead}</p>

    <div class="pilot-callout">
      <p class="pilot-pull">"{c.pilotQuote}"</p>
    </div>

    <p class="section-body">{c.pilotContext1}</p>
    <p class="section-body">{c.pilotContext2}</p>

    <div class="pilot-grid">
      {#each pilotJobs as job}
        <div class="pilot-card">
          <div class="pilot-card-header">
            <div class="pilot-icon">{@html job.icon}</div>
            <span class="pilot-tag">{job.tag}</span>
          </div>
          <h3 class="pilot-title">{job.title}</h3>
          <p class="pilot-desc">{job.desc}</p>
        </div>
      {/each}
    </div>

    <div class="pilot-footer-note">
      <p>{c.pilotFooter1}</p>
      <p>{c.pilotFooter2}</p>
    </div>
  </section>

  <!-- AUTHOR'S EDITION PREORDER -->
  <section class="launch-section" id="authors-edition">
    <div class="section-eyebrow">Limited Edition</div>
    <h2 class="section-title">The Author's Edition</h2>
    <p class="section-lead">
      100 copies. Hand-bound by the author, signed, individually numbered, and shipped with exclusive content not available anywhere else. If you want one, preorder now.
    </p>
    <AuthorsEdition />
  </section>

  <!-- CLOSING CTA -->
  <section class="launch-section launch-section--cta">
    <h2 class="cta-title">{c.ctaTitle}</h2>
    <p class="cta-body">{c.ctaBody}</p>
    <div class="cta-actions">
      <a href="/checklist" class="btn-primary">
        Get the Free Checklist
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <a href={c.ctaSecondaryHref} class="btn-secondary">{c.ctaSecondaryLabel}</a>
    </div>
  </section>

</div>
{/if}

<style>
  .launch-page {
    max-width: 860px;
    margin: 0 auto;
    padding: 2rem 1rem 4rem;
  }

  @media (min-width: 640px) {
    .launch-page { padding: 3rem 1.5rem 6rem; }
  }

  /* ── HEADER ── */
  .launch-header {
    margin-bottom: 4rem;
    text-align: center;
  }

  .launch-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #f59e0b;
    margin: 0 0 0.75rem;
    font-weight: 700;
    font-family: var(--font-primary, 'Inter', sans-serif);
  }

  .launch-title {
    font-size: clamp(2.5rem, 8vw, 4rem);
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 1rem;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }

  .launch-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.15rem);
    color: #94a3b8;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.65;
  }

  /* ── SECTIONS ── */
  .launch-section {
    margin-bottom: 5rem;
    padding-bottom: 5rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
  }

  .launch-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }

  .launch-section--alt {
    background: rgba(245, 158, 11, 0.03);
    border-radius: 16px;
    padding: 2.5rem 1rem;
    border: 1px solid rgba(245, 158, 11, 0.08);
    border-bottom: 1px solid rgba(245, 158, 11, 0.08);
    margin-left: -1rem;
    margin-right: -1rem;
  }

  @media (min-width: 640px) {
    .launch-section--alt {
      padding: 2.5rem 1.5rem;
      margin-left: -1.5rem;
      margin-right: -1.5rem;
    }
  }

  .section-eyebrow {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #f59e0b;
    font-weight: 700;
    margin-bottom: 0.6rem;
    font-family: var(--font-primary, 'Inter', sans-serif);
  }

  .section-title {
    font-size: clamp(1.4rem, 4vw, 2rem);
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 1rem;
    letter-spacing: -0.025em;
    line-height: 1.2;
  }

  .section-lead {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0 0 2.5rem;
    max-width: 680px;
  }

  .section-body {
    font-size: 0.97rem;
    color: #cbd5e1;
    line-height: 1.75;
    margin: 0 0 1.25rem;
    max-width: 720px;
  }

  /* ── 5 W's GRID ── */
  .wh-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .wh-card {
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    transition: border-color 0.2s ease;
  }

  .wh-card:hover {
    border-color: rgba(245, 158, 11, 0.2);
  }

  .wh-q {
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #f59e0b;
    min-width: 48px;
    padding-top: 0.15rem;
    font-family: var(--font-primary, 'Inter', sans-serif);
    flex-shrink: 0;
  }

  .wh-a {
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin: 0;
  }

  .wh-a :global(em) { color: #fbbf24; font-style: normal; }
  .wh-a :global(strong) { color: #f1f5f9; }

  /* ── PUBLICATION STEPS ── */
  .pub-steps {
    display: flex;
    flex-direction: column;
    gap: 0;
    position: relative;
  }

  .pub-steps::before {
    content: '';
    position: absolute;
    left: 17px;
    top: 24px;
    bottom: 24px;
    width: 2px;
    background: linear-gradient(to bottom, rgba(245, 158, 11, 0.4), rgba(245, 158, 11, 0.05));
  }

  .pub-step {
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
    padding: 1.25rem 0;
    position: relative;
  }

  .pub-step-num {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(245, 158, 11, 0.12);
    border: 2px solid rgba(245, 158, 11, 0.35);
    color: #f59e0b;
    font-size: 0.85rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
  }

  .pub-step-body {
    padding-top: 0.35rem;
    flex: 1;
  }

  .pub-step-body h3 {
    font-size: 1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .pub-step-body h3 a {
    color: inherit;
    text-decoration: none;
    transition: color 0.15s;
  }

  .pub-step-body h3 a:hover { color: #f59e0b; }

  .pub-step--active .pub-step-num {
    background: rgba(245, 158, 11, 0.18);
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.12);
  }

  .pub-live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.15rem 0.55rem;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 100px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #10b981;
    font-family: var(--font-primary, 'Inter', sans-serif);
    font-style: normal;
  }

  .pub-live-badge::before {
    content: '';
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #10b981;
    animation: live-pulse 2s ease-in-out infinite;
    flex-shrink: 0;
  }

  @keyframes live-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
  }

  .pub-step-body p {
    font-size: 0.92rem;
    color: #94a3b8;
    line-height: 1.65;
    margin: 0;
  }

  /* ── MONEY CARDS ── */
  .money-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  @media (min-width: 640px) {
    .money-grid { grid-template-columns: repeat(2, 1fr); }
  }

  .money-card {
    background: rgba(2, 6, 23, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 14px;
    padding: 1.5rem;
    transition: border-color 0.2s ease, transform 0.2s ease;
  }

  .money-card:hover {
    border-color: rgba(245, 158, 11, 0.25);
    transform: translateY(-2px);
  }

  .money-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 10px;
    color: #f59e0b;
    margin-bottom: 1rem;
  }

  .money-icon :global(svg) { width: 20px; height: 20px; }

  .money-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.65rem;
  }

  .money-body {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0 0 1rem;
  }

  .money-link {
    font-size: 0.85rem;
    font-weight: 600;
    color: #f59e0b;
    text-decoration: none;
    transition: color 0.15s ease;
  }

  .money-link:hover { color: #fbbf24; }

  /* ── PILOT CALLOUT ── */
  .pilot-callout {
    background: rgba(245, 158, 11, 0.06);
    border-left: 3px solid #f59e0b;
    border-radius: 0 10px 10px 0;
    padding: 1.25rem 1.5rem;
    margin: 0 0 2rem;
  }

  .pilot-pull {
    font-size: 1rem;
    color: #e2e8f0;
    line-height: 1.7;
    margin: 0;
    font-style: italic;
  }

  /* ── PILOT JOBS GRID ── */
  .pilot-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    margin: 2rem 0;
  }

  @media (min-width: 540px) {
    .pilot-grid { grid-template-columns: repeat(2, 1fr); }
  }

  @media (min-width: 720px) {
    .pilot-grid { grid-template-columns: repeat(3, 1fr); }
  }

  .pilot-card {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 12px;
    padding: 1.25rem;
    transition: border-color 0.2s ease, background 0.2s ease;
  }

  .pilot-card:hover {
    border-color: rgba(245, 158, 11, 0.2);
    background: rgba(30, 41, 59, 0.6);
  }

  .pilot-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
  }

  .pilot-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 9px;
    color: #f59e0b;
    flex-shrink: 0;
  }

  .pilot-icon :global(svg) { width: 16px; height: 16px; }

  .pilot-tag {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    font-family: var(--font-primary, 'Inter', sans-serif);
  }

  .pilot-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.5rem;
    line-height: 1.3;
  }

  .pilot-desc {
    font-size: 0.86rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
  }

  /* ── PILOT FOOTER NOTE ── */
  .pilot-footer-note {
    border-top: 1px solid rgba(148, 163, 184, 0.08);
    padding-top: 1.5rem;
    margin-top: 0.5rem;
  }

  .pilot-footer-note p {
    font-size: 0.92rem;
    color: #64748b;
    line-height: 1.7;
    margin: 0 0 1rem;
  }

  .pilot-footer-note p:last-child { margin-bottom: 0; }

  /* ── CLOSING CTA ── */
  .launch-section--cta {
    text-align: center;
    border-bottom: none;
  }

  .cta-title {
    font-size: clamp(1.5rem, 5vw, 2.25rem);
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 1rem;
    letter-spacing: -0.025em;
  }

  .cta-body {
    font-size: 1rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0 auto 2rem;
    max-width: 520px;
  }

  .cta-actions {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  @media (min-width: 480px) {
    .cta-actions { flex-direction: row; justify-content: center; }
  }

  /* ── BUTTONS ── */
  .btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.75rem 1.5rem;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 700;
    font-size: 0.9rem;
    border-radius: 9px;
    text-decoration: none;
    transition: background 0.15s ease, transform 0.15s ease;
    letter-spacing: 0.01em;
  }

  .btn-primary:hover {
    background: #fbbf24;
    transform: translateY(-1px);
  }

  .btn-secondary {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    background: rgba(245, 158, 11, 0.08);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.25);
    font-weight: 600;
    font-size: 0.9rem;
    border-radius: 9px;
    text-decoration: none;
    transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
  }

  .btn-secondary:hover {
    background: rgba(245, 158, 11, 0.14);
    border-color: rgba(245, 158, 11, 0.45);
    transform: translateY(-1px);
  }

  @media (prefers-reduced-motion: reduce) {
    .pub-live-badge::before { animation: none; }
    .money-card:hover,
    .wh-card:hover { transform: none; }
    .btn-primary:hover,
    .btn-secondary:hover { transform: none; }
  }
</style>
