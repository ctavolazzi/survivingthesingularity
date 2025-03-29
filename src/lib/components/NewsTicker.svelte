<script>
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';
  import { linear } from 'svelte/easing';

  // Props with default values
  export let title = "Latest Updates";
  export let autoScroll = true;
  export let scrollSpeed = 5000; // ms between news items
  export let refreshInterval = 300000; // 5 minutes by default
  export let maxItems = 5;
  export let backgroundColor = "rgba(15, 23, 42, 0.7)";
  export let textColor = "white";
  export let accentColor = "#3b82f6";
  export let items = null; // New prop to accept direct items
  export let newsItems = [];
  export const speed = 30; // Speed in seconds for a complete cycle
  export const autoplay = true;
  export const pauseOnHover = true;

  // Handle class properly - In Svelte, we use class directly
  let cssClass = "";
  export { cssClass as class };

  // State
  let currentIndex = 0;
  let scrollTimer;
  let refreshTimer;
  let isMounted = false;
  let isHovered = false;
  let tickerWidth;
  let viewportWidth;
  let tickerContainer;
  let loading = false;
  let error = null;

  // Keep track of visibility to prevent flash during transition
  let isVisible = true;
  let transitionTimer;

  // Progress bar for current item display time
  let progress = tweened(0, {
    duration: scrollSpeed,
    easing: cubicOut
  });

  // Update the progress tweened settings when scrollSpeed changes
  $: {
    if (progress) {
      progress = tweened(0, {
        duration: scrollSpeed,
        easing: cubicOut
      });
    }
  }

  // Fetch news items from API or use provided items
  async function fetchNewsItems() {
    try {
      loading = true;

      // If items are provided directly, use those instead of fetching
      if (items) {
        newsItems = items.slice(0, maxItems);
        loading = false;

        // Reset index if needed
        if (currentIndex >= newsItems.length) {
          currentIndex = 0;
        }

        // Start auto-scrolling if enabled
        if (autoScroll && isMounted && !isHovered) {
          startAutoScroll();
        }

        return;
      }

      // Otherwise fetch from API
      const response = await fetch(`/api/news-ticker?limit=${maxItems}`);

      if (!response.ok) {
        throw new Error(`Error fetching news ticker items: ${response.statusText}`);
      }

      const data = await response.json();
      newsItems = data.items;
      loading = false;

      // Reset index if needed
      if (currentIndex >= newsItems.length) {
        currentIndex = 0;
      }

      // Reset progress
      progress.set(0);

      // Start auto-scrolling if enabled
      if (autoScroll && isMounted && !isHovered) {
        startAutoScroll();
      }
    } catch (err) {
      console.error('Failed to fetch news ticker items:', err);
      error = err.message;
      loading = false;
    }
  }

  // Start auto-scrolling
  function startAutoScroll() {
    // Clear existing timer if any
    if (scrollTimer) clearTimeout(scrollTimer);

    // Reset progress
    progress.set(0);

    // Start progress animation
    progress.set(100, { duration: scrollSpeed });

    // Set timer for next item
    scrollTimer = setTimeout(() => {
      if (!isHovered && newsItems.length > 0) {
        changeItem((currentIndex + 1) % newsItems.length);
      }
    }, scrollSpeed);
  }

  // Watch for changes to scrollSpeed to restart auto-scroll with new speed
  $: if (isMounted && autoScroll && !isHovered && scrollSpeed) {
    if (scrollTimer) clearTimeout(scrollTimer);
    startAutoScroll();
  }

  // Smooth item change with consistent layout
  function changeItem(newIndex) {
    if (newIndex >= 0 && newIndex < newsItems.length) {
      // Fade out
      isVisible = false;

      // Clear any existing transition timer
      if (transitionTimer) clearTimeout(transitionTimer);

      // Wait for fade out to complete before changing the index
      transitionTimer = setTimeout(() => {
        currentIndex = newIndex;

        // Fade back in
        isVisible = true;

        // Always restart auto-scroll on item change to ensure consistent timing
        if (autoScroll) {
          startAutoScroll();
        }
      }, 250); // Slightly longer fade for better readability
    }
  }

  // Handle manual navigation
  function goToItem(index) {
    // Add wrap-around functionality
    if (index < 0) {
      index = newsItems.length - 1; // Wrap to the last item when going back from the first
    } else if (index >= newsItems.length) {
      index = 0; // Wrap to the first item when going forward from the last
    }

    if (index !== currentIndex) {
      // Stop current animation if any
      if (scrollTimer) clearTimeout(scrollTimer);

      // Reset progress
      progress.set(0);

      // Change item
      changeItem(index);
    }
  }

  // Handle mouse enter/leave for pausing auto-scroll
  function handleMouseEnter() {
    isHovered = true;
    if (scrollTimer) {
      clearTimeout(scrollTimer);
      let currentValue;
      const unsubscribe = progress.subscribe(value => {
        currentValue = value;
      });
      unsubscribe();
      progress.set(currentValue); // Pause progress animation
    }
  }

  function handleMouseLeave() {
    isHovered = false;
    if (autoScroll) {
      startAutoScroll();
    }
  }

  // Reactive statement to watch for changes in the items prop
  $: if (isMounted && items) {
    fetchNewsItems();
  }

  // Set up event handlers and fetch data on mount
  onMount(() => {
    isMounted = true;
    fetchNewsItems();

    // Set up refresh interval if using API (not needed for direct items)
    if (refreshInterval > 0 && !items) {
      refreshTimer = setInterval(fetchNewsItems, refreshInterval);
    }

    // Add resize listener for responsive adjustments
    const handleResize = () => {
      viewportWidth = window.innerWidth;
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Initial call

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });

  // Clean up on component unmount
  onDestroy(() => {
    isMounted = false;
    if (scrollTimer) clearTimeout(scrollTimer);
    if (refreshTimer) clearInterval(refreshTimer);
    if (transitionTimer) clearTimeout(transitionTimer);
  });

  // Reactive statement to adjust ticker behavior based on viewport
  $: {
    if (viewportWidth && isMounted) {
      // We're removing the mobile slowdown to respect the requested speed
      // No override needed - use the scrollSpeed as provided
    }
  }
</script>

<div
  bind:this={tickerContainer}
  class="news-ticker {cssClass}"
  style="--ticker-bg: {backgroundColor}; --ticker-text: {textColor}; --ticker-accent: {accentColor};"
  on:mouseenter={handleMouseEnter}
  on:mouseleave={handleMouseLeave}
  bind:clientWidth={tickerWidth}
  role="region"
  aria-label="News Ticker"
>
  <div class="ticker-header">
    <h3 class="ticker-title">{title}</h3>

    {#if newsItems.length > 0 && !loading}
      <div class="ticker-controls">
        <button
          class="control-button"
          on:click={() => goToItem(currentIndex - 1)}
          aria-label="Previous news item"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path fill-rule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clip-rule="evenodd" />
          </svg>
        </button>

        <div class="ticker-indicator">
          {#each newsItems as _, i}
            <button
              class="indicator-dot"
              class:active={i === currentIndex}
              on:click={() => goToItem(i)}
              aria-label={`Go to news item ${i + 1}`}
            ></button>
          {/each}
        </div>

        <button
          class="control-button"
          on:click={() => goToItem(currentIndex + 1)}
          aria-label="Next news item"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    {/if}
  </div>

  <div class="ticker-content">
    {#if loading && newsItems.length === 0}
      <div class="ticker-message" in:fade={{ duration: 200 }}>
        <span class="loading-text">Loading latest updates...</span>
      </div>
    {:else if error}
      <div class="ticker-message error" in:fade={{ duration: 200 }}>
        <span class="error-text">Unable to load updates: {error}</span>
      </div>
    {:else if newsItems.length === 0}
      <div class="ticker-message" in:fade={{ duration: 200 }}>
        <span>No updates available at this time.</span>
      </div>
    {:else}
      <div class="ticker-item-container">
        <div class="ticker-item" class:visible={isVisible} aria-hidden={!isVisible}>
          <a href={newsItems[currentIndex].link || '#'} class="ticker-link">
            <div class="ticker-meta">
              <span class="ticker-timestamp">{newsItems[currentIndex].date}</span>
              {#if newsItems[currentIndex].tag}
                <span class="ticker-tag ticker-tag-{newsItems[currentIndex].tag.toLowerCase().replace(' ', '-')}">{newsItems[currentIndex].tag}</span>
              {/if}
            </div>
            <div class="ticker-headline">
              <h4 class="ticker-text">{newsItems[currentIndex].text}</h4>
              {#if newsItems[currentIndex].link}
                <span class="read-more">Read more</span>
              {/if}
            </div>
          </a>
        </div>
      </div>
    {/if}
  </div>

  {#if autoScroll && newsItems.length > 1 && !loading && !error}
    <div class="ticker-progress">
      <div class="progress-bar" style="width: {$progress}%"></div>
    </div>
  {/if}
</div>

<style>
  .news-ticker {
    width: 100%;
    background-color: var(--ticker-bg);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    position: relative;
    margin: 0.25rem 0 0.75rem 0;
    color: var(--ticker-text);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: box-shadow 0.3s ease;
  }

  .news-ticker:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3), 0 0 8px rgba(59, 130, 246, 0.15);
  }

  .ticker-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    background-color: rgba(0, 0, 0, 0.2);
  }

  .ticker-title {
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0;
    display: flex;
    align-items: center;
    letter-spacing: 0.02em;
  }

  .ticker-title::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    background-color: var(--ticker-accent);
    border-radius: 50%;
    margin-right: 0.4rem;
    box-shadow: 0 0 8px var(--ticker-accent);
  }

  .ticker-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .control-button {
    background: transparent;
    border: none;
    color: var(--ticker-text);
    opacity: 0.7;
    cursor: pointer;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }

  .control-button:hover {
    opacity: 1;
    transform: scale(1.1);
  }

  .control-button:focus {
    outline: 2px solid var(--ticker-accent);
    outline-offset: 2px;
    border-radius: 50%;
  }

  .ticker-indicator {
    display: flex;
    gap: 0.4rem;
  }

  .indicator-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--ticker-text);
    opacity: 0.3;
    border: none;
    padding: 0;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .indicator-dot.active {
    opacity: 1;
    background-color: var(--ticker-accent);
    transform: scale(1.3);
    box-shadow: 0 0 6px var(--ticker-accent);
  }

  .indicator-dot:hover {
    opacity: 0.8;
    transform: scale(1.2);
  }

  .indicator-dot:focus {
    outline: 2px solid var(--ticker-accent);
    outline-offset: 2px;
  }

  .ticker-content {
    padding: 0.5rem 0.75rem;
    min-height: 3.5rem;
    display: flex;
    align-items: center;
    position: relative;
  }

  .ticker-item-container {
    width: 100%;
    min-height: 1.5rem;
    position: relative;
    overflow: hidden;
    height: auto;
  }

  .ticker-item {
    width: 100%;
    opacity: 0;
    transition: opacity 0.25s ease-in-out, transform 0.3s ease-out;
    transform: translateY(8px);
    position: relative;
  }

  .ticker-item.visible {
    opacity: 1;
    transform: translateY(0);
    animation: subtle-highlight 2.5s ease-out;
  }

  @keyframes subtle-highlight {
    0% { background-color: rgba(255, 255, 255, 0.05); }
    100% { background-color: transparent; }
  }

  .ticker-link {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.75rem;
    text-decoration: none;
    color: inherit;
    overflow: hidden;
    position: relative;
    padding: 0.15rem 0;
    transition: background-color 0.2s ease;
    border-radius: 6px;
  }

  .ticker-link:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }

  .ticker-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
    min-width: 90px;
    padding-left: 0.5rem;
  }

  .ticker-headline {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
    overflow: hidden;
    position: relative;
    padding-right: 0.5rem;
  }

  .ticker-headline::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 0; /* Only show when hovering */
    background: linear-gradient(90deg, var(--ticker-accent) 0%, transparent 100%);
    opacity: 0.1;
    transition: height 0.2s ease;
  }

  .ticker-timestamp {
    font-size: 0.7rem;
    opacity: 0.75;
    white-space: nowrap;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    flex-shrink: 0;
  }

  .ticker-text {
    font-size: 0.95rem;
    line-height: 1.3;
    font-weight: 500;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
    width: 100%;
    color: #fff;
    letter-spacing: 0.01em;
  }

  .ticker-tag {
    color: white;
    font-size: 0.6rem;
    font-weight: 600;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    white-space: nowrap;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    letter-spacing: 0.02em;
    text-transform: uppercase;
    flex-shrink: 0;
    opacity: 0.9;
    margin-top: 0.05rem;
  }

  /* Tag colors based on type */
  .ticker-tag-opinion {
    background-color: #8b5cf6; /* Purple */
  }

  .ticker-tag-breaking {
    background-color: #ef4444; /* Red */
    animation: pulse 2s infinite;
  }

  .ticker-tag-news {
    background-color: #3b82f6; /* Blue */
  }

  .ticker-tag-update, .ticker-tag-ai-update {
    background-color: #0ea5e9; /* Light blue */
  }

  .ticker-tag-tech {
    background-color: #0d9488; /* Teal */
  }

  .ticker-tag-policy {
    background-color: #6366f1; /* Indigo */
  }

  .ticker-tag-review {
    background-color: #f59e0b; /* Amber */
  }

  /* Default color for any other tags */
  .ticker-tag:not([class*="-"]) {
    background-color: var(--ticker-accent);
  }

  @keyframes pulse {
    0% { opacity: 0.9; }
    50% { opacity: 1; box-shadow: 0 0 10px rgba(239, 68, 68, 0.5); }
    100% { opacity: 0.9; }
  }

  .read-more {
    font-size: 0.8rem;
    opacity: 0.85;
    white-space: nowrap;
    transition: all 0.3s ease;
    font-weight: 500;
    color: var(--ticker-accent);
    margin-top: 0.25rem;
    display: flex;
    align-items: center;
  }

  .read-more::after {
    content: '→';
    margin-left: 0.25rem;
    transition: transform 0.3s ease;
  }

  .ticker-link:hover .read-more::after {
    transform: translateX(4px);
  }

  .ticker-message {
    width: 100%;
    text-align: center;
    font-size: 0.9rem;
    opacity: 0.8;
  }

  .ticker-message.error {
    color: #f87171;
  }

  .ticker-progress {
    height: 3px;
    background-color: rgba(255, 255, 255, 0.1);
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    overflow: hidden;
  }

  .progress-bar {
    height: 100%;
    background-color: var(--ticker-accent);
    transition-timing-function: linear;
    box-shadow: 0 0 8px var(--ticker-accent);
  }

  /* Responsive styles */
  @media (max-width: 768px) {
    .ticker-content {
      padding: 1rem 1.25rem;
    }

    .ticker-link {
      gap: 0.75rem;
    }

    .ticker-text {
      font-size: 0.95rem;
    }
  }

  @media (max-width: 640px) {
    .ticker-content {
      padding: 0.75rem 1rem;
      min-height: 4.5rem;
    }

    .ticker-timestamp {
      font-size: 0.7rem;
      padding: 0.1rem 0.35rem;
      background-color: rgba(255, 255, 255, 0.1);
      opacity: 0.7;
    }

    .ticker-tag {
      font-size: 0.6rem;
      padding: 0.1rem 0.35rem;
    }

    .ticker-link {
      grid-template-columns: 85px 1fr;
      gap: 0.75rem;
    }

    .ticker-text {
      font-size: 0.95rem;
      line-height: 1.3;
      -webkit-line-clamp: 2;
    }

    .read-more {
      font-size: 0.75rem;
    }
  }

  /* Additional adjustments for very narrow screens */
  @media (max-width: 380px) {
    .ticker-link {
      grid-template-columns: 70px 1fr;
      gap: 0.5rem;
    }

    .ticker-meta {
      min-width: 70px;
    }

    .ticker-title {
      font-size: 0.8rem;
    }

    .ticker-text {
      font-size: 0.85rem;
      line-height: 1.25;
    }

    .ticker-timestamp {
      font-size: 0.65rem;
      padding: 0.1rem 0.25rem;
    }

    .ticker-tag {
      font-size: 0.55rem;
      padding: 0.1rem 0.25rem;
    }
  }

  /* High-resolution screens */
  @media (min-width: 1440px) {
    .ticker-content {
      padding: 1.5rem 2rem;
    }

    .ticker-text {
      font-size: 1.05rem;
    }

    .ticker-header {
      padding: 1rem 2rem;
    }
  }
</style>