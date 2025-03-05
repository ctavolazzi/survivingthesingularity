import { loadBlogPosts } from '$lib/data/blog-posts/blogPosts';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
  try {
    // Only use the dynamic import method for loading blog posts
    const blogPosts = await loadBlogPosts();

    // Return blog post metadata for listing
    return {
      posts: blogPosts.map(post => ({
        title: post.title,
        date: post.date,
        author: post.author || 'Unknown',
        slug: post.slug || '',
        excerpt: post.excerpt || '',
        image: post.imageUrl || `/images/blog/${post.slug}.jpg`
      })).sort((a, b) => new Date(b.date) - new Date(a.date))
    };
  } catch (error) {
    console.error('Error loading blog posts:', error);
    return { posts: [] };
  }
}

// Disable prerendering for blog pages
export const prerender = false;

// Explicitly set ssr to false for Cloudflare compatibility
export const ssr = false;