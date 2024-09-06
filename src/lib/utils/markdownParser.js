// src/lib/utils/markdownParser.js
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkHtml from 'remark-html';
import { visit } from 'unist-util-visit';

// Custom plugin to handle our component placeholders
function customComponentPlugin() {
  return (tree) => {
    visit(tree, 'paragraph', (node) => {
      if (node.children.length === 1 && node.children[0].type === 'text') {
        const text = node.children[0].value;
        if (text === '{{NewsletterSignup}}') {
          node.type = 'html';
          node.value = '<svelte:component this={NewsletterSignup} />';
        } else if (text === '{{SkoolGroup}}') {
          node.type = 'html';
          node.value = '<svelte:component this={SkoolGroup} />';
        }
      }
    });
  };
}

export async function parseMarkdown(content) {
  const result = await unified()
    .use(remarkParse)
    .use(customComponentPlugin)
    .use(remarkHtml)
    .process(content);

  return result.toString();
}