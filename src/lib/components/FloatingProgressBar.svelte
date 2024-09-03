<script>
    import { onMount } from 'svelte';
  
    let progress = 0;
    let visible = false;
  
    onMount(() => {
      const handleScroll = () => {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Calculate progress
        progress = (scrollTop / (documentHeight - windowHeight)) * 100;
        
        // Show progress bar after scrolling a bit
        visible = scrollTop > 100;
      };
  
      window.addEventListener('scroll', handleScroll);
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
      height: 4px;
      background-color: rgba(255, 255, 255, 0.2);
      z-index: 1000;
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
    }
  
    .floating-progress-container.visible {
      opacity: 1;
    }
  
    .floating-progress-bar {
      height: 100%;
      background-color: #ff7708;
      transition: width 0.1s ease-out;
    }
  
    :global(.dark) .floating-progress-bar {
      background-color: #ff9933;
    }
</style>