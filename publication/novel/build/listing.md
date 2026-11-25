# KDP listing: Surviving the Singularity ({{VERSION}})

Copy and paste from here into the KDP setup pages. Numbers are filled in by the build.

## Book details

- **Title:** Surviving the Singularity
- **Subtitle:** A Solarpunk Novel
- **Author:** Christopher Tavolazzi
- **Language:** English
- **Publishing rights:** I own the copyright and hold the necessary publishing rights.
- **Primary audience:** no sexually explicit images or title. Reading age: leave blank (adult fiction, strong language).

## Description

The approved back cover copy:

{{BACK}}

## Keywords (7)

1. solarpunk novel
2. artificial intelligence fiction
3. near future science fiction
4. hopeful science fiction
5. technological singularity
6. automation and job loss
7. cooperative farm community

## Categories (KDP allows 3; pick the closest names it offers)

1. Science Fiction > Hard Science Fiction
2. Literature & Fiction > Literary Fiction
3. Science Fiction > Post-Apocalyptic or Dystopian is NOT a fit; if KDP offers "Solarpunk", "Climate Fiction" or "Technothrillers", take the closest of those as the third.

## About the author (also for Amazon Author Central)

{{BIO}}

## Back cover

Same text as the description above, set on the cover with the author photo, two lines about the author and the barcode box.

## Paperback settings

- Trim 6 x 9 in, no bleed, black ink, {{PAPER}} paper. Cover finish (matte or glossy) is your pick.
- Interior: `surviving-the-singularity-{{VERSION}}-print-6x9.pdf`, {{PAGES}} pages.
- Cover: `surviving-the-singularity-{{VERSION}}-paperback-cover.pdf`, {{WRAP}} in, spine {{SPINE}} in. KDP adds the barcode to the lower right of the back.
- Estimate, KDP US black ink ($1.00 + $0.012 a page, from memory of KDP's published rates; confirm in KDP's calculator): about ${{COST}} to print, so the lowest list price at 60% royalty is about ${{MIN}}.
- Large print ({{LP_PAGES}} pages, spine {{LP_SPINE}} in): about ${{LP_COST}} to print, lowest list price about ${{LP_MIN}}. Tick "Large print" on its own listing; it needs its own ISBN.

## Kindle settings

- Manuscript: `surviving-the-singularity-{{VERSION}}-kindle.epub`. Cover: `surviving-the-singularity-{{VERSION}}-kindle-cover.jpg` (1600 x 2560).
- No ISBN needed. DRM is your pick and cannot be changed later.

## ISBN, when you buy it

- In the US, ISBNs come from Bowker (myidentifiers.com). You do not send them the manuscript. You fill in a form: title, author, format, publication date, price.
- One ISBN per format: one for the paperback, a second if you publish the large print. The Kindle edition does not need one.
- Put the number in `publication/novel/build/book.json` under `isbn` and rebuild; it then prints on the copyright page. Type the same number, and the same imprint name you gave Bowker, into KDP.

## The AI question KDP asks

KDP asks whether text, images or translations are AI-generated. By its rules, AI-assisted work (your writing, edited or checked with AI) does not have to be declared, and AI-generated work does, even if you edited it afterward. "About This Book" says how you made the text. The cover art is a separate answer: if an image generator made it, declare the images.
