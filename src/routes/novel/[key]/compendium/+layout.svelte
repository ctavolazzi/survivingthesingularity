<script>
  // The compendium. The front page is one list. An entry page has the list of
  // all entries down the side on a wide screen, and after the entry on a phone.
  //
  // Reading rules for every page in here: one typeface (Inter) for everything
  // but titles and quotations, text lines no longer than about 62 characters,
  // and one left edge for labels and one for what they label.
  import { page } from '$app/stores';
  import ReaderControls from '../ReaderControls.svelte';

  export let data;

  $: currentId = $page.params.entryId ?? null;
</script>

<div class="compendium" class:on-entry={currentId}>
  <div class="bar">
    <p class="crumbs">
      <a href={data.base}>The novel</a>
      <span aria-hidden="true">/</span>
      {#if currentId}<a href="{data.base}/compendium">Compendium</a>{:else}<span class="here">Compendium</span>{/if}
    </p>
    <ReaderControls />
  </div>

  {#if currentId}
    <nav class="tree" aria-label="All entries">
      {#each data.tree as topic}
        <section>
          <h2>{topic.name}</h2>
          <ul>
            {#each topic.entries as entry}
              <li>
                <a href={entry.href} class:current={entry.id === currentId} aria-current={entry.id === currentId ? 'page' : undefined}>
                  {entry.name}
                </a>
              </li>
            {/each}
          </ul>
        </section>
      {/each}
    </nav>
  {/if}

  <div class="pane">
    <slot />
  </div>
</div>

<style>
  .compendium {
    /* Secondary words, a raised surface, and the surface under the pointer. */
    --soft: color-mix(in srgb, var(--ink) 72%, var(--bg));
    --panel: color-mix(in srgb, var(--ink) 5%, var(--bg));
    --hover: color-mix(in srgb, var(--ink) 9%, var(--bg));
    /* The label column, shared by the front page and the facts on an entry. */
    --label: 168px;
    max-width: 780px;
    margin: 0 auto;
    padding: 8px 24px 112px;
    font-family: Inter, system-ui, sans-serif;
    font-feature-settings: 'tnum';
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    row-gap: 36px;
  }
  .bar { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
  .crumbs { margin: 0; font-size: 16px; color: var(--soft); }
  .crumbs a { color: var(--soft); text-decoration: underline; text-decoration-color: var(--rule); text-underline-offset: 4px; }
  .crumbs a:hover { color: var(--accent); text-decoration-color: currentColor; }
  .crumbs span { margin: 0 4px; }
  .crumbs .here { margin: 0; color: var(--ink); font-weight: 600; }

  @media (min-width: 940px) {
    .compendium.on-entry {
      max-width: 1000px;
      grid-template-columns: 216px minmax(0, 1fr);
      column-gap: 64px;
      align-items: start;
    }
    .on-entry .bar { grid-column: 1 / -1; }
    .tree { position: sticky; top: 96px; }
  }
  @media (max-width: 939px) {
    .tree { order: 3; padding-top: 32px; border-top: 1px solid var(--rule); }
  }

  .tree section + section { margin-top: 22px; }
  .tree h2 { margin: 0 0 6px 12px; font-size: 14px; font-weight: 600; color: var(--accent); }
  .tree ul { list-style: none; margin: 0; padding: 0; }
  .tree a {
    display: block;
    padding: 8px 12px;
    border-radius: 8px;
    color: var(--soft);
    text-decoration: none;
    font-size: 16px;
    line-height: 1.3;
    transition: background-color 150ms ease, color 150ms ease;
  }
  .tree a:hover { background: var(--hover); color: var(--ink); }
  .tree a.current { background: var(--panel); color: var(--ink); font-weight: 600; box-shadow: inset 3px 0 0 var(--accent); }
  a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 6px; }
  .pane { min-width: 0; }
</style>
