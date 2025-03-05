import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export function load() {
  // Pre-order period has ended, redirect to homepage
  throw redirect(303, '/');
}