# sts-bridge: read this first

The bridge is the one place that says where every copy of the novel is, which copy is the book right now, and how a chat changes the manuscript without breaking it. Any chat, on any surface, starts here.

Recorded on 2026-11-25. This page is written by `node scripts/sts-bridge.mjs export md`. Do not edit it by hand:
change `src/lib/data/novel/instances.json` or `bridge-protocol.json` and export again.

## The book right now

**StS v6 draft (Nov 25)** (a Google Doc). The book right now, and the Doc the author reads for his final edits, mostly in the large print PDF built from it. Made 25 November by manuscript/tools/edits-v6/make_v6.py: v5 with every suggestion accepted (edits 1 to 86 and the follow-ups), then edits 87 to 138 from manuscript/novel/EDITS.md, written as a .docx with the 19 pictures (made smaller to fit the Drive connector) and converted by Drive. Seven fixes from the contradictions pass were then made in it directly, on the author's word. Edits from 139 on are logged in manuscript/novel/EDITS.md, with a row in manuscript/tools/edits-v6/ops.py and a check row; they are not in this Doc until the author says so.

## Every copy of the book

| Holds | State | What | Where |
|---|---|---|---|
| 2026-11-19 | behind by 7 | The author's Doc as it stood on 19 November, with his planning notes above the novel. | FINAL StS Manuscript |
| 2026-11-19 | behind by 7 | The repository copy of that Doc. Its commit history is the version history up to 19 November. | manuscript/novel/FINAL-StS-Manuscript.md |
| final | behind by 6 | The novel alone, 20 November. The first Revised Manuscript was made from it. | Surviving the Singularity, Final Manuscript |
| v1 | behind by 5 | Contradictions fixed, the 19 picture placeholders filled, the appendix added. | Surviving the Singularity, Revised Manuscript |
| v2 | behind by 4 | The fact-checked text: 204 claims checked, 13 changed. | Surviving the Singularity, Revised Manuscript v2 |
| v2 | behind by 4 | What a reader with the private link sees. One Markdown file for each section, in the order novel.json gives, with the 19 pictures. | The private reader at /novel/<key>/ |
| v3 | behind by 3 | The book as it stood before version 4, which was made from it. It keeps its 19 pictures. Leave it as it is. | Surviving the Singularity, Revised Manuscript v3 |
| v3 | stale copy | Superseded. A copy of v3 made at 8:05 on 22 November with the 19 pictures and captions removed. It has none of the edits made to v3 after that. It was first titled Revised Manuscript v4. | OLD: v3 text-only copy from Nov 22 morning (not v4) |
| v4 | behind by 2 | The plan for version 4 and the place where sessions leave notes for the author. At the top: who is working on what, and "Waiting on you". Then the rulings ("Decided so far"), a profile for every character, the list of fixes, and four notes for every chapter. No prose. | v4 scaffold |
| v4 | behind by 2 | Version 4, kept as the safe fallback. Every line-level pass of 23 and 24 November went in here on the author's yes: the F list, the R, S, V and G check, and the P list. Left untouched once v5 was copied from it. Do not edit it. | StS Final Draft v4 Surviving the Singularity |
| v5 | behind by 1 | The book as it stood through 25 November, kept untouched. It holds the author's edits 1 to 86 as suggestions he never accepted, and none of 87 onward. v6 was made from it. Do not edit it. | StS v5 draft (Nov 23) |
| v6 | CURRENT | The book right now, and the Doc the author reads for his final edits, mostly in the large print PDF built from it. Made 25 November by manuscript/tools/edits-v6/make_v6.py: v5 with every suggestion accepted (edits 1 to 86 and the follow-ups), then edits 87 to 138 from manuscript/novel/EDITS.md, written as a .docx with the 19 pictures (made smaller to fit the Drive connector) and converted by Drive. Seven fixes from the contradictions pass were then made in it directly, on the author's word. Edits from 139 on are logged in manuscript/novel/EDITS.md, with a row in manuscript/tools/edits-v6/ops.py and a check row; they are not in this Doc until the author says so. | StS v6 draft (Nov 25) |
| v7 | next version | A separate copy, kept apart from v6 on the author's word ("keep v7 as a totally new, totally separate thing"). v6 with every logged edit through 171, plus v7-only changes: "Recognize Your Power" at the very beginning and the very end, the Author's Note turned into a Dedication, and a Thank You to the reader. v6 stays the book he is editing; v7 does not follow its new edits unless he asks. See manuscript/novel/V7-CHANGES.md. | StS v7 draft (Nov 26) |
| v3 | stale copy | Topics and entries about the people, places and things in the book. Written from v3 as it stood on the morning of 22 November. Out of date since: it still says Second Crop (now Crop Dust), and its Items entry is the Fisher woodstove, which v3 has replaced with an amp. | The compendium at /novel/<key>/compendium |

