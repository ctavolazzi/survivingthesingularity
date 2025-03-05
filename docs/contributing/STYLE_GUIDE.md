# Surviving the Singularity Style Guide

## Component Structure
- Each component should follow this structure:
  1. `<script>` block (imports, props, logic)
  2. Template markup
  3. `<style>` block (only for component-specific styles)

## Naming Conventions
- Components: PascalCase (e.g., NewsletterSignup.svelte)
- Files and directories: kebab-case (e.g., timeline-items.json)
- Functions: camelCase (e.g., handleSubmit)
- CSS classes: kebab-case (e.g., newsletter-form)

## CSS Approach
- Use Tailwind for layout and utility classes
- Use component CSS for animations and component-specific styling
- Prefer Tailwind's built-in dark mode over custom implementations
- Avoid inline styles except for dynamic values

## State Management
- Use Svelte stores for global state
- Use component state for local concerns
- Document data flow between components

## API Architecture
- All data mutations should go through server endpoints
- Client-side code should only read data, not modify it directly
- Use environment variables for sensitive information
- Validate all user input on both client and server

## Security Guidelines
- Never expose API keys in client-side code
- Store sensitive values in `.env` files (never commit to version control)
- Use `$env/static/private` for server-side env vars
- Use `$env/static/public` for client-side env vars
- Implement proper authentication and authorization