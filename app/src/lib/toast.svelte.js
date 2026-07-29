/** Shared toast state. Rune state in a .svelte.js module, imported by any
 *  component that needs to say something without prop-drilling a callback. */

export const toast = $state({ message: '', visible: false });

let timer;

/** @param {string} message */
export function say(message) {
  toast.message = message;
  toast.visible = true;
  clearTimeout(timer);
  timer = setTimeout(() => {
    toast.visible = false;
  }, 5200);
}
