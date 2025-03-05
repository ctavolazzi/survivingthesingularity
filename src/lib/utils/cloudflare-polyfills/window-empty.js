// Empty polyfill for browser's window object
export default {
  fetch: async () => {
    // Return minimal fetch implementation
    return new Response();
  }
};

// For direct imports
export const fetch = async () => {
  return new Response();
};

// Also provide global.window if needed
if (typeof global !== 'undefined') {
  global.window = global.window || {
    fetch: async () => new Response()
  };
}