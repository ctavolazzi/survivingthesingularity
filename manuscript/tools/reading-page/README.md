# The reading page

One HTML page that puts the novel notes in `manuscript/` into a form CT can read on a phone:
the cast, the two maps, the scene draft, the beats, the shape of the book, the audit.

It is built from these files and nothing else:

| Tab | Built from |
|---|---|
| People, Rhymes, Method | `NOVEL-CHARACTER-PROFILES-2026-11-18.md` |
| Map | `NOVEL-MAP-EVERYONE-2026-11-19.md` and `NOVEL-MAP-ELIJAH-2026-11-19.md` |
| Drive | `NOVEL-DRIVE-FINDINGS-2026-11-19.md` |
| Scene | `drafts/draft-elijah-crash-out-arc.md` |
| Beats | `NOVEL-BEATS-2026-11-19.md` |
| Shape | `NOVEL-STRUCTURE-2026-11-19.md` (the chart is drawn from its chapter table) |
| Arcs | `NOVEL-CHARACTER-ARCS-2026-11-18.md` |
| Fixes | `NOVEL-CONSISTENCY-AUDIT-2026-11-18.md` |

So the way to change the page is to change the Markdown and build again.

## Build

```bash
pip install markdown
python3 manuscript/tools/reading-page/build_page.py /path/to/singularity-cast-bible.html
```

With no argument it writes `singularity-cast-bible.html` beside the script. That file is ignored
by git.

## Check

```bash
node manuscript/tools/reading-page/check.cjs /path/to/singularity-cast-bible.html /path/to/folder light
```

It opens the page at phone width, prints the overflow and any map text that runs past its box,
and saves a picture of each map. Run it once with `light` and once with `dark`.

## Publish

The page is a private Artifact on claude.ai titled "Singularity Cast Bible". To update it from a
new chat: read the artifact first with the Artifact tool, then publish the built file to the
same URL. Publishing without the URL makes a second page. CT has the link.

## The files

- `build_page.py` reads the Markdown and writes the page.
- `map_svg.py` draws one person's map from a file shaped like `NOVEL-MAP-ELIJAH-2026-11-19.md`.
- `bigmap.py` draws the map of everyone from `NOVEL-MAP-EVERYONE-2026-11-19.md`.
- `page.css` and `page.js` are the page's style and its tabs.

## How the maps parse their files

Both drawings are made from the text, so the text has to keep its shape.

- **Elijah's map:** a line starting `**He wants:**`, a line starting `**He is afraid of:**`, one
  table with seven columns, and a paragraph starting `**Where he ends, <chapters>:**`. The sixth
  column is `Yes`, `Half` or `No`.
- **The big map:** `## Elijah | <when> | <Yes, Half, No or Ends>` followed by one sentence, and
  `### <Name> | <when> | <Yes, Half, No, Open or None>` followed by bullets named `To Elijah`,
  `Wants`, `Tries`, `Stopped by`, `So` and `Ends`. A bullet left out is not drawn.
