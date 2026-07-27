# `sts refs`: the reverse index

**Status: DESIGN. Nothing below is built** except the two pieces noted as done.
Written 2026-07-26 against `sts.py` at `18b7126`.

The question this has to answer is one sentence long:

> What breaks if I cut this block?

Today nothing can answer it. `verify precedents` checks presence and absence,
`art list` links figures to the catalog, and `refs list` reads `sts:` pointers
backwards. None of those is a general reverse index, and the first two only
cover their own narrow kind.

---

## What the reference graph actually looks like

Measured 2026-07-26, not estimated. Counts are occurrences across
`src/lib/data/book/*.md`.

| Kind | Count | Machine-checkable today |
|---|---:|---|
| Precedent mentions `P-NN` | 98 | partly (`verify precedents`) |
| ...of which own a `## Precedent P-NN:` heading | 22 | yes |
| ...so genuine cross-references to a precedent | **76** | **no** |
| Figures | 84 | yes, via `art_id` in the index |
| Prose "Chapter N" | 103 | **no** |
| Prose "Appendix X" | 6 | **no** |
| Prose "Table N" | 3 | **no** |
| `sts:` pointers | 0 | yes (new, unadopted) |
| Footnotes `[^n]` | 0 | n/a |

Roughly **270 reference edges**, of which 84 are checked. The 76 precedent
cross-references and the 103 chapter mentions are the exposure: they are prose,
they are load-bearing, and nothing notices when they go wrong.

The Chapter 8 deduplication in `V0.7.3-SCOPE.md` is exactly this problem in the
field. Its work order had to be written by hand, and it carries a manual
constraint ("all seven `ch08-*.svg` figures must survive") precisely because no
tool could produce that list.

---

## The decision asked for: the two-path scheme

Wagtail's `reference_index.py` stores two paths per reference, and the split is
the whole insight. Porting it:

**`model_path`, the structural path.** Where a block sits in the *shape* of the
book, carrying no instance identity. A type chain:

```
chapter.figure.caption          a caption belonging to a figure in a chapter
chapter.precedent.heading       a precedent's own heading
appendix.list.source            a works-cited entry
chapter.paragraph               ordinary prose
part.heading                    a part divider's title
```

Answers questions of the form *every X of kind Y*: "every caption citing
Wikimedia", "every precedent heading", "every figure with no caption under it".
These are the queries that let a rule be enforced across the whole book instead
of spot-checked.

**`content_path`, the instance path.** The same location with each repeatable
level resolved to its id:

```
chapter8.figure[ch08-firewall-pipeline].caption
chapter14.precedent[P-16]
appendix-b.source[42]
chapter8.b0117
```

Answers *which one*, and jumps straight to it.

**The StS index already has the instance half and is missing the structural
half.** `manuscript-index.json` gives every block an id, a type, and a line
span, which is `content_path` in all but name. What it has no notion of is
*role*: it knows a block is a `paragraph`, not that it is the caption of a
figure that carries an art-catalog id, nor that it sits under a `## Precedent`
heading. `_md_blocks` already infers one such role (`caption`, from a single
italic paragraph following a figure), which is the seed of the structural layer
and proof the inference is cheap.

**Ruling: derive `model_path` at index time, from three inputs already present.**

1. **Section role**, from `book.json` order and id: `front`, `part`, `chapter`,
   `appendix`, `conclusion`.
2. **Heading ancestry**, from the `##`/`###` levels already recorded on heading
   blocks. Every non-heading block inherits the nearest heading above it.
3. **Semantic role**, from the pattern rules already in `_classify` plus the
   `## Precedent P-NN:` form `verify_precedents` matches.

No new source markup. No anchors in the `.md`. That constraint holds, which is
the only reason this is cheap.

---

## `describe_on_delete()` returns prose, not a count

`reference_index.py:862` is the other half worth copying deliberately. It does
not return "3 references". It returns sentences: "prevents deletion", "the
caption will also be deleted."

That difference decides whether the tool gets used. A count is a number someone
overrides. A sentence is a consequence someone reads.

Target output:

