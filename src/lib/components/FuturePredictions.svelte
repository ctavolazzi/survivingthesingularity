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

  let visible = false;

  onMount(() => {
    // Simple animation delay
    setTimeout(() => {
      visible = true;
    }, 500);
  });
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
          <li class="mb-10" in:fly={{ y: 20, delay: index * 150, duration: 400 }}>
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
    <p class="text-gray-700 dark:text-gray-300">
      Want to explore these predictions in depth?
    </p>
    <div class="text-center">
      <a href="/book" class="inline-block mt-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg">
        Read a Sample
      </a>
    </div>
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

  /* Mobile optimization */
  @media (max-width: 640px) {
    .future-predictions {
      padding: 1rem;
    }

    .future-footer {
      padding: 1rem;
    }
  }
</style>