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

## 2026-07-18 - Content-complete push: Egalitarian Pivot, Stage-2 evidence, citation sync
- Discovered the Conclusion's Bear Flag scene never names Elijah (grep + the site's inProgress flag both missed it); named him once, which also clears the false "in progress" badge on /book
- Wrote "The Egalitarian Pivot" into Ch. 7 Foundations (after Primate Backlash, bridging into P-09): the homepage-promised section; ~600 words on trust as the post-credential premium and the co-op as the scarcity-psychology cure
- Wove the June 2026 Stage-2 receipt into Ch. 2 (export directive -> worldwide shutoff -> same-day open-weight release; verified via web search, sources in Appendix B 162-165); rewrote the P-04 Red Flag block as a compressed case file to kill the double-telling
- Appendix B: added 133-161 (all Precedent Ledger sources) + 162-165 (Stage-2 evidence)
- book.json bumped 0.3.0 -> 0.3.1; built and probed Surviving-the-Singularity-v0.3.1.pdf/.epub (Egalitarian Pivot, June 2026 weave, Ledger manual, symptom index all present); PDF opened locally
- Compiled manuscript/StS-Complete-Draft-v0.0.9.md (80,220 words); book source now ~80,000 words
- EDITORIAL-QUEUE: both outline gaps marked resolved; drafts/ files it referenced never existed (noted in place)
- Manuscript is now content-complete per the queue's own definition; remaining pre-launch items are the voice pass, EPUB spot-read on devices, and production/front-matter work

## 2026-07-19 - v0.5.0: the illustrated draft (Claude's version)
- Every text-drawn diagram in the book is now a real figure: 33 hand-authored dark-theme SVGs in static/book-images/ (site palette, mono labels, self-contained canvases that render on any background), each with alt text and an italic caption. The 15 broken shattered-fence diagrams are gone; the 19 intact ASCII ones got real figures too (the ch12 mesh-scheduler stays a terminal block on purpose)
- Two box-drawn tables converted to markdown tables (ch5 efficiency, ch8 processing styles)
- Mechanical pass: preface epigraph spacing + quad-asterisk bold, intro paperback anachronism -> cheap novel, ch1 real table headers + LaTeX remnants removed + Transformer param count + FALC fifth driver + Grace et al. figures corrected, ch2 stage-transition dedup + adults defined, ch6 verbatim Economic Paradox dup replaced with a bridge, ch8 'final chapter' artifacts + article typos, ch9 bash comments fenced (rendered as H1s) + fence-wrapped bullets unwrapped, stale chapter cross-refs remapped across ch8/ch9/ch12/appendix A
- Credibility pass: invented formulas reframed as honest sourced claims (Gloria Mark on interruption, Shannon entropy as a lens, Kipping in plain language), model-collapse entropy direction fixed and inevitability hedged to the published result, overclaims softened (self-awareness, 98%, yield stats), Mathematical Dead End given actual arithmetic
- Em-dash sweep: 98 instances rewritten across ch4-ch9; all 30 shipped sections are now em-dash free, resolving the long-open policy question in favor of the global rule
- Pixel art: three part-divider banners drawn in Aseprite (event-horizon grid, cooperative fire circle, shouse homestead), exported 4x nearest-neighbor to static/book-images/part{1,2,3}-divider.png
- build-epub.sh now carries .svg into the EPUB/PDF image set
- Verified: npm run build clean, sts.py audit 0/0, marked-level render probe over all 30 sections (59 images all resolve, zero wreckage in any pre block), headless Chrome screenshots of 4 figures (1 label collision found and fixed)
- book.json 0.4.0 -> 0.5.0
- Later same day: PDF published as a public download at /downloads, view + download buttons on /book (version read live from book.json)

## 2026-07-19 (later) - v0.5.1: the Ledger's framing corrected (author ruling)
- CT ruling on the introduction's Precedent Ledger passage: "nothing like this has ever happened before" is TRUE, not a lie. The machine is unprecedented (a tool that invents new tools, one of our most sacred core functions); what is precedented is the size, shape, and scale of the change and the human reaction to it
- Rewrote the passage around that distinction, folding in CT's material: the goalpost-moving ("it can't do Y, until it does"), the AI-slop chorus as ego (the forager / hand-scribed manuscript / stage-play analogies), "the wise ones are learning how to solder," and the new thesis line: the technology is new every time, the stampede never is
- book.json 0.5.0 -> 0.5.1; recompiled draft (83,377 words); rebuilt EPUB + PDF at v0.5.1; public download swapped to Surviving-the-Singularity-v0.5.1.pdf (the /book buttons track book.version automatically)
