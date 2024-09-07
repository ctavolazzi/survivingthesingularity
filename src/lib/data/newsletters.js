const newsletterFiles = import.meta.glob('/src/lib/data/newsletters/*.md', { as: 'raw' });

export const newsletters = Object.fromEntries(
  Object.entries(newsletterFiles).map(([path, loader]) => [
    path.split('/').pop().replace('.md', ''),
    loader
  ])
);