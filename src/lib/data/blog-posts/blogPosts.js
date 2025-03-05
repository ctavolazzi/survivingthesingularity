/**
 * This file imports all blog posts and exports them as an array.
 */

// Import posts with try/catch to handle any missing files
let darpa_biomechanical_space_structures, robot_farm_bot, singularity_express;
let farm_bot_deep_dive, claude_projects_weekend_project;

try {
  // Use dynamic imports with relative paths
  darpa_biomechanical_space_structures = (await import('./darpa-biomechanical-space-structures/index.js')).post;
} catch (error) {
  console.error('Error importing darpa-biomechanical-space-structures:', error.message);
  darpa_biomechanical_space_structures = null;
}

try {
  robot_farm_bot = (await import('./robot-farm-bot/index.js')).post;
} catch (error) {
  console.error('Error importing robot-farm-bot:', error.message);
  robot_farm_bot = null;
}

try {
  singularity_express = (await import('./singularity-express/index.js')).post;
} catch (error) {
  console.error('Error importing singularity-express:', error.message);
  singularity_express = null;
}

try {
  farm_bot_deep_dive = (await import('./farm-bot-deep-dive/index.js')).post;
} catch (error) {
  console.error('Error importing farm-bot-deep-dive:', error.message);
  farm_bot_deep_dive = null;
}

try {
  claude_projects_weekend_project = (await import('./claude-projects-weekend-project/index.js')).post;
} catch (error) {
  console.error('Error importing claude-projects-weekend-project:', error.message);
  claude_projects_weekend_project = null;
}

// Filter out any null posts
export const blogPosts = [
  darpa_biomechanical_space_structures,
  robot_farm_bot,
  singularity_express,
  farm_bot_deep_dive,
  claude_projects_weekend_project
].filter(post => post !== null);