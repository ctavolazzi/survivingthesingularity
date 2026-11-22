<script>
  // Entry text with its links. The pieces come from bridge.tokens(), so
  // nothing here is drawn as raw HTML.
  /** @type {{text: string, href?: string | null, kind?: string, missing?: boolean}[]} */
  export let pieces = [];
</script>

{#each pieces as piece}{#if piece.href}<a href={piece.href} class={piece.kind}>{piece.text}</a>{:else if piece.missing}<span class="missing" title="No entry yet">{piece.text}</span>{:else}{piece.text}{/if}{/each}

<style>
  a {
    color: var(--accent);
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
  }
  a:hover { text-decoration-thickness: 2px; }
  a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 3px; }
  .missing { border-bottom: 1px dashed var(--muted); color: var(--muted); }
</style>
