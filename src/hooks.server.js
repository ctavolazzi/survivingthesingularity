// Minimal browser API polyfill
globalThis.location = { pathname: '/' };

// Required hook export
export function handle({ event, resolve }) {
  return resolve(event);
}
