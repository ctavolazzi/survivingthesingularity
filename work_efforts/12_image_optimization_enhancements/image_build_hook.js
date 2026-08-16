/**
 * Image Optimization Build Hook
 *
 * This script automatically generates responsive image variants
 * and WebP versions during the build process.
 *
 * It works by:
 * 1. Finding all images in the static and src/lib/images directories
 * 2. For each image, generating multiple size variants and WebP versions
 * 3. Creating a manifest file that maps original images to their optimized versions
 *
 * To use:
 * 1. Add this as a prebuild hook in package.json
 * 2. Use the ResponsiveImage component with the image paths
 */

import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import sharp from 'sharp';
import { glob } from 'glob';

// Get the directory of the current module
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '../../');

// Directories to process
const IMAGE_DIRS = [
  path.join(rootDir, 'static'),
  path.join(rootDir, 'src/lib/images')
];

// Directories to exclude
const EXCLUDE_DIRS = [
  path.join(rootDir, 'static/images/optimized'),
  // Share cards are fetched exactly once, by a scraper, at the single absolute
  // URL named in the page's og:image tag. Nothing ever requests a 400w webp of
  // one, so generating seven derivatives per card added 7.4MB of files no
  // request will ever match.
  path.join(rootDir, 'static/images/og'),
  path.join(rootDir, 'node_modules'),
  path.join(rootDir, '.svelte-kit')
];

// Output directory for optimized images
const OUTPUT_DIR = path.join(rootDir, 'static/images/optimized');

// Size variants to generate (widths in pixels)
const SIZES = [400, 800, 1200];

// Image types to process
const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png'];

// WebP encoder quality. Named because it is part of the cache key below.
const WEBP_QUALITY = 80;

// Build cache. Without it this script re-ran sharp over every source image on
// every build: 108 sources, 468 outputs, ~45s of the ~46s prebuild, all to
// reproduce bytes that were already on disk.
//
// The cache lives INSIDE the output directory and is committed alongside it,
// on purpose. The outputs are tracked in git, so a fresh clone already has
// them; shipping the cache next to them means a clean CI checkout skips too,
// instead of paying the full 45s to regenerate files git just handed it.
//
// A source is skipped only when all three hold:
//   1. its content hash matches the hash recorded last time,
//   2. the encoder config below is unchanged,
//   3. every output the cache claims for it still exists on disk.
// Any doubt regenerates. Run with --force to ignore the cache entirely.
const CACHE_FILE = path.join(OUTPUT_DIR, '.build-cache.json');
const CACHE_VERSION = 1;
const FORCE = process.argv.includes('--force');

// Changing sizes, quality or the extension list must invalidate every entry,
// so they are hashed into the key rather than compared field by field.
const CONFIG_KEY = crypto
  .createHash('sha256')
  .update(JSON.stringify({ SIZES, WEBP_QUALITY, IMAGE_EXTENSIONS }))
  .digest('hex')
  .slice(0, 16);

// Hash a file's bytes. Streaming keeps a 5MB source from being buffered whole
// just to fingerprint it.
async function hashFile(filePath) {
  const handle = await fs.open(filePath, 'r');
  try {
    const hash = crypto.createHash('sha256');
    for await (const chunk of handle.createReadStream()) hash.update(chunk);
    return hash.digest('hex');
  } finally {
    await handle.close();
  }
}

// Every file a manifest entry claims to have produced. Used to verify a cache
// hit against the disk, so a deleted output forces a regenerate.
function outputsOf(sizes) {
  const outputs = [];
  if (sizes.webp?.original) outputs.push(sizes.webp.original);
  for (const variant of Object.values(sizes.variants || {})) {
    if (variant.original) outputs.push(variant.original);
    if (variant.webp) outputs.push(variant.webp);
  }
  return outputs;
}

async function loadCache() {
  if (FORCE) return {};
  try {
    const raw = JSON.parse(await fs.readFile(CACHE_FILE, 'utf8'));
    if (raw.version !== CACHE_VERSION || raw.config !== CONFIG_KEY) return {};
    return raw.entries || {};
  } catch {
    // No cache, unreadable cache, or malformed cache all mean the same thing:
    // regenerate everything. A bad cache must never be able to fail the build.
    return {};
  }
}

// Sorted keys, so the cache file itself does not churn between builds.
async function saveCache(entries) {
  const sorted = {};
  for (const key of Object.keys(entries).sort()) sorted[key] = entries[key];
  await fs.writeFile(
    CACHE_FILE,
    JSON.stringify({ version: CACHE_VERSION, config: CONFIG_KEY, entries: sorted }, null, 2)
  );
}

async function exists(relativePath) {
  try {
    await fs.access(path.join(rootDir, relativePath));
    return true;
  } catch {
    return false;
  }
}

// Output names are derived from the source filename alone, so two sources in
// different directories can collapse onto the same output.
function outputBaseNameFor(imagePath) {
  return path.parse(imagePath).name.replace(/[^a-z0-9]/gi, '_').toLowerCase();
}

// Three copies of the cover currently collide on
// surviving_the_singularity_cover, and two copies of sts-welcome on
// sts_welcome. Today every colliding set is byte-identical so the last writer
// wins harmlessly, but the moment one copy is edited alone the output silently
// depends on walk order. Sorting makes the winner deterministic; this warning
// makes the collision visible before it costs someone an afternoon.
function warnOnNameCollisions(imagePaths) {
  const byOutputName = new Map();
  for (const imagePath of imagePaths) {
    const key = outputBaseNameFor(imagePath);
    if (!byOutputName.has(key)) byOutputName.set(key, []);
    byOutputName.get(key).push(path.relative(rootDir, imagePath));
  }

  for (const [key, sources] of byOutputName) {
    if (sources.length < 2) continue;
    const winner = sources[sources.length - 1];
    console.warn(
      `WARNING: ${sources.length} sources share the output name "${key}": ${sources.join(', ')}. ` +
      `"${winner}" wins. Rename one if they are meant to differ.`
    );
  }
}

