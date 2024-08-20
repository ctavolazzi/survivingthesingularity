import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined' && window.localStorage;

const createNewsletterStore = () => {
  const { subscribe, set } = writable(false);

  if (isBrowser) {
    const storedValue = localStorage.getItem('newsletterSubmitted') === 'true';
    set(storedValue);
  }

  return {
    subscribe,
    setSubmitted: () => {
      if (isBrowser) {
        localStorage.setItem('newsletterSubmitted', 'true');
      }
      set(true);
    },
    reset: () => {
      if (isBrowser) {
        localStorage.removeItem('newsletterSubmitted');
      }
      set(false);
    }
  };
};

export const newsletterSubmitted = createNewsletterStore();