<script>
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import SocialShare from '$lib/components/SocialShare.svelte';
  import { fade } from 'svelte/transition';

  const post = {
    title: "Neuralink's Latest Breakthrough: A New Era in Brain-Computer Interfaces",
    date: '2024-03-09',
    author: 'Christopher Tavolazzi',
    image: 'https://www.digitaltrends.com/wp-content/uploads/2019/07/finalmente-sapremo-neuralink-progetto-segreto-elon-musk-v3-388343.jpg?resize=1200%2C630&p=1',
    readingTime: '7 min read'
  };

  // Reading progress
  let readingProgress = 0;

  // Recent news articles
  const recentNews = [
    {
      title: "A Year of Telepathy",
      date: "Last month",
      link: "https://neuralink.com/blog/a-year-of-telepathy/",
      source: "Neuralink"
    },
    {
      title: "Musk's Neuralink gets FDA's breakthrough device tag for 'Blindsight' implant",
      date: "6 months ago",
      link: "https://www.reuters.com/business/healthcare-pharmaceuticals/musks-neuralink-receives-fdas-breakthrough-device-tag-brain-implant-2024-09-17/",
      source: "Reuters"
    },
    {
      title: "Elon Musk put a chip in this paralysed man's brain. Now he can move things with his mind.",
      date: "Last month",
      link: "https://www.theguardian.com/science/2025/feb/08/elon-musk-chip-paralysed-man-noland-arbaugh-chip-brain-neuralink",
      source: "The Guardian"
    },
    {
      title: "Elon Musk's Neuralink device Blindsight gets FDA breakthrough designation",
      date: "6 months ago",
      link: "https://www.mobihealthnews.com/news/elon-musks-neuralink-device-blindsight-gets-fda-breakthrough-device-designation",
      source: "MobiHealthNews"
    },
    {
      title: "Elon Musk says a third patient got a Neuralink brain implant. The work is part of a booming field",
      date: "2 months ago",
      link: "https://apnews.com/article/9dbc92206389f27fd032825cf1597ee5",
      source: "Associated Press"
    },
    {
      title: "Elon Musk's Neuralink Files to Trademark 'Telepathy'",
      date: "Last week",
      link: "https://www.wired.com/story/elon-musks-neuralink-files-trademark-telepathy",
      source: "Wired"
    },
    {
      title: "Neuralink receives approval to begin clinical trial in Canada on brain implant",
      date: "3 months ago",
      link: "https://www.mobihealthnews.com/news/neuralink-receives-approval-begin-clinical-trial-canada-brain-implant",
      source: "MobiHealthNews"
    }
  ];

  // Update reading progress on scroll
  onMount(() => {
    const updateReadingProgress = () => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight - windowHeight;
      readingProgress = (window.scrollY / documentHeight) * 100;
    };

    window.addEventListener('scroll', updateReadingProgress);
    return () => window.removeEventListener('scroll', updateReadingProgress);
  });
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content="Explore Neuralink's latest breakthroughs in brain-computer interface technology, including human trials, FDA approvals, and future implications." />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content="Explore Neuralink's latest breakthroughs in brain-computer interface technology, including human trials, FDA approvals, and future implications." />
  <meta property="og:image" content={post.image} />
  <meta property="og:url" content="https://survivingthesingularity.com/blog/neuralink-latest-breakthrough" />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={post.title} />
  <meta name="twitter:description" content="Explore Neuralink's latest breakthroughs in brain-computer interface technology, including human trials, FDA approvals, and future implications." />
  <meta name="twitter:image" content={post.image} />
</svelte:head>

<!-- Reading Progress Bar -->
<div class="fixed top-0 left-0 w-full h-1 bg-gray-200 dark:bg-gray-700 z-50">
  <div
    class="h-full bg-blue-600 transition-all duration-300"
    style="width: {readingProgress}%">
  </div>
</div>

