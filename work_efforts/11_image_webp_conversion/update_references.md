# Image Reference Update Guide

## Overview
After converting images to WebP format, we need to update references in the codebase to use the new WebP versions while providing appropriate fallbacks for browsers that don't support WebP.

## Local Image References
For local images referenced in HTML/Svelte files, replace direct image references with the following pattern:

```html
<!-- Before -->
<img src="/path/to/image.png" alt="Description">

<!-- After -->
<picture>
  <source srcset="/path/to/image.webp" type="image/webp">
  <img src="/path/to/image.png" alt="Description">
</picture>
```

## CSS Background Images
For CSS background images, use the following approach:

```css
/* Before */
.element {
  background-image: url('/path/to/image.png');
}

/* After */
.element {
  background-image: url('/path/to/image.png');
}

.webp .element {
  background-image: url('/path/to/image.webp');
}
```

Add a JavaScript snippet in the app's initialization to detect WebP support and add a 'webp' class to the HTML element:

```javascript
// WebP detection
(function() {
  const testWebP = (callback) => {
    const webP = new Image();
    webP.onload = webP.onerror = function () {
      callback(webP.height === 2);
    };
    webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
  };

  testWebP((support) => {
    if (support) {
      document.documentElement.classList.add('webp');
    }
  });
})();
```

## External Images and CDN References
For the blog post images from external URLs, we have several options:

1. Leave as is (these images are controlled by external services)
2. Download the images, convert them, and host them locally
3. Use image optimization services that can serve WebP automatically

## Converted Images
The following images have been successfully converted to WebP:

1. static/favicon-16x16.png → static/favicon-16x16.webp
2. static/android-chrome-192x192.png → static/android-chrome-192x192.webp
3. static/sts-welcome.png → static/sts-welcome.webp
4. static/img-missing.png → static/img-missing.webp
5. static/favicon.png → static/favicon.webp
6. static/sts-header_1000.png → static/sts-header_1000.webp
7. static/favicon-32x32.png → static/favicon-32x32.webp
8. static/images/treasure-tavern-logo-transparent.png → static/images/treasure-tavern-logo-transparent.webp
9. static/images/treasure-tavern-banner-600x800.png → static/images/treasure-tavern-banner-600x800.webp
10. static/images/treasure-tavern-square.png → static/images/treasure-tavern-square.webp

## Issues Encountered
The following files could not be converted:

1. static/images/default-avatar.jpg - Appears to be corrupted or not a valid image
2. static/images/blog/*.jpg - These are 0-byte files, indicating they are placeholder files
3. static/future-projections/future-of-jobs.png - Also a 0-byte file

## Next Steps
1. Add WebP detection script to the main app file
2. Update image references for successfully converted images
3. Consider downloading and hosting blog images locally for better optimization