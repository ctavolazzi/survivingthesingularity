---
title: "Future Predictions Heading Backlight"
status: "in progress"
priority: "medium"
assignee: "design team"
created: "2024-03-08"
last_updated: "2024-03-08"
tags: [design, visual effects, typography]
---

# Future Predictions Heading Backlight

## 🚩 Objectives
- Add a backlight (glow effect) behind the "Future Predictions" heading
- Enhance visual impact of this important section
- Maintain responsive design across all screen sizes
- Ensure the effect is visually appealing and on-brand

## 🛠 Tasks
- [x] Identify the current structure of the heading in FuturePredictions.svelte
- [x] Design and implement a backlight effect that complements the existing design
- [x] Ensure the effect works well with the existing title gradient and decoration
- [x] Test across various screen sizes and device types
- [x] Optimize animation performance

## 📝 Notes
The current implementation already has several visual effects:
1. A gradient color animation on the word "Future"
2. A decorative underline with glow animation
3. Text shadow effects

The backlight effect should complement these existing elements without overwhelming the design.

## 🐞 Issues Encountered
- Needed to add z-index handling to ensure the text remains above the backlight
- Adjusted blur and opacity levels to ensure the effect is visible but not overpowering
- Tailored the size and position for different screen sizes to maintain proportions
- Initially implemented with subtle effect; enhanced contrast and intensity based on feedback

## ✅ Outcomes & Results
- Added a radial gradient backlight effect behind the "Future Predictions" heading
- Created a pulsing animation that complements the existing gradient animations
- **Enhanced contrast and visual impact** with higher opacity values and stronger glow
- Added multi-layered box shadows for additional depth and visual prominence
- Ensured the effect scales appropriately on different screen sizes
- Maintained text readability while enhancing visual impact
- Used colors that match the existing design system (blue, purple, pink gradients)

## 📅 Timeline & Progress
- **Started**: 2024-03-08
- **Completed**: 2024-03-08
- **Updated**: 2024-03-08 (Enhanced contrast and effect intensity)

## 💻 Implementation Details
Added a pseudo-element (::before) to the "future-title" class with:
- Radial gradient background with brand colors (blue, purple, pink) at **higher opacity values**
- **Reduced blur effect** for sharper appearance
- **Added multi-layered box-shadow** for enhanced glow effect
- Animation to create a pulsing effect with **increased scale and opacity changes**
- Responsive adjustments for different screen sizes
- Proper z-index handling to maintain text readability