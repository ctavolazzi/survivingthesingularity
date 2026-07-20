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

## 2026-07-19 (later still) - v0.5.2: pull quote, scan tool, PLAIN + DELUXE variants, auditor brief
- "The wise ones are learning how to solder." moved to its own line as a pull quote (`> **...**` in 02-introduction.md); DELUXE renders it as a centered amber showpiece, site/EPUB as a bold blockquote, PLAIN folds it back into prose
- New `sts.py scan`: scannability auditor (pull-quote candidates, wall-of-text paragraphs, heading/emphasis deserts, list opportunities, per-chapter texture score). First run immediately surfaced "The stampede never is." as a top candidate
- New `scripts/build-pdf-variants.sh` + book-print-plain.css / book-print-deluxe.css: PLAIN (2 MB, pure text, no images, the reading floor) and DELUXE (running chapter headers, raised caps, styled pull quotes, TOC dot leaders with live page numbers, tinted tables/code, ornamental rules; the design ceiling). Ship draft sits between them by design
- weasyprint lesson recorded: floating ::first-letter crashes on image-only paragraphs; use inline raised caps
- AUDITOR-BRIEF.md written at repo root: full continuation prompt for future auditing agents (spin-up commands, canonical facts, done-list, toolbelt, verification recipes, versioning ritual, 9-pass audit roadmap, open items)
- book.json 0.5.1 -> 0.5.2; EPUB/PDF + variants rebuilt; public download swapped to v0.5.2

