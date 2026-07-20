/** @type {import('./$types').PageServerLoad} */
export async function load() {
  const posts = [
    {
      title: "No, Scientists Didn't Just Invent Anti-Gravity (What They Actually Found Is Stranger)",
      date: '2026-07-17',
      author: 'Christopher Tavolazzi',
      route: '/blog/no-scientists-didnt-just-invent-antigravity-what-they-actually-found-is-stranger',
      excerpt: "A new paper proposes a lab-feasible way to make gravity look repulsive for a filtered slice of particles. It's not a hoverboard. It's a real plan to test whether gravity itself is quantum, one of the biggest open questions in physics.",
      image: 'https://images.unsplash.com/photo-1708011271954-c0d2b3155ded?q=80&w=2072&auto=format&fit=crop'
    },
    {
      title: 'The Algal Biorefinery Blueprint: Engineering the Post-Petrochemical Stack',
      date: '2026-06-17',
      author: 'Christopher Tavolazzi',
      route: '/blog/algal-biorefinery-blueprint',
      excerpt: "Carbon credits alone can't fund a gigaton-scale algae operation. The companies winning this space produce bioplastics, medical oxygen, cement replacement, and closed-loop fuel from the same tank. Here's the full architecture.",
      image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=2070&auto=format&fit=crop'
    },
    {
      title: 'Algae Can Save Us. Here\'s Why Nobody\'s Talking About It.',
      date: '2026-06-17',
      author: 'Christopher Tavolazzi',
      route: '/blog/algae-saves-us',
      excerpt: "It grows in the White House pool. It makes flip-flops. It can produce fuel, medicine, and bioplastics. Algae is the most underrated survival technology on Earth. The only thing holding it back is a production bottleneck we can solve.",
      image: 'https://plus.unsplash.com/premium_photo-1661391815480-207c5853539c?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
      title: 'Whispers of the Future: The Paradigm Shift of Human-AI Relations',
      date: '2025-03-28',
      author: 'Christopher Tavolazzi',
      route: '/blog/whispers-of-the-future',
      excerpt: "There is something happening in the quiet corners of our lives. This is the beginning of something enormous, and we've seen it before. Every seismic societal shift starts in whispers.",
      image: '/images/blog/whispers-ai-featured.png'
    },
    {
      title: 'The Rise of Synthetic Biological Intelligence: A New Era in Computing',
      date: '2025-03-06',
      author: 'Christopher Tavolazzi',
      route: '/blog/synthetic-biological-intelligence',
      excerpt: 'Australian startup Cortical Labs has unveiled the CL1, the world\'s first commercial Synthetic Biological Intelligence system-a fusion of biology and tech with human neurons cultured directly onto silicon chips.',
      image: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1200&q=80&auto=format&fit=crop'
    },
    {
      title: 'The Future of Neural Interfaces: A Comprehensive Guide',
      date: '2024-03-09',
      author: 'Christopher Tavolazzi',
      route: '/blog/future-of-neural-interfaces',
      excerpt: 'Explore recent breakthroughs, future prospects, and ethical considerations in neural interfaces and brain-computer interfaces (BCIs).',
      image: 'https://images.unsplash.com/photo-1617791160536-598cf32026fb?w=1200&q=80&auto=format&fit=crop'
    },
    {
      title: 'Robot Farm Bot - The Future of Residential Agriculture',
      date: '2024-08-15',
      author: 'Christopher Tavolazzi',
      route: '/blog/robot-farm-bot',
      excerpt: 'Imagine a world where your backyard vegetable garden is tended by an AI-powered robot, ensuring a bountiful harvest with minimal effort. Welcome to the era of the Robot Farm Bot.',
      image: 'https://farm.bot/cdn/shop/files/FarmBot_Genesis_v1-3_c10ecd67-00ed-4ae1-a32e-111f11312655_2049x1365.jpg?v=1697756943'
    },
    {
      title: 'The Singularity Express Arrives at the Station',
      date: '2024-08-08',
      author: 'Christopher Tavolazzi',
      route: '/blog/singularity-express',
      excerpt: 'The Singularity Express has pulled into the station. A look at what "Level 2" reasoning AI means and why the jump matters.',
      image: '/images/surviving_the_singularity_cover_1200.png'
    },
    {
      title: 'Farm Bot Deep Dive - Exploring AI-Powered Precision Agriculture',
      date: '2024-08-24',
      author: 'Christopher Tavolazzi',
      route: '/blog/farm-bot-deep-dive',
      excerpt: 'Dive deep into the world of FarmBot, a revolutionary CNC automated, AI-powered system that\'s transforming backyard gardening and small-scale agriculture with precision and efficiency.',
      image: 'https://www.open-electronics.org/wp-content/uploads/2013/10/FarmBot-Genesis-Homepage-Image.jpg'
    },
    {
      title: 'Weekend Project - Building with Claude AI',
      date: '2024-08-30',
      author: 'Christopher Tavolazzi',
      route: '/blog/claude-projects-weekend-project',
      excerpt: 'Ready to supercharge your AI workflow? Join us for a weekend challenge exploring Claude Projects, a powerful new feature that\'s transforming how we interact with AI.',
      image: 'https://i.ytimg.com/vi/nbG2DO6Xsek/maxresdefault.jpg'
    },
    {
      title: 'DARPA Seeks Plans for Large Bio-Mechanical Space Structures',
      date: '2025-03-04',
      author: 'Christopher Tavolazzi',
      route: '/blog/darpa-biomechanical-space-structures',
      excerpt: 'DARPA has issued a request for information on building massive biological structures in space, exploring a sci-fi future where space infrastructure might be grown rather than assembled.',
      image: 'https://futurism.com/_next/image?url=https%3A%2F%2Fwordpress-assets.futurism.com%2F2025%2F02%2Fdarpa-requests-plans-large-bio-mechanical-space-structures.jpg&w=2048&q=75'
    },
    {
      title: "Neuralink's Latest Breakthrough: A New Era in Brain-Computer Interfaces",
      date: '2024-03-09',
      author: 'Christopher Tavolazzi',
      route: '/blog/neuralink-latest-breakthrough',
      excerpt: "Neuralink's first human trial participants are controlling computers with their thoughts. A look at where brain-computer interface technology stands today and what comes next.",
      image: 'https://www.digitaltrends.com/wp-content/uploads/2019/07/finalmente-sapremo-neuralink-progetto-segreto-elon-musk-v3-388343.jpg?resize=1200%2C630&p=1'
    },
    {
      title: 'Synthetic Biological Intelligence: Living Human Cells Power Next-Gen Computing',
      date: '2025-04-07',
      author: 'Christopher Tavolazzi',
      route: '/blog/synthetic-biological-computers',
      excerpt: "The world's first commercial \"biological computer\" fuses living human neurons with silicon hardware, potentially outpacing traditional AI systems while raising profound ethical questions.",
      image: '/images/surviving_the_singularity_cover_1200.png'
    }
  ];

  return {
    posts: posts.sort((a, b) => new Date(b.date) - new Date(a.date))
  };
}

// The post list is static data — prerender the blog index (and, via crawl, each
// linked post) so these read-only pages serve from the CDN edge.
export const prerender = true;