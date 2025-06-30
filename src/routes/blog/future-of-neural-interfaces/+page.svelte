<script>
  import { onMount } from 'svelte';
  import Spacer from '$lib/components/Spacer.svelte';

  import SocialShare from '$lib/components/SocialShare.svelte';
  import { fade } from 'svelte/transition';

  const post = {
    title: 'The Future of Neural Interfaces: A Comprehensive Guide',
    date: '2024-03-09',
    author: 'Christopher Tavolazzi',
    image: 'https://img.decrypt.co/insecure/rs:fit:3840:0:0:0/plain/https://cdn.decrypt.co/wp-content/uploads/2024/05/brian-implant-ai-gID_7.png@webp',
    readingTime: '8 min read'
  };

  // Reading progress
  let readingProgress = 0;

  // Image loading states
  let imageLoadingStates = new Map();

  // Handle image loading
  function handleImageLoad(imageId) {
    imageLoadingStates.set(imageId, true);
  }

  // Handle image error
  function handleImageError(imageId) {
    imageLoadingStates.set(imageId, false);
  }

  // Recent news articles with sources
  const recentNews = [
    {
      title: "Researchers design robotic arm controlled by your mind",
      date: "Last week",
      link: "https://nypost.com/video/researchers-design-robotic-arm-controlled-by-your-mind/",
      source: "New York Post"
    },
    {
      title: "Scientists Create Robotic Arm That Paralyzed Man Can Control with His Thoughts",
      date: "5 days ago",
      link: "https://people.com/scientists-create-robotic-arm-that-paralyzed-man-can-control-with-his-thoughts-11697185",
      source: "People"
    },
    {
      title: "Synchron's Brain-Computer Interface Now Has Nvidia's AI",
      date: "2 days ago",
      link: "https://www.wired.com/story/synchrons-brain-computer-interface-now-has-nvidias-ai",
      source: "Wired"
    },
    {
      title: "Neuralink wants to hook up its brain implant to a robotic arm",
      date: "3 months ago",
      link: "https://www.businessinsider.com/neuralink-hook-up-its-brain-implant-to-a-robotic-arm-2024-11",
      source: "Business Insider"
    },
    {
      title: "AI's Next Frontier: Are Brain-Computer Interfaces The Future Of Communication?",
      date: "1.6 years ago",
      link: "https://www.forbes.com/sites/bernardmarr/2023/08/11/ais-next-frontier-are-brain-computer-interfaces-the-future-of-communication/",
      source: "Forbes"
    },
    {
      title: "Breakthroughs in China's Brain-Computer Interface technologies",
      date: "1.7 years ago",
      link: "https://news.cgtn.com/news/2023-07-11/Breakthroughs-in-China-s-Brain-Computer-Interface-technologies-1llIxMVhYbu/index.html",
      source: "CGTN"
    },
    {
      title: "Brain-computer interface helps patient with locked-in syndrome communicate",
      date: "3.0 years ago",
      link: "https://www.livescience.com/brain-computer-interface-als-communicate",
      source: "Live Science"
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
  <meta name="description" content="Explore recent breakthroughs, future prospects, and ethical considerations in neural interfaces and brain-computer interfaces (BCIs)." />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content="Explore recent breakthroughs, future prospects, and ethical considerations in neural interfaces and brain-computer interfaces (BCIs)." />
  <meta property="og:image" content={post.image} />
  <meta property="og:url" content="https://survivingthesingularity.com/blog/future-of-neural-interfaces" />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={post.title} />
  <meta name="twitter:description" content="Explore recent breakthroughs, future prospects, and ethical considerations in neural interfaces and brain-computer interfaces (BCIs)." />
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
        description="Explore recent breakthroughs, future prospects, and ethical considerations in neural interfaces and brain-computer interfaces (BCIs)."
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
        Neural interfaces, also known as brain-computer interfaces (BCIs), are at the forefront of technological innovation, enabling direct communication between the human brain and external devices. This primer provides an in-depth exploration of recent advancements, future prospects, and ethical considerations in the realm of neural interfaces.
      </p>

      <section id="recent-breakthroughs" class="scroll-mt-16">
        <h2>Significant Breakthroughs</h2>
        <p>
          The field of neural interfaces has seen remarkable progress in recent years, with several groundbreaking developments that are reshaping our understanding of brain-computer interaction.
        </p>

        <div class="grid md:grid-cols-2 gap-6 my-6">
          <div class="breakthrough-card">
            <h3>Robotic Arm Controlled by Thought</h3>
            <p>
              Researchers at the University of California, San Francisco (UCSF) have developed a BCI that enabled a paralyzed individual to control a robotic arm using only his thoughts. By implanting tiny sensors on the brain's surface, the system interprets neural signals associated with imagined movements, allowing the user to manipulate objects. Remarkably, this system maintained functionality for up to seven months without requiring recalibration, marking a significant milestone in BCI durability and reliability.
            </p>
          </div>

          <div class="breakthrough-card">
            <h3>Integration with AI for Enhanced Performance</h3>
            <p>
              Companies like Synchron are integrating artificial intelligence (AI) to enhance BCI performance. Synchron's latest iteration of its BCI incorporates NVIDIA's AI technology, enabling faster and more accurate decoding of neural signals. This integration allows users, such as individuals with amyotrophic lateral sclerosis (ALS), to control devices like the Apple Vision Pro through thought alone, thereby improving their interaction with the digital world.
            </p>
          </div>

          <div class="breakthrough-card">
            <h3>Neuralink's Progress in Human Trials</h3>
            <p>
              Elon Musk's company, Neuralink, has made significant strides by implanting its N1 chip into a human subject, allowing control of a computer using thought. Despite challenges such as thread retraction due to brain movement, the subject remains optimistic about the technology's potential to improve quality of life.
            </p>
          </div>

          <div class="breakthrough-card">
            <h3>Bidirectional Communication</h3>
            <p>
              Recent years have seen unprecedented progress in neural interface technology, with multiple teams achieving record-breaking milestones. Researchers have successfully demonstrated bidirectional communication between the brain and external devices, enabling not just control but also sensory feedback. This two-way communication has been particularly successful in restoring touch sensation in prosthetic limbs, marking a crucial step toward more natural and intuitive neural interfaces.
            </p>
          </div>
        </div>
      </section>

      <section id="ai-in-bcis" class="scroll-mt-16">
        <h2>The Role of Artificial Intelligence in BCIs</h2>
        <p>
          The fusion of AI with neural interfaces is opening new horizons in neurotechnology:
        </p>

        <div class="grid md:grid-cols-2 gap-6 my-6">
          <div class="ai-card">
            <h3>Enhanced Signal Decoding</h3>
            <p>
              AI algorithms can process complex neural data, facilitating more intuitive and responsive control of prosthetics and other assistive devices. This synergy not only enhances the functionality of BCIs but also accelerates the development of applications aimed at restoring motor functions and communication abilities in individuals with neurological conditions.
            </p>
          </div>

          <div class="ai-card">
            <h3>Personalized BCIs</h3>
            <p>
              Advancements in machine learning (ML) are leading to more personalized BCIs that adapt to individual users' unique neural patterns, requiring less training time and improving user experience.
            </p>
          </div>
        </div>
      </section>

      <section id="future-prospects" class="scroll-mt-16">
        <h2>Near-Future Prospects</h2>
        <p>
          Looking ahead, several developments are poised to shape the future of neural interfaces:
        </p>

        <div class="grid md:grid-cols-3 gap-6 my-6">
          <div class="prospect-card">
            <h3>Non-Invasive BCIs</h3>
            <p>
              Advancements in non-invasive neural interfaces are making BCI technology more accessible and user-friendly. These devices allow users to interact with technology using brain signals without the need for surgical implantation.
            </p>
          </div>

          <div class="prospect-card">
            <h3>AI Integration</h3>
            <p>
              The integration of AI with BCIs is expected to enhance the decoding of neural signals, leading to more accurate and efficient control of devices. This could result in more seamless interactions between humans and machines.
            </p>
          </div>

          <div class="prospect-card">
            <h3>Commercialization</h3>
            <p>
              Companies like Neuralink are making strides toward commercializing BCI technology. Neuralink has received FDA approval for human clinical trials and has begun implanting its devices in patients, marking a significant step toward making BCIs widely available.
            </p>
          </div>
        </div>
      </section>

      <section id="ethical-considerations" class="scroll-mt-16">
        <h2>Ethical Considerations and Future Directions</h2>
        <p>
          As neural interface technology progresses, it raises important ethical questions:
        </p>

        <div class="grid md:grid-cols-3 gap-6 my-6">
          <div class="ethics-card">
            <h3>User Autonomy and Privacy</h3>
            <p>
              Ensuring that users maintain control over their neural data and that their privacy is protected is paramount.
            </p>
          </div>

          <div class="ethics-card">
            <h3>Cognitive Enhancement</h3>
            <p>
              The potential for BCIs to enhance cognitive abilities beyond therapeutic applications introduces debates about fairness and accessibility.
            </p>
          </div>

          <div class="ethics-card">
            <h3>Ethical Frameworks</h3>
            <p>
              Establishing robust ethical frameworks is crucial to ensure that these technologies are developed and deployed in ways that respect individual rights and societal norms.
            </p>
          </div>
        </div>
      </section>

      <section id="conclusion" class="scroll-mt-16">
        <h2>Conclusion</h2>
        <p>
          The future of neural interfaces is both promising and complex. Continued interdisciplinary collaboration among neuroscientists, engineers, ethicists, and policymakers will be essential to harness the full potential of BCIs while addressing the challenges they present.
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
            description="Explore recent breakthroughs, future prospects, and ethical considerations in neural interfaces and brain-computer interfaces (BCIs)."
            image={post.image}
          />
        </div>
      </div>

      <Spacer height="2rem" />
      <!-- Discord removed -->
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
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
    max-height: 80vh;
    border-radius: 0.5rem;
    transition: transform 0.5s ease;
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
  .breakthrough-card, .ai-card, .prospect-card, .ethics-card {
    padding: 1.5rem;
    border-radius: 0.75rem;
    background-color: var(--color-bg-secondary);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .breakthrough-card::before, .ai-card::before, .prospect-card::before, .ethics-card::before {
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

  .breakthrough-card:hover::before, .ai-card:hover::before, .prospect-card:hover::before, .ethics-card:hover::before {
    opacity: 1;
  }

  .breakthrough-card:hover, .ai-card:hover, .prospect-card:hover, .ethics-card:hover {
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

    .breakthrough-card, .ai-card, .prospect-card, .ethics-card {
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

  /* Progress bar styles */
  .reading-progress {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background-color: #3b82f6;
    z-index: 100;
    transition: width 0.1s ease-out;
  }
</style>