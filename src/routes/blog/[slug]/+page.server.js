import { loadBlogPosts } from '$lib/data/blog-posts/blogPosts';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
  const { slug } = params;

  try {
    // Load all posts using the dynamic import method
    const allPosts = await loadBlogPosts();

    // Find the requested post
    const post = allPosts.find(p => p.slug === slug);

    if (!post) {
      throw error(404, {
        message: 'Post not found',
        id: slug
      });
    }

    // Sort posts by date, newest first
    const sortedPosts = [...allPosts].sort((a, b) => {
      if (!a.date || !b.date) return 0;
      return new Date(b.date) - new Date(a.date);
    });

    const currentIndex = sortedPosts.findIndex(p => p.slug === slug);
    const nextPost = currentIndex > 0 ? sortedPosts[currentIndex - 1] : null;
    const prevPost = currentIndex < sortedPosts.length - 1 ? sortedPosts[currentIndex + 1] : null;

    // Include only essential data for navigation
    const nextPostData = nextPost ? {
      title: nextPost.title,
      slug: nextPost.slug
    } : null;

    const prevPostData = prevPost ? {
      title: prevPost.title,
      slug: prevPost.slug
    } : null;

    return {
      post: {
        ...post,
        authorAvatar: null,
        image: post.image || post.imageUrl || `/images/blog/${post.slug}.jpg`
      },
      nextPost: nextPostData,
      prevPost: prevPostData
    };
  } catch (err) {
    console.error(`Error loading post (${slug}):`, err);
    throw error(500, {
      message: 'Error loading post',
      id: slug
    });
  }
}

// Disable prerendering for dynamic blog posts
export const prerender = false;

// Explicitly set ssr to false for Cloudflare compatibility
export const ssr = false;