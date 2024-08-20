// Import all post index files dynamically
const postFiles = import.meta.glob('./**/index.js', { eager: true });

// Function to get default image URL
function getDefaultImageUrl(slug) {
  return `/images/blog/${slug}.jpg`;
}

// Process and export posts
export const posts = Object.entries(postFiles)
  .map(([key, module]) => {
    const { post } = module;
    const slug = key.split('/')[1]; // Get the folder name as slug
    return {
      ...post,
      slug,
      image: post.imageUrl || getDefaultImageUrl(slug),
      excerpt: post.excerpt || (post.content && post.content.split('\n').slice(0, 2).join('\n') + '...') || ''
    };
  })
  .filter(post => post.title && post.date) // Ensure we only include valid posts
  .sort((a, b) => new Date(b.date) - new Date(a.date)); // Sort by date, newest first

console.log('Processed posts:', posts); // For debugging