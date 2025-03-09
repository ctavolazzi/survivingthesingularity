<script>
  import { onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';

  // Handle class properly - In Svelte, we use class directly
  let cssClass = "";
  export { cssClass as class };

  // Future predictions data with essential fields
  const predictions = [
    {
      id: 1,
      year: "2025-2027",
      title: "Artificial General Intelligence Milestone",
      description: "The first AI system demonstrating capabilities across multiple domains at human-level performance, marking a significant step toward AGI.",
      confidence: "Medium",
      impact: "High",
      color: "#3b82f6" // Blue
    },
    {
      id: 2,
      year: "2028-2030",
      title: "Brain-Computer Interface Revolution",
      description: "Widespread adoption of non-invasive BCIs for everyday use, enabling direct mental control of devices and preliminary thought-to-text communication.",
      confidence: "Medium",
      impact: "Very High",
      color: "#8b5cf6" // Purple
    },
    {
      id: 3,
      year: "2032-2035",
      title: "Quantum Computing Breakthrough",
      description: "Practical quantum computers solving previously intractable problems, revolutionizing fields from materials science to drug discovery and AI training.",
      confidence: "Medium-High",
      impact: "Transformative",
      color: "#ec4899" // Pink
    },
    {
      id: 4,
      year: "2040-2045",
      title: "Technological Singularity Threshold",
      description: "The potential point at which technological growth becomes uncontrollable and irreversible, resulting in unforeseeable changes to human civilization.",
      confidence: "Speculative",
      impact: "Civilization-Altering",
      color: "#f59e0b" // Amber
    }
  ];

  let expandedItem = null;

  function toggleExpand(id) {
    expandedItem = expandedItem === id ? null : id;
  }

  // Calculate progress percentage toward singularity
  function calculateProgress() {
    const now = new Date();
    const startYear = 2023;
    const endYear = 2045;
    const totalYears = endYear - startYear;
    const yearsPassed = now.getFullYear() - startYear + (now.getMonth()/12);
    return Math.min(Math.max((yearsPassed / totalYears) * 100, 0), 100);
  }

  const singularityProgress = calculateProgress();
</script>

<div class="future-predictions-wrapper {cssClass}">
  <div class="future-predictions rounded-lg max-w-4xl mx-auto">
    <div class="future-header">
      <h2 class="future-title">
        <span class="title-highlight">Future</span> Predictions
        <div class="title-decoration"></div>
      </h2>

      <p class="subtitle">
        Based on extensive research and analysis from "Surviving the Singularity"
      </p>

      <!-- Removing the entire singularity timeline section -->
    </div>

    <div class="predictions-container">
      <div class="timeline-container">
        {#each predictions as prediction}
          <div class="timeline-item" class:expanded={expandedItem === prediction.id}>
            <div class="timeline-connector">
              <div class="timeline-line" style="background-color: {prediction.color}"></div>
              <div class="timeline-dot" style="background-color: {prediction.color}"></div>
            </div>

            <div class="timeline-content">
              <div class="year-badge" style="background-color: {prediction.color}">{prediction.year}</div>
              <h3 class="prediction-title">{prediction.title}</h3>
              <p class="prediction-desc">{prediction.description}</p>

              <div class="prediction-meta">
                <div class="meta-item">
                  <span class="meta-label">Confidence:</span>
                  <div class="confidence-value" style="color: {prediction.color}">
                    {prediction.confidence}
                  </div>
                </div>

                <div class="meta-item">
                  <span class="meta-label">Impact:</span>
                  <div class="impact-value" style="color: {prediction.color}">
                    {prediction.impact}
                  </div>
                </div>
              </div>

              <button
                class="learn-more"
                style="color: {prediction.color}"
                on:click={() => toggleExpand(prediction.id)}
              >
                {expandedItem === prediction.id ? 'Show Less' : 'Learn More'}
              </button>

              {#if expandedItem === prediction.id}
                <div class="expanded-content" in:slide={{ duration: 300 }}>
                  <div class="implications">
                    <h4>Potential Implications:</h4>
                    <ul>
                      <li>Economic shifts in labor markets and wealth distribution</li>
                      <li>New ethical and philosophical questions about consciousness and identity</li>
                      <li>Geopolitical power realignment based on technology leadership</li>
                      <li>Transformative impacts on healthcare, education, and governance</li>
                    </ul>
                  </div>
                </div>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    </div>
    <!--
    <div class="future-footer">
      <a href="/book" class="cta-button">
        <span>Explore Book Preview</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14"></path>
          <path d="m12 5 7 7-7 7"></path>
        </svg>
      </a>

      <a href="/discord" class="cta-button discord">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 127.14 96.36" fill="currentColor">
          <path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74S54,46,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5-12.74,11.44-12.74S96.23,46,96.12,53,91.08,65.69,84.69,65.69Z"></path>
        </svg>
        <span>Join the Discord</span>
      </a>
    </div> -->
  </div>
</div>

<style>
  /* Main container */
  .future-predictions-wrapper {
    margin: 1rem 0 1rem;
    overflow-x: hidden; /* Prevent horizontal overflow on small screens */
  }

  .future-predictions {
    background-color: #0c1424;
    padding: 2.5rem 2rem 2rem;
    color: #f1f5f9;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  }

  /* Header section */
  .future-header {
    margin-bottom: 3rem;
    text-align: center;
  }

  .future-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
    color: white;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    position: relative;
    display: inline-block;
    padding: 0 0.5rem 0.5rem;
    z-index: 1; /* Ensure text is above the backlight */
  }

  .future-title::before {
    content: "";
    position: absolute;
    top: -25%;
    left: -20%;
    width: 140%;
    height: 150%;
    background: radial-gradient(
      ellipse at center,
      rgba(59, 130, 246, 0.45) 0%,
      rgba(139, 92, 246, 0.4) 40%,
      rgba(236, 72, 153, 0.35) 70%,
      rgba(15, 23, 42, 0) 100%
    );
    z-index: -1;
    border-radius: 50%;
    filter: blur(12px);
    opacity: 0.9;
    animation: backlight-pulse 5s ease-in-out infinite alternate;
    pointer-events: none;
    box-shadow:
      0 0 20px rgba(59, 130, 246, 0.4),
      0 0 40px rgba(139, 92, 246, 0.3),
      0 0 60px rgba(236, 72, 153, 0.2);
  }

  @keyframes backlight-pulse {
    0% {
      transform: scale(1);
      opacity: 0.8;
    }
    50% {
      transform: scale(1.15);
      opacity: 1;
    }
    100% {
      transform: scale(1);
      opacity: 0.8;
    }
  }

  .title-highlight {
    background: linear-gradient(270deg, #3b82f6, #8b5cf6, #ec4899, #8b5cf6, #3b82f6);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    position: relative;
    animation: gradientAnimation 8s ease infinite;
  }

  @keyframes gradientAnimation {
    0% { background-position: 0% 50% }
    50% { background-position: 100% 50% }
    100% { background-position: 0% 50% }
  }

  .title-decoration {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, #ec4899, transparent);
    border-radius: 3px;
    animation: glowPulse 3s ease-in-out infinite;
  }

  @keyframes glowPulse {
    0% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.5); }
    50% { box-shadow: 0 0 15px rgba(236, 72, 153, 0.7); }
    100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.5); }
  }

  .subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-bottom: 2.5rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
  }

  /* Timeline items */
  .timeline-container {
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
    position: relative;
  }

  .timeline-item {
    display: flex;
    position: relative;
    transition: transform 0.2s ease;
  }

  .timeline-connector {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-right: 1.5rem;
    flex-shrink: 0;
    width: 40px;
  }

  .timeline-line {
    width: 2px;
    height: 100%;
    margin-bottom: -10px;
    opacity: 0.4;
  }

  .timeline-dot {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    margin-bottom: 10px;
    border: 2px solid #0f172a;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 2;
  }

  .timeline-content {
    flex: 1;
    background-color: #1a2234;
    border-radius: 10px;
    padding: 1.5rem;
    position: relative;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
  }

  .timeline-content:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  .timeline-item.expanded .timeline-content {
    background-color: #1a2336;
  }

  .year-badge {
    position: absolute;
    top: -12px;
    left: 20px;
    padding: 4px 12px;
    border-radius: 20px;
    color: white;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    letter-spacing: 0.01em;
  }

  .prediction-title {
    color: white;
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    padding-top: 0.75rem;
    line-height: 1.3;
    letter-spacing: -0.01em;
  }

  .prediction-desc {
    color: #cbd5e1;
    margin-bottom: 1.25rem;
    line-height: 1.6;
    font-size: 1rem;
  }

  /* Confidence and impact */
  .prediction-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    margin-bottom: 1.25rem;
    background-color: rgba(15, 23, 42, 0.4);
    padding: 0.75rem 1rem;
    border-radius: 6px;
  }

  .meta-item {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .meta-label {
    color: #94a3b8;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
  }

  .confidence-value,
  .impact-value {
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.01em;
  }

  /* Learn more button */
  .learn-more {
    display: inline-flex;
    background: none;
    border: none;
    padding: 0.5rem 0;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    letter-spacing: 0.01em;
  }

  .learn-more:hover {
    transform: translateX(3px);
  }

  /* Expanded content */
  .expanded-content {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #334155;
  }

  .implications h4 {
    color: white;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
  }

  .implications ul {
    color: #cbd5e1;
    padding-left: 1.75rem;
    list-style-type: disc;
  }

  .implications li {
    margin-bottom: 0.75rem;
    line-height: 1.6;
  }

  /* Footer */
  .future-footer {
    margin-top: 3.5rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.25rem;
  }

  .cta-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.85rem 1.75rem;
    background-color: #3b82f6;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.2s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    letter-spacing: 0.01em;
  }

  .cta-button:hover {
    background-color: #2563eb;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  .cta-button.discord {
    background-color: #5865F2;
  }

  .cta-button.discord:hover {
    background-color: #4752c4;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .future-predictions {
      padding: 2rem 1.5rem;
    }

    .future-title {
      font-size: 2rem;
    }

    .future-title::before {
      top: -15%;
      left: -10%;
      width: 120%;
      height: 130%;
      filter: blur(10px);
      box-shadow:
        0 0 15px rgba(59, 130, 246, 0.4),
        0 0 30px rgba(139, 92, 246, 0.3),
        0 0 45px rgba(236, 72, 153, 0.2);
    }

    .prediction-meta {
      flex-direction: column;
      gap: 1rem;
      padding: 0.75rem;
    }

    .timeline-content {
      padding: 1.25rem;
    }

    .prediction-title {
      font-size: 1.25rem;
    }
  }

  @media (max-width: 640px) {
    .future-predictions {
      padding: 1.5rem 1rem;
    }

    .future-title {
      font-size: 1.75rem;
    }

    .future-title::before {
      top: -10%;
      left: -5%;
      width: 110%;
      height: 120%;
      filter: blur(8px);
      box-shadow:
        0 0 10px rgba(59, 130, 246, 0.4),
        0 0 20px rgba(139, 92, 246, 0.3),
        0 0 30px rgba(236, 72, 153, 0.2);
    }

    .timeline-dot {
      width: 20px;
      height: 20px;
    }

    .timeline-connector {
      padding-right: 1rem;
      width: 30px;
    }

    .future-footer {
      flex-direction: column;
      align-items: stretch;
    }

    .cta-button {
      width: 100%;
      justify-content: center;
    }
  }
</style>