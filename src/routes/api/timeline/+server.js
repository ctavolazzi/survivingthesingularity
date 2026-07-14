import { json } from '@sveltejs/kit';
import timelineItems from '$lib/data/timelineItems.json';
import { rateLimit } from '$lib/server/rateLimit.js';

export async function GET({ url, getClientAddress }) {
  const ip = getClientAddress();
  const { allowed } = rateLimit(`timeline:${ip}`, 60, 60_000);
  if (!allowed) {
    return json({ error: 'Too many requests.' }, { status: 429 });
  }

  const page = Math.max(1, parseInt(url.searchParams.get('page') || '1') || 1);
  const limit = Math.min(50, Math.max(1, parseInt(url.searchParams.get('limit') || '5') || 5));

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