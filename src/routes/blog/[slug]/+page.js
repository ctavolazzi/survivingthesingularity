/** @type {import('./$types').PageLoad} */
export async function load({ params, data }) {
  const { slug } = params;

  try {
    // First try to load as MDsveX post
    const post = await import(`../posts/${slug}.md`);
    return {
      ...data,
      Content: post.default
    };
  } catch (error) {
    // If not found as MDsveX post, return the existing data
    return data;
  }
}