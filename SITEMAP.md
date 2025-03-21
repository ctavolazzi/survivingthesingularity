# Site Structure and Data Flow
*Last Updated: 2024-03-19 15:30 UTC*

## 1. Layout Components
- `+layout.svelte` (Root Layout)
  - Components:
    - `Navbar.svelte` - Main navigation
    - `Footer.svelte` - Site footer
    - `FloatingProgressBar.svelte` - Reading progress indicator
  - Data Flow:
    - Dark mode state management via `darkMode` store
    - Navigation handling with `afterNavigate`

## 2. Main Pages

### Home Page (`/`)
- Components:
  - `Countdown.svelte` - Singularity countdown timer
  - `Timeline.svelte` - Event timeline
  - `BookCallout.svelte` - Book promotion
  - `FuturePredictions.svelte` - Future predictions display
  - `NewsletterSignup.svelte` - Newsletter subscription
  - `FAQ.svelte` - Frequently asked questions
  - `LatestNews.svelte` - Latest updates
  - `BookSample.svelte` - Book preview
  - `DiscordButton.svelte` - Discord community link
  - `NewsTicker.svelte` - News updates
  - `FeaturedPosts.svelte` - Featured blog posts
  - `TreasureTavernAd.svelte` - Advertisement component
- Data Sources:
  - Blog posts from `$lib/data/blog-posts/blogPosts.js`
  - Timeline items from `$lib/data/timelineItems.json`
  - Test data from Supabase

### Blog (`/blog`)
- Components:
  - `NewsletterSignup.svelte`
  - `DiscordButton.svelte`
  - `FeaturedPosts.svelte`
  - `NewsTicker.svelte`
  - `TreasureTavernAd.svelte`
- Data Flow:
  - Blog posts loaded via `loadBlogPosts()`
  - Posts categorized and tagged dynamically

### Newsletter (`/newsletter`)
- Components:
  - `NewsletterLayout.svelte`
  - `NewsletterContent.svelte`
  - `NewsletterList.svelte`
- Data Flow:
  - Newsletter data from `$lib/data/newsletterData.js`
  - Pagination handled server-side
  - Dynamic component loading via `getNewsletterComponent`

### Book Section (`/book/[sectionId]`)
- Components:
  - `Pagination.svelte`
  - `FloatingPopupProgressBar.svelte`
  - `FloatingQuotePopup.svelte`
  - `Spacer.svelte`
  - `Markdown.svelte`
  - `TableOfContents.svelte`
- Data Flow:
  - Book content from `$lib/bookContent.js`
  - Section content loaded dynamically
  - Progress tracking via `bookPage` store

### Contact Page (`/contact`)
- Components:
  - `ContactForm.svelte`
- Data Flow:
  - Form submission handled client-side
  - Email service integration

### Profile Pages (`/profile/[username]`)
- Components:
  - `Avatar.svelte` (for profile images)
- Data Flow:
  - Profile data from Supabase
  - Avatar storage in Supabase storage

### Code Conductor Page (`/code-conductor`)
- Components:
  - Custom UI components for product showcase
  - Modal components for payment/contribution
- Data Flow:
  - GitHub integration for downloads
  - Payment processing (placeholder)

## 3. Data Sources

### Primary Data Sources:
1. **Supabase**
   - User profiles
   - Authentication
   - Test data

2. **Static Data**
   - Blog posts (`$lib/data/blog-posts/`)
   - Newsletter content (`$lib/data/newsletterData.js`)
   - Book content (`$lib/bookContent.js`)
   - Timeline items (`$lib/data/timelineItems.json`)

3. **File System**
   - Images and assets
   - Markdown content

### API Endpoints:
1. `/api/timeline`
   - Paginated timeline data
   - Returns JSON with items and pagination info

2. `/api/newsletter/subscribe`
   - Newsletter subscription handling
   - Email service integration

## 4. State Management

### Stores:
1. `darkMode` - Theme management
2. `bookPage` - Book reading progress
3. `tacticLibrary` - Tactics data
4. `blogPosts` - Blog post data

### Client-Side State:
- Navigation state
- Form states
- Modal states
- Loading states

## 5. Component Categories

### UI Components
- `Button.svelte` - Versatile button with multiple variants
- `Input.svelte` - Form input with validation
- `Checkbox.svelte` - Checkbox with label support
- `Spacer.svelte` - Utility for spacing

### Layout Components
- `Navbar.svelte` - Main navigation
- `ResponsiveImage.svelte` - Image handling with WebP support
- `SafeResponsiveImage.svelte` - Type-safe image wrapper

### Content Components
- `LatestNews.svelte` - Recent updates
- `FeaturedPosts.svelte` - Featured articles
- `NewsTicker.svelte` - Scrolling news
- `CountdownTimer.svelte` - Time-based displays
- `Countdown.svelte` - Detailed countdown

### Interactive Components
- `NewsletterSignup.svelte` - Newsletter subscription
- `ContactForm.svelte` - Contact form
- `SocialShare.svelte` - Social sharing
- `Auth.svelte` - Authentication

### Data Display Components
- `NewsletterList.svelte` - Newsletter listing
- `NewsletterContent.svelte` - Newsletter content
- `RoboticsCompanies.svelte` - Company data
- `Avatar.svelte` - User avatars

### Utility Components
- `JumpToLatest.svelte` - Scroll to latest content
- `PreorderDropin.svelte` - Pre-order functionality
- `SocialShare.svelte` - Social media sharing