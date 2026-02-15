<script>
  import { fly, fade } from 'svelte/transition';
  import { sections } from '$lib/data/blueprint.js';

  let step = 0;
  let answers = {
    housingCost: null,
    location: null,
    skills: [],
    goal: null
  };

  let showResults = false;
  let resultSections = [];

  const steps = [
    {
      question: "What's your current monthly housing cost?",
      key: 'housingCost',
      options: [
        { label: 'Under $1,000', value: 'low', icon: '1' },
        { label: '$1,000 - $2,000', value: 'mid', icon: '2' },
        { label: '$2,000 - $3,500', value: 'high', icon: '3' },
        { label: 'Over $3,500', value: 'very-high', icon: '4' },
      ]
    },
    {
      question: "Where are you currently based?",
      key: 'location',
      options: [
        { label: 'Urban / Metro', value: 'urban', icon: 'U' },
        { label: 'Suburban', value: 'suburban', icon: 'S' },
        { label: 'Rural', value: 'rural', icon: 'R' },
        { label: 'Nomadic / Flexible', value: 'nomadic', icon: 'N' },
      ]
    },
    {
      question: "Which skills do you already have?",
      key: 'skills',
      multi: true,
      options: [
        { label: 'Video / Content Creation', value: 'content', icon: 'V' },
        { label: 'Construction / Trades', value: 'trades', icon: 'C' },
        { label: 'Programming / Tech', value: 'tech', icon: 'T' },
        { label: 'None of these yet', value: 'none', icon: 'N' },
      ]
    },
    {
      question: "What's your primary goal?",
      key: 'goal',
      options: [
        { label: 'Slash housing costs NOW', value: 'housing', icon: 'H' },
        { label: 'Build income streams', value: 'income', icon: 'I' },
        { label: 'Digital sovereignty', value: 'digital', icon: 'D' },
        { label: 'Full independence roadmap', value: 'full', icon: 'F' },
      ]
    }
  ];

  function selectOption(key, value, multi = false) {
    if (multi) {
      if (value === 'none') {
        answers[key] = ['none'];
      } else {
        answers[key] = answers[key].filter(v => v !== 'none');
        if (answers[key].includes(value)) {
          answers[key] = answers[key].filter(v => v !== value);
        } else {
          answers[key] = [...answers[key], value];
        }
      }
    } else {
      answers[key] = value;
      // Auto-advance for non-multi steps
      setTimeout(() => {
        if (step < steps.length - 1) {
          step++;
        } else {
          calculateResults();
        }
      }, 300);
    }
  }

  function advanceMulti() {
    if (step < steps.length - 1) {
      step++;
    } else {
      calculateResults();
    }
  }

  function calculateResults() {
    const priority = [];

    // Always recommend economic-trap first
    priority.push({ slug: 'economic-trap', reason: 'Understand the macro landscape before acting', urgency: 'essential' });

    if (answers.goal === 'housing' || answers.goal === 'full' || answers.housingCost === 'high' || answers.housingCost === 'very-high') {
      priority.push({ slug: 'the-shouse', reason: `Your housing cost puts you in the overhead trap. The shouse chapter is your #1 lever.`, urgency: 'critical' });
      priority.push({ slug: 'physical-exit', reason: 'Learn the land acquisition strategy for rural relocation', urgency: 'high' });
    }

    if (answers.goal === 'income' || answers.goal === 'full' || answers.skills?.includes('content')) {
      priority.push({ slug: 'content-engine', reason: 'Build your content engine for recurring revenue', urgency: answers.goal === 'income' ? 'critical' : 'high' });
      priority.push({ slug: 'cash-engine', reason: 'Monetize with digital products and the $20 offer strategy', urgency: 'high' });
    }

    if (answers.goal === 'digital' || answers.goal === 'full' || answers.skills?.includes('tech')) {
      priority.push({ slug: 'digital-sovereignty', reason: 'Run local AI and decouple from cloud providers', urgency: answers.goal === 'digital' ? 'critical' : 'high' });
    }

    if (answers.skills?.includes('trades') || answers.goal === 'full') {
      priority.push({ slug: 'robotics', reason: 'Automate physical production with FarmBot and robotics', urgency: 'medium' });
    }

    // Always end with execute
    priority.push({ slug: 'execute', reason: 'Your personalized action steps and immediate directives', urgency: 'essential' });

    // Deduplicate
    const seen = new Set();
    resultSections = priority.filter(p => {
      if (seen.has(p.slug)) return false;
      seen.add(p.slug);
      return true;
    }).map(p => ({
      ...p,
      section: sections.find(s => s.slug === p.slug)
    })).filter(p => p.section);

    showResults = true;
  }

  function restart() {
    step = 0;
    answers = { housingCost: null, location: null, skills: [], goal: null };
    showResults = false;
    resultSections = [];
  }

  $: currentStep = steps[step];
  $: progressPct = showResults ? 100 : Math.round(((step) / steps.length) * 100);
</script>

