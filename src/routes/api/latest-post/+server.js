import { json } from '@sveltejs/kit';

// Import the same data source used by the blog page
// This ensures consistency across the application
/** @type {import('@sveltejs/kit').RequestHandler} */
export async function GET() {
  try {
    // Define blog posts with their routes
    // (mirroring the data structure in src/routes/blog/+page.server.js)
    const posts = [
      {
        title: 'The Rise of Synthetic Biological Intelligence: A New Era in Computing',
        date: '2025-03-06',
        author: 'Christopher Tavolazzi',
        route: '/blog/synthetic-biological-intelligence',
        excerpt: 'Australian startup Cortical Labs has unveiled the CL1, the world\'s first commercial Synthetic Biological Intelligence system—a fusion of biology and tech with human neurons cultured directly onto silicon chips.',
        image: 'https://images.unsplash.com/photo-1581093588401-fbb62a02f120?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80'
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
        excerpt: 'Choo Choo, Motherf**ker. The Singularity Express just pulled into the station, and it\'s one hell of a ride. Get ready for Level 2 - AI that can think and reason.',
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

    // Sort posts by date (newest first)
    const sortedPosts = posts.sort((a, b) => new Date(b.date) - new Date(a.date));

    // Get the newest post (first in the sorted array)
    const latestPost = sortedPosts[0];

    return json({
      post: latestPost
    });
  } catch (error) {
    console.error('Error fetching latest post:', error);
    return json(
      { error: 'Failed to fetch latest post' },
      { status: 500 }
    );
  }
}