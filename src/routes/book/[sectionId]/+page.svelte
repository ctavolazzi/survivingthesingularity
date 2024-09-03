<script>
  import { marked } from 'marked';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { bookPage } from '$lib/stores/bookPage';
  import Pagination from '$lib/components/Pagination.svelte';
  import FloatingPopupProgressBar from '$lib/components/FloatingPopupProgressBar.svelte';
  import FloatingQuotePopup from '$lib/components/FloatingQuotePopup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  export let data;

  let currentSection = 1;
  let totalSections = data.book.sections.length;

  // Convert markdown to HTML
  $: content = marked(data.content);

  $: {
    if (data && data.section) {
      currentSection = data.book.sections.findIndex(section => section.id === data.section.id) + 1;
    }
  }

  onMount(() => {
    currentSection = data.book.sections.findIndex(section => section.id === data.section.id) + 1;
    bookPage.setCurrentSection(data.section.id);
    bookPage.updateLastVisited();
  });

  function handleNavigation(event) {
    const { direction } = event.detail;
    const newIndex = currentSection + (direction === 'next' ? 1 : -1) - 1;
    if (newIndex >= 0 && newIndex < totalSections) {
      const newSection = data.book.sections[newIndex];
      if (newSection) {
        goto(`/book/${newSection.id}`);
      }
    }
  }
</script>

<FloatingPopupProgressBar />
<FloatingQuotePopup />

<svelte:head>
  <title>{data.book.title} - {data.section.title}</title>
  <meta name="description" content="Read {data.section.title} from {data.book.title}">
</svelte:head>

<Spacer height="50px" />

<div class="content-wrapper">
  <!-- Top link -->
  <div class="mt-4 mb-4 text-center">
    <a href="/book" class="toc-link">
      <span class="icon">&#8592;</span> Back to Table of Contents
    </a>
  </div>

  <!-- Existing Progress Bar -->
  <div class="progress-container mb-8">
    <div class="progress-bar" style="width: {(currentSection / totalSections) * 100}%"></div>
    <div class="progress-text">
      Part {currentSection} of {totalSections}
    </div>
  </div>

  <article class="prose prose-lg dark:prose-invert">
    {@html content}
  </article>

  <!-- Add this anchor element right after the article content -->
  <div id="article-end-anchor"></div>

  <!-- Bottom link -->
  <div class="mt-8 mb-4 text-center">
    <a href="/book" class="toc-link">
      <span class="icon">&#8592;</span> Back to Table of Contents
    </a>
  </div>

  <Pagination 
    {currentSection}
    {totalSections}
    on:navigate={handleNavigation}
  />
</div>

<style>
  :global(.prose) {
    max-width: 100%; /* Override Tailwind's max-width */
  }

  :global(.prose h1) {
    font-family: 'Orbitron', sans-serif;
    color: #ff7708;
    font-size: 2.25rem; /* Equivalent to text-4xl */
    line-height: 1.2;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    max-width: 100%;
    margin-bottom: 1rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  }

  :global(.prose p) {
    color: #333; /* Dark gray for better contrast */
    text-shadow: 0.5px 0.5px 1px rgba(255,255,255,0.5);
    text-align: left; /* Add this line to ensure left justification */
  }

  :global(.dark .prose h1) {
    color: #ff9933;
  }

  :global(.dark .prose p) {
    color: #e0e0e0; /* Light gray for dark mode */
    text-shadow: 0.5px 0.5px 1px rgba(0,0,0,0.5);
    text-align: left; /* Add this line to ensure left justification in dark mode */
  }

  @media (max-width: 640px) {
    :global(.prose h1) {
      font-size: 1.875rem; /* Equivalent to text-3xl */
    }
  }

  :global(.prose a) {
    color: #ff7708;
    text-decoration: none;
    transition: all 0.3s ease;
  }

  :global(.prose a:hover) {
    color: #ff9933;
    text-decoration: underline;
  }

  :global(.dark .prose a) {
    color: #ff9933;
  }

  :global(.dark .prose a:hover) {
    color: #ffb366;
  }

  :global(.prose a[href="/book"]) {
    color: white;
    text-decoration: none;
  }

  :global(.prose a[href="/book"]:hover) {
    text-decoration: none;
  }

  :global(.dark .prose a[href="/book"]) {
    color: #1a202c;
  }

  :global(.dark .prose a[href="/book"]:hover) {
    color: #2d3748;
  }

  :global(a[href="/book"]) {
    text-decoration: none;
  }

  :global(a[href="/book"]:hover) {
    text-decoration: underline;
  }

  :global(.dark a[href="/book"]) {
    color: #ff9933;
  }

  :global(.dark a[href="/book"]:hover) {
    color: #ffb366;
  }

  .toc-link {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: #ff7708;
    text-decoration: none;
    transition: all 0.3s ease;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    display: inline-flex;
    align-items: center;
  }

  .toc-link:hover {
    color: #ff9933;
    background-color: rgba(255, 119, 8, 0.1);
  }

  .icon {
    margin-right: 0.5rem;
    font-size: 1.5rem;
  }

  :global(.dark) .toc-link {
    color: #ff9933;
  }

  :global(.dark) .toc-link:hover {
    color: #ffb366;
    background-color: rgba(255, 153, 51, 0.1);
  }

  .content-wrapper {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  @media (max-width: 840px) {
    .content-wrapper {
      max-width: 100%;
    }
  }
</style>