Google Docs are named by title only, because this repository is public. Search Drive for the title.

## Notes about the book

- **Surviving the Singularity: Revision Plan.** The plan v3 was made from, 21 November.
- **Surviving the Singularity: The Harshest Critics.** What hostile readers would say about v2, 21 November.
- **Surviving the Singularity, v3 Change Log.** Every change from v2 to v3, with the words before and after.
- **Surviving the Singularity, Fact-Check Log (v2).** 204 claims and their sources.
- **Surviving the Singularity, Revised Manuscript: Change Log.** Every change from the Final Manuscript to the first revision.
- **Story Map 1 to 5.** Chapter by chapter, timeline, places, factions, characters. Written against the Final Manuscript on 21 November, so later versions can disagree with them.
- **00 Summary report, and dossiers 01 to 28.** One Drive dossier for each character, checked against the Final Manuscript.
- **Surviving the Singularity, Lived Layer (Nov 22, 2026).** A new layer for 21 dossiers. Its own note says none of it is in the book yet.
- **manuscript/novel/characters/.** A folder for each of 35 characters in the repository, built from the text of 19 November. Behind v5: the Character Bible is the checked one.
- **Surviving the Singularity, Characters (Drive folder).** The summary report, 28 character dossiers and the Lived Layer. Checked against the Final Manuscript of 20 November; the v4 scaffold's Characters section is newer.
- **Surviving the Singularity, Story Map (Drive folder).** Story Maps 1 to 5: contradictions, chapter by chapter, timeline and places, characters. Written 20 to 21 November.
- **Surviving the Singularity, Revision Notes (Drive folder).** The Revision Plan, the Harshest Critics, and the v3 Change Log, which ends with the November 22 passes. Since 24 November it also holds the Character Bible, the Story Structure and Character Arcs, and the StS Canon and Change Record.
- **Surviving the Singularity, Revised Manuscript v3 (compressed).pdf.** A PDF of v3 made early on 22 November, before that day's edits.
- **StS Preorders and Discount Codes (from Supabase, 2026-11-22).** A spreadsheet another session made on 22 November. It holds customer data, so it is listed by title only and was not opened.
- **StS v4 Chapter Arcs.** A story arc for each of the 46 sections, and the new chapter titles, written from version 4 by another session. Claude Code checked its 426 quotations against version 4: 6 are not word for word. The instructions it followed are in the Doc "Claude Code prompt: v4 chapter arcs and chapter titles" and on the branch novel/v4-arcs-titles-prompt.
- **OLD: V3 to V4 Readiness Audit (made without seeing the book; see the Editor's Letter).** Made by a tool that could not see the book. It contains nothing about the text. Replaced by the Editor's Letter.
- **StS v4: Editor's Letter and Readiness Audit (Nov 23).** The editorial read of version 4, 23 November: answers on arcs, sentences and voice, ten calls for the author, small continuity questions, notes for the Amazon file, and a punch list for all 46 sections. Its 124 quoted lines were checked against version 4.
- **StS workboard: who is doing what.** A Drive copy of manuscript/novel/WORKBOARD.md for chats that cannot read GitHub, remade on 24 November. Whoever changes the workboard remakes this copy.
- **StS v4 final edits, Nov 23 (Drive folder).** The Change log, the Scene pass and the Editing method from the final editing night. The Change log's last section, "v5 changes", logs changes made to v5 since 24 November, with the words before and after. It does not have the final edit made later that day; that is in section 9 of the process file. The process is recorded in manuscript/NOVEL-PROCESS-2026-11-23.md.
- **StS Canon and Change Record.** One entry for each decision the author makes about the book: the date, his words, and every file and place it changed. Started 24 November. In the Revision Notes folder. Repository copy: manuscript/NOVEL-CANON-AND-CHANGE-RECORD.md. It does not list the final edit of 24 November, which is in manuscript/NOVEL-PROCESS-2026-11-23.md, section 9.
- **Surviving the Singularity: Character Bible.** For each character: core motivation (marked as the author's call or proposed), backstory checked against v5, 2026 voice with real v5 lines, and flags where older notes disagree with v5. Complete as of 24 November: 27 entries (Elijah, Grace, Lou, Marta, David, Ma, the co-op table and the people outside it) and a list of minor characters, checked against v5 as it stood after the final edit. In the Revision Notes folder. Repository copy, the same text: manuscript/NOVEL-CHARACTER-BIBLE-2026-11-23.md. A Claude Doc with the same title is on claude.ai; it was not updated on 24 November.
- **Surviving the Singularity: Story Structure and Character Arcs.** The four-act structure of v5 and the arc of each main character, written from v5 on 23 November. In the Revision Notes folder. Repository copy: the file in manuscript/ whose name starts NOVEL-STORY-STRUCTURE (23 November). A Claude Doc with the same title is on claude.ai.
- **manuscript/tools/final-check/.** The checker and its self-test from the final edit of 24 November, the list of that session's edits, and the scripts that built the Character Bible entries. The README there says what each check proves and what it cannot.

## How to change the manuscript

1. Check the workboard before you start (manuscript/novel/WORKBOARD.md, or the block "Who is working on what" at the top of the v4 scaffold), and claim your task there. Two sessions started the same job on 22 November without knowing.
2. Find the current manuscript. Exactly one copy in the map is marked CURRENT. Edit that one and no other.
3. Read it fresh, right before the edit. The author and other chats type in it while you work, so a read from ten minutes ago is out of date.
4. Make the change as a suggestion, so the author can accept or reject it. Make a direct edit only when he has said so, in so many words, in this conversation.
5. Change words by exact match, never by position. Pick a short plain passage that appears exactly once in the whole Doc, and replace it.
6. Keep the match short. A suggestion deletes the matched words and types them again, which drops italics and links on them.
7. Read the Doc again. Confirm your suggestion is there and that nothing else moved.
8. Tell the author what you changed in a few plain lines, with the chapter.
9. If the change settles a fact (a name, a distance, who knows what), write it in that character's notes file and under "Decided so far" in the v4 scaffold.
10. If you make a new copy or a new version, add it to the map: instances.json in the repository, and the bridge page in Google Drive.

## House rules

- No em dashes or en dashes anywhere in the book or in notes about it.
- When the author dictates lines, use his words. Fix typos and change nothing else.
- The book has no pictures (the author cut them). The Google Docs still hold 19 old ones; the build leaves them out. Do not put pictures in the book.
- The book never says who Bidwell's watcher is. No edit may clear anyone of being that person.
- The author's personal journal material stays out of every file.
- Pushing to main on GitHub redeploys the live site. Do it only when he says.
- Reply to the author in a few short plain lines. Lead with what happened.

## If your chat can run code

```bash
node scripts/sts-bridge.mjs status              every copy, and which one is the book right now
node scripts/sts-bridge.mjs check               is the map sound
node scripts/sts-bridge.mjs where <name>        an entry, a chapter (chapter-9), or a copy (site-reader)
node scripts/sts-bridge.mjs edit READ.json --find "old words" --replace "new words"     checks the change and prints the request to send
node scripts/sts-bridge.mjs suggestions READ.json     the suggestions waiting in the Doc, by chapter
node scripts/sts-bridge.mjs verify READ.json --replace "new words"     after sending: is it there
```

`READ.json` is the saved result of the Docs connector's `read_doc` on the current manuscript. The
script never calls Google and never writes to the Doc. It checks your change and prints the request
for the connector's `update_doc`.

## If your chat cannot run code

1. Open the bridge page in Google Drive (search Drive for "sts-bridge"). It lists every copy with a link and marks the current one.
2. Read the current manuscript with the Docs connector.
3. Count how many times your passage appears. If it is not exactly once, lengthen it until it is.
4. Send one replaceAllText request with writeControl.writeMode set to SUGGEST and matchCase true.
5. Read the Doc again and find your suggestion.

```json
{
  "documentId": "<the current manuscript's id>",
  "writeControl": {
    "writeMode": "SUGGEST"
  },
  "requests": [
    {
      "replaceAllText": {
        "containsText": {
          "text": "old words, appearing once",
          "matchCase": true
        },
        "replaceText": "new words"
      }
    }
  ]
}
```

