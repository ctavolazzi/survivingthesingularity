# UI Component Library

This directory contains core UI components that should be used throughout the application to maintain consistency and reduce code duplication.

## Theme System

The application now uses a centralized theme system located in `src/lib/styles/theme.css`. This file contains common CSS variables for colors, spacing, and typography that should be used across components.

Benefits:
- Single source of truth for design tokens
- Consistent dark mode implementation
- Easier theme updates

## Available Components

### Button

A versatile button component with several variants.

```svelte
<script>
  import { Button } from '$lib/components/ui';
</script>

<Button>Default Button</Button>
<Button variant="secondary">Secondary Button</Button>
<Button variant="outline">Outline Button</Button>
<Button variant="accent">Accent Button</Button>
<Button variant="cta">Call to Action</Button>
<Button variant="discord">Discord Button</Button>
<Button href="/some-page" variant="primary">Link Button</Button>
```

**Props:**
- `variant`: 'primary' (default), 'secondary', 'outline', 'text', 'accent', 'cta', 'discord', 'danger'
- `size`: 'sm', 'md' (default), 'lg'
- `type`: Button type ('button' by default)
- `disabled`: Whether the button is disabled
- `fullWidth`: Whether the button should take full width
- `loading`: Whether to show loading spinner
- `icon`: Optional icon to display
- `href`: If provided, renders an `<a>` tag instead of a button

### Image

A simplified image component that handles responsive images and WebP format.

```svelte
<script>
  import { Image } from '$lib/components/ui';
</script>

<Image src="/images/example.jpg" alt="Example image" />
<Image src="/images/example.jpg" alt="Example with caption" caption="This is a caption" />
<Image src="/images/example.jpg" alt="Example with effects" border shadow hoverEffect />
```

**Props:**
- `src`: Image source (required)
- `alt`: Alt text for accessibility (required)
- `width`, `height`: Optional dimensions
- `loading`: 'lazy' (default) or 'eager'
- `class`: Additional CSS classes
- `caption`: Optional image caption
- `border`: Whether to add a border
- `rounded`: Whether to round corners (default: true)
- `shadow`: Whether to add a shadow
- `hoverEffect`: Whether to add hover effect (scale on hover)
- `srcWebp`: WebP version of the image (auto-generated if not provided)

### Card

A flexible card component for displaying content in a consistent way.

```svelte
<script>
  import { Card, Button } from '$lib/components/ui';
</script>

<Card>Basic card content</Card>

<Card variant="elevated" hoverable={true}>
  <h3>Card with title</h3>
  <p>This is a hoverable card with elevated styling.</p>
</Card>

<Card href="/some-page" hoverable={true}>
  This card is a link to another page
</Card>

<Card variant="feature" padding="lg">
  <h3>Feature Card</h3>
  <p>A card with special styling for feature highlights.</p>
  <Button>Learn More</Button>
</Card>
```

**Props:**
- `variant`: 'default', 'elevated', 'outline', 'feature'
- `padding`: 'none', 'sm', 'md' (default), 'lg'
- `fullWidth`: Whether the card should take full width
- `rounded`: Whether to use rounded corners (default: true)
- `elevation`: 'none', 'sm', 'md' (default), 'lg'
- `hoverable`: Whether to add hover effects (default: false)
- `clickable`: Whether to show a pointer cursor (default: false)
- `href`: If provided, renders an `<a>` tag instead of a div

## Best Practices

1. Use theme variables instead of hard-coded colors
2. Use UI components instead of creating custom implementations
3. Extend existing components when needed, rather than creating new ones
4. Keep components small and focused on a single responsibility
5. Use TypeScript for better prop validation and documentation