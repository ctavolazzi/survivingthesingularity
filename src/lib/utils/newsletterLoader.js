// This file provides utilities to load newsletter content components dynamically

// Import all newsletter components
import NewsletterEdition003 from '$lib/components/newsletters/NewsletterEdition003.svelte';
import NewsletterEdition001 from '$lib/components/newsletters/NewsletterEdition001.svelte';
import NewsletterEdition002 from '$lib/components/newsletters/NewsletterEdition002.svelte';

// Map of newsletter slugs to their component
const newsletterComponents = {
  'newsletter-edition-003': NewsletterEdition003,
  'newsletter-edition-001': NewsletterEdition001,
  'newsletter-edition-002': NewsletterEdition002
};

/**
 * Get the Svelte component for a newsletter by its slug
 * @param {string} slug - The newsletter slug
 * @returns {object|null} - The Svelte component or null if not found
 */
export function getNewsletterComponent(slug) {
  return newsletterComponents[slug] || null;
}

/**
 * Generate table of contents from HTML content
 * This is a client-side function to be used in onMount
 * @param {string} contentElement - The DOM element containing the newsletter content
 * @returns {Array} - Array of TOC items with id, text, and level
 */
export function generateTableOfContents(contentElement) {
  if (!contentElement) return [];

  const headers = contentElement.querySelectorAll('h2, h3');
  return Array.from(headers).map(header => ({
    id: header.id || header.textContent.toLowerCase().replace(/\s+/g, '-'),
    text: header.textContent,
    level: parseInt(header.tagName.charAt(1))
  }));
}