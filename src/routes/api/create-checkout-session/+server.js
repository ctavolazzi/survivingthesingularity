import { json } from '@sveltejs/kit';

/**
 * Returns a message that preorders are no longer available
 */
export async function POST({ request }) {
  return json({
    error: 'Preorders are no longer available',
    details: 'The preorder period has ended. Please check back soon for regular purchase options.'
  }, { status: 403 });
}