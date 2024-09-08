import { json } from '@sveltejs/kit';

export async function GET({ url }) {
  const targetUrl = url.searchParams.get('url');
  
  if (!targetUrl) {
    return json({ error: 'URL parameter is required' }, { status: 400 });
  }

  try {
    const response = await fetch(targetUrl);
    const html = await response.text();
    const title = html.match(/<title>(.*?)<\/title>/i)?.[1] || 'No title found';
    
    return json({ title });
  } catch (error) {
    console.error('Error fetching title:', error);
    return json({ error: 'Failed to fetch title' }, { status: 500 });
  }
}