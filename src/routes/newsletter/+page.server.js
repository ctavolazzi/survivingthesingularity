import { error } from '@sveltejs/kit';
import { getPaginatedNewsletters, getLatestNewsletter } from '$lib/data/newsletterData.js';

export async function load({ url, isPrerendering }) {
  try {
    // Default values for pagination
    let page = 1;
    let perPage = 10;

    // Only try to access searchParams if not prerendering
    if (!isPrerendering && url.searchParams) {
      page = parseInt(url.searchParams.get('page') || '1', 10);
      perPage = parseInt(url.searchParams.get('perPage') || '10', 10);
    }

    // Get paginated newsletters
    const { newsletters, pagination } = getPaginatedNewsletters(page, perPage);

    // Get the latest newsletter
    const latestNewsletter = getLatestNewsletter();

    return {
      newsletters,
      latestNewsletter,
      pagination
    };
  } catch (e) {
    console.error('Error loading newsletters:', e);
    throw error(500, 'Unable to load newsletters');
  }
}

// Disable prerendering for this page
export const prerender = false;