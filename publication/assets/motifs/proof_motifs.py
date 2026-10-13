"""Render reproducible review sheets and inspect original SVG geometry.

Requires the existing Playwright installation and Chromium. Does not install
dependencies or alter browser profiles. All outputs stay beside the SVGs.
"""

from pathlib import Path
from xml.sax.saxutils import escape
import json
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent


def proof_html(assets):
    cards = []
    for item in assets:
        cards.append(
            f'<figure><div><img src="{item["file"]}"><img src="{item["monochrome"]}"></div>'
            f'<figcaption>{escape(item["title"])} · each drawing 2 inches wide</figcaption></figure>'
        )
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><title>Print-size motif proof</title>
<style>@page{size:8.5in 11in;margin:.6in}*{box-sizing:border-box}body{margin:0;background:white;color:#202c28;font:11px Georgia,serif}h1{font-size:20px;font-weight:normal;margin:0 0 10px}p{margin:0 0 15px}main{display:grid;grid-template-columns:1fr 1fr;gap:20px 14px}figure{margin:0;break-inside:avoid}figure div{display:flex;gap:8px}img{width:2in;height:1.3in;display:block}figcaption{font-size:9px;padding-top:6px;text-align:center}@media screen{body{padding:35px;width:900px}}@media print{main{display:block}figure{width:100%;margin-bottom:18px}figure div{justify-content:center}figcaption{font-size:8px}}
</style><h1>Original motif proof</h1><p>Color and single-ink alternatives. Every drawing is placed 2 inches wide, including in the PDF proof.</p><main>'''+"\n".join(cards)+"</main></html>"


def main():
    data = json.loads((BASE / "manifest.json").read_text())
    (BASE / "print-size-proof.html").write_text(proof_html(data["assets"]), encoding="utf-8")
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width":1120,"height":1260}, device_scale_factor=1.5)
        page.goto((BASE / "contact-sheet.html").as_uri(), wait_until="networkidle")
        assert page.locator("img").evaluate_all("(a)=>a.every(x=>x.complete && x.naturalWidth===400)")
        page.screenshot(path=str(BASE / "contact-sheet.png"), full_page=True)
        page.goto((BASE / "print-size-proof.html").as_uri(), wait_until="networkidle")
        assert page.locator("img").evaluate_all("(a)=>a.every(x=>x.complete && x.naturalWidth===400)")
        page.screenshot(path=str(BASE / "print-size-proof.png"), full_page=True)
        page.pdf(path=str(BASE / "print-size-proof.pdf"), print_background=True, prefer_css_page_size=True)
        for item in data["assets"]:
            page.goto((BASE / item["file"]).as_uri(), wait_until="load")
            box = page.locator("svg > g").evaluate("g=>{const b=g.getBBox();return {x:b.x,y:b.y,width:b.width,height:b.height}}")
            assert box["x"] >= 25 and box["y"] >= 25, item["file"]
            assert box["x"]+box["width"] <= 375 and box["y"]+box["height"] <= 238, item["file"]
            results.append({"file":item["file"],"geometry_bounds":box})
        browser.close()
    (BASE / "proof-results.json").write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8")
    print(f"Rendered both review sheets and measured {len(results)} drawings.")


if __name__ == "__main__":
    main()
