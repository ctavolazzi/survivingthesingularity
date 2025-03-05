/**
 * This file provides a function to load all blog posts.
 * It's designed to work in both Node.js and Cloudflare environments.
 */

// Create a function to load all blog posts
export async function loadBlogPosts() {
  let posts = [];

  // Helper function for importing posts
  async function importPost(path, slug) {
    try {
      const module = await import(path);
      if (module && module.post) {
        // Ensure slug is set if not provided in the post
        if (!module.post.slug && slug) {
          module.post.slug = slug;
        }
        posts.push(module.post);
      }
    } catch (error) {
      console.error(`Error importing ${path}:`, error.message);
    }
  }

  // Define all blog posts with their import paths and slug fallbacks
  const postModules = [
    { path: './darpa-biomechanical-space-structures/index.js', slug: 'darpa-biomechanical-space-structures' },
    { path: './robot-farm-bot/index.js', slug: 'robot-farm-bot' },
    { path: './singularity-express/index.js', slug: 'singularity-express' },
    { path: './farm-bot-deep-dive/index.js', slug: 'farm-bot-deep-dive' },
    { path: './claude-projects-weekend-project/index.js', slug: 'claude-projects-weekend-project' }
  ];

  // Import all posts in parallel using Promise.all
  await Promise.all(postModules.map(post => importPost(post.path, post.slug)));

  // Sort posts by date (newest first)
  return posts.sort((a, b) => {
    // Handle missing dates gracefully
    if (!a.date) return 1;
    if (!b.date) return -1;
    return new Date(b.date) - new Date(a.date);
  });
}

// For backward compatibility, export an empty array as blogPosts
// This will be populated after loading
export const blogPosts = [];