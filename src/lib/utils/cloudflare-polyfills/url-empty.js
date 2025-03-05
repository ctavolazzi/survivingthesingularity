// Empty polyfill for url module in Cloudflare Workers
export default {
  fileURLToPath: (url) => url.replace('file://', '')
};

// Export individual functions for named imports
export const fileURLToPath = (url) => url.replace('file://', '');