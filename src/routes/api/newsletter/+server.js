import { readFile } from 'fs/promises';
import { join } from 'path';

export async function GET({ url }) {
  const filename = url.searchParams.get('filename');
  if (!filename) {
    return new Response('Filename is required', { status: 400 });
  }

  const newsletterPath = join(process.cwd(), 'src', 'lib', 'data', 'newsletters', filename);

  try {
    const content = await readFile(newsletterPath, 'utf-8');
    return new Response(content);
  } catch (error) {
    console.error('Error reading newsletter:', error);
    return new Response('Unable to read newsletter', { status: 500 });
  }
}