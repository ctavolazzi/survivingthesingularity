import { getPostBySlug, getAllPosts } from '$lib/utils/markdown';
import { loadBlogPosts } from '$lib/data/blog-posts/blogPosts';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
  const { slug } = params;
  let importedPosts = [];
  let markdownPost = null;

  // First try to load all posts using the dynamic import method
  // This is the preferred method for Cloudflare Workers
  try {
    importedPosts = await loadBlogPosts();
  } catch (err) {
    console.error('Error loading blog posts via dynamic imports:', err);
  }

  // Find the requested post from the imported posts
  const importedPost = importedPosts.find(p => p.slug === slug);

  // Try the server-side markdown loader as backup (won't work in Cloudflare)
  try {
    markdownPost = getPostBySlug(slug);
  } catch (err) {
    console.error('Error loading post via filesystem (expected in Cloudflare):', err);
    // This is expected to fail in Cloudflare, so we'll just continue
  }

  // Merge data from both sources, preferring the imported post data when available
  const post = importedPost ? {
    ...markdownPost,
    ...importedPost,
    // If markdown parsing was successful, use that HTML content
    content: markdownPost?.content || importedPost.content,
    rawContent: markdownPost?.rawContent || importedPost.content
  } : markdownPost;

  if (!post) {
    throw error(404, {
      message: 'Post not found',
      id: slug
    });
  }

  // Get all posts for navigation
  let allPosts = [];
  if (importedPosts.length > 0) {
    allPosts = importedPosts;
  } else {
    try {
      allPosts = getAllPosts();
    } catch (err) {
      console.error('Error getting all posts via filesystem (expected in Cloudflare):', err);
      // This is expected to fail in Cloudflare, so we'll just continue with an empty array
    }
  }

  // Sort by date, newest first (if there are dates, otherwise use array order)
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

  // Create a safe version of the post with explicit authorAvatar handling
  const safePost = {
    ...post,
    // Force null authorAvatar during SSR to prevent 404s
    authorAvatar: null,
    image: post.image || post.imageUrl || `/images/blog/${post.slug}.jpg` // Fallback to conventional path
  };

  return {
    post: safePost,
    nextPost: nextPostData,
    prevPost: prevPostData
  };
}

// Disable prerendering for dynamic blog posts
export const prerender = false;

// Provide entries for prerendering all posts
export async function entries() {
  try {
    const posts = await loadBlogPosts();
    return posts.map(post => ({
      slug: post.slug || ''
    }));
  } catch (err) {
    console.error('Error generating entries:', err);
    return [];
  }
}