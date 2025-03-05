# Blog Posts Directory

This directory contains all the blog posts for the Surviving the Singularity website.

## Directory Structure

Each blog post is contained in its own subdirectory with the following files:

- `content.md`: Contains the actual content of the blog post in Markdown format
- `index.js`: Contains metadata about the post and imports the content

For example:
```
blog-posts/
├── my-blog-post/
│   ├── content.md      # The actual content in Markdown
│   └── index.js        # Metadata and exports
└── ...
```

## Important Notes

1. **Every blog post directory MUST contain both a `content.md` file and an `index.js` file.**
2. The `index.js` file must import the content from the relative path `./content.md?raw`.
3. The `blogPosts.js` file at the root of this directory imports all blog posts and exports them as an array.

## Adding a New Blog Post

Use the built-in script to create a new blog post:

```bash
npm run create-blog "Your Blog Post Title"
```

This script will:
1. Create a new directory with a slug based on your title
2. Add template files with pre-filled metadata
3. Create a placeholder image

## Common Issues

If you encounter errors related to missing `content.md` files, check that:

1. Each blog post directory has a proper `content.md` file
2. The imports in `blogPosts.js` match the actual directory names
3. The import statements in each `index.js` file are correctly referencing `./content.md?raw`