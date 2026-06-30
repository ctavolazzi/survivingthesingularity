import { loadBlogPosts } from '$lib/data/blog-posts/blogPosts';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
  // Define blog posts directly with their routes
  const posts = [
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
      image: 'https://cdn.midjourney.com/2cfb73bc-4072-40fa-aa86-8cf4f842b428/0_2.png'
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
    }
  ];

  return {
    posts: posts.sort((a, b) => new Date(b.date) - new Date(a.date))
  };
}

// Disable prerendering since we're using async data fetching
export const prerender = false;