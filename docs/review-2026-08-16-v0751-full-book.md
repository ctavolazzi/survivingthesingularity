# Full-book page-by-page review — v0.7.5.1 (2026-08-16)

**Corpus:** `src/lib/data/book/` at `eb825cc`, `book.json` version `0.7.5.1` (released `0.7.5`).
**Version determination:** `book.json` is the only authoritative statement of the version (per V0.7.5.1-SCOPE.md). The directory/branch name `sts-v0.7.3` is a historical accident. Confirmed against RELEASES.md and the scope-doc chain (V0.7.3 → V0.7.4 → V0.7.5 → V0.7.5.1, only the last one OPEN).
**Method:** 8 parallel reviewers, every line of all 27 content files, each primed with VOICE-GUIDE.md and the house rules; `sts.py verify` harness; mechanical scans; Appendix B structural audit; cross-references verified against target chapters, not assumed.
**Second pass (2026-08-28):** external fact-check of non-precedent claims, `manuscript/` support-directory audit, hand-verification of the harness's unreachable links, Appendix B entry-quality audit. Every fact-check verdict rests on a source retrieved in-session; nothing is asserted from memory, and where a primary source could not be retrieved it is labelled as such.

---

## Scoreboard

| Layer | Verdict |
|---|---|
| `sts.py verify` (math, meta, refs, precedents) | **Clean** |
| Links, 245 sources | **0 dead.** 1 citation-content drift found by hand (source 62) that the checker cannot see |
| Built PDF + EPUB (v0.7.5) | **Clean** |
| Image/art layer | **Pass**, 3 should-fix |
| Appendix B structure | 232 entries, **no gaps**; 2 malformed, 4 duplicate URLs |
| Meta-doc exclusion | **Verified** — 30 sections ship, meta docs excluded |
| Prose / voice / continuity | **10 blockers**, ~50 should-fix |
| External fact-check | **15 confirmed errors**, 5 needing repair, 3 correct-as-written, 1 unverifiable |

**The three that matter most, in order:** (0) Chapter 7 asserts a claim the book's own Appendix B calls an error and dares the reader to check it; (1) the Mycodo block sends readers to a 404 and then to the wrong port; (12-chapter10:219) the barter sentence is legally false in a way that reads as advice to under-report income.

**Not yet done:** none of this is fixed. This is a findings document; every item is still open in source.

---

## Harness + mechanical layer (whole book) — CLEAN

- `sts.py verify`: math 0, meta drift 0, dangling cross-refs 0, precedents P-01..P-23 all present and indexed in Appendix D.
- Links: see the re-run note at the bottom of this file.
- Em dashes: 0 in book prose (only ELIJAH-PROTOCOL.md, a meta doc). "manifesto": only the sanctioned Appendix B citation titles. No static-data-as-"live" claims.
- Appendix B numbering: 1–232 contiguous, 0 gaps, 0 duplicate numbers. 4 URLs each appear under two different numbers (dedup candidates): Wikipedia Technological_singularity; MIT OCW Sousa PDF; LoC 2006681076 (153 vs 193, both citing Common Sense — possibly deliberate); Snopes Kodak.
- `book.json` / `manuscript-index.json` agree with each other and with the directory contents.
- **Meta-doc exclusion verified (2026-08-28).** `book.json` ships exactly 30 sections, 0 missing from disk, and the only `.md` files on disk that it does *not* ship are the three meta docs (`ELIJAH-PROTOCOL.md`, `README.md`, `VOICE-GUIDE.md`). This matters: ELIJAH-PROTOCOL carries **86 em dashes across 73 lines**, and this check is what proves they never reach a reader. Re-run it if the book manifest changes.

  *Correction (2026-08-28):* this line previously read "73 em dashes". That was a `grep -c` **line** count mistaken for a character count. 73 is the number of lines containing one; 86 is the number of dashes. Caught by `scripts/verify_review_claims.py` check A5, which is why that script exists.

## BLOCKERS

