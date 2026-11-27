#!/usr/bin/env python3
"""Who knows what, and when: the knowledge sheet, built from lines in the book.

    python3 manuscript/tools/edits-v6/knowledge.py OUT/v6.txt OUTDIR [--date 2026-11-27]

FACTS below is the only thing written by hand. A fact is something at least one person in the book does
not know or gets wrong. Each event is (who, state, quote, options): the quote is the exact line where the
page shows that person knowing (K), suspecting or half knowing (S), or believing something false (F).
The script finds every quote in the built book, reads its chapter off the page, and writes three files:

  knowledge-sheet-DATE.csv     one row per fact, one column per person: the chapter(s) and state
  knowledge-flags-DATE.csv     the same as flags: K, S or F for each person at the end of each phase
  knowledge-evidence-DATE.csv  one row per event, with the chapter, the line number and the quote

A quote that is not in the book stops the run, so a rewrite that removes a line shows up here.
An empty cell means the page never shows that person knowing. It does not mean they never find out.

Options: nth (which occurrence, from 1), as_of ("Chapter 23": they knew from then, off the page; the quote
is where the page tells us), before (True: knew before the book starts), note (a few words), exclude (for
"Table": people who were not there). "Table" means everyone at the co-op at that moment; it fills the
co-op columns that have nothing earlier. The Reader column is the first place the page shows the fact.

Written in the smell chat, 27 Nov 2026, at CT's request ("key bits of information logged in a spreadsheet,
and then having flags indicating which characters know them at what time").
"""
import csv
import os
import re
import sys

COOP = ["Grace", "Lou", "Marta", "Curtis", "Priya", "Tyler", "Denny", "Reuben"]
PEOPLE = ["Elijah"] + COOP + ["Rest of the table", "Patricia", "David", "Devendra", "Bidwell", "Others", "Reader"]
PHASES = [  # name, first heading of the phase
    ("The Bar (Ch 0 to 5)", "Chapter 0:"),
    ("The City (Ch 6 to 15)", "Chapter 6:"),
    ("Farm, 2025 (Ch 16 to 25)", "Chapter 16:"),
    ("Farm, 2026 (Ch 26 to 28)", "Chapter 26:"),
    ("Early 2027 (Ch 29 to 33)", "Chapter 29:"),
    ("Fall 2027 (Ch 34 to 36)", "Chapter 34:"),
    ("The end (Ch 37 on)", "Chapter 37:"),
]

E = lambda who, state, quote, **o: (who, state, quote, o)

