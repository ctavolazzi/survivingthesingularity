<script>
  import EmailGate from '$lib/components/EmailGate.svelte';

  // First 3 are the free teaser; the rest unlock after email.
  const teaser = [
    {
      n: '01',
      title: 'Audit your single points of failure',
      body: 'List every essential — food, water, power, income, shelter — that depends on one provider you do not control. That list is your real risk map.'
    },
    {
      n: '02',
      title: 'Run one local AI model this week',
      body: 'Install Ollama, pull a small model, and prove you can get useful answers with no cloud, no subscription, no permission. The tools are already free.'
    },
    {
      n: '03',
      title: 'Calculate your freedom number',
      body: 'The monthly cost to cover your essentials if your income vanished tomorrow. Write it down. Everything else is a campaign to lower it.'
    }
  ];

  const gated = [
    {
      n: '04',
      title: 'Start a skill that compounds',
      body: 'Pick one high-leverage skill — AI tooling, fabrication, growing food — and commit 30 minutes a day. Compounding beats intensity.'
    },
    {
      n: '05',
      title: 'Build a 30-day food buffer',
      body: 'Not prepping. Decoupling. A month of staples removes the weekly dependency and the anxiety that rides with it.'
    },
    {
      n: '06',
      title: 'Open a second income that needs no permission',
      body: 'A digital product, a service, content you own. The first dollar matters more than the amount — it proves the channel exists.'
    },
    {
      n: '07',
      title: 'Map your water and power',
      body: 'Know where they come from and what a 72-hour interruption actually looks like for you. You cannot harden what you have not mapped.'
    },
    {
      n: '08',
      title: 'Learn to grow one thing you eat',
      body: 'A single pot of something edible is a proof of concept for food autonomy. Start absurdly small. Just start.'
    },
    {
      n: '09',
      title: 'Price out a physical exit',
      body: 'Land cost per acre in three regions you would actually move to. Turn a vague someday into three real numbers.'
    },
    {
      n: '10',
      title: 'Automate one recurring task with AI',
      body: 'Reclaim the hours and build the muscle of delegating to machines you control — before you are forced to rent ones you do not.'
    },
    {
      n: '11',
      title: 'Cut fixed monthly obligations by 10%',
      body: 'Every dollar of recurring cost you remove permanently lowers your freedom number. Fixed costs are the enemy of optionality.'
    },
    {
      n: '12',
      title: 'Find three people building the same way',
      body: 'Independence is not isolation. A small group going the same direction is the difference between a phase and a life.'
    }
  ];
</script>

<svelte:head>
  <title>The Singularity Readiness Checklist - Surviving the Singularity</title>
  <meta name="description" content="12 concrete moves to build material independence before AGI. A free, actionable checklist." />
</svelte:head>

<div class="checklist-page">
  <header class="cl-header">
    <p class="cl-eyebrow">Free · Actionable</p>
    <h1 class="cl-title">The Singularity Readiness Checklist</h1>
    <p class="cl-lede">
      Twelve concrete moves to build real independence before AGI reprices everything.
      No theory. No fluff. Things you can start this week.
    </p>
  </header>

  <EmailGate
    storageKey="checklist"
    source="checklist"
    headline="Unlock the full 12-point checklist"
    sub="You've seen the first three. Enter your email and the other nine open right here on this page."
    buttonText="Unlock the Checklist"
  >
    <!-- Teaser: always visible -->
    <ol class="cl-list">
      {#each teaser as item}
        <li class="cl-item">
          <span class="cl-num">{item.n}</span>
          <div class="cl-body">
            <h2 class="cl-item-title">{item.title}</h2>
            <p class="cl-item-text">{item.body}</p>
          </div>
        </li>
      {/each}
    </ol>

    <!-- Gated: revealed after unlock -->
    <ol class="cl-list cl-list-gated" slot="gated" start="4">
      {#each gated as item}
        <li class="cl-item">
          <span class="cl-num">{item.n}</span>
          <div class="cl-body">
            <h2 class="cl-item-title">{item.title}</h2>
            <p class="cl-item-text">{item.body}</p>
          </div>
        </li>
      {/each}

      <li class="cl-closer">
        <p>That's the checklist. Now go deeper.</p>
        <div class="cl-closer-actions">
          <a href="/blueprint" class="cl-btn-primary">Read the Full Blueprint</a>
          <a href="/book" class="cl-btn-secondary">About the Book</a>
        </div>
      </li>
    </ol>
  </EmailGate>

  <p class="cl-disclaimer">
    The information here is a starting point for your own research, not a professional recommendation.
    <a href="/disclaimer">Read our terms &amp; disclaimers</a>.
  </p>
</div>

<style>
  .checklist-page {
    max-width: 720px;
    margin: 0 auto;
    padding: 3rem 1.25rem 5rem;
  }

  .cl-header {
    text-align: center;
    margin-bottom: 2.5rem;
  }

  .cl-eyebrow {
    font-family: var(--font-primary, 'JetBrains Mono', monospace);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0 0 0.85rem;
  }

  .cl-title {
    font-size: clamp(1.8rem, 5vw, 2.6rem);
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0 0 1rem;
  }

  .cl-lede {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0 auto;
    max-width: 540px;
  }

  .cl-list {
    list-style: none;
    padding: 0;
    margin: 0 0 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .cl-list-gated { margin-top: 1rem; }

  .cl-item {
    display: flex;
    gap: 1rem;
    padding: 1.1rem 1.25rem;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 12px;
  }

  .cl-num {
    flex-shrink: 0;
    font-family: var(--font-primary, 'JetBrains Mono', monospace);
    font-size: 0.95rem;
    font-weight: 700;
    color: #f59e0b;
    line-height: 1.6;
  }

  .cl-item-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.35rem;
    line-height: 1.3;
  }

  .cl-item-text {
    font-size: 0.94rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
  }

  .cl-closer {
    text-align: center;
    padding: 1.75rem 1.25rem;
    background: rgba(245, 158, 11, 0.05);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 12px;
    margin-top: 0.5rem;
  }
  .cl-closer p {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 1rem;
  }
  .cl-closer-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .cl-btn-primary,
  .cl-btn-secondary {
    padding: 0.65rem 1.3rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.9rem;
    text-decoration: none;
    transition: transform 0.15s ease, opacity 0.15s ease, border-color 0.15s ease;
  }
  .cl-btn-primary {
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
  }
  .cl-btn-primary:hover { transform: translateY(-1px); opacity: 0.92; }
  .cl-btn-secondary {
    color: #e2e8f0;
    border: 1px solid rgba(148, 163, 184, 0.25);
  }
  .cl-btn-secondary:hover { border-color: rgba(245, 158, 11, 0.4); }

  .cl-disclaimer {
    text-align: center;
    font-size: 0.8rem;
    color: #64748b;
    margin: 2.5rem 0 0;
  }
  .cl-disclaimer a { color: #94a3b8; text-decoration: underline; text-underline-offset: 2px; }
</style>
