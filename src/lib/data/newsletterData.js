// This file replaces the markdown-based newsletter system with a direct data approach

export const newsletters = [
  {
    slug: 'newsletter-edition-003',
    title: 'AI Ethics and Governance: Finding Balance in the Age of Rapid Innovation',
    date: 'March 6, 2025',
    description: 'A brief summary of this newsletter edition.',
    editionNumber: 3
  },
  {
    slug: 'newsletter-edition-002',
    title: 'Surviving the Singularity Newsletter 002',
    date: 'September 10, 2024',
    description: 'Navigating AI Advancements: Tools, Trends, and Strategies',
    editionNumber: 2
  },
  {
    slug: 'newsletter-edition-001',
    title: 'Surviving the Singularity Newsletter 001',
    date: 'September 3, 2024',
    description: 'Welcome to the AI Revolution: Your Guide to Surviving and Thriving',
    editionNumber: 1
  }
];

// Helper function to get all newsletters
export function getAllNewsletters() {
  return newsletters;
}

// Helper function to get a newsletter by slug
export function getNewsletterBySlug(slug) {
  return newsletters.find(newsletter => newsletter.slug === slug);
}

// Helper function to get the latest newsletter
export function getLatestNewsletter() {
  return newsletters.sort((a, b) => b.editionNumber - a.editionNumber)[0];
}

// Helper function to get paginated newsletters
export function getPaginatedNewsletters(page = 1, perPage = 10) {
  const sortedNewsletters = [...newsletters].sort((a, b) => b.editionNumber - a.editionNumber);
  const totalNewsletters = sortedNewsletters.length;
  const totalPages = Math.ceil(totalNewsletters / perPage);

  const paginatedNewsletters = sortedNewsletters.slice((page - 1) * perPage, page * perPage);

  return {
    newsletters: paginatedNewsletters,
    pagination: {
      currentPage: page,
      totalPages,
      totalItems: totalNewsletters,
      perPage
    }
  };
}