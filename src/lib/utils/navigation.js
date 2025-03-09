import { goto as svelteGoto } from '$app/navigation';

/**
 * Safely navigate to a path, ensuring the path is a valid string
 * @param {string|any} path - The path to navigate to
 * @param {Object} options - Options to pass to the goto function
 * @returns {Promise<void>} A promise that resolves when navigation is complete
 */
export function safeGoto(path, options = {}) {
  // Ensure path is a string, default to home if not
  const safePath = typeof path === 'string' ? path : '/';

  // Log a warning in development if an invalid path is passed
  if (typeof path !== 'string') {
    console.warn('Invalid navigation path detected:', path, 'Navigating to home instead.');
  }

  return svelteGoto(safePath, options);
}

/**
 * Navigate to a path with a callback when navigation is complete
 * @param {string|any} path - The path to navigate to
 * @param {Function} callback - Callback to execute after navigation
 * @param {Object} options - Options to pass to the goto function
 * @returns {Promise<void>} A promise that resolves when navigation and callback are complete
 */
export function gotoWithCallback(path, callback, options = {}) {
  return safeGoto(path, options).then(() => {
    if (typeof callback === 'function') {
      callback();
    }
  });
}

/**
 * Navigate to a path and scroll to top
 * @param {string|any} path - The path to navigate to
 * @param {Object} options - Options to pass to the goto function
 * @returns {Promise<void>} A promise that resolves when navigation and scrolling are complete
 */
export function gotoAndScrollTop(path, options = {}) {
  return gotoWithCallback(path, () => window.scrollTo(0, 0), options);
}