```
$ sts refs --to sts.chapter8.b0117

sts.chapter8.b0117  figure  10-chapter8.md:232  ch08-firewall-pipeline

  BLOCKS DELETION
    art-catalog id sts.diagram.ch08-firewall-pipeline has no other placement.
    Cutting this block orphans a cataloged asset.

  CASCADES
    The caption below it (b0118) belongs to this figure and will be
    left dangling.

  REFERRED TO BY
    Nothing points at this block by id.
```

and for a block that is safe:

```
$ sts refs --to sts.chapter8.b0091

sts.chapter8.b0091  paragraph  10-chapter8.md:171

  Nothing references this block. Safe to cut.
```

The three verdict classes are `BLOCKS DELETION` (cutting breaks a check that
currently passes), `CASCADES` (something else is structurally attached), and
`REFERRED TO BY` (someone points here but survives the loss). Anything with no
verdict prints the one-line safe case, because a tool that is silent when the
answer is "go ahead" is a tool people run.

---

## Schema

A sidecar, beside `manuscript-index.json`, same rules: generated, never
hand-edited, never mutates `.md`.

```jsonc
{
  "schema": "sts-reference-index/v1",
  "edges": [
    {
      "from_block":   "sts.chapter17.b0042",
      "from_path":    "chapter.paragraph",              // model_path
      "from_content": "chapter17.b0042",                // content_path
      "to_kind":      "precedent",                      // precedent|figure|section|art|source|block
      "to":           "P-16",
      "to_block":     "sts.chapter14.b0031",            // null if unresolvable
      "relation":     "cites",                          // cites|captions|places|indexes
      "detected":     "prose"                           // prose|pointer|structural
    }
  ]
}
```

`detected` is the field that earns its place. A `pointer` edge is exact, the
author wrote `sts:`. A `prose` edge is inferred from text like "Chapter 17" and
is a **guess**. Mixing those two silently would be the same mistake the pass-2
reconcile warning just fixed: presenting an inference with the same confidence
as a fact. Prose edges must be labelled as inferred everywhere they surface.

---

## Command surface

```bash
sts refs --to <id>          # the deletion-safety question. The reason this exists.
sts refs --from <id>        # what this block points at
sts refs --path <pattern>   # structural query: 'chapter.figure.caption'
sts refs build              # regenerate the sidecar
sts refs list               # existing: sts: pointer edges (DONE)
sts refs list --to <id>     # existing: those edges backwards (DONE)
```

`verify refs` already fails on a dangling `sts:` pointer. It should **not** fail
on a stale prose edge, because prose edges are inferred and a build that fails
on a guess trains people to ignore it. Prose findings belong in `sts refs`
output and in a `verify` note, not in the exit code.

---

## Build order

1. **Structural paths into the index.** Section role, heading ancestry,
   semantic role. Verifiable on its own: `sts id list --path chapter.figure`
   should return 84 figures without any edge table existing yet.
2. **Structural edges.** Figure to caption, figure to art-catalog, precedent
   heading to Appendix D. All exact, no inference. This alone answers the
   Chapter 8 figure constraint.
3. **Prose edges,** clearly marked as inferred. `P-NN` first, since the form is
   unambiguous. "Chapter N" second.
4. **`describe_on_delete`.** Only after 1 to 3, because the prose quality is the
   deliverable and it needs real edges to describe.

Stop after 2 if the value is not obvious. Steps 1 and 2 are exact and cheap;
step 3 is inference and carries a false-positive budget that has to be paid for
with tuning.

---

## Not doing

**Per-block revision history** (the fourth idea, parked). Still parked. It needs
an append-only log keyed on block id at every `id build`, and `id build` is not
yet trustworthy enough to be a historical record: it just started reporting that
it carries some ids by position rather than by content. Logging a positional
guess as "this paragraph evolved" would manufacture a history that did not
happen. Revisit once the positional count is routinely zero.

**Adopting Wagtail.** Settled and closed. See the 2026-07-26 analysis: Django,
Postgres, an always-on host, and it wants to own the page tree. If browser
editing ever becomes the real requirement, look at Decap or Tina, which sit on
git-backed markdown.
