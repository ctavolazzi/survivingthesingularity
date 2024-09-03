<script>
    import { onMount } from 'svelte';
  
    let progress = 0;
    let visible = false;
  
    onMount(() => {
      const handleScroll = () => {
        const windowHeight = window.innerHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Get the position of the top elements and the end anchor
        const topElementsHeight = document.querySelector('.progress-container').offsetTop + 
                                  document.querySelector('.progress-container').offsetHeight;
        const endAnchor = document.getElementById('article-end-anchor');
        const endAnchorPosition = endAnchor.offsetTop;
        
        // Calculate progress
        const articleScrollHeight = endAnchorPosition - topElementsHeight;
        progress = Math.max(0, Math.min(100, ((scrollTop - topElementsHeight) / articleScrollHeight) * 100));
        
        // Show progress indicator after scrolling past the top elements
        visible = scrollTop > topElementsHeight;
      };
  
      window.addEventListener('scroll', handleScroll);
      return () => window.removeEventListener('scroll', handleScroll);
    });
  </script>
  
  <div class="floating-progress-indicator" class:visible>
    <svg viewBox="0 0 36 36" class="circular-chart">
      <path class="circle-bg"
        d="M18 2.0845
          a 15.9155 15.9155 0 0 1 0 31.831
          a 15.9155 15.9155 0 0 1 0 -31.831"
      />
      <path class="circle"
        stroke-dasharray="{progress}, 100"
        d="M18 2.0845
          a 15.9155 15.9155 0 0 1 0 31.831
          a 15.9155 15.9155 0 0 1 0 -31.831"
      />
      <text x="18" y="20.35" class="percentage">{Math.round(progress)}%</text>
    </svg>
  </div>
  
  <style>
    .floating-progress-indicator {
      position: fixed;
      bottom: 20px;
      left: 20px;
      width: 60px;
      height: 60px;
      background-color: rgba(255, 255, 255, 0.9);
      border-radius: 50%;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      display: flex;
      justify-content: center;
      align-items: center;
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
      z-index: 1000;
    }
  
    .floating-progress-indicator.visible {
      opacity: 1;
    }
  
    .circular-chart {
      width: 50px;
      height: 50px;
    }
  
    .circle-bg {
      fill: none;
      stroke: #eee;
      stroke-width: 3.8;
    }
  
    .circle {
      fill: none;
      stroke: #ff7708;
      stroke-width: 2.8;
      stroke-linecap: round;
      transition: stroke-dasharray 0.1s ease-out;
    }
  
    .percentage {
      fill: #666;
      font-family: sans-serif;
      font-size: 0.5em;
      text-anchor: middle;
    }
  
    :global(.dark) .circle {
      stroke: #ff9933;
    }
  
    :global(.dark) .floating-progress-indicator {
      background-color: rgba(0, 0, 0, 0.7);
    }
  
    :global(.dark) .circle-bg {
      stroke: #444;
    }
  
    :global(.dark) .percentage {
      fill: #e0e0e0;
    }
  </style>