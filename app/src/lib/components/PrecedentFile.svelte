<script>
  import { open, rest, total } from '$lib/precedents.js';

  let active = $state(0);
  /** @type {HTMLButtonElement[]} */
  let tabEls = $state([]);

  /** @param {KeyboardEvent} e */
  function onkeydown(e) {
    const delta = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
    if (!delta) return;
    e.preventDefault();
    active = (active + delta + open.length) % open.length;
    tabEls[active]?.focus();
  }
</script>

<section class="band" id="precedent">
  <div class="wrap">
    <p class="kicker">The Precedent File</p>
    <!-- The count is derived. This is the sentence the live site got wrong. -->
    <h2 class="sec-h2">
      {total} times, people met a machine that changed everything.
    </h2>
    <p class="sec-lede">
      Every case is sourced so you can check the work. Three of them are open
      below, in full, exactly as they appear in the book. Nothing here is a
      summary written for a sales page.
    </p>

    <div class="tabs" role="tablist" aria-label="Sample precedents">
      {#each open as p, i (p.id)}
        <button
          bind:this={tabEls[i]}
          class="tab"
          class:is-active={active === i}
          role="tab"
          aria-selected={active === i}
          aria-controls="panel-{p.id}"
          id="tab-{p.id}"
          tabindex={active === i ? 0 : -1}
          onclick={() => (active = i)}
          {onkeydown}
        >
          <span class="tab-id">{p.id}</span>
          <span class="tab-t">{p.shortTitle}</span>
        </button>
      {/each}
    </div>

    {#each open as p, i (p.id)}
      {#if active === i}
        <article
          class="panel"
          role="tabpanel"
          id="panel-{p.id}"
          aria-labelledby="tab-{p.id}"
        >
          <h3 class="panel-h">
            {p.title}
            <span class="panel-date">{p.date}</span>
          </h3>

          {#each p.body as para}
            <!-- Book prose carries its own emphasis markup. It is authored
                 content from the manuscript, not user input. -->
            <p>{@html para}</p>
          {/each}

          <p class="pull"><strong>The rule.</strong> {p.rule}</p>

          <p class="panel-cut">
            The mechanism, the practice, and the sources continue in the book.
          </p>
        </article>
      {/if}
    {/each}

    <div class="rest">
      <p class="rest-h">{rest.length} more, every one sourced.</p>
      <ul class="rest-list">
        {#each rest as p (p.id)}
          <li>
            <span class="pid">{p.id}</span>
            {p.title}
            <i>{p.date}</i>
          </li>
        {/each}
      </ul>
    </div>
  </div>
</section>

<style>
  .tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
  }

  .tab {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 12px 18px;
    cursor: pointer;
    font-family: var(--sans);
    text-align: left;
    transition: border-color 140ms ease, background 140ms ease;
  }
  .tab:hover { border-color: var(--border-2); }
  .tab.is-active {
    background: var(--accent-dim);
    border-color: rgba(245, 158, 11, 0.45);
  }

  .tab-id {
    font: 600 11.5px/1 var(--mono);
    letter-spacing: 0.08em;
    color: var(--text-3);
  }
  .tab.is-active .tab-id { color: var(--accent); }
  .tab-t { font-size: 14.5px; font-weight: 500; color: var(--text); }

  .panel {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: clamp(24px, 3.5vw, 40px);
  }

  .panel-h {
    font: 600 clamp(20px, 2.6vw, 27px)/1.25 var(--serif);
    letter-spacing: -0.01em;
    margin: 0 0 22px;
  }
  .panel-date {
    display: block;
    font: 400 13px/1.4 var(--mono);
    letter-spacing: 0.03em;
    color: var(--text-3);
    margin-top: 7px;
  }

  .panel p {
    font-size: 16.5px;
    line-height: 1.72;
    color: var(--text-2);
    max-width: 72ch;
    margin: 0 0 18px;
  }
  /* :global is required because this markup arrives through {@html}, so the
     scoping attribute is never applied to it. */
  .panel p :global(em) { color: var(--text); font-style: italic; }
  .panel p :global(strong) { color: var(--text); font-weight: 600; }

  /* Two classes plus an element beats `.panel p`. No !important needed. */
  .panel p.pull {
    border-left: 3px solid var(--accent);
    background: var(--accent-dim);
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin: 26px 0 20px;
    color: var(--text);
  }
  .panel p.pull strong { color: var(--accent-hi); }

  .panel p.panel-cut {
    font: 400 14px/1.5 var(--mono);
    color: var(--text-3);
    border-top: 1px solid var(--border);
    padding-top: 16px;
    margin-bottom: 0;
  }

  .rest { margin-top: 36px; }

  .rest-h {
    font: 600 15px/1 var(--sans);
    color: var(--text);
    margin: 0 0 18px;
  }

  .rest-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: var(--r);
    overflow: hidden;
  }
  .rest-list li {
    background: var(--surface);
    padding: 12px 16px;
    font-size: 14.5px;
    color: var(--text-2);
    display: flex;
    align-items: baseline;
    gap: 11px;
  }
  .rest-list i {
    font-style: normal;
    color: var(--text-3);
    font-family: var(--mono);
    font-size: 12.5px;
    margin-left: auto;
    white-space: nowrap;
    padding-left: 12px;
  }
  .pid {
    font: 600 11.5px/1 var(--mono);
    color: var(--text-3);
    background: var(--surface-3);
    border-radius: 4px;
    padding: 4px 6px;
    flex: 0 0 auto;
  }

  @media (max-width: 700px) {
    .rest-list { grid-template-columns: 1fr; }

    /* The date is nowrap and pushed right by margin-left:auto, which at narrow
       widths runs it under the rounded container's overflow:hidden and clips it
       instead of overflowing the page. So it never trips a scrollWidth check,
       it just quietly becomes unreadable. Give it its own line instead. */
    .rest-list li { flex-wrap: wrap; }
    .rest-list i {
      flex-basis: 100%;
      margin-left: 0;
      padding-left: 31px;
      white-space: normal;
      font-size: 12px;
      margin-top: 3px;
    }
  }
  @media (max-width: 460px) {
    .tabs { flex-direction: column; }
    .tab { width: 100%; }
  }
  @media (prefers-reduced-motion: reduce) {
    .tab { transition: none; }
  }
</style>
