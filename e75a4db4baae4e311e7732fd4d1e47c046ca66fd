<script>
  import BookScene from './BookScene.svelte';
  import { sceneCatalog } from '$lib/bookScenes/catalog.js';
  export let id;
  export let src;
  export let alt;
  export let caption;
  $: scene = sceneCatalog[id];
</script>

<div class="book-scene-figure not-prose" data-book-scene={id}>
 <figure>
  <BookScene sceneId={id} {src} {alt} />
  <figcaption>{caption}</figcaption>
 </figure>
  <details>
    <summary>Follow the connections in text</summary>
    <p>{scene.description}</p>
    <table>
      <thead><tr>{#each scene.headings as heading}<th scope="col">{heading}</th>{/each}</tr></thead>
      <tbody>{#each scene.rows as row}<tr><th scope="row">{row[0]}</th><td>{row[1]}</td></tr>{/each}</tbody>
    </table>
  </details>
</div>

<style>
  .book-scene-figure { margin: 2.5rem 0; padding: 0; color: #f1f5f9; overflow: hidden; border: 1px solid #334155; border-radius: 8px; background: #020617; font-family: Inter, sans-serif; }
  .book-scene-figure > figure { margin: 0; padding: 0; }
  figcaption { padding: 1rem 1.25rem; color: #cbd5e1; font: 400 .92rem/1.65 Inter, sans-serif; text-align: left; }
  details { margin: 0 1.25rem 1.25rem; border-top: 1px solid #334155; padding-top: .9rem; font-size: .9rem; line-height: 1.6; }
  summary { color: #f59e0b; cursor: pointer; }
  summary:focus-visible { outline: 2px solid #3b82f6; outline-offset: 5px; }
  details p { margin: 1rem 0; }
  table { width: 100%; border-collapse: collapse; font-size: .85rem; line-height: 1.6; }
  th, td { border-bottom: 1px solid #334155; text-align: left; padding: .6rem .5rem; vertical-align: top; }
  thead { color: #94a3b8; }
  tbody th { width: 30%; color: #f1f5f9; font-weight: 600; }
  td { color: #cbd5e1; }
  @media print { .book-scene-figure { color: #0f172a; background: white; border: 0; break-inside: avoid; } figcaption { color: #334155; } details { display: none; } }
</style>
