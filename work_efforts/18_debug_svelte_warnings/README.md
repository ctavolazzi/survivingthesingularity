# Debug Svelte Warnings

## Overview
This work effort focuses on systematically addressing Svelte compiler warnings, CSS issues, and accessibility concerns in the SurvivingTheSingularity codebase. We'll tackle one issue at a time to ensure each fix is properly implemented and tested.

## Issues to Address
1. Unused CSS selectors
2. Accessibility warnings
3. Unused exports
4. Other compiler warnings
5. 404 errors for image files

## Plan of Action
1. Run the development server to identify all warnings
2. Categorize warnings by type and severity
3. Fix each issue one at a time, starting with high-impact warnings
4. Verify fixes and ensure no regressions
5. Document patterns to avoid similar issues in the future

## Progress Tracking
- [x] Run initial diagnostics
- [x] Fixed CSS import placement in app.css
- [x] Fixed accessibility issue in AGIRoadmap.svelte (added keyboard event handler)
- [x] Fixed accessibility issue in NewsTicker.svelte (added ARIA role)
- [x] Fixed accessibility issue in Image.svelte (made figcaption a direct child of figure)
- [x] Fixed unused CSS selectors in AGIRoadmap.svelte
- [x] Fixed unused export properties in NewsTicker.svelte
- [x] Fixed unused export properties in BookCallout.svelte
- [x] Removed many unused CSS selectors in Timeline.svelte
- [x] Fixed unused CSS class in FeaturedPosts.svelte by applying Tailwind classes directly
- [x] Removed large number of unused CSS selectors in start-here/+page.svelte related to TreasureTavernAd
- [x] Fixed image 404 errors by preventing automatic WebP generation in Image.svelte
- [ ] Fix remaining unused CSS selectors in pages
- [ ] Final verification

## Technical Approach
For each issue:
1. Identify the specific file and line number
2. Understand the warning context
3. Implement the minimal necessary fix
4. Test to ensure the warning is resolved
5. Document the fix for future reference

## Fixes Applied

### Accessibility Issues
1. **AGIRoadmap.svelte**: Added keyboard event handling to div with onClick event
   ```svelte
   on:keydown={(e) => {
     if (e.key === 'Enter' || e.key === ' ') {
       e.preventDefault();
       toggleFAQ(`${technology.name}-${index}`);
     }
   }}
   ```

2. **NewsTicker.svelte**: Added ARIA role to div with mouseenter/mouseleave events
   ```svelte
   role="region"
   aria-label="News Ticker"
   ```

3. **Image.svelte**: Replaced div with figure element for proper figcaption nesting
   ```svelte
   <figure class="image-container">
     <!-- content -->
     <figcaption><!-- caption --></figcaption>
   </figure>
   ```

### CSS Issues
1. **app.css**: Moved @import statement to the top of the file
   ```css
   /* Import centralized theme */
   @import './lib/styles/theme.css';

   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

2. **AGIRoadmap.svelte**: Removed unused CSS selectors
   - `.article-accordion:hover`
   - `.article-accordion`
   - `.article-accordion button:focus-visible`

3. **Timeline.svelte**: Removed numerous unused CSS selectors
   - `.singularity-cta-container`
   - `.singularity-cta-content`
   - `.singularity-cta-title`
   - `.singularity-cta-buttons`
   - `.singularity-cta-button`
   - `.book-button`, `.book-button:hover`
   - `.discord-button-container`
   - `.discord-button`, `.discord-button:hover`
   - `.discord-icon`
   - `.first-100-badge`
   - `.singularity-cta-description`
   - `.path-to-singularity-wrapper`

4. **FeaturedPosts.svelte**: Fixed unused CSS selector by applying Tailwind classes
   - Replaced `.featured-image` with direct Tailwind classes `class="w-full h-full object-cover block"`

5. **start-here/+page.svelte**: Removed numerous unused CSS selectors related to TreasureTavernAd component
   - Removed `.treasure-tavern-section`, `.treasure-tavern-ad`, and all related selectors
   - These were conflicting with the component's own styles

### Unused Exports
1. **NewsTicker.svelte**: Changed unused export props to export const
   ```svelte
   export const speed = 30;
   export const autoplay = true;
   export const pauseOnHover = true;
   ```

2. **BookCallout.svelte**: Changed unused export props to export const
   ```svelte
   export const imageSrc = bookCoverImage;
   export const imageWebPSrc = bookCoverImageWebP;
   ```

### Image Loading Issues
1. **Image.svelte**: Fixed 404 errors by removing automatic WebP generation
   ```svelte
   // BEFORE: Automatically generating WebP paths that don't exist
   $: {
     if (!srcWebp && src) {
       const extensions = ['.jpg', '.jpeg', '.png'];
       let foundExt = false;

       for (const ext of extensions) {
         if (src.toLowerCase().endsWith(ext)) {
           srcWebp = src.substring(0, src.length - ext.length) + '.webp';
           foundExt = true;
           break;
         }
       }
     }
   }

   // AFTER: Only use WebP when explicitly provided
   export let srcWebp = "";
   ```

## Challenges
1. **Large Svelte component files** - Some files have thousands of lines of code, making them difficult to edit all at once
2. **CSS selector dependencies** - Some selectors may be used in JavaScript or through dynamic classes, requiring careful verification
3. **Missing image files** - 404 errors occurred due to automatic generation of WebP paths that didn't exist