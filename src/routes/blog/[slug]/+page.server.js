import { getPostBySlug, getAllPosts } from '$lib/utils/markdown';
import { blogPosts as importedPosts } from '$lib/data/blog-posts/blogPosts';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export function load({ params }) {
  const { slug } = params;

  // First try to find the post from the imported posts (client-side imports)
  const importedPost = importedPosts.find(p => p.slug === slug);

  // Then try the server-side markdown loader as backup
  const markdownPost = getPostBySlug(slug);

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
  const allPosts = importedPosts.length > 0 ? importedPosts : getAllPosts();

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

// Enable prerendering for all blog posts
export const prerender = true;

// Provide entries for prerendering all posts
export function entries() {
  const posts = importedPosts.length > 0 ? importedPosts : getAllPosts();
  return posts.map(post => ({
    slug: post.slug || ''
  }));
}