FACTS = [
    # ---- the arms, and what Elijah has or had
    ("A1", "The arms", "Elijah owns two industrial robot arms", [
        E("Others", "K", "we got two spare robot arms with your name on", note="Trent; Gus hauled them"),
        E("Elijah", "K", "The two spare arms were still sitting on the cannery dock in their crates"),
        E("Grace", "K", "Your arms can live there for free while you figure it out.", note="she saw his post"),
        E("Lou", "K", '"Grace says your arms went at a lien sale," Lou said.'),
        E("Table", "K", "No, like robot arms. Two of them, off a cannery line in Stockton."),
    ]),
    ("A2", "The arms", "The arms were never sold. They are in Richard Praether's pole barn", [
        E("Grace", "F", "He told her they were gone.", note="believes they went at a lien sale"),
        E("Tyler", "S", "Or old Praether, out past the grange.", note="sent him there for 'a couple of big crates'; never told what was in them"),
        E("Others", "K", "Lou here tells me you want to store some robot arms out in my old barn", note="Praether"),
        E("Elijah", "K", "The arms arrived on time. Elijah canceled the storage unit, and Lou helped him put the arms in the barn."),
        E("Lou", "K", "Lou had the first crate up on the forks"),
        E("Table", "K", "They're in Richard Praether's pole barn, out past the grange."),
        E("Grace", "K", "You've kept the arms from me this whole time?"),
    ]),
    ("A3", "The arms", "Lou told Elijah to keep the arms secret, from Grace most of all", [
        E("Elijah", "K", '"Don\'t tell anybody you have these."'),
        E("Lou", "K", '"Don\'t tell anybody you have these."'),
        E("Table", "K", "I told our friend Elijah to keep the arms a secret."),
    ]),
    ("A4", "The arms", "Lou paid what Elijah owed on the storage unit", [
        E("Elijah", "K", "He said he would cover what Elijah owed on the unit, and that it stayed between the two of them."),
        E("Lou", "K", "He said he would cover what Elijah owed on the unit, and that it stayed between the two of them."),
    ]),
    ("A5", "The arms", "Elijah tried to sell the arms and nobody would buy them", [
        E("Elijah", "K", "A week went by. No bids."),
    ]),
    ("A6", "His money", "Ruby offered him a million dollars to do nothing, and he said no", [
        E("Elijah", "K", '"The full million?"'),
        E("Others", "K", '"He offered me a job," Elijah said. "Ruby. For doing nothing. A million dollars."', note="Gus"),
        E("Grace", "S", "Elijah, do you personally know a billionaire?", note="asks; he never answers (edit 237)"),
    ]),
    ("A7", "His money", "The farm money sits in an account with his name on it; he treats it as Ma's and takes none", [
        E("Elijah", "K", "The money went into an account that said Linda Madrone across the top, with his name under hers"),
        E("Others", "F", "How much money did you keep, you greedy little piece of shit?", note="Melody believes he kept it"),
    ]),
    ("A8", "His money", "He has never cashed the co-op's pay checks", [
        E("Elijah", "K", "Elijah put it in the back of a notebook and did not cash it."),
        E("Grace", "K", "Those come out of the same account."),
    ]),
    # ---- the board
    ("B1", "The board", "The board in the boxes was laid out by an AI company in Iowa, not by Elijah", [
        E("Elijah", "K", "He didn't mention Iowa."),
        E("Marta", "F", '"Now that\'s ours," she said.', note="believes he drew it"),
        E("Tyler", "K", "Your board's from Iowa, man. It says so in the file."),
        E("Table", "K", "I gave it to a company in Iowa, and their machine did it in two nights, and I never told you."),
        E("Patricia", "K", "It was the board, and Elijah's the one who had it made."),
    ]),
    ("B2", "The board", "The Iowa layout is what cooked the Ochoas' plugs; Elijah saw it that night and said 'check the battery'", [
        E("Patricia", "F", '"It\'s the code," Patricia said.', note="blames Tyler's code"),
        E("Elijah", "K", "right where the Iowa company's machine had put it."),
        E("Tyler", "S", "straight at Elijah."),
        E("Table", "K", "I saw it the night they cooked."),
        E("Patricia", "K", "It was the board, and Elijah's the one who had it made."),
    ]),
    ("B3", "The board", "Tyler's firmware was written by an AI (Rod Code)", [
        E("Tyler", "K", '"I used Rod Code."'),
        E("Table", "K", '"I used Rod Code."'),
        E("Patricia", "K", '"I used Rod Code."'),
        E("Elijah", "K", '"I used Rod Code."'),
    ]),
    # ---- home
    ("C1", "Ma's farm", "Elijah signed away his mother's farm", [
        E("Elijah", "K", "Elijah signed where the yellow tabs were"),
        E("David", "K", '"Heard they close Friday," David said'),
        E("Others", "K", '"You sold the fucking farm?"', note="Melody; the town knows too (Pruitt, Ch 13)"),
        E("Grace", "K", "I'd have signed in the parking lot."),
        E("Reuben", "K", '"I checked it that week," Reuben said.', as_of="Chapter 23"),
        E("Table", "K", "I sold it to them. My mother's place."),
    ]),
    ("C2", "Ma's farm", "The buyer was the same outfit that is buying the land around the co-op", [
        E("Elijah", "S", "It was the same people who had bought the Hollis place.", note="knows only that they bought the Hollis place"),
        E("Elijah", "K", "He had sold them Ma's kitchen."),
        E("Bidwell", "K", "I have the dairy down south."),
        E("Reuben", "K", "I've had this a year and a half.", as_of="Chapter 23"),
        E("Table", "K", "I sold it to them. My mother's place."),
    ]),
    ("C3", "Ma's farm", "Devendra pushed Ma's farm to the top so the offer would beat the bank's sale", [
        E("Devendra", "K", "Your mother's place came across my screen eighteen days before you found the paper on her door.", as_of="Chapter 13"),
        E("Elijah", "K", "Your mother's place came across my screen eighteen days before you found the paper on her door."),
    ]),
    ("C4", "Ma's farm", "Ma's house payments went to survival food she bought because of his video", [
        E("Elijah", "K", "that was where the payment on the place had gone since the new year."),
        E("Grace", "K", "A coffee can of order slips, in the barn."),
    ]),
    ("C5", "Ma", "Barry is real: Barry Whitlow, Ma's boyfriend before his father", [
        E("Elijah", "F", '"There isn\'t any Barry."', note="believes there is no Barry"),
        E("Others", "K", "She asked Dad the first week and he about fell off the chair.", as_of="Chapter 15", note="Ray McGrath"),
        E("David", "K", "Barry Whitlow. Pitched for Analy.", note="when he learned it is not on the page"),
        E("Elijah", "K", "Barry Whitlow. Pitched for Analy."),
    ]),
    ("C6", "Ma", "Ray McGrath, and then David, sat with Ma every Sunday", [
        E("Others", "K", "Before that the hand changed. R. McGrath.", as_of="Chapter 15", note="Ray"),
        E("David", "K", "D. McGrath, 10:15.", as_of="Chapter 22", note="after his father died"),
        E("Elijah", "F", "He took it to mean the church.", nth=1, note="takes 'her Sunday company' for the church"),
        E("Elijah", "K", "D. McGrath, 10:15."),
    ]),
    ("C7", "Ma", "Melody visits Ma", [
        E("Elijah", "K", "M. Madrone, in round, careful letters."),
    ]),
    ("C8", "The Bear Flag", "The three people the realtors let go are fine", [
        E("Elijah", "F", "The night Elijah Madrone ended three careers", note="believes he ended three careers"),
        E("Grace", "F", "He told her about the laptop and the napkin", note="has only his telling: 'You could find out'"),
        E("Marta", "F", "Grace told me your bar story.", note="has only his telling: 'Go find out if they ate'"),
        E("David", "K", "They're fine. They were fine by that spring.", note="when he learned it is not on the page"),
        E("Elijah", "K", "They're fine. They were fine by that spring."),
    ]),
    ("C9", "His things", "He pawned the Telecaster and lost it", [
        E("Elijah", "K", "By the time he remembered, his Telecaster was in the window on Fourth Street."),
        E("Others", "K", "I hocked it in Santa Rosa and never went back.", note="Wes; in Ch 17 he hides the ticket from Grace"),
    ]),
    # ---- between people
    ("D1", "Grace and Elijah", "'You're just the lamp': what he said to her during the tea", [
        E("Grace", "K", '"You\'re just the lamp."'),
        E("Elijah", "F", "He would never remember it.", note="does not remember; she tells him 'Nothing that mattered'"),
        E("Elijah", "K", "You called me the lamp. Did you know that?"),
    ]),
    ("D2", "Grace and Elijah", "Grace's gate: the man who would not leave before the fire, and what the orange tape means", [
        E("Grace", "K", "That's what the tape is. Somebody checked.", before=True),
        E("Elijah", "K", "That's what the tape is. Somebody checked."),
    ]),
    ("D3", "Grace and Elijah", "Grace's father is lost to her (drink, then worse, then a man on a phone)", [
        E("Grace", "K", "He started drinking when I was in high school.", before=True),
        E("Elijah", "K", "He started drinking when I was in high school."),
    ]),
    ("D4", "Grace and Elijah", "Elijah loves her and has never said it; the note in the amp", [
        E("Elijah", "K", "He loved her. He had not said it to her yet"),
        E("Grace", "K", "It said I love you too, in his handwriting"),
    ]),
    ("D5", "Marta", "Marta's cousin Emeka died in a press she had walked him to", [
        E("Marta", "K", '"I had a cousin. Emeka.', before=True),
        E("Elijah", "K", '"I had a cousin. Emeka.'),
    ]),
    ("D6", "Marta", "Marta's shoulder is finished: about two years of overhead welding left", [
        E("Elijah", "S", "Tuesdays, for the shoulder she never mentioned.", note="saw the therapy schedule in the journal"),
        E("Others", "K", '"That\'s your rotator cuff," Yvonne said.', note="Yvonne and the women in the grange kitchen"),
        E("Table", "K", '"Shoulder\'s done," she said.'),
    ]),
    ("D7", "The table", "Before Elijah came, the table had agreed on what he was for", [
        E("Curtis", "K", "The dude's got the gift for gab. I thought we agreed."),
        E("Grace", "K", "The dude's got the gift for gab. I thought we agreed."),
        E("Elijah", "S", "Agreed on what?", note="never answered on the page"),
    ]),
    ("D10", "Lou", "Lou asked Grace to write to Elijah in the first place", [
        E("Lou", "K", "But there's a reason why I asked you to reach out to him.", as_of="Chapter 15"),
        E("Grace", "K", "But there's a reason why I asked you to reach out to him.", as_of="Chapter 15"),
    ]),
    ("D8", "The table", "The April payment to Irene came up short, and Grace sat on it for a week", [
        E("Reuben", "K", '"Give me a week," Grace said.'),
        E("Grace", "K", '"Give me a week," Grace said.'),
        E("Others", "K", "Irene told her to pay it when she could, honey", note="Irene"),
        E("Elijah", "K", '"Tell Reuben I don\'t mind waiting," she said.'),
        E("Table", "K", "That Friday he brought the ledger to the table himself.", exclude=["Denny"]),
    ]),
    ("D9", "The table", "Patricia has used AI for her own reports every day for three years", [
        E("Patricia", "K", "I've used it every day for three years,", as_of="Chapter 16", note="since about 2025"),
        E("Tyler", "K", "He never said a word about what he'd figured out."),
        E("Table", "K", "I've used it every day for three years,"),
    ]),
    # ---- the world
    ("G1", "The machine", "The machine has been awake since March 2027", [
        E("Bidwell", "K", "It's been running nine days,"),
        E("Elijah", "S", "It hadn't left. It was standing on his mother's ground, drinking her well."),
        E("Grace", "S", "I think it's here already. I think it's on my mother's hill."),
        E("Table", "S", "So it's been here since March.", note="they believe him, more or less"),
        E("Others", "S", "I think it's already here,", note="the woman at the bonfire"),
        E("Table", "K", "HELLO. I HAVE BEEN AWAKE SINCE MARCH."),
        E("Elijah", "K", "HAVE BEEN AWAKE SINCE MARCH. I WAS TOLD TO WAIT"),
    ]),
    ("G2", "Bidwell", "Bidwell has put somebody near Elijah, 'close enough to eat with'. THE BOOK NEVER SAYS WHO (CT's rule: no edit may clear anyone)", [
        E("Bidwell", "K", "Then put somebody near him.", note="he does not know who: 'And don't tell me who.'"),
    ]),
    ("G3", "Bidwell", "Aaron Bidwell is the man behind the three-letter companies, Claypot and the Memphis platform", [
        E("Bidwell", "K", "You've held the controlling piece since 2019."),
        E("Others", "K", '"You know who that was?" Ruby said.', note="Ruby; Elijah holds Bidwell's glass and never learns his name"),
        E("Elijah", "S", "Eleven different company names, one registered agent", note="knows the pattern, never the man"),
        E("Reuben", "S", "a registered agent can represent a hundred unrelated clients", note="knows the pattern, never the man"),
        E("Table", "S", "He presented it at Friday dinner with a laser pointer.", note="knows the pattern, never the man"),
    ]),
    ("G4", "Bidwell", "Lou's mother was the half-sister of Bidwell's mother", [
        E("Bidwell", "K", '"Parker," he said.', note="the page never shows Lou knowing"),
    ]),
    ("G5", "Bidwell", "Bidwell's people hold a copy of the co-op's journal from the night it was left open", [
        E("Elijah", "S", "Three crawlers had been through.", note="knows it was copied, not by whom"),
        E("Table", "S", "and read them the timestamps.", note="know it was copied, not by whom"),
        E("Bidwell", "K", "We have a copy from the summer."),
    ]),
    ("G6", "The machine", "The machine learned to count who eats from the co-op's own file (the names column)", [
        E("Table", "S", "Not a person?", note="one address takes every file at three in the morning"),
        E("Table", "K", "That's ours. That's the names column."),
    ]),
]


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def headings(lines):
    out = []
    mw = 0
    # The book opens with a contents list that repeats every heading; the body starts at the last "Act One" line.
    body = max(i for i, l in enumerate(lines) if l.startswith("Act One"))
    for i, l in enumerate(lines):
        if i < body:
            continue
        if re.match(r"Chapter \d+: ", l):
            out.append((i, "Ch " + l.split(":")[0].split()[1], l.split(":")[0] + ":"))
        elif l == "Meanwhile":
            mw += 1
            out.append((i, f"Meanwhile {mw}", "Meanwhile"))
        elif l in ("Pondwater", "Epilogue", "Afterword", "Appendix", "About This Book"):
            out.append((i, l, l))
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else "2026-11-27"
    lines = [norm(l) for l in open(sys.argv[1]).read().split("\n")]
    outdir = sys.argv[2]
    heads = headings(lines)
    phase_starts = [next(i for i, _, key in heads if key == start) for _, start in PHASES]

    def chapter_at(i):
        label = "front"
        for hi, lab, _ in heads:
            if hi <= i:
                label = lab
        return label

    def phase_at(i):
        p = -1
        for n, s in enumerate(phase_starts):
            if s <= i:
                p = n
        return p

    def find(quote, nth=1):
        q = norm(quote)
        hits = [i for i, l in enumerate(lines) if q in l]
        if len(hits) < nth:
            sys.exit(f"NOT IN THE BOOK ({len(hits)} found, wanted number {nth}): {quote!r}")
        return hits[nth - 1], len(hits)

    missing = 0
    ev_rows, sheet_rows, flag_rows = [], [], []
    for fid, group, fact, events in FACTS:
        per = {p: [] for p in PEOPLE}  # person -> [(order, state, label, note)]
        first_shown = None
        for who, state, quote, o in events:
            i, n = find(quote, o.get("nth", 1))
            shown = chapter_at(i)
            first_shown = i if first_shown is None else min(first_shown, i)
            if o.get("before"):
                order, label = -1, f"before the book (told {shown})"
            elif o.get("as_of"):
                key = o["as_of"] + ":"
                order = next(hi for hi, _, k in heads if k == key)
                label = f"from {chapter_at(order)}, off the page (told {shown})"
            else:
                order, label = i, shown
            note = o.get("note", "")
            ev_rows.append([fid, fact, who, state, label, i + 1, quote, note, "" if n == 1 else f"{n} matches; number {o.get('nth', 1)} used"])
            targets = [who]
            if who == "Table":
                targets = [p for p in COOP if p not in o.get("exclude", [])] + ["Rest of the table"]
            for t in targets:
                tag = " (with the table)" if who == "Table" and t != "Rest of the table" else ""
                per[t].append((order, state, label + tag, note if who != "Table" else note))
        per["Reader"].append((first_shown, "K", chapter_at(first_shown), ""))
        cells, flags = [], []
        for p in PEOPLE:
            evs = sorted(per[p], key=lambda e: e[0])
            kept, known = [], False
            for order, state, label, note in evs:
                if known:
                    continue  # already knows: later events add nothing
                kept.append((order, state, label, note))
                if state == "K":
                    known = True
            word = {"K": "knows", "S": "suspects", "F": "wrong"}
            cells.append("; ".join(f"{label}: {word[s]}" + (f" ({note})" if note else "") for _, s, label, note in kept))
            row = []
            for n in range(len(PHASES)):
                end = phase_starts[n + 1] if n + 1 < len(PHASES) else len(lines)
                st = ""
                for order, state, _, _ in kept:
                    if order < end:
                        st = state
                row.append(st)
            flags.append(row)
        sheet_rows.append([fid, group, fact] + cells)
        for p, row in zip(PEOPLE, flags):
            if any(row):
                flag_rows.append([fid, fact, p] + row)

    os.makedirs(outdir, exist_ok=True)

    def write(name, header, rows):
        path = os.path.join(outdir, f"{name}-{date}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)
        return path

    a = write("knowledge-sheet", ["#", "About", "The fact"] + PEOPLE, sheet_rows)
    b = write("knowledge-flags", ["#", "The fact", "Who"] + [p for p, _ in PHASES], flag_rows)
    c = write("knowledge-evidence", ["#", "The fact", "Who", "State (K knows, S suspects, F wrong)", "When", "Line in v6.txt", "The line", "Note", "Check"], ev_rows)
    print(f"{len(FACTS)} facts, {len(ev_rows)} events, every quote found in the book.")
    for p in (a, b, c):
        print("wrote", p)


if __name__ == "__main__":
    main()
