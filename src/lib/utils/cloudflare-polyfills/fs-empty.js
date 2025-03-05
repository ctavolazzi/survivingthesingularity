// Empty polyfill for fs module in Cloudflare Workers
export default {
  existsSync: () => false,
  readFileSync: () => '',
  readdirSync: () => []
};

// Export individual functions for named imports
export const existsSync = () => false;
export const readFileSync = () => '';
export const readdirSync = () => [];