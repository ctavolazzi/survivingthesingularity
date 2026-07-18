# Development Log
*Last Updated: 2025-01-27 20:30 UTC*

## 2025-01-27 20:30 UTC - Project Exploration and Johnny Decimal Structure
- Conducted comprehensive project exploration and structure analysis
- Created work effort 00.01 for project exploration documentation
- Established Johnny Decimal structure for work_efforts directory (00-09_project_management/00_organization/)
- Documented key findings about project architecture, current state, and development workflow
- Identified project as SvelteKit-based educational platform about AI/Singularity preparedness
- Noted active development on Svelte warnings cleanup and recent blog post creation
- Set foundation for organized work effort management going forward
- Next step: User can proceed with specific development tasks using proper work effort structure

## 2025-03-29 20:55 UTC - Fixed Image Loading Issues
- Identified the root cause of 404 errors related to blog images
- The Image component was automatically generating WebP paths that didn't exist
- Fixed by removing the automatic WebP path generation in src/lib/components/ui/Image.svelte
- This resolved the 404 errors for images like whispers-ai-featured.webp
- Updated the work effort documentation with the solution

## 2025-03-29 20:45 UTC - Debugging Svelte Warnings
- Created work effort #18 focused on debugging Svelte warnings
- Taking a structured approach to address issues one at a time
- Focus areas include unused CSS selectors, accessibility warnings, and unused exports
- Documenting fixes to prevent similar issues in future
- Setting up progress tracking system to methodically address all warnings

### Fixes in progress:
- Added keyboard event handlers in AGIRoadmap.svelte to fix accessibility issues
- Added ARIA role and label in NewsTicker.svelte for better accessibility
- Fixed nesting of figcaption within figure in Image.svelte
- Moved @import statement to the top of app.css to fix CSS import issue
- Removed unused CSS selectors in AGIRoadmap.svelte
- Removed numerous unused CSS selectors in Timeline.svelte (21 selectors total)
- Changed unused export properties to export const in NewsTicker.svelte
- Changed unused export properties to export const in BookCallout.svelte
- Fixed unused CSS class in FeaturedPosts.svelte by applying Tailwind classes directly
- Removed a large number of unused CSS selectors in start-here/+page.svelte related to TreasureTavernAd

### Technical limitations:
- Large file size in start-here/+page.svelte is making comprehensive edits challenging
- Breaking down changes into smaller, focused updates to improve reliability

### Next steps:
- Continue addressing remaining CSS selector issues
- Implement final verification testing

## 2025-03-29 20:30 UTC - Continuing Svelte Debugging
- Made significant progress addressing various warnings
- Fixed unused CSS selector issues in the home page
- Working on addressing large components with many unused selectors

## 2025-03-28
### New Blog Post: Whispers of the Future
- Created new work effort (17) for blog post creation
- Blog post titled "Whispers of the Future: The Paradigm Shift of Human-AI Relations"
- Will explore the evolving relationship between humans and AI
- Plan to implement following project's established blog structure

### Blog Post Implementation: Whispers of the Future
- Created blog post files in src/lib/data/blog-posts/whispers-of-the-future/
- Created content.md with the essay content
- Created index.js with post metadata
- Updated blogPosts.js to include the new post at the top of the list
- Added custom featured image (2.77MB) for the post
- Ensured post date is set to 2025-03-28
- Created dedicated route page with styled content display
- Added post to the main blog listing page
- Work effort completed successfully

## 2024-03-19
### Site Structure Documentation
- Created comprehensive SITEMAP.md documenting:
  - Layout components and their data flow
  - Main pages and their components
  - Data sources and API endpoints
  - State management approach
  - Component categorization
- Added timestamps to documentation files for better tracking
- Organized components into logical categories:
  - UI Components
  - Layout Components
  - Content Components
  - Interactive Components
  - Data Display Components
  - Utility Components

### New Work Effort: AGI Roadmap Component
- Created new work effort document for AGI Roadmap component
- Defined component structure and features
- Planned implementation approach
- Established success criteria and dependencies
- Component will show remaining technological announcements needed for AGI
- Will be integrated into the home page to answer "what's next?" question

### AGI Roadmap Work Effort Organization
- Created dedicated folder structure for AGI Roadmap work effort
- Moved work effort documentation to README.md
- Created initial technologies.json with sample data
- Defined technology categories and their visual representations
- Established initial set of key technologies needed for AGI
- Set up dependency relationships between technologies

### AGI Roadmap Component Implementation
- Created AGIRoadmap.svelte component with:
  - Status indicators (red X for pending, green checkmark for satisfied)
  - Progress bars showing overall satisfaction level
  - FAQ section for each technology
  - Article links with satisfaction levels
  - Responsive design with dark mode support
- Updated technologies.json with:
  - FAQ items for each technology
  - Article links with dates and satisfaction levels
  - Visual categorization
- Implemented satisfaction tracking system
- Added hover effects and smooth transitions

## 2026-07-17 - Precedent Ledger weave + sts.py research/compile commands
- Wove the Precedent Ledger through the whole book: 22 ID'd historical allegories (P-01..P-22), one closing every section from Preface to Conclusion, in the Greene register (story -> mechanism -> rule)
- Range: Neolithic grain trap (c. 9500 BC) -> Bronze Age collapse -> Trithemius -> Red Flag Act -> Luddites -> Kodak/Sears/Blockbuster/Borders graveyard -> "internet is a passing fad" trio (Stoll 1995, Krugman 1998, Daily Mail 2000)
- Device introduced at the end of the Introduction; P-01 (the 1790s novel-reading panic) opens the ledger in the Preface; new Appendix D indexes all 22 with one-line rules
- Added `sts.py research` (Wikipedia API + Mojeek/DDG web search, --save to manuscript/sources/research-log.md); every new case verified with citable sources; apocrypha blacklist extended (manure-crisis quote, Pedro II "it talks", Duell)
- Added `sts.py compile`; produced manuscript/StS-Complete-Draft-v0.0.7.md (74,002 words, 29 sections)
- Verified: production build passes, /book pages render precedents (preview + curl), EPUB rebuild contains all 22 + Appendix D
- Book: 66,321 -> 73,636 words; Conclusion no longer the thin outlier (313 -> ~1,600 in book source)

## 2026-07-17 (later) - Precedent Ledger practice layer
- Added "The practice" to all 22 precedent blocks: three concrete, week-sized actions each, tied to the chapter's own protocol (energy audit, capability inventory, desire audit, receipts file, household premortem, etc.)
- Appendix D gained the operating manual: "How to Run the Ledger" (7 steps, Carnegie's use-instructions model: read twice, locate yourself, name your seat, run the rule in 24h, do the practices, quarterly review, teach one entry) plus "The Symptom Index" (22-row situation -> precedent lookup)
- Introduction now names the four-beat structure (story -> mechanism -> rule -> practice) and points at Appendix D
- Verified: 22 practice sections, no em dashes in new copy, production build passes, EPUB rebuilt with manual + index; compiled manuscript/StS-Complete-Draft-v0.0.8.md (78,857 words)
- Book source now ~78,650 words (was 73,636 after the morning weave)
