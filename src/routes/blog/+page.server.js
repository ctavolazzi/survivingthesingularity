import { getAllPosts } from '$lib/utils/markdown';
import { loadBlogPosts } from '$lib/data/blog-posts/blogPosts';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
  try {
    // First try to use the async load function
    const blogPosts = await loadBlogPosts();

    if (blogPosts && blogPosts.length > 0) {
      return {
        posts: blogPosts.map(post => ({
          title: post.title,
          date: post.date,
          author: post.author || 'Unknown',
          slug: post.slug || '', // Ensure we have a slug
          excerpt: post.excerpt || '',
          image: post.imageUrl || `/images/blog/${post.slug}.jpg` // Fallback to conventional path
        })).sort((a, b) => new Date(b.date) - new Date(a.date)) // Sort by date, newest first
      };
    }

    // Fallback to direct loading if needed
    const allPosts = getAllPosts();

    // Return only the metadata needed for the listing page
    return {
      posts: allPosts.map(post => ({
        title: post.title,
        date: post.date,
        author: post.author || 'Unknown',
        slug: post.slug,
        excerpt: post.excerpt,
        image: post.image || `/images/blog/${post.slug}.jpg` // Fallback to conventional path
      })).sort((a, b) => new Date(b.date) - new Date(a.date)) // Sort by date, newest first
    };
  } catch (error) {
    console.error('Error loading blog posts:', error);
    return { posts: [] };
  }
}

// Disable prerendering since we're now using async data fetching
export const prerender = false;