import { parseMarkdown } from '../src/lib/utils/markdownParser';

describe('parseMarkdown', () => {
  test('extracts title and date correctly', async () => {
    const content = `
# Test Newsletter
## Subtitle
### July 1, 2023
Content here...
    `;
    const { metadata } = await parseMarkdown(content);
    expect(metadata.title).toBe('Test Newsletter');
    expect(metadata.date).toBe('July 1, 2023');
  });

  test('generates table of contents correctly', async () => {
    const content = `
# Main Title
## Section 1
### Subsection 1.1
## Section 2
Content here...
    `;
    const { toc } = await parseMarkdown(content);
    expect(toc).toHaveLength(3);
    expect(toc[0].text).toBe('Section 1');
    expect(toc[1].text).toBe('Subsection 1.1');
    expect(toc[2].text).toBe('Section 2');
  });

  test('handles custom components correctly', async () => {
    const content = `
# Test Newsletter
{{NewsletterSignup}}
{{SkoolGroup}}
    `;
    const { htmlContent } = await parseMarkdown(content);
    expect(htmlContent).toContain('<svelte:component this={NewsletterSignup}');
    expect(htmlContent).toContain('<svelte:component this={SkoolGroup}');
  });
});