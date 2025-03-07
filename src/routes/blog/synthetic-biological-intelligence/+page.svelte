<script>
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import DiscordButton from '$lib/components/DiscordButton.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import SocialShare from '$lib/components/SocialShare.svelte';
  import RecommendedContent from '$lib/components/RecommendedContent.svelte';

  const post = {
    title: 'The Rise of Synthetic Biological Intelligence: A New Era in Computing',
    date: '2025-03-06',
    author: 'Christopher Tavolazzi',
    image: 'https://images.unsplash.com/photo-1581093588401-fbb62a02f120?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
    readingTime: '7 min read',
    audioSrc: '/audio/synthetic-biological-intelligence-notebooklm-podcast.mp3',
    audioTitle: 'Listen to the AI Audio Version: The Dawn of Neuron Computing',
    description: 'Explore the groundbreaking field of Synthetic Biological Intelligence that combines living neurons with silicon chips to create a new era of computing systems.'
  };

  let audio;

  // Briefing Document controls
  let showBriefing = false;
  let openBriefingSections = Array(9).fill(false);
  openBriefingSections[0] = true; // First section open by default

  const toggleBriefing = () => {
    showBriefing = !showBriefing;
  };

  const toggleBriefingSection = (index) => {
    openBriefingSections = openBriefingSections.map((state, i) => i === index ? !state : state);
  };

  // FAQ data and interactivity
  let openFaqs = Array(8).fill(false);
  openFaqs[0] = true; // First one open by default

  const toggleFaq = (index) => {
    openFaqs = openFaqs.map((state, i) => i === index ? !state : state);
  };

  const faqs = [
    {
      question: '1. What is Synthetic Biological Intelligence (SBI)?',
      answer: 'SBI is a new field that combines synthetic biology and computer science to create computing systems using living biological matter, particularly human neurons. These neurons are grown in a lab and interfaced with silicon chips containing microelectrode arrays. This fusion allows for the creation of AI systems that can learn and adapt in a more organic and energy-efficient manner than traditional silicon-based AI. The goal is to develop advanced programmable biological computing platforms.'
    },
    {
      question: '2. How does SBI work?',
      answer: 'SBI systems use lab-grown human neurons, often derived from induced pluripotent stem cells (iPSCs), cultured on silicon chips. These chips contain electrodes that both stimulate the neurons and read their electrical activity. By sending specific signals, the system can "reward" or "punish" the neurons based on their responses, effectively training them to perform certain tasks. The neurons form connections and adapt dynamically, learning from experience much like a human brain. This network of living cells is housed in a controlled environment ("body in a box") with pumps, temperature control, and gas systems to keep them alive and functioning.'
    },
    {
      question: '3. What are the potential applications of SBI?',
      answer: 'SBI has the potential to revolutionize several fields, including:<br><br><strong>Medical Research:</strong> Accelerating drug discovery, disease modeling, and personalized medicine by enabling researchers to study neurological diseases like Alzheimer\'s and epilepsy with more accuracy.<br><strong>Robotics:</strong> Creating robots that can learn and adapt more flexibly and efficiently than those programmed with traditional AI.<br><strong>Artificial General Intelligence (AGI):</strong> Providing a more sustainable pathway to AGI by offering faster decision-making, continuous learning, and greater energy and data efficiency compared to silicon-based systems.'
    },
    {
      question: '4. How does SBI compare to traditional AI in terms of energy efficiency?',
      answer: 'SBI systems are significantly more energy-efficient than traditional AI. For example, training a large language model like GPT-3 can consume as much energy as used by 120 households in a year. In contrast, a rack of 30 SBI units might only use around 1,000 watts, comparable to a small microwave. This energy efficiency stems from using living neurons, which consume significantly less power than silicon-based processors.'
    },
    {
      question: '5. Is SBI ready for widespread use?',
      answer: 'While SBI is a relatively new technology, it is becoming more accessible. Companies like Cortical Labs are now offering commercially available biocomputers and cloud-based access ("Wetware-as-a-Service") allowing researchers to experiment with the technology without needing specialized hardware. Increased funding and the development of prototype computing modules are further indicators that SBI could become a mainstream computing technology.'
    },
    {
      question: '6. Is SBI ethical? Are there concerns about consciousness or sentience?',
      answer: 'The ethical implications of SBI are a major consideration. Because SBI involves living brain cells, questions arise about the potential for consciousness or sentience and how these systems should be treated. Researchers are actively investigating ethical, legal, and regulatory issues related to SBI, including the moral status of human embryoids and the creation of appropriate oversight frameworks. While current SBI systems are not believed to possess awareness, ongoing monitoring and ethical discussions are essential.'
    },
    {
      question: '7. Is SBI likely to replace traditional silicon-based computing?',
      answer: 'SBI is not expected to completely replace silicon-based computing, but rather to complement it. SBI offers advantages in areas where adaptability, energy efficiency, and biological relevance are crucial. The hybridization of biological and silicon systems may provide the optimal path forward, combining the strengths of both approaches.'
    },
    {
      question: '8. What is the "Minimal Viable Brain" and why is it important?',
      answer: 'The "Minimal Viable Brain" (MVB) is the concept of bioengineering a human-like "brain" with the least amount of cell differentiation while maintaining the complexity needed for dynamic and responsive information processing. This concept seeks to identify the key biological components that allow something to process information according to underlying principles. Creating an MVB would provide researchers with a powerful and controlled model for studying intelligence, learning, and disease, leading to more nuanced analyses than currently possible with real brains.'
    }
  ];

  // Timeline data
  const timeline = [
    {
      date: 'Mid-2010s',
      description: 'The Broad Institute and other research teams introduce the concept of an "organ-on-a-chip."'
    },
    {
      date: '2019',
      description: 'Cortical Labs is founded, beginning their work on biological computing systems.'
    },
    {
      date: '2022',
      description: 'Cortical Labs gains attention for teaching approximately 800,000 human and mouse neurons in a dish (DishBrain) to play the video game Pong. Researchers publish their findings in the journal Neuron.'
    },
    {
      date: 'February 2023',
      description: '21 American researchers publish their thoughts about "Organoid Intelligence" (OI) in Frontiers in Science.'
    },
    {
      date: 'August 2023',
      description: 'Iltis and Matthews publish their paper on ethical issues concerning embryoids. Cortical Labs publishes research on critical dynamics in embodied in vitro neuronal networks.'
    },
    {
      date: '2023',
      description: 'Cortical Labs secures $15 million in funding to advance their biological computing technology.'
    },
    {
      date: '2024',
      description: 'Chinese researchers introduce a new brain-on-a-chip technology called MetaB.'
    },
    {
      date: 'March 2, 2025',
      description: 'Cortical Labs officially launches the CL1, the world\'s first commercially available biological computer, at the Mobile World Congress in Barcelona, Spain.'
    },
    {
      date: 'June 2025 (Expected)',
      description: 'First shipments of the CL1 biocomputer are expected. Cortical Labs hopes to have CL1 units and racks manufactured and ready to ship.'
    },
    {
      date: 'End of 2025 (Aims)',
      description: 'Cortical Labs is aiming to have four racks of CL1 units online and available through their Wetware-as-a-Service platform via the cloud.'
    }
  ];

  // Cast of Characters data
  const characters = [
    {
      name: 'Dr. Hon Weng Chong',
      role: 'Founder and CEO of Cortical Labs, focused on developing Proto Artificial General Intelligence Devices and democratizing access to biological computing technology.'
    },
    {
      name: 'Dr. Brett J. Kagan',
      role: 'Chief Scientific Officer of Cortical Labs, key researcher in the development of DishBrain and the CL1, focusing on biological aspects of SBI.'
    },
    {
      name: 'Ana S. Iltis',
      role: 'Policy researcher at Rice University\'s Baker Institute for Public Policy, investigating ethical implications of embryoid research.'
    },
    {
      name: 'Kirstin R.W. Matthews',
      role: 'Policy researcher at Rice University\'s Baker Institute for Public Policy, investigating ethical implications of embryoid research.'
    },
    {
      name: 'Sandra Acosta',
      role: 'Assistant Professor at the University of Barcelona, researching applications of the CL1 outside laboratory environments.'
    },
    {
      name: 'Christopher Tavolazzi',
      role: 'Founder of AIECO, specializing in AI/ML and R&D, author of "Surviving the Singularity."'
    },
    {
      name: 'Fred Jordan',
      role: 'Co-founder of Final Spark, a Swiss startup offering brain cell-powered computers via the cloud.'
    },
    {
      name: 'Robert Scoble',
      role: 'Futurist who interviewed Dr. Hon Weng Chong about SBI technology.'
    },
    {
      name: 'Sam Altman',
      role: 'CEO of OpenAI, leader in artificial intelligence development.'
    }
  ];

  // Recommended videos related to AI, neuroscience, and biological computing
  const recommendedVideos = [
    {
      id: "PNqwvJCz_2w",
      title: "Game Over? Voice Actors vs AI"
    },
    {
      id: "7Ip8TyjMyho",
      title: "Futurist: How AI and Robotics Will Reshape Our Economy"
    },
    {
      id: "GYBT66bPfu8",
      title: "Is the Gaming Industry Doomed?: Google's AI Generates Playable DOOM in Real-Time"
    }
  ];

  onMount(() => {
    // Add any audio initialization logic if needed
  });
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content={post.description} />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content={post.description} />
  <meta property="og:image" content={post.image} />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="blog-post">
  <article class="prose prose-lg dark:prose-invert mx-auto px-4 py-8 max-w-4xl">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
      <div class="flex items-center text-gray-600 dark:text-gray-400 mb-4">
        <span class="mr-4">{post.date}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">{post.readingTime}</span>
        <span class="mr-4">·</span>
        <span class="mr-4">By {post.author}</span>
        <button
          class="inline-flex items-center text-primary dark:text-primary-dark text-sm hover:text-primary-dark dark:hover:text-primary-hover-dark transition-colors ml-auto"
          on:click={() => {
            if (navigator.share) {
              navigator.share({
                title: post.title,
                text: post.description,
                url: window.location.href,
              }).catch(err => console.error('Error sharing:', err));
            } else {
              navigator.clipboard.writeText(window.location.href)
                .then(() => alert('Link copied to clipboard!'))
                .catch(err => console.error('Failed to copy:', err));
            }
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1">
            <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
            <polyline points="16 6 12 2 8 6"></polyline>
            <line x1="12" y1="2" x2="12" y2="15"></line>
          </svg>
          Share
        </button>
      </div>

      <div class="audio-player-container mb-6">
        <div class="flex items-center">
          <div class="audio-player-icon mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-headphones">
              <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
              <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
            </svg>
          </div>
          <div class="audio-player-text">
            <p class="text-sm font-medium">{post.audioTitle}</p>
          </div>
        </div>
        <audio
          bind:this={audio}
          src={post.audioSrc}
          controls
          preload="metadata"
          class="w-full mt-2"
        >
          Your browser does not support the audio element.
        </audio>
      </div>
    </header>

    <div class="featured-image-container mb-8 rounded-lg overflow-hidden">
      <img
        src={post.image}
        alt={post.title}
        class="w-full h-auto"
        loading="lazy"
        decoding="async"
      />
    </div>

    <div class="content">
      <p class="lead">
        Hold onto your neural implants, friends, because computing just made a quantum leap into the bioengineered unknown. Australian startup Cortical Labs has unveiled something wild: the CL1, the world's first commercial Synthetic Biological Intelligence (SBI) system.
      </p>

      <!-- FAQ Section -->
      <div class="faq-section mb-8 border-l-4 border-primary dark:border-primary-dark overflow-hidden rounded-sm">
        <div class="px-4 py-3 bg-gray-50 dark:bg-gray-800">
          <h2 class="text-xl font-bold mb-4">FAQ: Synthetic Biological Intelligence</h2>
          <div class="faq-container space-y-2">
            {#each faqs as faq, i}
              <div class="faq-item border border-gray-200 dark:border-gray-700 rounded-md overflow-hidden">
                <button
                  class="faq-question w-full px-4 py-2 text-left text-sm font-medium bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 flex justify-between items-center"
                  on:click={() => toggleFaq(i)}
                  aria-expanded={openFaqs[i]}
                  aria-controls={`faq-answer-${i}`}
                >
                  <span>{faq.question}</span>
                  <svg class={`w-4 h-4 transform transition-transform duration-200 ${openFaqs[i] ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </button>
                <div
                  id={`faq-answer-${i}`}
                  class="faq-answer px-4 py-2 text-sm bg-gray-50 dark:bg-gray-800"
                  class:hidden={!openFaqs[i]}
                >
                  <p class="text-gray-700 dark:text-gray-300">{@html faq.answer}</p>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>

      <!-- Featured Device Image -->
      <div class="device-showcase mb-8 bg-gray-50 dark:bg-gray-800 p-4 rounded-md">
        <h2 class="text-xl font-bold mb-3">The CL1: World's First Biological Computer</h2>
        <div class="flex flex-col md:flex-row items-center gap-4">
          <div class="md:w-3/5">
            <a href="https://corticallabs.com/images/footer-device.jpg" target="_blank" rel="noopener noreferrer" class="block">
              <img
                src="https://corticallabs.com/images/footer-device.jpg"
                alt="Cortical Labs CL1 Device - Biological Computer"
                class="w-full rounded-md border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-200"
              />
            </a>
          </div>
          <div class="md:w-2/5">
            <p class="text-sm mb-3">The CL1 is a fully-integrated biological computing platform where real neurons interface directly with silicon microelectrode arrays. This groundbreaking device maintains a life support system for neurons while enabling two-way electrical communication.</p>
            <a href="https://corticallabs.com/cl1.html" class="inline-block text-sm bg-primary text-white dark:bg-primary-dark px-3 py-1 rounded-md hover:opacity-90 transition-opacity">Learn more about CL1</a>
          </div>
        </div>
      </div>

      <div class="blog-content">
        <h2>Introduction: A Paradigm Shift on the Horizon</h2>
        <p>
          Hold onto your neural implants, friends, because computing just made a quantum leap into the bioengineered unknown. Australian startup Cortical Labs has unveiled something wild: the CL1, the world's first commercial Synthetic Biological Intelligence (SBI) system. This isn't your average silicon-and-code setup. It's a genuine fusion of biology and tech—human neurons cultured directly onto silicon chips—ushering in a mind-bending new era in artificial intelligence.
        </p>
        <p>
          Launched at the Mobile World Congress in Barcelona, the CL1 represents not just another incremental upgrade, but a radical departure from traditional computing methods.
        </p>

        <h2>What Exactly Is Synthetic Biological Intelligence?</h2>
        <p>
          Synthetic Biological Intelligence (SBI) combines the best of biology and silicon, creating computing systems that leverage the unique strengths of living brain tissue. At Cortical Labs, human neurons derived from induced pluripotent stem cells are grown into functioning neural networks. These neurons interface directly with specialized silicon microelectrode arrays (MEAs), which facilitate two-way electrical communication.
        </p>
        <p>
          Unlike traditional AI, which relies on pre-programmed algorithms, SBI learns organically. Neurons adapt, adjust, and respond dynamically, much like the human brain. Previous experiments demonstrated that neuron-based systems could learn simple tasks—such as playing Pong—in mere minutes, showcasing rapid adaptability far beyond current AI capabilities.
        </p>

        <h2>Why Should We Care?</h2>
        <p>
          The potential here is staggering. SBI could revolutionize multiple fields, starting with medicine. With real human neurons performing computations, researchers gain unprecedented insights into neurological diseases, accelerating drug discovery and medical innovation.
        </p>
        <p>
          But it doesn't stop there. The CL1's energy efficiency stands out starkly against traditional AI. While training a large AI model like GPT-3 consumes roughly 1,300 megawatt-hours—comparable to hundreds of homes annually—a full rack of 30 CL1 units sips only about 1,000 watts. In an era increasingly conscious of environmental sustainability, SBI could significantly cut the carbon footprint of data centers, aligning AI progress with ecological responsibility.
        </p>

        <h2>Transformative Impacts</h2>
        <p>
          Synthetic Biological Intelligence promises transformative impacts across diverse fields:
        </p>
        <ul>
          <li><strong>Medical breakthroughs:</strong> Enhanced neurological research and more precise drug testing.</li>
          <li><strong>Autonomous systems:</strong> Robots and vehicles that learn and adapt in real-time, not through tedious reprogramming.</li>
          <li><strong>Next-generation AI:</strong> Systems capable of human-like flexibility, adaptability, and rapid learning.</li>
        </ul>

        <!-- Timeline Section - Ultra Compact -->
        <div class="timeline-section my-6">
          <h2>The Evolution of SBI</h2>

          <div class="timeline-container relative border-l border-primary dark:border-primary-dark ml-3 mb-4">
            {#each timeline as event}
              <div class="timeline-item relative pl-4 pb-2">
                <div class="timeline-marker absolute -left-[4px] w-2 h-2 rounded-full bg-primary dark:bg-primary-dark"></div>
                <div class="timeline-content py-1">
                  <h4 class="font-bold text-xs text-primary dark:text-primary-dark inline mr-1">{event.date}:</h4>
                  <p class="text-xs inline">{event.description}</p>
                </div>
              </div>
            {/each}
          </div>
        </div>

        <div class="author-bio mt-6 p-3 bg-gray-50 dark:bg-gray-800 rounded border-l-4 border-primary dark:border-primary-dark text-sm">
          <p class="italic">
            <em>Christopher Tavolazzi is the founder of AIECO, specializing in AI/ML and R&D. He is also the author of "Surviving the Singularity," a blog and book dedicated to navigating the future of artificial intelligence.</em>
          </p>
        </div>
      </div>
    </div>
  </article>

  <Spacer height="2rem" />

  <div class="recommended-content-section">
    <RecommendedContent
      title="Explore More AI Content"
      description="Check out these videos about AI, neuroscience, and the future of technology"
      videos={recommendedVideos}
    />
  </div>

  <Spacer height="2rem" />

  <div class="newsletter-container">
    <NewsletterSignup />
    <DiscordButton />
  </div>
</div>

<style>
  .blog-post {
    min-height: 100vh;
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
  }

  .featured-image-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: contain;
    max-height: 80vh; /* Limit height on large screens */
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
  }

  .blog-content h2 {
    color: #ff7708;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-weight: bold;
    font-size: 1.875rem;
  }

  .blog-content h3 {
    color: #ff7708;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-weight: bold;
    font-size: 1.5rem;
  }

  .blog-content p {
    margin-bottom: 1rem;
    line-height: 1.625;
    color: var(--color-text-secondary);
  }

  .blog-content ul, .blog-content ol {
    padding-left: 1.5em;
    margin-left: 0;
    margin-bottom: 1.5rem;
  }

  .blog-content li {
    margin-bottom: 0.5em;
    color: var(--color-text-secondary);
  }

  .blog-content ul {
    list-style-type: disc;
  }

  .blog-content ol {
    list-style-type: decimal;
  }

  .blog-content a {
    color: #3b82f6;
    text-decoration: underline;
  }

  .blog-content a:hover {
    color: #2563eb;
  }

  .audio-player-container {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: var(--color-bg-secondary, #f3f4f6);
    margin-bottom: 1rem;
  }

  :global(.dark) .audio-player-container {
    background-color: var(--color-bg-secondary-dark, #374151);
  }

  .audio-player-icon {
    color: var(--color-primary, #f97316);
  }

  .share-container {
    display: flex;
    justify-content: center;
    margin: 0 auto;
    max-width: 300px;
  }

  .share-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: var(--color-primary, #f97316);
    color: white;
    font-weight: 500;
    padding: 0.5rem 1.25rem;
    border-radius: 0.375rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    font-size: 0.95rem;
  }

  .share-button:hover {
    background-color: var(--color-primary-dark, #ea580c);
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Timeline Styles */
  .timeline-section {
    position: relative;
    margin: 2rem 0;
  }

  .timeline-marker {
    border: 1px solid white;
    box-shadow: 0 0 0 1px var(--color-primary, #f97316);
    z-index: 2;
  }

  /* FAQ Styles */
  .faq-section {
    border-left: 4px solid var(--color-primary, #f97316);
    margin: 2rem 0;
  }

  .faq-item:hover {
    transform: translateX(2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .newsletter-container {
    max-width: 4xl;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Dark mode adjustments */
  :global(.dark) .blog-post {
    background-color: var(--color-bg-primary-dark);
    color: var(--color-text-primary-dark);
  }
</style>