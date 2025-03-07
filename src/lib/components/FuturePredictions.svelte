<script>
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';

  // Future predictions data
  const predictions = [
    {
      id: 1,
      year: "2025-2027",
      title: "Artificial General Intelligence Milestone",
      description: "The first AI system demonstrating capabilities across multiple domains at human-level performance, marking a significant step toward AGI.",
      confidence: "Medium",
      impact: "High"
    },
    {
      id: 2,
      year: "2028-2030",
      title: "Brain-Computer Interface Revolution",
      description: "Widespread adoption of non-invasive BCIs for everyday use, enabling direct mental control of devices and preliminary thought-to-text communication.",
      confidence: "Medium",
      impact: "Very High"
    },
    {
      id: 3,
      year: "2032-2035",
      title: "Quantum Computing Breakthrough",
      description: "Practical quantum computers solving previously intractable problems, revolutionizing fields from materials science to drug discovery and AI training.",
      confidence: "Medium-High",
      impact: "Transformative"
    },
    {
      id: 4,
      year: "2040-2045",
      title: "Technological Singularity Threshold",
      description: "The potential point at which technological growth becomes uncontrollable and irreversible, resulting in unforeseeable changes to human civilization.",
      confidence: "Speculative",
      impact: "Civilization-Altering"
    }
  ];

  let visible = true;
</script>

<div class="future-predictions p-4 bg-white dark:bg-gray-800 shadow-md rounded-lg max-w-3xl mx-auto mt-8">
  <div class="future-header">
    <h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-2">Future Predictions</h2>
    <p class="text-center text-gray-600 dark:text-gray-400 mb-6">Based on research from "Surviving the Singularity"</p>
    <hr class="mb-8 border-gray-200 dark:border-gray-700" />
  </div>

  <div class="predictions-container">
    {#if visible}
      <ol class="relative border-l border-blue-300 dark:border-blue-700 pl-4">
        {#each predictions as prediction, index}
          <li class="mb-10" in:fly={{ y: 10, delay: 0, duration: 100 }}>
            <div class="absolute w-3 h-3 bg-blue-300 rounded-full mt-1.5 -left-1.5 border border-white dark:border-gray-900 dark:bg-blue-700"></div>
            <time class="mb-1 text-sm font-normal leading-none text-blue-500 dark:text-blue-400">{prediction.year}</time>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{prediction.title}</h3>
            <p class="mb-2 text-base font-normal text-gray-500 dark:text-gray-400">{prediction.description}</p>
            <div class="flex gap-4 text-sm">
              <span class="text-gray-600 dark:text-gray-400">
                <strong>Confidence:</strong> {prediction.confidence}
              </span>
              <span class="text-gray-600 dark:text-gray-400">
                <strong>Impact:</strong> {prediction.impact}
              </span>
            </div>
          </li>
        {/each}
      </ol>
    {/if}
  </div>

  <div class="future-footer mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-center">
    <p class="text-gray-700 dark:text-gray-300 text-lg font-medium">
      Want to explore these predictions in depth?
    </p>
    <div class="mt-4 flex flex-col md:flex-row gap-4 justify-center items-center">
      <a href="/book" class="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-transform hover:scale-105">
        Explore Book Preview
      </a>
      <a href="/discord" class="discord-button">
        <div class="discord-icon-wrapper">
          <svg class="discord-icon" viewBox="0 -28.5 256 256" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid">
            <path d="M216.856339,16.5966031 C200.285002,8.84328665 182.566144,3.2084988 164.041564,0 C161.766523,4.11318106 159.108624,9.64549908 157.276099,14.0464379 C137.583995,11.0849896 118.072967,11.0849896 98.7430163,14.0464379 C96.9108417,9.64549908 94.1925838,4.11318106 91.8971895,0 C73.3526068,3.2084988 55.6133949,8.86399117 39.0420583,16.6376612 C5.61752293,67.146514 -3.4433191,116.400813 1.08711069,164.955721 C23.2560196,181.510915 44.7403634,191.567697 65.8621325,198.148576 C71.0772151,190.971126 75.7283628,183.341335 79.7352139,175.300261 C72.104019,172.400575 64.7949724,168.822202 57.8887866,164.667963 C59.7209612,163.310589 61.5131304,161.891452 63.2445898,160.431257 C105.36741,180.133187 151.134928,180.133187 192.754523,160.431257 C194.506336,161.891452 196.298154,163.310589 198.110326,164.667963 C191.183787,168.842556 183.854737,172.420929 176.223542,175.320965 C180.230393,183.341335 184.861538,190.991831 190.096624,198.16893 C211.238746,191.588051 232.743023,181.531619 254.911949,164.955721 C260.227747,108.668201 245.831087,59.8662432 216.856339,16.5966031 Z" fill="currentColor"></path>
          </svg>
        </div>
        <span>Join the Discord</span>
        <div class="first-100-badge">First 100 only</div>
      </a>
    </div>
    <p class="mt-4 text-sm text-gray-600 dark:text-gray-400">
      Connect with others preparing for the singularity and get early access to insights.
    </p>
  </div>
</div>

<style>
  .future-predictions {
    position: relative;
    background-image: linear-gradient(to bottom, rgba(255,255,255,0.8), rgba(255,255,255,1));
  }

  :global(.dark) .future-predictions {
    background-image: linear-gradient(to bottom, rgba(31,41,55,0.8), rgba(31,41,55,1));
  }

  .future-header h2 {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-fill-color: transparent;
  }

  .predictions-container {
    position: relative;
  }

  /* Add subtle glow effect to timeline dots */
  .predictions-container li div {
    box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
  }

  /* Discord button styling */
  .discord-button {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #5865F2;
    color: white;
    font-weight: bold;
    padding: 0.75rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    font-size: 1.1rem;
    transition: all 0.2s ease;
    position: relative;
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.3);
    overflow: visible;
  }

  .discord-button:hover {
    background-color: #4752c4;
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 16px rgba(88, 101, 242, 0.4);
  }

  .discord-icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
  }

  .discord-icon {
    width: 24px;
    height: 24px;
  }

  .first-100-badge {
    position: absolute;
    top: -10px;
    right: -10px;
    background: #FF1F8E;
    color: white;
    font-size: 0.7rem;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 12px;
    transform: rotate(5deg);
    box-shadow: 0 2px 6px rgba(255, 31, 142, 0.5);
    z-index: 2;
  }

  /* Mobile optimization */
  @media (max-width: 640px) {
    .future-predictions {
      padding: 1rem;
    }

    .future-footer {
      padding: 1rem;
    }

    .future-footer .flex {
      flex-direction: column;
      gap: 1rem;
    }
  }
</style>