<div class="configurator">
  <!-- Progress -->
  <div class="config-progress">
    <div class="config-progress-fill" style="width: {progressPct}%"></div>
  </div>

  {#if !showResults}
    <div class="config-step" in:fly={{ x: 40, duration: 300 }} out:fade={{ duration: 150 }}>
      <div class="step-counter">Step {step + 1} of {steps.length}</div>
      <h3 class="step-question">{currentStep.question}</h3>

      <div class="step-options">
        {#each currentStep.options as opt}
          {@const isSelected = currentStep.multi
            ? answers[currentStep.key]?.includes(opt.value)
            : answers[currentStep.key] === opt.value
          }
          <button
            class="config-option"
            class:config-option-selected={isSelected}
            on:click={() => selectOption(currentStep.key, opt.value, currentStep.multi)}
          >
            <span class="config-option-icon">{opt.icon}</span>
            <span class="config-option-label">{opt.label}</span>
            {#if isSelected}
              <svg class="config-check" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3 8L6.5 11.5L13 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            {/if}
          </button>
        {/each}
      </div>

      {#if currentStep.multi && answers[currentStep.key]?.length > 0}
        <button class="config-continue" on:click={advanceMulti}>
          Continue
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7H11M11 7L7.5 3.5M11 7L7.5 10.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
      {/if}

      {#if step > 0}
        <button class="config-back" on:click={() => step--}>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M9 6H3M3 6L5.5 3.5M3 6L5.5 8.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Back
        </button>
      {/if}
    </div>
  {:else}
    <div class="config-results" in:fly={{ y: 20, duration: 400 }}>
      <div class="results-header">
        <h3 class="results-title">Your Personalized Blueprint Path</h3>
        <p class="results-subtitle">Based on your situation, here's your recommended reading order:</p>
      </div>

      <div class="results-list">
        {#each resultSections as item, i}
          <a href="/blueprint/{item.slug}" class="result-card" style="animation-delay: {i * 80}ms">
            <div class="result-rank">{i + 1}</div>
            <div class="result-content">
              <div class="result-top">
                <span class="result-chapter">Ch. {item.section.number}</span>
                <span class="result-urgency urgency-{item.urgency}">{item.urgency}</span>
              </div>
              <h4 class="result-name">{item.section.title}</h4>
              <p class="result-reason">{item.reason}</p>
            </div>
            <svg class="result-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
        {/each}
      </div>

      <button class="config-restart" on:click={restart}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
        Retake Quiz
      </button>
    </div>
  {/if}
</div>

<style>
  .configurator {
    margin-top: 2rem;
  }

  .config-progress {
    height: 3px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 2px;
    margin-bottom: 2rem;
    overflow: hidden;
  }

  .config-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #10b981);
    border-radius: 2px;
    transition: width 0.4s ease;
  }

  .step-counter {
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.75rem;
  }

  .step-question {
    font-size: 1.4rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 1.5rem 0;
    letter-spacing: -0.02em;
  }

  .step-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }

  .config-option {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: rgba(30, 41, 59, 0.3);
    border: 1.5px solid rgba(148, 163, 184, 0.08);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
    text-align: left;
    position: relative;
  }

  .config-option:hover {
    border-color: rgba(245, 158, 11, 0.3);
    background: rgba(30, 41, 59, 0.5);
    transform: translateY(-1px);
  }

  .config-option-selected {
    border-color: #f59e0b;
    background: rgba(245, 158, 11, 0.08);
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.1);
  }

  .config-option-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(245, 158, 11, 0.08);
    color: #f59e0b;
    font-weight: 800;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
  }

  .config-option-selected .config-option-icon {
    background: rgba(245, 158, 11, 0.15);
  }

  .config-option-label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #cbd5e1;
  }

  .config-option-selected .config-option-label {
    color: #f1f5f9;
  }

  .config-check {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    color: #f59e0b;
  }

  .config-continue {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1.25rem;
    padding: 0.75rem 1.75rem;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: #0f172a;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
  }

  .config-continue:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
  }

  .config-back {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    margin-top: 0.75rem;
    padding: 0.5rem 1rem;
    background: none;
    border: none;
    color: #475569;
    font-size: 0.8rem;
    cursor: pointer;
    font-family: inherit;
    transition: color 0.2s;
  }

  .config-back:hover { color: #94a3b8; }

  /* Results */
  .results-header {
    margin-bottom: 1.5rem;
  }

  .results-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 0.5rem 0;
  }

  .results-subtitle {
    color: #64748b;
    font-size: 0.9rem;
    margin: 0;
  }

  .results-list {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .result-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 12px;
    text-decoration: none;
    transition: all 0.25s ease;
    animation: slideUp 0.4s ease forwards;
    opacity: 0;
  }

  @keyframes slideUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .result-card:hover {
    border-color: rgba(245, 158, 11, 0.2);
    background: rgba(30, 41, 59, 0.5);
    transform: translateX(4px);
  }

  .result-rank {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
    font-weight: 800;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
  }

  .result-content {
    flex: 1;
    min-width: 0;
  }

  .result-top {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
  }

  .result-chapter {
    font-size: 0.65rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .result-urgency {
    font-size: 0.55rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
  }

  .urgency-essential { background: rgba(245, 158, 11, 0.12); color: #f59e0b; }
  .urgency-critical { background: rgba(239, 68, 68, 0.12); color: #ef4444; }
  .urgency-high { background: rgba(59, 130, 246, 0.12); color: #3b82f6; }
  .urgency-medium { background: rgba(16, 185, 129, 0.12); color: #10b981; }

  .result-name {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.2rem 0;
  }

  .result-reason {
    font-size: 0.78rem;
    color: #64748b;
    margin: 0;
    line-height: 1.4;
  }

  .result-arrow {
    color: #334155;
    flex-shrink: 0;
    transition: all 0.2s;
  }

  .result-card:hover .result-arrow {
    color: #f59e0b;
    transform: translateX(3px);
  }

  .config-restart {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
    padding: 0.6rem 1.25rem;
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 10px;
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
  }

  .config-restart:hover {
    border-color: rgba(148, 163, 184, 0.15);
    color: #94a3b8;
  }

  @media (max-width: 640px) {
    .step-options {
      grid-template-columns: 1fr;
    }

    .step-question {
      font-size: 1.15rem;
    }
  }
</style>
