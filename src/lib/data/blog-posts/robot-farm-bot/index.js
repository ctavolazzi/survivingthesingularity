import content from './content.md?raw';
import { marked } from 'marked';

// Parse the content to HTML
const html = marked(content);

export const post = {
  title: "Robot Farm Bot: The Future of Residential Agriculture",
  date: "2024-08-15",
  author: "Christopher Tavolazzi",
  imageUrl: "https://farm.bot/cdn/shop/files/FarmBot_Genesis_v1-3_c10ecd67-00ed-4ae1-a32e-111f11312655_2049x1365.jpg?v=1697756943", // Replace with actual image URL
  content,
  html, // Add the parsed HTML content
  excerpt: "Imagine a world where your backyard vegetable garden is tended by an AI-powered robot, ensuring a bountiful harvest with minimal effort. Welcome to the era of the Robot Farm Bot.",
  slug: "robot-farm-bot"
};