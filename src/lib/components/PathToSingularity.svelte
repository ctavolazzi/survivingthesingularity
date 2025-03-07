<script>
  import { onMount } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';
  import { darkMode } from '$lib/stores/darkMode';
  import { goto } from '$app/navigation';

  let visible = false;
  let animationStarted = false;
  let animationPhase = 0;
  let sectionElement;

  const progress = tweened(0, {
    duration: 800,
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
        }, 50);
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

  function handleStartHereClick() {
    console.log("Start Here button clicked");
    goto('/start-here');
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
    <div class="button-container">
      <a
        href="/start-here"
        class="start-here-button"
        on:click|preventDefault={handleStartHereClick}
      >
        Start Here
      </a>
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
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15), inset 0 0 15px rgba(66, 153, 225, 0.4);
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
    animation: pulse-grid 15s infinite alternate;
  }

  @keyframes pulse-grid {
    0% {
      opacity: 0.3;
    }
    50% {
      opacity: 0.7;
    }
    100% {
      opacity: 0.3;
    }
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

  .path {
    font-weight: 500;
    color: rgba(var(--text-color-rgb, 255, 255, 255), 0.9);
    margin-bottom: 0.5rem;
    letter-spacing: 0.05em;
  }

  .char {
    display: inline-block;
    transition: opacity 0.5s, transform 0.5s;
  }

  .singularity {
    font-size: 3rem;
    font-weight: bold;
    color: var(--accent-color);
    text-shadow: 0 0 15px rgba(66, 153, 225, 0.6);
    position: relative;
  }

  .singularity-char {
    transition: opacity 0.5s, transform 2s cubic-bezier(0.25, 0.1, 0.25, 1);
  }

  .underline-container {
    width: 100%;
    height: 3px;
    margin-top: 1rem;
    overflow: hidden;
    position: relative;
  }

  .underline {
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, var(--accent-color), #667eea, #764ba2);
    transform-origin: left;
    box-shadow: 0 0 10px rgba(102, 126, 234, 0.8);
  }

  .underline::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 30px;
    height: 100%;
    background: rgba(255, 255, 255, 0.6);
    filter: blur(5px);
    animation: shine 3s infinite;
  }

  @keyframes shine {
    0% {
      left: -100px;
    }
    100% {
      left: 100%;
    }
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

  /* Mobile optimizations */
  @media (max-width: 480px) {
    .singularity-path {
      padding: 2rem 1.25rem;
      margin: 0.5rem 0.75rem 1.5rem;
      border-radius: 10px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2), inset 0 0 15px rgba(66, 153, 225, 0.4);
    }

    .path {
      font-size: 1.3rem;
      margin-bottom: 0.25rem;
    }

    .singularity {
      font-size: 2.8rem;
      letter-spacing: 0.02em;
    }

    .underline-container {
      margin-top: 0.75rem;
    }
  }

  .button-container {
    margin-top: 1.5rem;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease forwards;
    animation-delay: 0.3s;
    position: relative;
    z-index: 10;
    pointer-events: auto;
  }

  .start-here-button {
    display: inline-block;
    padding: 0.75rem 2rem;
    background: linear-gradient(135deg, #4299e1, #667eea);
    color: white;
    font-weight: 600;
    font-size: 1.1rem;
    border-radius: 30px;
    text-decoration: none;
    box-shadow: 0 4px 10px rgba(66, 153, 225, 0.4);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    z-index: 10;
    cursor: pointer;
    pointer-events: auto;
  }

  .start-here-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(66, 153, 225, 0.5);
  }

  .start-here-button:active {
    transform: translateY(-1px);
  }

  .start-here-button::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0));
    transform: translateX(-100%);
    transition: transform 0.6s ease;
  }

  .start-here-button:hover::after {
    transform: translateX(100%);
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Responsive styles for the button */
  @media (max-width: 480px) {
    .button-container {
      margin-top: 1.25rem;
    }

    .start-here-button {
      padding: 0.6rem 1.75rem;
      font-size: 1rem;
    }
  }
</style>
