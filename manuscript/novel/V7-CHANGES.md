# v7: what is in it and how it differs from v6

The Google Doc "StS v7 draft (Nov 26)", made 26 November 2026 at CT's request: "Please make the edits in a new v7
google doc, and then keep that separate. I want to keep working on v6 for the remainder of the duration of our
sessions, but keep v7 as a totally new, totally separate thing."

**v6 stays the book CT is editing.** New edits go into v6 (`manuscript/novel/EDITS.md`, from 172). v7 does
not follow them unless CT asks.

**26 Nov, later: the v7 changes are in v6 too.** CT: "I want the v6 that I'm reading in large print to be the most
current version." They are v6 edits 184 (first line), 185 (Dedication) and 186 (Thank You, last line). v7 itself is
unchanged and stays separate; `make_v7.py` still makes it from v6 through edit 171.

## How it was made

`manuscript/tools/edits-v7/make_v7.py` takes the v5 Doc with every suggestion accepted, applies every logged v6
edit (1 to 171, `manuscript/tools/edits-v6/ops.py`), checks them all, then applies the v7-only changes in
`manuscript/tools/edits-v7/ops_v7.py`. Read back after Drive made the Doc: its text matches the code's word for word;
56 headings, 9 subheadings, 19 pictures (made smaller to fit the Drive connector), no suggestions. The v6 edit check
shows edits 140 and 141 as partial in v7, because the Author's Note they edit is gone (change 3).

## The v7-only changes

CT (26 Nov): "About the author and author's note need to be revised to be a dedication instead of an author's note
and the about is a gratitude to the reader for their time, and a gentle request to use what they learned about the
world and themselves to do better than Elijah, but also to remember to believe in themselves. 'Recognize Your Power'
is the last final line in the entire text, at the ver very end, and at the very, very beginning."

Claude asked who the dedication is to, or whether to cut the Author's Note down to one in its own words. CT did not
say; these are drafts in v7 for him to change.

1. **The very beginning.** "Recognize Your Power" is the first line of the Doc, centered, above the title. [CT's words]
2. **Contents.** "Author's Note" becomes "Dedication", and "Thank You" is added after "Appendix".
3. **The Author's Note becomes a Dedication.** The heading "Author's Note" and the whole note are replaced by a
   heading "Dedication" and one centered line: "For the people I love who looked me in the eye like I'd finally lost
   it." [Claude's draft, made from CT's own sentence in the note: "I've watched people I love look me in the eye like
   I'd finally lost it."]
4. **Thank You, and the very end.** After the Appendix's last line, a heading "Thank You" and [Claude's draft, from
   CT's brief: gratitude for their time, do better than Elijah, believe in themselves]:

   > Thank you for your time. I know how much of it you gave me, and I don't take that lightly.
   >
   > You just spent a whole book with a man who saw it coming and still got most of it wrong. Take what you learned,
   > about the world and about yourself, and do better than Elijah did. Ask before you fix. Listen longer than feels
   > comfortable. Do one real thing before noon.
   >
   > And when it gets loud, believe in yourself. Most of what you need, you already have.

   Then the last line of the whole text, centered: "Recognize Your Power" [CT's words].

Not changed in v7: the "About the Author" page of the publication files (`publication/novel/build/book.json`), which
is outside the Doc. The Thank You section stands in for it in v7.
