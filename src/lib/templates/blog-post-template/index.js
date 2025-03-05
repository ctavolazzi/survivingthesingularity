import content from './content.md?raw';

export const post = {
  title: "Title of Your Blog Post",
  date: "2023-01-01",
  author: "Your Name",
  authorAvatar: null, // Optional: path to avatar image
  excerpt: "A short excerpt of your blog post (optional)",
  imageUrl: "/images/blog/your-post-slug.jpg", // Update this path
  tags: ["tag1", "tag2", "tag3"], // Optional: add tags
  content
};