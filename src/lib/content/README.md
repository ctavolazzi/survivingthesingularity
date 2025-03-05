# Content Management Guide

## Blog Posts

### Adding a New Blog Post

To add a new blog post, create a new Markdown file in the `src/lib/content/blog/` directory. The filename should be the URL-friendly slug of the post (e.g., `my-new-post.md`).

Each post should include frontmatter at the top of the file, followed by the content in Markdown format.

#### Example:

```md
---
title: "My New Blog Post Title"
date: "2024-03-04"
author: "Author Name"
image: "/images/blog/my-new-post.jpg"
excerpt: "A short excerpt that describes the post. This will appear in the post listings."
---

# My New Blog Post Title

This is the content of my blog post. You can use all standard Markdown formatting.

## Subheading

- List item
- Another list item

[Link text](https://example.com)

![Image alt text](/images/some-image.jpg)
```

### Required Frontmatter Fields

- `title`: The title of the blog post
- `date`: The publication date in YYYY-MM-DD format
- `author`: The author's name

### Optional Frontmatter Fields

- `image`: Path to the post's featured image. If not provided, it will look for an image at `/images/blog/[slug].jpg`
- `excerpt`: A short description of the post. If not provided, one will be generated from the first few sentences of content.

### Adding Images

Place blog post images in the `static/images/blog/` directory. The recommended naming convention is to use the same slug as your post for the primary image (e.g., `my-new-post.jpg`).

### Formatting Guidelines

- Use Markdown headings (# for title, ## for sections, etc.)
- Include appropriate spacing between sections
- Keep paragraphs relatively short for readability
- Use images to break up text and illustrate concepts
- Include links to relevant resources or sources

## Publishing Workflow

1. Create the Markdown file in the correct directory
2. Add any required images to the static directory
3. Test locally by running the development server
4. Commit your changes and push to the repository
5. The site will automatically rebuild and deploy the new content

# Blog Post Structure

> ⚠️ NOTE: The blog post system has been updated. The new structure is described below.

## New Blog Post Structure

Blog posts are now stored in the `src/lib/data/blog-posts` directory, with each post having its own subdirectory:

```
src/lib/data/blog-posts/
├── my-first-blog-post/
│   ├── content.md       # Content in Markdown format
│   └── index.js         # Metadata and exports
├── another-blog-post/
│   ├── content.md
│   └── index.js
└── ...
```

### Creating a New Blog Post

Use the built-in script to create a new blog post:

```bash
npm run create-blog "Your Blog Post Title"
```

This will:
1. Create a new directory with a slug based on your title
2. Add template files with pre-filled metadata

### Blog Post Files

#### content.md

This file contains the content of your blog post in Markdown format, with frontmatter metadata:

```markdown
---
title: My Blog Post Title
date: 2023-03-04
author: Your Name
excerpt: A short excerpt of your blog post (optional)
---

# My Blog Post Title

Your content here...
```

#### index.js

This file exports the post metadata and content:

```javascript
import content from './content.md?raw';

export const post = {
  title: "My Blog Post Title",
  date: "2023-03-04",
  author: "Your Name",
  authorAvatar: "/path/to/avatar.jpg", // Optional
  excerpt: "A short excerpt of your blog post",
  imageUrl: "/images/blog/my-blog-post-title.jpg",
  tags: ["tag1", "tag2"],
  content
};
```

### Images

Blog post images should be placed in the `static/images/blog/` directory, with the filename matching the post slug:

```
static/images/blog/my-blog-post-title.jpg
```

## Legacy Structure (Deprecated)

> ⚠️ This structure is deprecated and is only kept for backward compatibility.

The old structure used Markdown files directly in the `src/content/blog` directory:

```
src/content/blog/
├── my-first-blog-post.md
├── another-blog-post.md
└── ...
```

To migrate posts from the old format to the new format, run:

```bash
npm run migrate-blog
```