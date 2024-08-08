<!-- src/routes/blog/+page.svelte -->
<script>
  const posts = [
    {
      id: 1,
      title: "The Singularity Express Arrives at the Station",
      date: "2024-08-08",
      excerpt: "Choo Choo, Motherfuckers. The Singularity Express just pulled into the station, and it's one hell of a ride."
    },
    // Add more posts here as needed
  ];
</script>

<div class="container mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-8">Blog Posts</h1>

  <ul class="space-y-8">
    {#each posts as post}
      <li class="border-b border-gray-200 pb-8">
        <h2 class="text-2xl font-semibold mb-2">
          <a href="/blog/post{post.id}" class="text-black hover:text-gray-600 transition-colors duration-300">{post.title}</a>
        </h2>
        <p class="text-gray-600 text-sm mb-4">{post.date}</p>
        <p class="text-gray-800 mb-4">{post.excerpt}</p>
        <a href="/blog/post{post.id}" class="text-black hover:text-gray-600 transition-colors duration-300 font-semibold">Read more →</a>
      </li>
    {/each}
  </ul>
</div>

<style>
  :global(body) {
    background-color: #ffffff;
    color: #000000;
  }

  .container {
    max-width: 800px;
  }

  h1 {
    border-bottom: 2px solid #000000;
    padding-bottom: 0.5rem;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  @media (max-width: 640px) {
    h1 {
      font-size: 1.875rem;
    }
    h2 {
      font-size: 1.5rem;
    }
  }
</style>