// Minimal browser API polyfill
globalThis.location = { pathname: '/' };

// Required hook export
export function handle({ event, resolve }) {
  // Fix for "[object Object]" navigation errors
  // Check if the URL path includes "[object Object]" which indicates a navigation error
  if (event.url.pathname.includes('[object%20Object]') || event.url.pathname.includes('[object Object]')) {
    // Redirect to home page if an object was incorrectly passed to navigation
    return new Response('Redirect', {
      status: 302,
      headers: { Location: '/' }
    });
  }

  return resolve(event);
}
