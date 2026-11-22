<script>
  import Plate from '../Plate.svelte';
  import Linked from '../Linked.svelte';

  export let data;

  $: entry = data.entry;
  $: topic = data.topic;
  $: total = data.appearances.reduce((n, a) => n + a.paragraphs, 0);
</script>

<svelte:head>
  <title>{entry.name} | Compendium | Surviving the Singularity, the novel</title>
</svelte:head>

<article class="entry">
  <header class:with-picture={entry.image}>
    <div class="title">
      <p class="kind"><a href="{data.base}/compendium#topic-{topic.id}">{topic.name}</a></p>
      <h1>{entry.name}</h1>
      <p class="summary"><Linked pieces={entry.summary} /></p>
    </div>
    <!-- A real picture is shown large, under the title. With none, a small plate sits beside it. -->
    <Plate name={entry.name} image={entry.image} size={entry.image ? 'large' : 'small'} />
  </header>

  {#if entry.facts.length}
    <dl class="facts">
      {#each entry.facts as fact}
        <div>
          <dt>{fact.label}</dt>
          <dd><Linked pieces={fact.value} /></dd>
        </div>
      {/each}
    </dl>
  {/if}

  <div class="body">
    {#each entry.body as paragraph}
      <p><Linked pieces={paragraph} /></p>
    {/each}
  </div>

  {#each entry.quotes as quote}
    <figure class="quote">
      <blockquote>{quote.text}</blockquote>
      <figcaption><Linked pieces={quote.from} /></figcaption>
    </figure>
  {/each}

  {#if data.linked.length}
    <section aria-labelledby="see-also">
      <h2 id="see-also">See also</h2>
      <ul class="rows">
        {#each data.linked as other}
          <li>
            <a href={other.href}>
              <span class="words"><span class="name">{other.name}</span><span class="about">{other.summary}</span></span>
              <span class="go" aria-hidden="true">→</span>
            </a>
          </li>
        {/each}
      </ul>
    </section>
  {/if}

  {#if data.appearances.length}
    <section aria-labelledby="in-the-book">
      <h2 id="in-the-book">In the book</h2>
      <p class="note">Named in {total} paragraphs across {data.appearances.length} sections. Open one to read it.</p>
      <ol class="where">
        {#each data.appearances as place}
          <li><a href={place.href}><span>{place.title}</span><span class="n">{place.paragraphs}</span></a></li>
        {/each}
      </ol>
    </section>
  {/if}
</article>

<style>
  /* One measure for everything that is read as a line of words: about 63
     characters at the body size, and it grows with the text-size buttons.
     (Measured in the page, not in `ch`: `ch` follows the inherited font size
     and came out wider than the column.) */
  .entry { --measure: calc(var(--novel-size, 20px) * 29.5); }

  header { display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; margin-bottom: 32px; }
  header.with-picture { flex-direction: column; }
  .title { min-width: 0; }
  .kind { margin: 0 0 8px; font-size: 16px; font-weight: 600; }
  .kind a { color: var(--accent); text-decoration: none; }
  .kind a:hover { text-decoration: underline; text-underline-offset: 4px; }
  h1 {
    font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    font-size: clamp(38px, 8vw, 52px);
    font-weight: 400;
    line-height: 1.08;
    letter-spacing: -0.01em;
    margin: 0 0 14px;
    color: var(--ink);
    text-wrap: balance;
  }
  .summary { margin: 0; max-width: 34ch; color: var(--soft); font-size: 21px; line-height: 1.45; text-wrap: pretty; }

  .facts { margin: 0 0 36px; border-top: 1px solid var(--rule); }
  .facts div {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 2px;
    padding: 12px 0;
    border-bottom: 1px solid var(--rule);
  }
  @media (min-width: 620px) {
    .facts div { grid-template-columns: var(--label) minmax(0, 1fr); gap: 0; }
  }
  dt { font-size: 16px; font-weight: 500; color: var(--soft); line-height: 1.5; }
  dd { margin: 0; font-size: 17px; line-height: 1.5; color: var(--ink); max-width: 46ch; }

  .body { max-width: var(--measure); }
  .body p {
    font-size: calc(var(--novel-size, 20px) - 1px);
    line-height: 1.7;
    margin: 0 0 1.15em;
    color: var(--ink);
    text-wrap: pretty;
  }

  .quote { margin: 32px 0; padding: 4px 0 4px 22px; border-left: 3px solid var(--accent); max-width: var(--measure); }
  blockquote {
    margin: 0;
    font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    font-style: italic;
    font-size: calc(var(--novel-size, 20px) + 2px);
    line-height: 1.5;
    color: var(--ink);
    text-wrap: pretty;
  }
  figcaption { margin-top: 10px; font-size: 16px; line-height: 1.5; color: var(--soft); }

  section { margin-top: 56px; }
  h2 { font-size: 16px; font-weight: 600; color: var(--accent); margin: 0 0 10px; }
  .note { margin: 0 0 10px; color: var(--soft); font-size: 16px; line-height: 1.5; }

  ul, ol { list-style: none; margin: 0; padding: 0; }
  .rows { border-top: 1px solid var(--rule); }
  .rows li { border-bottom: 1px solid var(--rule); }
  .rows a, .where a {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin: 0 -14px;
    padding: 12px 14px;
    border-radius: 10px;
    text-decoration: none;
    transition: background-color 150ms ease;
  }
  .rows a:hover, .where a:hover { background: var(--hover); }
  .rows a:active, .where a:active { background: var(--panel); }
  .words { min-width: 0; }
  .name { display: block; font-size: 19px; font-weight: 600; line-height: 1.3; color: var(--ink); }
  .about { display: block; margin-top: 3px; font-size: 16px; line-height: 1.5; color: var(--soft); }
  .go { flex: none; font-size: 18px; color: var(--soft); transition: transform 150ms ease, color 150ms ease; }
  .rows a:hover .go { color: var(--accent); transform: translateX(3px); }

  /* The chapters that name the entry: short rows, two columns when there is room. */
  .where { border-top: 1px solid var(--rule); padding-top: 6px; }
  @media (min-width: 620px) {
    .where { columns: 2; column-gap: 48px; }
  }
  .where li { break-inside: avoid; }
  .where a { padding: 8px 14px; font-size: 16px; line-height: 1.4; color: var(--ink); }
  .n { flex: none; color: var(--soft); }
  a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
</style>
