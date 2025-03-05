# Newsletter System

This directory contains all the newsletter editions for Surviving the Singularity.

## Adding a New Newsletter

### Using the Script (Recommended)

The easiest way to create a new newsletter is to use the provided script:

```bash
node scripts/create-newsletter.js "Your Newsletter Title"
```

This will:
1. Create a new markdown file with the correct naming convention
2. Set the correct edition number automatically
3. Fill in the template with your title and today's date
4. Open the file in your default editor

### Manual Creation

If you prefer to create newsletters manually:

1. Create a new markdown file in this directory named `newsletter-edition-XXX.md` (replace XXX with the next edition number, padded to 3 digits)
2. Copy the template from `src/lib/components/NewsletterTemplate.md`
3. Update the frontmatter (title, date, description, edition)
4. Add your content

## Markdown Format

Each newsletter uses a standard format:

```md
---
title: "Your Newsletter Title"
date: "YYYY-MM-DD"
description: "A brief summary of this newsletter."
edition: XXX
---

# Your Content Here
```

The frontmatter (between the `---` lines) contains metadata about the newsletter.

## Publishing Workflow

1. Create a new newsletter file using the script or manually
2. Write your content in markdown format
3. Preview your newsletter by running the development server
4. Push your changes to deploy the newsletter
5. The system will automatically include your new newsletter in the newsletter list

## Pagination

The newsletter system includes pagination to handle large numbers of editions. By default, it shows 10 newsletters per page, but this can be adjusted by adding a `perPage` query parameter to the URL, e.g. `/newsletter?perPage=20`.

## Features

- Automatic sorting by edition number (newest first)
- Full-text search of newsletters
- Responsive design for all screen sizes
- Pagination for handling many newsletter editions
- Markdown support for rich content