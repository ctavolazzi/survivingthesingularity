<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import { marked } from 'marked';
  import sampleContent from '$lib/data/sample.md?raw';
  import ContactForm from '$lib/components/ContactForm.svelte';
  import Divider from '$lib/components/Divider.svelte';
  import StSBookImage from '$lib/images/Surviving-the-Singularity-Cover.png';
  import StSBookImageWebP from '$lib/images/Surviving-the-Singularity-Cover.webp';
  import SafeResponsiveImage from '$lib/components/SafeResponsiveImage.svelte';

  // Define responsive image sizes - halved from original values
  const bookCoverSizes = "(max-width: 600px) 40vw, (max-width: 1000px) 30vw, 20vw";

  let animatedSections = {};
  let isScrolled = false;

  onMount(() => {
    // Add scroll position detection for enhanced scrolling effects
    const handleScroll = () => {
      isScrolled = window.scrollY > 50;
    };

    window.addEventListener('scroll', handleScroll);

    // Set up intersection observer for scroll animations - as enhancement only
    try {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            if (entry.target.id) {
              animatedSections[entry.target.id] = true;
            }
          }
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

      // Observe all elements with animate-on-scroll class
      const sections = document.querySelectorAll('.animate-on-scroll');
      sections.forEach(section => {
        observer.observe(section);
      });
    } catch (error) {
      console.warn('Animation setup failed, but content will still be visible:', error);
    }

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
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
</script>

<svelte:head>
  <title>Free Book Sample | Surviving the Singularity</title>
  <meta name="description" content="Download your free guide on processing AI anxiety and confusion. Join thousands of other readers preparing for the future of technology.">
</svelte:head>

<main class="container mx-auto py-5 max-w-3xl dark:bg-gray-800/95 dark:text-gray-200">
  <header in:fade="{{ duration: 1000 }}" class="mb-6">
    <h1 class="text-5xl sm:text-6xl font-bold mb-3 text-center text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-600">Read a Free Sample</h1>
    <h2 class="text-2xl sm:text-3xl mb-4 text-center font-light max-w-2xl mx-auto leading-relaxed">The Ultimate Workbook for Processing AI Anxiety and Confusion</h2>
  </header>

  <div id="book-preview" class="animate-on-scroll flex flex-col md:flex-row items-center mb-10 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-2xl p-6 shadow-xl">
    <a href="/book" class="mb-8 md:mb-0 md:mr-10 transform transition-all duration-500 hover:scale-105 hover:rotate-1 focus:outline-none focus:ring-4 focus:ring-orange-200 dark:focus:ring-orange-900 rounded-xl">
      <SafeResponsiveImage
        src="/images/Surviving-the-Singularity-Cover.png"
        srcWebp="/images/Surviving-the-Singularity-Cover.webp"
        srcset="/images/Surviving-the-Singularity-Cover.png"
        srcsetWebp="/images/Surviving-the-Singularity-Cover.webp"
        sizes={bookCoverSizes}
        alt="Surviving the Singularity"
        class="StS-book-image rounded-xl shadow-2xl"
        loading="lazy"
      />
    </a>
    <div class="md:ml-4 w-full">
      <h3 class="text-2xl font-bold mb-5 text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-600">What You'll Learn</h3>
      <ul class="list-none pl-0 mb-6 space-y-3">
        <li class="flex items-start feature-item">
          <div class="feature-icon-container">
            <svg class="h-6 w-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <span class="text-lg">Practical exercises to process AI-related emotions</span>
        </li>
        <li class="flex items-start feature-item">
          <div class="feature-icon-container">
            <svg class="h-6 w-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <span class="text-lg">Strategies for adapting to rapid technological change</span>
        </li>
        <li class="flex items-start feature-item">
          <div class="feature-icon-container">
            <svg class="h-6 w-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <span class="text-lg">Insights from leading AI researchers and ethicists</span>
        </li>
        <li class="flex items-start feature-item">
          <div class="feature-icon-container">
            <svg class="h-6 w-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <span class="text-lg">Future-proofing techniques for your career and life</span>
        </li>
      </ul>
    </div>
  </div>

  <section id="preview-content" class="mb-10 animate-on-scroll">
    <h3 class="text-3xl sm:text-4xl font-bold mb-6 text-center">
      Surviving the Singularity Guide
    </h3>

    <div class="content bg-white dark:bg-gray-700 p-6 sm:p-8 rounded-2xl shadow-xl prose prose-orange dark:prose-invert lg:prose-lg mx-auto">
      {#if parsedContent}
        {@html parsedContent}
      {:else}
        <div class="flex justify-center items-center h-32">
          <div class="loading-spinner"></div>
          <p class="ml-4 text-gray-600 dark:text-gray-300">Loading content...</p>
        </div>
      {/if}
    </div>
  </section>

  <section id="contact-form" class="mb-8 animate-on-scroll">
    <div class="bg-gradient-to-b from-orange-100 via-orange-50/90 to-white dark:from-gray-800 dark:via-gray-800/80 dark:to-gray-900/90 p-6 md:p-8 rounded-2xl shadow-xl relative overflow-hidden">
      <!-- Background elements -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-orange-300 to-amber-400 rounded-full opacity-10 dark:opacity-5 blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-orange-400 to-amber-300 rounded-full opacity-10 dark:opacity-5 blur-3xl"></div>

      <div class="relative z-10">
        <h2 class="text-3xl sm:text-4xl font-bold mb-4 text-center text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-600">Stay Updated</h2>
        <p class="text-center mb-5 text-gray-700 dark:text-gray-300 text-lg max-w-2xl mx-auto">Get exclusive content and be the first to know about new releases and special offers.</p>

        <div class="max-w-md mx-auto bg-white/90 dark:bg-gray-800/60 p-6 rounded-xl shadow-lg backdrop-blur-sm border border-orange-100/50 dark:border-gray-700/50">
          <ContactForm on:submit={handleFormSubmit} />
          <p class="text-center text-xs text-gray-500 dark:text-gray-400 mt-3 italic">We respect your privacy and will never share your information.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="join-community" class="mb-8 animate-on-scroll">
    <div class="bg-gradient-to-b from-indigo-100 via-indigo-50/90 to-white dark:from-gray-800 dark:via-gray-800/80 dark:to-gray-900/90 p-6 md:p-8 rounded-2xl shadow-xl relative overflow-hidden">
      <!-- Background elements -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-indigo-300 to-purple-400 rounded-full opacity-10 dark:opacity-5 blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-indigo-400 to-purple-300 rounded-full opacity-10 dark:opacity-5 blur-3xl"></div>

      <div class="relative z-10">
        <h2 class="text-3xl sm:text-4xl font-bold mb-4 text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-600">Join Our Community</h2>
        <p class="text-center mb-5 text-gray-700 dark:text-gray-300 text-lg max-w-2xl mx-auto">Connect with others preparing for the singularity.</p>
      </div>
    </div>
  </section>
</main>

<style>
  main {
    background-color: white;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
    border-radius: 24px;
  }

  .StS-book-image {
    display: block;
    margin: 1rem auto;
    max-width: 100px;  /* Drastically reduced from 200px */
    max-height: 150px;  /* Fixed height instead of viewport-based */
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 8px;  /* Reduced border radius to match smaller size */
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15),
                0 3px 8px rgba(0, 0, 0, 0.08),
                0 0 0 1px rgba(0, 0, 0, 0.05);
    transition: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
  }

  .StS-book-image:hover {
    box-shadow: 0 20px 40px rgba(255, 153, 51, 0.2),
                0 10px 20px rgba(255, 153, 51, 0.1),
                0 0 0 1px rgba(255, 153, 51, 0.1);
  }

  .feature-item {
    transition: transform 0.3s ease;
  }

  .feature-item:hover {
    transform: translateX(5px);
  }

  .feature-icon-container {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(255, 153, 51, 0.2) 0%, rgba(255, 128, 0, 0.1) 100%);
    border-radius: 50%;
    padding: 8px;
    margin-right: 12px;
    flex-shrink: 0;
    box-shadow: 0 2px 5px rgba(255, 128, 0, 0.1);
  }

  .content {
    position: relative;
    border: 1px solid rgba(0, 0, 0, 0.05);
    overflow: hidden;
  }

  .content:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(to right, #FF9933, #FF8000);
    border-radius: 5px 5px 0 0;
  }

  .content :global(h2) {
    font-size: 1.85rem;
    color: #FF8000;
    margin-top: 2.5rem;
    margin-bottom: 1.2rem;
    border-bottom: 2px solid rgba(255, 153, 51, 0.2);
    padding-bottom: 0.7rem;
    font-weight: 700;
  }

  .content :global(p) {
    margin-bottom: 1.8rem;
    line-height: 1.9;
    font-size: 1.1rem;
    color: #374151;
  }

  .content :global(h2:first-of-type) {
    margin-top: 0;
  }

  .content :global(a) {
    color: #FF8000;
    text-decoration: none;
    border-bottom: 1px dotted #FF8000;
    transition: all 0.3s ease;
    font-weight: 500;
  }

  .content :global(a:hover) {
    color: #FF6600;
    border-bottom: 1px solid #FF6600;
  }

  .content :global(blockquote) {
    border-left: 4px solid #FF9933;
    padding: 1rem 0 1rem 1.5rem;
    margin: 2rem 0;
    background: rgba(255, 153, 51, 0.05);
    border-radius: 0 8px 8px 0;
    color: #4B5563;
    font-style: italic;
  }

  .content :global(ul), .content :global(ol) {
    margin-bottom: 1.8rem;
    line-height: 1.9;
    padding-left: 1.5rem;
  }

  .content :global(li) {
    margin-bottom: 0.8rem;
    position: relative;
  }

  .content :global(ul li::before) {
    content: '';
    position: absolute;
    left: -1.2rem;
    top: 0.6rem;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #FF9933;
  }

  /* Loading spinner */
  .loading-spinner {
    border: 4px solid rgba(255, 153, 51, 0.1);
    border-radius: 50%;
    border-top: 4px solid #FF9933;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Animate on scroll effects */
  .animate-on-scroll {
    opacity: 1; /* Start visible */
    transform: translateY(0); /* Start in normal position */
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* Tighter section spacing */
  section {
    margin-top: 2rem;
    margin-bottom: 2rem;
  }

  /* Adjust divider spacing */
  :global(.divider) {
    margin: 1rem auto;
  }

  :global(.stylish-divider) {
    margin: 1.5rem auto !important;
  }

  /* Dark mode adjustments */
  :global(.dark) .content {
    color: #e2e8f0;
    border-color: rgba(255, 255, 255, 0.1);
  }

  :global(.dark) .content :global(p) {
    color: #e2e8f0;
  }

  :global(.dark) .content :global(blockquote) {
    color: #cbd5e0;
    background: rgba(255, 255, 255, 0.03);
  }

  :global(.dark) .content :global(h2) {
    color: #FF9933;
    border-bottom-color: rgba(255, 153, 51, 0.3);
  }

  /* Additional responsive adjustments */
  @media (max-width: 640px) {
    .content {
      padding: 1.5rem;
    }

    .content:before {
      height: 3px;
    }

    .content :global(h2) {
      font-size: 1.5rem;
    }

    .content :global(p) {
      font-size: 1rem;
      line-height: 1.7;
    }

    .feature-icon-container {
      padding: 6px;
    }
  }

  @media (min-width: 1280px) {
    main {
      padding: 3rem 0.5rem;
    }
  }

  /* Treasure Tavern Container */
  .treasure-tavern-container {
    width: 100%;
    max-width: 900px;
    margin: 1rem auto;
    padding: 0 1rem;
  }

  @media (max-width: 768px) {
    .treasure-tavern-container {
      margin: 0.5rem auto;
    }
  }
</style>