0. **09-chapter7.md:40 — the book asserts, as dialogue, a claim its own Appendix B classifies as an error, and tells the reader to go verify it.** This is the most serious finding in the review.
   - Marta says: *"they deployed more soldiers against those weavers than they were using against Napoleon at the time. **Look it up, it's a hell of a statistic.**"*
   - **Appendix B entry 189** cites Hobsbawm's "The Machine Breakers" as *"the essay in which the Wellington comparison first appears, **cited here as the source of the error rather than as authority for it**."* Entry 188 is Anton Howes's article debunking it. The citation audit already reached the correct verdict; the prose never got the memo.
   - **The history:** Hobsbawm compared the 12,000 troops in the Midlands (1812) against Wellington's Peninsular force of **1808** (~11,000) — two figures four years apart. The correct like-for-like 1812 comparison is **~50,000 in the Peninsula vs 12,000 in the Midlands**. Marta's phrase "at the time" is precisely the clause that makes it false.
   - **Why it is a blocker, not a should-fix:** the line does not merely repeat a myth, it stakes credibility on it ("a hell of a statistic") and *instructs the reader to look it up* — and the first thing they find is the debunking, cited in this book's own bibliography. It also directly contradicts Appendix D's boast that fabricated tech-history quotes "were deliberately excluded from this book... The Ledger only carries cases that [survive contact with a primary source]."
   - **Fix:** Marta can keep the rhetorical force with the true and still-striking fact — Parliament made frame-breaking a capital crime and put twelve thousand soldiers into the disturbed counties (sourced at Appendix B 187, and already stated correctly at :144). Drop the Napoleon comparison and the "look it up."
   - Note `09-chapter7.md:144` states the troop figure correctly and carries no Wellington comparison, so the defect is isolated to the dialogue at :40.

1. **11-chapter9.md:185–187 — the Mycodo block carries three separate defects. Verified by HTTP probe 2026-08-28, not inferred.**
   - The install URL `https://raw.githubusercontent.com/kylegabriel/Mycodo/master/install` returns **404**. The reader pipes a 404 into `bash`.
   - Correcting the username alone does **not** fix it: `raw.githubusercontent.com/kizniche/Mycodo/master/install` also returns **404**. The documented installer lives on GitHub Pages, not raw.githubusercontent. Only `https://kizniche.github.io/Mycodo/install` returns **200**.
   - **Correct command:** `curl -L https://kizniche.github.io/Mycodo/install | bash`
   - **:187 is also wrong.** The book sends the reader to `http://<your-pi-ip>:8080`. Mycodo serves its web UI over **HTTPS on 443**: the documented instruction is to browse to `https://<ip>/`. A reader who follows the book gets a connection failure *after a successful install*, which is the worst place to lose them.
   - Probe evidence: `kylegabriel/...` 404 · `kizniche/...raw` 404 · `kizniche.github.io/Mycodo/install` 200.
