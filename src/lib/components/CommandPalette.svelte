<script>
  import { goto } from '$app/navigation';
  import { fade, fly } from 'svelte/transition';
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import { browser } from '$app/environment';

  export let open = false;

  const dispatch = createEventDispatcher();

  let query = '';
  let inputEl;
  let selectedIndex = 0;

  const pages = [
    { type: 'page', title: 'Home', desc: 'Main landing page', path: '/', icon: 'home', keywords: 'home landing main' },
    { type: 'page', title: 'Blog', desc: 'Articles & dispatches', path: '/blog', icon: 'edit', keywords: 'blog articles posts' },
    { type: 'page', title: 'Book', desc: 'Surviving the Singularity book', path: '/book', icon: 'book', keywords: 'book read purchase' },
    { type: 'page', title: 'Signals', desc: 'Live AI research feed', path: '/signals', icon: 'chapter', keywords: 'signals research arxiv ai feed' },
    { type: 'page', title: 'Early Access', desc: 'Get early access to everything', path: '/early-access', icon: 'user', keywords: 'early access buy purchase' },
    { type: 'page', title: 'About', desc: 'About the project', path: '/about', icon: 'info', keywords: 'about mission team' },
  ];

  const allItems = [...pages];

  $: filtered = query.trim()
    ? allItems.filter(item => {
        const q = query.toLowerCase();
        return item.title.toLowerCase().includes(q)
          || item.desc.toLowerCase().includes(q)
          || (item.keywords && item.keywords.toLowerCase().includes(q));
      })
    : allItems;

  $: selectedIndex = Math.min(selectedIndex, Math.max(0, filtered.length - 1));

  function handleOpen() {
    open = true;
    query = '';
    selectedIndex = 0;
    setTimeout(() => inputEl?.focus(), 50);
  }

  function handleClose() {
    open = false;
    query = '';
    dispatch('close');
  }

  function selectItem(item) {
    goto(item.path);
    handleClose();
  }

  function handleKeydown(e) {
    if (!open) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        handleOpen();
      }
      return;
    }

    if (e.key === 'Escape') {
      e.preventDefault();
      handleClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, filtered.length - 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, 0);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filtered[selectedIndex]) selectItem(filtered[selectedIndex]);
    }
  }

  onMount(() => {
    if (browser) window.addEventListener('keydown', handleKeydown);
  });

  onDestroy(() => {
    if (browser) window.removeEventListener('keydown', handleKeydown);
  });

  function getIcon(type) {
    switch (type) {
      case 'home': return `<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>`;
      case 'book': return `<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>`;
      case 'edit': return `<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>`;
      case 'user': return `<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>`;
      case 'info': return `<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>`;
      case 'chapter': return `<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/>`;
      default: return `<circle cx="12" cy="12" r="10"/>`;
    }
  }
</script>

{#if open}
  <button
    type="button"
    class="palette-overlay"
    on:click={handleClose}
    aria-label="Close command palette"
    transition:fade={{ duration: 150 }}
  ></button>
  <div class="palette" role="dialog" aria-modal="true" aria-label="Command palette" in:fly={{ y: -20, duration: 200 }}>
      <div class="palette-input-wrap">
        <svg class="palette-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          bind:this={inputEl}
          bind:value={query}
          type="text"
          class="palette-input"
          placeholder="Search pages..."
          spellcheck="false"
          autocomplete="off"
        />
        <kbd class="palette-esc">esc</kbd>
      </div>

      <div class="palette-results">
        {#if filtered.length === 0}
          <div class="palette-empty">
            <p>No results for "{query}"</p>
          </div>
        {:else}
          {#each filtered as item, i}
            <button
              class="palette-item"
              class:palette-item-active={i === selectedIndex}
              on:click={() => selectItem(item)}
              on:mouseenter={() => selectedIndex = i}
            >
              <svg class="palette-item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                {@html getIcon(item.icon)}
              </svg>
              <div class="palette-item-text">
                <span class="palette-item-title">{item.title}</span>
                <span class="palette-item-desc">{item.desc}</span>
              </div>
              <span class="palette-item-type">{item.type}</span>
            </button>
          {/each}
        {/if}
      </div>

      <div class="palette-footer">
        <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> navigate</span>
        <span><kbd>enter</kbd> select</span>
        <span><kbd>esc</kbd> close</span>
      </div>
    </div>
{/if}

<style>
  .palette-overlay {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.82);
    z-index: 9999;
    border: none;
    margin: 0;
    padding: 0;
    cursor: pointer;
  }

  .palette {
    position: fixed;
    top: 15vh;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10000;
    width: calc(100% - 2rem);
    max-width: 580px;
    background: #0a0f23;
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-left: 3px solid rgba(245, 158, 11, 0.4);
    border-radius: 0;
    overflow: hidden;
    box-shadow: 6px 6px 0 rgba(245, 158, 11, 0.08);
  }

  .palette-input-wrap {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
  }

  .palette-search-icon {
    color: #dde4ef;
    flex-shrink: 0;
  }

  .palette-input {
    flex: 1;
    background: none;
    border: none;
    outline: none;
    color: #f1f5f9;
    font-size: 1rem;
    font-family: inherit;
    caret-color: #f59e0b;
  }

  .palette-input::placeholder {
    color: #dde4ef;
  }

  .palette-esc {
    font-size: 0.76rem;
    padding: 0.15rem 0.4rem;
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 0;
    color: #dde4ef;
    font-family: var(--font-primary);
    background: rgba(30, 41, 59, 0.5);
  }

  .palette-results {
    max-height: 360px;
    overflow-y: auto;
    padding: 0.5rem;
  }

  .palette-results::-webkit-scrollbar {
    width: 4px;
  }

  .palette-results::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.1);
    border-radius: 2px;
  }

  .palette-empty {
    padding: 2rem;
    text-align: center;
    color: #dde4ef;
    font-size: 0.9rem;
  }

  .palette-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.65rem 0.75rem;
    border: none;
    background: none;
    cursor: pointer;
    border-radius: 0;
    transition: all 0.1s;
    text-align: left;
    font-family: inherit;
  }

  .palette-item:hover,
  .palette-item-active {
    background: rgba(245, 158, 11, 0.08);
  }

  .palette-item-icon {
    color: #dde4ef;
    flex-shrink: 0;
  }

  .palette-item-active .palette-item-icon {
    color: #f59e0b;
  }

  .palette-item-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .palette-item-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .palette-read-badge {
    font-size: 0.82rem;
    padding: 0.1rem 0.35rem;
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border-radius: 0;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .palette-item-desc {
    font-size: 0.85rem;
    color: #dde4ef;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .palette-item-type {
    font-size: 0.76rem;
    color: #dde4ef;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    flex-shrink: 0;
    font-family: var(--font-primary);
  }

  .palette-footer {
    display: flex;
    gap: 1.25rem;
    padding: 0.6rem 1rem;
    border-top: 1px solid rgba(148, 163, 184, 0.06);
    justify-content: center;
  }

  .palette-footer span {
    font-size: 0.76rem;
    color: #dde4ef;
    display: flex;
    align-items: center;
    gap: 0.3rem;
  }

  .palette-footer kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 18px;
    height: 18px;
    padding: 0 3px;
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 3px;
    background: rgba(30, 41, 59, 0.3);
    color: #dde4ef;
    font-family: var(--font-primary);
    font-size: 0.82rem;
  }

  @media (max-width: 640px) {
    .palette {
      top: 5vh;
      width: calc(100% - 1.5rem);
    }

    .palette-footer {
      display: none;
    }
  }
</style>
