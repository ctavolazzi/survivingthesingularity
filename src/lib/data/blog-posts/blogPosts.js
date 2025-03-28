/**
 * This file provides a function to load all blog posts.
 */

// Create a function to load all blog posts
export async function loadBlogPosts() {
  let posts = [];

  try {
    const whispersOfFuture = await import('./whispers-of-the-future/index.js');
    if (whispersOfFuture && whispersOfFuture.post) posts.push(whispersOfFuture.post);
  } catch (error) {
    console.error('Error importing whispers-of-the-future:', error.message);
  }

  try {
    const darpa = await import('./darpa-biomechanical-space-structures/index.js');
    if (darpa && darpa.post) posts.push(darpa.post);
  } catch (error) {
    console.error('Error importing darpa-biomechanical-space-structures:', error.message);
  }

  try {
    const farmBot = await import('./robot-farm-bot/index.js');
    if (farmBot && farmBot.post) posts.push(farmBot.post);
  } catch (error) {
    console.error('Error importing robot-farm-bot:', error.message);
  }

  try {
    const singularityExpress = await import('./singularity-express/index.js');
    if (singularityExpress && singularityExpress.post) posts.push(singularityExpress.post);
  } catch (error) {
    console.error('Error importing singularity-express:', error.message);
  }

  try {
    const farmBotDeepDive = await import('./farm-bot-deep-dive/index.js');
    if (farmBotDeepDive && farmBotDeepDive.post) posts.push(farmBotDeepDive.post);
  } catch (error) {
    console.error('Error importing farm-bot-deep-dive:', error.message);
  }

  try {
    const claudeProjects = await import('./claude-projects-weekend-project/index.js');
    if (claudeProjects && claudeProjects.post) posts.push(claudeProjects.post);
  } catch (error) {
    console.error('Error importing claude-projects-weekend-project:', error.message);
  }

  return posts;
}

// For backward compatibility, export an empty array as blogPosts
// This will be populated after loading
export const blogPosts = [];