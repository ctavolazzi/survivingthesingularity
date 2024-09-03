<script>
    import { onMount } from 'svelte';
    import { scale } from 'svelte/transition';
    import { elasticOut } from 'svelte/easing';
  
    let aiThreatLevel = 50;
  
    function updateThreatLevel() {
      aiThreatLevel = Math.floor(Math.random() * 100);
    }
  
    function getThreatColor(level) {
      if (level <= 33) return '#4caf50';
      if (level <= 66) return '#ffc107';
      return '#f44336';
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
    .ai-threat-meter {
      background-color: #f0f0f0;
      padding: 1rem;
      border-radius: 8px;
      text-align: center;
      margin-bottom: 2rem;
    }
  
    .meter {
      background-color: #e0e0e0;
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
    }
  
    p {
      font-size: 1.2rem;
      font-weight: bold;
    }
  
    small {
      font-style: italic;
    }
  </style>