<script>
  import { onMount } from 'svelte';
  export let content = '';
  export let showTableOfContents = true;
  export let metadata = { title: '', date: '' };

  let toc = [];

  onMount(() => {
    if (showTableOfContents) {
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = content;
      const headers = tempDiv.querySelectorAll('h2, h3');
      toc = Array.from(headers).map(header => ({
        id: header.id || header.textContent.toLowerCase().replace(/\s+/g, '-'),
        text: header.textContent,
        level: parseInt(header.tagName.charAt(1))
      }));
    }
  });

  function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
      const yOffset = -100;
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({top: y, behavior: 'smooth'});
    }
  }
</script>

<div class="newsletter-content">
  <header class="newsletter-header">
    <h1 class="newsletter-title">{metadata.title}</h1>
    {#if metadata.date}
      <p class="publication-date">Published on {metadata.date}</p>
    {/if}
  </header>

  {#if showTableOfContents && toc.length > 0}
    <div class="table-of-contents">
      <h2>Table of Contents</h2>
      <ul>
        {#each toc as item}
          <li class="toc-item-{item.level}">
            <a href="#{item.id}" on:click|preventDefault={() => scrollToSection(item.id)}>{item.text}</a>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
  <div class="content">
    {@html content}
  </div>
</div>

<style>
  .newsletter-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
  }

  .newsletter-header {
    position: relative;
    padding: 2rem 0;
    overflow: hidden;
  }

  .newsletter-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #3498db, #2ecc71);
  }

  .newsletter-title {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 0.5rem;
    background: linear-gradient(45deg, #3498db, #2ecc71);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  }

  .publication-date {
    position: relative;
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: rgba(52, 152, 219, 0.1);
    border-radius: 20px;
    font-size: 1rem;
    font-style: italic;
    opacity: 0.8;
  }

  .table-of-contents {
    border-left: 4px solid #3498db;
    padding: 1rem;
    margin-bottom: 2rem;
    background-color: rgba(52, 152, 219, 0.1);
    border-radius: 0 8px 8px 0;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .table-of-contents:hover {
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
  }

  .table-of-contents ul {
    list-style-type: none;
    padding-left: 0;
    position: relative;
  }

  .table-of-contents ul::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background-color: rgba(52, 152, 219, 0.3);
  }

  .table-of-contents li {
    position: relative;
    padding-left: 1rem;
  }

  .table-of-contents li::before {
    content: '';
    position: absolute;
    left: -4px;
    top: 50%;
    width: 10px;
    height: 10px;
    background-color: #3498db;
    border-radius: 50%;
    transform: translateY(-50%);
  }

  .toc-item-2 {
    margin-left: 0;
    margin-bottom: 0.5rem;
  }

  .toc-item-3 {
    margin-left: 1rem;
    margin-bottom: 0.5rem;
  }

  .table-of-contents a {
    text-decoration: none;
    transition: color 0.3s ease;
  }

  .table-of-contents a:hover {
    text-decoration: underline;
    border-bottom-color: #3498db;
  }

  :global(.newsletter-content h2) {
    font-size: 2.5rem;
    font-weight: 700;
    margin-top: 2rem;
    margin-bottom: 1rem;
    position: relative;
  }

  :global(.newsletter-content h2)::after {
    content: '';
    display: block;
    width: 50px;
    height: 3px;
    background-color: #3498db;
    margin-top: 0.5rem;
  }

  :global(.newsletter-content h3) {
    font-size: 2rem;
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
  }

  :global(.newsletter-content p) {
    margin-bottom: 1rem;
  }

  :global(.newsletter-content blockquote) {
    border-left: 4px solid #3498db;
    padding-left: 1rem;
    font-style: italic;
    color: #555;
    margin: 1rem 0;
  }

  :global(.newsletter-content a) {
    color: #3498db;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.3s ease;
  }

  :global(.newsletter-content a:hover) {
    border-bottom-color: #3498db;
  }

  /* Enhanced list styling */
  :global(.newsletter-content ul, .newsletter-content ol) {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
  }

  :global(.newsletter-content ul) {
    list-style-type: disc;
  }

  :global(.newsletter-content ul ul) {
    list-style-type: circle;
  }

  :global(.newsletter-content ul ul ul) {
    list-style-type: square;
  }

  :global(.newsletter-content ol) {
    list-style-type: decimal;
  }

  :global(.newsletter-content ol ol) {
    list-style-type: lower-alpha;
  }

  :global(.newsletter-content ol ol ol) {
    list-style-type: lower-roman;
  }

  :global(.newsletter-content li) {
    margin-bottom: 0.5rem;
  }

  :global(.newsletter-content li::marker) {
    color: #3498db;
  }

  @media (prefers-color-scheme: dark) {
    :global(.newsletter-content li::marker) {
      color: #5dade2;
    }
  }

  @media (max-width: 768px) {
    .newsletter-title {
      font-size: 2.5rem;
    }

    :global(.newsletter-content h2) {
      font-size: 2rem;
    }

    :global(.newsletter-content h3) {
      font-size: 1.75rem;
    }
  }

  @media (prefers-color-scheme: dark) {
    .publication-date {
      background-color: rgba(52, 152, 219, 0.2);
    }

    :global(.newsletter-content blockquote) {
      color: #bbb;
    }

    :global(.newsletter-content a) {
      color: #5dade2;
    }

    :global(.newsletter-content a:hover) {
      border-bottom-color: #5dade2;
    }
  }
</style>