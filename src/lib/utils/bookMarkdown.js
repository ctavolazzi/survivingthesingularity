import { marked } from 'marked';
import { katexExtension } from './katexExtension.js';

// One configured markdown entry point for the book renderer.
//
// `marked.use()` mutates the shared marked instance, so it has to run exactly
// once. Doing it here, as a module side effect, guarantees that: ES modules
// evaluate once per process no matter how many components import them. Calling
// `marked.use(katexExtension)` from a component's instance script would stack a
// fresh copy of both tokenizers on every mount, and the book route's component
// is reused across chapter navigations.
marked.use(katexExtension);

export function renderMarkdown(source) {
  return marked(source);
}
