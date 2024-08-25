<script>
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { marked } from 'marked';
  import sampleContent from '$lib/data/sample.md?raw';
  import ContactForm from '$lib/components/ContactForm.svelte';
  import Divider from '$lib/components/Divider.svelte';
  import StSBookImage from '$lib/images/default-blog-image.png';
  import Countdown from '$lib/components/Countdown.svelte';
  import StSFreeGuideImage from '$lib/images/StSFreeGuide.png';

  let showPopup = false;
  const targetDate = new Date("2027-11-20T23:59:59").getTime();

  onMount(() => {
    setTimeout(() => {
      showPopup = true;
    }, 8000); // Show popup after 8 seconds
  });

  function joinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  function backOnKickstarter() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  const parsedContent = marked(sampleContent);

  function handleFormSubmit(event) {
    // Handle form submission
    console.log('Form submitted:', event.detail);
    // Implement your form submission logic here
  }

  function closePopup() {
    showPopup = false;
  }

  function navigateToDownload() {
    window.location.href = '/download';
  }
</script>

<svelte:head>
  <title>Surviving the Singularity: Your Free Guide to Thriving in the AI Era</title>
  <meta name="description" content="Download your free guide on processing AI anxiety and confusion. Join 10,000+ readers preparing for the future of technology.">
</svelte:head>

<main class="container mx-auto px-4 py-8 max-w-3xl dark:bg-gray-800 dark:text-gray-200">
  <header in:fade="{{ duration: 1000 }}">
    <h1 class="text-4xl font-bold mb-4 text-center">Survive and Thrive in the AI Revolution</h1>
    <h2 class="text-2xl mb-8 text-center">The Ultimate Workbook for Processing AI Anxiety and Confusion</h2>
  </header>

  <div class="flex flex-col md:flex-row items-center mb-12">
    <img src={StSBookImage} alt="Surviving the Singularity" class="StS-book-image mb-8 md:mb-0 md:mr-8" />
    <div>
      <ul class="list-disc pl-5 mb-6">
        <li>Practical exercises to process AI-related emotions</li>
        <li>Strategies for adapting to rapid technological change</li>
        <li>Insights from leading AI researchers and ethicists</li>
        <li>Future-proofing techniques for your career and life</li>
      </ul>
      <p class="text-center text-sm">Join 10,000+ readers preparing for the future</p>
    </div>
  </div>

  <Divider />

  <section class="my-12">
    <h3 class="text-2xl font-bold mb-4 dark:text-gray-200">Preview: Surviving the Singularity Guide</h3>
    <div class="content bg-gray-100 dark:bg-gray-700 p-6 rounded-lg">
      {@html parsedContent}
    </div>
  </section>

  <Divider />

  <section class="text-center mt-16 mb-12">
    <h2 class="text-3xl font-bold mb-4">Limited Time Offer</h2>
    <p class="text-xl mb-8">Get 50% off when you pre-order now!</p>
    <Countdown targetDate={targetDate} />
    <div class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6 mt-8">
      <button on:click={joinSkool} class="action-button">
        Join Skool Community (Lock in your lifetime discount)
      </button>
      <button on:click={backOnKickstarter} class="action-button">
        Back on Kickstarter (Early Bird)
      </button>
    </div>
  </section>

  <Divider />

  <section class="mt-16">
    <h2 class="text-3xl font-bold mb-8 text-center">Stay Updated</h2>
    <p class="text-center mb-8">Get exclusive content and be the first to know about new releases and special offers.</p>
    <ContactForm on:submit={handleFormSubmit} />
  </section>
</main>

{#if showPopup}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" in:fade>
    <div class="bg-white dark:bg-gray-800 p-8 rounded-lg max-w-md relative" in:fly="{{ y: 200, duration: 500 }}">
      <button 
        on:click={closePopup} 
        class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        aria-label="Close popup"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <img src={StSFreeGuideImage} alt="Surviving the Singularity Free Guide" class="w-full mb-4 rounded-lg shadow-md">
      <h3 class="text-2xl font-bold mb-4 dark:text-gray-200">Don't miss out!</h3>
      <p class="mb-4 dark:text-gray-300">Get your free guide to surviving the AI revolution now.</p>
      <button on:click={navigateToDownload} class="cta-button mb-4 w-full">
        Get Free Guide
      </button>
      <button on:click={closePopup} class="text-sm text-gray-500 dark:text-gray-400 w-full">No thanks, I'll pass</button>
    </div>
  </div>
{/if}

<style>
  :global(body) {
    background-color: #f8f9fa;
    color: #333;
  }

  main {
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
  }

  .action-button {
    font-weight: bold;
    background-color: #FF9933;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
    font-size: 1rem;
    border-radius: 5px;
  }

  .action-button:hover {
    background-color: #FF8000;
    transform: translateY(-2px);
  }

  .content :global(h2) {
    font-size: 2rem;
    color: #333;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #FF9933;
    padding-bottom: 0.5rem;
  }

  .content :global(p) {
    margin-bottom: 1.5rem;
    line-height: 1.8;
    font-size: 1.1rem;
  }

  .content :global(h2:first-of-type) {
    margin-top: 0;
  }

  @media (max-width: 640px) {
    .content :global(h2) {
      font-size: 1.75rem;
    }

    .content :global(p) {
      font-size: 1rem;
    }

    .action-button {
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
    }
  }

  :global(.dark) body {
    background-color: #1a202c;
    color: #e2e8f0;
  }

  :global(.dark) main {
    background-color: #2d3748;
  }

  :global(.dark) .action-button {
    background-color: #FF9933;
    color: #1a202c;
  }

  :global(.dark) .action-button:hover {
    background-color: #FF8000;
  }

  :global(.dark) .content :global(h2) {
    color: #e2e8f0;
    border-bottom-color: #FF9933;
  }

  :global(.dark) .content :global(p) {
    color: #e2e8f0;
  }

  :global(.dark) .content-warning {
    background-color: rgba(255, 153, 51, 0.2);
  }

  :global(.dark) .content-warning p {
    color: #b0b0b0;
  }

  .content-warning {
    border-left: 4px solid #FF9933;
    padding: 0.5rem 1rem;
    background-color: rgba(255, 153, 51, 0.1);
    font-style: italic;
  }

  .content-warning p {
    margin: 0;
    font-size: 0.9rem;
    color: #666;
  }

  .StS-book-image {
    display: block;
    margin: 1rem auto;
    max-width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .cta-button {
    font-weight: bold;
    background-color: #FF9933;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
    font-size: 1rem;
    border-radius: 5px;
    animation: pulse 2s infinite;
    display: block;
    width: 100%;
    text-align: center;
  }

  .cta-button:hover {
    background-color: #FF8000;
    transform: translateY(-2px);
  }

  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
  }

  .StS-book-image {
    max-width: 300px;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  img {
    max-width: 100%;
    height: auto;
  }

  :global(.dark) .cta-button {
    color: #1a202c;
  }

  :global(.dark) .cta-button:hover {
    background-color: #FF8000;
  }
</style>