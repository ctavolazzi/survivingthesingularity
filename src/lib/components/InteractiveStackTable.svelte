<script>
  import { slide } from 'svelte/transition';

  const items = [
    {
      q: 'What might replace wage-only income dependence?',
      category: 'Labor & Time',
      color: '#f59e0b',
      a: `One framework the author has explored: matching physical labor to biology rather than desk hours. Open-source robotics projects (like Mobile Aloha, FarmBot, and others) aim to automate repetitive physical tasks, though at research or early-commercial stage, costs and capabilities vary enormously. None of this is a prescription; it's a domain worth watching.`,
      tags: ['Research stage', 'Costs vary widely', 'Not a recommendation'],
      link: null,
    },
    {
      q: 'What are some alternatives to fiat savings accounts?',
      category: 'Capital Preservation',
      color: '#3b82f6',
      a: `Inflation erodes purchasing power in savings accounts; that much is well-documented. Some people explore hard assets (land, tools, equipment), productive assets (small businesses, digital products), or inflation-hedged instruments. Each carries its own risks and legal/tax considerations.`,
      tags: ['Not financial advice', 'Consult a licensed advisor', 'Individual situation varies'],
      link: null,
    },
    {
      q: 'What might replace reliance on centralized safety nets?',
      category: 'Resilience Planning',
      color: '#10b981',
      a: `Social safety nets have structural funding challenges in many countries. Some people find it useful to think about layered personal resilience: paid-off shelter, food production capacity, community relationships, and diversified income. Local laws and codes vary enormously.`,
      tags: ['Not a substitute for insurance', 'Local laws vary', 'Consult professionals'],
      link: null,
    },
    {
      q: 'What are the trade-offs of local vs. cloud AI?',
      category: 'Intelligence Tools',
      color: '#8b5cf6',
      a: `Cloud AI is convenient but carries dependency risks: pricing changes, terms changes, availability gaps. Running open-weight models locally on consumer hardware (e.g., Llama, Mistral) is an option some find useful for privacy and continuity. Hardware capability and model quality change rapidly; any specific claim about what hardware can run what model today may be outdated within months. Evaluate for your own use case.`,
      tags: ['Landscape changes rapidly', 'No specific endorsement', 'Verify for your context'],
      link: null,
    },
    {
      q: 'How might content creation factor into a resilience plan?',
      category: 'Information & Reach',
      color: '#f97316',
      a: `Creator platforms offer one possible avenue for sharing knowledge and building an audience, which can eventually support other economic activity. Most creators earn little or nothing, especially early on. The author's "One-Hour Rule" is a heuristic, not a guarantee: if something took you more than an hour to learn, it might be worth teaching. Results vary widely and most depend on factors outside your control. Not a business plan.`,
      tags: ['Most creators earn little', 'Results vary widely', 'Not income advice'],
      link: null,
    },
  ];

  let openIndex = -1;

  function toggle(i) {
    openIndex = openIndex === i ? -1 : i;
  }
</script>

<div class="faq-wrap">
  {#each items as item, i}
    <div class="faq-item" class:faq-open={openIndex === i}>
      <button
        class="faq-trigger"
        on:click={() => toggle(i)}
        aria-expanded={openIndex === i}
      >
        <div class="faq-trigger-left">
          <span class="faq-category" style="color: {item.color}; border-color: {item.color}30; background: {item.color}10">{item.category}</span>
          <span class="faq-question">{item.q}</span>
        </div>
        <span class="faq-icon" class:faq-icon-open={openIndex === i} aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M4.5 6.75L9 11.25L13.5 6.75" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </button>

      {#if openIndex === i}
        <div class="faq-body" transition:slide={{ duration: 220 }}>
          <div class="faq-accent" style="background: {item.color}"></div>
          <div class="faq-content">
            <p class="faq-answer">{item.a}</p>
            <div class="faq-tags">
              {#each item.tags as tag}
                <span class="faq-tag">{tag}</span>
              {/each}
            </div>
          </div>
        </div>
      {/if}
    </div>
  {/each}
</div>

<style>
  .faq-wrap {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .faq-item {
    border: 1px solid rgba(148, 163, 184, 0.07);
    border-radius: 12px;
    overflow: hidden;
    transition: border-color 0.2s ease;
    background: rgba(15, 23, 42, 0.4);
  }

  .faq-item:hover {
    border-color: rgba(148, 163, 184, 0.14);
  }

  .faq-open {
    border-color: rgba(148, 163, 184, 0.18) !important;
    background: rgba(30, 41, 59, 0.5);
  }

  .faq-trigger {
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
    font-family: inherit;
    padding: 1.1rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    text-align: left;
  }

  .faq-trigger:focus-visible {
    outline: 2px solid #f59e0b;
    outline-offset: -2px;
    border-radius: 11px;
  }

  .faq-trigger-left {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    min-width: 0;
  }

  .faq-category {
    display: inline-block;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.18rem 0.5rem;
    border-radius: 4px;
    border: 1px solid;
    font-family: var(--font-primary);
    width: fit-content;
  }

  .faq-question {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e2e8f0;
    line-height: 1.4;
  }

  .faq-icon {
    flex-shrink: 0;
    color: #334155;
    transition: transform 0.25s ease, color 0.2s ease;
    display: flex;
    align-items: center;
  }

  .faq-trigger:hover .faq-icon {
    color: #dde4ef;
  }

  .faq-icon-open {
    transform: rotate(180deg);
    color: #f59e0b;
  }

  .faq-body {
    display: flex;
    gap: 0;
    border-top: 1px solid rgba(148, 163, 184, 0.06);
  }

  .faq-accent {
    width: 3px;
    flex-shrink: 0;
    opacity: 0.6;
  }

  .faq-content {
    padding: 1.1rem 1.25rem;
    flex: 1;
  }

  .faq-answer {
    font-size: 0.88rem;
    color: #dde4ef;
    line-height: 1.75;
    margin: 0 0 1rem 0;
  }

  .faq-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .faq-tag {
    font-size: 0.82rem;
    font-weight: 600;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    background: rgba(148, 163, 184, 0.06);
    color: #dde4ef;
    border: 1px solid rgba(148, 163, 184, 0.08);
    font-family: var(--font-primary);
    letter-spacing: 0.03em;
  }

  .faq-footer-note {
    margin-top: 1rem;
    font-size: 0.82rem;
    color: #dde4ef;
    line-height: 1.6;
    font-style: italic;
    max-width: 720px;
  }

  .faq-footer-note a {
    color: #dde4ef;
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  .faq-footer-note a:hover {
    color: #f59e0b;
  }

  @media (max-width: 640px) {
    .faq-trigger {
      padding: 1rem;
    }
    .faq-content {
      padding: 1rem;
    }
  }
</style>
