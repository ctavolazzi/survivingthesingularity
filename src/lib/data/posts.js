// $lib/data/posts.js

function getDefaultImageUrl(slug) {
  return `/images/blog/${slug}.jpg`;
}

export const posts = [
  {
    slug: 'first-post',
    title: 'My First Blog Post',
    date: '2024-08-03',
    content: 'This is the content of my first blog post...',
    get image() {
      return getDefaultImageUrl(this.slug);
    }
  },
  // Add more posts here
];