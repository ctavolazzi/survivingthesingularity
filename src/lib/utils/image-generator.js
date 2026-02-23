/**
 * Image Generator Utility
 *
 * Generates branded placeholder images using Canvas API.
 * Variable aspect ratios, text overlays, STS brand styling.
 *
 * Usage:
 *   import { generateImage, generateMeme } from '$lib/utils/image-generator.js';
 *
 *   const dataUrl = generateImage({
 *     width: 1200,
 *     height: 630,
 *     title: 'The Shouse Blueprint',
 *     subtitle: 'Build for $8K what costs $500K',
 *     style: 'dark'
 *   });
 *
 *   // Or generate a meme
 *   const memeUrl = generateMeme({
 *     topText: 'BANKS: "Here\'s a 30-year mortgage"',
 *     bottomText: 'ME: *builds shouse for $8K*',
 *     aspect: '1:1'
 *   });
 */

const BRAND = {
  bg: '#020617',
  bgAlt: '#0f172a',
  accent: '#f59e0b',
  accentAlt: '#f97316',
  text: '#f1f5f9',
  textMuted: '#94a3b8',
  textDim: '#475569',
  grid: 'rgba(245, 158, 11, 0.03)',
  font: "'Inter', 'SF Pro Display', system-ui, sans-serif",
  monoFont: "'JetBrains Mono', 'SF Mono', monospace",
};

const ASPECTS = {
  '16:9': { width: 1280, height: 720 },
  '4:3': { width: 1024, height: 768 },
  '1:1': { width: 1080, height: 1080 },
  '3:2': { width: 1200, height: 800 },
  '21:9': { width: 2560, height: 1080 },
  'og': { width: 1200, height: 630 },       // Open Graph
  'twitter': { width: 1200, height: 600 },   // Twitter card
  'story': { width: 1080, height: 1920 },    // Instagram story
};

/**
 * Generate a branded placeholder/hero image
 */
export function generateImage({
  width = 1200,
  height = 630,
  title = '',
  subtitle = '',
  badge = '',
  style = 'dark',
  aspect = null
} = {}) {
  if (aspect && ASPECTS[aspect]) {
    width = ASPECTS[aspect].width;
    height = ASPECTS[aspect].height;
  }

  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');

  // Background
  ctx.fillStyle = BRAND.bg;
  ctx.fillRect(0, 0, width, height);

  // Grid pattern
  ctx.strokeStyle = BRAND.grid;
  ctx.lineWidth = 1;
  const gridSize = 60;
  for (let x = 0; x < width; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }
  for (let y = 0; y < height; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }

  // Radial glow
  const glow = ctx.createRadialGradient(width / 2, height / 2, 0, width / 2, height / 2, width * 0.6);
  glow.addColorStop(0, 'rgba(245, 158, 11, 0.06)');
  glow.addColorStop(1, 'transparent');
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, width, height);

  // Badge
  if (badge) {
    ctx.font = `700 ${Math.floor(width * 0.012)}px ${BRAND.monoFont}`;
    ctx.fillStyle = BRAND.accent;
    ctx.letterSpacing = '2px';
    ctx.textAlign = 'center';
    ctx.fillText(badge.toUpperCase(), width / 2, height * 0.35);
  }

  // Title
  if (title) {
    const titleSize = Math.floor(width * 0.045);
    ctx.font = `900 ${titleSize}px ${BRAND.font}`;
    ctx.fillStyle = BRAND.text;
    ctx.textAlign = 'center';

    // Word wrap
    const words = title.split(' ');
    const lines = [];
    let currentLine = '';
    const maxWidth = width * 0.75;

    for (const word of words) {
      const testLine = currentLine ? `${currentLine} ${word}` : word;
      const metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth && currentLine) {
        lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = testLine;
      }
    }
    if (currentLine) lines.push(currentLine);

    const lineHeight = titleSize * 1.2;
    const startY = (height / 2) - ((lines.length - 1) * lineHeight / 2);

    lines.forEach((line, i) => {
      ctx.fillText(line, width / 2, startY + i * lineHeight);
    });
  }

  // Subtitle
  if (subtitle) {
    const subSize = Math.floor(width * 0.018);
    ctx.font = `500 ${subSize}px ${BRAND.font}`;
    ctx.fillStyle = BRAND.textMuted;
    ctx.textAlign = 'center';
    ctx.fillText(subtitle, width / 2, height * 0.68);
  }

  // Bottom brand bar
  ctx.fillStyle = BRAND.accent;
  ctx.fillRect(width * 0.4, height * 0.82, width * 0.2, 2);

  ctx.font = `700 ${Math.floor(width * 0.01)}px ${BRAND.monoFont}`;
  ctx.fillStyle = BRAND.textDim;
  ctx.textAlign = 'center';
  ctx.fillText('SURVIVING THE SINGULARITY', width / 2, height * 0.88);

  return canvas.toDataURL('image/png');
}

