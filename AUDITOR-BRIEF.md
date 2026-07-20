# AUDITOR BRIEF — Surviving the Singularity (book)

Continuation prompt for any agent auditing or editing this book. Read this file
FIRST, in full. It replaces repo spelunking: everything below was verified on
2026-07-19 at book v0.5.2. If you change the system (tools, paths, conventions,
versions), update this file in the same commit.

## 0. Spin-up (run these, read nothing else first)

```bash
cd ~/Code/active/survivingthesingularity
python3 scripts/sts.py status          # git + book version + audit + stripe, one screen
git log --oneline -8                   # what the last sessions did
tail -40 devlog.md                     # narrative history, newest entries at bottom
```

Then read the section of this brief for the pass you're running. Do NOT read
all 30 chapter files to "get oriented"; the roadmap below tells you which files
each pass actually needs.

## 1. Canonical facts

| Fact | Value |
|---|---|
| Repo | `~/Code/active/survivingthesingularity` (SvelteKit site + book) |
| Book source (ONLY truth) | `src/lib/data/book/*.md`, order + version in `book.json` |
| Current version | book.json `version` (v0.6.2 as of this writing, LIVE on main and prod). NEVER trust version strings in docs or filenames over book.json |
| Structure | 30 sections: intro, preface, ch0, 3 part dividers, ch1-18, conclusion, appendices A-E. Order: Introduction BEFORE Preface (deliberate) |
| Stale copies (never audit these) | `manuscript/StS-Complete-Draft-v*.md`, Desktop PDFs, `manuscript/drafts/` |
| Figures | `static/book-images/*.svg` (33 hand-authored) + `part{1,2,3}-divider.png` (pixel art) + photo headers. Referenced as `![alt](/book-images/…)` + italic caption line |
| Built artifacts | `book-build/Surviving-the-Singularity-v<X>.{epub,pdf}` + `-PLAIN.pdf` / `-DELUXE.pdf` variants |
| Public download | `static/downloads/Surviving-the-Singularity-v<X>.pdf`; the /book page buttons build their href from book.json version automatically |
| Branch | `weave-and-mobile-polish`. NEVER merge to main on your own: main auto-deploys prod, and prod runs LIVE Stripe keys. Merging is the author's call only. (2026-07-19 evening: CT explicitly authorized a merge; branch was merged to `main` at `fe12ffc` and Cloudflare deployed v0.6.2 to prod. Branch and main are reconciled to the same commit. The rule still stands for every future unsupervised merge.) |
| Book page gate | /book is password-gated client-side; password constant lives in `src/lib/bookAccessCode.js` (needed for Playwright verification) |
| Author rules | NO em dashes anywhere (settled, whole book swept at v0.5.0). NEVER use the word "manifesto" anywhere (settled at v0.6.2; only survivor is Bastani's real citation subtitle in Appendix B). Focus HYPER-LOCAL, not decentralized: "decentralized" only where it names actually-decentralized tech (mesh, LoRa, IPFS, distributed energy), never heralded as the goal (anchor thesis in ch9). Versions bump on every content change. Author = Christopher (CT); he rules on voice, structure, and anything touching money |
| Continuity bibles | `src/lib/data/book/ELIJAH-PROTOCOL.md` (narrative timeline, Chekhov registry), `WRITING_CHECKLIST.md` (style), `manuscript/EDITORIAL-QUEUE.md` (editorial state, latest-version header) |

## 2. Already done — do not redo

- **v0.5.0 "illustrated draft"**: all 34 ASCII diagrams → real SVG figures
  (site palette #020617/#f59e0b/#3b82f6, mono labels, alt text, captions);
  2 box tables → markdown; mechanical pass (dup Economic Paradox section,
  LaTeX remnants, blank table headers, FALC 5th driver, Grace et al. numbers,
  stale chapter cross-refs remapped, ch9 fence bugs); credibility pass
  (invented formulas → sourced claims, model-collapse entropy direction,
  overclaims softened); full em-dash sweep (98 instances).
- **v0.5.1**: intro's Ledger framing rewritten per CT ruling: the machine IS
  unprecedented (a tool that invents tools); the stampede is not. Thesis line:
  "The technology is new every time. The stampede never is."
- **v0.5.2**: "The wise ones are learning how to solder." became a standalone
  pull quote (`> **…**` in 02-introduction.md); `sts.py scan` added; PLAIN and
  DELUXE PDF variants added; PDF title-page version stamp + per-page footer.
- **v0.6.0-0.6.2 "the techno-optimist turn"** (CT rulings): Intro gained the
  ox/husbandry passage (labor delegated to something that runs on its own; "we're
  so back" vs "it's all over" are the same facts; capitalism persists but stops
  being mandatory for survival), the AI-slop hit sharpened onto wounded status,
  and two reader-punishing lines redirected off the reader. Ch17 gained "The Proof
  Is Not Hypothetical" (SECTOR 07 photobioreactor + EasyGrow DIY builders vs the
  industrial "reduces human touch" pitch; Appendix B sources 179-182; transcripts
  in manuscript/solarpunk-source/). Conclusion's Moral Mandate amplified into the
  closing call to action. Second-audit fixes: ch4 sneer→awe, ch18 "coward's way
  out"→"fear wearing the costume of caution," "slave protocol"→"leash" x2. Word
  rulings: "manifesto" removed everywhere; decentralization de-heralded → hyper-local.
  Site: /book download button removed (view-in-browser button stays), /book hero
  copy rewritten to the new framing. Merged to main and deployed live to prod.
- Fact-checks already verified: P-01..P-06 precedents, June 2026 export
  directive (sources 162-165), Red Flag Act, NYT 1903, DishBrain (AU$),
  Kipping math, Gloria Mark interruption research.

## 3. Toolbelt

```bash
python3 scripts/sts.py status|audit|book|scan|compile|live|stripe   # --json on all
python3 scripts/sts.py book --thin 1500     # word counts, thin chapters
python3 scripts/sts.py scan                 # scannability: pull quotes, walls, deserts, texture
python3 scripts/sts.py compile --force      # one-file draft in manuscript/
bash scripts/build-epub.sh vX.Y.Z           # shipping EPUB + PDF (version-stamped)
bash scripts/build-pdf-variants.sh vX.Y.Z   # PLAIN (floor) + DELUXE (ceiling) PDFs
```

- Pull-quote syntax in source: a standalone `> **Sentence.**` line. Site/EPUB
  render it as a bold blockquote; DELUXE renders it as a centered amber pull
  quote; PLAIN folds it back into prose. Errors log to `book-build/.variant-build.log`.
- Stylesheets: `scripts/book-print.css` (shipping), `-plain.css`, `-deluxe.css`.
  `BOOK_VERSION` placeholder is sed-stamped at build time.
- weasyprint gotcha: floating `::first-letter` crashes on image-only paragraphs
  (`AssertionError … BlockReplacedBox`); use inline raised caps instead.

## 4. Verification recipes (run before claiming anything is fixed)

```bash
# 1. Site render probe: renders every section with the site's own marked;
#    checks all images resolve and no diagram wreckage survives in <pre>.
node -e "$(cat <<'EOF'
const { marked } = require('marked'); const fs=require('fs');
const dir='src/lib/data/book'; const book=JSON.parse(fs.readFileSync(dir+'/book.json'));
let n=0, bad=[];
for (const s of book.sections){ const h=marked(fs.readFileSync(dir+'/'+s.file,'utf8'));
  for(const m of h.matchAll(/<img src="(\/book-images\/[^"]+)"/g)){n++;
    if(!fs.existsSync('static'+m[1]))bad.push(s.file+': '+m[1]);}
  for(const p of h.matchAll(/<pre>[\s\S]*?<\/pre>/g)) if(/[│┌└─▼◄►]/.test(p[0])) bad.push(s.file+': wreckage');}
console.log('imgs',n, bad.length?bad:'CLEAN');
EOF
)"

# 2. PDF check (pypdf is installed): version on title page, footers on pages
python3 -c "
from pypdf import PdfReader; r=PdfReader('book-build/<file>.pdf')
print(len(r.pages), 'v0.' in (r.pages[0].extract_text() or ''), 'v0.' in (r.pages[50].extract_text() or ''))"

# 3. /book page through the gate (Playwright lives in ~/Code/johnnyautoseed):
#    npm run build && npm run preview -- --port 4399, then drive the password
#    from src/lib/bookAccessCode.js into input[type=password], click Unlock.

# 4. Figures visually: chrome --headless --screenshot=<out> \
#    http://localhost:4399/book-images/<name>.svg
```

## 5. The versioning ritual (every content change, no exceptions)

1. Edit book source → bump `book.json` version (0.0.1-style increments).
2. `python3 scripts/sts.py compile --force`
3. `bash scripts/build-epub.sh v<X>` (+ variants if the pass touched formatting)
4. Swap `static/downloads/`: remove old PDF, `cp` new one (buttons auto-track).
5. Update records: `devlog.md` (append entry), `manuscript/EDITORIAL-QUEUE.md`
   (LATEST VERSION header), and the vault banner notes
   (`~/Documents/Personal-Remote-Vault/2026-07-1*_StS_*.md`, via SimpleAgentOS
   `atomic_io`, never raw writes).
6. Verify (section 4), commit on `weave-and-mobile-polish` with a `book:` prefix,
   push. Do not merge to main.

## 6. Audit roadmap (pick a pass; each lists exactly what to read)

| Pass | Read | Method |
|---|---|---|
| A. Rendering | nothing up front | Recipe 4.1, then `sts.py audit`. Fix only what it flags |
| B. Facts / allegories | One chapter at a time + `manuscript/HISTORY-CASEBOOK.md` | Verify every date, name, quote, number in P-07..P-22 (P-01..P-06 done). WebSearch receipts; log new sources to Appendix B (23-appendix-b.md, next number 179) |
| C. Voice unification | `WRITING_CHECKLIST.md` + the Foundations sections of ch4, 6-13, 18 | Biggest open job. Narrative scenes are strong; Foundations swing rant↔academic. Field-manual register is the target for Part III |
| D. Elijah continuity | `ELIJAH-PROTOCOL.md` + narrative openers of ch0-18 + conclusion | Timeline: toast → all-hands → resignation at 11 months → co-op arc. Check tells, seasons, Chekhov registry |
| E. Cross-refs | grep `(Chapter` and `(Chapters` across book dir | Verify against real TOC (land=12, soil=15, tools/mesh=17, servers=11, factory/ACT=9, mesh-network concept=14). Swept at v0.5.0; re-verify after any restructure |
| F. Scannability | `sts.py scan` output only | Promote flagged pull quotes (`> **…**`), split WALL paragraphs, add subheads in HEAD deserts. Narrative scenes are ALLOWED to be low-texture; judgment required |
| G. Figures | `static/book-images/*.svg` + captions in-place | Palette/type consistency, alt text truthfulness, contrast at render size (Recipe 4.4) |
| H. Sources | `23-appendix-b.md` | Click-check URLs resolve (166-178 cyberdeck sources still unverified); numbering continuous; every precedent claim has a source |
| I. Build QA | build outputs | Run ritual steps 2-3, Recipe 4.2, spot-read EPUB on a device (never done yet) |

## 7. Known open items (as of v0.5.2)

- Voice-unification pass (roadmap C) not started; it is the largest remaining job.
- Appendix C is 344 words; decide whether intentionally thin or expand.
- Cyberdeck source URLs 166-178 unverified (roadmap H).
- EPUB device spot-read never performed.
- The public PDF URL is unauthenticated while /book is $5-gated; CT ruled the
  download button be REMOVED (done at v0.6.2); the view-in-browser button stays
  and the PDF path is still public. He is fine with that. Do not re-add a download button.
- ~~Merge to main awaits CT.~~ DONE 2026-07-19 evening: CT authorized it; branch
  merged to main at `fe12ffc`, prod deployed v0.6.2, verified live (24/24 routes,
  v0.6.2 PDF serving). main and the branch are reconciled.
- Stripe go-live sequence (A1-A8 in the vault plan) is site work, not book work.
- Vault banners synced to v0.6.2 (2026-07-18_StS_Open_Items, _Master_Undone,
  2026-07-19_StS_Plan_of_Action) via SimpleAgentOS atomic_io.

## 8. Coordination

- Parallel sessions edit this repo. `git status` + file mtimes before editing;
  one committer per fix list; commit per coherent wave, `book:` prefix.
- Report-then-fix: for judgment calls (voice, structure, cuts) deliver findings
  to CT first. Mechanical defects (broken rendering, typos, stale refs) fix
  directly, with the verification recipes as your gate.