// Check if a path should be excluded
function shouldExclude(filePath) {
  // Exclude files in the optimization output directory and other special directories
  for (const excludeDir of EXCLUDE_DIRS) {
    if (filePath.startsWith(excludeDir)) {
      return true;
    }
  }

  // Exclude files that are already optimized
  const filename = path.basename(filePath);
  if (filename.includes('_original') ||
      filename.includes('_400') ||
      filename.includes('_800') ||
      filename.includes('_1200')) {
    return true;
  }

  return false;
}

// Initialize the process
async function main() {
  try {
    console.log('Starting image optimization build hook...');

    // Create output directory if it doesn't exist
    await fs.mkdir(OUTPUT_DIR, { recursive: true });

    // Find all images
    const imagePaths = [];
    for (const dir of IMAGE_DIRS) {
      for (const ext of IMAGE_EXTENSIONS) {
        try {
          const matches = await glob(`${dir}/**/*${ext}`);

          // Filter out optimized images and excluded directories
          const filteredMatches = matches.filter(filePath => !shouldExclude(filePath));
          imagePaths.push(...filteredMatches);
        } catch (error) {
          console.error(`Error finding images with extension ${ext} in ${dir}: ${error.message}`);
        }
      }
    }

    // glob does not promise a stable order, so an unsorted walk reshuffled the
    // manifest's keys on every build and left manifest.json permanently dirty
    // in git. Sorting also fixes which source wins a name collision (below).
    imagePaths.sort();

    console.log(`Found ${imagePaths.length} images to optimize`);

    warnOnNameCollisions(imagePaths);

    const cache = await loadCache();
    const nextCache = {};
    let skipped = 0;

    // Process each image
    const manifest = {};
    for (const imagePath of imagePaths) {
      const relativePath = path.relative(rootDir, imagePath);
      try {
        const hash = await hashFile(imagePath);
        const cached = cache[relativePath];

        if (cached && cached.hash === hash && cached.sizes) {
          const present = await Promise.all(outputsOf(cached.sizes).map(exists));
          if (present.every(Boolean)) {
            manifest[relativePath] = cached.sizes;
            nextCache[relativePath] = cached;
            skipped++;
            continue;
          }
        }

        const { sizes } = await processImage(imagePath);
        manifest[relativePath] = sizes;
        // A skipped image is only cached if it actually produced outputs.
        if (!sizes.skipped) nextCache[relativePath] = { hash, sizes };
      } catch (error) {
        console.error(`Failed to process image ${imagePath}: ${error.message}`);
        // Continue with next image
      }
    }

    // Write manifest file
    await fs.writeFile(
      path.join(OUTPUT_DIR, 'manifest.json'),
      JSON.stringify(manifest, null, 2)
    );

    await saveCache(nextCache);

    console.log(
      `Image optimization complete! ${skipped} unchanged, ${imagePaths.length - skipped} regenerated.`
    );
  } catch (error) {
    console.error('Error in image optimization:', error);
    process.exit(1);
  }
}

// Process a single image
async function processImage(imagePath) {
  try {
    const relativePath = path.relative(rootDir, imagePath);
    console.log(`Processing: ${relativePath}`);

    const parsedPath = path.parse(imagePath);
    const outputBaseName = outputBaseNameFor(imagePath);

    // Load the image with sharp
    const image = sharp(imagePath);
    const metadata = await image.metadata();

    // Create size variants in both original format and WebP
    const sizes = {
      original: {
        width: metadata.width,
        height: metadata.height,
        path: relativePath
      },
      webp: {},
      variants: {}
    };

    // Generate WebP version at original size.
    // Every output below works on image.clone(): sharp operations mutate the
    // instance, so e.g. .webp() here would otherwise stick and make every
    // later "original format" variant silently WebP-encoded inside a
    // .png/.jpg-named file.
    const webpOutputPath = path.join(OUTPUT_DIR, `${outputBaseName}_original.webp`);
    await image.clone().webp({ quality: WEBP_QUALITY }).toFile(webpOutputPath);
    sizes.webp.original = path.relative(rootDir, webpOutputPath);

    // Generate variants for different sizes
    for (const width of SIZES) {
      // Skip if requested width is larger than original
      if (width > metadata.width) continue;

      // Original format variant
      const outputPathOriginal = path.join(OUTPUT_DIR, `${outputBaseName}_${width}${parsedPath.ext}`);
      await image.clone().resize(width).toFile(outputPathOriginal);

      // WebP variant
      const outputPathWebP = path.join(OUTPUT_DIR, `${outputBaseName}_${width}.webp`);
      await image.clone().resize(width).webp({ quality: WEBP_QUALITY }).toFile(outputPathWebP);

      // Add to manifest
      if (!sizes.variants[width]) {
        sizes.variants[width] = {};
      }
      sizes.variants[width].original = path.relative(rootDir, outputPathOriginal);
      sizes.variants[width].webp = path.relative(rootDir, outputPathWebP);
    }

    return { relativePath, sizes };
  } catch (error) {
    console.error(`Error processing image ${imagePath}: ${error.message}`);
    // Return a minimal object that won't break the manifest
    return {
      relativePath: path.relative(rootDir, imagePath),
      sizes: {
        original: { path: path.relative(rootDir, imagePath) },
        skipped: true
      }
    };
  }
}

// Run the main function
main();