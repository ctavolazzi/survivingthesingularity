#!/usr/bin/env python3
"""Generate the free-sample PDF for Surviving the Singularity.

Bundles the Introduction + Chapter 1 markdown into a single PDF
with a cover page, written to static/StS-free-sample.pdf.

Usage (from project root):
    python3 scripts/generate_sample_pdf.py

Deps: weasyprint, markdown (both confirmed available).
"""
from __future__ import annotations

from pathlib import Path

import markdown
from weasyprint import HTML, CSS

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "src" / "lib" / "data" / "book"
COVER_IMG = ROOT / "static" / "Surviving-the-Singularity-Cover.png"
OUT_PDF = ROOT / "static" / "StS-free-sample.pdf"

SAMPLE_FILES = [
    ("02-introduction.md", "Introduction"),
    ("03-chapter1.md", "Chapter 1"),
]

CSS_STYLES = """
@page {
    size: Letter;
    margin: 1in 1in 1.25in 1in;
    @bottom-center {
        content: "Surviving the Singularity  ·  Free Sample  ·  survivingthesingularity.com/book";
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 9pt;
        color: #6b7280;
    }
    @bottom-right {
        content: counter(page);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 9pt;
        color: #6b7280;
    }
}
@page :first {
    margin: 0;
    @bottom-center { content: ""; }
    @bottom-right { content: ""; }
}

html { font-size: 12pt; }
body {
    font-family: Georgia, 'Times New Roman', serif;
    color: #111827;
    line-height: 1.55;
}

/* === COVER PAGE === */
.cover {
    page: first;
    background: #020617;
    color: #f1f5f9;
    height: 100vh;
    padding: 1.5in 1in;
    page-break-after: always;
    display: block;
    position: relative;
}
.cover-inner {
    text-align: center;
}
.cover-badge {
    display: inline-block;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.6);
    padding: 0.3em 0.9em;
    border-radius: 999px;
    margin-bottom: 1.4em;
}
.cover-cover-image {
    width: 2.4in;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    margin: 0.5em auto 1.2em;
    display: block;
}
.cover-title {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 30pt;
    font-weight: 800;
    margin: 0 0 0.3em;
    background: linear-gradient(135deg, #f1f5f9 0%, #f59e0b 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    line-height: 1.1;
}
.cover-sub {
    font-size: 13pt;
    color: #cbd5e1;
    font-style: italic;
    margin: 0 0 1.2em;
}
.cover-byline {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 11pt;
    color: #94a3b8;
    margin: 0 0 2em;
}
.cover-byline strong {
    color: #f1f5f9;
    font-weight: 600;
}
.cover-meta {
    position: absolute;
    bottom: 1in;
    left: 1in;
    right: 1in;
    text-align: center;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 9pt;
    color: #64748b;
    border-top: 1px solid rgba(148, 163, 184, 0.2);
    padding-top: 1em;
}
.cover-meta a { color: #f59e0b; text-decoration: none; }

/* === CONTENT === */
.section {
    page-break-before: always;
}
h1 {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 22pt;
    color: #111827;
    margin: 0 0 0.4em;
    line-height: 1.15;
}
h1 .eyebrow {
    display: block;
    font-size: 10pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #b45309;
    font-weight: 600;
    margin-bottom: 0.4em;
}
h2 {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 16pt;
    color: #111827;
    margin: 1.4em 0 0.4em;
}
h3 {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 13pt;
    color: #111827;
    margin: 1.1em 0 0.3em;
}
p {
    margin: 0 0 0.85em;
    text-align: justify;
    hyphens: auto;
}
blockquote {
    margin: 1em 0;
    padding: 0.4em 1em;
    border-left: 3px solid #f59e0b;
    color: #374151;
    font-style: italic;
}
ul, ol { margin: 0 0 1em 1.25em; }
li { margin-bottom: 0.4em; }
code {
    font-family: 'Menlo', 'JetBrains Mono', monospace;
    font-size: 0.9em;
    background: #f3f4f6;
    padding: 0.1em 0.35em;
    border-radius: 3px;
}
pre {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.8em 1em;
    overflow-x: auto;
    font-family: 'Menlo', 'JetBrains Mono', monospace;
    font-size: 9.5pt;
    line-height: 1.4;
}
hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1.5em 0;
}
a { color: #b45309; }

/* End-of-sample CTA */
.cta-end {
    page-break-before: always;
    padding: 1in 0.5in;
    text-align: center;
}
.cta-end h2 {
    font-size: 20pt;
    margin-bottom: 0.5em;
}
.cta-end p {
    font-size: 12pt;
    color: #4b5563;
    margin-bottom: 1.5em;
    text-align: center;
}
.cta-button {
    display: inline-block;
    padding: 0.7em 1.6em;
    background: #f59e0b;
    color: #1a0f00 !important;
    text-decoration: none;
    border-radius: 6px;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: 700;
    font-size: 11pt;
}
"""


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def main() -> None:
    md = markdown.Markdown(
        extensions=["extra", "smarty", "sane_lists"],
        output_format="html5",
    )

    cover_uri = COVER_IMG.as_uri() if COVER_IMG.exists() else ""
    cover_html = (
        f'<img class="cover-cover-image" src="{cover_uri}" alt="Cover" />'
        if cover_uri
        else ""
    )

    sections_html = []
    for filename, label in SAMPLE_FILES:
        path = BOOK_DIR / filename
        if not path.exists():
            print(f"WARNING: missing {path}")
            continue
        raw = strip_frontmatter(path.read_text(encoding="utf-8"))
        body_html = md.reset().convert(raw)
        sections_html.append(
            f'<section class="section">'
            f"<h1><span class=\"eyebrow\">{label}</span></h1>"
            f"{body_html}"
            f"</section>"
        )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Surviving the Singularity — Free Sample</title>
</head>
<body>

<div class="cover">
    <div class="cover-inner">
        <div class="cover-badge">Free Sample</div>
        {cover_html}
        <h1 class="cover-title">Surviving the Singularity</h1>
        <p class="cover-sub">A field manual for the people who refuse to be passive cargo when AI rewrites the world.</p>
        <p class="cover-byline">by <strong>Christopher Tavolazzi</strong></p>
    </div>
    <div class="cover-meta">
        Includes the Introduction + Chapter 1.<br>
        Full book and updates at <a href="https://survivingthesingularity.com/book">survivingthesingularity.com/book</a>
    </div>
</div>

{''.join(sections_html)}

<div class="cta-end">
    <h2>Liked what you read?</h2>
    <p>
        New chapters land as I write them. Get notified when the full book ships,
        and read the rest of the open draft for free.
    </p>
    <a class="cta-button" href="https://survivingthesingularity.com/book">Read the full open draft →</a>
    <p style="margin-top: 2em; font-size: 9.5pt; color: #9ca3af;">
        © Christopher Tavolazzi · survivingthesingularity.com
    </p>
</div>

</body>
</html>"""

    HTML(string=full_html, base_url=str(ROOT)).write_pdf(
        target=str(OUT_PDF),
        stylesheets=[CSS(string=CSS_STYLES)],
    )
    size_kb = OUT_PDF.stat().st_size // 1024
    print(f"wrote {OUT_PDF} ({size_kb} KB)")


if __name__ == "__main__":
    main()
