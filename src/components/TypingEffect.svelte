<script lang="ts">
    import { onMount } from 'svelte';
    import { cubicInOut } from 'svelte/easing';
    import { throttle } from '$lib/utils/lodash';
    
    export let text: string = '';
    export let typingSpeed: number = 150;
    export let deletingSpeed: number = 75;
    export let delayBeforeDeletion: number = 1000;
    export let ariaLabel: string = 'Typing effect';
    export let color: string = 'inherit';
    export let fontSize: string = 'inherit';
    export let animationStyle: 'default' | 'custom' = 'default';
    export let cursorStyle: 'default' | 'custom' = 'default';
    export let animationDuration: number = 2000;
    export let loop: boolean = false;
    export let loopDelay: number = 1000;
    export let onAnimationComplete: (({ text, totalDuration }: { text: string; totalDuration: number }) => void) | undefined = undefined;
    export let rainbowMode: boolean = false;
    export let rainbowColors: { color: string; name: string }[] = [
      { color: '#ff0000', name: 'Red' },
      { color: '#ff7f00', name: 'Orange' },
      { color: '#ffff00', name: 'Yellow' },
      { color: '#00ff00', name: 'Green' },
      { color: '#0000ff', name: 'Blue' },
      { color: '#4b0082', name: 'Indigo' },
      { color: '#9400d3', name: 'Violet' }
    ];
    export let rainbowColorInterval: number = 5;
    export let id: string = '';
    
    let displayedText = '';
    let internalText = '';
    let isDeleting = false;
    let fontIndex = 0;
    const fonts = ["'Palatino', serif", "'Arial', sans-serif", "'Courier New', monospace"];
    let isRainbowModeAnnounced = false;
    let typingEffectElement: HTMLElement | null = null;
    let animationCompleted = false;
    let rainbowColorIndex = 0;
    
    function handleRainbowModeToggle() {
      isRainbowModeAnnounced = rainbowMode;
    }
    
    $: handleRainbowModeToggle(rainbowMode);
    
    function initTypingEffect() {
      displayedText = '';
      isDeleting = false;
      animationCompleted = false;
      rainbowColorIndex = 0;
      startAnimation();
    }
    
    const throttledAnimateTyping = throttle((timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = timestamp - startTime;
      const duration = isDeleting ? deletingSpeed : typingSpeed;
      const animationProgress = Math.min(progress / duration, 1);
      const easedProgress = cubicInOut(animationProgress);
  
      if (!isDeleting && currentFrame < totalFrames) {
        currentFrame = Math.floor(easedProgress * totalFrames);
        displayedText = internalText.slice(0, currentFrame);
      } else if (isDeleting && currentFrame >= 0) {
        currentFrame = Math.floor((1 - easedProgress) * totalFrames);
        displayedText = internalText.slice(0, currentFrame);
        if (currentFrame === 0) {
          isDeleting = false;
          fontIndex = (fontIndex + 1) % fonts.length;
          if (loop) {
            setTimeout(initTypingEffect, loopDelay);
          } else {
            animationCompleted = true;
            handleAnimationComplete();
          }
          return;
        }
      } else if (currentFrame === totalFrames) {
        setTimeout(() => {
          isDeleting = true;
          startTime = null;
          animateTyping(performance.now());
        }, delayBeforeDeletion);
        return;
      }
      
      if (rainbowMode && !isDeleting && currentFrame % rainbowColorInterval === 0) {
        rainbowColorIndex = (rainbowColorIndex + 1) % rainbowColors.length;
      }
  
      requestAnimationFrame(animateTyping);
    }, 16);
    
    function startAnimation() {
      if (!internalText) return;
  
      const totalFrames = internalText.length;
      let currentFrame = 0;
      let startTime = null;
  
      function animateTyping(timestamp) {
        throttledAnimateTyping(timestamp);
      }
  
      animateTyping(performance.now());
    }
    
    function handleTextUpdate() {
      const slotContent = this.textContent.trim();
      internalText = slotContent || text;
      initTypingEffect();
    }
    
    function handleAnimationComplete() {
      onAnimationComplete?.({
        text: internalText,
        totalDuration: (internalText.length * typingSpeed) + (internalText.length * deletingSpeed) + delayBeforeDeletion
      });
    }
  
    onMount(() => {
      const handleResize = () => {
        initTypingEffect();
      };
      
      window.addEventListener('resize', handleResize);
      
      return () => {
        window.removeEventListener('resize', handleResize);
      };
    });
  </script>
  
  <div
    bind:this={typingEffectElement}
    use:handleTextUpdate
    on:slotchange={handleTextUpdate}
    {id}
    style="
      font-family: {fonts[fontIndex]};
      min-height: 1em;
      color: {rainbowMode ? rainbowColors[rainbowColorIndex].color : color};
      font-size: {fontSize};
    "
    aria-label={ariaLabel}
    role="region"
    aria-live="assertive"
    aria-atomic="true"
  >
    {#if internalText}
      <p>
        {displayedText}
        {#if !animationCompleted}
          <span
            class="blinking-caret"
            class:default={cursorStyle === 'default'}
            style="animation-duration: {animationDuration}ms;"
            aria-hidden="true"
          >|</span>
        {/if}
      </p>
      {#if rainbowMode && !isRainbowModeAnnounced}
        <span aria-live="polite" aria-atomic="true" class="visually-hidden">
          Rainbow mode activated. The typing effect will cycle through different colors.
        </span>
      {/if}
    {:else}
      <p>No text provided.</p>
    {/if}
    
    <slot></slot>
  </div>
  
  <style>
    .blinking-caret {
      animation: blink var(--animation-duration) infinite step-start;
    }
    
    .blinking-caret.default {
      border-right: 0.1em solid;
    }
    
    @keyframes blink {
      50% {
        opacity: 0;
      }
    }
    
    .visually-hidden {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
  </style>