<div class="blog-post">
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <button
        class="back-button mb-4 flex items-center text-blue-600 dark:text-blue-400 hover:underline"
        on:click={() => window.history.back()}
      >
        <span class="inline-block mr-1">←</span> Back to Blog
      </button>
      <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 leading-tight">{post.title}</h1>
      <div class="flex flex-wrap items-center text-sm md:text-base text-gray-600 dark:text-gray-400 gap-2 mb-4">
        <span>{post.date}</span>
        <span class="hidden md:inline">·</span>
        <span>{post.readingTime}</span>
        <span class="hidden md:inline">·</span>
        <span>By {post.author}</span>
      </div>

      <!-- Add SocialShare component -->
      <SocialShare
        title={post.title}
        description="Explore Neuralink's latest breakthroughs in brain-computer interface technology, including human trials, FDA approvals, and future implications."
        image={post.image}
      />
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden shadow-xl">
      <img
        src={post.image}
        alt={post.title}
        class="w-full h-auto transform hover:scale-105 transition-transform duration-500"
        loading="lazy"
        decoding="async"
      />
    </div>

    <div class="content">
      <p class="lead">
        Neuralink, the brain-computer interface company founded by Elon Musk, has recently achieved significant milestones in its mission to merge human cognition with artificial intelligence. These advancements hold promise for individuals with neurological challenges and signal a transformative era in neurotechnology.
      </p>

      <section id="recent-breakthroughs" class="scroll-mt-16">
        <h2>Recent Breakthroughs</h2>
        <p>
          The field of neural interfaces has seen remarkable progress in recent years, with several groundbreaking developments that are reshaping our understanding of brain-computer interaction.
        </p>

        <div class="grid md:grid-cols-2 gap-6 my-6">
          <div class="breakthrough-card">
            <h3>First Human Implantation</h3>
            <p>
              In January 2024, Neuralink successfully implanted its N1 chip into 29-year-old Noland Arbaugh, who had been quadriplegic since a 2016 diving accident. Post-implantation, Arbaugh demonstrated the ability to control a computer cursor using only his thoughts, enabling him to browse the internet, play video games, and communicate more effectively. This groundbreaking procedure marked a pivotal moment in BCI technology, showcasing the potential to restore autonomy to individuals with paralysis.
            </p>
          </div>

          <div class="breakthrough-card">
            <h3>FDA Breakthrough Device Designation</h3>
            <p>
              In September 2024, Neuralink's experimental implant, "Blindsight," received the FDA's breakthrough device designation. This implant aims to restore vision for individuals who have lost their sight, even in cases where the optic nerve has been damaged. The designation facilitates expedited development and review processes, underscoring the device's potential to address unmet medical needs.
            </p>
          </div>

          <div class="breakthrough-card">
            <h3>Expansion of Clinical Trials</h3>
            <p>
              By early 2025, Neuralink had implanted devices in three patients. The second patient utilized the implant to engage in activities such as playing video games and designing 3D objects, highlighting the device's versatility. Neuralink plans to extend trials to additional participants, aiming to refine the technology and broaden its applications.
            </p>
          </div>

          <div class="breakthrough-card">
            <h3>Technological Innovations</h3>
            <p>
              Neuralink has filed trademark applications for terms like "Telepathy," "Telekinesis," and "Blindsight." These filings suggest the company's ambition to develop technologies enabling direct mental communication between individuals, control of devices through thought, and restoration of vision, respectively. Such innovations could revolutionize human interaction with technology and each other.
            </p>
          </div>
        </div>
      </section>

      <section id="ai-integration" class="scroll-mt-16">
        <h2>Integration with AI</h2>
        <p>
          The company's advancements in AI integration have enhanced the functionality of its implants, allowing for more precise decoding of neural signals. This integration facilitates more intuitive control of devices, paving the way for applications beyond medical rehabilitation, including cognitive enhancement and seamless human-computer interaction.
        </p>
      </section>

      <section id="ethical-considerations" class="scroll-mt-16">
        <h2>Ethical and Societal Considerations</h2>
        <p>
          While Neuralink's progress offers hope for medical advancements, it also raises ethical questions. The potential for cognitive enhancement and direct brain-to-brain communication challenges existing notions of privacy, consent, and the essence of human identity. As the technology advances, it will be crucial to establish ethical frameworks that ensure equitable access and protect individual rights.
        </p>
      </section>

      <section id="conclusion" class="scroll-mt-16">
        <h2>Conclusion</h2>
        <p>
          Neuralink's recent breakthroughs signify a monumental leap in brain-computer interface technology. As the company continues to innovate, it holds the potential to transform medical treatments for neurological conditions and redefine the boundaries between human cognition and artificial intelligence. Ongoing research, clinical trials, and ethical deliberations will be essential to navigate the profound implications of integrating such technologies into society.
        </p>
      </section>
    </div>

    <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-center mb-8">
        <button
          class="back-button flex items-center text-blue-600 dark:text-blue-400 hover:underline"
          on:click={() => window.history.back()}
        >
          <span class="inline-block mr-1">←</span> Back to Blog
        </button>

        <!-- Add SocialShare component at the bottom too -->
        <div class="bottom-share">
          <SocialShare
            title={post.title}
            description="Explore Neuralink's latest breakthroughs in brain-computer interface technology, including human trials, FDA approvals, and future implications."
            image={post.image}
          />
        </div>
      </div>

      <!-- Supporting Data Section -->
      <div class="supporting-data px-4 max-w-4xl mx-auto mb-8">
        <h2 class="text-2xl font-bold mb-6">Supporting Data</h2>
        <div class="space-y-4">
          {#each recentNews as article}
            <a
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              class="block p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors border border-gray-200 dark:border-gray-700">
              <div class="flex justify-between items-start gap-4">
                <h3 class="text-lg font-medium flex-grow">{article.title}</h3>
                <span class="text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap">{article.date}</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-300 mt-2 flex items-center">
                <span class="inline-block w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                {article.source}
              </p>
            </a>
          {/each}
        </div>
      </div>

      <NewsletterSignup />
      <Spacer height="2rem" />
      <DiscordButton />
    </div>
  </article>
</div>

<style>
  /* Define CSS variables */
  :root {
    --color-bg-primary: #ffffff;
    --color-bg-secondary: #f3f4f6;
    --color-text-primary: #111827;
    --color-text-secondary: #4b5563;
    --color-accent: #3b82f6;
    --color-accent-light: #60a5fa;
  }

  :global(.dark) {
    --color-bg-primary: #111827;
    --color-bg-secondary: #1f2937;
    --color-text-primary: #f9fafb;
    --color-text-secondary: #9ca3af;
    --color-accent: #60a5fa;
    --color-accent-light: #93c5fd;
  }

  :global(body) {
    scroll-behavior: smooth;
  }

  .blog-post {
    min-height: 100vh;
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
    background-image:
      radial-gradient(circle at 100% 0%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
      radial-gradient(circle at 0% 100%, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
  }

  .featured-image-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 0.5rem;
    background-color: rgba(15, 23, 42, 0.05);
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
    max-height: 80vh;
    border-radius: 0.5rem;
    transform: scale(1);
    transition: transform 0.5s ease;
  }

  .featured-image-container img:hover {
    transform: scale(1.05);
  }

  .content {
    font-size: 1.125rem;
    line-height: 1.75;
  }

  .lead {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-bottom: 2rem;
    position: relative;
    padding-left: 1rem;
    border-left: 4px solid var(--color-accent);
  }

  /* Section headers with decorative elements */
  h2 {
    position: relative;
    display: inline-block;
    margin-bottom: 1.5rem;
  }

  h2::after {
    content: '';
    position: absolute;
    bottom: -0.5rem;
    left: 0;
    width: 3rem;
    height: 3px;
    background: linear-gradient(to right, var(--color-accent), var(--color-accent-light));
    border-radius: 2px;
  }

  /* Card styles with icons */
  .breakthrough-card {
    padding: 1.5rem;
    border-radius: 0.75rem;
    background-color: var(--color-bg-secondary);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .breakthrough-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(to right, var(--color-accent), var(--color-accent-light));
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .breakthrough-card:hover::before {
    opacity: 1;
  }

  .breakthrough-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }

  /* Section separators */
  section {
    position: relative;
    padding: 2rem 0;
  }

  section:not(:last-child)::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    max-width: 600px;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--color-accent-light), transparent);
    opacity: 0.3;
  }

  /* Newsletter section enhancement */
  .newsletter-section {
    max-width: 4xl;
    margin: 0 auto;
    position: relative;
    padding: 2rem;
    background: linear-gradient(135deg, var(--color-bg-secondary) 0%, var(--color-bg-primary) 100%);
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  /* Related links enhancement */
  .related-links {
    position: relative;
  }

  .related-links a {
    position: relative;
    transition: all 0.3s ease;
  }

  .related-links a:hover {
    transform: translateX(0.5rem);
  }

  .related-links a::before {
    content: '→';
    position: absolute;
    left: -1.5rem;
    opacity: 0;
    transition: all 0.3s ease;
    color: var(--color-accent);
  }

  .related-links a:hover::before {
    opacity: 1;
    left: -1rem;
  }

  /* Mobile optimizations */
  @media (max-width: 768px) {
    .prose {
      font-size: 1rem;
    }

    h1 {
      font-size: 2rem;
    }

    h2 {
      font-size: 1.5rem;
    }

    h3 {
      font-size: 1.25rem;
    }

    .breakthrough-card {
      padding: 1rem;
    }

    .newsletter-section {
      padding: 1rem;
    }
  }

  /* Reading progress bar enhancement */
  .fixed.top-0 {
    background: linear-gradient(to right, var(--color-accent), var(--color-accent-light));
  }

  .bottom-share :global(.share-container) {
    margin: 0;
  }

  @media (max-width: 640px) {
    .bottom-share {
      display: none; /* Hide bottom share on mobile to save space */
    }
  }

  .back-button {
    display: inline-flex;
    align-items: center;
    transition: all 0.2s ease;
  }

  .back-button:hover {
    transform: translateX(-2px);
  }
</style>