/**
 * Generate a meme-style image
 */
export function generateMeme({
  topText = '',
  bottomText = '',
  aspect = '1:1',
  style = 'impact'
} = {}) {
  const dims = ASPECTS[aspect] || ASPECTS['1:1'];
  const canvas = document.createElement('canvas');
  canvas.width = dims.width;
  canvas.height = dims.height;
  const ctx = canvas.getContext('2d');
  const { width, height } = dims;

  // Dark background
  ctx.fillStyle = BRAND.bg;
  ctx.fillRect(0, 0, width, height);

  // Subtle grid
  ctx.strokeStyle = 'rgba(245, 158, 11, 0.02)';
  ctx.lineWidth = 1;
  for (let x = 0; x < width; x += 40) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
  }
  for (let y = 0; y < height; y += 40) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
  }

  const fontSize = Math.floor(width * 0.05);

  // Top text
  if (topText) {
    ctx.font = `900 ${fontSize}px ${BRAND.font}`;
    ctx.fillStyle = BRAND.text;
    ctx.textAlign = 'center';
    ctx.strokeStyle = 'rgba(0,0,0,0.8)';
    ctx.lineWidth = 3;

    const topLines = wrapText(ctx, topText.toUpperCase(), width * 0.85);
    topLines.forEach((line, i) => {
      const y = height * 0.12 + i * fontSize * 1.3;
      ctx.strokeText(line, width / 2, y);
      ctx.fillText(line, width / 2, y);
    });
  }

  // Bottom text
  if (bottomText) {
    ctx.font = `900 ${fontSize}px ${BRAND.font}`;
    ctx.fillStyle = BRAND.accent;
    ctx.textAlign = 'center';
    ctx.strokeStyle = 'rgba(0,0,0,0.8)';
    ctx.lineWidth = 3;

    const bottomLines = wrapText(ctx, bottomText.toUpperCase(), width * 0.85);
    const startY = height * 0.82 - (bottomLines.length - 1) * fontSize * 1.3;
    bottomLines.forEach((line, i) => {
      const y = startY + i * fontSize * 1.3;
      ctx.strokeText(line, width / 2, y);
      ctx.fillText(line, width / 2, y);
    });
  }

  // Brand watermark
  ctx.font = `600 ${Math.floor(width * 0.012)}px ${BRAND.monoFont}`;
  ctx.fillStyle = 'rgba(148, 163, 184, 0.15)';
  ctx.textAlign = 'right';
  ctx.fillText('survivingthesingularity.com', width - 20, height - 15);

  return canvas.toDataURL('image/png');
}

/**
 * Generate an Open Graph image for a page
 */
export function generateOGImage({ title, subtitle, badge = 'SURVIVING THE SINGULARITY' }) {
  return generateImage({
    aspect: 'og',
    title,
    subtitle,
    badge
  });
}

/**
 * Download a generated image
 */
export function downloadImage(dataUrl, filename = 'sts-image.png') {
  const a = document.createElement('a');
  a.href = dataUrl;
  a.download = filename;
  a.click();
}

// Helper: word wrap text for canvas
function wrapText(ctx, text, maxWidth) {
  const words = text.split(' ');
  const lines = [];
  let currentLine = '';

  for (const word of words) {
    const testLine = currentLine ? `${currentLine} ${word}` : word;
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && currentLine) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) lines.push(currentLine);
  return lines;
}
