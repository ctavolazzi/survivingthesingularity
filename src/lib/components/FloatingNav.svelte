<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  import { fade } from 'svelte/transition';

  export let sections = [];

  let visible = false;
  let activeSection = '';
  let scrollProgress = 0;

  function handleScroll() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    scrollProgress = Math.min(100, Math.round((scrollTop / docHeight) * 100));

    // Show after scrolling past hero
    visible = scrollTop > window.innerHeight * 0.8;

    // Find active section
    for (let i = sections.length - 1; i >= 0; i--) {
      const el = document.getElementById(sections[i].id);
      if (el) {
        const rect = el.getBoundingClientRect();
        if (rect.top <= 200) {
          activeSection = sections[i].id;
          break;
        }
      }
    }
  }

  function scrollToSection(id) {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  onMount(() => {
    if (browser) {
      window.addEventListener('scroll', handleScroll, { passive: true });
      handleScroll();
    }
  });

  onDestroy(() => {
    if (browser) {
      window.removeEventListener('scroll', handleScroll);
    }
  });
</script>

{#if visible}
  <nav class="floating-nav" transition:fade={{ duration: 200 }}>
    <div class="fnav-progress">
      <div class="fnav-progress-fill" style="height: {scrollProgress}%"></div>
    </div>
    <div class="fnav-dots">
      {#each sections as section}
        <button
          class="fnav-dot"
          class:fnav-dot-active={activeSection === section.id}
          on:click={() => scrollToSection(section.id)}
          title={section.label}
        >
          <span class="fnav-dot-inner"></span>
          <span class="fnav-tooltip">{section.label}</span>
        </button>
      {/each}
    </div>
    <span class="fnav-pct">{scrollProgress}%</span>
  </nav>
{/if}

<style>
  .floating-nav {
    position: fixed;
    right: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
    z-index: 40;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
  }

  .fnav-progress {
    width: 2px;
    height: 60px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 1px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }

  .fnav-progress-fill {
    width: 100%;
    background: linear-gradient(180deg, #f59e0b, #10b981);
    border-radius: 1px;
    transition: height 0.15s ease;
  }

  .fnav-dots {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .fnav-dot {
    position: relative;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
  }

  .fnav-dot-inner {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.2s;
  }

  .fnav-dot:hover .fnav-dot-inner {
    background: rgba(245, 158, 11, 0.3);
    border-color: rgba(245, 158, 11, 0.4);
    transform: scale(1.4);
  }

  .fnav-dot-active .fnav-dot-inner {
    background: #f59e0b;
    border-color: #f59e0b;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.4);
    transform: scale(1.3);
  }

  .fnav-tooltip {
    position: absolute;
    right: calc(100% + 8px);
    white-space: nowrap;
    padding: 0.3rem 0.6rem;
    background: #0f172a;
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 6px;
    font-size: 0.68rem;
    font-weight: 600;
    color: #cbd5e1;
    opacity: 0;
    pointer-events: none;
    transform: translateX(4px);
    transition: all 0.15s;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  }

  .fnav-dot:hover .fnav-tooltip {
    opacity: 1;
    transform: translateX(0);
  }

  .fnav-pct {
    font-size: 0.55rem;
    color: #334155;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    margin-top: 0.5rem;
  }

  @media (max-width: 1100px) {
    .floating-nav {
      display: none;
    }
  }
</style>
