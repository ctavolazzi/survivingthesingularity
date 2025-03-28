<script>
  import BlogPostTemplate from '$lib/components/BlogPostTemplate.svelte';

  const post = {
    title: 'Using the Enhanced Blog Post Template',
    date: '2025-03-20',
    author: 'Christopher Tavolazzi',
    image: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=2070',
    readingTime: '5 min read',
    description: 'Learn how to use our enhanced blog post template to create beautiful, consistent posts with minimal effort.',
    audioSrc: '',
    audioTitle: ''
  };

  // Custom options for this specific blog post
  const options = {
    showBackButton: true,
    showProgressBar: true,
    showAds: true,
    showAuthorBio: true,
    showShareBottom: true,
    showMysteryBox: false,
    showTreasureTavern: true,
    fadeInContent: true,
    borderOnFeaturedImage: true
  };

  // Custom recommended videos for this post
  const recommendedVideos = [
    {
      id: "PNqwvJCz_2w",
      title: "Game Over? Voice Actors vs AI"
    },
    {
      id: "U1tQbD25dGY",
      title: "Futurist: How AI and Robotics Will Reshape Our Economy"
    },
    {
      id: "YLo7EH2zsW0",
      title: "AI Plays Minecraft: Voyager - An Open-Ended Embodied Agent with Large Language Models"
    }
  ];
</script>

<style>
  .featured-image-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 0.5rem;
    background-color: rgba(15, 23, 42, 0.05);
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .featured-image-container img {
    width: 100%;
    height: auto;
    object-fit: cover;
    max-height: 80vh;
    border-radius: 0.5rem;
    transform: scale(1);
    transition: transform 0.5s ease;
  }

  .featured-image-container img:hover {
    transform: scale(1.05);
  }
</style>

<BlogPostTemplate {post} {options} {recommendedVideos}>
  <h2>Getting Started with the Blog Template</h2>
  <p>
    Welcome to our enhanced blog template! This template makes it easy to create consistent,
    professional-looking blog posts without having to rewrite the same boilerplate code each time.
  </p>

  <p>
    The template handles all the common elements like headers, social sharing, and layout,
    while giving you complete control over the content.
  </p>

  <h2>Key Features</h2>
  <ul>
    <li><strong>Flexible Configuration:</strong> Customize the appearance and features through the options object</li>
    <li><strong>Social Sharing:</strong> Built-in sharing capabilities for all major platforms</li>
    <li><strong>Responsive Design:</strong> Looks great on all devices, from mobile to desktop</li>
    <li><strong>SEO Optimized:</strong> Includes all necessary meta tags and structured data</li>
    <li><strong>Reading Progress:</strong> Optional reading progress bar to enhance user experience</li>
    <li><strong>Audio Support:</strong> Optional audio player for podcast-style content</li>
  </ul>

  <h2>How to Use</h2>
  <p>
    Using the template is simple. Just import the BlogPostTemplate component, define your post object
    with all the necessary metadata, and then place your content between the component tags.
  </p>

  <p>The basic structure involves:</p>
  <ul>
    <li>Importing the template component</li>
    <li>Defining your post metadata (title, date, image, etc.)</li>
    <li>Setting any custom options</li>
    <li>Writing your content inside the template tags</li>
  </ul>

  <h2>Customization Options</h2>
  <p>
    The template provides several customization options through the <code>options</code> object:
  </p>

  <table class="w-full border-collapse my-4">
    <thead>
      <tr class="bg-gray-100 dark:bg-gray-800">
        <th class="p-2 text-left">Option</th>
        <th class="p-2 text-left">Description</th>
        <th class="p-2 text-left">Default</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>showBackButton</code></td>
        <td class="p-2">Display a back button at the top and bottom</td>
        <td class="p-2"><code>true</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>showProgressBar</code></td>
        <td class="p-2">Show a reading progress bar at the top</td>
        <td class="p-2"><code>false</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>showAds</code></td>
        <td class="p-2">Display ads at the bottom of the post</td>
        <td class="p-2"><code>true</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>showAuthorBio</code></td>
        <td class="p-2">Show the author bio section</td>
        <td class="p-2"><code>true</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>showShareBottom</code></td>
        <td class="p-2">Display sharing buttons at the bottom</td>
        <td class="p-2"><code>true</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>showMysteryBox</code></td>
        <td class="p-2">Show the Mystery Box ad</td>
        <td class="p-2"><code>false</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>showTreasureTavern</code></td>
        <td class="p-2">Show the Treasure Tavern ad</td>
        <td class="p-2"><code>true</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>fadeInContent</code></td>
        <td class="p-2">Fade in the content when the page loads</td>
        <td class="p-2"><code>true</code></td>
      </tr>
      <tr class="border-t border-gray-200 dark:border-gray-700">
        <td class="p-2"><code>borderOnFeaturedImage</code></td>
        <td class="p-2">Add a shadow border to the featured image</td>
        <td class="p-2"><code>false</code></td>
      </tr>
    </tbody>
  </table>

  <h2>Styling Content</h2>
  <p>
    The template provides global styles for common HTML elements within the content area.
    You don't need to add additional styling for basic elements like headings, paragraphs,
    lists, and blockquotes.
  </p>

  <h3>Example Blockquote</h3>
  <blockquote>
    This template makes creating blog posts so much easier. I can focus on the content
    while the template handles all the layout and styling for me!
  </blockquote>

  <h2>Advanced Features</h2>
  <p>
    For more advanced blog posts, you can include custom components within the content area.
    The template will seamlessly integrate them into the layout.
  </p>

  <p>
    We hope you enjoy using this template to create beautiful blog posts for Surviving the Singularity!
  </p>
</BlogPostTemplate>