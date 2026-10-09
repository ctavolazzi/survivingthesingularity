# This directory is the book

**You are in the single source of truth.** The book is the `.md` files here, and
`book.json` decides which of them are the book and in what order.

Both halves are required:

- **`*.md`** holds the prose. One file per section.
- **`book.json`** is the manifest: which files, what order, what titles, plus the
  version, title and subtitle that become EPUB and PDF metadata.

Neither is the book on its own.

## A file in this folder is not automatically in the book

**`book.json` is the gate.** If a `.md` file here is not listed in its `sections`
array, it is not in the book, is not on the website, and is not in the EPUB or the
PDFs.

That is deliberate, and it is what lets craft documents live beside the manuscript
without leaking into it. Right now 33 `.md` files are in this directory and 30 are
in the book. The three that are not:

| File | What it is |
| --- | --- |
| `VOICE-GUIDE.md` | the voice reference. Read before writing. |
| `ELIJAH-PROTOCOL.md` | the narrative throughline spec |
| `README.md` | this file |

Check the gate rather than trusting it:

```bash
python3 scripts/sts.py book        # per-section word counts, straight from book.json
python3 scripts/sts.py verify      # math, meta, refs, precedents
```

## Everything with book text in it, except this folder, is output

| Artifact | Made by |
| --- | --- |
| The `/book` reader and `/read` | `src/lib/bookContent.js` |
| Shipping EPUB and review PDF | `scripts/build-epub.sh` |
| PLAIN and DELUXE PDFs | `scripts/build-pdf-variants.sh` |
| `manuscript/StS-Complete-Draft-*.md` | `sts.py compile` |
| `manuscript-index.json` | `sts.py id build` |

Five consumers, none of which keeps an editable copy. **Hand-editing any of them is
lost work**: the next build overwrites it. Fix the source and rebuild.

Two traps in particular:

1. **The compiled drafts in `manuscript/` look like the manuscript.** They are
   exports. Nothing reads them back.
2. **`manuscript-index.json` is a cache, not truth.** `sts.py id verify` re-parses
   the live source and checks that against itself, so it cannot tell you the index
   file on disk has gone stale. A clean `id verify` is not evidence the index is
   current.

Also not sources, despite looking like them: `src/lib/data/book-v1-archive/` and
`src/lib/data/sample.md`. Nothing imports either.

## Formatting

- Standard Markdown. HTML inline where a layout needs it.
- **Images live in `static/book-images/`** and are referenced as
  `/book-images/name.png`, not from a subdirectory of this folder.
- Internal cross-references should be pointers, not typed numbers:
  `[](sts:chapter1)` renders "Chapter 1" and follows the chapter if it is
  renumbered. `sts.py verify refs` fails the build on a pointer that lands
  nowhere. See `REFS-DESIGN.md`.

## After editing

```bash
python3 scripts/sts.py verify      # exits non-zero on a real problem
python3 scripts/sts.py id build    # refresh the block index
```

Do not run the full build ritual per change. EPUB, PDF variants and the
`static/downloads/` swap happen once, at version close. See `AUDITOR-BRIEF.md`.

## License

© 2026 Christopher Tavolazzi. All rights reserved. The text is free to read online
and may not be reproduced or distributed without permission.

---

## Voice guidance below is SUPERSEDED

> **Do not write to the guide below.** It is blog-era guidance from an earlier
> incarnation of this project: a humor quota, emoji headings, "Buckle up,
> buttercup." It contradicts the register the book actually uses now, and an agent
> following it literally writes the wrong book. `WRITING_CHECKLIST.md` was deleted
> on 2026-07-26 for exactly this reason and this is the same material.
>
> **The voice reference is [`VOICE-GUIDE.md`](VOICE-GUIDE.md)**, which is written
> against the shipped prose and quotes real lines from the book.
>
> Kept only as a record of where the project started.

### Guidelines for Writing in the Dynamic Satirical Style of Christopher Tavolazzi (superseded)

## Introduction

Christopher Tavolazzi's writing style in "Surviving the Singularity" can be described as **Dynamic Satirical Commentary**. It combines humor, satire, and direct engagement to discuss complex topics like AI and the future of humanity. To help you emulate this distinctive voice, we've outlined key motifs, norms, and structural techniques that characterize his style.

---

## 1. Tone and Voice

### Conversational and Relatable

- **Second-Person Narrative:** Address the reader directly using "you" to create intimacy.
- **Colloquial Language:** Use everyday speech and slang to make complex ideas accessible.

*Example:*
> "You're thinking, 'Sure, AI is cool and all, but will I still be able to afford my daily latte, it's the only thing I look forward to in this cold world?'"

### Witty and Humorous

- **Light-hearted Sarcasm:** Employ sarcasm to add humor without alienating the reader.
- **Playful Exaggerations:** Use hyperbole for comedic effect.

*Example:*
> "AI is like that, but on steroids, wearing a jetpack, and it's getting closer faster and faster every day."

### Satirical and Critical

- **Cultural Critique:** Use satire to comment on societal norms and future implications.
- **Irony:** Highlight contradictions to provoke thought.

*Example:*
> "As for the billionaires, well, let's just say that hoarding wealth in a post-scarcity economy might become as socially acceptable as hoarding toilet paper during a pandemic."

---

## 2. Themes and Motifs

### Technology vs. Humanity

- **Examining Impact:** Explore how technological advancements affect human lives and jobs.
- **Future Speculation:** Discuss potential scenarios in a speculative yet grounded manner.

