<script>
  import { onMount } from 'svelte';
  import technologies from '$lib/data/technologies.json';
  import { fade, slide } from 'svelte/transition';

  // Function to get status indicator
  function getStatusIndicator(technology) {
    const satisfactionLevel = getSatisfactionLevel(technology);
    if (satisfactionLevel >= 0.8) return '✅';
    if (satisfactionLevel >= 0.4) return '~';
    return '✕';
  }

  // Function to get the overall satisfaction level
  function getSatisfactionLevel(technology) {
    if (!technology.articles.length) return 0;
    return technology.articles.reduce((acc, article) => acc + article.satisfactionLevel, 0) / technology.articles.length;
  }

  // Function to format date
  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  // Track expanded state for each article and FAQ
  let expandedArticles = new Set();
  let expandedFAQs = new Set();

  function toggleArticle(articleId) {
    if (expandedArticles.has(articleId)) {
      expandedArticles.delete(articleId);
    } else {
      expandedArticles.add(articleId);
    }
    expandedArticles = expandedArticles; // Trigger reactivity
  }

  function toggleFAQ(faqId) {
    if (expandedFAQs.has(faqId)) {
      expandedFAQs.delete(faqId);
    } else {
      expandedFAQs.add(faqId);
    }
    expandedFAQs = expandedFAQs; // Trigger reactivity
  }
</script>

<div class="agi-roadmap bg-gray-900 rounded-xl p-8 shadow-2xl border border-gray-800">
  <h2 class="text-4xl font-bold text-center mb-12 text-white" in:fade>What's Next?</h2>

  <div class="space-y-16">
    {#each technologies.technologies as technology}
      <div class="technology-item" in:fade={{ duration: 400, delay: 200 }}>
        <!-- Header with Status -->
        <div class="flex items-center gap-4 mb-6">
          <div class="status-indicator text-2xl bg-gray-800 rounded-full p-2 w-12 h-12 flex items-center justify-center border border-gray-700">
            {getStatusIndicator(technology)}
          </div>
          <h3 class="text-3xl font-bold text-white">{technology.name}</h3>
        </div>

        <!-- Description -->
        <p class="text-gray-300 text-lg mb-8 leading-relaxed">{technology.description}</p>

        <!-- FAQ Section -->
        <div class="faq-section mb-8">
          <h4 class="text-xl font-semibold mb-4 text-white">FAQ</h4>
          <div class="space-y-3">
            {#each technology.faq as faq, index}
              <div
                class="faq-item bg-gray-800 rounded-lg overflow-hidden border border-gray-700 hover:border-gray-600 transition-all duration-300"
                on:click={() => toggleFAQ(`${technology.name}-${index}`)}
                role="button"
                tabindex="0"
              >
                <div class="p-4 cursor-pointer flex justify-between items-center">
                  <p class="font-medium text-white">{faq.question}</p>
                  <span class="text-gray-400 transform transition-transform duration-300" class:rotate-180={expandedFAQs.has(`${technology.name}-${index}`)}>
                    ▼
                  </span>
                </div>
                {#if expandedFAQs.has(`${technology.name}-${index}`)}
                  <div class="px-4 pb-4" transition:slide={{ duration: 300 }}>
                    <p class="text-gray-300">{faq.answer}</p>
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        </div>

        <!-- Supporting Data -->
        <div class="supporting-data">
          <h4 class="text-xl font-semibold mb-3 text-white">Supporting Data</h4>
          <div class="space-y-3">
            {#each technology.articles as article}
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                class="block bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors border border-gray-700/50 overflow-hidden"
              >
                <div class="flex items-start p-4">
                  <!-- Article Thumbnail -->
                  <div class="article-thumbnail w-20 h-20 bg-gray-700/50 rounded-md overflow-hidden flex-shrink-0">
                    {#if article.thumbnail}
                      <img
                        src={article.thumbnail}
                        alt={article.title}
                        class="w-full h-full object-cover"
                      />
                    {:else}
                      <div class="w-full h-full flex items-center justify-center text-gray-400">
                        📄
                      </div>
                    {/if}
                  </div>

                  <div class="flex-grow px-4">
                    <!-- Title and Date -->
                    <div class="flex flex-col">
                      <h3 class="text-lg font-medium text-white mb-1">{article.title}</h3>
                      <p class="text-sm text-gray-400">{formatDate(article.date)}</p>
                    </div>
                  </div>

                  <!-- Chevron Icon -->
                  <div class="text-gray-400 self-center">
                    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 6L15 12L9 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                </div>
              </a>
            {/each}
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .agi-roadmap {
    background: linear-gradient(to bottom, rgba(17, 24, 39, 0.95), rgba(17, 24, 39, 0.98));
    backdrop-filter: blur(10px);
  }

  .technology-item {
    position: relative;
  }

  .technology-item::after {
    content: '';
    position: absolute;
    bottom: -2rem;
    left: 10%;
    width: 80%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(75, 85, 99, 0.3), transparent);
  }

  .technology-item:last-child::after {
    display: none;
  }

  .status-indicator {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  }

  .faq-item:hover, .article-accordion:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }

  /* Ensure smooth transitions */
  .faq-item, .article-accordion {
    transition: all 0.3s ease;
  }

  /* Improve focus states for accessibility */
  .faq-item:focus-visible, .article-accordion button:focus-visible {
    outline: 2px solid #60A5FA;
    outline-offset: 2px;
  }

  /* Custom scrollbar for webkit browsers */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: rgba(17, 24, 39, 0.95);
  }

  ::-webkit-scrollbar-thumb {
    background: rgba(75, 85, 99, 0.5);
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: rgba(75, 85, 99, 0.7);
  }

  .article-thumbnail img {
    transition: transform 0.3s ease;
  }

  .article-thumbnail:hover img {
    transform: scale(1.05);
  }

  .supporting-data {
    margin-top: 1.5rem;
  }

  .supporting-data a {
    transition: all 0.2s ease;
  }

  .supporting-data a:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .supporting-data a:hover .text-gray-400 {
    color: #ffffff;
  }
</style>