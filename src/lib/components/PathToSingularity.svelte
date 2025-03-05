<script>
  import { onMount } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';
  import { darkMode } from '$lib/stores/darkMode';

  let visible = false;
  let animationStarted = false;
  let animationPhase = 0;
  let sectionElement;

  const progress = tweened(0, {
    duration: 2000,
    easing: cubicOut
  });

  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        visible = true;
        progress.set(1);
        setTimeout(() => {
          animationStarted = true;
          startAnimation();
        }, 100);
        observer.unobserve(sectionElement);
      }
    }, { threshold: 0.1 });

    observer.observe(sectionElement);
  });

  function startAnimation() {
    animationPhase = 1;
    setTimeout(() => {
      animationPhase = 2;
      setTimeout(() => {
        animationPhase = 0;
        setTimeout(startAnimation, 1000);
      }, 2000);
    }, 2000);
  }
</script>

<section class="singularity-path" class:dark={$darkMode} bind:this={sectionElement}>
  <div class="grid-background"></div>
  {#if visible}
    <h2 class="title">
      <span class="path">
        {#each 'The Path to the'.split('') as char, i}
          <span
            class="char"
            style="transition-delay: {i * 50}ms; opacity: 1; transform: translateY(0);"
          >
            {char === ' ' ? '\u00A0' : char}
          </span>
        {/each}
      </span>
      <span class="singularity">
        {#each 'Singularity'.split('') as char, i}
          <span
            class="char singularity-char"
            style="
              --char-index: {i};
              transition-delay: {i * 50}ms;
              opacity: 1;
              transform: none;
            "
          >
            {char}
          </span>
        {/each}
      </span>
    </h2>
    <div class="underline-container">
      <div
        class="underline"
        style="transform: scaleX({$progress});"
      ></div>
    </div>
  {/if}
</section>

<style>
  .singularity-path {
    --bg-color: #f8fafc;
    --text-color: #1a202c;
    --accent-color: #4299e1;
    --grid-color: rgba(66, 153, 225, 0.1);

    padding: 3rem 2rem;
    text-align: center;
    background: radial-gradient(circle at center, var(--bg-color), var(--bg-color-secondary));
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1), inset 0 0 15px rgba(66, 153, 225, 0.3);
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
    min-height: 200px;
    color: var(--text-color);
  }

  .singularity-path.dark {
    --bg-color: #1a202c;
    --bg-color-secondary: #2d3748;
    --text-color: #f8fafc;
    --accent-color: #63b3ed;
    --grid-color: rgba(99, 179, 237, 0.1);
  }

  .grid-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
      linear-gradient(var(--grid-color) 1px, transparent 1px),
      linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
    background-size: 20px 20px;
    z-index: 1;
  }

  .title {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0;
    line-height: 1.1;
    position: relative;
    z-index: 2;
  }

  .path, .singularity {
    display: block;
    white-space: nowrap;
  }

  .char {
    display: inline-block;
    transition: opacity 0.5s, transform 0.5s;
  }

  .singularity {
    font-size: 3rem;
    font-weight: bold;
    color: var(--accent-color);
  }

  .singularity-char {
    transition: opacity 0.5s, transform 2s cubic-bezier(0.25, 0.1, 0.25, 1);
  }

  .underline-container {
    width: 100%;
    height: 2px;
    margin-top: 1rem;
    overflow: hidden;
  }

  .underline {
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, var(--accent-color), #667eea, #764ba2);
    transform-origin: left;
    box-shadow: 0 0 10px rgba(102, 126, 234, 0.8);
  }

  @media (min-width: 640px) {
    .singularity-path {
      padding: 4rem 3rem;
    }

    .path {
      font-size: 2rem;
    }

    .singularity {
      font-size: 5.5rem;
    }
  }
</style>
