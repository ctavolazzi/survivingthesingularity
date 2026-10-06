import BookFigure from './BookFigure.svelte';
import { sceneIds } from '$lib/bookScenes/catalog.js';

// A comment marker enhances its adjacent ordinary Markdown image/caption.
// The same source remains a complete figure in EPUB, PDF, and without JS.
export const interactiveRegistry = Object.fromEntries(sceneIds.map(id => [id, BookFigure]));
