import { json } from '@sveltejs/kit';

/**
 * Endpoint to fetch featured blog posts with Cloudflare caching
 * @param {Object} request - The request object
 * @returns {Object} JSON response with featured posts data
 */
export async function GET({ url, platform, request }) {
  // Get query parameters with defaults
  const limit = parseInt(url.searchParams.get('limit') || '3');

  // Define featured posts
  const featuredPosts = [
    {
      title: 'Whispers of the Future: The Paradigm Shift of Human-AI Relations',
      date: '2025-03-28',
      author: 'Christopher Tavolazzi',
      route: '/blog/whispers-of-the-future',
      excerpt: "There is something happening in the quiet corners of our lives. This is the beginning of something enormous, and we've seen it before. Every seismic societal shift starts in whispers.",
      image: '/images/blog/whispers-ai-featured.png',
      featured: true
    },
    {
      title: 'The Rise of Synthetic Biological Intelligence: A New Era in Computing',
      date: '2025-03-06',
      author: 'Christopher Tavolazzi',
      route: '/blog/synthetic-biological-intelligence',
      excerpt: 'Australian startup Cortical Labs has unveiled the CL1, the world\'s first commercial Synthetic Biological Intelligence system—a fusion of biology and tech with human neurons cultured directly onto silicon chips.',
      image: 'https://images.unsplash.com/photo-1581093588401-fbb62a02f120?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80',
      featured: true
    },
    {
      title: 'The Singularity Express Arrives at the Station',
      date: '2024-08-08',
      author: 'Christopher Tavolazzi',
      route: '/blog/singularity-express',
      excerpt: 'Choo Choo, Motherf**ker. The Singularity Express just pulled into the station, and it\'s one hell of a ride. Get ready for Level 2 - AI that can think and reason.',
      image: 'https://cdn.midjourney.com/2cfb73bc-4072-40fa-aa86-8cf4f842b428/0_2.png',
      featured: true
    }
  ];

  // Keep them in the order defined above by not sorting them
  const sortedPosts = featuredPosts.slice(0, limit);

  // Prepare the response object
  const responseData = {
    posts: sortedPosts,
    total: featuredPosts.length
  };

  // Set up caching with Cloudflare
  const response = json(responseData);

  // Add cache control headers
  response.headers.append('Cache-Control', 'public, max-age=300, s-maxage=1800');
  response.headers.append('Surrogate-Control', 'max-age=1800');

  // If we have access to Cloudflare platform (in production), use Cache API
  if (platform?.caches) {
    try {
      const cache = platform.caches.default;

      // Check if we have a cached response
      const cacheKey = new Request(request.url, {
        method: 'GET',
        headers: request.headers
      });

      // Try to get from cache first
      const cachedResponse = await cache.match(cacheKey);

      if (cachedResponse) {
        return cachedResponse;
      }

      // If not in cache, store this response in cache
      await cache.put(cacheKey, response.clone());

      // Log cache operation (for debugging)
      console.log(`Cached featured posts data at ${new Date().toISOString()}`);
    } catch (error) {
      console.error('Cloudflare caching error:', error);
      // Silently fail on cache errors, still return the data
    }
  }

  return response;
}