<!-- src/lib/components/TableOfContents.svelte -->
<script>
  import { goto } from '$app/navigation';
  // Remove these imports as they're no longer needed
  // import { fly, fade } from 'svelte/transition';
  // import { quintOut } from 'svelte/easing';
  import { darkMode } from '$lib/stores/darkMode';
  import { bookPage } from '$lib/stores/bookPage';
  
  export let sections = [];
  let hoveredIndex = -1;
  let currentSectionId;

  bookPage.subscribe(state => {
    currentSectionId = state.currentSectionId;
  });

  function handleClick(sectionId) {
    bookPage.setCurrentSection(sectionId);
    goto(`/book/${sectionId}`);
  }
</script>

<nav class="table-of-contents">
  <div class="title-container">
    <h2>Table of Contents</h2>
  </div>
  <ul>
    {#each sections as section, index}
      <li 
        class:active={section.id === currentSectionId}
        on:mouseenter={() => hoveredIndex = index}
        on:mouseleave={() => hoveredIndex = -1}
      >
        <button on:click={() => handleClick(section.id)}>
          <span class="section-number">{index + 1}</span>
          <span class="section-title">{section.title}</span>
          {#if hoveredIndex === index || section.id === currentSectionId}
            <span class="hover-effect"></span>
          {/if}
        </button>
      </li>
    {/each}
  </ul>
</nav>

<style>
  .table-of-contents {
    background-color: #ffffff;
    color: #2d3748;
    padding: 1rem;
    border-radius: 0.5rem;
    width: 100%;
    max-width: 800px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
  }

  .title-container {
    background: linear-gradient(135deg, #ff9933, #ff8000);
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
  }

  h2 {
    font-size: 2.25rem;
    font-weight: 800;
    text-align: center;
    margin: 0;
    line-height: 1.2;
    color: #ffffff;
    letter-spacing: -0.025em;
  }

  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  li {
    margin-bottom: 0.75rem;
  }

  button {
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
    font-family: inherit;
    font-size: 1rem;
    text-align: left;
    padding: 0.75rem 1rem;
    border-radius: 0.25rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
  }

  button:hover, button:focus {
    background-color: rgba(255, 153, 51, 0.1);
    outline: none;
  }

  .section-number {
    font-weight: bold;
    color: #ff7708;
    margin-right: 1rem;
    font-size: 1.1rem;
    min-width: 1.5rem;
  }

  .section-title {
    flex-grow: 1;
  }

  .hover-effect {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, rgba(255, 153, 51, 0.2) 0%, rgba(255, 153, 51, 0) 100%);
    pointer-events: none;
    transition: opacity 0.3s ease;
    opacity: 0;
  }

  button:hover .hover-effect,
  .active button .hover-effect {
    opacity: 1;
  }

  /* Dark mode styles */
  :global(.dark) .table-of-contents {
    background-color: #2d3748;
    color: #f7fafc;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  }

  :global(.dark) .title-container {
    background: linear-gradient(135deg, #ff9933, #ff8000);
  }

  :global(.dark) h2 {
    color: #2d3748;
  }

  :global(.dark) button {
    color: #f7fafc;
  }

  :global(.dark) button:hover, :global(.dark) button:focus {
    background-color: rgba(255, 153, 51, 0.2);
  }

  :global(.dark) .section-number {
    color: #ffb366;
  }

  @media (max-width: 640px) {
    .title-container {
      padding: 1rem;
    }

    h2 {
      font-size: 1.75rem;
    }

    button {
      font-size: 0.9rem;
      padding: 0.5rem 0.75rem;
    }

    .section-number {
      font-size: 1rem;
      margin-right: 0.75rem;
    }
  }

  .active button {
    background-color: rgba(255, 153, 51, 0.2);
    font-weight: bold;
  }
</style>
