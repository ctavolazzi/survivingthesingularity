---
title: "Image WebP Conversion"
status: "completed"
priority: "medium"
assignee: "development team"
created: "2024-03-09"
last_updated: "2024-03-09"
tags: [performance, images, optimization]
---

# Image WebP Conversion

## 🚩 Objectives
- Convert appropriate images in the project to WebP format
- Improve page load times and performance
- Maintain image quality while reducing file sizes
- Ensure browser compatibility with appropriate fallbacks

## 🛠 Tasks
- [x] Identify all local images that can be converted to WebP
- [x] Research if external image URLs can be optimized (or need to be downloaded and hosted locally)
- [x] Install necessary tools for WebP conversion
- [x] Convert PNG and JPG images to WebP format
- [x] Update image references in the codebase
- [x] Implement fallbacks for browsers that don't support WebP
- [x] Test the website after conversion to ensure all images display correctly

## 📝 Notes
WebP is a modern image format that offers superior compression and quality compared to traditional formats like JPEG and PNG. Benefits include:

1. Better compression: WebP images are typically 25-34% smaller than PNGs and JPEGs
2. Support for transparency like PNG
3. Faster page load times and reduced bandwidth usage
4. Wide browser support (all modern browsers support WebP)

Results from our conversion:
- Successfully converted 10 PNG images to WebP format in the static directory
- Additionally converted 7 more images in the src/lib/images directory
- Achieved significant file size reductions:
  - sts-welcome.png: 1.1MB → 120KB (89% reduction)
  - img-missing.png: 1.8MB → 184KB (90% reduction)
  - treasure-tavern-logo-transparent.png: 436KB → 112KB (74% reduction)
  - treasure-tavern-banner-600x800.png: 836KB → 72KB (91% reduction)
  - treasure-tavern-square.png: 508KB → 52KB (90% reduction)
  - sts-header_1000.png: 56KB → 20KB (64% reduction)
  - android-chrome-192x192.png: 8.0KB → 4.0KB (50% reduction)
  - favicon.png: 8.0KB → 4.0KB (50% reduction)
  - favicon-16x16.png and favicon-32x32.png: minimal size reduction
  - Surviving-the-Singularity-Cover.png: 420KB → 212KB (50% reduction)
  - sts-chess.jpg: 52KB → 32KB (38% reduction)
  - default-blog-image.png: 36KB → 8KB (78% reduction)
  - StSFreeGuide.png: 280KB → 56KB (80% reduction)

## 🐞 Issues Encountered
- Several image files were 0-byte placeholders and couldn't be converted (e.g., blog image files)
- Blog post images are all externally hosted, so we couldn't convert those
- The default-avatar.jpg file appears to be corrupted or invalid
- Including both PNG and WebP versions increases the total size initially, but with proper caching and browser compatibility handling, only the appropriate version should be downloaded
- Path issues: Initial implementation incorrectly used "/static/" prefix for WebP images, which was fixed during the review

## ✅ Outcomes & Results
- Implemented WebP detection script in app.html to add a 'webp' class to the HTML element when WebP is supported
- Added WebP versions of favicons with appropriate fallbacks
- Updated site.webmanifest to include WebP icon references
- Added WebP background images with CSS fallbacks for browsers that don't support WebP
- Updated components to use `<picture>` elements with WebP sources and PNG/JPG fallbacks:
  - BookCallout component now uses WebP format with fallback
- Updated conditional references to use WebP versions first:
  - ProjectionCard component now refers to WebP version of the fallback image
- Total reduction in image size for supported browsers: approximately 4MB
- Better performance and faster load times, especially for users on slower connections

## 📅 Timeline & Progress
- **Started**: 2024-03-09
- **Completed**: 2024-03-09
- **Additional Improvements**: 2024-03-09