## 2026-07-19 (later still) - v0.6.0: the techno-optimist turn (CT ruling)
- CT ruling on tone: the book must confront defeatism, not the reader. "It's all over" and "we're so back" are the same facts read by two kinds of people; the tools don't choose, people do. Abrasion aims at the AI-slop crowd and the doomers, never the anxious young reader we're recruiting. The argument to make explicit: capitalism persists (not the end of the world OR the end of capitalism), what ends is it being MANDATORY for survival. Optional, not abolished.
- Introduction: inserted the ox/husbandry passage (you don't program an ox; you point it at the field and the work gets done without a human doing it; the machine is the second time in history labor can be delegated to something that runs on its own), folding in the "easier to imagine the end of the world than the end of capitalism" reflex and the capitalism-optional argument. Sharpened the AI-slop confrontation onto wounded status ("I was special for knowing how to do this, and now I'm not... think about someone other than yourself for once"), still landing on the "learning how to solder" pull quote. Redirected two reader-punishing lines off the reader: the "parroting a Reddit thread / you're the noise" jab (now aimed at the loud voices, with the reader invited to go verify) and the "stop looking for a safe space" culture-war tripwire (now "stop waiting for someone to promise you it'll be fine").
- Chapter 17 (Tools of the Trade): added Foundations section "The Proof Is Not Hypothetical" - real DIY builders as evidence for the optimism the book asserts. SECTOR 07's 3D-printed photobioreactor (algae fish-food loop on a Bambu A1 + Pi + Arduino, honestly unfinished, schematics free) and Kirsten Dirksen's EasyGrow (one-man off-grid vertical farms + self-wound axial-flux wind turbines, feeding a stadium/Nigeria/Argentina, "I'm not in business to get rich, I'm in business to grow food and help people grow food"), contrasted against the industrial vertical-farm pitch ("reduces labor costs," "decreases human touch"). Same tech, opposite spirit; the tools don't choose, people do.
- Sourced four YouTube builds transcribed for this pass (yt-dlp, auto-subs cleaned to plain text) into Appendix B 179-182. Raw transcripts + the full editorial/tone note live in manuscript/solarpunk-source/.
- book.json 0.5.2 -> 0.6.0; compiled draft (84,401 words); render probe CLEAN (59 imgs resolve, zero wreckage); rebuilt EPUB + PDF at v0.6.0 (254 pages, version on title page, footers verified); public download swapped to Surviving-the-Singularity-v0.6.0.pdf (the /book buttons track book.version automatically)
- Did NOT touch ch4's "pathetic absurdity / human arrogance" passage; it aims contempt at executives and politicians, not the reader, so it's left as author's call.

## 2026-07-19 (final) - v0.6.1: the techno-optimist turn, completed
- Second tone audit closed out the four items flagged after v0.6.0: ch4's "look back and laugh at the sheer, pathetic absurdity / that is the scale of human arrogance" reframed from sneer to awe ("feel the vertigo of the distances involved / we reached for a leash and closed our hand on infinity"), target (Stage-2 regulators) kept; ch18's "the ultimate coward's way out" reframed to "fear wearing the costume of caution. Name the vulnerability out loud, then build against it anyway"; two "slave protocol" metaphors (ch8 batch-processing, ch10 platform metrics) reworded to "leash," matching the book's own "electronic leash" vocabulary (ch17).
- Conclusion "The Moral Mandate" amplified into the closing call to action per CT's direction: things are changing and you can do this; you can have robots that grow your food and build your house, and you can make/teach/train them yourself; drop the outdated mindset and the self-doubt (the last fence nobody else can tear down for you); look it straight in the face, now; do it for your kids, grandkids, all of humanity; every capable person who wakes up is one more on the side of the light; don't let the capitalist goblins regulate you out of the opportunity; you were not born to increase shareholder value, you were born to care for the Earth, the Sky, and each other. Kept the existing "Wake the fuck up" punch upstream in the Foundations so the Mandate echoes without repeating verbatim.
- book.json 0.6.0 -> 0.6.1; compiled draft 84,796 words; render probe CLEAN; EPUB/PDF rebuilt at v0.6.1 (255 pages, title stamp + footers verified); public download swapped to Surviving-the-Singularity-v0.6.1.pdf.
- Full second-audit result recorded: reader-scolding second person now zero across the book; no unreframed doom (remaining "too late/doomed" instances are in-scene narrative, historical cases, or the Eddington thermodynamics epigraph); capitalism-persists argument consistent with the Preface ("not a guide to overthrow the system") and ch6 ("we do not need to take anyone's money"). v0.6.1 is the complete draft.

## 2026-07-19 (final +1) - v0.6.2: two word rulings (manifesto out, decentralization de-heralded)
- CT ruling: never use the word "manifesto" (settled, same weight as the em-dash rule). Removed from book prose (ch1 "the FALC manifesto posits" -> "FALC posits"; ch5 "the manifesto chapters of this book" -> "the Foundations chapters of this book"). Renamed the internal hot first-person voice register in ELIJAH-PROTOCOL.md from "Manifesto" to "Declaration" (+ EDITORIAL-QUEUE register table). Only survivor is the real published subtitle of Aaron Bastani's "Fully Automated Luxury Communism: A Manifesto" in Appendix B (altering a real citation would falsify it; flagged to CT). Saved as a global feedback memory.
- CT ruling: focus on hyper-local over decentralized. Decentralization is NOT the goal and must not be heralded or championed; the goal is hyper-local survival, community building, individual empowerment that benefits the community, deglobalization, and self-reliance (your own mind and hands). "Decentralized" stays only where it names actually-decentralized tech (mesh, LoRa, Meshtastic, IPFS, crypto, distributed energy). Reframed the heralding uses: ch8 "decentralized philosophy of The Commons" -> "hyper-local"; ch8 "decentralized node of three households" -> "hyper-local node"; ch12 "productive node in a decentralized industrial network" -> "hyper-local industrial network"; ch14 "high-leverage, decentralized design" -> "hyper-local design"; ch17 figure "Decentralized Fab Lab" -> "Independent Fab Lab" (matches the chapter's own text) + "gold standard for decentralized fabrication" -> "local, independent fabrication"; appendix C "decentralized, rational actors" -> "independent, rational actors"; appendix A "decentralized technological coordination are critical public goods" -> "hyper-local technological coordination". The anchor thesis already lives in ch9 ("Deglobalization, Not Decentralization: 'Decentralized' is a dangerous word... The real target is deglobalization"), so the terminology now matches the book's own stated position.
- Also folded in this wave (built but not yet shipped at v0.6.1): ch4 sneer -> awe, ch18 "coward's way out" -> "fear wearing the costume of caution," two "slave protocol" -> "leash," and the Conclusion's Moral Mandate amplified into the closing call to action.
- book.json 0.6.1 -> 0.6.2 (0.6.1 never shipped separately); compiled 84,795 words; render probe CLEAN; EPUB/PDF rebuilt at v0.6.2 (255 pages, stamped, footers verified); public download swapped to v0.6.2. Third full tone audit: reader-scolding second person zero, culture-war tripwires zero, shipped book em-dash-free and manifesto-free.
