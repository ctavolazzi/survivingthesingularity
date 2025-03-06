<script>
  import { onMount } from 'svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
  import Spacer from '$lib/components/Spacer.svelte';

  const post = {
    title: 'The Rise of Synthetic Biological Intelligence: A New Era in Computing',
    date: '2025-03-06',
    author: 'Christopher Tavolazzi',
    image: 'https://images.unsplash.com/photo-1581093588401-fbb62a02f120?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
    readingTime: '7 min read',
    audioSrc: '/audio/synthetic-biological-intelligence-notebooklm-podcast.mp3',
    audioTitle: 'Listen to the AI Audio Version: The Dawn of Neuron Computing'
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

  onMount(() => {
    // Add any audio initialization logic if needed
  });
</script>

<div class="blog-post">
  <article class="prose prose-lg dark:prose-invert mx-auto px-3 sm:px-4 py-6 max-w-3xl">
    <header class="mb-6">
      <h1 class="text-3xl sm:text-4xl font-bold mb-3">{post.title}</h1>
      <div class="flex flex-wrap items-center text-sm text-gray-600 dark:text-gray-400 mb-3">
        <span class="mr-3">{post.date}</span>
        <span class="mr-3">·</span>
        <span class="mr-3">{post.readingTime}</span>
        <span class="mr-3">·</span>
        <span>By {post.author}</span>
      </div>
    </header>

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

    <div class="featured-image-container mb-6 rounded-lg overflow-hidden">
      <img
        src={post.image}
        alt={post.title}
        class="w-full h-auto"
        loading="lazy"
        decoding="async"
      />
    </div>

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

    <div class="content text-base">
      <h2 class="text-xl font-bold mt-6 mb-3">Introduction: A Paradigm Shift on the Horizon</h2>
      <p class="mb-4">
        Hold onto your neural implants, friends, because computing just made a quantum leap into the bioengineered unknown. Australian startup Cortical Labs has unveiled something wild: the CL1, the world's first commercial Synthetic Biological Intelligence (SBI) system. This isn't your average silicon-and-code setup. It's a genuine fusion of biology and tech—human neurons cultured directly onto silicon chips—ushering in a mind-bending new era in artificial intelligence.
      </p>
      <p class="mb-4">
        Launched at the Mobile World Congress in Barcelona, the CL1 represents not just another incremental upgrade, but a radical departure from traditional computing methods.
      </p>

      <h2 class="text-xl font-bold mt-6 mb-3">What Exactly Is Synthetic Biological Intelligence?</h2>
      <p class="mb-4">
        Synthetic Biological Intelligence (SBI) combines the best of biology and silicon, creating computing systems that leverage the unique strengths of living brain tissue. At Cortical Labs, human neurons derived from induced pluripotent stem cells are grown into functioning neural networks. These neurons interface directly with specialized silicon microelectrode arrays (MEAs), which facilitate two-way electrical communication.
      </p>
      <p class="mb-4">
        Unlike traditional AI, which relies on pre-programmed algorithms, SBI learns organically. Neurons adapt, adjust, and respond dynamically, much like the human brain. Previous experiments demonstrated that neuron-based systems could learn simple tasks—such as playing Pong—in mere minutes, showcasing rapid adaptability far beyond current AI capabilities.
      </p>

      <h2 class="text-xl font-bold mt-6 mb-3">Why Should We Care?</h2>
      <p class="mb-4">
        The potential here is staggering. SBI could revolutionize multiple fields, starting with medicine. With real human neurons performing computations, researchers gain unprecedented insights into neurological diseases, accelerating drug discovery and medical innovation.
      </p>
      <p class="mb-4">
        But it doesn't stop there. The CL1's energy efficiency stands out starkly against traditional AI. While training a large AI model like GPT-3 consumes roughly 1,300 megawatt-hours—comparable to hundreds of homes annually—a full rack of 30 CL1 units sips only about 1,000 watts. In an era increasingly conscious of environmental sustainability, SBI could significantly cut the carbon footprint of data centers, aligning AI progress with ecological responsibility.
      </p>

      <h2 class="text-xl font-bold mt-6 mb-3">Transformative Impacts</h2>
      <p class="mb-3">
        Synthetic Biological Intelligence promises transformative impacts across diverse fields:
      </p>
      <ul class="list-disc pl-5 mb-6 space-y-1">
        <li><strong>Medical breakthroughs:</strong> Enhanced neurological research and more precise drug testing.</li>
        <li><strong>Autonomous systems:</strong> Robots and vehicles that learn and adapt in real-time, not through tedious reprogramming.</li>
        <li><strong>Next-generation AI:</strong> Systems capable of human-like flexibility, adaptability, and rapid learning.</li>
      </ul>

      <!-- Timeline Section - Ultra Compact -->
      <div class="timeline-section my-6">
        <h2 class="text-xl font-bold mb-3">The Evolution of SBI</h2>

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

      <div class="cortical-links mb-6 text-sm">
        <p class="mb-2 font-semibold">Learn more about Cortical Labs and SBI:</p>
        <ul class="space-y-1 text-xs">
          <li>
            <a href="https://corticallabs.com/" class="text-primary dark:text-primary-dark hover:underline">
              Cortical Labs Official Website
            </a>
          </li>
          <li>
            <a href="https://corticallabs.com/cl1.html" class="text-primary dark:text-primary-dark hover:underline">
              CL1 Biological Computer Purchase Page
            </a>
          </li>
          <li>
            <a href="https://corticallabs.com/cloud.html" class="text-primary dark:text-primary-dark hover:underline">
              Cortical Cloud - Deploy Real Neurons
            </a>
          </li>
        </ul>
        <div class="mt-3 mb-2">
          <p class="text-xs mb-1">The CL1 Device:</p>
          <a href="https://corticallabs.com/images/footer-device.jpg" target="_blank" rel="noopener noreferrer">
            <img
              src="https://corticallabs.com/images/footer-device.jpg"
              alt="Cortical Labs CL1 Device"
              class="w-full max-w-[250px] h-auto rounded border border-gray-200 dark:border-gray-700"
            />
          </a>
        </div>
      </div>

      <h2 class="text-xl font-bold mt-6 mb-3">The Ethical Frontier: Navigating Uncharted Territory</h2>
      <p class="mb-4">
        Yet, blending human neurons with machines isn't ethically straightforward. We face fundamental questions: Does a bioengineered neuron-based system possess consciousness? What rights, if any, might such entities deserve? Could these living machines experience suffering?
      </p>
      <p class="mb-4">
        Biosecurity is another critical concern. What happens if these bioengineered neurons are inadvertently released or misused? SBI straddles the line between life and machine, challenging our moral frameworks and requiring rigorous oversight.
      </p>
      <p class="mb-4">
        Moreover, SBI opens questions around privacy, identity, and autonomy. If computers integrate biological elements derived from humans, how do we protect personal data and biological integrity?
      </p>

      <h2 class="text-xl font-bold mt-6 mb-3">Looking Ahead: The Road to Singularity</h2>
      <p class="mb-4">
        SBI isn't just innovation; it's evolution. As we edge closer to the Technological Singularity—the hypothetical tipping point where AI transcends human intelligence—systems like CL1 could play a defining role.
      </p>
      <p class="mb-4">
        Will SBI systems achieve consciousness? If so, how do we treat them? The potential merger of human and artificial intelligence could redefine humanity itself, presenting us with both incredible opportunities and profound challenges.
      </p>
      <p class="mb-4">
        The launch of CL1 is our cue to engage deeply with these questions. Technological advancement doesn't happen in isolation—it reflects our values, ethics, and collective vision for humanity's future. It's crucial we approach SBI thoughtfully, shaping its integration responsibly and ethically.
      </p>
      <p class="mb-4">
        Stay curious, stay informed, and as always, keep questioning.
      </p>

      <!-- Study Guide Section - Streamlined -->
      <div class="study-guide mt-8 border-l-4 border-primary dark:border-primary-dark bg-gray-50 dark:bg-gray-800 rounded-sm">
        <div class="p-4">
          <h2 class="text-xl font-bold mb-4">Synthetic Biological Intelligence: A Comprehensive Study Guide</h2>

          <details class="mb-4">
            <summary class="font-semibold cursor-pointer py-1">I. Review of Key Concepts</summary>
            <div class="pt-2 pl-4">
              <p class="mb-2 text-sm">Before diving into the specifics, ensure you understand these core ideas:</p>
              <ul class="list-disc pl-5 space-y-1 text-sm">
                <li><strong>Artificial Intelligence (AI):</strong> The broad field of creating machines capable of performing tasks that typically require human intelligence.</li>
                <li><strong>Synthetic Biology:</strong> The design and construction of new biological parts, devices, and systems, or the redesign of existing, natural biological systems for useful purposes.</li>
                <li><strong>Biological Computing:</strong> Utilizing biological materials, like cells, to perform computational tasks.</li>
                <li><strong>Neuron:</strong> A specialized cell in the nervous system that transmits information via electrical and chemical signals.</li>
                <li><strong>Stem Cells:</strong> Cells with the potential to develop into many different types of cells in the body.</li>
                <li><strong>Induced Pluripotent Stem Cells (iPSCs):</strong> Adult cells that have been reprogrammed back to a stem cell-like state.</li>
                <li><strong>Artificial General Intelligence (AGI):</strong> A hypothetical level of AI intelligence that matches or surpasses human intelligence across a wide range of tasks.</li>
                <li><strong>Ethics in AI:</strong> The moral principles and guidelines that govern the development and deployment of AI technologies, considering issues like bias, fairness, and potential harm.</li>
              </ul>
            </div>
          </details>

          <details class="mb-4">
            <summary class="font-semibold cursor-pointer py-1">II. Quiz: Test Your Knowledge</summary>
            <div class="pt-2 pl-4">
              <p class="mb-2 text-sm">Answer the following questions in 2-3 sentences each:</p>
              <ol class="list-decimal pl-5 space-y-1 text-sm">
                <li>What is synthetic biological intelligence (SBI), and how does it differ from traditional AI?</li>
                <li>What is Cortical Labs' CL1, and what are its key components?</li>
                <li>Explain the "DishBrain" experiment and its significance in the development of SBI.</li>
                <li>How does SBI offer potential advantages in energy efficiency compared to traditional AI systems?</li>
                <li>What are some potential applications of SBI in the field of medicine?</li>
                <li>What are some of the ethical concerns associated with SBI, and what are some attempts to address those concerns?</li>
                <li>What is meant by "wetware as a service (WaaS)" in the context of SBI?</li>
                <li>Explain how the CL1 facilitates a connection between organic networks and digital setups.</li>
                <li>What is the "Minimal Viable Brain" concept, and what are its implications for the future of SBI?</li>
                <li>How did Cortical Labs train the neurons on DishBrain?</li>
              </ol>
            </div>
          </details>

          <details class="mb-4">
            <summary class="font-semibold cursor-pointer py-1">III. Quiz Answer Key</summary>
            <div class="pt-2 pl-4 text-sm">
              <ol class="list-decimal pl-5 space-y-2">
                <li>SBI combines biological components, such as living neurons, with silicon hardware to create a system that learns and adapts organically. Unlike traditional AI, which relies on algorithms, SBI leverages the inherent learning capabilities of biological neurons.</li>
                <li>The CL1 is Cortical Labs' commercially available biocomputer, powered by living human brain cells. Its key components include lab-grown neurons on a silicon chip with electrodes, a life support system, and software for data monitoring and experiment tracking.</li>
                <li>The "DishBrain" experiment involved training approximately 800,000 neurons on a chip to play the video game Pong. This experiment demonstrated that neurons outside of the body can process information and learn through stimulus, rewards, and feedback.</li>
                <li>SBI leverages living neurons, which are inherently energy-efficient, using far less power than traditional silicon-based processors. This difference in energy consumption makes SBI a potentially more sustainable approach to achieving AGI.</li>
                <li>SBI can be applied in drug discovery and disease modeling, enabling researchers to test therapeutics and personalize medicine. The approach facilitates new avenues to study neurological diseases like epilepsy and Alzheimer's in dynamic and responsive ways.</li>
                <li>Ethical concerns of SBI include the potential for consciousness, animal testing replacements, or sentience in lab-grown neural networks. One attempt to address the concerns is the open debate among experts, in addition to following all legal requirements as determined by health agencies and bioethics committees.</li>
                <li>Wetware as a service (WaaS) is Cortical Lab's cloud based system of remote access to their biological computers, so that individuals may pay for time using the neural networks without needing to buy them outright.</li>
                <li>The CL1 has lab-cultivated cells grown across a silicon chip that has pins used to send electrical impulses into the web of neurons and receive impulses back.</li>
                <li>The concept of the minimal viable brain is how to bioengineer a human-like "brain" with the least amount of superfluous cell differentiation, but one that would have the complexity that growing a neural network made up of homogenous cell types doesn't have.</li>
                <li>Cortical Labs trained the neurons on DishBrain by sending electrical signals to tell the cells where the paddle was and the cells would respond; if the virtual ball was missed a random chaotic signal was sent back, which the cells didn't like and caused the system to avoid the behavior; if they hit the ball the signal was more predictable, causing the cells to adapt to hitting the ball.</li>
              </ol>
            </div>
          </details>

          <details class="mb-4">
            <summary class="font-semibold cursor-pointer py-1">IV. Essay Questions</summary>
            <div class="pt-2 pl-4">
              <p class="mb-2 text-sm">Consider these questions for further exploration and critical thinking:</p>
              <ol class="list-decimal pl-5 space-y-1 text-sm">
                <li>Analyze the potential benefits and risks of SBI compared to traditional AI. How might SBI impact society in the long term?</li>
                <li>Discuss the ethical implications of creating synthetic biological intelligence. What safeguards and regulations are necessary to ensure responsible development and use of this technology?</li>
                <li>Evaluate the feasibility of achieving Artificial General Intelligence (AGI) through SBI. What are the key challenges and potential breakthroughs that would need to occur?</li>
                <li>Compare and contrast the approaches to biological computing taken by Cortical Labs, Final Spark, and Chinese researchers. What are the strengths and weaknesses of each approach?</li>
                <li>Explore the philosophical implications of SBI. How might this technology challenge our understanding of consciousness, intelligence, and what it means to be human?</li>
              </ol>
            </div>
          </details>

          <details>
            <summary class="font-semibold cursor-pointer py-1">V. Glossary of Key Terms</summary>
            <div class="pt-2 pl-4 text-sm">
              <dl class="space-y-2">
                <div>
                  <dt class="font-bold">Artificial General Intelligence (AGI):</dt>
                  <dd class="ml-4">A hypothetical level of AI intelligence that matches or surpasses human intelligence across a wide range of tasks.</dd>
                </div>
                <div>
                  <dt class="font-bold">Artificial Intelligence (AI):</dt>
                  <dd class="ml-4">The broad field of creating machines capable of performing tasks that typically require human intelligence.</dd>
                </div>
                <div>
                  <dt class="font-bold">Biological Computing:</dt>
                  <dd class="ml-4">Utilizing biological materials, like cells, to perform computational tasks.</dd>
                </div>
                <div>
                  <dt class="font-bold">CMOS Chip:</dt>
                  <dd class="ml-4">A type of integrated circuit commonly used in electronics.</dd>
                </div>
                <div>
                  <dt class="font-bold">DishBrain:</dt>
                  <dd class="ml-4">The name given to the initial SBI experiment by Cortical Labs, where neurons were grown in a dish and trained to play Pong.</dd>
                </div>
                <div>
                  <dt class="font-bold">Microelectrode Arrays (MEAs):</dt>
                  <dd class="ml-4">Devices used to interface with neurons, enabling researchers to stimulate and record electrical activity.</dd>
                </div>
                <div>
                  <dt class="font-bold">Minimal Viable Brain (MVB):</dt>
                  <dd class="ml-4">A concept referring to the simplest possible biological structure capable of exhibiting basic intelligence.</dd>
                </div>
                <div>
                  <dt class="font-bold">SBI (Synthetic Biological Intelligence):</dt>
                  <dd class="ml-4">A system that leverages the unique strengths of living brain tissue.</dd>
                </div>
                <div>
                  <dt class="font-bold">Wetware as a Service (WaaS):</dt>
                  <dd class="ml-4">A model where users can remotely access and utilize biological computers for research and development purposes via the cloud.</dd>
                </div>
              </dl>
            </div>
          </details>
        </div>
      </div>

      <div class="author-bio mt-6 p-3 bg-gray-50 dark:bg-gray-800 rounded border-l-4 border-primary dark:border-primary-dark text-sm">
        <p class="italic">
          <em>Christopher Tavolazzi is the founder of AIECO, specializing in AI/ML and R&D. He is also the author of "Surviving the Singularity," a blog and book dedicated to navigating the future of artificial intelligence.</em>
        </p>
      </div>
    </div>
  </article>

  <div class="newsletter-section max-w-3xl mx-auto px-3 sm:px-4 py-4">
    <NewsletterSignup />
  </div>
</div>

<style>
  .blog-post {
    min-height: 100vh;
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
  }

  .audio-player-container {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: var(--color-bg-secondary, #f3f4f6);
    margin-bottom: 2rem;
  }

  :global(.dark) .audio-player-container {
    background-color: var(--color-bg-secondary-dark, #374151);
  }

  .audio-player-container audio {
    width: 100%;
    margin-top: 0.5rem;
  }

  .audio-player-icon {
    color: var(--color-primary, #f97316);
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

  blockquote {
    border-left: 4px solid var(--color-primary);
    padding-left: 1rem;
    margin: 2rem 0;
    font-style: italic;
    color: var(--color-text-secondary);
  }

  .newsletter-section {
    max-width: 4xl;
    margin: 0 auto;
    padding: 0 1rem;
  }

  /* Dark mode adjustments */
  :global(.dark) .blog-post {
    background-color: var(--color-bg-primary-dark);
    color: var(--color-text-primary-dark);
  }

  /* FAQ Styles */
  .faq-section {
    border-left: 4px solid var(--color-primary, #f97316);
  }

  .faq-item {
    transition: all 0.3s ease;
  }

  .faq-item:hover {
    transform: translateX(2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .faq-question {
    transition: background-color 0.2s ease;
  }

  .faq-answer {
    line-height: 1.6;
    transition: all 0.3s ease;
  }

  /* Timeline Styles */
  .timeline-section {
    position: relative;
  }

  .timeline-container {
    position: relative;
  }

  .timeline-item {
    transition: transform 0.2s ease;
  }

  .timeline-marker {
    border: 1px solid white;
    box-shadow: 0 0 0 1px var(--color-primary, #f97316);
    z-index: 2;
  }

  .timeline-content {
    transition: all 0.2s ease;
  }

  /* Briefing Document Styles */
  .briefing-document {
    font-size: 0.95rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .briefing-header {
    transition: background-color 0.2s ease;
  }

  .briefing-header:hover {
    background-color: var(--color-bg-hover, #f5f5f5);
  }

  :global(.dark) .briefing-header:hover {
    background-color: var(--color-bg-hover-dark, #2d3748);
  }

  .section-header {
    cursor: pointer;
    transition: all 0.2s ease;
    padding: 0.5rem;
    border-radius: 0.25rem;
  }

  .section-header:hover {
    background-color: var(--color-bg-hover, #f5f5f5);
  }

  :global(.dark) .section-header:hover {
    background-color: var(--color-bg-hover-dark, #2d3748);
  }

  .briefing-content blockquote {
    margin: 0.75rem 0;
    font-size: 0.9rem;
  }

  /* Cortical Links Styles */
  .cortical-links a {
    transition: color 0.2s ease;
  }

  .cortical-links img {
    transition: transform 0.2s ease;
  }

  .cortical-links img:hover {
    transform: scale(1.02);
  }

  /* Device Showcase Styles */
  .device-showcase {
    border-left: 4px solid var(--color-primary, #f97316);
  }

  .device-showcase img {
    transition: all 0.3s ease;
  }

  .device-showcase img:hover {
    transform: scale(1.01);
  }

  @media (max-width: 768px) {
    .device-showcase .flex-col {
      gap: 1rem;
    }
  }
</style>