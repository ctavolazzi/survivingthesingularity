import { error } from '@sveltejs/kit';
import { getNewsletterBySlug, getAllNewsletters } from '$lib/data/newsletterData.js';

export async function load({ params }) {
  const { slug } = params;

  try {
    // Get the newsletter by slug
    const newsletter = getNewsletterBySlug(slug);

    if (!newsletter) {
      console.error(`Newsletter not found for slug: ${slug}`);
      throw error(404, 'Newsletter not found');
    }

    // Get all newsletters for navigation
    const allNewsletters = getAllNewsletters();

    return {
      newsletter,
      allNewsletters
    };
  } catch (e) {
    console.error(`Error loading newsletter ${slug}:`, e);
    throw error(404, 'Newsletter not found');
  }
}