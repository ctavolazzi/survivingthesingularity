// Empty polyfill for path module in Cloudflare Workers
export default {
  join: (...args) => args.join('/'),
  dirname: (path) => path.split('/').slice(0, -1).join('/'),
  resolve: (...args) => args.join('/')
};

// Export individual functions for named imports
export const join = (...args) => args.join('/');
export const dirname = (path) => path.split('/').slice(0, -1).join('/');
export const resolve = (...args) => args.join('/');