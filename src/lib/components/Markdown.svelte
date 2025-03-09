<script>
  import { marked } from 'marked';

  /**
   * A component that renders markdown content as HTML.
   * @param {string} content - The markdown content to render
   */
  export let content = '';

  // Convert markdown to HTML
  $: html = marked(content);
</script>

<div class="markdown-content">
  {@html html}
</div>

<style>
  .markdown-content :global(h1) {
    font-size: 2rem;
    font-weight: 700;
    margin: 1rem 0;
  }

  .markdown-content :global(h2) {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 1rem 0;
  }

  .markdown-content :global(h3) {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 1rem 0;
  }

  .markdown-content :global(p) {
    margin-bottom: 1rem;
    line-height: 1.5;
  }

  .markdown-content :global(ul),
  .markdown-content :global(ol) {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
  }

  .markdown-content :global(li) {
    margin-bottom: 0.5rem;
  }

  .markdown-content :global(a) {
    color: var(--color-primary, #3b82f6);
    text-decoration: underline;
  }

  .markdown-content :global(blockquote) {
    border-left: 4px solid var(--color-primary, #3b82f6);
    padding-left: 1rem;
    margin: 1rem 0;
    font-style: italic;
  }

  .markdown-content :global(code) {
    font-family: monospace;
    background: rgba(0, 0, 0, 0.05);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-size: 0.9em;
  }

  .markdown-content :global(pre) {
    background: rgba(0, 0, 0, 0.05);
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
    margin: 1rem 0;
  }

  .markdown-content :global(pre code) {
    background: transparent;
    padding: 0;
  }

  .markdown-content :global(img) {
    max-width: 100%;
    height: auto;
  }

  .markdown-content :global(hr) {
    border: 0;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    margin: 2rem 0;
  }
</style>