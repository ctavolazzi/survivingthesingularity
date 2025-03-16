<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import { fly, scale } from 'svelte/transition'; // Import Svelte transitions
  import { quintOut } from 'svelte/easing'; // Import easing function
  import { writable } from 'svelte/store';

  // Image imports
  // const codeImagePath = '/images/code-conductor.webp'; // Not needed anymore
  const heroBackgroundImage = '/images/code-conductor-hero.webp'; // Updated path to use static folder

  // Download state
  let isDownloading = false;
  let isPaying = false;
  let isContributing = false; // New state for contribution modal
  let paymentAmount = 5; // Default suggested amount
  let paymentUrl = 'https://github.com/ctavolazzi/code-conductor'; // Updated with correct URL and casing

  // Reference to the contribute button for animations
  let contributeButton;
  let buttonRect = { x: 0, y: 0, width: 0, height: 0 };

  // Modal reference
  let modalContent;
  let modalBackdrop;

  // Function to handle modal closing when clicking outside
  function handleOutsideClick(event) {
    if (isContributing && modalContent && !modalContent.contains(event.target)) {
      isContributing = false;
    }
  }

  // Use onMount to handle browser-only code
  onMount(() => {
    // Watch for changes to isContributing and add/remove event listener accordingly
    const unsubscribe = isContributing$.subscribe(value => {
      if (value) {
        // Small delay to avoid the same click that opens the modal from closing it
        setTimeout(() => {
          document.addEventListener('mousedown', handleOutsideClick);
        }, 0);
      } else {
        document.removeEventListener('mousedown', handleOutsideClick);
      }
    });

    // Clean up on component unmount
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
      unsubscribe();
    };
  });

  // Create a store to track isContributing
  const isContributing$ = writable(false);

  // Keep the store in sync with the variable
  $: {
    isContributing$.set(isContributing);
  }

  // Removing fake testimonials

  // Benefits
  const benefits = [
    {
      title: "Never Lose Your Work",
      description: "Every session picks up exactly where you left off.",
      icon: "🔄"
    },
    {
      title: "Keep Your AI on Task",
      description: "Structured markdown documents keep your AI assistance laser-focused.",
      icon: "🎯"
    },
    {
      title: "Instant Context Recall",
      description: "Effortlessly retrieve related tasks, notes, and ideas to guide your AI.",
      icon: "🧠"
    },
    {
      title: "Human-Friendly, AI-Ready",
      description: "Plain text organization means easy management, future-proof flexibility, and compatibility with any LLM.",
      icon: "🤝"
    }
  ];

  // Features
  const features = [
    {
      title: "Automated Workflow Runner",
      description: "Structured guidance to streamline development.",
      icon: "✅"
    },
    {
      title: "Obsidian-Style Linking",
      description: "Effortlessly link ideas, workflows, and context.",
      icon: "✅"
    },
    {
      title: "Folder-Based Management",
      description: "Keep project resources organized and accessible.",
      icon: "✅"
    },
    {
      title: "Hardware-Agnostic",
      description: "Runs smoothly on any machine, any LLM.",
      icon: "✅"
    }
  ];

  // Customization options
  const customizations = [
    {
      title: "Use Your Preferred Tools",
      description: "Works with Cursor, VSCode, Obsidian, or any text editor—it's just markdown!",
      icon: "🛠️"
    },
    {
      title: "Create Your Own Interface",
      description: "Design your own workflow and organization system using our building blocks.",
      icon: "🎨"
    },
    {
      title: "Contribute & Extend",
      description: "Open source on GitHub—add features, templates, or entirely new modules.",
      icon: "🌱"
    },
    {
      title: "Agentic Workflow Ready",
      description: "Feed these structured documents into agents and watch them take off.",
      icon: "🚀"
    }
  ];

  // Download functions
  async function downloadFromGitHub() {
    isDownloading = true;
    window.open(paymentUrl, '_blank');
    // Simulate download time
    await new Promise(resolve => setTimeout(resolve, 2000));
    isDownloading = false;
  }

  function handlePaymentClick() {
    isPaying = true;
  }

  function handleContributeClick() {
    // Get the position and size of the contribute button for animation origin
    if (contributeButton) {
      const rect = contributeButton.getBoundingClientRect();
      buttonRect = {
        x: rect.x,
        y: rect.y,
        width: rect.width,
        height: rect.height
      };
    }
    isContributing = true;
  }

  function handlePaymentSubmit() {
    // Here you would actually process the payment
    // For now, we'll just redirect to GitHub as a placeholder
    window.open(paymentUrl, '_blank');
    isPaying = false;
  }
