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
      text: 'Cortical Labs unveils CL1, a commercial Synthetic Biological Intelligence platform',
      tag: 'Reported',
      link: '/blog/synthetic-biological-intelligence'
    },
    {
      date: '2025-03-04',
      text: 'DARPA issues RFI on large bio-mechanical space structures',
      tag: 'Reported',
      link: '/blog/darpa-biomechanical-space-structures'
    },
    {
      date: '2025-03-28',
      text: 'Essay: Whispers of the Future - the paradigm shift in human-AI relations',
      tag: 'Commentary',
      link: '/blog/whispers-of-the-future'
    },
    {
      date: '2024-08-08',
      text: 'Commentary: what "Level 2" reasoning AI implies for the road to AGI',
      tag: 'Commentary',
      link: '/blog/singularity-express'
    },
    {
      date: '2024-08-24',
      text: 'Field notes: FarmBot deep-dive on AI-assisted precision agriculture',
      tag: 'Field Notes',
      link: '/blog/farm-bot-deep-dive'
    },
    {
      date: '2026-05-25',
      text: 'Reminder: site content is research and commentary - see disclaimer',
      tag: 'Notice',
      link: '/disclaimer'
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