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

// Output directory for optimized images
const OUTPUT_DIR = path.join(rootDir, 'static/images/optimized');

// Size variants to generate (widths in pixels)
const SIZES = [400, 800, 1200];

// Image types to process
const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png'];

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
        const matches = await glob(`${dir}/**/*${ext}`);
        imagePaths.push(...matches);
      }
    }

    console.log(`Found ${imagePaths.length} images to optimize`);

    // Process each image
    const manifest = {};
    for (const imagePath of imagePaths) {
      const { relativePath, sizes } = await processImage(imagePath);
      manifest[relativePath] = sizes;
    }

    // Write manifest file
    await fs.writeFile(
      path.join(OUTPUT_DIR, 'manifest.json'),
      JSON.stringify(manifest, null, 2)
    );

    console.log('Image optimization complete!');
  } catch (error) {
    console.error('Error in image optimization:', error);
    process.exit(1);
  }
}

// Process a single image
async function processImage(imagePath) {
  const relativePath = path.relative(rootDir, imagePath);
  console.log(`Processing: ${relativePath}`);

  const parsedPath = path.parse(imagePath);
  const fileName = parsedPath.name;
  const outputBaseName = fileName.replace(/[^a-z0-9]/gi, '_').toLowerCase();

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

  // Generate WebP version at original size
  const webpOutputPath = path.join(OUTPUT_DIR, `${outputBaseName}_original.webp`);
  await image.webp({ quality: 80 }).toFile(webpOutputPath);
  sizes.webp.original = path.relative(rootDir, webpOutputPath);

  // Generate variants for different sizes
  for (const width of SIZES) {
    // Skip if requested width is larger than original
    if (width > metadata.width) continue;

    const resized = image.resize(width);

    // Original format variant
    const outputPathOriginal = path.join(OUTPUT_DIR, `${outputBaseName}_${width}${parsedPath.ext}`);
    await resized.toFile(outputPathOriginal);

    // WebP variant
    const outputPathWebP = path.join(OUTPUT_DIR, `${outputBaseName}_${width}.webp`);
    await resized.webp({ quality: 80 }).toFile(outputPathWebP);

    // Add to manifest
    if (!sizes.variants[width]) {
      sizes.variants[width] = {};
    }
    sizes.variants[width].original = path.relative(rootDir, outputPathOriginal);
    sizes.variants[width].webp = path.relative(rootDir, outputPathWebP);
  }

  return { relativePath, sizes };
}

// Run the main function
main();