2. **14-chapter12.md:178–196** — six stale cross-refs in the Phase checklist, all old-numbering fossils, several contradicted by this same file: No-Notifications "(Chapter 3)"→Ch8; LoRa Mesh "(Chapter 10)"→Ch17 (file says Ch17 at L130); GPU workstation "(Chapter 7)"→Ch11 (file says Ch11 at L137); Shouse "(Chapter 5)"→Ch13; DC Microgrid "(Chapter 6)"→Ch17; Mycodo "(Chapter 8)"→Ch9 (file says Ch9 at L109).
3. **13-chapter11.md:297** — "DC bus bar we built in Chapter 6" → Chapter 17.
4. **17-chapter15.md:141** — "Chapter 2 Redirection Protocol" → Chapter 14. Related: :129 "thermodynamic limits... Chapter 1" suspect; **19-chapter17.md:71** "In Chapter 2... Municipal Mesh" → Chapter 14.
5. **Precedent count is off by one in three places, and the conclusion contradicts itself 14 lines apart.** The Ledger holds 23 entries (P-01..P-23 verified present in the book body, Appendix D, and `manuscript/HISTORY-CASEBOOK.md` — all three agree, no gaps).
   - `21-conclusion.md:83` prints **"Precedent P-23: The Passing Fad"**, then `:97` tells the reader "You have now read **twenty-two** entries in the Precedent Ledger" — immediately after they finished the twenty-third.
   - `21-conclusion.md:103` — "**Twenty-two** entries agree on the ending" → twenty-three. (The same line's "twenty-one practices" counts something else; confirm what "practices" enumerates before changing it.)
   - `02-introduction.md:71` — "**twenty-two** documented episodes" → twenty-three.
6. **25-appendix-d.md:103 — wrong referent, and the paragraph's own next sentence proves it.** The fabrications list runs: Western Union "telephone is a toy" → Gates's "640K" → the 1894 "nine feet of manure" → the Bavarian medical board's train/brain-disease decree → "everything that can be invented has been invented". The text then says "**The last one** is worth naming specifically, because it is the single most-cited example of **railway technophobia**" — but the last one is the *patent-office* quote, which has nothing to do with railways. The railway item (the Bavarian decree) is second-to-last. That the following sentence goes on to discuss "the documented history of resistance to the railway" as the better material confirms the intended referent is the Bavarian decree, not the patent quote.
7. **22-appendix-a.md:12** — "historic self-preservation codes deployed during the early days of the Singularity" states fabricated in-universe history as fact, contradicting the book's own sourcing standard.
8. **20-chapter18.md:98–102** — "Synthesis and the New Social Contract" is full academic register inside a field-manual chapter (the VOICE-GUIDE's named defect at strength). Same defect in Part I: **03-chapter1.md:123–180**, four Foundations sections in whitepaper register.
9. **07-chapter5.md:69** — "Now that those supply chains have collapsed... you are on your own": present-tense collapse assertion; prepper drift against the thesis. Related cluster: :62 drone-hunt, :116 "cracks of a technological collapse", :99 "microscopic elite... gathering wood".

## SHOULD-FIX, by file

- **00-chapter0.md:160** — italic bridge explains the scene's moral after "You're holding it."; cut per the vise rule.
- **01-preface.md** — :25 comma tag; :45 "we will explore" drift plus "next few chapters" undersell; :57 "neural link electrodes" blog-era joke; :35 "bypass their systems entirely" secession-adjacent; :43 changelog language in reader prose.
- **02-introduction.md** — :65 "Think about someone other than yourself for once." condescension at the reader (cut); profanity density :13–21.
- **03-chapter1.md** — :64 seventeen/sixteen count contradiction; :84 "Fifteen decades" vs 180 years; :74 Ulam quote abridged inside quote marks; :82 Kelly "five minutes" → years; :68 "quiet for a century" vs 1863 next entry; :47–53 scene over-explains.
- **04-chapter2.md** — :80 "Nobody... Nobody" absolutes; :100 motive-attribution absolutes; :148 "They're lying"/dumb dichotomy; :150–152 accusation aimed at the reader; profanity ×6; :166–176 Stage-5 exit logic duplicated in ch3.
- **05-chapter3.md** — :62–74 primate register; :94 "suffering is the only thing that makes them feel real" sneer; :100 sideways-8 image doesn't parse (no 8 on the page).
- **06-chapter4.md** — :26 "$80 power bill" continuity (baseline ~$40, $211.46 arrives later); :56 humanity/its/their agreement; :90–92 LaTeX render risk in built outputs.
- **07-chapter5.md** — :50 chakra freeze joke at the reader; :54 "independent existence" identity; :118 "decentralized educational content"; :71–72 Third Law gloss non sequitur; :140 "Not one... Every single one" absolutes; :200 "wide stocking frame" forward ref unintroduced; :40 scene explains itself.
- **08-chapter6.md** — :70,:87 "marginal cost of zero" vs ch5's wattage thesis → "collapsing toward zero"; :68 plural/singular; :76 dangling modifier plus "obviously superior".
- **09-chapter7.md** — :96 "365-degree cameras" → 360; :54 "Primarily low-empathy individuals" labels people, not incentives; :50 "demographic lines of empathy" doesn't parse; :70–92 sustained uncontracted Jahoda/Keynes drift; :86 "Behavioral economists Sendhil Mullainathan" (one person).
- **10-chapter8.md** — :228–242 the chapter closes twice: false ending at "Let's get to work," then a second complete essay (Relational Autonomy, :246–346) with its own sections and the real handoff; visible merge seam (curly-apostrophe cluster :248–339 marks the paste). :272–274 "drops exponentially" vs E ∝ 1/N (inverse-linear); :94–100 vs :260–264 E_maintenance defined twice with different meanings; "we must / Do not" drift through the second essay.
- **11-chapter9.md** — :100 'Shouse (Shed House)' contradicts ch13:56 'Shop-House'; :93 "ruin the lives of the subsequent council" garbled; :22 broom timeline conflict (ch7: ~5 weeks by September; ch8: 5 months by November; ch9 says "two months" in January — should be ~5 months); :122–156 uncontracted drift.
- **12-chapter10.md** — :190–197 the taught Judo example is a manufactured conspiracy-outrage frame with an invented grandfather, contradicting :48's own "The cargo has to be true"; rebuild on a true hook. :48 narrative explains its own moral; :170 "We are not passivists." reads as a typo for pacifists; :160 "millions of joules" per page is ~3 orders of magnitude high.
- **13-chapter11.md** — :301–305 closer hands off to soil/seed trays but the next chapter is Land (old-order fossil); :74–76 panopticon rant register plus state/corporate mismatch; :250,:296 "a Autonomous/a autonomous"; :60,:84,:94 uncontracted drift.
- **14-chapter12.md** — :95 spray-foam "Chapter 5" → Ch13; :174 "autonomous, autonomous" doubled; :152 vs :160 15,000 kcal vs 5 kg incoherent; :214,:222 profanity in headings; :170–236 whole-book capstone sits mid-Part III.
- **15-chapter13.md** — :70–72 penal-colony escalation still stands (the VOICE-GUIDE's flagged passage, half-fixed); :20 vs :108 forty thousand pounds vs its own load calc (~33k loaded, ~17k empty); :59 vs :96 permitting stance contradiction (engage vs evade); :86 "absolute, raving mad" garble.
- **16-chapter14.md** — :8 doubled quotes in epigraph; :56 tense mismatch.
- **17-chapter15.md** — :58 "independent wealth funds" → sovereign wealth funds (sweep casualty); :100–101 religious/educational tax-shield advice is legally reckless, and the "Starving the Beast" title; :108,:135 "independent" as identity ("The Independent Seed Bank" → Community).
- **18-chapter16.md** — :62 "we are going to talk about" drift; :107 EXIF "hidden files" wrong; :120 "we fallback" → fall back; :128 "completely immune" absolute. (:156/:158 "79 pages" — RESOLVED: Appendix B correction of record sources it to the LoC collation; no change needed.)
- **19-chapter17.md** — :52 "late twenty-first century" timeline slip → early; :90 "a elevated"; :111 lead-acid "decades" wrong spec; :132 PET → PETG materials error; :149 "completely impenetrable" absolute; :153 "doomers never" name-calling; :129 vs :155 RepRap rule vs Bambu A1 hero contradiction.
- **20-chapter18.md** — :60 "Google producing synthetic neurons" unverifiable; :66 "exactly five" vs item 5 "Unknown Anomaly"; :71,:102 "Primate Backlash" condescension; :92 "you are failing" at the reader; :100 "Abundance Quotient" second metric coined once; :114 "mechanical transducers" jargon-nothing.
- **21-conclusion.md** — :63 "Stop parroting the cowards" double violation; :71 "capitalist goblins" name-calling; :27 Sunday→Thursday is four days, not three.
- **22-appendix-a.md** — :4 "designed to... ever serve" absolutes plus intent; :74–79 Section 6 non-cooperation with taxation reads as nullification (drop "tax"); :52–54 broken list structure; :86 garbled placeholders; :25 40% over-attributed to "corporate distribution".
- **24-appendix-c.md** — :7 "Nobody agrees on one" kill-list word.
- **26-appendix-e.md** — :75 "ten of thousands" typo; :34 phone-capability claim contradicts :52,:80; :21 quote without quote marks.
- **part2-divider.md:5** — "psychology of the collapse" vs part title "The Cooperative Transition" → transition.
- **part3-divider.md:5** — 2027 self-improvement stated as fact; "Most people... retreating into panic" condescension-adjacent.

## Notable NITS (selection)

- Typography: mixed curly/straight apostrophes (01, 07, 08, 09, 10 files, ch12); ellipsis style inconsistent (01 vs 00); en-dash ranges vs hyphen policy (04, 05 titles; conclusion "1995 to 2000" vs App D "1995–2000"); trailing whitespace 01:35; heading case PREFACE/INTRODUCTION vs Chapter 0; part1-divider "What is" vs book.json (change both or neither).
- Numbers to verify: enclosure "four thousand acts" (~5,200 cited); Blockbuster 9,000 stores in a 2000 scene (~7,700 then); 1970 house/income "roughly twice" (~2.7×); Moravec 1988 vs 2030–2040 attribution; "Universal Basic Computing" vs Altman's "universal basic compute"; 04:98 June 2026 Commerce directive needs a source; 06:5 Edmond de Belamy credit (Obvious collective); 15:38 eighty-pound plate stove (~250–400 lb real); 17:3 ch12-prefixed header image on ch15; 11:134 Haber-Bosch "3% of global carbon" (usually ~1.4–1.8%); 11:202 "sub-millimeter" FarmBot precision (millimeter-class); 10:206 unsourced 48-hour dopamine claim; 12:219 "cannot tax... barter" liability flag (IRS taxes barter).
- Sasson quote rendered two ways (16:88 vs :181); 05:9 Tsiolkovsky "letter" italicized as a title; 13-chapter11 Mistral → Mixtral 8x22B, broken bold :109,:115, arena.py vs crucible naming; 15-chapter13 wL²/8 labeled continuous, watts-as-energy :206, Ditra → Kerdi :220; 19-chapter17 "solder iron" ×2, 900 MHz vs 915/868 framing; 09-chapter7 Waymo table comma splices, "Safe Street Rebels" vs the singular in the cited Guardian source, "over 5,692 participants"; 12-chapter10 "Setup" as verb :176, "It is time" vs the book's "It's time" signature :229.
- Profanity budget: intro, ch2, ch5, ch12 exceed "a handful, each load-bearing"; ch18:58 "Wake the fuck up" is reader-directed (confirm sanctioned).
- POSITIVE: 11-chapter9.md:83 "Resilience, not secession." is the strongest thesis-compliant framing in Part III. The Elijah/Denny chronology otherwise reconciles cleanly to a ~2031 narrative present. Ch7's AFM/Luddite/Sousa/Petrillo history and ch9's chemistry check against the record. All cross-refs in ch7–10 verified correct against their target chapters.

## Built artifacts (audited 2026-08-16)

- **Surviving-the-Singularity-v0.7.5.pdf: CLEAN.** 293 pages, correct "v0.7.5" stamp on cover and all 293 page footers (zero 0.7.4/0.7.5.1 stamps), all 30 sections + 3 part dividers present, 279-entry PDF outline fully resolvable and monotonic, zero LaTeX/markdown leakage, zero mojibake, zero em dashes. The 4 literal `[*****]` strings are the ordinance blanks, verbatim from source.
- **Surviving-the-Singularity-v0.7.5.epub: CLEAN.** Valid EPUB (zip + mimetype + container.xml), 33 spine items = cover/title/nav + exactly the 30 source sections, 122-item manifest fully present, 34 nav links all resolve, 87/87 images present and non-zero (86 source refs + cover), zero render defects.
- **v0.7.4 pair: INTACT** (integrity-only scope).
- **Municipal-Autonomy-Code.pdf: FUNCTIONAL, ONE FLAG** — built 2026-07-04, carries 6 em dashes from a pre-sweep snapshot of Appendix A (current source has zero). Stale content, needs a rebuild at next publish.

## Image/art layer (audited 2026-08-16)

- PASS: 86/86 book markdown image refs resolve; art-catalog.json 113/113 asset paths exist; image-dimensions.json 68/68 dimensions match actual pixels (0 drift); 0 zero-byte/unreadable files; 0 empty alt text (87/87 refs, 86/86 catalog figures); 24/24 photos carry credit blocks; 0 images unreferenced-by-everything.
- SHOULD-FIX: `static/book-images/ch18-compass-map.jpg` is PNG data with a .jpg extension (wrong MIME in the built EPUB). Appendices B, C, D have no header image (every other section has one in its first 6 lines; Appendix A has only the inline redirection-matrix SVG). `manuscript/ART-CATALOG.md` aggregate counts are stale vs art-catalog.json (claims 66 figures/79 assets; JSON has 86 figure-bearing/113).
- NIT: 21 files in static/book-images/ are unreferenced by book source + catalog but ARE used by site routes and the v1 archive — cleanup candidates only if that usage is confirmed dead.

## Fact-check layer (2026-08-28) — claims verified against external sources

The v0.7.5 citation audit verified the 23 Precedent Ledger entries. This pass targets the **non-precedent** claims: loose statistics and attributions in the prose that no precedent covers. Every verdict below was reached by retrieving a source; nothing is asserted from memory. Line numbers corrected against the files (two claims were previously mis-filed to `06-chapter4.md`, which is actually "Universal and Multiverse Apex").

### Confirmed errors — a number or a name is wrong

| Where | Claim | What sources say | Fix |
|---|---|---|---|
| `04-chapter2.md:56` | "four thousand acts of Parliament" (enclosure) | UK Parliament: **over 5,200 enclosure bills, 1604–1914**, ~6.8M acres | "more than five thousand acts". If ~4,000 is meant as the 1750–1830 wave specifically, the text must say so |
| `03-chapter1.md:178` | "**Universal Basic Computing** (UBC)", attributed to Sam Altman | Altman's coinage (All-In, May 2024) is "**Universal Basic Compute**" | One word. Because Altman is named, this is a misquote, not a variant |
| `11-chapter9.md:134` | Haber-Bosch "roughly **3%** of global carbon emissions" | IEA: ammonia production ≈ **1.3%** of global energy-system CO₂. No source reaches 3%. The *entire* synthetic-N supply chain is ~2.1%, and production is only 38.8% of that | "roughly 1.3%". **The energy half of the sentence (1–2% of global energy supply) is correct** — change only the emissions figure |
| `11-chapter9.md:202` | FarmBot gantry moves with "**sub-millimeter** precision" | FarmBot publishes no sub-mm spec; its own language is millimeter accuracy, and its user forum reports **1–5 mm drift** between runs | "millimeter precision". (The NEMA 17 detail is correct) |
| `12-chapter10.md:160` | one page of slop costs "**millions of joules**" | ~500 output tokens ≈ **1,080 J**. Realistic order is **10³ J**, not 10⁶ — off by ~1000× | "on the order of a kilojoule", or drop the per-page figure and keep the aggregate framing the paragraph already uses. The argument survives on real numbers |
| `10-chapter8.md:206` | "within about **forty-eight hours** your dopamine receptors begin to up-regulate" | No literature supports receptor upregulation on that timescale, and none exists for screen abstinence at all. Volkow's PET work is the counterexample: striatal D2/D3 availability **unchanged after 9 months** of abstinence | Cut the mechanism, keep the phenomenology. Do not substitute a different timeline — the claim class is unsupported, not mis-numbered |
| `15-chapter13.md:38` | the Fisher stove as "**eighty pounds** of plate steel" | Lightest Fisher ever made (Baby Bear) is **245 lb**; Grandma Bear 406 lb. A firebrick lining alone is 40–90 lb, meeting or exceeding the stated total | "two hundred and fifty pounds" (Baby Bear) or "four hundred pounds" (Grandma Bear, the right size class for 16×40 ft) |
| `15-chapter13.md:20` vs `:108` | "**forty thousand pounds** of steel" (two 40ft high-cubes) vs the chapter's own $W_{total} = 15{,}000$ kg = **33,069 lb** for the *loaded finished dwelling* | Two empty 40ft high-cube tares = **17,200–18,520 lb**. Line 20 makes bare steel heavier than line 108's entire loaded building | Change :20 to "**eighteen thousand pounds**". Leave :108's 15,000 kg chain alone — it is internally consistent and correctly derived |
| `19-chapter17.md:111` | salvaged deep-cycle lead-acid "can keep your lights on **for decades**" | New flooded lead-acid in home storage: **5–8 years**; AGM 4–6; golf-cart cells 3–5. And the book describes *salvaged* cells, which start with life already spent | "three to eight years, depending on how hard you cycle them and how well you keep them watered", plus the salvage caveat. Overstated ~3–5× even against best-case new stock |
| `19-chapter17.md:132` | turn discarded PET bottles "directly into high-strength printing filament **(PETG)**" | Wrong polymer. PETG is glycol-**modified** PET (CHDM substitution) done during polymerization at the resin plant; it cannot be made by re-extruding bottle flake. Bottle-derived filament is **rPET** | Change "(PETG)" to "(rPET)". **The process itself is real and tested** — only the material name is wrong |
| `20-chapter18.md:60` | "We already have **Google producing synthetic neurons**… What happens when you combine them? You put a brain in a box" | Google's "synthetic neurons" (MoGen) are **computer-generated 3D geometry used as training data** for brain-map reconstruction — not physical, not biological, not hardware. Nothing about them can be combined with Cortical Labs wetware. Real *physical* artificial neurons exist, but from **USC** (diffusive memristors) and **Northwestern/Georgia Tech** (organic electrochemical), not Google | Drop the Google clause or swap in USC/Northwestern. As written the "combine them" argument loses its second leg entirely |
| `09-chapter7.md:92` | 'the "**Safe Street Rebels**"' | The group is **Safe Street Rebel**, singular — including in the slug of the Guardian piece the book itself cites as source 56 | Singular, and it stays singular even when referring to its members |
| `17-chapter15.md:58` | "**independent wealth funds**" | Not a term in the finance literature. The standard term is **sovereign wealth funds**. Confirmed a terminology-sweep casualty: the string entered at commit `5164f49` ("terminology audit fixes"), and "sovereign" survives elsewhere in the book, so no blanket ban existed | "sovereign wealth funds". The other 11 `independent <word>` hits in `book/` were checked and read as ordinary adjectival use |
| `12-chapter10.md:219` | an algorithm "cannot **tax** or regulate a local barter system operating in cash, physical silver, or real-world labor" | **Legally false.** IRS Topic 420: barter income is taxable at fair market value in the year received, and the IRS explicitly assumes no cash changes hands. Business barter → Schedule C; non-business → Schedule 1; exchanges file 1099-B. Silver adds a capital-gain event | Reframe from legality to **observability**, which is the real point: an algorithm cannot easily *see* it. As written this reads as advice to under-report income. The site `/disclaimer` covers the website, not the book, and "barter" appears exactly once in the whole book, so this sentence carries the entire treatment |

### Timing / methodology / attribution repairs

- **`04-chapter2.md:98` — the June 2026 Commerce directive is REAL and well-documented.** Commerce under Secretary Lutnick, **June 12, 2026**, required a license before transfer of Anthropic's Mythos and Fable models to any foreign person, citing a guardrail bypass yielding zero-day discovery and working exploit code. **One error: the book says the lab switched the models off "the next day"; it was the same day, June 12** — and the book's own following line, "One order. One day.", already contradicts "next day". Fix to "the same day"; consider date-stamping, since the record is public. **One sub-claim remains unverified: "within weeks, security researchers were reporting that the freely downloadable model matched the restricted one."** That is the load-bearing sentence of the passage and has no retrieved source. Verify or soften before publication. (The Chinese-lab sub-claim corroborates: GLM-5.2 from Z.ai, MIT license, June 13 2026, trained largely on Huawei Ascend silicon.)
- **`16-chapter14.md:92` — Blockbuster "nine thousand stores and sixty million customers" is attached to a year-2000 scene. 9,000 is the 2004 peak** (9,094 stores); the 2000 figure is ~7,700, and "sixty million" is also a peak-era number. **Caveat: the FY2000 10-K could not be retrieved (sec.gov 403s), so the exact 2000 count is not nailed down.** Either drop the count or confirm against the 10-K by hand. Do not leave 9,000 on a 2000 scene.
- **`08-chapter6.md:95` — the house-price argument silently mixes two different measures.** 1970 median home *value* (Census, $17,000) against 1970 median household income ($8,730) = **1.95×**, so "roughly twice" holds on that basis. But the modern "closer to six times" is a *sale-price* ratio, and 1970 sale prices give **~2.6–2.7×**. Comparing a 1970 value ratio to a present-day price ratio inflates the deterioration, and the "costs tripled" claim rides on the mismatch (2.7→6 is ~2.2×, not a tripling). Make both ends the same measure.
- **`08-chapter6.md:3,5` — every checkable Belamy fact is right** (GAN, Christie's Oct 2018, $432,500 against a $7,000–10,000 estimate, first at a major house) **but the creator is uncredited.** The work is by the Paris collective **Obvious**; the caption's Wikimedia credit line "Artificial intelligence software, Public domain" reads as though no human made it — a live liability *in a chapter about authorship*. Same caption is duplicated in `art-catalog.json` (~line 735) and must be fixed in both or they drift. (Unverified: the contested claim that the GAN code derives from Robbie Barrat's open-source model — check before adding any creator line.)
- **`11-chapter9.md:102` — CORRECT AS WRITTEN; the earlier review premise was wrong.** Borough Hall, Park Slope and Bay Ridge are the **Con Edison distribution-network names**, not a loose neighborhood list, and "distribution networks" is the precise register. No change. *(Lower-confidence side-note on the same line: "Initiated in 2015 as a collaboration between LO3 Energy, Siemens, and ConsenSys" — first transactions were April 2016 and Siemens came later via next47, so it was not a founding party.)*
- **`09-chapter7.md:82` — the LAMB-scale sentence welds two unrelated sources together, and the count is exact rather than a floor.** The "13 studies / 5,692 participants" is real and traceable (Muller & Waters 2012, Australian and German samples) — but **5,692 is an exact total, so "over 5,692" is indefensible**, and "major" is an embellishment the source does not support. Worse, **the 70% figure comes from a different study entirely**: a large-scale German survey (N=9,303) reporting ~75% of the partial correlation with health satisfaction and 68% of the effect on mental health. That paper does not reference the 13-study body at all, so the book's "13 studies… consistently proving the 70%" is a claim neither source makes. Split the sentence into its two real halves; drop "over", "major", and "consistently proving".
- **`03-chapter1.md:82` — Moravec attribution CORRECT.** Mind Children (1988) does carry the 2030 anchor; the 2040 succession framing is durably attributed to him. The hedged "somewhere around 2030 to 2040" survives.

### Appendix B entry quality (audited 2026-08-28)

Numbering re-verified by sequential scan: **all 232 entries present, no gaps.** (An earlier regex-based parse of mine reported a gap at 40 — that was a false positive caused by entry 40's own title beginning "8. ", and it is recorded here so nobody re-derives it.)

- **Two malformed entries, both raw scrapes rather than citations.** **Entry 40** is a PDF's running text, carrying its own chapter numbering and truncated mid-word: `8. Unemployment and well-being Brendan Burchell and Alex J. Wood 8.1 Introduction Research by psychologists and others has consi`. **Entry 31** is likewise scraped prose from a note.com post, truncated at "things that can be digital". Both need rewriting as proper citations.
- **Four URLs appear under two numbers each** (confirmed): Snopes Kodak [107, 223]; MIT OCW Sousa [119, 200]; Wikipedia Technological_singularity [148, 154]; LoC 2006681076 [153, 193]. The last pair may be deliberate (both cite *Common Sense*); the other three are dedup candidates.
- **Not a defect:** entries from ~148 onward are long and heavily annotated. That is the post-audit *corrections of record* style, and it is the strongest sourcing in the book. A length heuristic flags them; do not "clean" them up.

## Links

`sts.py verify --links`, re-run 2026-08-16 after a network outage killed the first attempt. **245 sources checked: 0 dead (404/410), 20 bot-blocked (403/429 — not evidence of death; spot-check by hand, do not bulk-edit Appendix B), 6 server errors (recheck later, likely transient: 2× PubMed 203, Frontiers 204, archive.org 502, web.archive.org 503, globaldialogue 500), 2 no-answer (theoffgridshop.com.au TLS alert, transformco.com cert-verify fail).** Harness verdict: Clean.

### Hand-verification of the 2 "unreachable" sources (2026-08-28) — both are harness false negatives, but one hides a real defect

Both URLs return **200** under `curl` with strict TLS verification (`ssl_verify_result 0`) and serve ~23 KB of real content. The harness's "no HTTP answer after 3 tries" is a limitation of **its own** Python TLS stack, not evidence about the sources. Do not act on that line without a hand check.

- **Source 225 (transformco.com/press-releases/pr/1882) — GOOD, no action.** Serves `Timeline: "Digital Sears" Announcements and News`, which matches what Appendix B cites it for (the 1996 informational sears.com and the 1997 Craftsman e-commerce launch).
- **Source 62 (theoffgridshop.com.au) — CONTENT DRIFT, needs repair.** Appendix B cites it as `"The Shouse" | 8kVA Inverter | 14.36kWH Battery | 8kW Solar`. The URL now serves a generic services page, `What We Install — Sigenergy, Deye, EcoFlow, Victron, Off-Grid & Hybrid`. **The cited product listing is gone, so the source no longer supports the specs it is cited for** — and `11-chapter9.md:100` leans on exactly those numbers ("8kVA to 10kVA... expandable 8kWh battery banks"). Replace with an Internet Archive snapshot of the original listing, or re-source the specs.

**Instrument limitation worth recording:** the link checker tests HTTP status only, so this entire failure class — *URL returns 200, but the page no longer says what it is cited for* — is structurally invisible to it. A green link run is not evidence that a citation still holds. Source 62 was found only because the SSL false negative forced a hand check; nothing in the harness would ever have surfaced it.

## `manuscript/` support directory (audited 2026-08-28)

Scope: 59 files. The `StS-Complete-Draft-*.md` compiled drafts are **generated outputs**, overwritten on the next build; staleness there is expected and is not a defect. Findings concern the genuine source/tracking docs only.

- **`EDITORIAL-QUEUE.md` is stale as a tracking doc.** Its "Open defects found on intake" (2026-07-26) lists three items; **two are already fixed in source and the queue never recorded it**: the Chapter 9 rounding error now correctly reads `≈ 7.03 mg/L` at :248, and the unsourced Wellington/Peninsular-army comparison is gone from `09-chapter7.md:144` (the sentence now stops at "twelve thousand soldiers sent into the disturbed counties"). A queue that reports fixed work as open is a trap for the next session.
- **Defect 1 (subtitle drift) is substantially resolved but not closed.** The actual *subtitle* is now consistent across the three surfaces that matter: `book.json`, `src/app.html`, and `BookCoverModal.svelte:101` all read "The 9 Stages of the Singularity and the Future of Earth". What remains is a lesser **marketing-descriptor** drift: `app.html` says "A field manual for staying human as AI rewrites work, money, and survival" while the landing page and five legal pages say "A practical field guide for staying human in the age of AI". One sweep, one ruling.
- **Queue header counts are stale.** It presents itself as "LATEST VERSION: v0.7.5" at 90,647 words. The open cycle is v0.7.5.1 and current book source measures **93,702 words** (content files only, excluding the meta docs).
- **`ART-CATALOG.md` aggregate counts stale** (already recorded in the image-layer section above).
- **Precedent ledger cross-check: CLEAN.** P-01..P-23 appear in `HISTORY-CASEBOOK.md`, Appendix D, and the book body with no gaps or orphans in any of the three.
- `SOURCE-OF-TRUTH-PRIMER.md` and `CHAPTER-AGENT-PRIMER.md` are current and correctly describe the `book.json`-gate model. No stale auth-system references in any hand-maintained doc (the grep hits are the ordinary word "account" in historical passages, plus compiled outputs).
