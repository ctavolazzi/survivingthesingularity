import { json } from '@sveltejs/kit';

/**
 * Endpoint to fetch news ticker items with Cloudflare caching
 * @param {Object} request - The request object
 * @returns {Object} JSON response with news ticker items
 */
export async function GET({ url, platform, request }) {
  // Get query parameters with defaults
  const limit = parseInt(url.searchParams.get('limit') || '5');

  // Define news items
  // In a real application, these could come from a database or external API
  const newsItems = [
    {
      date: '2025-03-06',
      text: 'New synthetic biological intelligence breakthrough announced by Cortical Labs',
      tag: 'Breaking',
      link: '/blog/synthetic-biological-intelligence'
    },
    {
      date: '2025-03-04',
      text: 'DARPA seeks proposals for biological space structures - major implications for space industry',
      tag: 'New',
      link: '/blog/darpa-biomechanical-space-structures'
    },
    {
      date: '2025-03-01',
      text: 'Claude 4 Opus released with unprecedented reasoning capabilities',
      tag: 'AI News',
      link: '/blog/claude-projects-weekend-project'
    },
    {
      date: '2024-02-28',
      text: 'New regulatory framework for AGI proposed by international coalition',
      tag: 'Policy',
      link: '/blog/singularity-express'
    },
    {
      date: '2024-02-25',
      text: 'Preview our exclusive book "Surviving the Singularity" - first chapter now available',
      tag: 'Book',
      link: '/sample'
    },
    {
      date: '2024-02-22',
      text: 'Latest FarmBot update adds advanced computer vision capabilities',
      tag: 'Tech',
      link: '/blog/farm-bot-deep-dive'
    },
    {
      date: '2024-02-20',
      text: 'Our newsletter has reached 10,000 subscribers! Thank you for your support.',
      tag: 'Milestone',
      link: '/blog/robot-farm-bot'
    }
  ];

  // Apply limit and return newer items first
  const limitedItems = newsItems.slice(0, limit);

  // Prepare the response object
  const responseData = {
    items: limitedItems,
    total: newsItems.length,
    timestamp: new Date().toISOString() // Add timestamp to force refresh
  };

  // Set up caching with Cloudflare
  const response = json(responseData);

  // Add cache control headers to prevent caching
  response.headers.append('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  response.headers.append('Pragma', 'no-cache');
  response.headers.append('Expires', '0');

  // If we have access to Cloudflare platform (in production), use Cache API and KV
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

      // If Cloudflare KV is available, we could use it for storing the news items
      // This is just an example of how it might be implemented
      if (platform.env && platform.env.NEWS_TICKER) {
        try {
          // Check if we have news items in KV
          const kvNews = await platform.env.NEWS_TICKER.get('latest_news', { type: 'json' });

          if (kvNews && Array.isArray(kvNews) && kvNews.length > 0) {
            // Use news items from KV instead
            const kvResponse = json({
              items: kvNews.slice(0, limit),
              total: kvNews.length,
              source: 'kv'
            });

            // Add same cache headers
            kvResponse.headers.append('Cache-Control', 'public, max-age=180, s-maxage=600');
            kvResponse.headers.append('Surrogate-Control', 'max-age=600');

            // Store in cache
            await cache.put(cacheKey, kvResponse.clone());

            return kvResponse;
          }
        } catch (kvError) {
          console.error('KV error:', kvError);
          // Fall back to hardcoded news if KV fails
        }
      }

      // If not in cache or KV failed, store this response in cache
      await cache.put(cacheKey, response.clone());

      // Log cache operation (for debugging)
      console.log(`Cached news ticker data at ${new Date().toISOString()}`);
    } catch (error) {
      console.error('Cloudflare caching error:', error);
      // Silently fail on cache errors, still return the data
    }
  }

  return response;
}