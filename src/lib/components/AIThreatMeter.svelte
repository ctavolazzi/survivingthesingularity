<script>
    import { onMount } from 'svelte';
    import { scale } from 'svelte/transition';
    import { elasticOut } from 'svelte/easing';

    let aiThreatLevel = 50;

    function updateThreatLevel() {
      aiThreatLevel = Math.floor(Math.random() * 100);
    }

    function getThreatColor(level) {
      if (level <= 33) return 'var(--color-safe)';
      if (level <= 66) return 'var(--color-warning)';
      return 'var(--color-danger)';
    }

    onMount(() => {
      const interval = setInterval(updateThreatLevel, 5000);
      return () => clearInterval(interval);
    });
  </script>
  
  <div class="ai-threat-meter" in:scale="{{ duration: 500, delay: 200, easing: elasticOut }}">
    <h2>Current AI Threat Level</h2>
    <div class="meter">
      <div 
        class="meter-fill" 
        style="width: {aiThreatLevel}%; background-color: {getThreatColor(aiThreatLevel)};"
      ></div>
    </div>
    <p>Threat Level: {aiThreatLevel}% {aiThreatLevel > 80 ? '😱' : aiThreatLevel > 50 ? '😰' : '😎'}</p>
    <small>(Half-joking, fully serious)</small>
  </div>
  
  <style>
    :global(:root) {
      --color-safe: #4caf50;
      --color-warning: #ffc107;
      --color-danger: #f44336;
      --color-bg-secondary: #f0f0f0;
      --color-bg-tertiary: #e0e0e0;
      --color-text-primary: #333333;
      --color-text-secondary: #666666;
    }

    :global(.dark) {
      --color-safe: #45a049;
      --color-warning: #ffb300;
      --color-danger: #e53935;
      --color-bg-secondary: #4a5d78; /* Steel blue shade */
      --color-bg-tertiary: #3a4a5e; /* Darker steel blue for contrast */
      --color-text-primary: #ffffff;
      --color-text-secondary: #cccccc;
    }

    .ai-threat-meter {
      background-color: var(--color-bg-secondary);
      color: var(--color-text-primary);
      padding: 1rem;
      border-radius: 8px;
      text-align: center;
      margin-bottom: 2rem;
    }

    .meter {
      background-color: var(--color-bg-tertiary);
      height: 20px;
      border-radius: 10px;
      overflow: hidden;
      margin: 1rem 0;
    }

    .meter-fill {
      height: 100%;
      transition: width 0.5s ease-in-out, background-color 0.5s ease-in-out;
    }

    h2 {
      font-size: 1.5rem;
      margin-bottom: 1rem;
      color: var(--color-text-primary);
    }

    p {
      font-size: 1.2rem;
      font-weight: bold;
      color: var(--color-text-primary);
    }

    small {
      font-style: italic;
      color: var(--color-text-secondary);
    }
  </style>