### Adaptation and Survival

- **Navigating Change:** Emphasize the importance of adaptability in rapidly changing environments.
- **Survival Strategies:** Offer practical advice mixed with humor.

### Societal Commentary

- **Economic Shifts:** Analyze the evolution of economies in the age of AI.
- **Cultural Evolution:** Reflect on how societal values may change.

---

## 3. Structure and Organization

### Engaging Headings and Subheadings

- **Creative Titles:** Use witty, attention-grabbing headings.

*Example:*
> "The Great Job Shuffle (or How I Learned to Stop Worrying and Love the Bot)"

### Varied Paragraph Lengths

- **Short and Long Paragraphs:** Mix brief paragraphs for emphasis with longer ones for detail to maintain rhythm.

### Bullet Points and Lists

- **Breaking Down Information:** Use lists to present data, statistics, or steps clearly.

*Example:*
> Here are a few tips:
> 1. Embrace lifelong learning...
> 2. Cultivate your humanity...

### Interactive Elements

- **Questions and Prompts:** Include direct questions to encourage reflection.

*Example:*
> **What Would You Do?** You're the CEO of a mid-sized company...

---

## 4. Language and Vocabulary

### Colloquial Expressions

- **Metaphors and Similes:** Use figurative language to explain concepts.

*Example:*
> "Think less 'career ladder' and more 'career jungle gym.'"

### Pop Culture References

- **Current Trends:** Include references to modern culture for relatability.

*Example:*
> "We're a species that invented competitive hot dog eating, for crying out loud."

### Vivid Imagery

- **Descriptive Language:** Paint pictures in the reader's mind to illustrate points.

*Example:*
> "Imagine a typical work week in 2030..."

---

## 5. Humor Techniques

### Hyperbole and Exaggeration

- **Amplify for Effect:** Use overstatements to enhance humor.

*Example:*
> "AI is going to make a lot of current jobs obsolete. Possibly all of them."

### Irony and Sarcasm

- **Contrast Expectations:** Highlight the difference between expectations and reality.

*Example:*
> "Not cool, Jeff. Not cool."

### Anecdotes and Stories

- **Relatable Scenarios:** Begin sections with short stories to draw readers in.

*Example:*
> "Picture this: It's a crisp Monday morning in 2023, and John Miller is pulling into the parking lot..."

---

## 6. Sentence Construction

### Varied Sentence Lengths

- **Rhythmic Flow:** Alternate between short and long sentences to keep the reader engaged.

### Parenthetical Asides

- **Informal Interjections:** Add side comments for humor or extra information.

*Example:*
> "(That's already a thing, by the way. Look it up.)"

### Rhetorical Questions

- **Engagement Tools:** Pose questions to involve the reader in the conversation.

*Example:*
> "But wait, won't people just become lazy good-for-nothings if they don't have to work?"

---

## 7. Reader Engagement

### Direct Address

- **Building Connection:** Use "you" and "we" to foster a sense of dialogue.

### Call-to-Action Prompts

- **Encouraging Reflection:** Ask the reader to consider their own views or actions.

*Example:*
> **Pause and Reflect:** How would you feel about having multiple gigs instead of a traditional job?

### Humorous Disclaimers

- **Lightening the Mood:** Use disclaimers to add a humorous touch.

*Example:*
> (Disclaimer: The author accepts no responsibility for any existential crises triggered by this chapter.)

---

## 8. Content Balance

### Informative Yet Entertaining

- **Combining Facts and Fun:** Present data and serious topics with a humorous twist.

### Optimism with Realism

- **Hopeful Outlook:** Acknowledge challenges but highlight potential positive outcomes.

*Example:*
> "Yes, things are going to change dramatically. But humans are adaptable. We survived ice ages, plagues, and the invention of the selfie stick. We'll survive this too."

### Credibility

- **Supporting Evidence:** Reference studies and reports to add legitimacy.

*Example:*
> "A 2020 World Economic Forum report predicted that by 2025, 85 million jobs may be displaced by AI..."

---

## 9. Creating Variety and Flow

### Transition Phrases

- **Smooth Progression:** Use transitions to link ideas and guide the reader.

*Example:*
> "Now, here's where things get really interesting."

### Sentence Starters

- **Avoid Monotony:** Begin sentences differently to keep the reader's attention.

### Pacing

- **Adjusting Speed:** Use short sentences for fast-paced sections and longer ones to slow down and explain.

### Thematic Cohesion

- **Consistent Motifs:** Revisit themes throughout the text for unity.

---

## 10. Revision and Refinement

### Read Aloud

- **Flow Check:** Reading your work aloud can help identify awkward phrasing or rhythm issues.

### Seek Feedback

- **Third-Party Insights:** Get opinions from others to fine-tune humor and clarity.

### Clarity and Precision

- **Simplify Complex Ideas:** Ensure that complicated concepts are explained clearly without oversimplifying.

### Maintain Authenticity

- **Your Own Voice:** While emulating the style, infuse your unique perspective to keep the writing genuine.

---

## Conclusion

Emulating Christopher Tavolazzi's dynamic satirical style involves blending humor, direct engagement, and insightful commentary. By applying these guidelines, you can craft writing that not only entertains but also provokes thought and invites readers to explore complex topics with a smile. Remember, the key is to make your reader feel like they're part of a lively conversation, one that's as enlightening as it is enjoyable.

Happy writing, and don't forget to keep your jetpack ready, it's a wild ride into the future!
