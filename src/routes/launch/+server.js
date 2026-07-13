import { redirect } from '@sveltejs/kit';

// /launch retired 2026-07-12: the site sells one thing, the $5 standard-edition
// preorder. Old emails and backlinks land on the preorder page instead.
export function GET() {
  throw redirect(301, '/early-access');
}
