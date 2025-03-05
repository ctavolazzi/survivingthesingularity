import { getPostBySlug, getAllPosts } from '$lib/utils/markdown';
import { blogPosts as importedPosts } from '$lib/data/blog-posts/blogPosts';
import { error } from '@sveltejs/kit';
import { promises as fs } from 'node:fs';
import { join } from 'node:path';

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
  const { slug } = params;

  // Check if this is an MDsveX post first (they take precedence)
  if (slug === 'test') {
    // For MDsveX posts, we don't need to do anything special here
    // The +page.js will handle importing the .md file
    return {
      post: {
        title: 'MDsveX Test',
        date: new Date().toISOString(),
        author: 'System',
        slug: 'test',
        excerpt: 'A test of our new MDsveX integration',
        image: '/images/blog/default.jpg',
        authorAvatar: null
      },
      nextPost: null,
      prevPost: null
    };
  }

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
  const allPosts = [
    // Add MDsveX test post
    {
      title: 'MDsveX Test',
      date: new Date().toISOString(),
      author: 'System',
      slug: 'test',
      excerpt: 'A test of our new MDsveX integration'
    },
    ...(importedPosts.length > 0 ? importedPosts : getAllPosts())
  ];

  // Sort by date, newest first
  const sortedPosts = allPosts.sort((a, b) => {
    if (!a.date || !b.date) return 0;
    return new Date(b.date) - new Date(a.date);
  });

  const currentIndex = sortedPosts.findIndex(p => p.slug === slug);
  const nextPost = currentIndex > 0 ? sortedPosts[currentIndex - 1] : null;
  const prevPost = currentIndex < sortedPosts.length - 1 ? sortedPosts[currentIndex + 1] : null;

  const nextPostData = nextPost ? {
    title: nextPost.title,
    slug: nextPost.slug
  } : null;

  const prevPostData = prevPost ? {
    title: prevPost.title,
    slug: prevPost.slug
  } : null;

  const safePost = {
    ...post,
    authorAvatar: null,
    image: post.image || post.imageUrl || `/images/blog/${post.slug}.jpg`
  };

  return {
    post: safePost,
    nextPost: nextPostData,
    prevPost: prevPostData
  };
}

// Disable prerendering since we're using async data fetching
export const prerender = false;

// Provide entries for prerendering all posts
export function entries() {
  const posts = [
    { slug: 'test' },
    ...(importedPosts.length > 0 ? importedPosts : getAllPosts()).map(post => ({
      slug: post.slug || ''
    }))
  ];
  return posts;
}