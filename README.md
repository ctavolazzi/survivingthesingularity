# Surviving the Singularity

A resource platform providing educational content to help people prepare for the technological Singularity.

## Project Overview

Surviving the Singularity is a web application built with SvelteKit that offers:

- Educational resources about AI and the technological Singularity
- A data warehouse with curated information on AI developments, robotics, and future projections
- Book samples and resources from "Surviving the Singularity"
- Blog posts and news related to AI advancements
- Newsletters to keep users updated on significant technological changes

## Tech Stack

- **Frontend**: SvelteKit, Tailwind CSS, Flowbite components
- **Backend**: Supabase
- **Data Processing**: Markdown processing with marked/remark
- **Deployment**: Adapts to various hosting environments

## Development

### Getting Started

1. Clone the repository:
```bash
git clone [repository-url]
cd survivingthesingularity
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

4. Start the development server:
```bash
npm run dev -- --open
```

### Building for Production

```bash
npm run build
```

Preview the production build with:
```bash
npm run preview
```

## Project Structure

- `src/routes/` - Application pages and API endpoints
- `src/lib/components/` - Reusable UI components
- `src/lib/data/` - Content and data resources
- `src/lib/content/` - Blog posts and other content in markdown format
- `src/lib/utils/` - Utility functions and helpers
- `src/lib/server/` - Server-side utilities
- `static/` - Static assets
- `cursor/` - Development logs and documentation

## Blog System

The blog system follows SvelteKit conventions:

- **Blog posts** are stored as markdown files with frontmatter in `src/lib/content/blog/`
- Each post has its own markdown file with metadata in the frontmatter section
- Server-side loading is handled through `+page.server.js` files
- Blog images are stored in `static/images/blog/`

For detailed instructions on adding new blog posts, see the [Blog Content Guide](src/lib/content/README.md).

## Working with Blog Posts

Blog posts are stored in the `src/lib/data/blog-posts` directory, with each post in its own subdirectory containing:

- `content.md`: The main content of the blog post in Markdown format
- `index.js`: Metadata and exports for the blog post

### Adding a New Blog Post

To create a new blog post:

```bash
# Using npm
npm run create-blog "Your Blog Post Title"

# Using the script directly
node scripts/create-blog-post.js "Your Blog Post Title"
```

This will:
1. Create a new directory in `src/lib/data/blog-posts` with a slug based on the title
2. Add a template `content.md` and `index.js` file
3. Pre-fill some metadata fields with the current date

### Migrating Blog Posts

If you have blog posts in the old format (`.md` files in `src/content/blog`), you can migrate them to the new format:

```bash
npm run migrate-blog
```

This will:
1. Find all `.md` files in the old location
2. Create a directory structure in `src/lib/data/blog-posts` for each post
3. Generate the necessary `content.md` and `index.js` files

## Development Approach

This project has transitioned from a community-contributed platform to a curated educational resource. For details on this transition, see [the development log](./cursor/devlog.md).

## Contributing

While we no longer accept direct contributions to the data warehouse, we welcome code improvements and bug fixes. Please see our [contributing guidelines](./docs/contributing/CONTRIBUTING.md) for detailed information on how to contribute to this project.

Our contributing documentation includes:
- [Style Guide](./docs/contributing/STYLE_GUIDE.md) - Code style and formatting guidelines
- [Supabase Security Guidelines](./docs/contributing/SUPABASE_SECURITY.md) - Security best practices for database work

## License

This project is private and not licensed for public use or distribution.
