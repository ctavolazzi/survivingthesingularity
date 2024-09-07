import { newsletters } from '$lib/newsletters';

export async function GET({ url }) {
  const filename = url.searchParams.get('filename');
  if (!filename) {
    return new Response('Filename is required', { status: 400 });
  }

  try {
    const content = await newsletters[filename]();
    return new Response(content);
  } catch (error) {
    console.error('Error reading newsletter:', error);
    return new Response('Unable to read newsletter', { status: 500 });
  }
}