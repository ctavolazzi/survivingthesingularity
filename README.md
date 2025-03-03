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
- `src/lib/server/` - Server-side utilities
- `static/` - Static assets
- `cursor/` - Development logs and documentation

## Development Approach

This project has transitioned from a community-contributed platform to a curated educational resource. For details on this transition, see [the development log](./cursor/devlog.md).

## Contributing

While we no longer accept direct contributions to the data warehouse, we welcome code improvements and bug fixes. Please see our [style guide](./STYLE_GUIDE.md) for coding standards.

## License

This project is private and not licensed for public use or distribution.
