#!/usr/bin/env node
/**
 * Script to migrate blog posts from the old format to the new format
 * Run with: node scripts/migrate-blog-posts.js
 */

import { migrateOldPosts } from '../src/lib/utils/migrate-posts.js';

console.log('Starting blog post migration...');
migrateOldPosts();
console.log('Blog post migration complete!');