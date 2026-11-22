<script>
  export let data;

  $: count = data.tree.reduce((n, topic) => n + topic.entries.length, 0);
</script>

<svelte:head>
  <title>Compendium | Surviving the Singularity, the novel</title>
</svelte:head>

<main>
  <h1>Compendium</h1>
  <p class="lede">The people, places and things in the book. Open one and follow the links.</p>
  <p class="count">Draft. {count} entries so far.</p>

  <!-- Topics down the left, their entries beside them. -->
  <div class="index">
    {#each data.tree as topic}
      <section id="topic-{topic.id}" aria-labelledby="name-{topic.id}">
        <h2 id="name-{topic.id}">{topic.name}</h2>
        <ul>
          {#each topic.entries as entry}
            <li>
              <a href={entry.href}>
                <span class="words">
                  <span class="name">{entry.name}</span>
                  <span class="about">{entry.summary}</span>
                </span>
                <span class="go" aria-hidden="true">→</span>
              </a>
            </li>
          {/each}
        </ul>
      </section>
    {/each}
  </div>
</main>

<style>
  h1 {
    font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    font-size: clamp(38px, 8vw, 52px);
    font-weight: 400;
    line-height: 1.08;
    letter-spacing: -0.01em;
    margin: 0 0 16px;
    color: var(--ink);
  }
  .lede { margin: 0 0 8px; max-width: 36ch; color: var(--ink); font-size: 21px; line-height: 1.5; text-wrap: pretty; }
  .count { margin: 0 0 40px; color: var(--soft); font-size: 16px; }

  section {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 4px;
    padding: 20px 0;
    border-top: 1px solid var(--rule);
  }
  section:last-child { border-bottom: 1px solid var(--rule); }
  @media (min-width: 620px) {
    section { grid-template-columns: var(--label) minmax(0, 1fr); gap: 0; }
  }
  h2 { margin: 0; padding-top: 11px; font-size: 16px; font-weight: 600; color: var(--accent); }
  ul { list-style: none; margin: 0; padding: 0; }

  li a {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin: 0 -14px;
    padding: 10px 14px;
    border-radius: 10px;
    text-decoration: none;
    transition: background-color 150ms ease;
  }
  li a:hover { background: var(--hover); }
  li a:active { background: var(--panel); }
  .words { min-width: 0; }
  .name { display: block; font-size: 20px; font-weight: 600; line-height: 1.3; color: var(--ink); }
  .about { display: block; margin-top: 3px; font-size: 16px; line-height: 1.5; color: var(--soft); }
  .go { flex: none; font-size: 18px; color: var(--soft); transition: transform 150ms ease, color 150ms ease; }
  li a:hover .go { color: var(--accent); transform: translateX(3px); }
  a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
</style>
