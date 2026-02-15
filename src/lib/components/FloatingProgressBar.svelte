<script>
    import { onMount } from 'svelte';

    let progress = 0;
    let visible = false;
    let ticking = false;

    onMount(() => {
      const handleScroll = () => {
        if (!ticking) {
          window.requestAnimationFrame(() => {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            // Calculate progress
            progress = (scrollTop / (documentHeight - windowHeight)) * 100;

            // Show progress bar after scrolling a bit
            visible = scrollTop > 100;

            ticking = false;
          });

          ticking = true;
        }
      };

      window.addEventListener('scroll', handleScroll, { passive: true });
      return () => window.removeEventListener('scroll', handleScroll);
    });
</script>

<div class="floating-progress-container" class:visible>
    <div class="floating-progress-bar" style="width: {progress}%"></div>
</div>

<style>
    .floating-progress-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 2px;
      background-color: rgba(148, 163, 184, 0.1);
      z-index: 1000;
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
    }

    .floating-progress-container.visible {
      opacity: 1;
    }

    .floating-progress-bar {
      height: 100%;
      background: linear-gradient(90deg, #3b82f6, #8b5cf6);
      transition: width 0.1s ease-out;
      box-shadow: 0 0 8px rgba(99, 179, 237, 0.4);
    }
</style>