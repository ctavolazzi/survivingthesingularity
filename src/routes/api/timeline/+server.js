import { json } from '@sveltejs/kit';
import timelineItems from '$lib/data/timelineItems.json';

/**
 * Endpoint to fetch paginated timeline data
 * @param {Object} params - Request parameters
 * @returns {Object} JSON response with paginated timeline data
 */
export async function GET({ url }) {
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = parseInt(url.searchParams.get('limit') || '5');

  const start = (page - 1) * limit;
  const end = start + limit;

  const paginatedItems = timelineItems.timelineItems.slice(start, end);
  const totalPages = Math.ceil(timelineItems.timelineItems.length / limit);

  return json({
    items: paginatedItems,
    pagination: {
      currentPage: page,
      totalPages,
      totalItems: timelineItems.timelineItems.length,
      hasMore: page < totalPages
    }
  });
}