</script>

<div class="main-content">
  <div class="hero-section text-white py-16 px-4 md:py-24" style="background-image: url('{heroBackgroundImage}'); background-size: cover; background-position: center; position: relative;">
    <!-- Darker gradient overlay for better text readability -->
    <div class="absolute inset-0 bg-gradient-to-b from-black/90 via-black/70 to-black/90"></div>

    <div class="container mx-auto max-w-4xl text-center relative z-10">
      <!-- Clean, unified header container -->
      <div class="glass-panel backdrop-blur-sm p-12 rounded-2xl bg-black/50 border border-white/10 shadow-2xl mx-auto">
        <!-- Main heading -->
        <h1 class="text-5xl md:text-7xl font-bold mb-5 text-shadow-xl text-white">Code Conductor</h1>

        <!-- Subtitle with gradient underline -->
        <div class="relative inline-block mb-10">
          <p class="text-xl md:text-3xl font-bold text-shadow-md">AI Context Management System</p>
          <div class="h-1 w-full bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mt-2"></div>
        </div>

        <!-- Description with improved spacing -->
        <p class="text-lg md:text-xl mb-12 max-w-2xl mx-auto">
          A lightweight, markdown-based system for AI-driven workflows. Works with Cursor, VSCode, Obsidian, or any text editor.
        </p>

        <!-- Button container with improved spacing -->
        <div class="flex flex-col md:flex-row justify-center gap-8 mb-8">
          <button on:click={downloadFromGitHub}
            class="download-button bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white px-8 py-4 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
            class:downloading={isDownloading}
            disabled={isDownloading}>
            {isDownloading ? 'Opening...' : 'Download Now'}
            <span class="button-icon ml-2">{isDownloading ? '⟳' : '↓'}</span>
          </button>
          <button on:click={handleContributeClick}
            bind:this={contributeButton}
            class="pay-button bg-transparent border-2 border-white/80 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white/10 transition-all">
            Contribute
          </button>
        </div>
        <p class="text-white/80 text-sm">Immediate productivity with no complex installation</p>
      </div>
    </div>
  </div>

  <div class="setup-section py-16 px-4 bg-white dark:bg-gray-800">
    <div class="container mx-auto max-w-4xl text-center">
      <h2 class="text-3xl font-bold mb-6 dark:text-white">Set Up in Seconds</h2>
      <p class="text-lg max-w-3xl mx-auto mb-10 dark:text-gray-300">
        No complex installation. No dependencies. No learning curve. Just download, open, and start working.
      </p>

      <!-- Improved installation command display -->
      <div class="install-command-container mx-auto mb-12 max-w-2xl">
        <div class="bg-gray-900 rounded-xl overflow-hidden shadow-xl">
          <div class="flex items-center bg-gray-800 px-4 py-2">
            <div class="flex space-x-1 mr-auto">
              <div class="w-3 h-3 rounded-full bg-red-500"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div class="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <span class="text-gray-400 text-sm">Terminal</span>
          </div>
          <div class="p-4 text-left">
            <div class="flex items-start">
              <span class="text-green-400 mr-2">$</span>
              <code class="text-white text-base font-mono">pip install code-conductor</code>
            </div>
            <p class="text-gray-400 text-xs mt-3 border-t border-gray-700 pt-3">For the most up-to-date version, check <a href="https://github.com/ctavolazzi/code-conductor" class="text-blue-400 hover:underline" target="_blank">GitHub</a></p>
          </div>
        </div>
      </div>

      <div class="steps-container flex flex-col md:flex-row justify-center gap-8 mb-8">
        <div class="step p-6 rounded-lg bg-blue-50 dark:bg-gray-700 text-center w-full md:w-1/3">
          <div class="step-number bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">1</div>
          <h3 class="text-xl font-semibold mb-2 dark:text-white">Download</h3>
          <p class="dark:text-gray-300">Install with pip or clone from GitHub</p>
        </div>

        <div class="step p-6 rounded-lg bg-blue-50 dark:bg-gray-700 text-center w-full md:w-1/3">
          <div class="step-number bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">2</div>
          <h3 class="text-xl font-semibold mb-2 dark:text-white">Open</h3>
          <p class="dark:text-gray-300">Use with Cursor, VSCode, Obsidian, or any text editor</p>
        </div>

        <div class="step p-6 rounded-lg bg-blue-50 dark:bg-gray-700 text-center w-full md:w-1/3">
          <div class="step-number bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">3</div>
          <h3 class="text-xl font-semibold mb-2 dark:text-white">Create</h3>
          <p class="dark:text-gray-300">Start your first work effort and watch productivity soar</p>
        </div>
      </div>
    </div>
  </div>

  <div class="how-it-works-section py-16 px-4 bg-gray-50 dark:bg-gray-900">
    <div class="container mx-auto max-w-4xl">
      <h2 class="text-3xl font-bold text-center mb-6 dark:text-white">How It Works</h2>

      <p class="text-lg text-center max-w-3xl mx-auto mb-12 dark:text-gray-300">
        Built for use with tools like <span class="font-bold">Cursor</span> and <span class="font-bold">Obsidian</span>, this system leverages simple, powerful markdown documents interconnected with intuitive Obsidian-style links. It's your AI's persistent memory, allowing seamless context retrieval, focused tasks, and effortless expansion.
      </p>

      <div class="integration-icons flex justify-center gap-12 mb-12">
        <div class="text-center">
          <div class="text-5xl mb-3">💻</div>
          <div class="font-semibold dark:text-white">Cursor</div>
        </div>
        <div class="text-center">
          <div class="text-5xl mb-3">🔄</div>
          <div class="font-semibold dark:text-white">Seamless Integration</div>
        </div>
        <div class="text-center">
          <div class="text-5xl mb-3">🔮</div>
          <div class="font-semibold dark:text-white">Obsidian</div>
        </div>
      </div>
    </div>
  </div>

  <div class="benefits-section py-16 px-4 bg-white dark:bg-gray-800">
    <div class="container mx-auto max-w-4xl">
      <h2 class="text-3xl font-bold text-center mb-12 dark:text-white">Key Benefits</h2>

      <div class="benefits-grid grid md:grid-cols-2 gap-8">
        {#each benefits as benefit}
          <div class="benefit-card p-6 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-md transition-all">
            <div class="benefit-icon text-4xl mb-4">{benefit.icon}</div>
            <h3 class="text-xl font-semibold mb-2 dark:text-white">{benefit.title}</h3>
            <p class="dark:text-gray-300">{benefit.description}</p>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="customization-section py-16 px-4 bg-gradient-to-br from-purple-700 to-indigo-800 text-white">
    <div class="container mx-auto max-w-4xl">
      <h2 class="text-3xl font-bold text-center mb-6">Make It Your Own</h2>
      <p class="text-lg text-center max-w-3xl mx-auto mb-12">
        Use it <span class="italic">exactly</span> how you want. These highly modular building blocks become powerful inputs for agentic workflows, handling an immense amount of work with an incredibly lightweight system.
      </p>

      <div class="customization-grid grid md:grid-cols-2 gap-8">
        {#each customizations as customization}
          <div class="customization-card p-6 rounded-lg bg-white/10 hover:bg-white/15 transition-all">
            <div class="customization-icon text-4xl mb-4">{customization.icon}</div>
            <h3 class="text-xl font-semibold mb-2">{customization.title}</h3>
            <p class="text-white/90">{customization.description}</p>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="features-section py-16 px-4 bg-gray-50 dark:bg-gray-900">
    <div class="container mx-auto max-w-4xl">
      <h2 class="text-3xl font-bold text-center mb-12 dark:text-white">Features You'll Love</h2>

      <div class="features-grid grid md:grid-cols-2 gap-6">
        {#each features as feature}
          <div class="feature-card p-6 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:shadow-md transition-all">
            <div class="flex items-start">
              <div class="feature-icon text-2xl text-green-500 mr-4">{feature.icon}</div>
              <div>
                <h3 class="text-lg font-semibold mb-1 dark:text-white">{feature.title}</h3>
                <p class="dark:text-gray-300">{feature.description}</p>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="use-cases-section py-16 px-4 bg-white dark:bg-gray-800">
    <div class="container mx-auto max-w-4xl">
      <h2 class="text-3xl font-bold text-center mb-12 dark:text-white">Build Anything You Want</h2>

      <div class="use-cases-container">
        <div class="use-case mb-12 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h3 class="text-xl font-semibold mb-4 dark:text-white">Infinite Ways to Use It</h3>
          <ul class="grid md:grid-cols-2 gap-4 pl-5 dark:text-gray-300 list-disc">
            <li>Personal coding assistant with memory</li>
            <li>Team collaboration knowledge base</li>
            <li>Research organization system</li>
            <li>Project documentation hub</li>
            <li>Agentic workflow framework</li>
            <li>Cross-project knowledge linking</li>
            <li>LLM context management</li>
            <li>Custom development workflows</li>
          </ul>
        </div>

        <div class="quote-container p-6 bg-blue-50 dark:bg-gray-700 rounded-lg text-center">
          <p class="text-xl italic mb-0 dark:text-white">
            "Build anything you want with this easy-to-use, easy-to-customize method of working with AI LLMs."
          </p>
        </div>
      </div>
    </div>
  </div>

  <div class="github-section py-16 px-4 bg-white dark:bg-gray-800">
    <div class="container mx-auto max-w-4xl text-center">
      <h2 class="text-3xl font-bold mb-6 dark:text-white">Contribute on GitHub</h2>
      <p class="text-lg max-w-3xl mx-auto mb-10 dark:text-gray-300">
        This is an evolving, community-driven project. Add your own templates, workflows, or entirely new features. The possibilities are endless.
      </p>

      <div class="github-button-container">
        <a href={paymentUrl} target="_blank" class="inline-flex items-center px-8 py-4 bg-gray-800 text-white rounded-lg font-semibold text-lg hover:bg-gray-700 transition-all">
          <svg class="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path></svg>
          View on GitHub
        </a>
      </div>
    </div>
  </div>

  <div class="cta-section py-16 px-4 bg-gradient-to-br from-indigo-800 to-blue-600 text-white">
    <div class="container mx-auto max-w-4xl text-center">
      <h2 class="text-3xl font-bold mb-6">Getting Started is Easy</h2>
      <p class="text-xl mb-8">Experience immediate productivity with your AI workflows.</p>

      <div class="flex flex-col md:flex-row justify-center gap-6 mb-6">
        <button on:click={downloadFromGitHub}
          class="download-button bg-white text-indigo-800 px-8 py-4 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
          class:downloading={isDownloading}
          disabled={isDownloading}>
          {isDownloading ? 'Opening...' : 'Download From GitHub'}
          <span class="button-icon ml-2">{isDownloading ? '⟳' : '↓'}</span>
        </button>
      </div>

      <p class="mt-8 text-white/90 text-sm">
        Built by Christopher Tavolazzi (<span class="italic">@thecoffeejesus</span>). Share your journey and keep your AI workflows connected.
      </p>
    </div>
  </div>
</div>

{#if isPaying}
  <div class="payment-modal fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <div class="modal-content bg-white dark:bg-gray-800 rounded-lg p-8 max-w-md w-full">
      <h3 class="text-2xl font-bold mb-4 dark:text-white">Support This Project</h3>
      <p class="mb-6 dark:text-gray-300">Choose an amount you think is fair. Your support helps us continue development.</p>

      <div class="amount-selector flex flex-wrap gap-3 mb-6">
        {#each [0, 5, 10, 20, 50] as amount}
          <button
            class="px-4 py-2 rounded border border-gray-300 dark:border-gray-600 {paymentAmount === amount ? 'bg-indigo-600 text-white' : 'dark:text-white'}"
            on:click={() => paymentAmount = amount}>
            {amount === 0 ? 'Free' : `$${amount}`}
          </button>
        {/each}
        <input
          type="number"
          class="px-4 py-2 rounded border border-gray-300 dark:border-gray-600 w-24 dark:bg-gray-700 dark:text-white"
          bind:value={paymentAmount}
          min="0"
        />
      </div>

      <div class="flex gap-4">
        <button
          class="flex-1 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-white px-4 py-2 rounded"
          on:click={() => isPaying = false}>
          Cancel
        </button>
        <button
          class="flex-1 bg-indigo-600 text-white px-4 py-2 rounded"
          on:click={handlePaymentSubmit}>
          {paymentAmount === 0 ? 'Download Free' : `Pay $${paymentAmount}`}
        </button>
      </div>
    </div>
  </div>
{/if}

{#if isContributing}
  <div
    bind:this={modalBackdrop}
    class="fixed inset-0 bg-black bg-opacity-80 z-50"
    on:click|self={() => isContributing = false}
    role="presentation"
    on:keydown={(e) => e.key === 'Escape' && (isContributing = false)}
    tabindex="-1"
  ></div>
  <div
    bind:this={modalContent}
    class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md bg-gray-900 text-white rounded-xl p-6 sm:p-8 shadow-2xl border border-gray-700 z-[100]"
  >
    <h3 class="text-2xl font-bold mb-4">Contribute to Code Conductor</h3>

    <p class="mb-4 text-gray-300">
      The best way to contribute to Code Conductor is on GitHub:
    </p>

    <div class="mb-6">
      <div class="p-4 mb-3 rounded-lg border border-gray-700 bg-gray-800/50">
        <h4 class="font-semibold mb-2 text-white flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
          Raise an Issue
        </h4>
        <p class="text-gray-300 text-sm">
          Found a bug or have a feature request? Open an issue on our GitHub repository to let us know.
        </p>
      </div>

      <div class="p-4 mb-3 rounded-lg border border-gray-700 bg-gray-800/50">
        <h4 class="font-semibold mb-2 text-white flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M6 2c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6H6zm7 7V3.5L18.5 9H13z"/></svg>
          Make a Pull Request
        </h4>
        <p class="text-gray-300 text-sm">
          Want to contribute code? Fork the repository, make your changes, and submit a pull request.
        </p>
      </div>

      <div class="p-4 rounded-lg border border-gray-700 bg-gray-800/50">
        <h4 class="font-semibold mb-2 text-white flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
          Review Code
        </h4>
        <p class="text-gray-300 text-sm">
          Help review pull requests from other contributors and provide feedback.
        </p>
      </div>
    </div>

    <div class="flex gap-4 mt-6">
      <button
        class="flex-1 bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
        on:click={() => isContributing = false}>
        Close
      </button>
      <a
        href={paymentUrl}
        target="_blank"
        class="flex-1 bg-indigo-600 text-white px-4 py-2 rounded flex items-center justify-center hover:bg-indigo-700 transition-colors"
        on:click={() => isContributing = false}>
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path></svg>
          Go to GitHub
      </a>
    </div>

    <!-- Close button in top right -->
    <button
      class="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
      on:click={() => isContributing = false}
      aria-label="Close modal"
    >
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
      </svg>
    </button>
  </div>
{/if}

<style>
  .main-content {
    width: 100%;
  }

  .hero-section {
    position: relative;
    background-size: cover;
    background-position: center;
  }

  .benefit-card, .feature-card, .customization-card {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .benefit-icon, .customization-icon {
    font-size: 2.5rem;
  }

  .download-button, .pay-button {
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }

  .download-button:hover, .pay-button:hover {
    transform: translateY(-2px);
  }

  .button-icon {
    display: inline-block;
  }

  .downloading .button-icon {
    animation: spin 1s linear infinite;
  }

  /* Glass panel effect */
  .glass-panel {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }

  /* Text shadow classes for better readability */
  .text-shadow-md {
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  .text-shadow-xl {
    text-shadow: 0 6px 12px rgba(0, 0, 0, 0.5), 0 3px 6px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.7);
  }

  /* Custom transitions for the modal */
  :global(.contribution-modal) {
    --transform-origin: center;
  }

  @keyframes spin {
    100% { transform: rotate(360deg); }
  }

  @media (max-width: 768px) {
    .benefits-grid,
    .features-grid,
    .customization-grid {
      grid-template-columns: 1fr;
    }

    .integration-icons {
      flex-direction: column;
      align-items: center;
      gap: 2rem;
    }
  }
</style>

<script context="module">
  // Custom transition function that expands from the button
  function modalIn(node, { duration = 400, buttonRect = null, easing = t => t }) {
    const styles = getComputedStyle(node);
    const transform = styles.transform === 'none' ? '' : styles.transform;

    // Calculate origin based on button position
    let originX = '50%';
    let originY = '50%';
    let startX = 0;
    let startY = 0;

    if (buttonRect) {
      // Get the center of the button relative to viewport
      const buttonCenterX = buttonRect.x + buttonRect.width / 2;
      const buttonCenterY = buttonRect.y + buttonRect.height / 2;

      // Get viewport dimensions
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      // Calculate origin as percentages
      originX = (buttonCenterX / viewportWidth) * 100 + '%';
      originY = (buttonCenterY / viewportHeight) * 100 + '%';

      // Calculate start position for translation (not needed for this specific animation)
      startX = 0;
      startY = 0;
    }

    return {
      duration,
      easing,
      css: t => {
        const scale = t;
        return `
          transform-origin: ${originX} ${originY};
          transform: ${transform} scale(${scale}) translate(${startX * (1-t)}px, ${startY * (1-t)}px);
          opacity: ${t};
        `;
      }
    };
  }

  function modalOut(node, { duration = 300, buttonRect = null, easing = t => t }) {
    const styles = getComputedStyle(node);
    const transform = styles.transform === 'none' ? '' : styles.transform;

    // Calculate origin based on button position (same as modalIn)
    let originX = '50%';
    let originY = '50%';
    let endX = 0;
    let endY = 0;

    if (buttonRect) {
      const buttonCenterX = buttonRect.x + buttonRect.width / 2;
      const buttonCenterY = buttonRect.y + buttonRect.height / 2;

      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      originX = (buttonCenterX / viewportWidth) * 100 + '%';
      originY = (buttonCenterY / viewportHeight) * 100 + '%';

      endX = 0;
      endY = 0;
    }

    return {
      duration,
      easing,
      css: t => {
        const scale = t;
        return `
          transform-origin: ${originX} ${originY};
          transform: ${transform} scale(${scale}) translate(${endX * (1-t)}px, ${endY * (1-t)}px);
          opacity: ${t};
        `;
      }
    };
  }
</script>